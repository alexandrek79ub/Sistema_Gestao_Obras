#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Cálculo CPM (Caminho Crítico) e DTO de Cronograma.

Realiza o Forward Pass (Early Start/Finish), Backward Pass (Late Start/Finish),
cálculo de Folga Total (Total Float/Slack), Folga Livre (Free Slack) e Criticidade.
"""

from datetime import date, datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple


def calcular_cpm_detalhado(
    atividades: List[Dict[str, Any]],
    data_inicio_iso: str = "2026-10-01"
) -> Dict[str, Any]:
    """
    Executa o algoritmo CPM completo (Forward e Backward Pass) sobre a lista de atividades.
    
    Cada atividade deve conter:
    - id: str
    - duracao_dias: int
    - predecessoras: List[str]

    Retorna DTO com:
    - duracao_total_dias: int
    - data_inicio: date
    - data_fim: date
    - caminho_critico: List[str]
    - atividades: Dict[str, Dict[str, Any]] (com es, ef, ls, lf, folga_total, folga_livre, critica, datas)
    """
    if not atividades:
        raise ValueError("Lista de atividades vazia para cálculo do CPM.")

    atividades_map = {a["id"]: a for a in atividades}
    
    # 1. Detectar nós e predecessoras
    preds_map: Dict[str, List[str]] = {}
    sucs_map: Dict[str, List[str]] = {aid: [] for aid in atividades_map}

    for aid, a in atividades_map.items():
        preds = [p for p in a.get("predecessoras", []) if p in atividades_map]
        preds_map[aid] = preds
        for p in preds:
            sucs_map[p].append(aid)

    # 2. Forward Pass (Early Start e Early Finish)
    es: Dict[str, int] = {}
    ef: Dict[str, int] = {}

    for aid in atividades_map:
        es[aid] = 0
        dur = int(atividades_map[aid].get("duracao_dias", 1))
        ef[aid] = dur

    # Propagação até convergência ou detecção de ciclo
    max_iter = len(atividades_map) * 2 + 10
    iter_count = 0
    changed = True

    while changed and iter_count < max_iter:
        changed = False
        iter_count += 1
        for aid, a in atividades_map.items():
            dur = int(a.get("duracao_dias", 1))
            max_pred_ef = 0
            for p in preds_map[aid]:
                if ef[p] > max_pred_ef:
                    max_pred_ef = ef[p]
            if max_pred_ef > es[aid]:
                es[aid] = max_pred_ef
                ef[aid] = max_pred_ef + dur
                changed = True

    if iter_count >= max_iter:
        raise ValueError("Ciclo detectado nas relações de precedência do CPM.")

    duracao_total = max(ef.values()) if ef else 0

    # 3. Backward Pass (Late Finish e Late Start)
    lf: Dict[str, int] = {}
    ls: Dict[str, int] = {}

    for aid in atividades_map:
        lf[aid] = duracao_total
        dur = int(atividades_map[aid].get("duracao_dias", 1))
        ls[aid] = duracao_total - dur

    changed = True
    iter_count = 0

    while changed and iter_count < max_iter:
        changed = False
        iter_count += 1
        for aid, a in atividades_map.items():
            dur = int(a.get("duracao_dias", 1))
            if sucs_map[aid]:
                min_suc_ls = min(ls[s] for s in sucs_map[aid])
                if min_suc_ls < lf[aid]:
                    lf[aid] = min_suc_ls
                    ls[aid] = min_suc_ls - dur
                    changed = True

    # 4. Cálculo de Folga Total, Folga Livre e Criticidade
    dt_inicio = date.fromisoformat(data_inicio_iso) if isinstance(data_inicio_iso, str) else data_inicio_iso
    resultado_atividades = {}
    caminho_critico = []

    for aid, a in atividades_map.items():
        dur = int(a.get("duracao_dias", 1))
        folga_total = ls[aid] - es[aid]
        if sucs_map[aid]:
            folga_livre = min(es[s] for s in sucs_map[aid]) - ef[aid]
        else:
            folga_livre = duracao_total - ef[aid]

        critica = (folga_total == 0)
        if critica:
            caminho_critico.append(aid)

        # Mapeamento para datas corridas/civis da rede
        t_inicio = dt_inicio + timedelta(days=es[aid])
        t_fim = dt_inicio + timedelta(days=ef[aid])

        resultado_atividades[aid] = {
            "id": aid,
            "duracao_dias": dur,
            "predecessoras": preds_map[aid],
            "sucessoras": sucs_map[aid],
            "es": es[aid],
            "ef": ef[aid],
            "ls": ls[aid],
            "lf": lf[aid],
            "folga_total": folga_total,
            "folga_livre": folga_livre,
            "critica": critica,
            "data_inicio": t_inicio.isoformat(),
            "data_fim": t_fim.isoformat()
        }

    dt_fim_projeto = dt_inicio + timedelta(days=duracao_total)

    return {
        "duracao_total_dias": duracao_total,
        "data_inicio": dt_inicio.isoformat(),
        "data_fim": dt_fim_projeto.isoformat(),
        "caminho_critico": caminho_critico,
        "atividades": resultado_atividades,
        "total_atividades": len(resultado_atividades)
    }
