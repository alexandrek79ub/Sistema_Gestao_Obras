#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Geração do Caderno de FVS (Fichas de Verificação de Serviço) Bloqueantes.
Arquitetura Modular v2.0 Lean (Manual de Boas Práticas §2).

Uso:
    python scripts/gerar_fvs_bloqueantes.py --obra OBRA_TMULT
    python scripts/gerar_fvs_bloqueantes.py --dir projetos/OBRA_TMULT
"""

import os
import sys
import json
import openpyxl
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.common.obra_io import (
    parse_obra_args, resolver_obra_dir, carregar_config_obra, salvar_markdown, ROOT_DIR
)
from scripts.common.excel_theme import (
    NAVY, BLUE_DARK, RED_FILL, ZEBRA_LIGHT,
    FONT_TITLE, FONT_HEADER, FONT_BOLD, FONT_REGULAR, FONT_RED,
    THIN_BORDER, ALIGN_CENTER, ALIGN_LEFT
)

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates", "qualidade")
CATALOGO_FVS_PATH = os.path.join(ROOT_DIR, "apoio", "catalogo_fvs.json")


def carregar_definicoes_fvs():
    """Carrega catálogo auditável de definições de FVSs bloqueantes."""
    with open(CATALOGO_FVS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def gerar_fichas_individuais_fvs(output_dir, fvs_list, sigla, nome):
    """Gera os 8 arquivos individuais de FVS prontos para impressão e prancheta."""
    fvs_dir = os.path.join(output_dir, "FVS")
    os.makedirs(fvs_dir, exist_ok=True)

    with open(os.path.join(TEMPLATES_DIR, "template_fvs_individual.md"), "r", encoding="utf-8") as f:
        base_tmpl = f.read()

    for f in fvs_list:
        itens_md = "\n".join([
            f"- [ ] **Item {i+1:02d}:** {it}  \n  *Status:* [ ] C (Conforme) | [ ] NC (Não Conforme) | [ ] NA (Não Aplica) — *Obs:* ________________"
            for i, it in enumerate(f['itens_verificacao'])
        ])
        md_content = (base_tmpl
                      .replace("{{CODIGO}}", f['codigo'])
                      .replace("{{TITULO_UPPER}}", f['titulo'].upper())
                      .replace("{{NOME_OBRA}}", nome)
                      .replace("{{SIGLA_OBRA}}", sigla)
                      .replace("{{POP}}", f['pop'])
                      .replace("{{NBR}}", f['nbr'])
                      .replace("{{TOLERANCIA}}", f['tolerancia'])
                      .replace("{{ITENS_CHECKLIST}}", itens_md)
                      .replace("{{CONTRATO_BLOQUEADO}}", f['contrato_bloqueado'])
                      .replace("{{SERVICO_SUCESSOR_BLOQUEADO}}", f['servico_sucessor_bloqueado']))

        caminho_fvs = os.path.join(fvs_dir, f"{f['codigo']}_{f['titulo'].split(',')[0].replace(' ', '_').upper()}.md")
        with open(caminho_fvs, "w", encoding="utf-8") as file:
            file.write(md_content)


def gerar_caderno_mestre_fvs(output_dir, fvs_list, sigla, nome):
    """Compila o Caderno Mestre unificado de FVS Bloqueantes em Markdown."""
    caderno_path = os.path.join(output_dir, f"CADERNO_FVS_BLOQUEANTES_{sigla}.md")

    tabela_resumo = [
        f"| **{f['codigo']}** | {f['titulo']} | {f['nbr'].split('(')[0].strip()} | **{f['contrato_bloqueado']}** | {f['servico_sucessor_bloqueado']} |"
        for f in fvs_list
    ]

    detalhamento = []
    for f in fvs_list:
        itens_txt = "\n".join([f"  {idx+1}. {it}" for idx, it in enumerate(f['itens_verificacao'])])
        detalhamento.append(
            f"### 📌 {f['codigo']} — {f['titulo']}\n"
            f"* **Normas ABNT:** {f['nbr']}\n"
            f"* **Procedimentos POP:** {f['pop']}\n"
            f"* **Contrato Bloqueado em Caso de Reprovação:** `{f['contrato_bloqueado']}`\n"
            f"* **Serviço Sucessor Condicionado:** `{f['servico_sucessor_bloqueado']}`\n"
            f"* **Tolerâncias Rígidas:** {f['tolerancia']}\n"
            f"* **Checklist Mínimo:**\n{itens_txt}\n"
        )

    with open(os.path.join(TEMPLATES_DIR, "template_caderno_mestre_fvs.md"), "r", encoding="utf-8") as f:
        base_tmpl = f.read()

    conteudo = (base_tmpl
                .replace("{{NOME_UPPER}}", nome.upper())
                .replace("{{SIGLA_OBRA}}", sigla)
                .replace("{{TABELA_RESUMO_FVS}}", "\n".join(tabela_resumo))
                .replace("{{DETALHAMENTO_FVS}}", "\n".join(detalhamento)))

    with open(caderno_path, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return caderno_path


def construir_matriz_excel_fvs(output_dir, fvs_list, sigla, nome):
    """Gera matriz Excel com amarração visual entre FVS, NBR e bloqueios contratuais."""
    excel_path = os.path.join(output_dir, f"MATRIZ_BLOQUEIO_FVS_CONTRATOS_{sigla}.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title, ws.views.sheetView[0].showGridLines = "Matriz FVS e Bloqueios", True

    FONT_SUB = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    FONT_TH = Font(name="Calibri", size=10, bold=True, color="FFFFFF")

    # 1. Cabeçalho Principal
    ws.merge_cells("A1:G1")
    c1 = ws["A1"]
    c1.value, c1.font, c1.fill, c1.alignment = f"MATRIZ DE QUALIDADE, FVS E BLOQUEIOS CONTRATUAIS — {nome.upper()}", FONT_TITLE, NAVY, ALIGN_CENTER
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:G2")
    c2 = ws["A2"]
    c2.value, c2.font, c2.fill, c2.alignment = "Amarração Direta entre Inspeções em Campo, Tolerâncias NBR e Retenção de Medições de Empreiteiros", FONT_SUB, BLUE_DARK, ALIGN_CENTER
    ws.row_dimensions[2].height = 18

    # 2. Cabeçalhos de Colunas
    headers = [
        ("Código", 12), ("Disciplina Inspecionada", 30), ("Norma Técnica ABNT", 25),
        ("POP de Referência", 25), ("Tolerância Dimensional Normativa", 45),
        ("Contrato Financeiramente Bloqueado", 25), ("Serviço Sucessor Condicionado", 35)
    ]
    for col_idx, (h_text, width) in enumerate(headers, start=1):
        cell = ws.cell(row=3, column=col_idx, value=h_text)
        cell.font, cell.fill, cell.border = FONT_TH, BLUE_DARK, THIN_BORDER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(col_idx)].width = width
    ws.row_dimensions[3].height = 28

    # 3. Linhas de Dados
    for row_idx, f in enumerate(fvs_list, start=4):
        ws.cell(row=row_idx, column=1, value=f['codigo']).font = FONT_BOLD
        ws.cell(row=row_idx, column=1).alignment = ALIGN_CENTER
        ws.cell(row=row_idx, column=2, value=f['titulo']).font = FONT_BOLD
        ws.cell(row=row_idx, column=3, value=f['nbr'])
        ws.cell(row=row_idx, column=4, value=f['pop'])

        c_tol = ws.cell(row=row_idx, column=5, value=f['tolerancia'])
        c_tol.alignment = Alignment(wrap_text=True)

        c_bloq = ws.cell(row=row_idx, column=6, value=f['contrato_bloqueado'])
        c_bloq.font, c_bloq.fill, c_bloq.alignment = FONT_RED, RED_FILL, ALIGN_CENTER

        c_suc = ws.cell(row=row_idx, column=7, value=f['servico_sucessor_bloqueado'])
        c_suc.alignment = Alignment(wrap_text=True)

        for col in range(1, 8):
            cell = ws.cell(row=row_idx, column=col)
            cell.border = THIN_BORDER
            if row_idx % 2 == 1 and col != 6:
                cell.fill = ZEBRA_LIGHT
        ws.row_dimensions[row_idx].height = 45

    wb.save(excel_path)
    return excel_path


def main():
    args = parse_obra_args("Motor Universal de FVSs Bloqueantes de Campo.")
    obra_dir = resolver_obra_dir(args)
    config = carregar_config_obra(obra_dir)
    sigla = config.get("sigla_obra", "OBRA")
    nome = config.get("nome_obra", sigla)

    print(f"\n=======================================================")
    print(f"🛡️ MOTOR UNIVERSAL DE QUALIDADE DE CAMPO E FVS")
    print(f"=======================================================")
    print(f"📂 Diretório da Obra: {obra_dir}")
    print(f"🏗️  Obra Ativa: {nome} ({sigla})")

    output_dir = os.path.join(obra_dir, "04_PRODUCAO_E_AVANCO")
    os.makedirs(output_dir, exist_ok=True)

    fvs_list = carregar_definicoes_fvs()

    print(f"\n[1/3] Gerando 8 Fichas Individuais de Verificação de Serviço em 04_PRODUCAO_E_AVANCO/FVS/...")
    gerar_fichas_individuais_fvs(output_dir, fvs_list, sigla, nome)
    print(f"      ✅ 8 FVSs estruturadas em Markdown prontas para impressão e prancheta")

    print(f"\n[2/3] Compilando Caderno Mestre CADERNO_FVS_BLOQUEANTES_{sigla}.md...")
    caderno_path = gerar_caderno_mestre_fvs(output_dir, fvs_list, sigla, nome)
    print(f"      ✅ Caderno Mestre gerado: {caderno_path}")

    print(f"\n[3/3] Construindo Matriz Visual MATRIZ_BLOQUEIO_FVS_CONTRATOS_{sigla}.xlsx...")
    excel_path = construir_matriz_excel_fvs(output_dir, fvs_list, sigla, nome)
    print(f"      ✅ Planilha Excel gerada: {excel_path}")
    print(f"\n✨ Motor de FVSs Bloqueantes concluído com 100% de sucesso!")


if __name__ == "__main__":
    main()
