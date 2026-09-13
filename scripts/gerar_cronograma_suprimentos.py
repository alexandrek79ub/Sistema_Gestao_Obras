#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Planejamento de Suprimentos & Contratações Multi-Obra
Ecossistema de Gestão de Obras & PMO Virtual — v2.0 Lean

Gera com precisão determinística:
1. CRONOGRAMA_MESTRE_SUPRIMENTOS_[SIGLA].md  (Materiais & Equipamentos na Linha de Base)
2. CRONOGRAMA_MESTRE_SUPRIMENTOS_[SIGLA].xlsx (Planilha executiva multi-abas via OpenPyXL)
3. PLANO_CONTRATACAO_EMPREITEIROS_[SIGLA].md  (Subcontratações baseadas no Histograma)
4. CATALOGO_COMPLETO_REQUISICOES_COMPRA_[SIGLA].md (RCs com UCC, EAP e Centros de Custo)

Dados externos (sem hardcode no Python):
- apoio/catalogo_suprimentos.json   → regras de lead time, alçadas e diretrizes de governança
- scripts/templates/suprimentos/    → textos fixos dos documentos Markdown

Alinhado a:
- POP 05 (Solicitação de Compras e Suprimentos)
- POP 06 (Recebimento de Materiais)
- SKILL GESTÃO 03 (Alçadas de Aprovação e Governança)
- Linha de Base e Orçamento Consolidado

Uso:
    python scripts/gerar_cronograma_suprimentos.py --obra OBRA_TMULT
    python scripts/gerar_cronograma_suprimentos.py --obra RESIDENCIAL_ALPHA
