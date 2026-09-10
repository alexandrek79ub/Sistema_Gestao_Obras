#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Geração do Dossiê Executivo de Contratação da OBRA_TMULT:
1. Histograma de Mão de Obra (Headcount & Horas-Homem) -> 06_SST_E_RH
2. Histograma de Equipamentos e Instalações de Canteiro -> 04_PRODUCAO_E_AVANCO
3. Curva ABC Dupla (Composições de Serviços e Famílias de Insumos) -> 02_ORCAMENTO_BASE_E_CONTRATOS
"""

import os
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_ORCAMENTO = os.path.join(BASE_DIR, "projetos", "OBRA_TMULT", "02_ORCAMENTO_BASE_E_CONTRATOS")
DIR_PRODUCAO = os.path.join(BASE_DIR, "projetos", "OBRA_TMULT", "04_PRODUCAO_E_AVANCO")
DIR_RH = os.path.join(BASE_DIR, "projetos", "OBRA_TMULT", "06_SST_E_RH")

os.makedirs(DIR_ORCAMENTO, exist_ok=True)
os.makedirs(DIR_PRODUCAO, exist_ok=True)
os.makedirs(DIR_RH, exist_ok=True)

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

# ==============================================================================
# 1. HISTOGRAMA DE MÃO DE OBRA
# ==============================================================================
def gerar_histograma_mao_de_obra():
    print("-> Gerando Histograma de Mão de Obra...")
    
    dados_mo = [
        # Tipo, Função / Cargo, Categoria, Salário/Custo Base (R$/mês), M1, M2, M3, M4, M5, M6
        ["Gestão", "Engenheiro Residente (60%)", "Mensalista", 10680.00, 1, 1, 1, 1, 1, 1],
        ["Gestão", "Mestre de Obras Geral (100%)", "Mensalista", 7120.00, 1, 1, 1, 1, 1, 1],
        ["SST / Apoio", "Técnico de Segurança do Trabalho (TST)", "Mensalista", 4500.00, 1, 1, 1, 1, 1, 1],
        ["SST / Apoio", "Almoxarife / Apontador de Campo", "Mensalista", 3500.00, 1, 1, 1, 1, 1, 1],
        ["SST / Apoio", "Vigia Noturno / Segurança Patrimonial", "Mensalista", 3500.00, 1, 1, 1, 1, 1, 1],
        
        # Produção Civil
        ["Produção", "Pedreiro Oficial (Alvenaria / Reboco)", "Horista/Produção", 3200.00, 2, 2, 5, 4, 1, 1],
        ["Produção", "Ladrilhista / Azulejista (Porcelanato)", "Horista/Produção", 3400.00, 0, 0, 0, 0, 3, 0],
        ["Produção", "Carpinteiro de Fôrmas e Escoramento", "Horista/Produção", 3200.00, 0, 4, 0, 0, 0, 0],
        ["Produção", "Armador de Ferragens CA-50/CA-60", "Horista/Produção", 3200.00, 2, 3, 0, 0, 0, 0],
        ["Produção", "Montador de Estrutura Metálica / Telhadista", "Especialista", 3600.00, 0, 0, 3, 0, 0, 0],
        ["Produção", "Pintor Oficial Imobiliário", "Horista/Produção", 3100.00, 0, 0, 0, 0, 1, 4],
        ["Produção", "Servente de Obras / Ajudante Prático", "Horista/Produção", 2200.00, 4, 5, 5, 4, 2, 2],
        
        # Instalações e Especialidades
        ["Instalações", "Eletricista Instalador / Telecom", "Oficial", 3300.00, 0, 0, 0, 2, 2, 2],
        ["Instalações", "Encanador / Bombeiro Hidráulico", "Oficial", 3300.00, 0, 0, 0, 2, 1, 1],
        ["Instalações", "Mecânico / Montador de Climatização HVAC", "Especialista", 3800.00, 0, 0, 0, 0, 2, 2],
        ["Instalações", "Marceneiro / Montador de Esquadrias", "Oficial", 3200.00, 0, 0, 0, 0, 2, 0],
        
        # Logística Mecanizada & Pós-Obra
        ["Apoio", "Operador de Retroescavadeira / Máquinas", "Operador", 3600.00, 1, 0, 0, 0, 0, 0],
        ["Apoio", "Auxiliar de Limpeza Especializada Pós-Obra", "Apoio", 2100.00, 0, 0, 0, 0, 0, 2],
    ]
    
    cols = ["Grupo", "Função / Cargo", "Categoria", "Custo Base Ref (R$/mês)", "Mês 1", "Mês 2", "Mês 3", "Mês 4", "Mês 5", "Mês 6"]
    df_mo = pd.DataFrame(dados_mo, columns=cols)
    
    # Calcular totais mensais de Headcount e Horas-Homem (HH)
    # Assumindo jornada de 220h mensais por profissional
    totais_headcount = [df_mo[f"Mês {m}"].sum() for m in range(1, 7)]
    totais_hh = [hc * 220 for hc in totais_headcount]
    
    # Exportar CSV
    csv_path = os.path.join(DIR_RH, "HISTOGRAMA_MAO_DE_OBRA_TMULT.csv")
    df_mo.to_csv(csv_path, sep=';', index=False, encoding='utf-8-sig')
    
    # Exportar Excel com OpenPyXL
    xlsx_path = os.path.join(DIR_RH, "HISTOGRAMA_MAO_DE_OBRA_TMULT.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Histograma de Mão de Obra"
    ws.views.sheetView[0].showGridLines = True
    
    ws.merge_cells("A1:J2")
    ws["A1"] = "OBRA TMULT (PORTO DO AÇU) — HISTOGRAMA DE MÃO DE OBRA & HEADCOUNT MENSAL"
    ws["A1"].fill = NAVY_HEADER
    ws["A1"].font = FONT_TITLE
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws.merge_cells("A3:J3")
    ws["A3"] = "Planejamento Físico de Efetivo | 6 Meses (180 Dias) | Carga Horária Padrão: 220 Horas-Homem (HH) / mês"
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
        
    for r_idx, row_data in enumerate(dados_mo, start=6):
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
                
    # Linha Total Headcount
    r_hc = len(dados_mo) + 6
    ws.cell(row=r_hc, column=1, value="TOTAL").alignment = Alignment(horizontal="center")
    ws.cell(row=r_hc, column=2, value="HEADCOUNT TOTAL DE CAMPO (Operários + Gestão)").alignment = Alignment(horizontal="left")
    for m_idx, hc in enumerate(totais_headcount, start=5):
        ws.cell(row=r_hc, column=m_idx, value=hc).number_format = '#,##0'
        ws.cell(row=r_hc, column=m_idx).alignment = Alignment(horizontal="center")
        
    for c in range(1, 11):
        cell = ws.cell(row=r_hc, column=c)
        cell.fill = GOLD_ACCENT
        cell.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        cell.border = THIN_BORDER

    # Linha Total Horas-Homem (HH)
    r_hh = r_hc + 1
    ws.cell(row=r_hh, column=1, value="TOTAL HH").alignment = Alignment(horizontal="center")
    ws.cell(row=r_hh, column=2, value="TOTAL DE HORAS-HOMEM PREVISTAS (220h / profissional)").alignment = Alignment(horizontal="left")
    for m_idx, hh in enumerate(totais_hh, start=5):
        ws.cell(row=r_hh, column=m_idx, value=hh).number_format = '#,##0'
        ws.cell(row=r_hh, column=m_idx).alignment = Alignment(horizontal="center")
        
    for c in range(1, 11):
        cell = ws.cell(row=r_hh, column=c)
        cell.fill = GREEN_LIGHT
        cell.font = FONT_BOLD
        cell.border = DOUBLE_BOTTOM
        
    col_widths = {1: 14, 2: 44, 3: 18, 4: 22, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12}
    for c_idx, w in col_widths.items():
        ws.column_dimensions[get_column_letter(c_idx)].width = w
        
    wb.save(xlsx_path)
    print(f"   -> Salvo: {csv_path}")
    print(f"   -> Salvo: {xlsx_path}")
    return df_mo, totais_headcount, totais_hh

# ==============================================================================
# 2. HISTOGRAMA DE EQUIPAMENTOS
# ==============================================================================
def gerar_histograma_equipamentos():
    print("-> Gerando Histograma de Equipamentos...")
    
    dados_eq = [
        # Equipamento / Instalação Provisória, Capacidade / Modelo, Unidade, M1, M2, M3, M4, M5, M6, Observação Operacional
        ["Módulo Habitável Escritório / Reuniões", "Container Acoplado 6,00x2,40m c/ AC", "un", 1, 1, 1, 1, 1, 1, "Permanência integral 6 meses"],
        ["Módulo Vestiário / Sanitário NR-18", "Container 6,00x2,40m c/ chuveiros", "un", 1, 1, 1, 1, 1, 1, "Atende até 20 operários"],
        ["Módulo Refeitório NR-18", "Container 6,00x2,40m climatizado c/ mesas", "un", 1, 1, 1, 1, 1, 1, "Vivência e alimentação"],
        ["Módulo Almoxarifado / Ferramentaria", "Container Marítimo Dry 20 pés c/ prateleiras", "un", 1, 1, 1, 1, 1, 1, "Guarda de insumos e ferramentas"],
        ["Sanitários Químicos Portáteis", "Cabine Polietileno (Limpeza 2x/sem)", "un", 2, 2, 2, 2, 2, 2, "Apoio de campo"],
        ["Retroescavadeira 4x4 c/ Operador", "Tração 4x4, caçamba 1,0 m³", "un", 1, 0, 0, 0, 0, 0, "Escavação de sapatas e cavas"],
        ["Caminhão Basculante Traçado 12m³", "Eixos 6x4 caçamba basculante", "un", 1, 0, 0, 0, 0, 0, "Bota-fora de terra e entulho"],
        ["Compactador de Percussão (Sapo)", "Motor 4T Gasolina, força golpe 14 kN", "un", 1, 0, 0, 0, 0, 0, "Compactação fundo de cavas e valas"],
        ["Betoneira Elétrica 400 Litros", "Motor 2 CV Trifásico 220V", "un", 1, 1, 1, 1, 0, 0, "Argamassas e concreto magro"],
        ["Cimbramento e Escoramento Metálico", "Torres metálicas, forcados e escoras", "m²·m", 0, 888, 0, 0, 0, 0, "Suporte laje e vigas superiores"],
        ["Andaimes Tubulares Fachadeiros", "Quadros 1,50x1,00m c/ rodapé e guarda-corpo", "m²", 0, 0, 200, 200, 100, 0, "Alvenaria, reboco e cobertura"],
        ["Máquina de Projeção de Argamassa", "Rendimento 1,5 m³/h contínua", "un", 0, 0, 0, 1, 0, 0, "Aceleração emboço paulista"],
        ["Bomba Hidrostática de Teste", "Pressão até 25 bar c/ manômetro calibrado", "un", 0, 0, 0, 1, 0, 0, "Ensaio de estanqueidade 72h"],
        ["Plataforma Elevatória Tesoura Elétrica", "Altura trabalho 10m silenciosa", "un", 0, 0, 0, 0, 1, 1, "Dutos HVAC, iluminação e rede"],
        ["Bomba de Vácuo + Manifold Digital", "Bomba 10 CFM duplo estágio", "cj", 0, 0, 0, 0, 1, 1, "Instalação e comissionamento splits"],
        ["Caçambas Estacionárias de Entulho", "Capacidade 5 m³ (PGRCC)", "un", 2, 2, 2, 2, 2, 2, "Giro rotativo de resíduos"],
        ["Grupo Gerador Silenciado 50 kVA", "Diesel automático cabinado 70 dB", "un", 1, 1, 1, 0, 0, 0, "Apoio elétrico até ligação definitiva"],
    ]
    
    cols = ["Equipamento / Instalação Provisória", "Especificação / Modelo", "Unid", "Mês 1", "Mês 2", "Mês 3", "Mês 4", "Mês 5", "Mês 6", "Finalidade Operacional"]
    df_eq = pd.DataFrame(dados_eq, columns=cols)
    
    csv_path = os.path.join(DIR_PRODUCAO, "HISTOGRAMA_EQUIPAMENTOS_TMULT.csv")
    df_eq.to_csv(csv_path, sep=';', index=False, encoding='utf-8-sig')
    
    xlsx_path = os.path.join(DIR_PRODUCAO, "HISTOGRAMA_EQUIPAMENTOS_TMULT.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Histograma de Equipamentos"
    ws.views.sheetView[0].showGridLines = True
    
    ws.merge_cells("A1:J2")
    ws["A1"] = "OBRA TMULT (PORTO DO AÇU) — HISTOGRAMA DE EQUIPAMENTOS & INFRAESTRUTURA DE CANTEIRO"
    ws["A1"].fill = NAVY_HEADER
    ws["A1"].font = FONT_TITLE
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws.merge_cells("A3:J3")
    ws["A3"] = "Dimensionamento de Maquinário, Andaimes e Módulos Habitáveis NR-18 ao longo dos 6 Meses de Execução"
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
        
    for r_idx, row_data in enumerate(dados_eq, start=6):
        for c_idx, val in enumerate(row_data, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = FONT_REGULAR
            cell.border = THIN_BORDER
            if 4 <= c_idx <= 9:
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal="center")
            elif c_idx == 3:
                cell.alignment = Alignment(horizontal="center")
            else:
                cell.alignment = Alignment(horizontal="left")
            if r_idx % 2 == 1:
                cell.fill = GRAY_LIGHT
                
    col_widths = {1: 40, 2: 38, 3: 8, 4: 10, 5: 10, 6: 10, 7: 10, 8: 10, 9: 10, 10: 35}
    for c_idx, w in col_widths.items():
        ws.column_dimensions[get_column_letter(c_idx)].width = w
        
    wb.save(xlsx_path)
    print(f"   -> Salvo: {csv_path}")
    print(f"   -> Salvo: {xlsx_path}")
    return df_eq

# ==============================================================================
# 3. CURVA ABC DE COMPOSIÇÕES E INSUMOS
# ==============================================================================
def gerar_curva_abc_completa():
    print("-> Gerando Curva ABC de Serviços e Insumos...")
    
    # 3.1 Curva ABC de Serviços (Composições da EAP)
    orc_path = os.path.join(DIR_ORCAMENTO, "ORCAMENTO_BASE_CONSOLIDADO.csv")
    df_orc = pd.read_csv(orc_path, sep=';', encoding='utf-8')
    
    eap_col = [c for c in df_orc.columns if 'digo EAP' in c or 'EAP' in c][0]
    desc_col = [c for c in df_orc.columns if 'Descricao' in c or 'Item' in c][0]
    
    def parse_val(v):
        if isinstance(v, str):
            v = v.replace('R$', '').strip().replace('.', '').replace(',', '.')
        return float(v)
        
    df_orc['Preco_Total'] = df_orc['Custo Total (R$)'].apply(parse_val)
    df_orc['Preco_Unit'] = df_orc['Preço Unitário (R$)'].apply(parse_val)
    
    # Ordenar por Preço Total decrescente
    df_serv = df_orc.sort_values(by='Preco_Total', ascending=False).reset_index(drop=True)
    total_geral = df_serv['Preco_Total'].sum()
    
    df_serv['Pct_Individual'] = (df_serv['Preco_Total'] / total_geral) * 100
    df_serv['Pct_Acumulado'] = df_serv['Pct_Individual'].cumsum()
    
    # Classificação ABC
    # Faixa A: até 80% | Faixa B: 80% a 95% | Faixa C: 95% a 100%
    def classificar_abc(acum):
        if acum <= 80.0001:
            return 'A'
        elif acum <= 95.0001:
            return 'B'
        else:
            return 'C'
            
    df_serv['Classe_ABC'] = df_serv['Pct_Acumulado'].apply(classificar_abc)
    
    # 3.2 Curva ABC de Insumos Principais (Famílias Agregadas de Custo Direto)
    # Total Custo Direto: R$ 1.314.562,67
    dados_insumos = [
        # Família de Insumo, Tipo (Material/MO/Equip/Gestão), Custo Direto Total (R$), Qtd Macro, Unid, Participação (%)
        ["Mão de Obra de Canteiro & Vivência (Alimentação / Transporte / EPIs)", "Gestão/MO", 175565.82, 6.0, "mês", "EAP 1.0.5 e 1.0.6 (16 operários)"],
        ["Equipe Técnica & Supervisão (Engenheiro Residente + Mestre + TST)", "Gestão", 175200.00, 6.0, "mês", "EAP 1.0.1 e 1.0.2"],
        ["Argamassas e Serviços de Revestimento (Emboço / Reboco Paulista)", "Material/MO", 93265.17, 2122.88, "m²", "Argamassa usinada e aplicação"],
        ["Telhas Termoacústicas Trapezoidais Sandwich 30mm EPS", "Material", 86023.36, 381.29, "m²", "Chapa pré-pintada e núcleo EPS"],
        ["Aparelhos de Ar-Condicionado Split (Cassete 36k, Hi-Wall 18k/12k Inverter)", "Equipamento", 78027.30, 8.0, "un", "Equipamentos de climatização"],
        ["Blocos de Concreto Estrutural e Vedação (14x19x39cm)", "Material", 73592.48, 12733.0, "un", "Alvenaria e platibanda"],
        ["Concreto Usinado fck 30 MPa (Sapatas, Baldrames, Pilares, Vigas, Laje)", "Material", 48102.50, 61.44, "m³", "Fundações e supraestrutura"],
        ["Piso Porcelanato Retificado 60x60cm Polido/Acetinado", "Material", 45522.04, 368.40, "m²", "Pisos internos"],
        ["Esquadrias de Madeira (Portas) e Alumínio/Vidro (Janelas)", "Material/MO", 39336.56, 30.0, "cj", "Portas completas e janelas caixilho"],
        ["Locação de Módulos Habitáveis Containers NR-18 e Sanitários", "Equipamento", 38300.00, 6.0, "mês", "4 containers + 2 sanitários químicos"],
        ["Fôrmas de Compensado Resinado 17mm e Cimbramento Metálico", "Material", 37340.20, 480.0, "m²", "Madeiramento e escoras metálicas"],
        ["Aço CA-50 / CA-60 Cortado e Dobrado (Fundações e Lajes)", "Material", 36240.10, 3110.0, "kg", "Armaduras estruturais"],
        ["Vigotas Treliçadas TR 16745 e EPS para Lajes H12", "Material", 25673.16, 968.80, "m", "Laje pré-moldada"],
        ["Cabeamento Estruturado UTP Cat6 e Cabos Elétricos de Cobre Flexível", "Material", 34500.00, 3600.0, "m", "Infraestrutura de força e telecom"],
        ["Pintura Látex Acrílica 3 Demãos (Tintas, Selador, Massas e Lixas)", "Material", 25800.00, 2491.28, "m²", "Paredes internas e tetos"],
        ["Impermeabilização (Manta Asfáltica 4mm em Calhas e Tinta Asfáltica)", "Material", 18500.00, 220.0, "m²", "Baldrames, calhas e áreas molhadas"],
        ["Tubulações e Conexões PVC (Água Fria, Esgoto e Pluvial)", "Material", 16400.00, 450.0, "m", "Prumadas e ramais prediais"],
        ["Disjuntores, Quadros QDG/QDF e Painéis de Iluminação LED 60x60", "Material", 15500.00, 52.0, "cj", "Aparelhagem e luminárias"],
        ["Louças Sanitárias, Cubas, Metais Nobres e Acessórios", "Material", 14800.00, 24.0, "cj", "Bacias acopladas e torneiras"],
        ["Estrutura Metálica de Cobertura (Perfis U Enrijecidos e Calhas)", "Material", 11200.00, 400.0, "kg", "Terças e rufos galvanizados"],
        ["Contas de Consumo Provisórias de Canteiro (Energia / Água / Fibra)", "Gestão", 14100.00, 6.0, "mês", "Concessionárias locais"],
        ["Outros Insumos Menores e Conexões Secundárias", "Diversos", 26733.98, 1.0, "vb", "Fixações, parafusos, fitas, colas"],
    ]
    
    cols_ins = ["Família de Insumo / Recurso Chave", "Natureza de Custo", "Custo Direto Total (R$)", "Qtd Macro", "Unid", "Referência / Aplicação na Obra"]
    df_ins = pd.DataFrame(dados_insumos, columns=cols_ins)
    tot_ins = df_ins["Custo Direto Total (R$)"].sum()
    df_ins["Pct_Individual"] = (df_ins["Custo Direto Total (R$)"] / tot_ins) * 100
    df_ins["Pct_Acumulado"] = df_ins["Pct_Individual"].cumsum()
    df_ins["Classe_ABC"] = df_ins["Pct_Acumulado"].apply(classificar_abc)
    
    # Exportar CSV de Serviços e Insumos
    csv_serv_path = os.path.join(DIR_ORCAMENTO, "CURVA_ABC_SERVICOS_TMULT.csv")
    df_serv.to_csv(csv_serv_path, sep=';', index=False, encoding='utf-8-sig')
    
    csv_ins_path = os.path.join(DIR_ORCAMENTO, "CURVA_ABC_INSUMOS_TMULT.csv")
    df_ins.to_csv(csv_ins_path, sep=';', index=False, encoding='utf-8-sig')
    
    # Exportar Excel com OpenPyXL com 2 Abas (Composições e Insumos)
    xlsx_path = os.path.join(DIR_ORCAMENTO, "CURVA_ABC_SERVICOS_E_INSUMOS_TMULT.xlsx")
    wb = openpyxl.Workbook()
    
    # Aba 1: ABC Insumos
    ws1 = wb.active
    ws1.title = "Curva ABC Insumos"
    ws1.views.sheetView[0].showGridLines = True
    
    ws1.merge_cells("A1:I2")
    ws1["A1"] = "CURVA ABC DE FAMÍLIAS DE INSUMOS & RECURSOS — OBRA TMULT"
    ws1["A1"].fill = NAVY_HEADER
    ws1["A1"].font = FONT_TITLE
    ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws1.merge_cells("A3:I3")
    ws1["A3"] = f"Abertura Analítica do Custo Direto Total: R$ {tot_ins:,.2f} | Base SINAPI SP 07/2026"
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
            cell_abc.fill = PatternFill(start_color="FFD1D1", end_color="FFD1D1", fill_type="solid") # Vermelho claro
        elif r["Classe_ABC"] == 'B':
            cell_abc.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # Amarelo claro
        else:
            cell_abc.fill = PatternFill(start_color="D9EAD3", end_color="D9EAD3", fill_type="solid") # Verde claro
            
        for c in range(1, 9):
            ws1.cell(row=r_num, column=c).font = FONT_REGULAR
            ws1.cell(row=r_num, column=c).border = THIN_BORDER
            if idx % 2 == 1:
                ws1.cell(row=r_num, column=c).fill = GRAY_LIGHT
                
    # Linha Total Insumos
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

    # Aba 2: ABC Serviços (158 Itens)
    ws2 = wb.create_sheet(title="Curva ABC Serviços (158I)")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2.merge_cells("A1:J2")
    ws2["A1"] = "CURVA ABC DE COMPOSIÇÕES E PACOTES DE SERVIÇOS (158 ITENS DA EAP)"
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
        ws2.cell(row=r_num, column=4, value=str(r["Disciplina"]).strip()).alignment = Alignment(horizontal="center")
        ws2.cell(row=r_num, column=5, value=r["Qtd Projeto"]).number_format = '#,##0.00'
        ws2.cell(row=r_num, column=6, value=str(r["Unidade Proj"]).strip()).alignment = Alignment(horizontal="center")
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

if __name__ == "__main__":
    print("=== EXECUTANDO MOTOR DE DOSSIÊ DE CONTRATAÇÃO TMULT ===")
    gerar_histograma_mao_de_obra()
    gerar_histograma_equipamentos()
    gerar_curva_abc_completa()
    print("=== GERAÇÃO CONCLUÍDA COM SUCESSO! ===")
