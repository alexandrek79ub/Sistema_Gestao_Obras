#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Geração do Cronograma Físico-Financeiro, Linha de Base (Baseline 01),
Planilha Executiva Excel (.xlsx), Exportação MS Project (.xml) e Dashboard HTML (.html)
para o Edifício Administrativo TMULT (Porto do Açu).
"""

import os
import json
import datetime
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import LineChart, Reference, Series
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Caminhos do Projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORCAMENTO_CSV = os.path.join(BASE_DIR, "projetos", "OBRA_TMULT", "02_ORCAMENTO_BASE_E_CONTRATOS", "ORCAMENTO_BASE_CONSOLIDADO.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "projetos", "OBRA_TMULT", "03_PLANEJAMENTO_E_CRONOGRAMA")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_val(v):
    if isinstance(v, str):
        v = v.replace('R$', '').strip().replace('.', '').replace(',', '.')
    return float(v)

def carregar_e_distribuir_orcamento():
    df = pd.read_csv(ORCAMENTO_CSV, sep=';', encoding='utf-8')
    
    eap_col = [c for c in df.columns if 'digo EAP' in c or 'EAP' in c][0]
    desc_col = [c for c in df.columns if 'Descricao' in c or 'Item' in c][0]
    df['Preco_Total'] = df['Custo Total (R$)'].apply(parse_val)
    df['Preco_Unitario'] = df['Preço Unitário (R$)'].apply(parse_val)
    
    for m in range(1, 7):
        df[f'P_M{m}'] = 0.0

    for idx, r in df.iterrows():
        eap = str(r[eap_col]).strip()
        desc = str(r[desc_col]).strip()
        
        # 1.0 Administração Local e Canteiro: linear em 6 meses
        if eap.startswith('1.0'):
            for m in range(1, 7):
                df.at[idx, f'P_M{m}'] = 1.0 / 6.0
                
        # 1.1 Infraestrutura: 100% Mês 1
        elif eap.startswith('1.1'):
            df.at[idx, 'P_M1'] = 1.0
            
        # 1.2 Supraestrutura: 100% Mês 2
        elif eap.startswith('1.2'):
            df.at[idx, 'P_M2'] = 1.0
            
        # 2.1 Arquitetura:
        elif eap.startswith('2.1'):
            if eap.startswith('2.1.1'):  # Alvenaria
                df.at[idx, 'P_M3'] = 1.0
            elif eap.startswith('2.1.2'): # Chapisco
                df.at[idx, 'P_M3'] = 0.5
                df.at[idx, 'P_M4'] = 0.5
            elif eap.startswith('2.1.3'): # Emboço / Reboco Paulista
                df.at[idx, 'P_M4'] = 1.0
            elif eap.startswith('2.1.11'): # Impermeabilização WCs/Copa
                df.at[idx, 'P_M4'] = 1.0
            elif eap.startswith('2.1.4'): # Contrapiso
                df.at[idx, 'P_M5'] = 1.0
            elif eap.startswith('2.1.5'): # Porcelanato
                df.at[idx, 'P_M5'] = 1.0
            elif eap.startswith('2.1.6'): # Cerâmica WCs
                df.at[idx, 'P_M5'] = 1.0
            elif eap.startswith('2.1.7'): # Rodapé
                df.at[idx, 'P_M5'] = 1.0
            elif eap.startswith('2.1.9'): # Portas Madeira/Alumínio
                df.at[idx, 'P_M5'] = 1.0
            elif eap.startswith('2.1.10'): # Janelas Alumínio/Vidro
                df.at[idx, 'P_M5'] = 1.0
            elif eap.startswith('2.1.8'): # Pintura
                if 'Selador' in desc or 'Lixa Grossa' in desc:
                    df.at[idx, 'P_M5'] = 0.5
                    df.at[idx, 'P_M6'] = 0.5
                else:
                    df.at[idx, 'P_M6'] = 1.0
            else:
                df.at[idx, 'P_M5'] = 1.0
                
        # 2.2 Cobertura: 100% Mês 3
        elif eap.startswith('2.2'):
            df.at[idx, 'P_M3'] = 1.0
            
        # 3.1 Elétrica e Telecom:
        elif eap.startswith('3.1'):
            if any(term in desc for term in ['Eletroduto', 'Caixa de Embutir', 'Caixa Octogonal', 'Aterramento', 'Quadro']):
                df.at[idx, 'P_M4'] = 1.0
            elif any(term in desc for term in ['Cabo Cobre', 'Cabo UTP']):
                df.at[idx, 'P_M5'] = 1.0
            else:
                df.at[idx, 'P_M6'] = 1.0
                
        # 3.2 Hidráulica:
        elif eap.startswith('3.2'):
            if any(term in desc for term in ['Tubo PVC Soldável', 'Tubo PVC Esgoto', 'Tubo PVC Pluvial', 'Joelho', 'Tê ', 'Curva', 'Junção', 'Registro de Gaveta', 'Registro de Pressão', 'Válvula de Retenção']):
                df.at[idx, 'P_M4'] = 1.0
            else:
                df.at[idx, 'P_M6'] = 1.0
                
        # 3.3 HVAC:
        elif eap.startswith('3.3'):
            if any(term in desc for term in ['Tubulação Cobre', 'Tubo PVC Condensado', 'Exaustor']):
                df.at[idx, 'P_M5'] = 1.0
            else:
                df.at[idx, 'P_M6'] = 1.0

    # Calcular valores monetários
    for m in range(1, 7):
        df[f'V_M{m}'] = (df['Preco_Total'] * df[f'P_M{m}']).round(2)

    # Ajuste de arredondamento de centavos para garantir que a soma seja rigorosamente igual a Preco_Total
    for idx, r in df.iterrows():
        soma_v = sum(r[f'V_M{m}'] for m in range(1, 7))
        diff = round(r['Preco_Total'] - soma_v, 2)
        if abs(diff) > 0.0001:
            # ajusta no último mês com valor
            for m in range(6, 0, -1):
                if df.at[idx, f'P_M{m}'] > 0:
                    df.at[idx, f'V_M{m}'] = round(df.at[idx, f'V_M{m}'] + diff, 2)
                    break

    return df, eap_col, desc_col

def gerar_csv(df, eap_col, desc_col):
    out_csv = os.path.join(OUTPUT_DIR, "CRONOGRAMA_FISICO_FINANCEIRO_TMULT.csv")
    
    cols_export = [
        eap_col, desc_col, 'Disciplina', 'Qtd Projeto', 'Unidade Proj', 'Preço Unitário (R$)', 'Custo Total (R$)',
        'P_M1', 'V_M1', 'P_M2', 'V_M2', 'P_M3', 'V_M3', 'P_M4', 'V_M4', 'P_M5', 'V_M5', 'P_M6', 'V_M6'
    ]
    
    df_export = df[cols_export].copy()
    
    # Renomear colunas para padrão amigável
    df_export.columns = [
        'Código EAP', 'Item / Descrição', 'Disciplina', 'Qtd Projeto', 'Unidade', 'Preço Unitário (R$)', 'Preço Total Turnkey (R$)',
        '% Mês 1', 'R$ Mês 1', '% Mês 2', 'R$ Mês 2', '% Mês 3', 'R$ Mês 3', '% Mês 4', 'R$ Mês 4', '% Mês 5', 'R$ Mês 5', '% Mês 6', 'R$ Mês 6'
    ]
    
    df_export.to_csv(out_csv, sep=';', index=False, encoding='utf-8-sig')
    print(f"-> CSV gerado com sucesso: {out_csv}")
    return out_csv

def gerar_excel(df, eap_col, desc_col):
    out_xlsx = os.path.join(OUTPUT_DIR, "CRONOGRAMA_FISICO_FINANCEIRO_TMULT.xlsx")
    wb = openpyxl.Workbook()
    
    # ==========================
    # ABA 1: RESUMO EXECUTIVO & CURVA S
    # ==========================
    ws1 = wb.active
    ws1.title = "Resumo Executivo & Curva S"
    ws1.views.sheetView[0].showGridLines = True
    
    # Cores Corporativas (Estilo Engenharia Portuária / Marinho & Ouro)
    NAVY_HEADER = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    GOLD_ACCENT = PatternFill(start_color="D99B26", end_color="D99B26", fill_type="solid")
    BLUE_LIGHT = PatternFill(start_color="E8EEF5", end_color="E8EEF5", fill_type="solid")
    GRAY_LIGHT = PatternFill(start_color="F2F4F7", end_color="F2F4F7", fill_type="solid")
    GREEN_LIGHT = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
    
    FONT_TITLE = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    FONT_SUBTITLE = Font(name="Calibri", size=11, italic=True, color="E8EEF5")
    FONT_HEADER = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    FONT_BOLD = Font(name="Calibri", size=11, bold=True, color="1B365D")
    FONT_REGULAR = Font(name="Calibri", size=11, color="333333")
    
    THIN_BORDER = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC')
    )
    DOUBLE_BOTTOM_BORDER = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='double', color='1B365D')
    )
    
    # Cabeçalho Principal
    ws1.merge_cells("A1:G2")
    ws1["A1"] = "EDIFÍCIO ADMINISTRATIVO TMULT (PORTO DO AÇU) — CRONOGRAMA FÍSICO-FINANCEIRO & CURVA S"
    ws1["A1"].fill = NAVY_HEADER
    ws1["A1"].font = FONT_TITLE
    ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws1.merge_cells("A3:G3")
    ws1["A3"] = "Linha de Base Oficial 01 (Baseline 01) | Prazo: 6 Meses (26 Semanas / 180 Dias) | Base Orçamentária: SINAPI SP 07/2026 Turnkey"
    ws1["A3"].fill = PatternFill(start_color="284B78", end_color="284B78", fill_type="solid")
    ws1["A3"].font = FONT_SUBTITLE
    ws1["A3"].alignment = Alignment(horizontal="center", vertical="center")
    
    # Tabela da Curva S
    headers_curva = ["Mês / Período", "Faturamento Mensal (R$)", "% Mensal", "Faturamento Acumulado (R$)", "% Financeiro Acumulado", "% Físico Acumulado"]
    row_curva = 5
    for col_idx, h in enumerate(headers_curva, start=2):
        cell = ws1.cell(row=row_curva, column=col_idx, value=h)
        cell.fill = NAVY_HEADER
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
    
    totais_mes = [df[f'V_M{m}'].sum() for m in range(1, 7)]
    tot_geral = sum(totais_mes)
    fisico_acum = [12.05, 30.20, 54.10, 69.85, 88.40, 100.00]
    
    acum_val = 0.0
    for m in range(1, 7):
        r_num = row_curva + m
        v = totais_mes[m-1]
        acum_val += v
        pct_m = v / tot_geral
        pct_fin_acum = acum_val / tot_geral
        
        ws1.cell(row=r_num, column=2, value=f"Mês {m}").alignment = Alignment(horizontal="center")
        ws1.cell(row=r_num, column=3, value=v).number_format = '"R$ "#,##0.00'
        ws1.cell(row=r_num, column=4, value=pct_m).number_format = '0.00%'
        ws1.cell(row=r_num, column=5, value=acum_val).number_format = '"R$ "#,##0.00'
        ws1.cell(row=r_num, column=6, value=pct_fin_acum).number_format = '0.00%'
        ws1.cell(row=r_num, column=7, value=fisico_acum[m-1] / 100.0).number_format = '0.00%'
        
        for c_idx in range(2, 8):
            cell = ws1.cell(row=r_num, column=c_idx)
            cell.font = FONT_REGULAR
            cell.border = THIN_BORDER
            if m % 2 == 0:
                cell.fill = GRAY_LIGHT
    
    # Linha Total Curva S
    r_total = row_curva + 7
    ws1.cell(row=r_total, column=2, value="TOTAL GLOBAL").alignment = Alignment(horizontal="center")
    ws1.cell(row=r_total, column=3, value=tot_geral).number_format = '"R$ "#,##0.00'
    ws1.cell(row=r_total, column=4, value=1.0).number_format = '0.00%'
    ws1.cell(row=r_total, column=5, value=tot_geral).number_format = '"R$ "#,##0.00'
    ws1.cell(row=r_total, column=6, value=1.0).number_format = '0.00%'
    ws1.cell(row=r_total, column=7, value=1.0).number_format = '0.00%'
    
    for c_idx in range(2, 8):
        cell = ws1.cell(row=r_total, column=c_idx)
        cell.fill = GREEN_LIGHT
        cell.font = FONT_BOLD
        cell.border = DOUBLE_BOTTOM_BORDER

    # Inserir Gráfico da Curva S no Excel
    chart = LineChart()
    chart.title = "Curva S de Avanço Planejado (Físico vs Financeiro)"
    chart.style = 13
    chart.y_axis.title = "Avanço Acumulado (%)"
    chart.x_axis.title = "Período (Meses)"
    chart.width = 18
    chart.height = 10
    
    # Referências para gráfico (Colunas 6 e 7: % Financeiro e % Físico)
    data_ref = Reference(ws1, min_col=6, min_row=row_curva, max_col=7, max_row=row_curva + 6)
    cats_ref = Reference(ws1, min_col=2, min_row=row_curva + 1, max_row=row_curva + 6)
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    
    ws1.add_chart(chart, "B15")
    
    # Ajustar larguras das colunas da Aba 1
    col_widths_ws1 = {1: 4, 2: 18, 3: 25, 4: 16, 5: 25, 6: 22, 7: 20}
    for col_idx, width in col_widths_ws1.items():
        ws1.column_dimensions[get_column_letter(col_idx)].width = width

    # ==========================
    # ABA 2: CRONOGRAMA ANALÍTICO (158 ITENS)
    # ==========================
    ws2 = wb.create_sheet(title="Cronograma Analítico")
    ws2.views.sheetView[0].showGridLines = True
    
    # Cabeçalho Aba 2
    ws2.merge_cells("A1:T2")
    ws2["A1"] = "OBRA TMULT — MATRIZ ANALÍTICA DE DISTRIBUIÇÃO MENSAL (158 ITENS DA EAP)"
    ws2["A1"].fill = NAVY_HEADER
    ws2["A1"].font = FONT_TITLE
    ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    headers_analitico = [
        "Código EAP", "Descrição do Pacote / Serviço", "Disciplina", "Qtd Proj", "Unid",
        "Preço Unit (R$)", "Preço Total Turnkey (R$)",
        "% M1", "R$ Mês 1", "% M2", "R$ Mês 2", "% M3", "R$ Mês 3",
        "% M4", "R$ Mês 4", "% M5", "R$ Mês 5", "% M6", "R$ Mês 6", "Total %"
    ]
    
    row_hdr = 4
    for col_idx, h in enumerate(headers_analitico, start=1):
        cell = ws2.cell(row=row_hdr, column=col_idx, value=h)
        cell.fill = NAVY_HEADER
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        
    row_idx = 5
    for i, r in df.iterrows():
        ws2.cell(row=row_idx, column=1, value=str(r[eap_col]).strip()).alignment = Alignment(horizontal="center")
        ws2.cell(row=row_idx, column=2, value=str(r[desc_col]).strip()).alignment = Alignment(horizontal="left")
        ws2.cell(row=row_idx, column=3, value=str(r['Disciplina']).strip()).alignment = Alignment(horizontal="center")
        ws2.cell(row=row_idx, column=4, value=r['Qtd Projeto']).number_format = '#,##0.00'
        ws2.cell(row=row_idx, column=5, value=str(r['Unidade Proj']).strip()).alignment = Alignment(horizontal="center")
        ws2.cell(row=row_idx, column=6, value=r['Preco_Unitario']).number_format = '"R$ "#,##0.00'
        ws2.cell(row=row_idx, column=7, value=r['Preco_Total']).number_format = '"R$ "#,##0.00'
        
        # Meses 1 a 6
        ws2.cell(row=row_idx, column=8, value=r['P_M1']).number_format = '0.00%'
        ws2.cell(row=row_idx, column=9, value=r['V_M1']).number_format = '"R$ "#,##0.00'
        ws2.cell(row=row_idx, column=10, value=r['P_M2']).number_format = '0.00%'
        ws2.cell(row=row_idx, column=11, value=r['V_M2']).number_format = '"R$ "#,##0.00'
        ws2.cell(row=row_idx, column=12, value=r['P_M3']).number_format = '0.00%'
        ws2.cell(row=row_idx, column=13, value=r['V_M3']).number_format = '"R$ "#,##0.00'
        ws2.cell(row=row_idx, column=14, value=r['P_M4']).number_format = '0.00%'
        ws2.cell(row=row_idx, column=15, value=r['V_M4']).number_format = '"R$ "#,##0.00'
        ws2.cell(row=row_idx, column=16, value=r['P_M5']).number_format = '0.00%'
        ws2.cell(row=row_idx, column=17, value=r['V_M5']).number_format = '"R$ "#,##0.00'
        ws2.cell(row=row_idx, column=18, value=r['P_M6']).number_format = '0.00%'
        ws2.cell(row=row_idx, column=19, value=r['V_M6']).number_format = '"R$ "#,##0.00'
        
        # Total % (Fórmula de soma)
        ws2.cell(row=row_idx, column=20, value=f"=H{row_idx}+J{row_idx}+L{row_idx}+N{row_idx}+P{row_idx}+R{row_idx}").number_format = '0.00%'
        
        for c in range(1, 21):
            cell = ws2.cell(row=row_idx, column=c)
            cell.font = FONT_REGULAR
            cell.border = THIN_BORDER
            if i % 2 == 1:
                cell.fill = GRAY_LIGHT
        row_idx += 1

    # Linha Totalizador
    ws2.cell(row=row_idx, column=1, value="TOTAL").alignment = Alignment(horizontal="center")
    ws2.cell(row=row_idx, column=2, value="TOTAL GERAL DO EMPREENDIMENTO (TURNKEY)").alignment = Alignment(horizontal="left")
    ws2.cell(row=row_idx, column=7, value=f"=SUM(G5:G{row_idx-1})").number_format = '"R$ "#,##0.00'
    
    ws2.cell(row=row_idx, column=9, value=f"=SUM(I5:I{row_idx-1})").number_format = '"R$ "#,##0.00'
    ws2.cell(row=row_idx, column=11, value=f"=SUM(K5:K{row_idx-1})").number_format = '"R$ "#,##0.00'
    ws2.cell(row=row_idx, column=13, value=f"=SUM(M5:M{row_idx-1})").number_format = '"R$ "#,##0.00'
    ws2.cell(row=row_idx, column=15, value=f"=SUM(O5:O{row_idx-1})").number_format = '"R$ "#,##0.00'
    ws2.cell(row=row_idx, column=17, value=f"=SUM(Q5:Q{row_idx-1})").number_format = '"R$ "#,##0.00'
    ws2.cell(row=row_idx, column=19, value=f"=SUM(S5:S{row_idx-1})").number_format = '"R$ "#,##0.00'
    
    ws2.cell(row=row_idx, column=8, value=f"=I{row_idx}/G{row_idx}").number_format = '0.00%'
    ws2.cell(row=row_idx, column=10, value=f"=K{row_idx}/G{row_idx}").number_format = '0.00%'
    ws2.cell(row=row_idx, column=12, value=f"=M{row_idx}/G{row_idx}").number_format = '0.00%'
    ws2.cell(row=row_idx, column=14, value=f"=O{row_idx}/G{row_idx}").number_format = '0.00%'
    ws2.cell(row=row_idx, column=16, value=f"=Q{row_idx}/G{row_idx}").number_format = '0.00%'
    ws2.cell(row=row_idx, column=18, value=f"=S{row_idx}/G{row_idx}").number_format = '0.00%'
    ws2.cell(row=row_idx, column=20, value=1.0).number_format = '0.00%'
    
    for c in range(1, 21):
        cell = ws2.cell(row=row_idx, column=c)
        cell.fill = GREEN_LIGHT
        cell.font = FONT_BOLD
        cell.border = DOUBLE_BOTTOM_BORDER

    # Larguras das Colunas Aba 2
    col_widths_ws2 = {
        1: 14, 2: 50, 3: 22, 4: 12, 5: 10, 6: 16, 7: 22,
        8: 10, 9: 18, 10: 10, 11: 18, 12: 10, 13: 18,
        14: 10, 15: 18, 16: 10, 17: 18, 18: 10, 19: 18, 20: 12
    }
    for col_idx, width in col_widths_ws2.items():
        ws2.column_dimensions[get_column_letter(col_idx)].width = width

    wb.save(out_xlsx)
    print(f"-> Excel Executivo gerado com sucesso: {out_xlsx}")
    return out_xlsx

def gerar_ms_project_xml():
    out_xml = os.path.join(OUTPUT_DIR, "CRONOGRAMA_TMULT_MSPROJECT.xml")
    
    # Carregar dados CPM determinísticos
    cpm_file = os.path.join(BASE_DIR, "scratch", "dados_cpm_tmult_180d.json")
    with open(cpm_file, "r", encoding="utf-8") as f:
        cpm_raw = json.load(f)
    
    start_date = datetime.date(2026, 10, 1)
    
    # Atividades e custos estimados agregados
    tasks = cpm_raw["atividades"]
    
    xml_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Project xmlns="http://schemas.microsoft.com/project">
    <Name>OBRA_TMULT_BASELINE_01</Name>
    <Title>Edifício Administrativo TMULT - Porto do Açu</Title>
    <StartDate>{start_date.isoformat()}T08:00:00</StartDate>
    <FinishDate>{(start_date + datetime.timedelta(days=180)).isoformat()}T17:00:00</FinishDate>
    <CalendarUID>1</CalendarUID>
    <DefaultStartTime>08:00:00</DefaultStartTime>
    <DefaultFinishTime>17:00:00</DefaultFinishTime>
    <MinutesPerDay>480</MinutesPerDay>
    <MinutesPerWeek>2400</MinutesPerWeek>
    <DaysPerMonth>20</DaysPerMonth>
    <Tasks>
"""
    
    # Tarefa 0 (Projeto Geral)
    xml_content += f"""        <Task>
            <UID>0</UID>
            <ID>0</ID>
            <Name>OBRA TMULT - EDIFÍCIO ADMINISTRATIVO (180 DIAS)</Name>
            <Type>1</Type>
            <CreateDate>{datetime.date.today().isoformat()}T08:00:00</CreateDate>
            <Start>{start_date.isoformat()}T08:00:00</Start>
            <Finish>{(start_date + datetime.timedelta(days=180)).isoformat()}T17:00:00</Finish>
            <Duration>PT1440H0M0S</Duration>
            <Summary>1</Summary>
            <Critical>1</Critical>
        </Task>
"""
    
    task_uid_map = {}
    current_day = 0
    for idx, t in enumerate(tasks, start=1):
        task_uid_map[t["id"]] = idx
        
    for idx, t in enumerate(tasks, start=1):
        dur_days = t["duracao_dias"]
        dur_hours = dur_days * 8
        
        # Datas estimadas
        t_start = start_date + datetime.timedelta(days=current_day)
        t_finish = t_start + datetime.timedelta(days=dur_days)
        current_day += dur_days if t["id"] in ["A01_MOB_CANTEIRO", "A02_ESCAV_INFRA", "A03_SAPATAS_CONC"] else 0
        
        preds_xml = ""
        for p in t.get("predecessoras", []):
            if p in task_uid_map:
                preds_xml += f"""            <PredecessorLink>
                <PredecessorUID>{task_uid_map[p]}</PredecessorUID>
                <Type>1</Type>
                <CrossProject>0</CrossProject>
                <LinkLag>0</LinkLag>
                <LagFormat>7</LagFormat>
            </PredecessorLink>
"""

        xml_content += f"""        <Task>
            <UID>{idx}</UID>
            <ID>{idx}</ID>
            <Name>{t["id"].replace('_', ' ')}</Name>
            <Active>1</Active>
            <Duration>PT{dur_hours}H0M0S</Duration>
            <Start>{t_start.isoformat()}T08:00:00</Start>
            <Finish>{t_finish.isoformat()}T17:00:00</Finish>
            <Critical>1</Critical>
{preds_xml}        </Task>
"""

    xml_content += """    </Tasks>
</Project>
"""
    with open(out_xml, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"-> XML MS Project gerado com sucesso: {out_xml}")
    return out_xml

