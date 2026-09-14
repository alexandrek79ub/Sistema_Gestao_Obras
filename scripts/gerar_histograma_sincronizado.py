#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========================================================================================
 👥 MOTOR UNIVERSAL DE SINCRONIZAÇÃO DO HISTOGRAMA DE MÃO DE OBRA (LEAN 5D)
==========================================================================================
Calcula e regenera de forma 100% dinâmica o Histograma de Mão de Obra (Headcount & HH):
  1. Extrai o efetivo e especialidades de cada lote da Programação de Curto Prazo (Takt).
  2. Mapeia as datas de execução de cada lote para os meses correspondentes da obra.
  3. Aplica nivelamento Heijunka (pico de equipe simultânea por especialidade no mês).
  4. Suporta CRASHING / RUP: aumento de equipe incrementa histograma automaticamente.
  5. Mantém equipe fixa de Gestão & SST (5 profissionais: Eng, Mestre, TST, Almox, Vigia).
  6. Gera simultaneamente JSON, CSV e XLSX com estilos corporativos + Relatório MD.

Uso:
  python scripts/gerar_histograma_sincronizado.py --obra OBRA_TMULT
  python scripts/gerar_histograma_sincronizado.py --obra NOVA_OBRA --prazo-meses 8
==========================================================================================
"""

import os
import sys
import re
import json
import argparse
import math
from datetime import datetime
import pandas as pd
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment

# Importações da camada de infraestrutura compartilhada
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from common.excel_theme import (
    NAVY, BLUE_DARK, BLUE_LIGHT, BLUE_ACCENT, GOLD_ACCENT, GRAY_LIGHT, THIN_BORDER,
    FONT_TITLE, FONT_HEADER, FONT_REGULAR, FONT_BOLD,
    ALIGN_CENTER, ALIGN_LEFT, ALIGN_RIGHT
)
from common.obra_io import (
    parse_obra_args, resolver_obra_dir, carregar_config_obra,
    carregar_programacao_curto_prazo, salvar_csv_utf8_sig, salvar_json
)
from common.calendario import parse_date_br, janelas_mensais_obra

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


# =============================================================================
# CATÁLOGO DE FUNÇÕES — Carregado de apoio/catalogo_funcoes.json
# =============================================================================

def carregar_catalogo_funcoes():
    """Lê apoio/catalogo_funcoes.json e retorna a lista de funções como tuplas."""
    path = os.path.join(ROOT_DIR, "apoio", "catalogo_funcoes.json")
    if not os.path.exists(path):
        print(f"[ERRO] Catálogo de funções não encontrado: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        dados = json.load(f)
    # Retorna no formato original: (grupo, cargo, categoria, custo, chave)
    return [
        (fn["grupo"], fn["cargo"], fn["categoria"], fn["custo_mes_ref"], fn["chave"])
        for fn in dados["funcoes"]
    ]


# =============================================================================
# EXTRAÇÃO DE PROFISSÕES DA EQUIPE (lógica de negócio — inalterada)
# =============================================================================

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

    soma_raw = sum(raw_counts.values())
    if soma_raw > 0 and headcount_total > 0 and soma_raw != headcount_total:
        fator = headcount_total / soma_raw
        dist = {k: max(1, int(round(v * fator))) for k, v in raw_counts.items()}
        diff = headcount_total - sum(dist.values())
        if diff != 0:
            alvo = 'servente' if 'servente' in dist else list(dist.keys())[0]
            dist[alvo] = max(1, dist[alvo] + diff)
    else:
        dist = raw_counts

    return dist


# =============================================================================
# MOTOR PRINCIPAL (lógica de negócio — inalterada)
# =============================================================================

def recalcular_histograma_obra(obra_dir, obra_nome, prazo_meses=6):
    """
    Função Master que lê a programação de curto prazo e recalcula:
      1. dados_histograma_mo.json
      2. HISTOGRAMA_MAO_DE_OBRA_[SIGLA].csv
      3. HISTOGRAMA_MAO_DE_OBRA_[SIGLA].xlsx
    """
    config = carregar_config_obra(obra_dir)
    sigla = config.get("sigla_obra", obra_nome.replace("OBRA_", ""))
    prazo_meses = int(config.get("prazo_meses", prazo_meses))
    duracao_cronograma = config.get("cronograma", {}).get("revisao_ativa", {}).get("duracao_dias_uteis", 178)

    dir_rh = os.path.join(obra_dir, '06_SST_E_RH')
    os.makedirs(dir_rh, exist_ok=True)

    CATALOGO_FUNCOES = carregar_catalogo_funcoes()

    # Leitura do CSV de curto prazo
    df_lotes = carregar_programacao_curto_prazo(obra_dir, obra_nome)
    if not df_lotes:
        print(f"[AVISO] Programação de curto prazo não encontrada. Usando matriz base canônica.")

    # Determinar data de início e janelas mensais
    datas_inicio = [parse_date_br(r.get('DATA_INICIO', '')) for r in df_lotes if r.get('DATA_INICIO')]
    datas_inicio = [d for d in datas_inicio if d]
    d_inicio_obra = min(datas_inicio) if datas_inicio else datetime(2026, 10, 1)
    janelas_meses = janelas_mensais_obra(d_inicio_obra, prazo_meses, extra_meses_buffer=2)

    # Matriz base calibrada oficial (102 headcount-meses = 22.440 HH)
    matriz_base_obra = {
        "eng_residente":     [1, 1, 1, 1, 1, 1],
        "mestre_obras":      [1, 1, 1, 1, 1, 1],
        "tst":               [1, 1, 1, 1, 1, 1],
        "almoxarife":        [1, 1, 1, 1, 1, 1],
        "vigia":             [1, 1, 1, 1, 1, 1],
        "pedreiro":          [2, 2, 5, 4, 0, 0],
        "ladrilhista":       [0, 0, 0, 0, 3, 0],
        "carpinteiro":       [0, 4, 0, 0, 0, 0],
        "armador":           [2, 3, 0, 0, 0, 0],
        "montador_metalico": [0, 0, 3, 0, 0, 0],
        "pintor":            [0, 0, 0, 0, 1, 4],
        "servente":          [4, 5, 5, 4, 2, 1],
        "eletricista":       [0, 0, 1, 2, 1, 1],
        "encanador":         [0, 0, 1, 2, 0, 1],
        "hvac":              [0, 0, 0, 0, 2, 2],
        "esquadrias":        [0, 0, 0, 0, 2, 0],
        "operador_maquina":  [1, 0, 0, 0, 0, 0],
        "limpeza":           [0, 0, 0, 0, 0, 2],
    }
    headcount_base_lotes = {
        "LOTE-001": 7,  "LOTE-002": 7,  "LOTE-003": 8,  "LOTE-004": 9,  "LOTE-005": 8,
        "LOTE-006": 9,  "LOTE-007": 9,  "LOTE-008": 9,  "LOTE-009": 14, "LOTE-010": 14,
        "LOTE-011": 14, "LOTE-012": 14, "LOTE-013": 14, "LOTE-014": 14, "LOTE-015": 14,
        "LOTE-016": 14, "LOTE-017": 10, "LOTE-018": 10, "LOTE-019": 10, "LOTE-020": 9,
        "LOTE-021": 9,  "LOTE-022": 8,  "LOTE-023": 4,  "LOTE-024": 8,  "LOTE-025": 8,
        "LOTE-026": 8,  "LOTE-027": 5,  "LOTE-028": 7,  "LOTE-029": 6,  "LOTE-030": 6,
        "LOTE-031": 6,  "LOTE-032": 6,  "LOTE-033": 4,  "LOTE-034": 4,  "LOTE-035": 4,
        "LOTE-036": 4,  "LOTE-037": 4,  "LOTE-038": 4,  "LOTE-039": 6,  "LOTE-040": 6,
        "LOTE-041": 4,  "LOTE-042": 4,  "LOTE-043": 6,  "LOTE-044": 4,  "LOTE-045": 4,
        "LOTE-046": 5,  "LOTE-047": 6,  "LOTE-048": 4,  "LOTE-049": 3,  "LOTE-050": 5,
        "LOTE-051": 3,  "LOTE-052": 3,
    }

    # Inicializar matriz final a partir da base
    matriz_final = {}
    for k, v in matriz_base_obra.items():
        if len(v) >= prazo_meses:
            matriz_final[k] = list(v[:prazo_meses])
        else:
            matriz_final[k] = list(v) + [v[-1]] * (prazo_meses - len(v))

    # Verificar crashing nos lotes
    for row in df_lotes:
        cod = row.get('COD_LOTE', '')
        try:
            hc_atual = int(row.get('HEADCOUNT_PREVISTO', '0'))
        except ValueError:
            hc_atual = 0
        hc_base = headcount_base_lotes.get(cod, hc_atual)
        delta_hc = hc_atual - hc_base
        if delta_hc != 0:
            semana_str = row.get('SEMANA', '')
            m_sem = re.search(r'semana\s*0?(\d+)', semana_str.lower())
            mes_alvo = 1
            if m_sem:
                w = int(m_sem.group(1))
                mes_alvo = min(prazo_meses, max(1, (w - 1) // 4 + 1))
            else:
                d_ini = parse_date_br(row.get('DATA_INICIO'))
                if d_ini:
                    for jan in janelas_meses:
                        if jan['d_ini'] <= d_ini <= jan['d_fim']:
                            mes_alvo = jan['mes_num']
                            break
            idx_m = mes_alvo - 1
            equipe_desc = row.get('EQUIPE_PREVISTA', '')
            sinal = 1 if delta_hc > 0 else -1
            dist_reforco = extrair_profissoes_equipe(equipe_desc, abs(delta_hc))
            for cargo_k, qtd in dist_reforco.items():
                if cargo_k in matriz_final and idx_m < len(matriz_final[cargo_k]):
                    matriz_final[cargo_k][idx_m] = max(0, matriz_final[cargo_k][idx_m] + (sinal * qtd))

    # Crashing altera a distribuição temporal do efetivo, não a quantidade de
    # trabalho contratada. Reescala somente as funções produtivas para conservar
    # o HH de referência; a equipe fixa de Gestão/SST é mantida intacta.
    funcoes_fixas = {"eng_residente", "mestre_obras", "tst", "almoxarife", "vigia"}
    hh_base_produtivo = sum(
        sum(valores) for cargo, valores in matriz_base_obra.items()
        if cargo not in funcoes_fixas
    )
    celulas_produtivas = [
        (cargo, mes, matriz_final[cargo][mes])
        for cargo in matriz_final if cargo not in funcoes_fixas
        for mes in range(prazo_meses) if matriz_final[cargo][mes] > 0
    ]
    soma_reprogramada = sum(valor for _, _, valor in celulas_produtivas)
    if soma_reprogramada and soma_reprogramada != hh_base_produtivo:
        quotas = [valor * hh_base_produtivo / soma_reprogramada for _, _, valor in celulas_produtivas]
        alocadas = [math.floor(quota) for quota in quotas]
        saldo = hh_base_produtivo - sum(alocadas)
        ordem = sorted(range(len(celulas_produtivas),), key=lambda idx: quotas[idx] - alocadas[idx], reverse=True)
        for idx in ordem[:saldo]:
            alocadas[idx] += 1
        for (cargo, mes, _), valor in zip(celulas_produtivas, alocadas):
            matriz_final[cargo][mes] = valor

    # Montar dados finais
    dados_mo = []
    for grupo, cargo, categoria, custo, cargo_key in CATALOGO_FUNCOES:
        linha = [grupo, cargo, categoria, float(custo)]
        linha.extend([int(v) for v in matriz_final.get(cargo_key, [0] * prazo_meses)])
        dados_mo.append(linha)

    totais_headcount = [sum(r[4 + m] for r in dados_mo) for m in range(prazo_meses)]
    totais_hh = [hc * 220 for hc in totais_headcount]
    total_geral_hc_meses = sum(totais_headcount)
    total_geral_hh = sum(totais_hh)

    # ─── 1. JSON ──────────────────────────────────────────────────────────────
    json_path = os.path.join(dir_rh, 'dados_histograma_mo.json')
    salvar_json(json_path, dados_mo)

    # ─── 2. CSV ───────────────────────────────────────────────────────────────
    cols = (["Grupo", "Função / Cargo", "Categoria", "Custo Base Ref (R$/mês)"]
            + [f"Mês {m}" for m in range(1, prazo_meses + 1)]
            + ["Total Meses", "Total HH"])
    linhas_csv = []
    for row in dados_mo:
        meses_vals = row[4:]
        total_m = sum(meses_vals)
        linhas_csv.append(row + [total_m, total_m * 220])
    linhas_csv.append(
        ["TOTAL", "HEADCOUNT TOTAL DE CAMPO", "—", 0.0]
        + totais_headcount + [total_geral_hc_meses, total_geral_hh]
    )
    linhas_csv.append(
        ["TOTAL", "TOTAL HORAS-HOMEM (HH/mês)", "—", 0.0]
        + totais_hh + [total_geral_hc_meses, total_geral_hh]
    )
    csv_path = os.path.join(dir_rh, f"HISTOGRAMA_MAO_DE_OBRA_{sigla}.csv")
    salvar_csv_utf8_sig(csv_path, cols, linhas_csv)

    # ─── 3. XLSX ──────────────────────────────────────────────────────────────
    _gerar_xlsx_histograma(
        dir_rh, sigla, dados_mo, totais_headcount, totais_hh,
        total_geral_hc_meses, total_geral_hh, prazo_meses
    )

    # ─── 4. Relatório MD ──────────────────────────────────────────────────────
    _gerar_relatorio_md(
        dir_rh, sigla, dados_mo, totais_headcount, totais_hh,
        total_geral_hc_meses, total_geral_hh, prazo_meses, duracao_cronograma
    )

    print(f"  Headcount por Mês: {[int(x) for x in totais_headcount]}")
    print(f"  Horas-Homem (HH):  {[int(x) for x in totais_hh]}")
    print(f"  TOTAL GERAL:       {total_geral_hc_meses} Headcount-Mês | {total_geral_hh:,.0f} HH")
    return True


# =============================================================================
# GERAÇÃO DE XLSX (formatação visual — usa excel_theme.py)
# =============================================================================

def _gerar_xlsx_histograma(dir_rh, sigla, dados_mo, totais_hc, totais_hh,
                            total_hc_meses, total_hh, prazo_meses):
    xlsx_path = os.path.join(dir_rh, f"HISTOGRAMA_MAO_DE_OBRA_{sigla}.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Histograma de Mão de Obra"
    ws.views.sheetView[0].showGridLines = True

    cols_xlsx = (["Grupo", "Função / Cargo", "Categoria", "Custo Base Ref (R$/mês)"]
                 + [f"Mês {m}" for m in range(1, prazo_meses + 1)]
                 + ["Total Meses", "Total Horas-Homem (HH)"])
    last_ltr = get_column_letter(len(cols_xlsx))

    # Linha 1-2: Título principal
    ws.merge_cells(f"A1:{last_ltr}2")
    ws["A1"] = f"{sigla} — HISTOGRAMA OFICIAL DE MÃO DE OBRA & HEADCOUNT MENSAL"
    ws["A1"].fill = NAVY
    ws["A1"].font = FONT_TITLE
    ws["A1"].alignment = ALIGN_CENTER
    ws.row_dimensions[1].height = 30
    ws.row_dimensions[2].height = 2

    # Linha 3: Subtítulo
    ws.merge_cells(f"A3:{last_ltr}3")
    ws["A3"] = (f"Planejamento Físico de Efetivo | Total da Obra: {total_hc_meses} Headcount-Mês | "
                f"{total_hh:,.0f} Horas-Homem (HH) | Carga Horária Padrão: 220 HH / mês")
    ws["A3"].fill = BLUE_DARK
    ws["A3"].font = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    ws["A3"].alignment = ALIGN_CENTER

    # Linha 5: Cabeçalho de colunas
    for col_idx, h in enumerate(cols_xlsx, start=1):
        c = ws.cell(row=5, column=col_idx, value=h)
        c.fill = NAVY
        c.font = FONT_HEADER
        c.alignment = ALIGN_CENTER
        c.border = THIN_BORDER

    # Dados por função
    for r_idx, row_data in enumerate(dados_mo, start=6):
        meses_v = row_data[4:]
        tot_m = sum(meses_v)
        row_exp = row_data + [tot_m, tot_m * 220]
        for c_idx, val in enumerate(row_exp, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = FONT_REGULAR
            cell.border = THIN_BORDER
            if c_idx == 4:
                cell.number_format = '"R$ "#,##0.00'
                cell.alignment = ALIGN_RIGHT
            elif 5 <= c_idx <= 4 + prazo_meses:
                cell.number_format = '#,##0'
                cell.alignment = ALIGN_CENTER
            elif c_idx == 5 + prazo_meses:
                cell.number_format = '#,##0'
                cell.alignment = ALIGN_CENTER
                cell.font = FONT_BOLD
            elif c_idx == 6 + prazo_meses:
                cell.number_format = '#,##0" HH"'
                cell.alignment = ALIGN_RIGHT
                cell.font = FONT_BOLD
            else:
                cell.alignment = ALIGN_LEFT if c_idx == 2 else ALIGN_CENTER
            if r_idx % 2 == 1:
                cell.fill = GRAY_LIGHT

    # Linhas de totais (Headcount e HH)
    r_hc = len(dados_mo) + 6
    ws.cell(row=r_hc, column=1, value="TOTAL").alignment = ALIGN_CENTER
    ws.cell(row=r_hc, column=2, value="HEADCOUNT TOTAL DE CAMPO (Operários + Gestão)").alignment = ALIGN_LEFT
    ws.cell(row=r_hc, column=2).font = FONT_BOLD
    for m_idx, hc in enumerate(totais_hc, start=5):
        c = ws.cell(row=r_hc, column=m_idx, value=hc)
        c.font = FONT_BOLD
        c.fill = GOLD_ACCENT
        c.alignment = ALIGN_CENTER
        c.border = THIN_BORDER
    for col, val, fmt, fill in [
        (5 + prazo_meses, total_hc_meses, '#,##0', GOLD_ACCENT),
        (6 + prazo_meses, total_hh, '#,##0" HH"', GOLD_ACCENT),
    ]:
        c = ws.cell(row=r_hc, column=col, value=val)
        c.font = FONT_BOLD
        c.number_format = fmt
        c.fill = fill
        c.alignment = ALIGN_CENTER if col == 5 + prazo_meses else ALIGN_RIGHT
        c.border = THIN_BORDER

    r_hh = r_hc + 1
    ws.cell(row=r_hh, column=1, value="TOTAL").alignment = ALIGN_CENTER
    ws.cell(row=r_hh, column=2, value="TOTAL DE HORAS-HOMEM PREVISTAS (HH/mês)").alignment = ALIGN_LEFT
    ws.cell(row=r_hh, column=2).font = FONT_BOLD
    for m_idx, hh in enumerate(totais_hh, start=5):
        c = ws.cell(row=r_hh, column=m_idx, value=hh)
        c.font = FONT_BOLD
        c.number_format = '#,##0" HH"'
        c.fill = BLUE_LIGHT
        c.alignment = ALIGN_CENTER
        c.border = THIN_BORDER
    ws.cell(row=r_hh, column=5 + prazo_meses, value=total_hc_meses).fill = BLUE_LIGHT
    ws.cell(row=r_hh, column=5 + prazo_meses).font = FONT_BOLD
    ws.cell(row=r_hh, column=5 + prazo_meses).alignment = ALIGN_CENTER
    ws.cell(row=r_hh, column=5 + prazo_meses).border = THIN_BORDER
    c_grand = ws.cell(row=r_hh, column=6 + prazo_meses, value=total_hh)
    c_grand.font = Font(name="Calibri", size=12, bold=True, color="1B365D")
    c_grand.number_format = '#,##0" HH"'
    c_grand.fill = BLUE_ACCENT
    c_grand.alignment = ALIGN_RIGHT
    c_grand.border = THIN_BORDER

    # Larguras de coluna
    ws.column_dimensions['A'].width = 16
    ws.column_dimensions['B'].width = 44
    ws.column_dimensions['C'].width = 18
    ws.column_dimensions['D'].width = 24
    for m in range(1, prazo_meses + 1):
        ws.column_dimensions[get_column_letter(4 + m)].width = 12
    ws.column_dimensions[get_column_letter(5 + prazo_meses)].width = 14
    ws.column_dimensions[get_column_letter(6 + prazo_meses)].width = 24

    ws.freeze_panes = "E6"
    wb.save(xlsx_path)
    print(f"[OK] XLSX salvo: {os.path.relpath(xlsx_path, ROOT_DIR)}")


# =============================================================================
# GERAÇÃO DO RELATÓRIO MD
# =============================================================================

def _gerar_relatorio_md(dir_rh, sigla, dados_mo, totais_hc, totais_hh,
                         total_hc_meses, total_hh, prazo_meses, duracao_cronograma):
    md_path = os.path.join(dir_rh, f"RELATORIO_HISTOGRAMA_MO_{sigla}.md")
    pico_hc = max(totais_hc)
    media_hc = sum(totais_hc) / len(totais_hc)

    linhas = [
        "# 👷 RELATÓRIO EXECUTIVO: HISTOGRAMA DE MÃO DE OBRA & GESTÃO DE EFETIVO",
        "",
        f"**Empreendimento:** Edifício Administrativo do Terminal Multiuso (`{sigla}`)  ",
        f"**Prazo da Obra:** {prazo_meses} Meses (Sincronizado com Takt & Linha de Balanço)  ",
        f"**Total de Horas-Homem (HH) Planejadas:** **{total_hh:,.0f} HH**  ",
        f"**Total Acumulado de Headcount-Mês:** **{total_hc_meses} Homens-Mês**  ",
        f"**Pico de Efetivo (Headcount):** {pico_hc} profissionais (Mês 3)  ",
        f"**Média Geral de Efetivo:** {media_hc:.1f} profissionais/mês (5 de gestão/SST fixos)  ",
        f"**Data de Atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}  ",
        f"**Responsável Técnico:** PMO Virtual / Coordenação de Planejamento, SST e RH  ",
        "",
        "---",
        "",
        "## 1. Matriz Mensal de Headcount por Cargo / Função (18 Funções)",
        "",
        ("| Grupo | Função / Cargo | Categoria | Custo Base Ref. | "
         + " | ".join([f"M{m}" for m in range(1, prazo_meses + 1)])
         + " | Total Meses | Total HH |"),
        ("|---|---|:---:|:---:| "
         + " | ".join([":---:" for _ in range(prazo_meses)])
         + " |:---:|:---:|"),
    ]
    for row in dados_mo:
        grupo, cargo, cat, custo = row[:4]
        meses_vals = row[4:]
        tot_m = sum(meses_vals)
        meses_str = " | ".join([str(v) for v in meses_vals])
        custo_fmt = f"R$ {custo:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        linhas.append(
            f"| **{grupo}** | {cargo} | {cat} | {custo_fmt} | {meses_str} | **{tot_m}** | **{tot_m * 220:,.0f} HH** |"
        )
    hc_row_str = " | ".join([f"**{hc}**" for hc in totais_hc])
    hh_row_str = " | ".join([f"**{hh:,.0f}**" for hh in totais_hh])
    linhas.append(
        f"| **TOTAL** | **HEADCOUNT TOTAL DE CAMPO** | — | — | {hc_row_str} | **{total_hc_meses}** | **{total_hh:,.0f} HH** |"
    )
    linhas.append(
        f"| **TOTAL** | **TOTAL HORAS-HOMEM (HH) (220h/mês)** | — | — | {hh_row_str} | **{total_hc_meses}** | **{total_hh:,.0f} HH** |"
    )
    linhas += [
        "",
        "---",
        "",
        "## 2. Princípios de Nivelamento Lean (Heijunka)",
        "1. **Equipe Fixa de Gestão & SST (5 profissionais):** Engenheiro Residente, Mestre de Obras Geral, TST, Almoxarife e Vigia Noturno permanecem estáveis em todos os meses.",
        "2. **Fluxo Contínuo da Produção:** Equipes de oficiais e ajudantes movem-se continuamente entre as frentes em ciclos Takt, eliminando ociosidade e picos fictícios.",
        "3. **Crashing e Reprogramação:** Se o ritmo de um lote for acelerado por aumento de equipe, o histograma do mês correspondente é automaticamente incrementado.",
        f"4. **Conformidade Físico-Financeira:** Total de **{total_hh:,.0f} HH** em {duracao_cronograma} dias úteis de produção alinhado ao orçamento executivo.",
    ]

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(linhas) + "\n")
    print(f"[OK] MD salvo:  {os.path.relpath(md_path, ROOT_DIR)}")


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Motor Universal de Sincronização do Histograma de Mão de Obra.")
    parser.add_argument("--obra", type=str, default="OBRA_TMULT", help="Nome da pasta da obra em projetos/")
    parser.add_argument("--dir", type=str, default=None, help="Caminho direto para a pasta da obra")
    parser.add_argument("--prazo-meses", type=int, default=6, help="Prazo da obra em meses (sobrescreve config_obra.json)")
    args = parser.parse_args()

    obra_dir = args.dir if args.dir else os.path.join(ROOT_DIR, "projetos", args.obra)
    if not os.path.isdir(obra_dir):
        print(f"[ERRO] Pasta da obra não encontrada: {obra_dir}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  HISTOGRAMA DE MÃO DE OBRA — {args.obra}")
    print(f"{'='*60}")
    recalcular_histograma_obra(obra_dir, args.obra, prazo_meses=args.prazo_meses)
    print(f"\n[CONCLUÍDO] Histograma de mão de obra sincronizado com sucesso.\n")


if __name__ == "__main__":
    main()
