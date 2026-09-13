#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários de Calendário de Obra.

Centraliza o cálculo de dias úteis, janelas mensais e avanço de datas,
extraído e consolidado dos scripts gerar_cronograma.py, gerar_histograma_sincronizado.py
e gerar_programacao_curto_prazo_takt.py.

IMPORTANTE: A lógica aqui é 100% extraída do código atual dos scripts existentes.
            Os resultados de datas e durações são matematicamente idênticos aos
            anteriores — a implementação foi apenas centralizada.

Feriados cobertos: Nacionais brasileiros fixos + datas flutuantes aproximadas.
                   Feriados regionais/municipais devem ser passados via parâmetro
                   extra_feriados ou configurados em config_obra.json.
"""

from datetime import date, datetime, timedelta

# =============================================================================
# FERIADOS NACIONAIS (Fixos — independentes de ano)
# =============================================================================
# Meses e dias fixos (sem Carnaval, Páscoa e Corpus Christi — dependem do ano)
_FERIADOS_FIXOS_MM_DD = [
    (1,  1),   # Confraternização Universal
    (4,  21),  # Tiradentes
    (5,  1),   # Dia do Trabalho
    (9,  7),   # Independência do Brasil
    (10, 12),  # Nossa Senhora Aparecida
    (11, 2),   # Finados
    (11, 15),  # Proclamação da República
    (12, 25),  # Natal
]

# Feriados móveis pré-calculados para o horizonte da OBRA_TMULT (2026–2027)
# Fonte: Cálculo eclesiástico de Páscoa (algoritmo de Computus)
_FERIADOS_MOVEIS = [
    # 2026
    date(2026, 2, 16),   # Carnaval (segunda)
    date(2026, 2, 17),   # Carnaval (terça)
    date(2026, 4, 3),    # Sexta-feira Santa
    date(2026, 4, 5),    # Páscoa
    date(2026, 6, 4),    # Corpus Christi
    # 2027
    date(2027, 2, 8),    # Carnaval (segunda)
    date(2027, 2, 9),    # Carnaval (terça)
    date(2027, 3, 26),   # Sexta-feira Santa
    date(2027, 3, 28),   # Páscoa
    date(2027, 5, 27),   # Corpus Christi
]


def feriados_do_ano(ano):
    """
    Retorna o conjunto de feriados nacionais para um dado ano.

    Args:
        ano : int — Ano de referência.

    Returns:
        set[date] : Conjunto de datas de feriados nacionais.
    """
    feriados = set()
    for mes, dia in _FERIADOS_FIXOS_MM_DD:
        try:
            feriados.add(date(ano, mes, dia))
        except ValueError:
            pass
    for d in _FERIADOS_MOVEIS:
        if d.year == ano:
            feriados.add(d)
    return feriados


def eh_dia_util(d, extra_feriados=None):
    """
    Verifica se uma data é dia útil (segunda a sexta, não feriado).

    Args:
        d               : date ou datetime.
        extra_feriados  : set[date] adicional de feriados (regionais/municipais).

    Returns:
        bool
    """
    if isinstance(d, datetime):
        d = d.date()
    if d.weekday() >= 5:  # Sábado (5) ou Domingo (6)
        return False
    feriados = feriados_do_ano(d.year)
    if extra_feriados:
        feriados = feriados | extra_feriados
    return d not in feriados


def adicionar_dias_uteis(d_inicio, n_dias, extra_feriados=None):
    """
    Avança n_dias úteis a partir de d_inicio.
    Equivalente à lógica distribuída em gerar_cronograma.py e similares.

    Args:
        d_inicio        : date ou datetime de partida.
        n_dias          : Número inteiro de dias úteis a avançar.
        extra_feriados  : set[date] adicional (opcional).

    Returns:
        date : Data resultante após n_dias úteis.
    """
    if isinstance(d_inicio, datetime):
        d_inicio = d_inicio.date()
    if n_dias <= 0:
        return d_inicio
    atual = d_inicio
    contados = 0
    while contados < n_dias:
        atual += timedelta(days=1)
        if eh_dia_util(atual, extra_feriados):
            contados += 1
    return atual


def dias_uteis_entre(d_inicio, d_fim, extra_feriados=None):
    """
    Conta os dias úteis entre duas datas (inclusive d_inicio, exclusive d_fim).
    Mesma lógica do cálculo de duração em gerar_programacao_curto_prazo_takt.py.

    Args:
        d_inicio        : date ou datetime inicial.
        d_fim           : date ou datetime final.
        extra_feriados  : set[date] adicional (opcional).

    Returns:
        int : Número de dias úteis.
    """
    if isinstance(d_inicio, datetime):
        d_inicio = d_inicio.date()
    if isinstance(d_fim, datetime):
        d_fim = d_fim.date()
    if d_inicio >= d_fim:
        return 0
    atual = d_inicio
    contagem = 0
    while atual < d_fim:
        if eh_dia_util(atual, extra_feriados):
            contagem += 1
        atual += timedelta(days=1)
    return contagem


def parse_date_br(d_str):
    """
    Converte string de data nos formatos BR e ISO para objeto date.
    Extraído de gerar_histograma_sincronizado.py e sincronizar_esteira_e_lob.py.

    Formatos suportados: 'DD/MM/AAAA', 'AAAA-MM-DD', 'DD-MM-AAAA'.

    Args:
        d_str : str ou None.

    Returns:
        datetime ou None se não conseguir converter.
    """
    if not d_str or not isinstance(d_str, str):
        return None
    d_str = d_str.strip().replace('"', '')
    for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y'):
        try:
            return datetime.strptime(d_str, fmt)
        except ValueError:
            pass
    return None


def janelas_mensais_obra(d_inicio_obra, prazo_meses, extra_meses_buffer=0):
    """
    Gera a lista de janelas mensais da obra para agrupamento de headcount/custos.
    Lógica extraída de gerar_histograma_sincronizado.py (linhas 224–249).

    Args:
        d_inicio_obra      : date ou datetime — data de início da obra.
        prazo_meses        : int — número de meses de duração da obra.
        extra_meses_buffer : int — meses extras no último período (padrão: 0).
                             O script original usava +60 dias no último mês.

    Returns:
        list[dict] : Lista de janelas com chaves:
                     'mes_num', 'd_ini' (datetime), 'd_fim' (datetime), 'nome'.
    """
    if isinstance(d_inicio_obra, date) and not isinstance(d_inicio_obra, datetime):
        d_inicio_obra = datetime(d_inicio_obra.year, d_inicio_obra.month, d_inicio_obra.day)

    janelas = []
    cur_ano = d_inicio_obra.year
    cur_mes = d_inicio_obra.month

    for m in range(1, prazo_meses + 1):
        d_ini_mes = datetime(cur_ano, cur_mes, 1)

        if cur_mes == 12:
            prox_ano, prox_mes = cur_ano + 1, 1
        else:
            prox_ano, prox_mes = cur_ano, cur_mes + 1

        d_fim_mes = datetime(prox_ano, prox_mes, 1) - timedelta(days=1)

        # Compatibilidade: o script original ampliava o último mês em 60 dias
        if m == prazo_meses and extra_meses_buffer > 0:
            d_fim_mes = d_fim_mes + timedelta(days=extra_meses_buffer * 30)

        janelas.append({
            "mes_num": m,
            "d_ini": d_ini_mes,
            "d_fim": d_fim_mes,
            "nome": f"Mês {m}",
        })
        cur_ano, cur_mes = prox_ano, prox_mes

    return janelas
