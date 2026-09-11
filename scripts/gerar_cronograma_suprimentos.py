#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Planejamento de Suprimentos & Contratações Multi-Obra
Ecossistema de Gestão de Obras & PMO Virtual

Gera com precisão determinística:
1. CRONOGRAMA_MESTRE_SUPRIMENTOS_[SIGLA].md (Materiais & Equipamentos integrados na Linha de Base)
2. CRONOGRAMA_MESTRE_SUPRIMENTOS_[SIGLA].xlsx (Planilha executiva multi-abas estilizada via OpenPyXL)
3. PLANO_CONTRATACAO_EMPREITEIROS_[SIGLA].md (Subcontratações baseadas no Histograma)
4. CATALOGO_COMPLETO_REQUISICOES_COMPRA_[SIGLA].md (As RCs com UCC, EAP e Centros de Custo)

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
import csv
import json
import argparse
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def gerar_cronograma_suprimentos(obra_nome=None, custom_dir=None):
    base_repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if custom_dir:
        proj_dir = os.path.abspath(custom_dir)
        obra_id = os.path.basename(proj_dir)
    elif obra_nome:
        proj_dir = os.path.join(base_repo_dir, "projetos", obra_nome)
        obra_id = obra_nome
    else:
        raise ValueError("É necessário especificar --obra [NOME_OBRA] ou --dir [CAMINHO].")

    if not os.path.exists(proj_dir):
        raise FileNotFoundError(f"Diretório da obra não encontrado: {proj_dir}")

    # 1. Carregar configuração da obra
    config_path = os.path.join(proj_dir, "config_obra.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {}

    nome_obra = config.get("nome_obra", obra_id)
    sigla_obra = config.get("sigla_obra", obra_id)
    area_m2 = config.get("area_construida_m2", "N/A")
    prazo_meses = config.get("prazo_meses", 6.0)

    sup_dir = os.path.join(proj_dir, "05_SUPRIMENTOS_E_FINANCEIRO")
    os.makedirs(sup_dir, exist_ok=True)

    # 2. Carregar catálogos de dados da obra
    mat_file = os.path.join(sup_dir, "catalogo_materiais_rc.json")
    if not os.path.exists(mat_file):
        tpl_mat = os.path.join(base_repo_dir, "projetos", "OBRA", "05_SUPRIMENTOS_E_FINANCEIRO", "catalogo_materiais_rc.template.json")
        if os.path.exists(tpl_mat):
            with open(tpl_mat, "r", encoding="utf-8") as f:
                materiais = json.load(f)
        else:
            materiais = []
    else:
        with open(mat_file, "r", encoding="utf-8") as f:
            materiais = json.load(f)

    eq_file = os.path.join(sup_dir, "catalogo_equipamentos_re.json")
    if not os.path.exists(eq_file):
        tpl_eq = os.path.join(base_repo_dir, "projetos", "OBRA", "05_SUPRIMENTOS_E_FINANCEIRO", "catalogo_equipamentos_re.template.json")
        if os.path.exists(tpl_eq):
            with open(tpl_eq, "r", encoding="utf-8") as f:
                equipamentos = json.load(f)
        else:
            equipamentos = []
    else:
        with open(eq_file, "r", encoding="utf-8") as f:
            equipamentos = json.load(f)

    sub_file = os.path.join(sup_dir, "plano_subcontratos.json")
    if os.path.exists(sub_file):
        with open(sub_file, "r", encoding="utf-8") as f:
            subcontratos = json.load(f)
    else:
        subcontratos = []

    total_materiais = sum(float(m.get("cd_orcado", 0.0)) for m in materiais)
    total_subcontratos = sum(float(s.get("valor_base", 0.0)) for s in subcontratos)

    print(f"\n" + "="*80)
    print(f"🚀 INICIANDO MOTOR UNIVERSAL DE SUPRIMENTOS: {sigla_obra}")
    print(f"📂 Diretório: {sup_dir}")
    print(f"📦 Pacotes: {len(materiais)} Materiais (RC) | {len(equipamentos)} Equipamentos (RE) | {len(subcontratos)} Subcontratos")
    print("="*80)

    # 3. Geração do Cronograma Mestre em Markdown
    md_crono_name = f"CRONOGRAMA_MESTRE_SUPRIMENTOS_{sigla_obra}.md"
    md_crono_path = os.path.join(sup_dir, md_crono_name)
    linhas_crono = [
        f"# 📅 CRONOGRAMA MESTRE DE SUPRIMENTOS: MATERIAIS & EQUIPAMENTOS",
        "",
        f"> **Empreendimento:** {nome_obra} ({area_m2} m²)  ",
        f"> **Horizonte Temporal:** {prazo_meses:,.0f} Meses ({prazo_meses*4.33:.0f} Semanas / {prazo_meses*30:.0f} Dias Corridos) — Linha de Base  ",
        f"> **Governança:** POP 05, POP 06, POP 17 e Skill Gestão 03  ",
        f"> **Data de Atualização:** {datetime.now().strftime('%d/%m/%Y')} | **Engenheiro Chefe:** PMO Virtual",
        "",
        "---",
        "",
        "## 1. Premissas Operacionais & Regras de Gatilho (POP 05)",
        "",
        "Para garantir o abastecimento contínuo do canteiro sem atrasos logísticos e sem sobrecarga do fluxo de caixa, a Engenharia e Suprimentos operam sob a regra de **Gatilho de Disparo Antecipado**:",
        "",
        "- **Data Gatilho da RC (Engenharia):** Prazo limite para a obra emitir a RC técnica com quantidades em UCC, EAP e Centro de Custo;",
        "- **Lead Time de Suprimentos:** Tempo regulamentar para cotação de 3 propostas, equalização técnica, aprovação da Diretoria (Skill 03) e entrega;",
        "- **Data de Necessidade Física no Canteiro:** Momento exato em que o insumo deve estar descarregado e inspecionado (POP 06);",
        "- **Regra de Pagamento Padrão:** Faturamento D+30 após entrega física aprovada.",
        "",
        "---",
        "",
        f"## 2. Cronograma de Suprimentos — MATERIAIS E INSUMOS CRÍTICOS ({len(materiais)} Pacotes)",
        "",
        "| Nº RC | Pacote de Fornecimento | Centro Custo | Qtd Comercial UCC | Disparo RC | Emissão PC | Entrega Obra | Sem. | Lead | Custo Direto Base | Critério de Recebimento (POP 06) |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |"
    ]

    for m in materiais:
        val_str = f"R$ {float(m.get('cd_orcado', 0.0)):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
        linhas_crono.append(
            f"| **{m['rc']}** | {m['pacote']} | `{m['cc']}` | {m['qtd_ucc']} | {m['data_gatilho_rc']} | {m['data_pc']} | **{m['data_obra']}** | `{m.get('semana', '-')}` | {m['lead_dias']}d | {val_str} | {m.get('criterio_pop06', '-')} |"
        )

    linhas_crono.extend([
        "",
        f"**Custo Direto Orçado dos Materiais:** R$ {total_materiais:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."),
        "",
        "---",
        "",
        f"## 3. Cronograma de Suprimentos — EQUIPAMENTOS & INSTALAÇÕES PROVISÓRIAS ({len(equipamentos)} Itens)",
        "",
        "| Item | Equipamento / Instalação | Qtd | Un | Meses | Semanas | Centro Custo | Lead | Disparo Pedido | Mobilização | Desmobilização | Modalidade Contratual | Fornecedor Alvo / Função |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |"
    ])

    for eq in equipamentos:
        linhas_crono.append(
            f"| `{eq['item']}` | **{eq['nome']}** | {eq['qtd']} | {eq['und']} | {eq['meses']} | `{eq['semanas']}` | `{eq['cc']}` | {eq['lead_dias']}d | {eq['data_solic']} | **{eq['data_mobil']}** | {eq['data_desmob']} | {eq['modalidade']} | {eq['fornecedor_alvo']} — *{eq['funcao']}* |"
        )

    linhas_crono.extend([
        "",
        "---",
        "",
        "## 4. Plano de Ação Imediato para a Equipe de Suprimentos",
        "",
        "1. **Disparo Antecipado de RCs:** Respeitar rigorosamente a matriz D-30 (cotação), D-15 (pedido) e D-0 (canteiro);",
        "2. **Homologação Prévia de Terceiros:** Coleta de documentação SST (POP 17 / NR-18) com 30 dias de antecedência;",
        "3. **Acompanhamento no Tracker Kanban:** Manter os semáforos verdes através de revisão semanal no comitê de obras.",
        "",
        "*Documento oficial gerado e auditado pelo Sistema de Gestão de Obras (PMO Virtual).*"
    ])

    with open(md_crono_path, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_crono))
    print(f"✅ Cronograma Mestre de Suprimentos MD gerado: {md_crono_path}")

    # 4. Geração do Excel OpenPyXL Multi-Abas
    xlsx_name = f"CRONOGRAMA_MESTRE_SUPRIMENTOS_{sigla_obra}.xlsx"
    xlsx_path = os.path.join(sup_dir, xlsx_name)
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    NAVY_HEADER = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    GRAY_LIGHT = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
    FONT_TITLE = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
    FONT_HEADER = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    FONT_BOLD = Font(name="Calibri", size=10, bold=True, color="1B365D")
    BORDER_THIN = Border(
        left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'), bottom=Side(style='thin', color='DDDDDD')
    )
    BORDER_TOTAL = Border(top=Side(style='thin', color='1B365D'), bottom=Side(style='double', color='1B365D'))

    # Aba 1: Materiais
    ws_mat = wb.create_sheet(title="Materiais e Insumos")
    ws_mat.views.sheetView[0].showGridLines = True
    ws_mat.merge_cells("A1:K1")
    ws_mat["A1"] = f"CRONOGRAMA MESTRE DE SUPRIMENTOS: MATERIAIS & INSUMOS ({sigla_obra})"
    ws_mat["A1"].font = FONT_TITLE
    ws_mat["A1"].fill = NAVY_HEADER
    ws_mat["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_mat.row_dimensions[1].height = 28

    ws_mat.merge_cells("A2:K2")
    ws_mat["A2"] = f"{nome_obra} | Prazos de Gatilho vs Lead Time POP 05"
    ws_mat["A2"].font = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    ws_mat["A2"].fill = PatternFill(start_color="203A43", end_color="203A43", fill_type="solid")
    ws_mat["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_mat.row_dimensions[2].height = 20

    headers_mat = [
        "Nº RC", "Pacote de Fornecimento", "Disciplina", "EAP Ref.", "Centro de Custo",
        "Qtd Comercial UCC", "Data Gatilho RC", "Data Emissão PC", "Data Entrega Obra",
        "Semana", "Custo Direto Base (R$)"
    ]
    start_r = 4
    ws_mat.row_dimensions[start_r].height = 24
    for c_idx, h in enumerate(headers_mat, start=1):
        c = ws_mat.cell(row=start_r, column=c_idx, value=h)
        c.font = FONT_HEADER
        c.fill = NAVY_HEADER
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER_THIN

    tot_mat_val = 0.0
    for idx, m in enumerate(materiais, start=start_r+1):
        ws_mat.row_dimensions[idx].height = 20
        ws_mat.cell(row=idx, column=1, value=m.get("rc", "")).alignment = Alignment(horizontal="center")
        ws_mat.cell(row=idx, column=2, value=m.get("pacote", "")).alignment = Alignment(horizontal="left")
        ws_mat.cell(row=idx, column=3, value=m.get("disciplina", "")).alignment = Alignment(horizontal="left")
        ws_mat.cell(row=idx, column=4, value=m.get("eap", "")).alignment = Alignment(horizontal="center")
        ws_mat.cell(row=idx, column=5, value=m.get("cc", "")).alignment = Alignment(horizontal="center")
        ws_mat.cell(row=idx, column=6, value=m.get("qtd_ucc", "")).alignment = Alignment(horizontal="right")
        ws_mat.cell(row=idx, column=7, value=m.get("data_gatilho_rc", "")).alignment = Alignment(horizontal="center")
        ws_mat.cell(row=idx, column=8, value=m.get("data_pc", "")).alignment = Alignment(horizontal="center")
        c_ent = ws_mat.cell(row=idx, column=9, value=m.get("data_obra", ""))
        c_ent.alignment = Alignment(horizontal="center")
        c_ent.font = FONT_BOLD
        ws_mat.cell(row=idx, column=10, value=m.get("semana", "-")).alignment = Alignment(horizontal="center")
        val = float(m.get("cd_orcado", 0.0))
        c_val = ws_mat.cell(row=idx, column=11, value=val)
        c_val.number_format = '"R$ "#,##0.00'
        c_val.alignment = Alignment(horizontal="right")
        tot_mat_val += val
        for col in range(1, 12):
            ws_mat.cell(row=idx, column=col).border = BORDER_THIN
            if idx % 2 == 0:
                ws_mat.cell(row=idx, column=col).fill = GRAY_LIGHT

    # Total Materiais
    tot_row = start_r + len(materiais) + 1
    ws_mat.row_dimensions[tot_row].height = 24
    ws_mat.merge_cells(start_row=tot_row, start_column=1, end_row=tot_row, end_column=10)
    ws_mat.cell(row=tot_row, column=1, value=f"TOTAL CUSTO DIRETO DOS {len(materiais)} PACOTES DE MATERIAIS:").font = FONT_BOLD
    ws_mat.cell(row=tot_row, column=1).alignment = Alignment(horizontal="right", vertical="center")
    c_tot = ws_mat.cell(row=tot_row, column=11, value=tot_mat_val)
    c_tot.number_format = '"R$ "#,##0.00'
    c_tot.font = FONT_BOLD
    c_tot.alignment = Alignment(horizontal="right")
    for col in range(1, 12):
        ws_mat.cell(row=tot_row, column=col).border = BORDER_TOTAL

    # Aba 2: Equipamentos
    ws_eq = wb.create_sheet(title="Equipamentos e Canteiro")
    ws_eq.views.sheetView[0].showGridLines = True
    ws_eq.merge_cells("A1:K1")
    ws_eq["A1"] = f"CRONOGRAMA DE EQUIPAMENTOS & LOCAÇÕES ({sigla_obra})"
    ws_eq["A1"].font = FONT_TITLE
    ws_eq["A1"].fill = NAVY_HEADER
    ws_eq["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_eq.row_dimensions[1].height = 28

    headers_eq = [
        "Item", "Equipamento / Instalação", "Tipo / Modelo", "Qtd", "Un",
        "Meses Atuação", "Semanas", "Centro de Custo", "Data Solicitação",
        "Data Mobilização", "Data Desmobilização"
    ]
    ws_eq.row_dimensions[3].height = 24
    for c_idx, h in enumerate(headers_eq, start=1):
        c = ws_eq.cell(row=3, column=c_idx, value=h)
        c.font = FONT_HEADER
        c.fill = NAVY_HEADER
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER_THIN

    for idx, eq in enumerate(equipamentos, start=4):
        ws_eq.row_dimensions[idx].height = 20
        ws_eq.cell(row=idx, column=1, value=eq.get("item", "")).alignment = Alignment(horizontal="center")
        ws_eq.cell(row=idx, column=2, value=eq.get("nome", "")).alignment = Alignment(horizontal="left")
        ws_eq.cell(row=idx, column=3, value=eq.get("tipo", "")).alignment = Alignment(horizontal="left")
        ws_eq.cell(row=idx, column=4, value=eq.get("qtd", 1)).alignment = Alignment(horizontal="center")
        ws_eq.cell(row=idx, column=5, value=eq.get("und", "un")).alignment = Alignment(horizontal="center")
        ws_eq.cell(row=idx, column=6, value=eq.get("meses", "")).alignment = Alignment(horizontal="center")
        ws_eq.cell(row=idx, column=7, value=eq.get("semanas", "")).alignment = Alignment(horizontal="center")
        ws_eq.cell(row=idx, column=8, value=eq.get("cc", "")).alignment = Alignment(horizontal="center")
        ws_eq.cell(row=idx, column=9, value=eq.get("data_solic", "")).alignment = Alignment(horizontal="center")
        c_mob = ws_eq.cell(row=idx, column=10, value=eq.get("data_mobil", ""))
        c_mob.alignment = Alignment(horizontal="center")
        c_mob.font = FONT_BOLD
        ws_eq.cell(row=idx, column=11, value=eq.get("data_desmob", "")).alignment = Alignment(horizontal="center")
        for col in range(1, 12):
            ws_eq.cell(row=idx, column=col).border = BORDER_THIN
            if idx % 2 == 0:
                ws_eq.cell(row=idx, column=col).fill = GRAY_LIGHT

    # Aba 3: Subcontratos
    if subcontratos:
        ws_sub = wb.create_sheet(title="Plano de Empreiteiros")
        ws_sub.views.sheetView[0].showGridLines = True
        ws_sub.merge_cells("A1:G1")
        ws_sub["A1"] = f"PLANO MESTRE DE CONTRATAÇÃO DE EMPREITEIROS ({sigla_obra})"
        ws_sub["A1"].font = FONT_TITLE
        ws_sub["A1"].fill = NAVY_HEADER
        ws_sub["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws_sub.row_dimensions[1].height = 28

        headers_sub = [
            "Cód.", "Pacote de Empreitada", "Período Atuação", "Pico Mão de Obra",
            "Centro de Custo", "Forma de Medição", "Regra de Retenção Técnica"
        ]
        ws_sub.row_dimensions[3].height = 24
        for c_idx, h in enumerate(headers_sub, start=1):
            c = ws_sub.cell(row=3, column=c_idx, value=h)
            c.font = FONT_HEADER
            c.fill = NAVY_HEADER
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            c.border = BORDER_THIN

        for idx, sub in enumerate(subcontratos, start=4):
            ws_sub.row_dimensions[idx].height = 22
            ws_sub.cell(row=idx, column=1, value=sub.get("cod", "")).alignment = Alignment(horizontal="center")
            ws_sub.cell(row=idx, column=2, value=sub.get("nome", "")).alignment = Alignment(horizontal="left")
            ws_sub.cell(row=idx, column=3, value=f"{sub.get('mes', '')} ({sub.get('semanas', '')})").alignment = Alignment(horizontal="center")
            ws_sub.cell(row=idx, column=4, value=sub.get("pico", "")).alignment = Alignment(horizontal="left")
            ws_sub.cell(row=idx, column=5, value=sub.get("cc", "")).alignment = Alignment(horizontal="center")
            ws_sub.cell(row=idx, column=6, value=sub.get("medicao", "")).alignment = Alignment(horizontal="left")
            ws_sub.cell(row=idx, column=7, value=sub.get("retencao", "")).alignment = Alignment(horizontal="left")
            for col in range(1, 8):
                ws_sub.cell(row=idx, column=col).border = BORDER_THIN
                if idx % 2 == 0:
                    ws_sub.cell(row=idx, column=col).fill = GRAY_LIGHT

    wb.save(xlsx_path)
    print(f"✅ Cronograma Mestre de Suprimentos XLSX gerado: {xlsx_path}")

    # 5. Geração do Catálogo Completo de RCs
    md_cat_name = f"CATALOGO_COMPLETO_REQUISICOES_COMPRA_{sigla_obra}.md"
    md_cat_path = os.path.join(sup_dir, md_cat_name)
    linhas_cat = [
        f"# 🛒 CATÁLOGO MESTRE: REQUISIÇÕES DE COMPRA ({sigla_obra})",
        "",
        f"> **Empreendimento:** {nome_obra} ({area_m2} m²)  ",
        f"> **Finalidade:** Banco de Dados Oficial de Suprimentos com Rastreabilidade EAP e Centros de Custo  ",
        f"> **Custo Direto Base Auditado dos Materiais:** R$ {total_materiais:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."),
        "",
        "---",
        "",
        f"## 1. Visão Geral das {len(materiais)} Requisições de Compra",
        "",
        "| Nº RC | Pacote de Compra | Centro Custo | EAP Vinculada | Quantidade em UCC | Disparo RC (Eng) | Data Limite na Obra | Lead | Custo Direto (R$) |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]

    for m in materiais:
        val_str = f"R$ {float(m.get('cd_orcado', 0.0)):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
        linhas_cat.append(
            f"| **{m['rc']}** | {m['pacote']} | `{m['cc']}` | `{m['eap']}` | {m['qtd_ucc']} | {m['data_gatilho_rc']} | **{m['data_obra']}** | {m['lead_dias']}d | {val_str} |"
        )

    linhas_cat.extend([
        "",
        f"**Valor Total Consolidado dos Insumos:** R$ {total_materiais:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."),
        "",
        "---",
        "",
        "## 2. Instruções para Compradores e Almoxarifado",
        "",
        f"1. **Rastreabilidade Obrigatória nas Notas Fiscais:** Toda NF-e emitida pelos fornecedores deve conter em Informações Complementares: `Material destinado à {sigla_obra} - Centro de Custo: [CC] - Pedido de Compra: [Nº PC]`;",
        "2. **Conferência Física no Canteiro (POP 06):** Almoxarife e Engenharia conferem lote a lote com o romaneio e certificados de qualidade antes de assinar o canhoto da NF;",
        "3. **Alçadas de Governança (Skill 03):** Valores até R$ 15.000 (Comprador + Eng. Residente); de R$ 15.000 a R$ 50.000 (Gerente de Operações); acima de R$ 50.000 (Diretoria Executiva).",
        "",
        "*Catálogo Mestre pronto para integração com o ERP da construtora.*"
    ])

    with open(md_cat_path, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_cat))
    print(f"✅ Catálogo de RCs MD gerado: {md_cat_path}")

    # 6. Geração do Plano de Contratação de Empreiteiros
    if subcontratos:
        md_sub_name = f"PLANO_CONTRATACAO_EMPREITEIROS_{sigla_obra}.md"
        md_sub_path = os.path.join(sup_dir, md_sub_name)
        linhas_sub = [
            f"# 👷 PLANO MESTRE DE CONTRATAÇÃO DE EMPREITEIROS & SUBCONTRATOS",
            "",
            f"> **Empreendimento:** {nome_obra} ({area_m2} m²)  ",
            f"> **Referência:** EAP Baseline e Governança Contratual  ",
            f"> **Data:** {datetime.now().strftime('%d/%m/%Y')}",
            "",
            "---",
            "",
            "## 1. Diretrizes de Governança de Subcontratados",
            "",
            "1. **Portão de Segurança SST (POP 17 / NR-18):** Nenhuma empresa terceirizada entra no canteiro sem envio de ASOs, treinamentos de NR-18/NR-35 e fichas de EPI;",
            "2. **Critério de Medição por FVS:** A medição mensal só é aprovada pelo Engenheiro Residente se acompanhada da respectiva FVS assinada;",
            "3. **Retenção Técnica Contratual (5%):** Em todas as medições retém-se 5% do valor bruto da nota fiscal, liberada após o término do período de garantia da etapa.",
            "",
            "---",
            "",
            f"## 2. Mapa dos {len(subcontratos)} Pacotes de Mão de Obra",
            "",
            "| Cód. | Especialidade do Pacote | Período de Atuação | Pico de Efetivo | Centro de Custo | Forma de Medição | Retenção (5%) | Escopo Técnico Resumido |",
            "| :---: | :--- | :---: | :---: | :---: | :--- | :--- | :--- |"
        ]

        for s in subcontratos:
            linhas_sub.append(
                f"| `{s['cod']}` | **{s['nome']}** | {s['mes']} (`{s['semanas']}`) | {s['pico']} | `{s['cc']}` | {s['medicao']} | {s['retencao']} | {s['escopo']} |"
            )

        linhas_sub.extend([
            "",
            "---",
            "*Plano de Subcontratação emitido em total conformidade com a Linha de Base.*"
        ])

        with open(md_sub_path, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas_sub))
        print(f"✅ Plano de Empreiteiros MD gerado: {md_sub_path}")

    return {
        "status": "sucesso",
        "md_crono": md_crono_path,
        "xlsx_crono": xlsx_path,
        "md_cat": md_cat_path,
        "materiais_total": len(materiais),
        "equipamentos_total": len(equipamentos),
        "subcontratos_total": len(subcontratos)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motor Universal de Planejamento de Suprimentos Multi-Obra")
    parser.add_argument("--obra", help="Nome da pasta da obra em /projetos/ (ex: OBRA_TMULT, RESIDENCIAL_ALPHA)")
    parser.add_argument("--dir", help="Caminho direto para a pasta da obra")
    args = parser.parse_args()

    if not args.obra and not args.dir:
        parser.print_help()
        sys.exit(1)

    gerar_cronograma_suprimentos(obra_nome=args.obra, custom_dir=args.dir)
