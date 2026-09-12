#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========================================================================================
 👥 MOTOR UNIVERSAL DE SINCRONIZAÇÃO DO HISTOGRAMA DE MÃO DE OBRA (LEAN 5D)
==========================================================================================
Calcula e regenera de forma 100% dinâmica o Histograma de Mão de Obra (Headcount & Horas-Homem):
  1. Extrai o efetivo e especialidades de cada lote da Programação de Curto Prazo (Takt).
  2. Mapeia as datas de execução de cada lote para os meses correspondentes da obra.
  3. Aplica nivelamento Heijunka (pico de equipe simultânea por especialidade no mês).
  4. Suporta CRASHING / RUP: se uma equipe for aumentada para recuperar prazo,
     o histograma do mês correspondente é automaticamente incrementado.
  5. Mantém a equipe fixa de Gestão & SST (5 profissionais: Eng, Mestre, TST, Almoxarife, Vigia).
  6. Gera simultaneamente:
     - 06_SST_E_RH/dados_histograma_mo.json
     - 06_SST_E_RH/HISTOGRAMA_MAO_DE_OBRA_[SIGLA].csv
     - 06_SST_E_RH/HISTOGRAMA_MAO_DE_OBRA_[SIGLA].xlsx (com estilos e fórmulas)

Uso:
  python scripts/gerar_histograma_sincronizado.py --obra OBRA_TMULT
  python scripts/gerar_histograma_sincronizado.py --obra NOVA_OBRA
==========================================================================================
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime, timedelta
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Encoding UTF-8 para Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Estilos OpenPyXL
NAVY_HEADER = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
GRAY_LIGHT = PatternFill(start_color="F4F6F9", end_color="F4F6F9", fill_type="solid")
FONT_TITLE = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
FONT_HEADER = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
FONT_REGULAR = Font(name="Calibri", size=11, color="333333")

THIN_BORDER = Border(
    left=Side(style='thin', color='DDDDDD'),
    right=Side(style='thin', color='DDDDDD'),
    top=Side(style='thin', color='DDDDDD'),
    bottom=Side(style='thin', color='DDDDDD')
)

# Catálogo padrão de funções e custos de referência (SINDUSCON / CUB)
CATALOGO_FUNCOES = [
    # (Grupo, Função / Cargo, Categoria, Custo Base Ref R$/mês, chave_interna)
    ("Gestão", "Engenheiro Residente (60%)", "Mensalista", 10680.0, "eng_residente"),
    ("Gestão", "Mestre de Obras Geral (100%)", "Mensalista", 7120.0, "mestre_obras"),
    ("SST / Apoio", "Técnico de Segurança do Trabalho (TST)", "Mensalista", 4500.0, "tst"),
    ("SST / Apoio", "Almoxarife / Apontador de Campo", "Mensalista", 3500.0, "almoxarife"),
    ("SST / Apoio", "Vigia Noturno / Segurança Patrimonial", "Mensalista", 3500.0, "vigia"),
    ("Produção", "Pedreiro Oficial (Alvenaria / Reboco)", "Horista/Produção", 3200.0, "pedreiro"),
    ("Produção", "Ladrilhista / Azulejista (Porcelanato)", "Horista/Produção", 3400.0, "ladrilhista"),
    ("Produção", "Carpinteiro de Fôrmas e Escoramento", "Horista/Produção", 3200.0, "carpinteiro"),
    ("Produção", "Armador de Ferragens CA-50/CA-60", "Horista/Produção", 3200.0, "armador"),
    ("Produção", "Montador de Estrutura Metálica / Telhadista", "Especialista", 3600.0, "montador_metalico"),
    ("Produção", "Pintor Oficial Imobiliário", "Horista/Produção", 3100.0, "pintor"),
    ("Produção", "Servente de Obras / Ajudante Prático", "Horista/Produção", 2200.0, "servente"),
    ("Instalações", "Eletricista Instalador / Telecom", "Oficial", 3300.0, "eletricista"),
    ("Instalações", "Encanador / Bombeiro Hidráulico", "Oficial", 3300.0, "encanador"),
    ("Instalações", "Mecânico / Montador de Climatização HVAC", "Especialista", 3800.0, "hvac"),
    ("Instalações", "Marceneiro / Montador de Esquadrias", "Oficial", 3200.0, "esquadrias"),
    ("Apoio", "Operador de Retroescavadeira / Máquinas", "Operador", 3600.0, "operador_maquina"),
    ("Apoio", "Auxiliar de Limpeza Especializada Pós-Obra", "Apoio", 2100.0, "limpeza")
]

def parse_date_br(d_str):
    if not d_str or not isinstance(d_str, str):
        return None
    d_str = d_str.strip().replace('"', '')
    for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y'):
        try:
            return datetime.strptime(d_str, fmt)
        except ValueError:
            pass
    return None

