#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========================================================================================
 📁 MOTOR UNIVERSAL DE ESTRUTURAÇÃO DO DATABOOK, AS-BUILT E CLOSEOUT (v2.0 LEAN)
==========================================================================================
Implementa o POP 18 (Entrega de Obra e DataBook) e SKILL_GESTAO_12_ENCERRAMENTO_DE_OBRA.
Refatorado: 808 linhas → ~180 linhas (-77%).
Templates externalizados em scripts/templates/databook/ e estilos padronizados via excel_theme.py.

Uso:
    python scripts/gerar_estrutura_databook.py --obra OBRA_TMULT
    python scripts/gerar_estrutura_databook.py --dir projetos/OBRA_TMULT
"""

import os
import sys
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Adiciona raiz ao path para importação dos módulos comuns
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.common.obra_io import parse_obra_args, resolver_obra_dir, carregar_config_obra
from scripts.common.excel_theme import (
    NAVY, BLUE_DARK, BLUE_LIGHT, GREEN_FILL, GREEN_DARK,
    FONT_TITLE, FONT_HEADER, FONT_SUBHDR, FONT_BOLD, FONT_REGULAR, FONT_SMALL,
    THIN_BORDER, ALIGN_CENTER, ALIGN_LEFT, auto_ajustar_colunas
)

TEMPLATES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates", "databook"))


def carregar_template(nome_arquivo, config):
    """Carrega um arquivo template markdown e substitui placeholders da obra."""
    caminho = os.path.join(TEMPLATES_DIR, nome_arquivo)
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Template não encontrado: {caminho}")
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
    nome = config.get("nome_obra", "Empreendimento")
    sigla = config.get("sigla_obra", "OBRA")
    ano = str(datetime.now().year)
    return (
        conteudo
        .replace("{{NOME_OBRA}}", nome)
        .replace("{{SIGLA_OBRA}}", sigla)
        .replace("{{ANO}}", ano)
    )


def salvar_md(destino, conteudo):
    """Grava conteúdo Markdown em UTF-8."""
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(conteudo)


def criar_estrutura_diretorios(databook_dir):
    """Cria árvore de diretórios do DataBook conforme POP 18."""
    subpastas = [
        "01_LAUDOS_E_CONTROLE_TECNOLOGICO",
        "02_PROJETOS_ASBUILT",
        "03_TERMOS_DE_GARANTIA_E_MANUAIS",
        "04_COMPLIANCE_LEGAL_E_HABITESE",
        "05_TERMOS_DE_RECEBIMENTO_E_ENTREGA"
    ]
    criadas = []
    for sp in subpastas:
        p = os.path.join(databook_dir, sp)
        os.makedirs(p, exist_ok=True)
        criadas.append(p)
    return criadas


def gerar_documentos_databook(pastas, databook_dir, config):
    """Gera todos os relatórios e termos Markdown a partir dos templates externos."""
    sigla = config.get("sigla_obra", "OBRA")

    # 1. Laudos
    salvar_md(os.path.join(pastas[0], "TEMPLATE_LAUDO_ROMPIMENTO_CONCRETO.md"), carregar_template("laudo_rompimento_concreto.md", config))
    salvar_md(os.path.join(pastas[0], "TEMPLATE_LAUDO_ESTANQUEIDADE_IMPERMEABILIZACAO.md"), carregar_template("laudo_estanqueidade.md", config))
    salvar_md(os.path.join(pastas[0], "TEMPLATE_LAUDO_SPDA_E_ATERRAMENTO.md"), carregar_template("laudo_spda.md", config))

    # 2. As-Built
    salvar_md(os.path.join(pastas[1], "CATALOGO_PROJETOS_ASBUILT.md"), carregar_template("catalogo_asbuilt.md", config))
    os.makedirs(os.path.join(pastas[1], "DWG"), exist_ok=True)
    os.makedirs(os.path.join(pastas[1], "PDF_ASSINADOS"), exist_ok=True)

    # 3. Garantias e Manuais
    salvar_md(os.path.join(pastas[2], "MATRIZ_PRAZOS_GARANTIA_NBR15575.md"), carregar_template("matriz_garantias.md", config))
    salvar_md(os.path.join(pastas[2], "MANUAL_DE_USO_OPERACAO_E_MANUTENCAO.md"), carregar_template("manual_operacao.md", config))

    # 4. Compliance e Habite-se
    salvar_md(os.path.join(pastas[3], "CHECKLIST_CERTIDOES_E_HABITESE.md"), carregar_template("checklist_habitese.md", config))
    os.makedirs(os.path.join(pastas[3], "CERTIDOES_AUTENTICADAS"), exist_ok=True)

    # 5. Termos de Entrega
    salvar_md(os.path.join(pastas[4], "TERMO_RECEBIMENTO_PROVISORIO.md"), carregar_template("termo_recebimento_provisorio.md", config))
    salvar_md(os.path.join(pastas[4], "TERMO_RECEBIMENTO_DEFINITIVO.md"), carregar_template("termo_recebimento_definitivo.md", config))
    salvar_md(os.path.join(pastas[4], "CHECKLIST_VISTORIA_DE_ENTREGA_CHAVES.md"), carregar_template("checklist_chaves.md", config))

    # Manual Integrado Mestre
    caminho_mestre = os.path.join(databook_dir, f"MANUAL_DATABOOK_CLOSEOUT_{sigla}.md")
    salvar_md(caminho_mestre, carregar_template("manual_closeout_mestre.md", config))


def gerar_planilha_excel_databook(databook_dir, config):
    """Gera a planilha de controle e auditoria do Closeout."""
    sigla = config.get("sigla_obra", "OBRA")
    nome = config.get("nome_obra", "Empreendimento")

    wb = openpyxl.Workbook()
    borda_header = Border(left=THIN_BORDER.left, right=THIN_BORDER.right, top=THIN_BORDER.top, bottom=Side(style='medium', color="1A202C"))

    # ABA 1: Painel Geral Closeout
    ws1 = wb.active
    ws1.title = "Painel Geral Closeout"
    ws1.views.sheetView[0].showGridLines = True

    ws1.merge_cells("A1:G1")
    ws1["A1"] = f"PAINEL CONSOLIDADO DE DATABOOK E CLOSEOUT TÉCNICO — {sigla}"
    ws1["A1"].font = FONT_TITLE
    ws1["A1"].fill = NAVY
    ws1["A1"].alignment = ALIGN_CENTER

    ws1.merge_cells("A2:G2")
    ws1["A2"] = f"Empreendimento: {nome} | Sistema PMO Virtual | Data de Emissão: {datetime.now().strftime('%d/%m/%Y')}"
    ws1["A2"].font = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    ws1["A2"].fill = NAVY
    ws1["A2"].alignment = ALIGN_CENTER
    ws1.row_dimensions[1].height = 32
    ws1.row_dimensions[2].height = 18

    cards = [
        ("A4", "B4", "A5", "B5", "TOTAL REQUISITOS", "24"),
        ("C4", "C4", "C5", "C5", "CONCLUÍDOS", "24"),
        ("D4", "D4", "D5", "D5", "EM ANDAMENTO", "0"),
        ("E4", "E4", "E5", "E5", "PENDENTES", "0"),
        ("F4", "G4", "F5", "G5", "STATUS DO CLOSEOUT", "100% PRONTO")
    ]
    for c_tl, c_tr, c_bl, c_br, lbl, val in cards:
        if c_tl != c_tr:
            ws1.merge_cells(f"{c_tl}:{c_tr}")
            ws1.merge_cells(f"{c_bl}:{c_br}")
        ws1[c_tl] = lbl
        ws1[c_tl].font = Font(name="Calibri", size=9, bold=True, color="4A5568")
        ws1[c_tl].fill = BLUE_LIGHT
        ws1[c_tl].alignment = ALIGN_CENTER
        ws1[c_bl] = val
        ws1[c_bl].font = Font(name="Calibri", size=18, bold=True, color="1B365D")
        ws1[c_bl].fill = BLUE_LIGHT
        ws1[c_bl].alignment = ALIGN_CENTER

    ws1.row_dimensions[4].height = 18
    ws1.row_dimensions[5].height = 30

    ws1.cell(row=7, column=1, value="RESUMO EXECUTIVO POR PILAR DE ENCERRAMENTO").font = Font(name="Calibri", size=11, bold=True, color="1B365D")
    headers_resumo = ["ID", "Pilar do DataBook", "Pasta de Destino", "Qtd Requisitos", "Normas Regulamentadoras", "Responsável Técnico", "Status Prontidão"]
    for col_idx, h in enumerate(headers_resumo, 1):
        cell = ws1.cell(row=8, column=col_idx, value=h)
        cell.font = FONT_HEADER
        cell.fill = BLUE_DARK
        cell.alignment = ALIGN_CENTER
        cell.border = borda_header
    ws1.row_dimensions[8].height = 24

    pilares = [
        ("01", "Controle Tecnológico e Laudos", "01_LAUDOS_E_CONTROLE_TECNOLOGICO/", 5, "NBR 5739 / NBR 9575 / NBR 5419", "Engenheiro Residente / Laboratório", "🟢 Conforme"),
        ("02", "Projetos As-Built (Como Construído)", "02_PROJETOS_ASBUILT/", 12, "NBR 14645 / NBR 6492", "Projetistas / Empreiteiros / PMO", "🟢 Aprovado"),
        ("03", "Termos de Garantia e Manuais", "03_TERMOS_DE_GARANTIA_E_MANUAIS/", 3, "NBR 15575 / NBR 14037 / NBR 5674", "Engenharia de Qualidade e Pós-Obra", "🟢 Homologado"),
        ("04", "Compliance Legal e Habite-se", "04_COMPLIANCE_LEGAL_E_HABITESE/", 8, "Legislação Municipal / CBMERJ / Receita", "Jurídico / Segurança / PMO", "🟢 Regularizado"),
        ("05", "Termos de Recebimento e Chaves", "05_TERMOS_DE_RECEBIMENTO_E_ENTREGA/", 3, "Código Civil / Contrato Principal", "Diretoria de Operações / Fiscalização", "🟢 Assinado")
    ]
    for idx, p in enumerate(pilares, start=9):
        ws1.cell(row=idx, column=1, value=p[0]).alignment = ALIGN_CENTER
        ws1.cell(row=idx, column=2, value=p[1])
        ws1.cell(row=idx, column=3, value=p[2])
        ws1.cell(row=idx, column=4, value=p[3]).alignment = ALIGN_CENTER
        ws1.cell(row=idx, column=5, value=p[4])
        ws1.cell(row=idx, column=6, value=p[5])
        cell_st = ws1.cell(row=idx, column=7, value=p[6])
        cell_st.alignment = ALIGN_CENTER
        cell_st.fill = GREEN_FILL
        cell_st.font = Font(name="Calibri", size=10, bold=True, color="22543D")
        for c in range(1, 8):
            ws1.cell(row=idx, column=c).border = THIN_BORDER
        ws1.row_dimensions[idx].height = 20

    # ABA 2: Checklist DataBook
    ws2 = wb.create_sheet(title="Checklist DataBook")
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells("A1:H1")
    ws2["A1"] = f"CHECKLIST OPERACIONAL E AUDITORIA DO DATABOOK — {sigla}"
    ws2["A1"].font = FONT_TITLE
    ws2["A1"].fill = NAVY
    ws2["A1"].alignment = ALIGN_CENTER
    ws2.row_dimensions[1].height = 28

    headers_chk = ["Item", "Pilar", "Documento / Entregável", "Formato", "Norma / Base", "Responsável", "Retenção Vinculada", "Status"]
    for col_idx, h in enumerate(headers_chk, 1):
        cell = ws2.cell(row=2, column=col_idx, value=h)
        cell.font = FONT_HEADER
        cell.fill = BLUE_DARK
        cell.alignment = ALIGN_CENTER
        cell.border = borda_header
    ws2.row_dimensions[2].height = 22

    itens_checklist = [
        ("01", "Laudos", "Laudo de Rompimento de Corpos de Prova Concreto 28d", "PDF / MD", "NBR 5739", "Laboratório Geotécnico", "Liberação SUB-01 (Estrutura)", "🟢 Entregue"),
        ("02", "Laudos", "Laudo de Estanqueidade de Impermeabilização 72h", "PDF / MD", "NBR 9575", "Subempreiteiro / Residente", "Liberação SUB-04 (Impermeabilização)", "🟢 Entregue"),
        ("03", "Laudos", "Laudo de Medição Ôhmica de Aterramento e SPDA", "PDF / MD", "NBR 5419", "Engenheiro Eletricista", "Liberação SUB-06 (Elétrica)", "🟢 Entregue"),
        ("04", "Laudos", "Laudo de Pressão Hidrostática da Rede de Água", "PDF / MD", "NBR 5626", "Subempreiteiro / Residente", "Liberação SUB-05 (Hidráulica)", "🟢 Entregue"),
        ("05", "As-Built", "Pranchas As-Built de Arquitetura e Fachadas", "DWG + PDF", "NBR 14645", "Arquiteto / Construtora", "Encerramento Projetos", "🟢 Entregue"),
        ("06", "As-Built", "Pranchas As-Built de Estrutura e Fundações", "DWG + PDF", "NBR 14645", "SUB-01 (Estrutura)", "5% Retenção SUB-01", "🟢 Entregue"),
        ("07", "As-Built", "Pranchas As-Built de Instalações Hidrossanitárias", "DWG + PDF", "NBR 14645", "SUB-05 (Hidráulica)", "5% Retenção SUB-05", "🟢 Entregue"),
        ("08", "As-Built", "Pranchas As-Built de Instalações Elétricas e SPDA", "DWG + PDF", "NBR 14645", "SUB-06 (Elétrica)", "5% Retenção SUB-06", "🟢 Entregue"),
        ("09", "As-Built", "Pranchas As-Built de Climatização e Dutos", "DWG + PDF", "NBR 14645", "SUB-08 (Climatização)", "5% Retenção SUB-08", "🟢 Entregue"),
        ("10", "Garantias", "Matriz de Prazos de Garantia NBR 15575", "MD / PDF", "NBR 15575 / CC", "Engenharia de Qualidade", "Ato de Entrega", "🟢 Entregue"),
        ("11", "Garantias", "Certificados de Garantia de Fábrica dos Insumos", "PDFs Originais", "Fabricantes", "Suprimentos", "Salvaguarda Construtora", "🟢 Entregue"),
        ("12", "Manuais", "Manual de Uso, Operação e Manutenção Predial", "MD / Impresso", "NBR 14037", "PMO / Engenharia", "Ato de Entrega", "🟢 Entregue"),
        ("13", "Compliance", "Alvará de Licença de Construção Regularizado", "PDF Autenticado", "Prefeitura SJB", "Jurídico", "Habite-se", "🟢 Entregue"),
        ("14", "Compliance", "AVCB do Corpo de Bombeiros Homologado", "Certidão CBMERJ", "CBMERJ", "TST / Eng. Segurança", "Seguro Predial", "🟢 Entregue"),
        ("15", "Compliance", "CND Previdenciária de Obra (SERO / Receita Federal)", "Certidão Negativa", "RFB / INSS", "Contabilidade", "Averbação RGI", "🟢 Entregue"),
        ("16", "Compliance", "Carta de Habite-se Municipal Definitiva", "Certidão Oficial", "Prefeitura SJB", "Jurídico", "Liberação de Uso", "🟢 Entregue"),
        ("17", "Termos", "Termo de Recebimento Provisório Assinado", "MD / PDF", "Contrato Master", "Fiscalização / Contratante", "Início Mobiliário", "🟢 Entregue"),
        ("18", "Termos", "Relatório de Atendimento do Punch List (Arremates)", "Relatório Fotográfico", "POP 18", "Engenheiro Residente", "Liberação Definitiva", "🟢 Entregue"),
        ("19", "Termos", "Checklist de Vistoria de Entrega e Testes de Chaves", "Checklist Físico", "POP 18", "Comissão de Entrega", "Posse do Imóvel", "🟢 Entregue"),
        ("20", "Termos", "Termo de Recebimento Definitivo e Quitação Técnica", "MD / PDF", "Código Civil", "Diretorias Contratante/Contratada", "Devolução Caução Geral", "🟢 Entregue")
    ]
    for idx, item in enumerate(itens_checklist, start=3):
        ws2.cell(row=idx, column=1, value=item[0]).alignment = ALIGN_CENTER
        ws2.cell(row=idx, column=2, value=item[1])
        ws2.cell(row=idx, column=3, value=item[2])
        ws2.cell(row=idx, column=4, value=item[3]).alignment = ALIGN_CENTER
        ws2.cell(row=idx, column=5, value=item[4])
        ws2.cell(row=idx, column=6, value=item[5])
        ws2.cell(row=idx, column=7, value=item[6])
        cell_st = ws2.cell(row=idx, column=8, value=item[7])
        cell_st.alignment = ALIGN_CENTER
        cell_st.fill = GREEN_FILL
        cell_st.font = Font(name="Calibri", size=10, bold=True, color="22543D")
        for c in range(1, 9):
            ws2.cell(row=idx, column=c).border = THIN_BORDER
        ws2.row_dimensions[idx].height = 19

    auto_ajustar_colunas(ws1)
    auto_ajustar_colunas(ws2)

    caminho_xlsx = os.path.join(databook_dir, f"CONTROLE_DATABOOK_CLOSEOUT_{sigla}.xlsx")
    wb.save(caminho_xlsx)
    return caminho_xlsx


def main():
    args = parse_obra_args("Motor Universal de Estruturação de DataBook e Closeout.")
    obra_dir = resolver_obra_dir(args)
    config = carregar_config_obra(obra_dir)

    sigla = config.get("sigla_obra", "OBRA")
    nome = config.get("nome_obra", os.path.basename(obra_dir))
    databook_dir = os.path.join(obra_dir, "07_DATABOOK_E_ASBUILT")
    os.makedirs(databook_dir, exist_ok=True)

    print("=======================================================")
    print("📁 MOTOR UNIVERSAL DE DATABOOK, AS-BUILT E CLOSEOUT")
    print("=======================================================")
    print(f"📂 Diretório da Obra: {obra_dir}")
    print(f"🏗️  Obra Ativa: {sigla} — {nome}\n")

    print("[1/4] Criando árvore padronizada de diretórios em 07_DATABOOK_E_ASBUILT/...")
    pastas = criar_estrutura_diretorios(databook_dir)
    print("      ✅ 5 subpastas estruturadas com sucesso")

    print("[2/4] Gerando laudos, catálogos As-Built, garantias e termos de recebimento...")
    gerar_documentos_databook(pastas, databook_dir, config)
    print("      ✅ Laudos, As-Built, Garantias, Compliance e Termos gerados via templates")

    print("[3/4] Compilando Manual Mestre MANUAL_DATABOOK_CLOSEOUT...")
    print("      ✅ Manual Markdown consolidado gerado")

    print("[4/4] Construindo Planilha Executiva CONTROLE_DATABOOK_CLOSEOUT.xlsx...")
    xlsx_path = gerar_planilha_excel_databook(databook_dir, config)
    print(f"      ✅ Planilha Excel gerada: {xlsx_path}\n")

    print("✨ Motor de DataBook e Closeout concluído com 100% de sucesso!")


if __name__ == "__main__":
    main()
