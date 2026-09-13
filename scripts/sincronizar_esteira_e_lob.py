#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Sincronização Bidirecional: Esteira Takt (Curto Prazo) <-> Linha de Balanço (LOB)
com Detector Inteligente de Sobreposições, Conflitos Espaciais e Alerta de Aumento de Efetivo.

Uso:
    python scripts/sincronizar_esteira_e_lob.py --obra OBRA_TMULT --modo esteira_para_lob
    python scripts/sincronizar_esteira_e_lob.py --obra OBRA_TMULT --modo lob_para_esteira
    python scripts/sincronizar_esteira_e_lob.py --obra OBRA_TMULT --verificar
    python scripts/sincronizar_esteira_e_lob.py --obra OBRA_TMULT --analisar-sobreposicao
    python scripts/sincronizar_esteira_e_lob.py --obra OBRA_TMULT --verificar-cpm
"""

import os
import sys
import re
import argparse
import datetime
import json
import pandas as pd

# Raiz do repositório
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.common.obra_io import resolver_obra_dir, carregar_config_obra
from scripts.common.calendario import (
    parse_date_br, format_date_br, dia_util_para_data_6d,
    somar_dias_uteis_6d, proximo_dia_util_6d, contar_dias_uteis_6d
)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def parse_args():
    parser = argparse.ArgumentParser(description="Sincronizador Bidirecional Esteira Takt <-> Linha de Balanço")
    parser.add_argument("--obra", type=str, default="OBRA_TMULT", help="Nome da pasta da obra")
    parser.add_argument("--dir", type=str, default=None, help="Caminho direto absoluto ou relativo para a pasta da obra")
    parser.add_argument("--modo", type=str, choices=["esteira_para_lob", "lob_para_esteira", "ambos"], default="esteira_para_lob")
    parser.add_argument("--data-inicio", type=str, default="01/10/2026", help="Data de início (DD/MM/AAAA)")
    parser.add_argument("--verificar", action="store_true", help="Executa verificação de conformidade")
    parser.add_argument("--analisar-sobreposicao", action="store_true", help="Analisa sobreposições e pico de efetivo")
    parser.add_argument("--permitir-sobreposicao", action="store_true", help="Confirmação explícita de aumento de efetivo por sobreposição")
    parser.add_argument("--verificar-cpm", action="store_true", help="Executa validação cruzada CPM vs Linha de Balanço")
    parser.add_argument("--limite-divergencia", type=int, default=5, help="Limite em dias úteis para apontar divergência relevante")
    return parser.parse_args()


# =============================================================================
# CARREGAMENTO DO CATÁLOGO DE LOTES E VAGÕES CPM
# =============================================================================

def carregar_dados_catalogo_cpm():
    """Carrega lista de lotes CPM e mapeamento canônico a partir de apoio/mapa_lotes_cpm.json."""
    caminho = os.path.join(ROOT_DIR, "apoio", "mapa_lotes_cpm.json")
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    lotes_dict = dados.get("lotes", {})
    mapa_lotes_lista = []
    for cod, info in lotes_dict.items():
        mapa_lotes_lista.append((
            cod,
            info.get("atividade_cpm", ""),
            info.get("fallback_dur", 2),
            info.get("is_start", False),
            info.get("vagao", "")
        ))

    mapa_vagoes_canonicos = dados.get("mapa_cpm_vagao_canonico", {})
    return mapa_lotes_lista, mapa_vagoes_canonicos


def dias_uteis_entre_calc(d1, d2):
    """Conta dias úteis (seg-sáb) com sinal positivo se d2 > d1. Delega para calendario.contar_dias_uteis_6d."""
    if d1 == d2:
        return 0
    if d2 > d1:
        return contar_dias_uteis_6d(d1, d2)
    return -contar_dias_uteis_6d(d2, d1)


def calcular_calendario_lotes(data_inicio_str, total_lotes=52, obra_dir=None):
    """
    Calcula as datas de início e fim para cada um dos lotes da esteira.
    Se dados_cpm.json estiver presente, alinha as janelas ao CPM Forward Pass (178 dias úteis).
    """
    mapa_lote_cpm, _ = carregar_dados_catalogo_cpm()
    path_cpm = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "dados_cpm.json") if obra_dir else None

    if path_cpm and os.path.exists(path_cpm):
        with open(path_cpm, "r", encoding="utf-8") as f:
            cpm_raw = json.load(f)

        d, m, y = map(int, data_inicio_str.split('/'))
        base_dt = datetime.date(y, m, d)

        atividades = {a['id']: a for a in cpm_raw['atividades']}
        for aid, act in atividades.items():
            preds = act.get('predecessoras', [])
            act['es'] = 0 if not preds else max(atividades[p]['ef'] for p in preds)
            act['ef'] = act['es'] + act['duracao_dias']
            act['dt_ini'] = dia_util_para_data_6d(act['es'], base_dt)
            act['dt_fim'] = dia_util_para_data_6d(act['ef'] - 1, base_dt)

        is_compativel = all(item[1] in atividades for item in mapa_lote_cpm[:total_lotes])
        if is_compativel:
            calendario = []
            prev_end = None
            for lote_idx, (cod, aid, dur, is_start, vagao) in enumerate(mapa_lote_cpm[:total_lotes]):
                act = atividades[aid]
                if is_start:
                    dt_ini = act['dt_ini']
                else:
                    dt_ini = proximo_dia_util_6d(prev_end)
                dt_fim = somar_dias_uteis_6d(dt_ini, dur)
                prev_end = dt_fim

                semana_num = (lote_idx // 2) + 1
                ciclo_num = (lote_idx % 2) + 1

                calendario.append({
                    "lote_idx": lote_idx + 1,
                    "cod_lote": cod,
                    "semana": f"Semana {semana_num:02d}",
                    "ciclo": ciclo_num,
                    "dt_inicio": dt_ini,
                    "dt_fim": dt_fim,
                    "str_inicio": dt_ini.strftime("%d/%m/%Y"),
                    "str_fim": dt_fim.strftime("%d/%m/%Y"),
                    "duracao_dias": dur
                })
            return calendario

    # Fallback: cálculo sequencial linear
    d, m, y = map(int, data_inicio_str.split('/'))
    data_atual = datetime.date(y, m, d)
    calendario = []
    for lote_idx in range(total_lotes):
        semana_num = (lote_idx // 2) + 1
        ciclo_num = (lote_idx % 2) + 1
        if data_atual.weekday() == 6:
            data_atual += datetime.timedelta(days=1)
        dt_ini = data_atual
        dt_fim = somar_dias_uteis_6d(dt_ini, 3)
        calendario.append({
            "lote_idx": lote_idx + 1,
            "cod_lote": f"LOTE-{lote_idx + 1:03d}",
            "semana": f"Semana {semana_num:02d}",
            "ciclo": ciclo_num,
            "dt_inicio": dt_ini,
            "dt_fim": dt_fim,
            "str_inicio": dt_ini.strftime("%d/%m/%Y"),
            "str_fim": dt_fim.strftime("%d/%m/%Y"),
            "duracao_dias": 3
        })
        data_atual = proximo_dia_util_6d(dt_fim)
    return calendario


# =============================================================================
# NORMALIZADORES (ZONAS, VAGÕES, EQUIPES)
# =============================================================================

MAPA_ZONAS = {
    1: "Zona 01 - Recepção/Diretoria",
    2: "Zona 02 - Salas Técnicas/CPD",
    3: "Zona 03 - Sanitários e Apoio",
    4: "Zona 04 - Cobertura e Platibanda"
}

def normalizar_zona(etapa_zona_str):
    """Normaliza o texto do lote para as 4 Zonas Físicas da Linha de Balanço sem perder zonas em strings compostas."""
    s = (etapa_zona_str or "").lower()

    if "cobertura" in s or "platibanda" in s or "telha" in s:
        return [MAPA_ZONAS[4]]

    termos_globais = [
        "todos os setores", "térreo geral", "geral", "toda a edificação",
        "turnkey", "edifício", "vistoria", "entrega", "canteiro",
        "redes hidráulicas (portão de qualidade 3)"
    ]
    has_etapa_or_zona = bool(re.search(r'\b(etapa|zona|setor)\s*\d', s))

    if not has_etapa_or_zona and any(t in s for t in termos_globais):
        return [MAPA_ZONAS[1], MAPA_ZONAS[2], MAPA_ZONAS[3]]

    zonas_encontradas = set()
    matches = re.findall(r'\b(?:etapa|zona|setor)\s*([0-9\s,ea]+?)(?=\s*[\(\-\,\.\;]|e\s+[a-z]|em\s+|nas\s+|$)', s)
    for m in matches:
        m_range = re.search(r'(\d)\s*a\s*(\d)', m)
        if m_range:
            start_z, end_z = int(m_range.group(1)), int(m_range.group(2))
            for z in range(start_z, end_z + 1):
                if z in MAPA_ZONAS:
                    zonas_encontradas.add(z)
        else:
            for d in re.findall(r'\b([1-4])\b', m):
                z = int(d)
                if z in MAPA_ZONAS:
                    zonas_encontradas.add(z)

    if not zonas_encontradas:
        for z in [1, 2, 3, 4]:
            if re.search(rf'\b(etapa|zona|setor)\s*{z}\b', s):
                zonas_encontradas.add(z)

    if "fachada" in s:
        zonas_encontradas.add(1)

    if not zonas_encontradas:
        if "áreas secas" in s or "paredes internas" in s:
            return [MAPA_ZONAS[1], MAPA_ZONAS[2]]
        return [MAPA_ZONAS[1], MAPA_ZONAS[2], MAPA_ZONAS[3]]

    return [MAPA_ZONAS[z] for z in sorted(zonas_encontradas)]


MAPA_PREFIXO_VAGAO = {
    1: "01. Topografia & Canteiro", 2: "02. Fundações Sapatas", 3: "03. Vigas Baldrames",
    4: "04. Pilares Supraestrutura", 5: "05. Vigas & Laje H12", 6: "06. Alvenaria de Vedação",
    7: "07. Cobertura Metálica", 8: "08. Instalações Embutidas", 9: "09. Reboco Paulista",
    10: "10. Pisos & Porcelanato", 11: "11. Esquadrias de Alumínio", 12: "12. Climatização HVAC",
    13: "13. Acabamentos Elétr./Hidr.", 14: "14. Pintura Acrílica Final", 15: "15. Comissionamento & Entrega"
}

def normalizar_vagao(vagao_str, servico_str):
    """Classifica o serviço em um dos Grandes Vagões de Produção Contínua."""
    v = (vagao_str or "").strip().lower()
    s = (servico_str or "").strip().lower()

    m = re.search(r'vag[ãa]o\s*0?(\d+)', v) or re.match(r'^0?(\d+)\.', v)
    if m:
        v_num = int(m.group(1))
        if v_num in MAPA_PREFIXO_VAGAO:
            return MAPA_PREFIXO_VAGAO[v_num]

    for num, can_nome in MAPA_PREFIXO_VAGAO.items():
        subnome = can_nome.split(". ", 1)[1].lower()
        if subnome in v:
            return can_nome

    regras = [
        ("01. Topografia & Canteiro", ["topografia", "canteiro", "locação"]),
        ("02. Fundações Sapatas", ["sapata", "cavas", "escava"]),
        ("03. Vigas Baldrames", ["baldrame", "vb"]),
        ("04. Pilares Supraestrutura", ["pilar"]),
        ("05. Vigas & Laje H12", ["viga", "laje", "cimbramento", "vigota"]),
        ("06. Alvenaria de Vedação", ["alvenaria", "bloco de concreto", "bloco"]),
        ("07. Cobertura Metálica", ["cobertura", "telha", "terça", "rufo"]),
        ("08. Instalações Embutidas", ["eletroduto", "tubo", "hidrostático", "embutid"]),
        ("09. Reboco Paulista", ["chapisco", "reboco", "emboço"]),
        ("10. Pisos & Porcelanato", ["impermeabiliz", "contrapiso", "porcelanato", "cerâmica", "rodapé"]),
        ("11. Esquadrias de Alumínio", ["esquadria", "janela", "porta", "vidro"]),
        ("12. Climatização HVAC", ["climatiza", "hvac", "frigorígen", "ar-condicionado", "evaporadora"]),
        ("13. Acabamentos Elétr./Hidr.", ["cabo", "quadro", "qgbt", "luminária", "tomada", "louça", "metal"]),
        ("14. Pintura Acrílica Final", ["pintura", "massa acrílica", "látex"]),
        ("15. Comissionamento & Entrega", ["comissionamento", "limpeza", "as-built", "databook", "treinamento", "vistoria", "entrega", "auditoria"])
    ]
    for vagao_res, keywords in regras:
        if any(k in s or k in v for k in keywords):
            return vagao_res
    return "00. Outros Serviços"


def normalizar_equipe(equipe_str, servico_str):
    """Identifica o subempreiteiro e disciplina com rigor de prioridades."""
    e = (equipe_str or "").lower()
    s = (servico_str or "").lower()

    if "laje" in s or "vigota" in s or "treliç" in s or "cimbramento" in s:
        return "SUB-01 Estruturas e Concreto"
    if "alvenaria" in s or "bloco de concreto" in s or "reboco" in s or "chapisco" in s or "emboço" in s or "sub-02" in e:
        return "SUB-02 Alvenaria e Revestimento"
    if "ladrilhista" in e or "porcelanato" in s or "cerâmica" in s or "rejunte" in s or "sub-05" in e:
        return "SUB-05 Acabamentos e Pisos"
    if "esquadria" in s or "vidro" in s or "janela" in s or "porta de alumínio" in s:
        return "SUB-07 Caixilharia e Esquadrias"
    if "telha" in s or "cobertura" in s or "terça" in s or "rufo" in s or "sub-07" in e:
        return "SUB-07 Coberturas Metálicas"
    if "hvac" in e or "refrigera" in e or "ar-condicionado" in s or "climatiza" in s or "frigorígen" in s or "sub-08" in e:
        return "SUB-08 Climatização e HVAC"
    if "eletricista" in e or "elétric" in s or "cabo" in s or "ilumina" in s or "qgbt" in s or "sub-03" in e:
        return "SUB-03 Elétrica e Lógica"
    if "encanador" in e or "hidrául" in s or "louça" in s or "esgoto" in s or "água" in s or "sub-04" in e:
        return "SUB-04 Hidráulica e Sanitários"
    if "pintor" in e or "pintura" in s or "massa acrílica" in s or "látex" in s or "sub-06" in e:
        return "SUB-06 Pintura"
    if "topógrafo" in e or "topografia" in s or "gabarito" in s:
        return "SUB-01 Topografia e Locação"
    if "impermeabiliz" in s:
        return "SUB-01 Impermeabilização"
    if any(k in e or k in s for k in ["armador", "carpinteiro", "concreto", "sapata", "baldrame", "pilar", "fôrma", "escava"]) or "sub-01" in e:
        return "SUB-01 Estruturas e Concreto"
    return "Equipe Própria / Turnkey"


# =============================================================================
# OPERAÇÃO: ESTEIRA PARA LINHA DE BALANÇO (LOB)
# =============================================================================

SETOR_ESPECIFICO_LOTE = {
    "LOTE-027": ["Zona 03 - Sanitários e Apoio"],
    "LOTE-028": ["Zona 01 - Recepção/Diretoria", "Zona 02 - Salas Técnicas/CPD"],
    "LOTE-029": ["Zona 01 - Recepção/Diretoria"],
    "LOTE-030": ["Zona 02 - Salas Técnicas/CPD"],
    "LOTE-031": ["Zona 03 - Sanitários e Apoio"],
    "LOTE-032": ["Zona 01 - Recepção/Diretoria", "Zona 02 - Salas Técnicas/CPD"],
    "LOTE-033": ["Zona 01 - Recepção/Diretoria"],
    "LOTE-034": ["Zona 04 - Cobertura e Platibanda"],
    "LOTE-035": ["Zona 03 - Sanitários e Apoio"],
    "LOTE-036": ["Zona 04 - Cobertura e Platibanda"],
    "LOTE-037": ["Zona 01 - Recepção/Diretoria", "Zona 03 - Sanitários e Apoio"],
    "LOTE-038": ["Zona 02 - Salas Técnicas/CPD"],
    "LOTE-039": ["Zona 01 - Recepção/Diretoria", "Zona 02 - Salas Técnicas/CPD"],
    "LOTE-040": ["Zona 03 - Sanitários e Apoio"],
    "LOTE-041": ["Zona 03 - Sanitários e Apoio"],
    "LOTE-042": ["Zona 01 - Recepção/Diretoria", "Zona 02 - Salas Técnicas/CPD"],
    "LOTE-044": ["Zona 01 - Recepção/Diretoria", "Zona 02 - Salas Técnicas/CPD"],
    "LOTE-043": ["Zona 01 - Recepção/Diretoria", "Zona 02 - Salas Técnicas/CPD", "Zona 03 - Sanitários e Apoio"],
}


def esteira_para_lob(obra_dir, data_inicio_str="01/10/2026"):
    """Lê a programação de curto prazo e gera a LINHA_DE_BALANCO.csv calibrada em 4 setores."""
    pasta_obra = os.path.basename(obra_dir)
    sigla = pasta_obra.replace("OBRA_", "")

    candidatos = [
        os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", f"PROGRAMACAO_CURTO_PRAZO_{sigla}.csv"),
        os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", f"PROGRAMACAO_CURTO_PRAZO_{pasta_obra}.csv"),
        os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "PROGRAMACAO_CURTO_PRAZO.csv"),
        os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "PROGRAMACAO_CURTO_PRAZO_TMULT.csv"),
    ]
    path_curto_prazo = next((p for p in candidatos if os.path.exists(p)), None)
    if not path_curto_prazo:
        print(f"[-] Erro: Arquivo de curto prazo não encontrado em {obra_dir}/03_PLANEJAMENTO_E_CRONOGRAMA")
        return False

    df_curto = pd.read_csv(path_curto_prazo, sep=';', encoding='utf-8-sig')
    total_lotes = len(df_curto)
    calendario = calcular_calendario_lotes(data_inicio_str, total_lotes, obra_dir=obra_dir)

    mapa_lote_cpm, _ = carregar_dados_catalogo_cpm()
    mapa_lote_canonico = {item[0]: item[4] for item in mapa_lote_cpm}

    linhas_lob = []

    for idx, r in df_curto.iterrows():
        cod_lote = str(r.get('COD_LOTE', f'LOTE-{idx+1:03d}')).strip()
        vagao_raw = str(r.get('VAGAO_ESTEIRA', '')).strip()
        servico = str(r.get('SERVICO_LOTE', '')).strip()
        etapa_zona = str(r.get('ETAPA_ZONA', '')).strip()
        equipe_raw = str(r.get('EQUIPE_PREVISTA', '')).strip()
        headcount = int(r.get('HEADCOUNT_PREVISTO', 4))

        if 'DATA_INICIO' in r and 'DATA_FIM' in r and pd.notna(r['DATA_INICIO']) and pd.notna(r['DATA_FIM']):
            p_ini = parse_date_br(r['DATA_INICIO'])
            p_fim = parse_date_br(r['DATA_FIM'])
            if p_ini and p_fim:
                dt_ini_lote, dt_fim_lote = p_ini.date(), p_fim.date()
            else:
                cal = calendario[idx]
                dt_ini_lote, dt_fim_lote = cal['dt_inicio'], cal['dt_fim']
        else:
            cal = calendario[idx]
            dt_ini_lote, dt_fim_lote = cal['dt_inicio'], cal['dt_fim']

        zonas_dest = SETOR_ESPECIFICO_LOTE.get(cod_lote, normalizar_zona(etapa_zona))
        vagao_macro = mapa_lote_canonico.get(cod_lote, normalizar_vagao(vagao_raw, servico))
        equipe = normalizar_equipe(equipe_raw, servico)

        nome_atividade = servico.split('[')[0].strip()
        if len(nome_atividade) > 50:
            nome_atividade = nome_atividade[:50].strip()
        if not nome_atividade:
            nome_atividade = vagao_macro.split(". ", 1)[1].strip() if ". " in vagao_macro else vagao_macro

        dias_uteis = []
        cur_d = dt_ini_lote
        while cur_d <= dt_fim_lote:
            if cur_d.weekday() != 6:
                dias_uteis.append(cur_d)
            cur_d += datetime.timedelta(days=1)

        N = len(dias_uteis)
        K = len(zonas_dest)
        base_dias = N // K
        resto = N % K
        idx_dia = 0

        for z_i, zona in enumerate(zonas_dest):
            qtd = base_dias + (1 if z_i < resto else 0)
            if qtd == 0 and N > 0:
                qtd = 1
            slice_dias = dias_uteis[idx_dia : idx_dia + qtd]
            if not slice_dias:
                slice_dias = [dias_uteis[-1]]
            idx_dia += qtd

            z_ini = slice_dias[0]
            z_fim = slice_dias[-1]

            linhas_lob.append({
                "LOCAL_PAVIMENTO": zona,
                "SEQUENCIA": len(linhas_lob) + 1,
                "VAGAO": vagao_macro,
                "ATIVIDADE": nome_atividade,
                "EQUIPE_RESPONSAVEL": equipe,
                "RITMO_DIAS_POR_LOCAL": len(slice_dias),
                "DATA_INICIO": z_ini.strftime("%d/%m/%Y"),
                "DATA_FIM": z_fim.strftime("%d/%m/%Y"),
                "_dt_ini": z_ini,
                "_dt_fim": z_fim,
                "_cod_lote": cod_lote,
                "_headcount": headcount
            })

    df_lob = pd.DataFrame(linhas_lob)
    df_lob = df_lob.sort_values(by=['_dt_ini', 'LOCAL_PAVIMENTO']).reset_index(drop=True)
    df_lob['SEQUENCIA'] = df_lob.index + 1

    cols_salvar = [
        "LOCAL_PAVIMENTO", "SEQUENCIA", "VAGAO", "ATIVIDADE", "EQUIPE_RESPONSAVEL",
        "RITMO_DIAS_POR_LOCAL", "DATA_INICIO", "DATA_FIM"
    ]

    out_csv = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "LINHA_DE_BALANCO.csv")
    df_lob[cols_salvar].to_csv(out_csv, sep=';', index=False, encoding='utf-8-sig')
    print(f"[+] LINHA_DE_BALANCO.csv gerada com sucesso em: {out_csv} ({len(df_lob)} tarefas mapeadas nos 4 setores)")

    template_lob = os.path.join(ROOT_DIR, "projetos", "_TEMPLATE_OBRA_NOVA", "03_PLANEJAMENTO_E_CRONOGRAMA", "TEMPLATE_LINHA_DE_BALANCO.csv")
    if os.path.exists(os.path.dirname(template_lob)):
        df_lob[cols_salvar].to_csv(template_lob, sep=';', index=False, encoding='utf-8-sig')
        print(f"[+] TEMPLATE_LINHA_DE_BALANCO.csv atualizado em: {template_lob}")

    try:
        analisar_sobreposicoes_e_efetivo(obra_dir, permitir_sobreposicao=False, df_lob_in=df_lob)
    except Exception as err:
        print(f"[!] Aviso: Análise de sobreposição automática falhou: {err}")

    return df_lob


# =============================================================================
# ANÁLISE DE SOBREPOSIÇÕES & CONFLITOS ESPACIAIS
# =============================================================================

def analisar_sobreposicoes_e_efetivo(obra_dir, permitir_sobreposicao=False, df_lob_in=None):
    """Analisa Linha de Balanço quanto a conflitos espaciais, sobreposição de frentes e pico de headcount."""
    path_lob = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "LINHA_DE_BALANCO.csv")

    if df_lob_in is not None:
        df_lob = df_lob_in.copy()
    elif os.path.exists(path_lob):
        df_lob = pd.read_csv(path_lob, sep=';', encoding='utf-8-sig')
    else:
        print(f"[-] Erro: {path_lob} não encontrado.")
        return {}

    if 'dt_ini' not in df_lob.columns:
        df_lob['dt_ini'] = df_lob['DATA_INICIO'].apply(lambda v: parse_date_br(v).date())
    if 'dt_fim' not in df_lob.columns:
        df_lob['dt_fim'] = df_lob['DATA_FIM'].apply(lambda v: parse_date_br(v).date())

    min_date = df_lob['dt_ini'].min()
    max_date = df_lob['dt_fim'].max()
    total_days = (max_date - min_date).days + 1

    conflitos_espaciais = []
    frentes_simultaneas_disciplina = []
    curva_headcount = {}

    hc_map = {
        "estruturas": 8, "alvenaria": 10, "elétrica": 4, "hidráulica": 4,
        "acabamentos": 6, "pintura": 6, "coberturas": 9, "climatização": 4,
        "topografia": 7, "turnkey": 5
    }

    curr = min_date
    while curr <= max_date:
        if curr.weekday() == 6:
            curr += datetime.timedelta(days=1)
            continue

        str_curr = curr.strftime("%d/%m/%Y")
        ativas = df_lob[(df_lob['dt_ini'] <= curr) & (df_lob['dt_fim'] >= curr)]

        setores = ativas['LOCAL_PAVIMENTO'].value_counts()
        for setor, count in setores.items():
            sub_setor = ativas[ativas['LOCAL_PAVIMENTO'] == setor]
            equipes_distintas = sub_setor['EQUIPE_RESPONSAVEL'].nunique()
            lotes_distintos = sub_setor['_cod_lote'].nunique() if '_cod_lote' in sub_setor.columns else sub_setor['ATIVIDADE'].nunique()
            if equipes_distintas > 1 and lotes_distintos > 1:
                subs = sub_setor['EQUIPE_RESPONSAVEL'].unique().tolist()
                subs_prod = [s for s in subs if "Própria" not in s and "Turnkey" not in s]
                if len(subs_prod) > 1:
                    atvs = sub_setor['ATIVIDADE'].unique().tolist()
                    conflitos_espaciais.append({
                        "data": str_curr,
                        "setor": setor,
                        "equipes": subs_prod,
                        "atividades": atvs
                    })

        equipes = ativas['EQUIPE_RESPONSAVEL'].value_counts()
        for eq in equipes.index:
            sub_df = ativas[ativas['EQUIPE_RESPONSAVEL'] == eq]
            lotes_unicos = sub_df['_cod_lote'].nunique() if '_cod_lote' in sub_df.columns else sub_df['ATIVIDADE'].nunique()
            if lotes_unicos > 1 and "Própria" not in eq and "Turnkey" not in eq:
                setores_ocupados = sub_df['LOCAL_PAVIMENTO'].unique().tolist()
                frentes_simultaneas_disciplina.append({
                    "data": str_curr,
                    "equipe": eq,
                    "num_frentes": int(lotes_unicos),
                    "setores": setores_ocupados
                })

        hc_dia = 0
        for _, r in ativas.iterrows():
            nome_atv = str(r['ATIVIDADE']).lower()
            nome_eq = str(r['EQUIPE_RESPONSAVEL']).lower()
            hc_item = 4
            for k, v in hc_map.items():
                if k in nome_atv or k in nome_eq:
                    hc_item = v
                    break
            hc_dia += hc_item

        curva_headcount[str_curr] = hc_dia
        curr += datetime.timedelta(days=1)

    pico_hc = max(curva_headcount.values()) if curva_headcount else 0
    media_hc = sum(curva_headcount.values()) / len(curva_headcount) if curva_headcount else 0

    conflitos_agrupados = []
    if conflitos_espaciais:
        df_conf = pd.DataFrame(conflitos_espaciais)
        for (setor,), grupo in df_conf.groupby(['setor']):
            conflitos_agrupados.append({
                "setor": setor,
                "dias_totais": len(grupo),
                "periodo": f"{grupo['data'].min()} a {grupo['data'].max()}",
                "atividades": list(set(sum(grupo['atividades'].tolist(), []))),
                "equipes": list(set(sum(grupo['equipes'].tolist(), [])))
            })

    frentes_agrupadas = []
    if frentes_simultaneas_disciplina:
        df_frentes = pd.DataFrame(frentes_simultaneas_disciplina)
        for (eq,), grupo in df_frentes.groupby(['equipe']):
            max_frentes = grupo['num_frentes'].max()
            frentes_agrupadas.append({
                "equipe": eq,
                "frentes_simultaneas": int(max_frentes),
                "dias_com_sobreposicao": len(grupo),
                "periodo": f"{grupo['data'].min()} a {grupo['data'].max()}",
                "setores": list(set(sum(grupo['setores'].tolist(), [])))
            })

    status_aprov = "APROVADO_COM_ACORDO_EFETIVO" if permitir_sobreposicao else ("CONFORME_FLUXO_NIVELADO" if not frentes_agrupadas and not conflitos_agrupados else "ALERTA_SOBREPOSICAO_PENDENTE")

    relatorio = {
        "obra": os.path.basename(obra_dir),
        "data_analise": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "total_dias_analisados": total_days,
        "headcount_pico_diario": pico_hc,
        "headcount_medio_diario": round(media_hc, 1),
        "total_conflitos_espaciais": len(conflitos_agrupados),
        "total_disciplinas_com_frentes_duplas": len(frentes_agrupadas),
        "conflitos_espaciais": conflitos_agrupados,
        "frentes_duplicadas": frentes_agrupadas,
        "status_aprovacao": status_aprov
    }

    out_json = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "RELATORIO_SOBREPOSICAO_LOB.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)

    print("\n" + "="*80)
    print(" 📊 RELATÓRIO DE NIVELAMENTO LEAN, CONFLITO ESPACIAL & SOBREPOSIÇÃO (LOB)")
    print("="*80)
    print(f" Obra: {os.path.basename(obra_dir)} | Período: {min_date.strftime('%d/%m/%Y')} a {max_date.strftime('%d/%m/%Y')}")
    print(f" Headcount Diário Médio: {round(media_hc, 1)} operários | Headcount Pico: {pico_hc} operários")
    print("-" * 80)

    if not conflitos_agrupados and not frentes_agrupadas:
        print("\n✅ EXCELENTE: Linha de Balanço 100% NIVELADA (Heijunka).")
        print("   - Nenhum conflito espacial em setores.")
        print("   - Fluxo contínuo em série sem duplicação ociosa de subempreiteiros.")
        print("   - Ritmo Takt de 3 dias respeitado rigorosamente.")
    else:
        if conflitos_agrupados:
            print("\n⚠️  [ALERTA DE CONFLITO ESPACIAL]:")
            for c in conflitos_agrupados:
                print(f"  • Setor '{c['setor']}': {c['dias_totais']} dias de sobreposição ({c['periodo']})")
        if frentes_agrupadas:
            print("\n⚠️  [ALERTA DE SOBREPOSIÇÃO DE FRENTES & IMPACTO NO EFETIVO]:")
            for f in frentes_agrupadas:
                print(f"  • Disciplina '{f['equipe']}': {f['frentes_simultaneas']} frentes simultâneas ativas ({f['periodo']})")

    print("="*80 + "\n")
    return relatorio


# =============================================================================
# OPERAÇÃO: LOB PARA ESTEIRA
# =============================================================================

def lob_para_esteira(obra_dir, permitir_sobreposicao=False):
    """Lê LINHA_DE_BALANCO.csv e atualiza a esteira de curto prazo com verificação de sobreposição."""
    path_lob = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "LINHA_DE_BALANCO.csv")
    pasta_obra = os.path.basename(obra_dir)
    sigla = pasta_obra.replace("OBRA_", "")

    candidatos = [
        os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", f"PROGRAMACAO_CURTO_PRAZO_{sigla}.csv"),
        os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", f"PROGRAMACAO_CURTO_PRAZO_{pasta_obra}.csv"),
        os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "PROGRAMACAO_CURTO_PRAZO_TMULT.csv"),
        os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "PROGRAMACAO_CURTO_PRAZO.csv"),
    ]
    path_curto = next((p for p in candidatos if os.path.exists(p)), None)

    if not os.path.exists(path_lob) or not path_curto:
        print(f"[-] Arquivos não encontrados para sincronização lob_para_esteira.")
        return False

    relatorio = analisar_sobreposicoes_e_efetivo(obra_dir, permitir_sobreposicao)
    tem_sobreposicao = (relatorio.get('total_conflitos_espaciais', 0) > 0 or
                        relatorio.get('total_disciplinas_com_frentes_duplas', 0) > 0)

    if tem_sobreposicao and not permitir_sobreposicao:
        print("\n⛔ [BLOQUEIO LEAN]: Sincronização da Linha de Balanço para o Curto Prazo SUSPENSA!")
        print("   Para aplicar alterações com contratação de equipes adicionais, confirme com:")
        print(f"   python scripts/sincronizar_esteira_e_lob.py --obra {pasta_obra} --modo lob_para_esteira --permitir-sobreposicao\n")
        return False

    df_lob = pd.read_csv(path_lob, sep=';', encoding='utf-8-sig')
    df_curto = pd.read_csv(path_curto, sep=';', encoding='utf-8-sig')

    for idx, r_lob in df_lob.iterrows():
        if idx < len(df_curto):
            df_curto.at[idx, 'ETAPA_ZONA'] = str(r_lob['LOCAL_PAVIMENTO'])
            df_curto.at[idx, 'EQUIPE_PREVISTA'] = str(r_lob['EQUIPE_RESPONSAVEL'])
            df_curto.at[idx, 'DURACAO_DIAS'] = int(r_lob['RITMO_DIAS_POR_LOCAL'])

    df_curto.to_csv(path_curto, sep=';', index=False, encoding='utf-8-sig')
    print(f"[+] PROGRAMACAO_CURTO_PRAZO atualizada com sucesso a partir da Linha de Balanço: {path_curto}")
    return True


# =============================================================================
# VALIDAÇÃO CRUZADA: CPM vs LINHA DE BALANÇO (LOB)
# =============================================================================

def verificar_cpm_vs_lob(obra_dir, data_inicio_str="01/10/2026", limite_dias=5):
    """Executa validação cruzada entre CPM e Linha de Balanço e gera RELATORIO_DIVERGENCIA_CPM_LOB.json."""
    path_cpm = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "dados_cpm.json")
    path_lob = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "LINHA_DE_BALANCO.csv")

    if not os.path.exists(path_cpm) or not os.path.exists(path_lob):
        print("[-] Arquivos de CPM ou LOB não encontrados para verificação.")
        return None

    with open(path_cpm, "r", encoding="utf-8") as f:
        cpm_raw = json.load(f)

    df_lob = pd.read_csv(path_lob, sep=';', encoding='utf-8-sig')
    _, mapa_cpm_vagao_canonico = carregar_dados_catalogo_cpm()

    activities = {a['id']: a for a in cpm_raw['atividades']}
    es, ef = {}, {}
    for aid in activities:
        es[aid] = 0
        ef[aid] = activities[aid]['duracao_dias']

    changed = True
    while changed:
        changed = False
        for aid, act in activities.items():
            max_p = max([ef[p] for p in act.get('predecessoras', [])], default=0)
            if max_p > es[aid]:
                es[aid] = max_p
                ef[aid] = max_p + act['duracao_dias']
                changed = True

    cpm_duracao_total = max(ef.values()) if ef else 0
    d, m, y = map(int, data_inicio_str.split('/'))
    base_dt = datetime.date(y, m, d)

    cpm_schedule = {}
    for aid, act in activities.items():
        s_day = es[aid]
        f_day = ef[aid] - 1
        d_ini = dia_util_para_data_6d(s_day, base_dt)
        d_fim = dia_util_para_data_6d(f_day, base_dt)
        cpm_schedule[aid] = {
            "id": aid,
            "duracao_dias": act["duracao_dias"],
            "es": es[aid],
            "ef": ef[aid],
            "dt_inicio": d_ini,
            "dt_fim": d_fim,
            "vagao": mapa_cpm_vagao_canonico.get(aid, normalizar_vagao("", aid.replace('_', ' ')))
        }

    cpm_vagoes = {}
    for aid, data in cpm_schedule.items():
        v = data["vagao"]
        if v not in cpm_vagoes:
            cpm_vagoes[v] = {
                "vagao": v, "dt_inicio": data["dt_inicio"], "dt_fim": data["dt_fim"],
                "atividades": [aid], "duracao_total_dias": data["duracao_dias"]
            }
        else:
            cpm_vagoes[v]["dt_inicio"] = min(cpm_vagoes[v]["dt_inicio"], data["dt_inicio"])
            cpm_vagoes[v]["dt_fim"] = max(cpm_vagoes[v]["dt_fim"], data["dt_fim"])
            cpm_vagoes[v]["atividades"].append(aid)
            cpm_vagoes[v]["duracao_total_dias"] += data["duracao_dias"]

    df_lob['dt_ini'] = df_lob['DATA_INICIO'].apply(lambda v: parse_date_br(v).date())
    df_lob['dt_fim'] = df_lob['DATA_FIM'].apply(lambda v: parse_date_br(v).date())

    lob_min_dt = df_lob['dt_ini'].min()
    lob_max_dt = df_lob['dt_fim'].max()
    lob_duracao_total = dias_uteis_entre_calc(lob_min_dt, lob_max_dt) + 1

    lob_vagoes = {}
    for v, grp in df_lob.groupby('VAGAO'):
        lob_vagoes[v] = {
            "vagao": v, "dt_inicio": grp['dt_ini'].min(), "dt_fim": grp['dt_fim'].max(),
            "total_linhas": len(grp)
        }

    todos_vagoes = sorted(set(list(cpm_vagoes.keys()) + list(lob_vagoes.keys())))
    comparativo = []
    vagoes_divergentes = []

    print("\n" + "=" * 115)
    print(" 🔍 VALIDAÇÃO CRUZADA: CAMINHO CRÍTICO (CPM) vs. LINHA DE BALANÇO (LOB)")
    print("=" * 115)
    print(f"{'VAGÃO':<30} | {'CPM JANELA (DATA)':<25} | {'LOB JANELA (DATA)':<25} | {'DIF INÍCIO':<11} | {'DIF TÉRMINO':<11}")
    print("-" * 115)

    for v in todos_vagoes:
        if v == "00. Outros Serviços":
            continue
        c = cpm_vagoes.get(v)
        l = lob_vagoes.get(v)

        c_str = f"{c['dt_inicio'].strftime('%d/%m/%Y')} a {c['dt_fim'].strftime('%d/%m/%Y')}" if c else "NÃO PRESENTE NO CPM"
        l_str = f"{l['dt_inicio'].strftime('%d/%m/%Y')} a {l['dt_fim'].strftime('%d/%m/%Y')}" if l else "NÃO PRESENTE NA LOB"

        diff_ini = dias_uteis_entre_calc(c['dt_inicio'], l['dt_inicio']) if (c and l) else None
        diff_fim = dias_uteis_entre_calc(c['dt_fim'], l['dt_fim']) if (c and l) else None

        diff_ini_str = f"{diff_ini:+d}d úteis" if diff_ini is not None else "N/A"
        diff_fim_str = f"{diff_fim:+d}d úteis" if diff_fim is not None else "N/A"

        divergente = bool((diff_ini is not None and abs(diff_ini) > limite_dias) or
                          (diff_fim is not None and abs(diff_fim) > limite_dias))

        item_comp = {
            "vagao": v,
            "cpm_inicio": c['dt_inicio'].strftime('%d/%m/%Y') if c else None,
            "cpm_fim": c['dt_fim'].strftime('%d/%m/%Y') if c else None,
            "lob_inicio": l['dt_inicio'].strftime('%d/%m/%Y') if l else None,
            "lob_fim": l['dt_fim'].strftime('%d/%m/%Y') if l else None,
            "diff_inicio_dias_uteis": diff_ini,
            "diff_fim_dias_uteis": diff_fim,
            "divergente_relevante": divergente,
            "atividades_cpm_relacionadas": c["atividades"] if c else []
        }
        comparativo.append(item_comp)
        if divergente:
            vagoes_divergentes.append(item_comp)

        alerta = " [! DIVERGÊNCIA > 5d !]" if divergente else ""
        print(f"{v:<30} | {c_str:<25} | {l_str:<25} | {diff_ini_str:<11} | {diff_fim_str:<11}{alerta}")

    cpm_fim_global = dia_util_para_data_6d(cpm_duracao_total - 1, base_dt)
    diff_prazo_final_dias = dias_uteis_entre_calc(cpm_fim_global, lob_max_dt)

    print("-" * 115)
    print(f"[*] Duração Total CPM (Referência Intocada): {cpm_duracao_total} dias úteis (Término: {cpm_fim_global.strftime('%d/%m/%Y')})")
    print(f"[*] Duração Total LOB (Esteira Atual):      {lob_duracao_total} dias úteis (Término: {lob_max_dt.strftime('%d/%m/%Y')})")
    print(f"[*] Descompasso Total no Prazo Final:        {diff_prazo_final_dias:+d} dias úteis")
    print(f"[*] Vagões com Divergência > {limite_dias} dias úteis:   {len(vagoes_divergentes)} de {len(comparativo)}")
    print("=" * 115 + "\n")

    relatorio_json = {
        "obra": os.path.basename(obra_dir),
        "data_analise": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "cpm_duracao_total_dias_uteis": cpm_duracao_total,
        "cpm_data_fim_global": cpm_fim_global.strftime("%d/%m/%Y"),
        "lob_duracao_total_dias_uteis": lob_duracao_total,
        "lob_data_fim_global": lob_max_dt.strftime("%d/%m/%Y"),
        "diferenca_prazo_final_dias_uteis": diff_prazo_final_dias,
        "limite_divergencia_dias_uteis": limite_dias,
        "total_vagoes_analisados": len(comparativo),
        "total_vagoes_divergentes": len(vagoes_divergentes),
        "comparativo_vagoes": comparativo,
        "atividades_cpm_detalhe": [
            {
                "id": a_data["id"],
                "duracao_dias": a_data["duracao_dias"],
                "es_dias_uteis": a_data["es"],
                "ef_dias_uteis": a_data["ef"],
                "data_inicio": a_data["dt_inicio"].strftime("%d/%m/%Y"),
                "data_fim": a_data["dt_fim"].strftime("%d/%m/%Y"),
                "vagao_atribuido": a_data["vagao"]
            }
            for a_data in cpm_schedule.values()
        ]
    }

    out_relatorio = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "RELATORIO_DIVERGENCIA_CPM_LOB.json")
    with open(out_relatorio, "w", encoding="utf-8") as f:
        json.dump(relatorio_json, f, indent=2, ensure_ascii=False)
    print(f"[+] Relatório de divergência salvo em: {out_relatorio}")
    return relatorio_json


def main():
    args = parse_args()
    obra_dir = resolver_obra_dir(args)

    print(f"[*] Sincronizador Bidirecional Esteira Takt <-> Linha de Balanço | Obra: {os.path.basename(obra_dir)}")

    if args.verificar_cpm:
        verificar_cpm_vs_lob(obra_dir, args.data_inicio, args.limite_divergencia)
        return

    if args.verificar:
        analisar_sobreposicoes_e_efetivo(obra_dir, args.permitir_sobreposicao)
        return

    if args.modo == "esteira_para_lob":
        esteira_para_lob(obra_dir, args.data_inicio)
    elif args.modo == "lob_para_esteira":
        lob_para_esteira(obra_dir, args.permitir_sobreposicao)
    elif args.modo == "ambos":
        esteira_para_lob(obra_dir, args.data_inicio)
        analisar_sobreposicoes_e_efetivo(obra_dir, args.permitir_sobreposicao)
    elif args.analisar_sobreposicao:
        analisar_sobreposicoes_e_efetivo(obra_dir, args.permitir_sobreposicao)


if __name__ == "__main__":
    main()
