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
from datetime import date

# Raiz do repositório
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.common.obra_io import resolver_obra_dir, carregar_config_obra
from scripts.common.calendario import dia_util_para_data_6d, parse_date_br

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

    for cod_lote, info in mapa_cpm.items():
        aid = info.get("atividade_cpm")
        num = info.get("num", 1)
        den = info.get("den", 1)
        fallback_dur = info.get("fallback_dur", 2)
        frac = num / den if den != 0 else 1.0

        if aid in atividades:
            if cod_lote == "LOTE-016":
                a09_dur = atividades.get("A09_CONCRET_LAJE_H12", 1)
                a10_dur = atividades.get("A10_CURA_DESFORMA", 12)
                duracoes_derivadas[cod_lote] = a09_dur + a10_dur + 3
            elif frac == 1.0:
                duracoes_derivadas[cod_lote] = atividades[aid]
            else:
                dur_calc = int(round(atividades[aid] * frac))
                duracoes_derivadas[cod_lote] = dur_calc if dur_calc > 0 else fallback_dur
        else:
            duracoes_derivadas[cod_lote] = fallback_dur

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


def salvar_programacao_obra(nome_obra, takt_dias=3, obra_dir=None):
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

    dest_template = os.path.join(ROOT_DIR, 'projetos', '_TEMPLATE_OBRA_NOVA', '03_PLANEJAMENTO_E_CRONOGRAMA', 'TEMPLATE_PROGRAMACAO_CURTO_PRAZO.csv')
    if os.path.exists(os.path.dirname(dest_template)):
        dest_paths.append(dest_template)

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

    weekday_br = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    # Carrega janelas do calendário CPM do catálogo se necessário
    caminho_cat = os.path.join(ROOT_DIR, "apoio", "catalogo_lotes_takt.json")
    cal_cpm_map = {}
    if os.path.exists(caminho_cat):
        with open(caminho_cat, "r", encoding="utf-8") as f:
            cal_cpm_map = json.load(f).get("calendario_cpm_dias", {})

    for lote in lotes:
        cod = lote['COD_LOTE']
        d_ini = lote.get('CPM_DIA_INICIO')
        d_fim = lote.get('CPM_DIA_FIM')
        if (d_ini is None or d_fim is None) and cod in cal_cpm_map:
            d_ini, d_fim = cal_cpm_map[cod]

        if d_ini is not None and d_fim is not None:
            dt_i = dia_util_para_data_6d(d_ini - 1, base_dt)
            dt_f = dia_util_para_data_6d(d_fim - 1, base_dt)
            lote['DATA_INICIO'] = dt_i.strftime("%d/%m/%Y")
            lote['DATA_FIM'] = dt_f.strftime("%d/%m/%Y")
            lote['DURACAO_DIAS'] = str(d_fim - d_ini + 1)
            w_i = weekday_br[dt_i.weekday()]
            w_f = weekday_br[dt_f.weekday()]
            if d_ini == d_fim:
                lote['DIAS_SEMANA'] = f"Dia {d_ini:03d} ({w_i})"
            else:
                lote['DIAS_SEMANA'] = f"Dias {d_ini:03d} a {d_fim:03d} ({w_i}-{w_f})"

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
    args = parser.parse_args()

    obra_dir = resolver_obra_dir(args)
    salvar_programacao_obra(args.obra, takt_dias=args.takt_dias, obra_dir=obra_dir)


if __name__ == '__main__':
    main()