"""

import os
import sys
import json
import argparse
from datetime import datetime

import openpyxl
from openpyxl.utils import get_column_letter

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Caminhos base do ecossistema
# ---------------------------------------------------------------------------

BASE_REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APOIO_DIR     = os.path.join(BASE_REPO_DIR, "apoio")
TPL_DIR       = os.path.join(BASE_REPO_DIR, "scripts", "templates", "suprimentos")

# ---------------------------------------------------------------------------
# Importar helpers corporativos (com fallback)
# ---------------------------------------------------------------------------

sys.path.insert(0, os.path.join(BASE_REPO_DIR, "scripts", "common"))
try:
    from excel_theme import (
        NAVY, BLUE_DARK,
        FONT_TITLE_WHITE, FONT_HEADER_WHITE, FONT_BOLD_NAVY,
        BORDER_THIN, BORDER_TOTAL,
        FILL_GRAY_LIGHT, FILL_SUBTITLE,
        aplicar_larguras_colunas, aplicar_freeze,
    )
    _THEME_OK = True
except ImportError:
    _THEME_OK = False

if not _THEME_OK:
    from openpyxl.styles import Font, PatternFill, Border, Side
    NAVY            = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    BLUE_DARK       = PatternFill(start_color="203A43", end_color="203A43", fill_type="solid")
    FILL_GRAY_LIGHT = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
    FILL_SUBTITLE   = BLUE_DARK
    FONT_TITLE_WHITE  = Font(name="Calibri", size=13, bold=True,  color="FFFFFF")
    FONT_HEADER_WHITE = Font(name="Calibri", size=10, bold=True,  color="FFFFFF")
    FONT_BOLD_NAVY    = Font(name="Calibri", size=10, bold=True,  color="1B365D")
    _s = Side(style="thin",   color="DDDDDD")
    _h = Side(style="thin",   color="1B365D")
    _d = Side(style="double", color="1B365D")
    BORDER_THIN  = Border(left=_s, right=_s, top=_s, bottom=_s)
    BORDER_TOTAL = Border(top=_h, bottom=_d)

    def aplicar_larguras_colunas(ws, larguras):
        for col, w in larguras.items():
            ws.column_dimensions[col].width = w

    def aplicar_freeze(ws, cell):
        ws.freeze_panes = cell

from openpyxl.styles import Alignment, Font

# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _ler_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _ler_template(nome: str) -> str:
    path = os.path.join(TPL_DIR, nome)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Template não encontrado: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _fmt_brl(valor: float) -> str:
    """Formata float como R$ 1.234,56."""
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")


def _salvar_md(path: str, conteudo: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"\u2705 Gerado: {os.path.basename(path)}")

def gerar_cronograma_suprimentos(obra_nome=None, custom_dir=None):

    # --- 1. Resolver diretório da obra ---
    if custom_dir:
        proj_dir = os.path.abspath(custom_dir)
        obra_id  = os.path.basename(proj_dir)
    elif obra_nome:
        proj_dir = os.path.join(BASE_REPO_DIR, "projetos", obra_nome)
        obra_id  = obra_nome
    else:
        raise ValueError("É necessário especificar --obra [NOME_OBRA] ou --dir [CAMINHO].")

    if not os.path.exists(proj_dir):
        raise FileNotFoundError(f"Diretório da obra não encontrado: {proj_dir}")

    # --- 2. Carregar config_obra.json ---
    config_path = os.path.join(proj_dir, "config_obra.json")
    config      = _ler_json(config_path) if os.path.exists(config_path) else {}

    nome_obra   = config.get("nome_obra",          obra_id)
    sigla_obra  = config.get("sigla_obra",          obra_id)
    area_m2     = config.get("area_construida_m2", "N/A")
    prazo_meses = float(config.get("prazo_meses",  6.0))

    sup_dir = os.path.join(proj_dir, "05_SUPRIMENTOS_E_FINANCEIRO")
    os.makedirs(sup_dir, exist_ok=True)

    # --- 3. Carregar catálogo global de suprimentos (apoio/catalogo_suprimentos.json) ---
    cat_sup_path = os.path.join(APOIO_DIR, "catalogo_suprimentos.json")
    catalogo_sup = _ler_json(cat_sup_path) if os.path.exists(cat_sup_path) else {}

    diretrizes_sub_raw  = catalogo_sup.get("diretrizes_governanca_subcontratos", [])
    instrucoes_comp_raw = catalogo_sup.get("instrucoes_compradores_almoxarifado", [])

    # Renderizar listas como Markdown numerado
    diretrizes_sub_md  = "\n".join(
        f"{i+1}. {item}" for i, item in enumerate(diretrizes_sub_raw)
    )
    instrucoes_comp_md = "\n".join(
        f"{i+1}. {item.replace('{SIGLA_OBRA}', sigla_obra)}"
        for i, item in enumerate(instrucoes_comp_raw)
    )

    # --- 4. Carregar catálogos de dados da obra ---
    def _carregar_catalogo_obra(nome_arquivo: str, template_fallback: str) -> list:
        path = os.path.join(sup_dir, nome_arquivo)
        if not os.path.exists(path):
            tpl = os.path.join(BASE_REPO_DIR, "projetos", "_TEMPLATE_OBRA_NOVA",
                               "05_SUPRIMENTOS_E_FINANCEIRO", template_fallback)
            return _ler_json(tpl) if os.path.exists(tpl) else []
        return _ler_json(path)

    materiais    = _carregar_catalogo_obra("catalogo_materiais_rc.json",
                                           "catalogo_materiais_rc.template.json")
    equipamentos = _carregar_catalogo_obra("catalogo_equipamentos_re.json",
                                            "catalogo_equipamentos_re.template.json")
    sub_file     = os.path.join(sup_dir, "plano_subcontratos.json")
    subcontratos = _ler_json(sub_file) if os.path.exists(sub_file) else []

    total_materiais = sum(float(m.get("cd_orcado", 0.0)) for m in materiais)

    print(f"\n{'='*80}")
    print(f"🚀 MOTOR UNIVERSAL DE SUPRIMENTOS v2.0 Lean: {sigla_obra}")
    print(f"📂 Saída : {sup_dir}")
    print(f"📋 Cat.  : {cat_sup_path}")
    print(f"📦 Pacotes: {len(materiais)} Materiais | {len(equipamentos)} Equipamentos | {len(subcontratos)} Subcontratos")
    print("="*80)

    data_atual = datetime.now().strftime("%d/%m/%Y")

    # =========================================================================
    # 5. Cronograma Mestre de Suprimentos — MARKDOWN (via template)
    # =========================================================================
    tpl_crono = _ler_template("template_cronograma_mestre_suprimentos.md")

    linhas_mat = []
    for m in materiais:
        linhas_mat.append(
            f"| **{m['rc']}** | {m['pacote']} | `{m['cc']}` | {m['qtd_ucc']} "
            f"| {m['data_gatilho_rc']} | {m['data_pc']} | **{m['data_obra']}** "
            f"| `{m.get('semana', '-')}` | {m['lead_dias']}d | {_fmt_brl(float(m.get('cd_orcado', 0.0)))} "
            f"| {m.get('criterio_pop06', '-')} |"
        )
    tabela_materiais = "\n".join(linhas_mat) if linhas_mat else "_Nenhum material cadastrado._"

    linhas_eq = []
    for eq in equipamentos:
        linhas_eq.append(
            f"| `{eq['item']}` | **{eq['nome']}** | {eq['qtd']} | {eq['und']} "
            f"| {eq['meses']} | `{eq['semanas']}` | `{eq['cc']}` | {eq['lead_dias']}d "
            f"| {eq['data_solic']} | **{eq['data_mobil']}** | {eq['data_desmob']} "
            f"| {eq['modalidade']} | {eq['fornecedor_alvo']} — *{eq['funcao']}* |"
        )
    tabela_equipamentos = "\n".join(linhas_eq) if linhas_eq else "_Nenhum equipamento cadastrado._"

    md_crono = (
        tpl_crono
        .replace("{{NOME_OBRA}}",             nome_obra)
        .replace("{{AREA_M2}}",               str(area_m2))
        .replace("{{PRAZO_MESES}}",           f"{prazo_meses:,.0f}")
        .replace("{{TOTAL_SEMANAS}}",         f"{prazo_meses * 4.33:.0f}")
        .replace("{{TOTAL_DIAS}}",            f"{prazo_meses * 30:.0f}")
        .replace("{{DATA_ATUAL}}",            data_atual)
        .replace("{{TOTAL_MATERIAIS}}",       str(len(materiais)))
        .replace("{{TABELA_MATERIAIS}}",      tabela_materiais)
        .replace("{{VALOR_TOTAL_MATERIAIS}}", _fmt_brl(total_materiais))
        .replace("{{TOTAL_EQUIPAMENTOS}}",    str(len(equipamentos)))
        .replace("{{TABELA_EQUIPAMENTOS}}",   tabela_equipamentos)
    )
    md_crono_path = os.path.join(sup_dir, f"CRONOGRAMA_MESTRE_SUPRIMENTOS_{sigla_obra}.md")
    _salvar_md(md_crono_path, md_crono)

    # =========================================================================
    # 6. Catálogo de Requisições de Compra — MARKDOWN (via template)
    # =========================================================================
    tpl_cat = _ler_template("template_catalogo_requisicoes_compra.md")

    linhas_rc = []
    for m in materiais:
        linhas_rc.append(
            f"| **{m['rc']}** | {m['pacote']} | `{m['cc']}` | `{m['eap']}` "
            f"| {m['qtd_ucc']} | {m['data_gatilho_rc']} | **{m['data_obra']}** "
            f"| {m['lead_dias']}d | {_fmt_brl(float(m.get('cd_orcado', 0.0)))} |"
        )
    tabela_rcs = "\n".join(linhas_rc) if linhas_rc else "_Nenhuma RC cadastrada._"

    md_cat = (
        tpl_cat
        .replace("{{SIGLA_OBRA}}",            sigla_obra)
        .replace("{{NOME_OBRA}}",             nome_obra)
        .replace("{{AREA_M2}}",               str(area_m2))
        .replace("{{TOTAL_MATERIAIS}}",       str(len(materiais)))
        .replace("{{TABELA_CATALOGO_RCS}}",   tabela_rcs)
        .replace("{{VALOR_TOTAL_MATERIAIS}}", _fmt_brl(total_materiais))
        .replace("{{INSTRUCOES_COMPRADORES}}", instrucoes_comp_md)
    )
    md_cat_path = os.path.join(sup_dir, f"CATALOGO_COMPLETO_REQUISICOES_COMPRA_{sigla_obra}.md")
    _salvar_md(md_cat_path, md_cat)

    # =========================================================================
    # 7. Plano de Contratação de Empreiteiros — MARKDOWN (via template)
    # =========================================================================
    md_sub_path = None
    if subcontratos:
        tpl_sub = _ler_template("template_plano_contratacao_empreiteiros.md")

        linhas_sub = []
        for s in subcontratos:
            linhas_sub.append(
                f"| `{s['cod']}` | **{s['nome']}** | {s['mes']} (`{s['semanas']}`) "
                f"| {s['pico']} | `{s['cc']}` | {s['medicao']} | {s['retencao']} "
                f"| {s['escopo']} |"
            )
        tabela_sub = "\n".join(linhas_sub)

        md_sub = (
            tpl_sub
            .replace("{{NOME_OBRA}}",              nome_obra)
            .replace("{{AREA_M2}}",                str(area_m2))
            .replace("{{DATA_ATUAL}}",             data_atual)
            .replace("{{TOTAL_SUBCONTRATOS}}",     str(len(subcontratos)))
            .replace("{{DIRETRIZES_SUBCONTRATOS}}", diretrizes_sub_md)
            .replace("{{TABELA_SUBCONTRATOS}}",    tabela_sub)
        )
        md_sub_path = os.path.join(sup_dir, f"PLANO_CONTRATACAO_EMPREITEIROS_{sigla_obra}.md")
        _salvar_md(md_sub_path, md_sub)

    # =========================================================================
    # 8. Excel multi-abas (OpenPyXL)
    # =========================================================================
    xlsx_path = os.path.join(sup_dir, f"CRONOGRAMA_MESTRE_SUPRIMENTOS_{sigla_obra}.xlsx")
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    def _cabecalho_aba(ws, titulo: str, subtitulo: str, n_cols: int) -> int:
        """Escreve as 2 linhas de cabeçalho padrão. Retorna a linha de início dos headers."""
        col_letra = get_column_letter(n_cols)
        ws.merge_cells(f"A1:{col_letra}1")
        ws["A1"] = titulo
        ws["A1"].font      = FONT_TITLE_WHITE
        ws["A1"].fill      = NAVY
        ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[1].height = 28
        ws.merge_cells(f"A2:{col_letra}2")
        ws["A2"] = subtitulo
        ws["A2"].font      = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
        ws["A2"].fill      = FILL_SUBTITLE
        ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[2].height = 20
        return 4

    def _escrever_header(ws, headers: list, linha: int):
        ws.row_dimensions[linha].height = 24
        for c_idx, h in enumerate(headers, start=1):
            c = ws.cell(row=linha, column=c_idx, value=h)
            c.font      = FONT_HEADER_WHITE
            c.fill      = NAVY
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            c.border    = BORDER_THIN

    # ---- Aba 1: Materiais ----
    ws_mat = wb.create_sheet(title="Materiais e Insumos")
    start_r = _cabecalho_aba(
        ws_mat,
        f"CRONOGRAMA MESTRE DE SUPRIMENTOS: MATERIAIS & INSUMOS ({sigla_obra})",
        f"{nome_obra} | Prazos de Gatilho vs Lead Time POP 05",
        11
    )
    headers_mat = [
        "Nº RC", "Pacote de Fornecimento", "Disciplina", "EAP Ref.", "Centro de Custo",
        "Qtd Comercial UCC", "Data Gatilho RC", "Data Emissão PC", "Data Entrega Obra",
        "Semana", "Custo Direto Base (R$)"
    ]
    _escrever_header(ws_mat, headers_mat, start_r)

    tot_mat_val = 0.0
    for idx, m in enumerate(materiais, start=start_r + 1):
        ws_mat.row_dimensions[idx].height = 20
        fill_alt = FILL_GRAY_LIGHT if idx % 2 == 0 else None

        def _c(col, val, align="center", bold=False):
            cell = ws_mat.cell(row=idx, column=col, value=val)
            cell.alignment = Alignment(horizontal=align)
            cell.border    = BORDER_THIN
            if bold:     cell.font = FONT_BOLD_NAVY
            if fill_alt: cell.fill = fill_alt

        _c(1,  m.get("rc", ""))
        _c(2,  m.get("pacote", ""),          "left")
        _c(3,  m.get("disciplina", ""),       "left")
        _c(4,  m.get("eap", ""))
        _c(5,  m.get("cc", ""))
        _c(6,  m.get("qtd_ucc", ""),          "right")
        _c(7,  m.get("data_gatilho_rc", ""))
        _c(8,  m.get("data_pc", ""))
        _c(9,  m.get("data_obra", ""),        "center", bold=True)
        _c(10, m.get("semana", "-"))
        val = float(m.get("cd_orcado", 0.0))
        c_val = ws_mat.cell(row=idx, column=11, value=val)
        c_val.number_format = '"R$ "#,##0.00'
        c_val.alignment = Alignment(horizontal="right")
        c_val.border    = BORDER_THIN
        if fill_alt: c_val.fill = fill_alt
        tot_mat_val += val

    # Linha de total
    tot_row = start_r + len(materiais) + 1
    ws_mat.row_dimensions[tot_row].height = 24
    ws_mat.merge_cells(start_row=tot_row, start_column=1, end_row=tot_row, end_column=10)
    t = ws_mat.cell(row=tot_row, column=1,
                    value=f"TOTAL CUSTO DIRETO DOS {len(materiais)} PACOTES DE MATERIAIS:")
    t.font      = FONT_BOLD_NAVY
    t.alignment = Alignment(horizontal="right", vertical="center")
    t.border    = BORDER_TOTAL
    c_tot = ws_mat.cell(row=tot_row, column=11, value=tot_mat_val)
    c_tot.number_format = '"R$ "#,##0.00'
    c_tot.font      = FONT_BOLD_NAVY
    c_tot.alignment = Alignment(horizontal="right")
    c_tot.border    = BORDER_TOTAL

    aplicar_larguras_colunas(ws_mat, {
        "A": 10, "B": 38, "C": 18, "D": 12, "E": 16,
        "F": 18, "G": 16, "H": 16, "I": 16, "J": 10, "K": 20
    })
    aplicar_freeze(ws_mat, "B5")

    # ---- Aba 2: Equipamentos ----
    ws_eq = wb.create_sheet(title="Equipamentos e Canteiro")
    _cabecalho_aba(
        ws_eq,
        f"CRONOGRAMA DE EQUIPAMENTOS & LOCAÇÕES ({sigla_obra})",
        f"{nome_obra} | Mobilização, Desmobilização e Lead Times POP 04",
        11
    )
    headers_eq = [
        "Item", "Equipamento / Instalação", "Tipo / Modelo", "Qtd", "Un",
        "Meses Atuação", "Semanas", "Centro de Custo", "Data Solicitação",
        "Data Mobilização", "Data Desmobilização"
    ]
    _escrever_header(ws_eq, headers_eq, 3)

    for idx, eq in enumerate(equipamentos, start=4):
        ws_eq.row_dimensions[idx].height = 20
        fill_alt = FILL_GRAY_LIGHT if idx % 2 == 0 else None

        def _eq(col, val, align="center", bold=False):
            cell = ws_eq.cell(row=idx, column=col, value=val)
            cell.alignment = Alignment(horizontal=align)
            cell.border    = BORDER_THIN
            if bold:     cell.font = FONT_BOLD_NAVY
            if fill_alt: cell.fill = fill_alt

        _eq(1,  eq.get("item", ""))
        _eq(2,  eq.get("nome", ""),         "left")
        _eq(3,  eq.get("tipo", ""),         "left")
        _eq(4,  eq.get("qtd", 1))
        _eq(5,  eq.get("und", "un"))
        _eq(6,  eq.get("meses", ""))
        _eq(7,  eq.get("semanas", ""))
        _eq(8,  eq.get("cc", ""))
        _eq(9,  eq.get("data_solic", ""))
        _eq(10, eq.get("data_mobil", ""),   "center", bold=True)
        _eq(11, eq.get("data_desmob", ""))

    aplicar_larguras_colunas(ws_eq, {
        "A": 8,  "B": 36, "C": 22, "D": 8,  "E": 8,
        "F": 14, "G": 14, "H": 16, "I": 16, "J": 18, "K": 18
    })
    aplicar_freeze(ws_eq, "B4")

    # ---- Aba 3: Subcontratos ----
    if subcontratos:
        ws_sub = wb.create_sheet(title="Plano de Empreiteiros")
        _cabecalho_aba(
            ws_sub,
            f"PLANO MESTRE DE CONTRATAÇÃO DE EMPREITEIROS ({sigla_obra})",
            f"{nome_obra} | Governança SST (POP 17) e Retenção Técnica (5%)",
            7
        )
        headers_sub = [
            "Cód.", "Pacote de Empreitada", "Período Atuação", "Pico Mão de Obra",
            "Centro de Custo", "Forma de Medição", "Regra de Retenção Técnica"
        ]
        _escrever_header(ws_sub, headers_sub, 3)

        for idx, sub in enumerate(subcontratos, start=4):
            ws_sub.row_dimensions[idx].height = 22
            fill_alt = FILL_GRAY_LIGHT if idx % 2 == 0 else None

            def _sub(col, val, align="center"):
                cell = ws_sub.cell(row=idx, column=col, value=val)
                cell.alignment = Alignment(horizontal=align)
                cell.border    = BORDER_THIN
                if fill_alt: cell.fill = fill_alt

            _sub(1, sub.get("cod", ""))
            _sub(2, sub.get("nome", ""),                               "left")
            _sub(3, f"{sub.get('mes', '')} ({sub.get('semanas', '')})")
            _sub(4, sub.get("pico", ""),                               "left")
            _sub(5, sub.get("cc", ""))
            _sub(6, sub.get("medicao", ""),                            "left")
            _sub(7, sub.get("retencao", ""),                           "left")

        aplicar_larguras_colunas(ws_sub, {
            "A": 10, "B": 36, "C": 22, "D": 24,
            "E": 16, "F": 28, "G": 30
        })
        aplicar_freeze(ws_sub, "B4")

    wb.save(xlsx_path)
    print(f"✅ Gerado: {os.path.basename(xlsx_path)}")

    # =========================================================================
    # Resumo final
    # =========================================================================
    print(f"\n{'='*80}")
    print(f"🏁 SUPRIMENTOS CONCLUÍDO — {sigla_obra}")
    print(f"   MD Cronograma  : {os.path.basename(md_crono_path)}")
    print(f"   MD Catálogo RC : {os.path.basename(md_cat_path)}")
    if md_sub_path:
        print(f"   MD Empreiteiros: {os.path.basename(md_sub_path)}")
    print(f"   XLSX           : {os.path.basename(xlsx_path)}")
    print("="*80)

    return {
        "status":              "sucesso",
        "md_crono":           md_crono_path,
        "xlsx_crono":         xlsx_path,
        "md_cat":             md_cat_path,
        "md_sub":             md_sub_path,
        "materiais_total":    len(materiais),
        "equipamentos_total": len(equipamentos),
        "subcontratos_total": len(subcontratos),
    }


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Motor Universal de Planejamento de Suprimentos v2.0 Lean"
    )
    parser.add_argument("--obra", help="Nome da pasta da obra em /projetos/ (ex: OBRA_TMULT)")
    parser.add_argument("--dir",  help="Caminho direto para a pasta da obra")
    args = parser.parse_args()

    if not args.obra and not args.dir:
        parser.print_help()
        sys.exit(1)

    gerar_cronograma_suprimentos(obra_nome=args.obra, custom_dir=args.dir)

