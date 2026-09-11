#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Geração da Planilha de Medição Evolutiva de Empreiteiros (12 Quinzenas).

Uso:
    python scripts/gerar_planilha_medicao.py --obra OBRA_TMULT
    python scripts/gerar_planilha_medicao.py --obra RESIDENCIAL_ALPHA
    python scripts/gerar_planilha_medicao.py --dir projetos/OBRA_TMULT
"""

import os
import sys
import json
import argparse
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def parse_args():
    parser = argparse.ArgumentParser(description="Motor Universal de Medição de Empreiteiros.")
    parser.add_argument("--obra", type=str, default="OBRA_TMULT", help="Nome da pasta da obra em projetos/")
    parser.add_argument("--dir", type=str, default=None, help="Caminho completo da pasta da obra")
    return parser.parse_args()

def construir_planilha_medicao_completa(pacotes, output_dir, titulo_obra, sigla, num_medicoes=12):
    caminho = os.path.join(output_dir, "PLANILHA_MEDICAO_QUINZENAL_EMPREITEIROS.xlsx")
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # Remove aba padrão em branco

    # Cores Corporativas
    NAVY_HEADER = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    BLUE_SUBHEADER = PatternFill(start_color="284B78", end_color="284B78", fill_type="solid")
    MEDICAO_HDR = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    TOTAL_HDR = PatternFill(start_color="137333", end_color="137333", fill_type="solid")
    GRAY_LIGHT = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
    YELLOW_LIGHT = PatternFill(start_color="FEF7E0", end_color="FEF7E0", fill_type="solid")
    GREEN_LIGHT = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
    BLUE_LIGHT = PatternFill(start_color="E8EEF5", end_color="E8EEF5", fill_type="solid")
    
    FONT_TITLE = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    FONT_INFO = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    FONT_HEADER = Font(name="Calibri", size=9, bold=True, color="FFFFFF")
    FONT_BOLD = Font(name="Calibri", size=9, bold=True, color="1B365D")
    FONT_REGULAR = Font(name="Calibri", size=9, color="333333")
    FONT_GREEN = Font(name="Calibri", size=9, bold=True, color="137333")
    FONT_GOLD = Font(name="Calibri", size=9, bold=True, color="B06000")

    BORDER_THIN = Border(
        left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'), bottom=Side(style='thin', color='DDDDDD')
    )
    BORDER_TOTAL = Border(
        top=Side(style='thin', color='1B365D'), bottom=Side(style='double', color='1B365D'),
        left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD')
    )

    for pac in pacotes:
        ws = wb.create_sheet(title=pac.get("tab_name", pac["cod"]))
        ws.views.sheetView[0].showGridLines = True
        
        col_acum = 6 + num_medicoes + 1
        col_saldo = 6 + num_medicoes + 2
        col_pct = 6 + num_medicoes + 3
        last_col_letter = get_column_letter(col_pct)

        # Cabeçalho Principal
        ws.merge_cells(f"A1:{last_col_letter}1")
        ws["A1"] = f"{sigla} — BOLETIM EVOLUTIVO DE MEDIÇÃO QUINZENAL: {pac['cod']} ({pac['titulo'].upper()})"
        ws["A1"].font = FONT_TITLE
        ws["A1"].fill = NAVY_HEADER
        ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[1].height = 28

        # Subcabeçalho Informativo
        ws.merge_cells(f"A2:{last_col_letter}2")
        ws["A2"] = f"Empreiteiro: {pac.get('empreiteiro', 'Homologado')} | Centro de Custo: {pac.get('cc', '')} | Vigência: {pac.get('vigencia', '')} | Retenção Técnica: 5,0% | Governança: POP 09 e POP 17"
        ws["A2"].font = FONT_INFO
        ws["A2"].fill = BLUE_SUBHEADER
        ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[2].height = 20

        # Linha 4 e 5: Cabeçalhos da Tabela
        headers_col_fixas = [
            ("A", "Código\nEAP", 1),
            ("B", "Descrição Pormenorizada do Serviço Contratado", 1),
            ("C", "Unid", 1),
            ("D", "Quantidade\nContratada", 1),
            ("E", "Preço Unitário\n(R$)", 1),
            ("F", "Total Contrato\n(R$)", 1),
        ]

        ws.row_dimensions[4].height = 18
        ws.row_dimensions[5].height = 24

        # Fixas: Mescla Linha 4 e 5 verticalmente
        for col_letter, title, _ in headers_col_fixas:
            cell_ref = f"{col_letter}4"
            ws.merge_cells(f"{col_letter}4:{col_letter}5")
            ws[cell_ref] = title
            ws[cell_ref].font = FONT_HEADER
            ws[cell_ref].fill = NAVY_HEADER
            ws[cell_ref].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            ws[cell_ref].border = BORDER_THIN

        # Colunas de Medição 1 a N
        col_med_ini = get_column_letter(7)
        col_med_fim = get_column_letter(6 + num_medicoes)
        ws.merge_cells(f"{col_med_ini}4:{col_med_fim}4")
        ws[f"{col_med_ini}4"] = f"AVANÇO FÍSICO QUINZENAL DE PRODUÇÃO ({num_medicoes} MEDIÇÕES CONTRATUAIS - QTD MEDIDA)"
        ws[f"{col_med_ini}4"].font = FONT_HEADER
        ws[f"{col_med_ini}4"].fill = MEDICAO_HDR
        ws[f"{col_med_ini}4"].alignment = Alignment(horizontal="center", vertical="center")

        for m in range(1, num_medicoes + 1):
            col_idx = 6 + m
            c_letter = get_column_letter(col_idx)
            cell = ws.cell(row=5, column=col_idx, value=f"Medição {m}\n(Qtd)")
            cell.font = FONT_HEADER
            cell.fill = MEDICAO_HDR
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = BORDER_THIN

        # Colunas Finais
        ws.merge_cells(f"{get_column_letter(col_acum)}4:{last_col_letter}4")
        ws[f"{get_column_letter(col_acum)}4"] = "SALDOS E FECHAMENTO ACUMULADO"
        ws[f"{get_column_letter(col_acum)}4"].font = FONT_HEADER
        ws[f"{get_column_letter(col_acum)}4"].fill = TOTAL_HDR
        ws[f"{get_column_letter(col_acum)}4"].alignment = Alignment(horizontal="center", vertical="center")

        finais = [
            (col_acum, "Total Medido\nAcumulado"),
            (col_saldo, "Saldo a Medir\n(Quantidade)"),
            (col_pct, "% Avanço\nFísico")
        ]
        for c_idx, title in finais:
            cell = ws.cell(row=5, column=c_idx, value=title)
            cell.font = FONT_HEADER
            cell.fill = TOTAL_HDR
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = BORDER_THIN

        # Linhas de Dados de Serviços
        start_row = 6
        servicos = pac.get("servicos", [])
        end_data_row = start_row + len(servicos) - 1

        for s_idx, s in enumerate(servicos, start=start_row):
            r = s_idx
            ws.row_dimensions[r].height = 20

            ws.cell(row=r, column=1, value=s["eap"]).alignment = Alignment(horizontal="center", vertical="center")
            ws.cell(row=r, column=2, value=s["desc"]).alignment = Alignment(horizontal="left", vertical="center")
            ws.cell(row=r, column=3, value=s["und"]).alignment = Alignment(horizontal="center", vertical="center")
            
            c_qtd = ws.cell(row=r, column=4, value=s["qtd"])
            c_qtd.number_format = '#,##0.00'
            c_qtd.alignment = Alignment(horizontal="right", vertical="center")
            
            c_pu = ws.cell(row=r, column=5, value=s["pu"])
            c_pu.number_format = '"R$ "#,##0.00'
            c_pu.alignment = Alignment(horizontal="right", vertical="center")
            
            c_tot = ws.cell(row=r, column=6, value=f"=D{r}*E{r}")
            c_tot.number_format = '"R$ "#,##0.00'
            c_tot.font = FONT_BOLD
            c_tot.alignment = Alignment(horizontal="right", vertical="center")
            
            # Medições 1 a N
            for m in range(1, num_medicoes + 1):
                col_m = 6 + m
                sim_val = 0.0
                if "simulacao" in pac and s["eap"] in pac["simulacao"]:
                    sim_arr = pac["simulacao"][s["eap"]]
                    if m - 1 < len(sim_arr):
                        sim_val = sim_arr[m - 1]
                        
                c_cell = ws.cell(row=r, column=col_m, value=sim_val)
                c_cell.number_format = '#,##0.00'
                c_cell.alignment = Alignment(horizontal="right", vertical="center")
                if sim_val > 0:
                    c_cell.fill = YELLOW_LIGHT
                    c_cell.font = FONT_BOLD
                    
            c_acum = ws.cell(row=r, column=col_acum, value=f"=SUM({col_med_ini}{r}:{col_med_fim}{r})")
            c_acum.number_format = '#,##0.00'
            c_acum.font = FONT_BOLD
            c_acum.alignment = Alignment(horizontal="right", vertical="center")
            
            letter_acum = get_column_letter(col_acum)
            c_saldo = ws.cell(row=r, column=col_saldo, value=f"=D{r}-{letter_acum}{r}")
            c_saldo.number_format = '#,##0.00'
            c_saldo.alignment = Alignment(horizontal="right", vertical="center")
            
            c_pct = ws.cell(row=r, column=col_pct, value=f"={letter_acum}{r}/D{r}")
            c_pct.number_format = '0.00%'
            c_pct.font = FONT_BOLD
            c_pct.alignment = Alignment(horizontal="center", vertical="center")
            
            for ci in range(1, col_pct + 1):
                cell_item = ws.cell(row=r, column=ci)
                cell_item.border = BORDER_THIN
                if s_idx % 2 == 0 and cell_item.fill.start_color.index != 'FEF7E0':
                    cell_item.fill = GRAY_LIGHT

        # LINHAS DE RODAPÉ
        r_bruto = end_data_row + 1
        ws.row_dimensions[r_bruto].height = 24
        ws.merge_cells(start_row=r_bruto, start_column=1, end_row=r_bruto, end_column=5)
        ws.cell(row=r_bruto, column=1, value="TOTAL BRUTO MEDIDO NO PERÍODO (R$):").font = FONT_BOLD
        ws.cell(row=r_bruto, column=1).alignment = Alignment(horizontal="right", vertical="center")
        
        ws.cell(row=r_bruto, column=6, value=f"=SUM(F{start_row}:F{end_data_row})").number_format = '"R$ "#,##0.00'
        ws.cell(row=r_bruto, column=6).font = FONT_BOLD
        ws.cell(row=r_bruto, column=6).alignment = Alignment(horizontal="right", vertical="center")
        
        for m in range(1, num_medicoes + 1):
            col_m = 6 + m
            col_letter = get_column_letter(col_m)
            c_bruto = ws.cell(
                row=r_bruto, column=col_m,
                value=f"=SUMPRODUCT($E${start_row}:$E${end_data_row},{col_letter}${start_row}:{col_letter}${end_data_row})"
            )
            c_bruto.number_format = '"R$ "#,##0.00'
            c_bruto.font = FONT_BOLD
            c_bruto.alignment = Alignment(horizontal="right", vertical="center")
            
        c_tot_acum_r = ws.cell(
            row=r_bruto, column=col_acum,
            value=f"=SUM({get_column_letter(7)}{r_bruto}:{get_column_letter(6+num_medicoes)}{r_bruto})"
        )
        c_tot_acum_r.number_format = '"R$ "#,##0.00'
        c_tot_acum_r.font = FONT_BOLD
        c_tot_acum_r.alignment = Alignment(horizontal="right", vertical="center")
        
        c_tot_saldo_r = ws.cell(
            row=r_bruto, column=col_saldo,
            value=f"=F{r_bruto}-{get_column_letter(col_acum)}{r_bruto}"
        )
        c_tot_saldo_r.number_format = '"R$ "#,##0.00'
        c_tot_saldo_r.font = FONT_BOLD
        c_tot_saldo_r.alignment = Alignment(horizontal="right", vertical="center")
        
        c_tot_pct = ws.cell(
            row=r_bruto, column=col_pct,
            value=f"={get_column_letter(col_acum)}{r_bruto}/F{r_bruto}"
        )
        c_tot_pct.number_format = '0.00%'
        c_tot_pct.font = FONT_BOLD
        c_tot_pct.alignment = Alignment(horizontal="center", vertical="center")
        
        for ci in range(1, col_pct + 1):
            cell_b = ws.cell(row=r_bruto, column=ci)
            cell_b.fill = BLUE_LIGHT
            cell_b.border = BORDER_TOTAL

        # Linha Acumulado
        r_acum = r_bruto + 1
        ws.row_dimensions[r_acum].height = 20
        ws.merge_cells(start_row=r_acum, start_column=1, end_row=r_acum, end_column=6)
        ws.cell(row=r_acum, column=1, value="TOTAL ACUMULADO ATÉ A MEDIÇÃO (R$):").font = FONT_BOLD
        ws.cell(row=r_acum, column=1).alignment = Alignment(horizontal="right", vertical="center")
        
        for m in range(1, num_medicoes + 1):
            col_m = 6 + m
            col_letter = get_column_letter(col_m)
            col_ini_letter = get_column_letter(7)
            c_ac = ws.cell(row=r_acum, column=col_m, value=f"=SUM({col_ini_letter}${r_bruto}:{col_letter}${r_bruto})")
            c_ac.number_format = '"R$ "#,##0.00'
            c_ac.font = FONT_BOLD
            c_ac.alignment = Alignment(horizontal="right", vertical="center")

        # Linha Saldo
        r_saldo = r_acum + 1
        ws.row_dimensions[r_saldo].height = 20
        ws.merge_cells(start_row=r_saldo, start_column=1, end_row=r_saldo, end_column=6)
        ws.cell(row=r_saldo, column=1, value="SALDO DO CONTRATO APÓS MEDIÇÃO (R$):").font = FONT_BOLD
        ws.cell(row=r_saldo, column=1).alignment = Alignment(horizontal="right", vertical="center")
        
        for m in range(1, num_medicoes + 1):
            col_m = 6 + m
            col_letter = get_column_letter(col_m)
            c_sd = ws.cell(row=r_saldo, column=col_m, value=f"=$F${r_bruto}-{col_letter}{r_acum}")
            c_sd.number_format = '"R$ "#,##0.00'
            c_sd.font = FONT_REGULAR
            c_sd.alignment = Alignment(horizontal="right", vertical="center")

        # Linha % Avanço
        r_pct_acum = r_saldo + 1
        ws.row_dimensions[r_pct_acum].height = 20
        ws.merge_cells(start_row=r_pct_acum, start_column=1, end_row=r_pct_acum, end_column=6)
        ws.cell(row=r_pct_acum, column=1, value="% AVANÇO ACUMULADO NO CONTRATO:").font = FONT_BOLD
        ws.cell(row=r_pct_acum, column=1).alignment = Alignment(horizontal="right", vertical="center")
        
        for m in range(1, num_medicoes + 1):
            col_m = 6 + m
            col_letter = get_column_letter(col_m)
            c_pc = ws.cell(row=r_pct_acum, column=col_m, value=f"={col_letter}{r_acum}/$F${r_bruto}")
            c_pc.number_format = '0.00%'
            c_pc.font = FONT_BOLD
            c_pc.alignment = Alignment(horizontal="center", vertical="center")

        # Linha Retenção 5%
        r_ret = r_pct_acum + 1
        ws.row_dimensions[r_ret].height = 20
        ws.merge_cells(start_row=r_ret, start_column=1, end_row=r_ret, end_column=6)
        ws.cell(row=r_ret, column=1, value="(-) RETENÇÃO TÉCNICA DE GARANTIA (5,0%):").font = FONT_BOLD
        ws.cell(row=r_ret, column=1).alignment = Alignment(horizontal="right", vertical="center")
        
        for m in range(1, num_medicoes + 1):
            col_m = 6 + m
            col_letter = get_column_letter(col_m)
            c_rt = ws.cell(row=r_ret, column=col_m, value=f"={col_letter}{r_bruto}*0.05")
            c_rt.number_format = '"R$ "#,##0.00'
            c_rt.font = FONT_GOLD
            c_rt.alignment = Alignment(horizontal="right", vertical="center")

        # Linha Valor Líquido
        r_liq = r_ret + 1
        ws.row_dimensions[r_liq].height = 24
        ws.merge_cells(start_row=r_liq, start_column=1, end_row=r_liq, end_column=6)
        ws.cell(row=r_liq, column=1, value="(=) VALOR LÍQUIDO A LIBERAR NA NF-e:").font = FONT_BOLD
        ws.cell(row=r_liq, column=1).alignment = Alignment(horizontal="right", vertical="center")
        
        for m in range(1, num_medicoes + 1):
            col_m = 6 + m
            col_letter = get_column_letter(col_m)
            c_lq = ws.cell(row=r_liq, column=col_m, value=f"={col_letter}{r_bruto}-{col_letter}{r_ret}")
            c_lq.number_format = '"R$ "#,##0.00'
            c_lq.font = FONT_GREEN
            c_lq.fill = GREEN_LIGHT
            c_lq.alignment = Alignment(horizontal="right", vertical="center")

        for r_foot in [r_acum, r_saldo, r_pct_acum, r_ret, r_liq]:
            for ci in range(1, col_pct + 1):
                ws.cell(row=r_foot, column=ci).border = BORDER_THIN

        ws.freeze_panes = "G6"
        ws.column_dimensions["A"].width = 11
        ws.column_dimensions["B"].width = 46
        ws.column_dimensions["C"].width = 8
        ws.column_dimensions["D"].width = 16
        ws.column_dimensions["E"].width = 16
        ws.column_dimensions["F"].width = 18
        for m in range(1, num_medicoes + 1):
            ws.column_dimensions[get_column_letter(6 + m)].width = 15
        ws.column_dimensions[get_column_letter(col_acum)].width = 18
        ws.column_dimensions[get_column_letter(col_saldo)].width = 16
        ws.column_dimensions[get_column_letter(col_pct)].width = 14

    wb.save(caminho)
    print(f"-> Planilha Master de Medição gerada: {caminho}")

def main():
    args = parse_args()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if args.dir:
        project_dir = os.path.abspath(args.dir)
    else:
        project_dir = os.path.join(base_dir, "projetos", args.obra)
        
    if not os.path.exists(project_dir):
        print(f"[ERRO] Diretório não encontrado: {project_dir}")
        sys.exit(1)
        
    config_file = os.path.join(project_dir, "config_obra.json")
    config = {}
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
            
    dados_obra = config.get("dados_obra", {})
    sigla = dados_obra.get("sigla", config.get("sigla_obra", os.path.basename(project_dir).replace("OBRA_", "")))
    titulo = dados_obra.get("nome_obra", config.get("nome_obra", f"Obra {sigla}"))
    prazo_meses = int(dados_obra.get("prazo_meses", config.get("prazo_meses", 6)))
    num_medicoes = prazo_meses * 2 # Ciclos quinzenais
    
    med_json = os.path.join(project_dir, "02_ORCAMENTO_BASE_E_CONTRATOS", "dados_medicoes_empreiteiros.json")
    if not os.path.exists(med_json):
        print(f"[ERRO] Arquivo de medições não encontrado: {med_json}")
        sys.exit(1)
        
    with open(med_json, "r", encoding="utf-8") as f:
        pacotes = json.load(f)
        
    output_dir = os.path.join(project_dir, "02_ORCAMENTO_BASE_E_CONTRATOS", "CONTRATOS_EMPREITEIROS")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"=== MOTOR UNIVERSAL DE PLANILHA DE MEDIÇÃO: {titulo} ({sigla}) ===")
    construir_planilha_medicao_completa(pacotes, output_dir, titulo, sigla, num_medicoes=num_medicoes)
    print("=== PLANILHA DE MEDIÇÃO GERADA COM SUCESSO! ===")

if __name__ == "__main__":
    main()