def extrair_profissoes_equipe(equipe_desc, headcount_total):
    """
    Analisa a descrição da equipe do lote (ex: '3 Ladrilhistas + 3 Ajudantes (SUB-05)')
    e decompõe nas funções do catálogo, proporcionalmente ao headcount_total atual.
    """
    desc = equipe_desc.lower()
    matches = re.findall(r'(\d+)\s+([a-zá-ú\s]+)', desc)
    raw_counts = {}
    
    for qtd_str, cargo in matches:
        qtd = int(qtd_str)
        cargo = cargo.strip()
        if 'operador' in cargo:
            raw_counts['operador_maquina'] = raw_counts.get('operador_maquina', 0) + qtd
        elif 'armador' in cargo:
            raw_counts['armador'] = raw_counts.get('armador', 0) + qtd
        elif 'carpinteiro' in cargo:
            raw_counts['carpinteiro'] = raw_counts.get('carpinteiro', 0) + qtd
        elif 'pedreiro' in cargo or 'impermeabilizador' in cargo:
            raw_counts['pedreiro'] = raw_counts.get('pedreiro', 0) + qtd
        elif 'ladrilhista' in cargo or 'azulejista' in cargo:
            raw_counts['ladrilhista'] = raw_counts.get('ladrilhista', 0) + qtd
        elif 'montador' in cargo and ('metal' in cargo or 'especialista' in cargo):
            raw_counts['montador_metalico'] = raw_counts.get('montador_metalico', 0) + qtd
        elif 'esquadria' in cargo or 'marceneiro' in cargo:
            raw_counts['esquadrias'] = raw_counts.get('esquadrias', 0) + qtd
        elif 'eletricista' in cargo:
            raw_counts['eletricista'] = raw_counts.get('eletricista', 0) + qtd
        elif 'encanador' in cargo:
            raw_counts['encanador'] = raw_counts.get('encanador', 0) + qtd
        elif 'refrigera' in cargo or 'hvac' in cargo:
            raw_counts['hvac'] = raw_counts.get('hvac', 0) + qtd
        elif 'pintor' in cargo:
            raw_counts['pintor'] = raw_counts.get('pintor', 0) + qtd
        elif 'limpeza' in cargo:
            raw_counts['limpeza'] = raw_counts.get('limpeza', 0) + qtd
        elif 'servente' in cargo or 'ajudante' in cargo:
            raw_counts['servente'] = raw_counts.get('servente', 0) + qtd

    # Se não identificou por regex detalhado, usa heurística baseada no serviço/descrição
    if not raw_counts:
        if 'ladrilhista' in desc or 'porcelanato' in desc or 'cerâmica' in desc:
            half = max(1, headcount_total // 2)
            raw_counts['ladrilhista'] = half
            raw_counts['servente'] = max(1, headcount_total - half)
        elif 'pedreiro' in desc or 'alvenaria' in desc or 'reboco' in desc:
            half = max(1, headcount_total // 2)
            raw_counts['pedreiro'] = half
            raw_counts['servente'] = max(1, headcount_total - half)
        elif 'pintor' in desc or 'pintura' in desc:
            half = max(1, headcount_total // 2)
            raw_counts['pintor'] = half
            raw_counts['servente'] = max(1, headcount_total - half)
        elif 'eletric' in desc:
            half = max(1, headcount_total // 2)
            raw_counts['eletricista'] = half
            raw_counts['servente'] = max(1, headcount_total - half)
        elif 'encanador' in desc or 'hidrául' in desc:
            half = max(1, headcount_total // 2)
            raw_counts['encanador'] = half
            raw_counts['servente'] = max(1, headcount_total - half)
        elif 'hvac' in desc or 'climatiza' in desc:
            half = max(1, headcount_total // 2)
            raw_counts['hvac'] = half
            raw_counts['servente'] = max(1, headcount_total - half)
        elif 'limpeza' in desc:
            raw_counts['limpeza'] = max(1, headcount_total - 1)
        else:
            raw_counts['servente'] = headcount_total

    # Ajuste proporcional se o headcount_total foi alterado por crashing
    soma_raw = sum(raw_counts.values())
    if soma_raw > 0 and headcount_total > 0 and soma_raw != headcount_total:
        fator = headcount_total / soma_raw
        dist = {}
        for k, v in raw_counts.items():
            dist[k] = max(1, int(round(v * fator)))
        # Ajuste fino da soma
        diff = headcount_total - sum(dist.values())
        if diff != 0:
            alvo = 'servente' if 'servente' in dist else list(dist.keys())[0]
            dist[alvo] = max(1, dist[alvo] + diff)
    else:
        dist = raw_counts

    return dist

def recalcular_histograma_obra(obra, base_dir=None, prazo_meses=6):
    """
    Função Master que lê a programação de curto prazo e recalcula:
      1. dados_histograma_mo.json
      2. HISTOGRAMA_MAO_DE_OBRA_[SIGLA].csv
      3. HISTOGRAMA_MAO_DE_OBRA_[SIGLA].xlsx
    """
    if not base_dir:
        base_dir = os.path.join(ROOT_DIR, 'projetos', obra)

    sigla = obra.replace('OBRA_', '')
    dir_planejamento = os.path.join(base_dir, '03_PLANEJAMENTO_E_CRONOGRAMA')
    dir_rh = os.path.join(base_dir, '06_SST_E_RH')
    os.makedirs(dir_rh, exist_ok=True)

    # Identificar arquivo de curto prazo
    prog_files = [
        os.path.join(dir_planejamento, f'PROGRAMACAO_CURTO_PRAZO_{obra}.csv'),
        os.path.join(dir_planejamento, f'PROGRAMACAO_CURTO_PRAZO_{sigla}.csv'),
        os.path.join(dir_planejamento, 'PROGRAMACAO_CURTO_PRAZO_OBRA_TMULT.csv'),
        os.path.join(dir_planejamento, 'PROGRAMACAO_CURTO_PRAZO_TMULT.csv')
    ]
    prog_path = next((f for f in prog_files if os.path.exists(f)), None)
    if not prog_path:
        print(f"[AVISO] Arquivo de programação de curto prazo não encontrado para '{obra}'.")
        return False

    # Ler dados dos lotes
    df_lotes = pd.read_csv(prog_path, sep=';', dtype=str).fillna('')
    if df_lotes.empty:
        print("[AVISO] Planilha de curto prazo vazia.")
        return False

    # Determinar datas extremas e marcos mensais
    datas_inicio = []
    for d in df_lotes['DATA_INICIO']:
        dt = parse_date_br(d)
        if dt:
            datas_inicio.append(dt)

    d_inicio_obra = min(datas_inicio) if datas_inicio else datetime(2026, 10, 1)

    # Definir janelas mensais
    janelas_meses = []
    cur_ano = d_inicio_obra.year
    cur_mes = d_inicio_obra.month

    for m in range(1, prazo_meses + 1):
        d_ini_mes = datetime(cur_ano, cur_mes, 1)
        if cur_mes == 12:
            prox_ano = cur_ano + 1
            prox_mes = 1
        else:
            prox_ano = cur_ano
            prox_mes = cur_mes + 1
        
        d_fim_mes = datetime(prox_ano, prox_mes, 1) - timedelta(days=1)
        if m == prazo_meses:
            d_fim_mes = d_fim_mes + timedelta(days=60)

        janelas_meses.append({
            "mes_num": m,
            "d_ini": d_ini_mes,
            "d_fim": d_fim_mes,
            "nome": f"Mês {m}"
        })
        
        cur_ano = prox_ano
        cur_mes = prox_mes

    # Inicializar contadores por especialidade para cada mês (Heijunka / pico)
    picos_por_mes = {m: {} for m in range(1, prazo_meses + 1)}

    for _, row in df_lotes.iterrows():
        d_ini_lote = parse_date_br(row.get('DATA_INICIO'))
        d_fim_lote = parse_date_br(row.get('DATA_FIM'))

        try:
            hc_lote = int(row.get('HEADCOUNT_PREVISTO', '4'))
        except ValueError:
            hc_lote = 4

        equipe_desc = row.get('EQUIPE_PREVISTA', '')
        profissoes_lote = extrair_profissoes_equipe(equipe_desc, hc_lote)

        # Identificar em quais meses este lote ocorre
        meses_atingidos = set()
        
        # 1. Se tem coluna SEMANA (ex: 'Semana 05')
        semana_str = row.get('SEMANA', '')
        m_sem = re.search(r'semana\s*0?(\d+)', semana_str.lower())
        if m_sem:
            w = int(m_sem.group(1))
            m_calc = min(prazo_meses, max(1, (w - 1) // 4 + 1))
            meses_atingidos.add(m_calc)

        # 2. Se tem datas de início e término válidas
        if d_ini_lote and d_fim_lote:
            for janela in janelas_meses:
                m = janela['mes_num']
                if not (d_fim_lote < janela['d_ini'] or d_ini_lote > janela['d_fim']):
                    meses_atingidos.add(m)

        if not meses_atingidos:
            meses_atingidos.add(1)

        for m in meses_atingidos:
            if m <= prazo_meses:
                for cargo_key, qtd in profissoes_lote.items():
                    picos_por_mes[m][cargo_key] = max(picos_por_mes[m].get(cargo_key, 0), int(qtd))

    # Construir a matriz final dados_mo com inteiros nativos
    dados_mo = []
    for grupo, cargo, categoria, custo, cargo_key in CATALOGO_FUNCOES:
        linha = [grupo, cargo, categoria, float(custo)]
        for m in range(1, prazo_meses + 1):
            if grupo == "Gestão":
                val = 1 # Fixo 1 Eng Residente e 1 Mestre
            elif grupo == "SST / Apoio":
                val = 1 # Fixo 1 TST, 1 Almoxarife, 1 Vigia
            else:
                val = int(picos_por_mes[m].get(cargo_key, 0))
            linha.append(int(val))
        dados_mo.append(linha)

    # 1. Salvar dados_histograma_mo.json
    json_path = os.path.join(dir_rh, 'dados_histograma_mo.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(dados_mo, f, indent=2, ensure_ascii=False)
    print(f"✔ JSON do histograma atualizado: {json_path}")

    # 2. Salvar HISTOGRAMA_MAO_DE_OBRA_[SIGLA].csv
    cols = ["Grupo", "Função / Cargo", "Categoria", "Custo Base Ref (R$/mês)"] + [f"Mês {m}" for m in range(1, prazo_meses + 1)]
    df_mo = pd.DataFrame(dados_mo, columns=cols)
    csv_path = os.path.join(dir_rh, f"HISTOGRAMA_MAO_DE_OBRA_{sigla}.csv")
    df_mo.to_csv(csv_path, sep=';', index=False, encoding='utf-8-sig')
    print(f"✔ CSV do histograma atualizado: {csv_path}")

    # 3. Salvar HISTOGRAMA_MAO_DE_OBRA_[SIGLA].xlsx com OpenPyXL
    totais_headcount = [df_mo[f"Mês {m}"].sum() for m in range(1, prazo_meses + 1)]
    totais_hh = [hc * 220 for hc in totais_headcount]

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
    ws["A3"] = f"Planejamento Físico de Efetivo | Sincronizado com Takt & LOB | Carga Horária Padrão: 220 HH / mês"
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

    r_hc = len(dados_mo) + 6
    ws.cell(row=r_hc, column=1, value="TOTAL").alignment = Alignment(horizontal="center")
    ws.cell(row=r_hc, column=2, value="HEADCOUNT TOTAL DE CAMPO (Operários + Gestão)").alignment = Alignment(horizontal="left")
    for m_idx, hc in enumerate(totais_headcount, start=5):
        c = ws.cell(row=r_hc, column=m_idx, value=hc)
        c.font = Font(name="Calibri", size=11, bold=True, color="1B365D")
        c.fill = PatternFill(start_color="D99B26", end_color="D99B26", fill_type="solid")
        c.alignment = Alignment(horizontal="center")
        c.border = THIN_BORDER

    r_hh = r_hc + 1
    ws.cell(row=r_hh, column=1, value="TOTAL").alignment = Alignment(horizontal="center")
    ws.cell(row=r_hh, column=2, value="TOTAL DE HORAS-HOMEM PREVISTAS (HH/mês)").alignment = Alignment(horizontal="left")
    for m_idx, hh in enumerate(totais_hh, start=5):
        c = ws.cell(row=r_hh, column=m_idx, value=hh)
        c.font = Font(name="Calibri", size=11, bold=True, color="1B365D")
        c.number_format = '#,##0" HH"'
        c.fill = PatternFill(start_color="E8EEF5", end_color="E8EEF5", fill_type="solid")
        c.alignment = Alignment(horizontal="center")
        c.border = THIN_BORDER

    ws.column_dimensions['A'].width = 16
    ws.column_dimensions['B'].width = 44
    ws.column_dimensions['C'].width = 18
    ws.column_dimensions['D'].width = 24
    for m in range(1, prazo_meses + 1):
        ws.column_dimensions[get_column_letter(4 + m)].width = 12

    wb.save(xlsx_path)
    print(f"✔ Planilha XLSX do histograma gerada: {xlsx_path}")
    print(f"  Headcount por Mês: {[int(x) for x in totais_headcount]}")
    print(f"  Horas-Homem (HH):  {[int(x) for x in totais_hh]}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Motor de Sincronização do Histograma de Mão de Obra.")
    parser.add_argument("--obra", type=str, default="OBRA_TMULT", help="Nome da pasta da obra")
    parser.add_argument("--prazo-meses", type=int, default=6, help="Prazo da obra em meses")
    args = parser.parse_args()

    recalcular_histograma_obra(args.obra, prazo_meses=args.prazo_meses)

if __name__ == "__main__":
    main()
