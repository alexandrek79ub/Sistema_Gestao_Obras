#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: gerar_programacao_curto_prazo_takt.py
Motor Universal de Programação de Curto Prazo (Weekly Work Plan - WWP)
estruturada rigorosamente como uma ESTEIRA DE PRODUÇÃO LEAN (Takt Planning),
harmonizada integralmente com o Caminho Crítico (dados_cpm.json)
e a Linha de Balanço Canônica de 15 Vagões.

Uso:
    python scripts/gerar_programacao_curto_prazo_takt.py --obra OBRA_TMULT
    python scripts/gerar_programacao_curto_prazo_takt.py --obra RESIDENCIAL_ALPHA
    python scripts/gerar_programacao_curto_prazo_takt.py --dir projetos/OBRA_TMULT
"""

import os
import sys
import csv
import json
import copy
import argparse
import subprocess
import math
from datetime import date

# Raiz do repositório
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.common.obra_io import resolver_obra_dir, carregar_config_obra
from scripts.common.calendario import dia_util_para_data_6d, parse_date_br, proximo_dia_util_6d, somar_dias_uteis_6d

# Blindagem UTF-8 no Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def carregar_mapa_cpm():
    """Carrega o catálogo de frações e atividades CPM de apoio/mapa_lotes_cpm.json."""
    caminho = os.path.join(ROOT_DIR, "apoio", "mapa_lotes_cpm.json")
    if not os.path.exists(caminho):
        print(f"[-] Aviso: {caminho} não encontrado.")
        return {}
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
    return dados.get("lotes", {})


def derivar_duracoes_do_cpm(cpm_path):
    """Lê dados_cpm.json e deriva dinamicamente as durações de cada lote."""
    if not os.path.exists(cpm_path):
        print(f"[-] Aviso: {cpm_path} não encontrado. Mantendo durações canônicas.")
        return {}
    with open(cpm_path, "r", encoding="utf-8") as f:
        cpm_data = json.load(f)
    atividades = {a['id']: a['duracao_dias'] for a in cpm_data.get('atividades', [])}

    mapa_cpm = carregar_mapa_cpm()
    duracoes_derivadas = {}

    lotes_por_atividade = {}
    for cod_lote, info in mapa_cpm.items():
        lotes_por_atividade.setdefault(info.get("atividade_cpm"), []).append((cod_lote, info))

    for aid, lotes_atividade in lotes_por_atividade.items():
        if aid not in atividades:
            for cod_lote, info in lotes_atividade:
                duracoes_derivadas[cod_lote] = int(info.get("fallback_dur", 2))
            continue

        # LOTE-016 representa uma janela composta de concretagem, cura e folga
        # tecnológica; ela não é uma fração de uma única atividade CPM.
        especiais = [(cod, info) for cod, info in lotes_atividade if cod == "LOTE-016"]
        regulares = [(cod, info) for cod, info in lotes_atividade if cod != "LOTE-016"]
        for cod_lote, _ in especiais:
            duracoes_derivadas[cod_lote] = (
                atividades.get("A09_CONCRET_LAJE_H12", 1)
                + atividades.get("A10_CURA_DESFORMA", 12) + 3
            )

        if not regulares:
            continue

        duracao_atividade = int(atividades[aid])
        if duracao_atividade < len(regulares):
            raise ValueError(
                f"Atividade {aid} tem {duracao_atividade}d para {len(regulares)} lotes; "
                "não é possível preservar lotes com duração mínima de 1 dia."
            )

        pesos = [info.get("num", 1) / max(1, info.get("den", 1)) for _, info in regulares]
        soma_pesos = sum(pesos)
        quotas = [duracao_atividade * peso / soma_pesos for peso in pesos]
        alocadas = [max(1, math.floor(quota)) for quota in quotas]
        saldo = duracao_atividade - sum(alocadas)

        # Método do maior resto: as frações dos lotes somam exatamente a duração
        # do CPM, eliminando dias fantasmas introduzidos por arredondamento unitário.
        ordem = sorted(range(len(regulares)), key=lambda idx: quotas[idx] - math.floor(quotas[idx]), reverse=True)
        for idx in ordem:
            if saldo <= 0:
                break
            alocadas[idx] += 1
            saldo -= 1
        if saldo < 0:
            for idx in reversed(ordem):
                while saldo < 0 and alocadas[idx] > 1:
                    alocadas[idx] -= 1
                    saldo += 1
        if saldo != 0:
            raise ValueError(f"Não foi possível ratear exatamente a duração da atividade {aid}.")

        for (cod_lote, _), duracao_lote in zip(regulares, alocadas):
            duracoes_derivadas[cod_lote] = duracao_lote

    return duracoes_derivadas


def obter_lotes_padrao(nome_obra=""):
    """
    Retorna os lotes de produção calculados em ritmo de esteira Takt (52 lotes / 26 semanas / 15 vagões)
    a partir do catálogo externo apoio/catalogo_lotes_takt.json.
    """
    caminho_cat = os.path.join(ROOT_DIR, "apoio", "catalogo_lotes_takt.json")
    if not os.path.exists(caminho_cat):
        raise FileNotFoundError(f"Catálogo de lotes não encontrado: {caminho_cat}")

    with open(caminho_cat, "r", encoding="utf-8") as f:
        catalogo = json.load(f)

    return copy.deepcopy(catalogo.get("lotes", []))


def aplicar_cpm_aos_lotes(lotes, cpm_path, data_inicio):
    """Deriva datas, duracoes e efetivo dos lotes diretamente do CPM."""
    with open(cpm_path, "r", encoding="utf-8") as f:
        cpm = json.load(f)

    atividades = {item["id"]: dict(item) for item in cpm.get("atividades", [])}
    pendentes = set(atividades)
    while pendentes:
        prontos = [aid for aid in pendentes if all(pred not in pendentes for pred in atividades[aid].get("predecessoras", []))]
        if not prontos:
            raise ValueError("CPM contem ciclo ou predecessora inexistente.")
        for aid in prontos:
            atividade = atividades[aid]
            atividade["es"] = max((atividades[pred]["ef"] for pred in atividade.get("predecessoras", [])), default=0)
            atividade["ef"] = atividade["es"] + int(atividade["duracao_dias"])
            pendentes.remove(aid)

    mapa = carregar_mapa_cpm()
    ultimo_fim = {}
    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
    for lote in lotes:
        info = mapa.get(lote["COD_LOTE"], {})
        atividade = atividades.get(info.get("atividade_cpm"))
        if not atividade:
            continue
        duracao = max(1, int(lote["DURACAO_DIAS"]))
        inicio_cpm = dia_util_para_data_6d(atividade["es"], data_inicio)
        inicio = proximo_dia_util_6d(ultimo_fim[atividade["id"]]) if atividade["id"] in ultimo_fim else inicio_cpm
        inicio = max(inicio, inicio_cpm)
        fim = somar_dias_uteis_6d(inicio, duracao)
        ultimo_fim[atividade["id"]] = fim

        duracao_base = max(1, int(info.get("fallback_dur", duracao)))
        efetivo_base = max(1, int(lote.get("HEADCOUNT_PREVISTO", 1)))
        lote["HEADCOUNT_PREVISTO"] = str(math.ceil(efetivo_base * duracao_base / duracao))
        lote["DATA_INICIO"] = inicio.strftime("%d/%m/%Y")
        lote["DATA_FIM"] = fim.strftime("%d/%m/%Y")
        lote["DIAS_SEMANA"] = f"Dias {atividade['es'] + 1:03d} a {atividade['es'] + duracao:03d} ({dias_semana[inicio.weekday()]}-{dias_semana[fim.weekday()]})"


def salvar_programacao_obra(nome_obra, takt_dias=3, obra_dir=None, sincronizar_lob=True):
    """Gera e salva a esteira de curto prazo (Takt / WWP) harmonizada com o CPM."""
    if not obra_dir:
        obra_dir = os.path.join(ROOT_DIR, 'projetos', nome_obra)

    pasta_plan = os.path.join(obra_dir, '03_PLANEJAMENTO_E_CRONOGRAMA')
    os.makedirs(pasta_plan, exist_ok=True)

    sigla = os.path.basename(obra_dir).replace('OBRA_', '')
    dest_paths = [
        os.path.join(pasta_plan, f'PROGRAMACAO_CURTO_PRAZO_{sigla}.csv'),
        os.path.join(pasta_plan, f'PROGRAMACAO_CURTO_PRAZO_{os.path.basename(obra_dir)}.csv'),
    ]
    if os.path.basename(obra_dir) == 'OBRA_TMULT':
        dest_paths.append(os.path.join(pasta_plan, 'PROGRAMACAO_CURTO_PRAZO_TMULT.csv'))

    lotes = obter_lotes_padrao(nome_obra)

    # Derivação dinâmica do CPM se dados_cpm.json existir na obra
    cpm_path = os.path.join(pasta_plan, 'dados_cpm.json')
    duracoes_cpm = derivar_duracoes_do_cpm(cpm_path)
    if duracoes_cpm:
        print(f'[*] Sincronizando {len(lotes)} lotes com as durações reais do CPM ({cpm_path})...')
        for lote in lotes:
            cod = lote['COD_LOTE']
            if cod in duracoes_cpm:
                lote['DURACAO_DIAS'] = str(duracoes_cpm[cod])

    # Configuração de data base da obra
    config = carregar_config_obra(obra_dir)
    dt_inicio_cfg = config.get("data_inicio") or "01/10/2026"
    parsed_base = parse_date_br(dt_inicio_cfg)
    base_dt = parsed_base.date() if parsed_base else date(2026, 10, 1)

    if os.path.exists(cpm_path):
        aplicar_cpm_aos_lotes(lotes, cpm_path, base_dt)

    fieldnames = [
        'COD_LOTE', 'SEMANA', 'DIAS_SEMANA', 'DATA_INICIO', 'DATA_FIM',
        'ETAPA_ZONA', 'VAGAO_ESTEIRA', 'SERVICO_LOTE', 'META_FISICA',
        'DURACAO_DIAS', 'EQUIPE_PREVISTA', 'HEADCOUNT_PREVISTO',
        'EQUIPAMENTOS_PREVISTOS', 'MATERIAIS_UCC', 'RUP_META_HH_UNID',
        'STATUS_EXECUCAO', 'RDO_VINCULADO'
    ]

    # Grava em todos os destinos relevantes com padrão utf-8-sig e delimitador ';'
    unique_paths = list(dict.fromkeys(dest_paths))
    for p in unique_paths:
        with open(p, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';', quoting=csv.QUOTE_ALL, extrasaction='ignore')
            writer.writeheader()
            for lote in lotes:
                writer.writerow(lote)
        print(f'[LEAN TAKT] Sucesso: {len(lotes)} lotes gravados em {p}')

    # Sincronização Automática com a Linha de Balanço (LOB)
    if not sincronizar_lob:
        return
    try:
        script_sync = os.path.join(ROOT_DIR, 'scripts', 'sincronizar_esteira_e_lob.py')
        if os.path.exists(script_sync):
            print('[SINCRONIZADOR LEAN] Disparando sincronização com a Linha de Balanço (LOB)...')
            subprocess.run([sys.executable, script_sync, '--obra', os.path.basename(obra_dir), '--modo', 'esteira_para_lob'], check=True)
    except Exception as err:
        print(f'[!] Aviso: Sincronização com LOB via subprocesso falhou: {err}')


def main():
    parser = argparse.ArgumentParser(description='Gerador Universal de Programação de Curto Prazo em Esteira Lean (Takt Time)')
    parser.add_argument('--obra', type=str, default='OBRA_TMULT', help='Nome da pasta da obra em projetos/')
    parser.add_argument('--dir', type=str, default=None, help='Caminho direto absoluto ou relativo para a pasta da obra')
    parser.add_argument('--takt-dias', type=int, default=3, help='Duração do Takt Time em dias úteis (1 a 6 dias, padrão 3)')
    parser.add_argument('--sem-lob', action='store_true')
    args = parser.parse_args()

    obra_dir = resolver_obra_dir(args)
    salvar_programacao_obra(args.obra, takt_dias=args.takt_dias, obra_dir=obra_dir, sincronizar_lob=not args.sem_lob)


if __name__ == '__main__':
    main()