def gerar_dashboard_html(df):
    out_html = os.path.join(OUTPUT_DIR, "CRONOGRAMA_DASHBOARD_INTERATIVO.html")
    
    totais_mes = [df[f'V_M{m}'].sum() for m in range(1, 7)]
    tot_geral = sum(totais_mes)
    acum_val = 0.0
    pct_fin_acum = []
    for v in totais_mes:
        acum_val += v
        pct_fin_acum.append(acum_val / tot_geral * 100)
    
    fisico_acum = [12.05, 30.20, 54.10, 69.85, 88.40, 100.00]
    meses = [f"Mês {m}" for m in range(1, 7)]
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=("Curva S Planejada: Avanço Físico vs Financeiro Acumulado", "Desembolso e Faturamento Mensal (R$)"),
        vertical_spacing=0.15
    )
    
    # Curva S
    fig.add_trace(
        go.Scatter(x=meses, y=fisico_acum, name="% Físico Acumulado", mode='lines+markers', line=dict(color='#1B365D', width=3), marker=dict(size=8)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=meses, y=pct_fin_acum, name="% Financeiro Acumulado", mode='lines+markers', line=dict(color='#D99B26', width=3, dash='dot'), marker=dict(size=8)),
        row=1, col=1
    )
    
    # Barras de Faturamento
    fig.add_trace(
        go.Bar(x=meses, y=totais_mes, name="Faturamento Mensal (R$)", marker_color='#284B78', text=[f"R$ {v:,.0f}" for v in totais_mes], textposition='auto'),
        row=2, col=1
    )
    
    fig.update_layout(
        title="<b>PMO VIRTUAL: DASHBOARD EXECUTIVO DO CRONOGRAMA — OBRA TMULT (PORTO DO AÇU)</b><br><sup>Baseline 01 | R$ 1.660.762,28 Turnkey | 180 Dias Corridos</sup>",
        height=750,
        showlegend=True,
        template="plotly_white",
        font=dict(family="Arial, sans-serif")
    )
    
    fig.write_html(out_html)
    print(f"-> Dashboard HTML Interativo gerado: {out_html}")
    return out_html

if __name__ == "__main__":
    print("=== INICIANDO GERAÇÃO DO PACOTE INTEGRADO DE CRONOGRAMA TMULT ===")
    df, eap_col, desc_col = carregar_e_distribuir_orcamento()
    gerar_csv(df, eap_col, desc_col)
    gerar_excel(df, eap_col, desc_col)
    gerar_ms_project_xml()
    gerar_dashboard_html(df)
    print("=== PACOTE INTEGRADO GERADO COM SUCESSO! ===")
