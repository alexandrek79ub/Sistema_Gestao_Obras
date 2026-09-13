#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Geração de RDO (Relatório Diário de Obra) e Painel de Produção.
Arquitetura Modular v2.0 Lean (Manual de Boas Práticas §2).

Uso:
    python scripts/gerar_rdo.py --obra OBRA_TMULT
    python scripts/gerar_rdo.py --dir projetos/OBRA_TMULT
"""

import os
import sys
import openpyxl
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.common.obra_io import (
    parse_obra_args, resolver_obra_dir, carregar_config_obra, salvar_markdown, salvar_csv_utf8_sig
)
from scripts.common.excel_theme import (
    NAVY, BLUE_DARK, HEADER_GRAY, ZEBRA_LIGHT, GREEN_FILL, YELLOW_LIGHT,
    FONT_TITLE, FONT_HEADER, FONT_BOLD, FONT_REGULAR, FONT_GREEN,
    THIN_BORDER, DOUBLE_BOTTOM_BORDER, ALIGN_CENTER, ALIGN_RIGHT, ALIGN_LEFT
)

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates", "rdo")

SEMANA1_DADOS = [
    {
        "num": "001", "data": "22/09/2026", "dia": "Terça-feira", "clima_m": "Sol", "clima_t": "Sol",
        "temp": "24°C a 29°C", "cond": "Praticável", "h_paral": 0.0, "ef_prop": 5, "ef_terc": 8, "hh": 104,
        "eap": "1.0.1 (Mobilização Canteiro NR-18) e 1.1.1 (Locação Topográfica da Obra)",
        "equip": "LOC-01 (Mini Retro - 6h), LOC-05 (Gerador - 8h), LOC-03 (Sapo - 4h)",
        "fvs": "FVS-01-TOPOGRAFIA_E_LOCACAO", "fvs_status": "Aprovado",
        "obs": "Início oficial de mobilização. Entrega e montagem dos 4 containers NR-18 e ligação provisória de água pipa e gerador. Execução do gabarito de tábua corrida perimetral com estação total (POP 21). DDS de integração NR-18 aplicado a todos os 13 trabalhadores."
    },
    {
        "num": "002", "data": "23/09/2026", "dia": "Quarta-feira", "clima_m": "Sol", "clima_t": "Nublado",
        "temp": "23°C a 27°C", "cond": "Praticável", "h_paral": 0.0, "ef_prop": 5, "ef_terc": 10, "hh": 120,
        "eap": "1.1.1 (Escavação Mecânica e Manual de Sapatas S1 a S16)",
        "equip": "LOC-01 (Mini Retro - 8h), LOC-06 (Caçamba Estacionária)",
        "fvs": "FVS-01-TOPOGRAFIA_E_LOCACAO e FVS-02-FUNDACOES", "fvs_status": "Aprovado Parcial (Liberação de eixos 1 a 4)",
        "obs": "Escavação mecânica com mini retroescavadeira das primeiras 16 sapatas isoladas. Equipe de serventes fazendo o acerto manual de fundo de cava e descarte em caçamba. Sem interferências subterrâneas encontradas."
    },
    {
        "num": "003", "data": "24/09/2026", "dia": "Quinta-feira", "clima_m": "Nublado", "clima_t": "Chuva Fraca",
        "temp": "21°C a 25°C", "cond": "Praticável c/ Restrição", "h_paral": 1.0, "ef_prop": 5, "ef_terc": 11, "hh": 120,
        "eap": "1.1.1 (Escavação S17 a S32) e 1.1.2 (Apiloamento e Lastro de Concreto Magro S1 a S12)",
        "equip": "LOC-01 (Mini Retro - 6h), LOC-02 (Betoneira 400L - 5h), LOC-03 (Compactador - 4h)",
        "fvs": "FVS-02-FUNDACOES (Lastro Magro e Nivelamento)", "fvs_status": "Aprovado",
        "obs": "Chuva leve às 15h paralisou escavação externa por 1 hora. Equipe remanejada para montagem e corte de armaduras na bancada coberta do canteiro. Lançamento de concreto magro espessura 5cm nas sapatas S1 a S12."
    },
    {
        "num": "004", "data": "25/09/2026", "dia": "Sexta-feira", "clima_m": "Sol", "clima_t": "Sol",
        "temp": "22°C a 28°C", "cond": "Praticável", "h_paral": 0.0, "ef_prop": 5, "ef_terc": 12, "hh": 136,
        "eap": "1.1.5 (Montagem de Fôrmas Sapatas S1-S16) e 1.1.10 (Posicionamento Armaduras S1-S16)",
        "equip": "LOC-02 (Betoneira - 4h), LOC-05 (Gerador - 8h)",
        "fvs": "FVS-02-FUNDACOES (Armação e Fôrmas de Sapatas)", "fvs_status": "Aprovado c/ Ressalva (Ajustar espaçadores pastilha em S4 e S7)",
        "obs": "Carpinteiros posicionando fôrmas compensadas 17mm e armadores fixando as malhas de ferro CA-50 com espaçadores tipo pastilha para garantir cobrimento normativo de 40mm. Inspeção do Engenheiro liberou fôrmas após ajuste de pastilhas nas sapatas S4 e S7."
    },
    {
        "num": "005", "data": "26/09/2026", "dia": "Sábado (Meio Período)", "clima_m": "Sol", "clima_t": "Ensolarado",
        "temp": "23°C a 30°C", "cond": "Praticável", "h_paral": 0.0, "ef_prop": 3, "ef_terc": 8, "hh": 44,
        "eap": "1.1.3 (Concretagem 1ª Etapa Sapatas S1-S16 fck 30 MPa)",
        "equip": "Caminhão Betoneira Usinado + Bomba Lança, Vibrador de Imersão",
        "fvs": "FVS-03-ESTRUTURA_CONCRETO (Concretagem Fundação)", "fvs_status": "Aprovado (6 CPs moldados)",
        "obs": "Concretagem usinada de 18,5 m³ de concreto fck 30 MPa (NF 4821 - Usina Norte Fluminense). Slump test medido em 12 ± 2 cm. Moldados 6 corpos de prova para ensaios aos 7, 14 e 28 dias. Início imediato da cura úmida com aspersão de água e lona plástica."
    }
]


def gerar_templates_rdo(output_dir, config):
    """Gera template Markdown e CSV de RDO a partir de template desacoplado."""
    sigla, nome = config.get("sigla_obra", "OBRA"), config.get("nome_obra", "Obra")
    with open(os.path.join(TEMPLATES_DIR, "template_rdo_executivo.md"), "r", encoding="utf-8") as f:
        template_md = f.read().replace("{{NOME_OBRA}}", nome).replace("{{SIGLA_OBRA}}", sigla)
    salvar_markdown(os.path.join(output_dir, "TEMPLATE_RDO_EXECUTIVO.md"), template_md)

    csv_header = (
        "NUM_RDO;DATA;DIA_SEMANA;CLIMA_MANHA;CLIMA_TARDE;CONDICAO_TRABALHO;HORAS_PARALISACAO;"
        "EFETIVO_PROPRIO;EFETIVO_TERCEIRO;TOTAL_EFETIVO;TOTAL_HH;"
        "EQUIPAMENTOS_ATIVOS;ITENS_EAP_EXECUTADOS;FVS_INSPECIONADA;STATUS_FVS;OCORRENCIAS;ENGENHEIRO_APROVADOR\n"
    )
    with open(os.path.join(output_dir, "TEMPLATE_RDO_EXECUTIVO.csv"), "w", encoding="utf-8") as f:
        f.write(csv_header)


def gerar_rdos_piloto_semana1(output_dir, config):
    """Gera os 5 diários de obra da Semana 1 a partir do template externo."""
    rdos_dir = os.path.join(output_dir, "RDOS")
    os.makedirs(rdos_dir, exist_ok=True)
    sigla, nome = config.get("sigla_obra", "TMULT"), config.get("nome_obra", "TMULT — Edifício Administrativo")

    with open(os.path.join(TEMPLATES_DIR, "template_rdo_diario.md"), "r", encoding="utf-8") as f:
        base_tmpl = f.read()

    for d in SEMANA1_DADOS:
        txt = (base_tmpl
               .replace("{{NUM}}", d['num'])
               .replace("{{NOME_OBRA}}", nome)
               .replace("{{SIGLA_OBRA}}", sigla)
               .replace("{{DATA}}", d['data'])
               .replace("{{DIA}}", d['dia'])
               .replace("{{CLIMA_M}}", d['clima_m'])
               .replace("{{CLIMA_T}}", d['clima_t'])
               .replace("{{TEMP}}", d['temp'])
               .replace("{{COND}}", d['cond'])
               .replace("{{H_PARAL}}", str(d['h_paral']))
               .replace("{{EF_PROP}}", str(d['ef_prop']))
               .replace("{{EF_TERC}}", str(d['ef_terc']))
               .replace("{{EF_TOT}}", str(d['ef_prop'] + d['ef_terc']))
               .replace("{{HH}}", str(d['hh']))
               .replace("{{EQUIP}}", d['equip'])
               .replace("{{EAP}}", d['eap'])
               .replace("{{FVS}}", d['fvs'])
               .replace("{{FVS_STATUS}}", d['fvs_status'])
               .replace("{{OBS}}", d['obs']))
        caminho_rdo = os.path.join(rdos_dir, f"RDO_{d['num']}_{d['data'].replace('/', '-')}.md")
        with open(caminho_rdo, "w", encoding="utf-8") as f:
            f.write(txt)

    return SEMANA1_DADOS


def construir_painel_excel_rdos(output_dir, config, semana1_dados):
    """Gera o painel Excel corporativo com Dashboard Diário e Registro RDO."""
    sigla = config.get("sigla_obra", "TMULT")
    nome = config.get("nome_obra", "TMULT — Edifício Administrativo")
    excel_path = os.path.join(output_dir, "PAINEL_RDOS_OBRA.xlsx")
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    FONT_SUBTITLE = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    FONT_TH = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    FONT_REG = Font(name="Calibri", size=9, color="333333")
    FONT_AMBER = Font(name="Calibri", size=9, bold=True, color="B06000")
    FONT_B9 = Font(name="Calibri", size=9, bold=True, color="1B365D")
    FONT_G9 = Font(name="Calibri", size=9, bold=True, color="137333")

    # 1. ABA 1: PAINEL GERAL (DASHBOARD)
    ws_dash = wb.create_sheet(title="Painel Geral de Produção")
    ws_dash.views.sheetView[0].showGridLines = True

    ws_dash.merge_cells("A1:H1")
    c1 = ws_dash["A1"]
    c1.value, c1.font, c1.fill, c1.alignment = f"PAINEL CONSOLIDADO DE PRODUÇÃO E RDOS — {nome.upper()}", FONT_TITLE, NAVY, ALIGN_CENTER
    ws_dash.row_dimensions[1].height = 28

    ws_dash.merge_cells("A2:H2")
    c2 = ws_dash["A2"]
    c2.value, c2.font, c2.fill, c2.alignment = "Controle Contínuo de Diários de Obra, Mão de Obra, Clima, Equipamentos e FVS Bloqueantes", FONT_SUBTITLE, BLUE_DARK, ALIGN_CENTER
    ws_dash.row_dimensions[2].height = 18

    for c_top, c_bot, tit in [("B4", "C5", "TOTAL DIAS REGISTRADOS"), ("D4", "E5", "TOTAL HORAS-HOMEM (HH)"), ("F4", "G5", "HORAS DE PARALISAÇÃO")]:
        ws_dash.merge_cells(f"{c_top}:{c_bot}")
        cell = ws_dash[c_top]
        cell.value, cell.font, cell.fill, cell.alignment = f"{tit}\n", FONT_B9, HEADER_GRAY, openpyxl.styles.Alignment(horizontal="center", vertical="center", wrap_text=True)

    kpi_defs = [
        ("B6", "C6", "Dias com RDO Emitido:", "=COUNTA('Registro Diário RDO'!A6:A100)", None),
        ("D6", "E6", "Média de Efetivo / Dia:", "=AVERAGE('Registro Diário RDO'!H6:H100)", "#,##0.0"),
        ("F6", "G6", "Total Horas Paralisação:", "=SUM('Registro Diário RDO'!F6:F100)", "#,##0.0"),
    ]
    for lbl_c, val_c, lbl, form, fmt in kpi_defs:
        ws_dash[lbl_c].value, ws_dash[lbl_c].font = lbl, FONT_REG
        ws_dash[val_c].value, ws_dash[val_c].font = form, FONT_B9
        if fmt: ws_dash[val_c].number_format = fmt

    headers_dash = ["SEMANA OPERACIONAL", "PERÍODO", "DIAS TRABALHADOS", "TOTAL HH", "STATUS CAMINHO CRÍTICO", "FVS LIBERADAS"]
    for c_idx, h in enumerate(headers_dash, start=2):
        cell = ws_dash.cell(row=9, column=c_idx, value=h)
        cell.fill, cell.font = NAVY, FONT_TH

    semanas = [
        ("Semana S01 (Mobilização)", "22/09/2026 a 26/09/2026", 5, "=SUM('Registro Diário RDO'!I6:I10)", "No Prazo (Fundações Iniciadas)", "FVS-01 e FVS-02 Aprovadas"),
        ("Semana S02 (Fundações)", "29/09/2026 a 03/10/2026", "-", "-", "Aguardando Início", "Pendente"),
        ("Semana S03 (Baldrames)", "06/10/2026 a 10/10/2026", "-", "-", "Aguardando Início", "Pendente"),
        ("Semana S04 (Pilares P1-P24)", "13/10/2026 a 17/10/2026", "-", "-", "Aguardando Início", "Pendente"),
        ("Semana S05 (Laje H12 e Vigas)", "20/10/2026 a 24/10/2026", "-", "-", "Aguardando Início", "Pendente"),
        ("Semana S06 (Desforma e Cura)", "27/10/2026 a 31/10/2026", "-", "-", "Aguardando Início", "Pendente"),
    ]
    for r_idx, (sem, per, dias, hh_f, status, fvs) in enumerate(semanas, start=10):
        ws_dash.cell(row=r_idx, column=2, value=sem).font = FONT_B9
        ws_dash.cell(row=r_idx, column=3, value=per).font = FONT_REG
        c_d = ws_dash.cell(row=r_idx, column=4, value=dias)
        c_d.font, c_d.alignment = FONT_REG, ALIGN_CENTER
        c_hh = ws_dash.cell(row=r_idx, column=5, value=hh_f)
        c_hh.font, c_hh.alignment = FONT_B9, ALIGN_RIGHT
        if str(hh_f).startswith("="): c_hh.number_format = "#,##0"
        c_st = ws_dash.cell(row=r_idx, column=6, value=status)
        c_st.font = FONT_G9 if "No Prazo" in status else FONT_REG
        ws_dash.cell(row=r_idx, column=7, value=fvs).font = FONT_REG
        for c in range(2, 8): ws_dash.cell(row=r_idx, column=c).border = THIN_BORDER

    for col in ws_dash.columns:
        ws_dash.column_dimensions[get_column_letter(col[0].column)].width = 18

    # 2. ABA 2: REGISTRO DIÁRIO RDO
    ws_log = wb.create_sheet(title="Registro Diário RDO")
    ws_log.views.sheetView[0].showGridLines = True

    headers_log = [
        ("Nº RDO", 10), ("Data", 12), ("Dia Semana", 14), ("Clima Manhã", 14), ("Clima Tarde", 14),
        ("Horas Paralisadas", 16), ("Efetivo Próprio", 14), ("Efetivo Terceiro", 14), ("Total Efetivo", 14),
        ("Total HH", 12), ("Pacotes EAP Executados", 35), ("FVS Inspecionada", 25), ("Status FVS", 16),
        ("Ocorrências e Observações de Canteiro", 50)
    ]
    ws_log.merge_cells("A1:N1")
    clog1 = ws_log["A1"]
    clog1.value, clog1.font, clog1.fill, clog1.alignment = f"DIÁRIO DE BORDO E REGISTRO DIÁRIO DE PRODUÇÃO (RDOS) — {sigla}", FONT_TITLE, NAVY, ALIGN_CENTER
    ws_log.row_dimensions[1].height, ws_log.row_dimensions[3].height = 25, 28

    for c_idx, (h_name, width) in enumerate(headers_log, start=1):
        cell = ws_log.cell(row=3, column=c_idx, value=h_name)
        cell.font, cell.fill, cell.border = FONT_TH, BLUE_DARK, THIN_BORDER
        cell.alignment = openpyxl.styles.Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws_log.column_dimensions[get_column_letter(c_idx)].width = width

    curr_row = 4
    for d in semana1_dados:
        ws_log.cell(row=curr_row, column=1, value=f"RDO-{d['num']}").alignment = ALIGN_CENTER
        ws_log.cell(row=curr_row, column=2, value=d['data']).alignment = ALIGN_CENTER
        ws_log.cell(row=curr_row, column=3, value=d['dia'])
        ws_log.cell(row=curr_row, column=4, value=d['clima_m'])
        ws_log.cell(row=curr_row, column=5, value=d['clima_t'])

        c_hp = ws_log.cell(row=curr_row, column=6, value=d['h_paral'])
        c_hp.alignment, c_hp.number_format = ALIGN_RIGHT, "#,##0.0"

        ws_log.cell(row=curr_row, column=7, value=d['ef_prop']).alignment = ALIGN_RIGHT
        ws_log.cell(row=curr_row, column=8, value=d['ef_terc']).alignment = ALIGN_RIGHT

        c_tot = ws_log.cell(row=curr_row, column=9, value=f"=G{curr_row}+H{curr_row}")
        c_tot.font, c_tot.alignment = FONT_B9, ALIGN_RIGHT

        c_hh = ws_log.cell(row=curr_row, column=10, value=d['hh'])
        c_hh.font, c_hh.alignment, c_hh.number_format = FONT_B9, ALIGN_RIGHT, "#,##0"

        ws_log.cell(row=curr_row, column=11, value=d['eap'])
        ws_log.cell(row=curr_row, column=12, value=d['fvs'])

        c_st = ws_log.cell(row=curr_row, column=13, value=d['fvs_status'])
        c_st.font = FONT_G9 if "Aprovado" in d['fvs_status'] else FONT_AMBER
        c_st.fill = GREEN_FILL if "Aprovado" in d['fvs_status'] else YELLOW_LIGHT
        c_st.alignment = ALIGN_CENTER

        ws_log.cell(row=curr_row, column=14, value=d['obs'])

        for col in range(1, 15):
            cell = ws_log.cell(row=curr_row, column=col)
            cell.border = THIN_BORDER
            if curr_row % 2 == 1 and col != 13:
                cell.fill = ZEBRA_LIGHT
        curr_row += 1

    ws_log.cell(row=curr_row, column=1, value="TOTAL SEMANA 1").font = FONT_B9
    for col_i, form, fmt in [(6, f"=SUM(F4:F{curr_row-1})", "#,##0.0"), (7, f"=AVERAGE(G4:G{curr_row-1})", "#,##0.0"),
                             (8, f"=AVERAGE(H4:H{curr_row-1})", "#,##0.0"), (9, f"=AVERAGE(I4:I{curr_row-1})", "#,##0.0"),
                             (10, f"=SUM(J4:J{curr_row-1})", "#,##0")]:
        c_t = ws_log.cell(row=curr_row, column=col_i, value=form)
        c_t.font, c_t.number_format = FONT_B9, fmt

    for col in range(1, 15):
        ws_log.cell(row=curr_row, column=col).border = DOUBLE_BOTTOM_BORDER

    wb.save(excel_path)
    return excel_path


def main():
    args = parse_obra_args("Motor Universal de RDO e Painel de Produção.")
    obra_dir = resolver_obra_dir(args)
    config = carregar_config_obra(obra_dir)
    sigla = config.get("sigla_obra", "OBRA")

    print(f"\n=======================================================")
    print(f"🚀 MOTOR UNIVERSAL DE RDO E PRODUÇÃO DE CAMPO")
    print(f"=======================================================")
    print(f"📂 Diretório da Obra: {obra_dir}")
    print(f"🏗️  Obra Ativa: {config.get('nome_obra', sigla)} ({sigla})")

    output_dir = os.path.join(obra_dir, "04_PRODUCAO_E_AVANCO")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[1/3] Gerando Templates Executivos de RDO (Markdown e CSV)...")
    gerar_templates_rdo(output_dir, config)
    print(f"      ✅ TEMPLATE_RDO_EXECUTIVO.md gerado")
    print(f"      ✅ TEMPLATE_RDO_EXECUTIVO.csv gerado")

    print(f"\n[2/3] Gerando Lote Piloto da Semana 1 de Mobilização (RDO-001 a RDO-005)...")
    semana1 = gerar_rdos_piloto_semana1(output_dir, config)
    print(f"      ✅ 5 Diários de Obra gerados em 04_PRODUCAO_E_AVANCO/RDOS/")

    print(f"\n[3/3] Construindo Planilha Executiva PAINEL_RDOS_OBRA.xlsx...")
    excel_path = construir_painel_excel_rdos(output_dir, config, semana1)
    print(f"      ✅ Planilha Excel gerada com sucesso: {excel_path}")
    print(f"\n✨ Motor de RDO concluído com 100% de sucesso!")


if __name__ == "__main__":
    main()
