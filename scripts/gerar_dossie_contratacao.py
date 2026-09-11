#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Geração do Dossiê Executivo de Contratação:
1. Histograma de Mão de Obra (Headcount & Horas-Homem) -> 06_SST_E_RH
2. Histograma de Equipamentos e Instalações de Canteiro -> 04_PRODUCAO_E_AVANCO
3. Curva ABC Dupla (Composições de Serviços e Famílias de Insumos) -> 02_ORCAMENTO_BASE_E_CONTRATOS

Uso:
    python scripts/gerar_dossie_contratacao.py --obra OBRA_TMULT
    python scripts/gerar_dossie_contratacao.py --obra RESIDENCIAL_ALPHA
    python scripts/gerar_dossie_contratacao.py --dir projetos/OBRA_TMULT
"""

import os
import sys
import json
import argparse
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Estilos OpenPyXL
NAVY_HEADER = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
GOLD_ACCENT = PatternFill(start_color="D99B26", end_color="D99B26", fill_type="solid")
GRAY_LIGHT = PatternFill(start_color="F4F6F9", end_color="F4F6F9", fill_type="solid")
GREEN_LIGHT = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
BLUE_LIGHT = PatternFill(start_color="E8EEF5", end_color="E8EEF5", fill_type="solid")

FONT_TITLE = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
FONT_HEADER = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
FONT_BOLD = Font(name="Calibri", size=11, bold=True, color="1B365D")
FONT_REGULAR = Font(name="Calibri", size=11, color="333333")

THIN_BORDER = Border(
    left=Side(style='thin', color='DDDDDD'),
    right=Side(style='thin', color='DDDDDD'),
    top=Side(style='thin', color='DDDDDD'),
    bottom=Side(style='thin', color='DDDDDD')
)
DOUBLE_BOTTOM = Border(
    left=Side(style='thin', color='DDDDDD'),
    right=Side(style='thin', color='DDDDDD'),
    top=Side(style='thin', color='DDDDDD'),
    bottom=Side(style='double', color='1B365D')
)

def parse_args():
    parser = argparse.ArgumentParser(description="Motor Universal de Dossiê Executivo de Contratação.")
    parser.add_argument("--obra", type=str, default="OBRA_TMULT", help="Nome da pasta da obra em projetos/")
    parser.add_argument("--dir", type=str, default=None, help="Caminho completo da pasta da obra")
    return parser.parse_args()

def parse_val(v):
    if isinstance(v, str):
        v = v.replace('R$', '').strip().replace('.', '').replace(',', '.')
    return float(v)

# ==============================================================================
# 1. HISTOGRAMA DE MÃO DE OBRA
# ==============================================================================
def gerar_histograma_mao_de_obra(dir_rh, dados_mo, sigla, titulo_obra, prazo_meses=6):
    print("-> Gerando Histograma de Mão de Obra...")
    cols = ["Grupo", "Função / Cargo", "Categoria", "Custo Base Ref (R$/mês)"] + [f"Mês {m}" for m in range(1, prazo_meses + 1)]
    
    # Ajustar linhas para o número exato de meses
    dados_mo_ajustados = []
    for row in dados_mo:
        prefixo = row[:4]
        meses_vals = row[4:]
        if len(meses_vals) >= prazo_meses:
            ajustado = prefixo + meses_vals[:prazo_meses]
        else:
            ajustado = prefixo + meses_vals + [meses_vals[-1] if meses_vals else 0] * (prazo_meses - len(meses_vals))
        dados_mo_ajustados.append(ajustado)

    df_mo = pd.DataFrame(dados_mo_ajustados, columns=cols)
    
    totais_headcount = [df_mo[f"Mês {m}"].sum() for m in range(1, prazo_meses + 1)]
    totais_hh = [hc * 220 for hc in totais_headcount]
    
    csv_path = os.path.join(dir_rh, f"HISTOGRAMA_MAO_DE_OBRA_{sigla}.csv")
    df_mo.to_csv(csv_path, sep=';', index=False, encoding='utf-8-sig')
    
    xlsx_path = os.path.join(dir_rh, f"HISTOGRAMA_MAO_DE_OBRA_{sigla}.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Histograma de Mão de Obra"
    ws.views.sheetView[0].showGridLines = True
    
    last_ltr = get_column_letter(len(cols))
    ws.merge_cells(f"A1:{last_ltr}2")
    ws["A1"] = f"{sigla} — HISTOGRAMA DE MÃO DE OBRA & HEADCOUNT MENSAL"
    ws["A1"].fill = NAVY_HEADER
    ws["A1"].font = FONT_TITLE
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws.merge_cells(f"A3:{last_ltr}3")
    ws["A3"] = f"Planejamento Físico de Efetivo | {prazo_meses} Meses ({prazo_meses * 30} Dias) | Carga Horária Padrão: 220 Horas-Homem (HH) / mês"
    ws["A3"].fill = PatternFill(start_color="284B78", end_color="284B78", fill_type="solid")
    ws["A3"].font = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    ws["A3"].alignment = Alignment(horizontal="center", vertical="center")
    
    row_hdr = 5
    for col_idx, h in enumerate(cols, start=1):
        cell = ws.cell(row=row_hdr, column=col_idx, value=h)
        cell.fill = NAVY_HEADER
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        
    for r_idx, row_data in enumerate(dados_mo_ajustados, start=6):
        for c_idx, val in enumerate(row_data, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = FONT_REGULAR
            cell.border = THIN_BORDER
            if c_idx == 4:
                cell.number_format = '"R$ "#,##0.00'
                cell.alignment = Alignment(horizontal="right")
            elif c_idx >= 5:
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal="center")
            else:
                cell.alignment = Alignment(horizontal="left" if c_idx == 2 else "center")
            if r_idx % 2 == 1:
                cell.fill = GRAY_LIGHT
                
    r_hc = len(dados_mo_ajustados) + 6
    ws.cell(row=r_hc, column=1, value="TOTAL").alignment = Alignment(horizontal="center")
    ws.cell(row=r_hc, column=2, value="HEADCOUNT TOTAL DE CAMPO (Operários + Gestão)").alignment = Alignment(horizontal="left")
    for m_idx, hc in enumerate(totais_headcount, start=5):
        ws.cell(row=r_hc, column=m_idx, value=hc).number_format = '#,##0'
        ws.cell(row=r_hc, column=m_idx).alignment = Alignment(horizontal="center")
        
    for c in range(1, len(cols) + 1):
        cell = ws.cell(row=r_hc, column=c)
        cell.fill = GOLD_ACCENT
        cell.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        cell.border = THIN_BORDER

    r_hh = r_hc + 1
    ws.cell(row=r_hh, column=1, value="TOTAL HH").alignment = Alignment(horizontal="center")
    ws.cell(row=r_hh, column=2, value="TOTAL DE HORAS-HOMEM PREVISTAS (220h / profissional)").alignment = Alignment(horizontal="left")
    for m_idx, hh in enumerate(totais_hh, start=5):
        ws.cell(row=r_hh, column=m_idx, value=hh).number_format = '#,##0'
        ws.cell(row=r_hh, column=m_idx).alignment = Alignment(horizontal="center")
        
    for c in range(1, len(cols) + 1):
        cell = ws.cell(row=r_hh, column=c)
        cell.fill = GREEN_LIGHT
        cell.font = FONT_BOLD
        cell.border = DOUBLE_BOTTOM
        
    col_widths = {1: 14, 2: 44, 3: 18, 4: 22}
    for c_i in range(5, len(cols) + 1):
        col_widths[c_i] = 12
    for c_idx, w in col_widths.items():
        ws.column_dimensions[get_column_letter(c_idx)].width = w
        
    wb.save(xlsx_path)
    print(f"   -> Salvo: {csv_path}")
    print(f"   -> Salvo: {xlsx_path}")
    return df_mo

# ==============================================================================
# 2. HISTOGRAMA DE EQUIPAMENTOS
# ==============================================================================
def gerar_histograma_equipamentos(dir_prod, dados_eq, sigla, titulo_obra, prazo_meses=6):
    print("-> Gerando Histograma de Equipamentos...")
    cols = ["Equipamento / Instalação Provisória", "Especificação / Modelo", "Unid"] + [f"Mês {m}" for m in range(1, prazo_meses + 1)] + ["Finalidade Operacional"]
    
    dados_eq_ajustados = []
    for row in dados_eq:
        prefixo = row[:3]
        meses_vals = row[3:-1]
        sufixo = [row[-1]]
        if len(meses_vals) >= prazo_meses:
            ajustado = prefixo + meses_vals[:prazo_meses] + sufixo
        else:
            ajustado = prefixo + meses_vals + [meses_vals[-1] if meses_vals else 0] * (prazo_meses - len(meses_vals)) + sufixo
        dados_eq_ajustados.append(ajustado)

    df_eq = pd.DataFrame(dados_eq_ajustados, columns=cols)
    
    csv_path = os.path.join(dir_prod, f"HISTOGRAMA_EQUIPAMENTOS_{sigla}.csv")
    df_eq.to_csv(csv_path, sep=';', index=False, encoding='utf-8-sig')
    
    xlsx_path = os.path.join(dir_prod, f"HISTOGRAMA_EQUIPAMENTOS_{sigla}.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Histograma de Equipamentos"
    ws.views.sheetView[0].showGridLines = True
    
    last_ltr = get_column_letter(len(cols))
    ws.merge_cells(f"A1:{last_ltr}2")
    ws["A1"] = f"{sigla} — HISTOGRAMA DE EQUIPAMENTOS & INFRAESTRUTURA DE CANTEIRO"
    ws["A1"].fill = NAVY_HEADER
    ws["A1"].font = FONT_TITLE
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws.merge_cells(f"A3:{last_ltr}3")
    ws["A3"] = f"Dimensionamento de Maquinário, Andaimes e Módulos Habitáveis ao longo dos {prazo_meses} Meses de Execução"
    ws["A3"].fill = PatternFill(start_color="284B78", end_color="284B78", fill_type="solid")
    ws["A3"].font = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    ws["A3"].alignment = Alignment(horizontal="center", vertical="center")
    
    row_hdr = 5
    for col_idx, h in enumerate(cols, start=1):
        cell = ws.cell(row=row_hdr, column=col_idx, value=h)
        cell.fill = NAVY_HEADER
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        
    for r_idx, row_data in enumerate(dados_eq_ajustados, start=6):
        for c_idx, val in enumerate(row_data, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = FONT_REGULAR
            cell.border = THIN_BORDER
            if 4 <= c_idx <= 3 + prazo_meses:
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal="center")
            elif c_idx == 3:
                cell.alignment = Alignment(horizontal="center")
            else:
                cell.alignment = Alignment(horizontal="left")
            if r_idx % 2 == 1:
                cell.fill = GRAY_LIGHT
                
    col_widths = {1: 40, 2: 38, 3: 8}
    for c_i in range(4, 4 + prazo_meses):
        col_widths[c_i] = 10
    col_widths[4 + prazo_meses] = 35
    for c_idx, w in col_widths.items():
        ws.column_dimensions[get_column_letter(c_idx)].width = w
        
    wb.save(xlsx_path)
    print(f"   -> Salvo: {csv_path}")
    print(f"   -> Salvo: {xlsx_path}")
    return df_eq

# ==============================================================================
# 3. CURVA ABC DE COMPOSIÇÕES E INSUMOS
# ==============================================================================
def gerar_curva_abc_completa(dir_orcamento, orc_path, dados_insumos, sigla, titulo_obra):
    print("-> Gerando Curva ABC de Serviços e Insumos...")
    
    df_orc = pd.read_csv(orc_path, sep=';', encoding='utf-8')
    eap_col = [c for c in df_orc.columns if 'digo EAP' in c or 'EAP' in c][0]
    desc_col = [c for c in df_orc.columns if 'Descricao' in c or 'Item' in c][0]
    
    df_orc['Preco_Total'] = df_orc['Custo Total (R$)'].apply(parse_val)
    df_orc['Preco_Unit'] = df_orc['Preço Unitário (R$)'].apply(parse_val)
    
    df_serv = df_orc.sort_values(by='Preco_Total', ascending=False).reset_index(drop=True)
    total_geral = df_serv['Preco_Total'].sum()
    
    df_serv['Pct_Individual'] = (df_serv['Preco_Total'] / total_geral) * 100
    df_serv['Pct_Acumulado'] = df_serv['Pct_Individual'].cumsum()
    
    def classificar_abc(acum):
        if acum <= 80.0001:
            return 'A'
        elif acum <= 95.0001:
            return 'B'
        else:
            return 'C'
            
    df_serv['Classe_ABC'] = df_serv['Pct_Acumulado'].apply(classificar_abc)
    
    cols_ins = ["Família de Insumo / Recurso Chave", "Natureza de Custo", "Custo Direto Total (R$)", "Qtd Macro", "Unid", "Referência / Aplicação na Obra"]
    df_ins = pd.DataFrame(dados_insumos, columns=cols_ins)
    tot_ins = df_ins["Custo Direto Total (R$)"].sum()
    df_ins["Pct_Individual"] = (df_ins["Custo Direto Total (R$)"] / tot_ins) * 100
    df_ins["Pct_Acumulado"] = df_ins["Pct_Individual"].cumsum()
    df_ins["Classe_ABC"] = df_ins["Pct_Acumulado"].apply(classificar_abc)
    
    csv_serv_path = os.path.join(dir_orcamento, f"CURVA_ABC_SERVICOS_{sigla}.csv")
    df_serv.to_csv(csv_serv_path, sep=';', index=False, encoding='utf-8-sig')
    
    csv_ins_path = os.path.join(dir_orcamento, f"CURVA_ABC_INSUMOS_{sigla}.csv")
    df_ins.to_csv(csv_ins_path, sep=';', index=False, encoding='utf-8-sig')
    
    xlsx_path = os.path.join(dir_orcamento, f"CURVA_ABC_SERVICOS_E_INSUMOS_{sigla}.xlsx")
    wb = openpyxl.Workbook()
    
    # Aba 1: Insumos
    ws1 = wb.active
    ws1.title = "Curva ABC Insumos"
    ws1.views.sheetView[0].showGridLines = True
    
    ws1.merge_cells("A1:I2")
    ws1["A1"] = f"CURVA ABC DE FAMÍLIAS DE INSUMOS & RECURSOS — {sigla}"
    ws1["A1"].fill = NAVY_HEADER
    ws1["A1"].font = FONT_TITLE
    ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws1.merge_cells("A3:I3")
    ws1["A3"] = f"Abertura Analítica do Custo Direto Total: R$ {tot_ins:,.2f}"
    ws1["A3"].fill = PatternFill(start_color="284B78", end_color="284B78", fill_type="solid")
    ws1["A3"].font = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    ws1["A3"].alignment = Alignment(horizontal="center", vertical="center")
    
    headers_ins = ["Item", "Família de Insumo / Recurso Chave", "Natureza", "Custo Direto (R$)", "Qtd", "Unid", "% Indiv.", "% Acum.", "Classe ABC"]
    row_hdr = 5
    for c_idx, h in enumerate(headers_ins, start=1):
        cell = ws1.cell(row=row_hdr, column=c_idx, value=h)
        cell.fill = NAVY_HEADER
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = THIN_BORDER
        
    for idx, r in df_ins.iterrows():
        r_num = idx + 6
        ws1.cell(row=r_num, column=1, value=idx+1).alignment = Alignment(horizontal="center")
        ws1.cell(row=r_num, column=2, value=r["Família de Insumo / Recurso Chave"]).alignment = Alignment(horizontal="left")
        ws1.cell(row=r_num, column=3, value=r["Natureza de Custo"]).alignment = Alignment(horizontal="center")
        ws1.cell(row=r_num, column=4, value=r["Custo Direto Total (R$)"]).number_format = '"R$ "#,##0.00'
        ws1.cell(row=r_num, column=5, value=r["Qtd Macro"]).number_format = '#,##0.00'
        ws1.cell(row=r_num, column=6, value=r["Unid"]).alignment = Alignment(horizontal="center")
        ws1.cell(row=r_num, column=7, value=r["Pct_Individual"] / 100.0).number_format = '0.00%'
        ws1.cell(row=r_num, column=8, value=r["Pct_Acumulado"] / 100.0).number_format = '0.00%'
        
        cell_abc = ws1.cell(row=r_num, column=9, value=r["Classe_ABC"])
        cell_abc.alignment = Alignment(horizontal="center")
        cell_abc.font = Font(name="Calibri", size=11, bold=True)
        if r["Classe_ABC"] == 'A':
            cell_abc.fill = PatternFill(start_color="FFD1D1", end_color="FFD1D1", fill_type="solid")
        elif r["Classe_ABC"] == 'B':
            cell_abc.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
        else:
            cell_abc.fill = PatternFill(start_color="D9EAD3", end_color="D9EAD3", fill_type="solid")
            
        for c in range(1, 9):
            ws1.cell(row=r_num, column=c).font = FONT_REGULAR
            ws1.cell(row=r_num, column=c).border = THIN_BORDER
            if idx % 2 == 1:
                ws1.cell(row=r_num, column=c).fill = GRAY_LIGHT
                
    r_tot_ins = len(df_ins) + 6
    ws1.cell(row=r_tot_ins, column=1, value="TOTAL").alignment = Alignment(horizontal="center")
    ws1.cell(row=r_tot_ins, column=2, value="TOTAL CUSTO DIRETO DA OBRA").alignment = Alignment(horizontal="left")
    ws1.cell(row=r_tot_ins, column=4, value=tot_ins).number_format = '"R$ "#,##0.00'
    ws1.cell(row=r_tot_ins, column=7, value=1.0).number_format = '0.00%'
    ws1.cell(row=r_tot_ins, column=8, value=1.0).number_format = '0.00%'
    for c in range(1, 10):
        cell = ws1.cell(row=r_tot_ins, column=c)
        cell.fill = GREEN_LIGHT
        cell.font = FONT_BOLD
        cell.border = DOUBLE_BOTTOM
        
    col_w_ins = {1: 8, 2: 45, 3: 16, 4: 22, 5: 12, 6: 8, 7: 12, 8: 12, 9: 14}
    for c_idx, w in col_w_ins.items():
        ws1.column_dimensions[get_column_letter(c_idx)].width = w

    # Aba 2: Serviços
    ws2 = wb.create_sheet(title=f"Curva ABC Serviços ({len(df_serv)}I)")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2.merge_cells("A1:J2")
    ws2["A1"] = f"CURVA ABC DE COMPOSIÇÕES E PACOTES DE SERVIÇOS ({len(df_serv)} ITENS DA EAP)"
    ws2["A1"].fill = NAVY_HEADER
    ws2["A1"].font = FONT_TITLE
    ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    headers_serv = ["Rank", "Código EAP", "Descrição do Pacote / Serviço", "Disciplina", "Qtd Proj", "Unid", "Preço Total Turnkey (R$)", "% Indiv.", "% Acum.", "Classe ABC"]
    for c_idx, h in enumerate(headers_serv, start=1):
        cell = ws2.cell(row=4, column=c_idx, value=h)
        cell.fill = NAVY_HEADER
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = THIN_BORDER
        
    for idx, r in df_serv.iterrows():
        r_num = idx + 5
        ws2.cell(row=r_num, column=1, value=idx+1).alignment = Alignment(horizontal="center")
        ws2.cell(row=r_num, column=2, value=str(r[eap_col]).strip()).alignment = Alignment(horizontal="center")
        ws2.cell(row=r_num, column=3, value=str(r[desc_col]).strip()).alignment = Alignment(horizontal="left")
        ws2.cell(row=r_num, column=4, value=str(r.get("Disciplina", "")).strip()).alignment = Alignment(horizontal="center")
        ws2.cell(row=r_num, column=5, value=r["Qtd Projeto"]).number_format = '#,##0.00'
        ws2.cell(row=r_num, column=6, value=str(r.get("Unidade Proj", "")).strip()).alignment = Alignment(horizontal="center")
        ws2.cell(row=r_num, column=7, value=r["Preco_Total"]).number_format = '"R$ "#,##0.00'
        ws2.cell(row=r_num, column=8, value=r["Pct_Individual"] / 100.0).number_format = '0.00%'
        ws2.cell(row=r_num, column=9, value=r["Pct_Acumulado"] / 100.0).number_format = '0.00%'
        
        cell_abc = ws2.cell(row=r_num, column=10, value=r["Classe_ABC"])
        cell_abc.alignment = Alignment(horizontal="center")
        cell_abc.font = Font(name="Calibri", size=11, bold=True)
        if r["Classe_ABC"] == 'A':
            cell_abc.fill = PatternFill(start_color="FFD1D1", end_color="FFD1D1", fill_type="solid")
        elif r["Classe_ABC"] == 'B':
            cell_abc.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
        else:
            cell_abc.fill = PatternFill(start_color="D9EAD3", end_color="D9EAD3", fill_type="solid")
            
        for c in range(1, 10):
            ws2.cell(row=r_num, column=c).font = FONT_REGULAR
            ws2.cell(row=r_num, column=c).border = THIN_BORDER
            if idx % 2 == 1:
                ws2.cell(row=r_num, column=c).fill = GRAY_LIGHT
                
    col_w_serv = {1: 8, 2: 14, 3: 45, 4: 20, 5: 12, 6: 8, 7: 22, 8: 12, 9: 12, 10: 14}
    for c_idx, w in col_w_serv.items():
        ws2.column_dimensions[get_column_letter(c_idx)].width = w
        
    wb.save(xlsx_path)
    print(f"   -> Salvo: {csv_serv_path}")
    print(f"   -> Salvo: {csv_ins_path}")
    print(f"   -> Salvo: {xlsx_path}")
    return df_serv, df_ins

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
    
    dir_orcamento = os.path.join(project_dir, "02_ORCAMENTO_BASE_E_CONTRATOS")
    dir_producao = os.path.join(project_dir, "04_PRODUCAO_E_AVANCO")
    dir_rh = os.path.join(project_dir, "06_SST_E_RH")
    
    os.makedirs(dir_orcamento, exist_ok=True)
    os.makedirs(dir_producao, exist_ok=True)
    os.makedirs(dir_rh, exist_ok=True)
    
    # Carregar dados estruturados
    mo_json = os.path.join(dir_rh, "dados_histograma_mo.json")
    eq_json = os.path.join(dir_producao, "dados_histograma_equipamentos.json")
    ins_json = os.path.join(dir_orcamento, "dados_familias_insumos.json")
    orc_path = os.path.join(dir_orcamento, "ORCAMENTO_BASE_CONSOLIDADO.csv")
    
    if not os.path.exists(orc_path):
        print(f"[ERRO] Orçamento base não encontrado: {orc_path}")
        sys.exit(1)
        
    with open(mo_json, "r", encoding="utf-8") as f:
        dados_mo = json.load(f)
    with open(eq_json, "r", encoding="utf-8") as f:
        dados_eq = json.load(f)
    with open(ins_json, "r", encoding="utf-8") as f:
        dados_insumos = json.load(f)
        
    print(f"=== MOTOR UNIVERSAL DE DOSSIÊ DE CONTRATAÇÃO: {titulo} ({sigla}) ===")
    gerar_histograma_mao_de_obra(dir_rh, dados_mo, sigla, titulo, prazo_meses=prazo_meses)
    gerar_histograma_equipamentos(dir_producao, dados_eq, sigla, titulo, prazo_meses=prazo_meses)
    gerar_curva_abc_completa(dir_orcamento, orc_path, dados_insumos, sigla, titulo)
    print("=== DOSSIÊ DE CONTRATAÇÃO GERADO COM SUCESSO! ===")

if __name__ == "__main__":
    main()
