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
"""

import os
import sys
import argparse
import datetime
import json
import pandas as pd

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def parse_args():
    parser = argparse.ArgumentParser(description="Sincronizador Bidirecional Esteira Takt <-> Linha de Balanço")
    parser.add_argument("--obra", type=str, default="OBRA_TMULT", help="Nome da pasta da obra")
    parser.add_argument("--modo", type=str, choices=["esteira_para_lob", "lob_para_esteira", "ambos"], default="esteira_para_lob")
    parser.add_argument("--data-inicio", type=str, default="01/10/2026", help="Data de início (DD/MM/AAAA)")
    parser.add_argument("--verificar", action="store_true", help="Executa verificação de conformidade")
    parser.add_argument("--analisar-sobreposicao", action="store_true", help="Analisa sobreposições e pico de efetivo")
    parser.add_argument("--permitir-sobreposicao", action="store_true", help="Confirmação explícita de aumento de efetivo por sobreposição")
    return parser.parse_args()

def calcular_calendario_lotes(data_inicio_str, total_lotes=52):
    """
    Calcula as datas de início e fim para cada um dos 52 lotes de 3 dias úteis (Seg-Qua e Qui-Sáb).
    Início padrão da TMULT: 01/10/2026 (Quinta-feira).
    """
    d, m, y = map(int, data_inicio_str.split('/'))
    data_atual = datetime.date(y, m, d)
    
    calendario = []
    
    for lote_idx in range(total_lotes):
        semana_num = (lote_idx // 2) + 1
        ciclo_num = (lote_idx % 2) + 1  # 1: Seg-Qua (ou primeiros 3 dias), 2: Qui-Sáb (segundos 3 dias)
        
        # Se for domingo, pula para segunda
        if data_atual.weekday() == 6:
            data_atual += datetime.timedelta(days=1)
            
        dt_ini = data_atual
        
        # Duração de 3 dias de trabalho
        # Avança 2 dias úteis
        dias_uteis_adicionados = 0
        cursor = dt_ini
        while dias_uteis_adicionados < 2:
            cursor += datetime.timedelta(days=1)
            if cursor.weekday() != 6:  # Pula domingo
                dias_uteis_adicionados += 1
                
        dt_fim = cursor
        
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
        
        # Prepara próximo lote: dia útil seguinte
        prox = dt_fim + datetime.timedelta(days=1)
        if prox.weekday() == 6:  # Pula domingo
            prox += datetime.timedelta(days=1)
        data_atual = prox
        
    return calendario

def normalizar_zona(etapa_zona_str):
    """Normaliza o texto do lote para as 4 Zonas Físicas da Linha de Balanço (sem setores fictícios)."""
    s = (etapa_zona_str or "").lower()
    
    # 1. Cobertura
    if "cobertura" in s or "platibanda" in s or "telha" in s:
        return ["Zona 04 - Cobertura e Platibanda"]
        
    # 2. Zonas específicas individuais
    if "zona 1" in s or "etapa 1" in s:
        if "zona 2" in s or "etapa 2" in s:
            return ["Zona 01 - Recepção/Diretoria", "Zona 02 - Salas Técnicas/CPD"]
        return ["Zona 01 - Recepção/Diretoria"]
        
    if "zona 2" in s or "etapa 2" in s:
        if "zona 3" in s or "etapa 3" in s:
            return ["Zona 02 - Salas Técnicas/CPD", "Zona 03 - Sanitários e Apoio"]
        return ["Zona 02 - Salas Técnicas/CPD"]
        
    if "zona 3" in s or "etapa 3" in s:
        return ["Zona 03 - Sanitários e Apoio"]
        
    # 3. Serviços gerais de térreo (Laje, Instalações, etc.) -> Cobrem as 3 zonas térreas
    if "térreo geral" in s or "todos os setores" in s or "geral" in s or "áreas secas" in s or "paredes internas" in s:
        return ["Zona 01 - Recepção/Diretoria", "Zona 02 - Salas Técnicas/CPD", "Zona 03 - Sanitários e Apoio"]
        
    # 4. Serviços de comissionamento/turnkey geral -> Cobrem as 3 zonas do edifício
    if "turnkey" in s or "edifício" in s or "vistoria" in s or "entrega" in s or "canteiro" in s:
        return ["Zona 01 - Recepção/Diretoria", "Zona 02 - Salas Técnicas/CPD", "Zona 03 - Sanitários e Apoio"]
        
    return ["Zona 01 - Recepção/Diretoria", "Zona 02 - Salas Técnicas/CPD", "Zona 03 - Sanitários e Apoio"]

def normalizar_vagao(vagao_str, servico_str):
    """Classifica o serviço em um dos Grandes Vagões de Produção Contínua."""
    s = (servico_str or "").lower()
    v = (vagao_str or "").lower()
    
    if "topografia" in v or "canteiro" in v or "locação" in s:
        return "01. Topografia & Canteiro"
    if "sapata" in s or "cavas" in s or ("escava" in s and "baldrame" not in s):
        return "02. Fundações Sapatas"
    if "baldrame" in s or "vb" in s:
        return "03. Vigas Baldrames"
    if "pilar" in s:
        return "04. Pilares Supraestrutura"
    if "viga" in s or "laje" in s or "cimbramento" in s or "vigota" in s:
        return "05. Vigas & Laje H12"
    if "alvenaria" in s or "bloco de concreto" in s or "bloco" in s:
        return "06. Alvenaria de Vedação"
    if "cobertura" in s or "telha" in s or "terça" in s or "rufo" in s:
        return "07. Cobertura Metálica"
    if "eletroduto" in s or "tubo" in s or "hidrostático" in s or "embutid" in s:
        return "08. Instalações Embutidas"
    if "chapisco" in s or "reboco" in s or "emboço" in s:
        return "09. Reboco Paulista"
    if "impermeabiliz" in s or "contrapiso" in s or "porcelanato" in s or "cerâmica" in s or "rodapé" in s:
        return "10. Pisos & Porcelanato"
    if "esquadria" in s or "janela" in s or "porta" in s or "vidro" in s:
        return "11. Esquadrias de Alumínio"
    if "climatiza" in s or "hvac" in s or "frigorígen" in s or "ar-condicionado" in s or "evaporadora" in s:
        return "12. Climatização HVAC"
    if "cabo" in s or "quadro" in s or "qgbt" in s or "luminária" in s or "tomada" in s or "louça" in s or "metal" in s:
        return "13. Acabamentos Elétr./Hidr."
    if "pintura" in s or "massa acrílica" in s or "látex" in s:
        return "14. Pintura Acrílica Final"
    if "comissionamento" in s or "limpeza" in s or "as-built" in s or "databook" in s or "treinamento" in s or "vistoria" in s or "entrega" in s or "auditoria" in s:
        return "15. Comissionamento & Entrega"
    return "00. Outros Serviços"

def normalizar_equipe(equipe_str, servico_str):
    """Identifica o subempreiteiro e disciplina com rigor de prioridades."""
    e = (equipe_str or "").lower()
    s = (servico_str or "").lower()
    
    # 1. Estruturas pesadas / Lajes
    if "laje" in s or "vigota" in s or "treliç" in s or "cimbramento" in s:
        return "SUB-01 Estruturas e Concreto"
    # 2. Disciplinas específicas
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
    if "armador" in e or "carpinteiro" in e or "concreto" in s or "sapata" in s or "baldrame" in s or "pilar" in s or "laje" in s or "fôrma" in s or "escava" in s or "sub-01" in e:
        return "SUB-01 Estruturas e Concreto"
    return "Equipe Própria / Turnkey"

def esteira_para_lob(obra_dir, data_inicio_str="01/10/2026"):
    """
    Lê PROGRAMACAO_CURTO_PRAZO_*.csv e gera a LINHA_DE_BALANCO.csv calibrada para os 4 setores físicos reais.
    """
    path_curto_prazo = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "PROGRAMACAO_CURTO_PRAZO_TMULT.csv")
    if not os.path.exists(path_curto_prazo):
        # Tenta nome genérico
        path_curto_prazo = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "PROGRAMACAO_CURTO_PRAZO.csv")
        
    if not os.path.exists(path_curto_prazo):
        print(f"[-] Erro: Arquivo de curto prazo não encontrado em {path_curto_prazo}")
        return False
        
    df_curto = pd.read_csv(path_curto_prazo, sep=';', encoding='utf-8')
    total_lotes = len(df_curto)
    calendario = calcular_calendario_lotes(data_inicio_str, total_lotes)
    
    linhas_lob = []
    
    for idx, r in df_curto.iterrows():
        cal = calendario[idx]
        cod_lote = str(r.get('COD_LOTE', f'LOTE-{idx+1:03d}')).strip()
        vagao_raw = str(r.get('VAGAO_ESTEIRA', '')).strip()
        servico = str(r.get('SERVICO_LOTE', '')).strip()
        etapa_zona = str(r.get('ETAPA_ZONA', '')).strip()
        equipe_raw = str(r.get('EQUIPE_PREVISTA', '')).strip()
        headcount = int(r.get('HEADCOUNT_PREVISTO', 4))
        
        zonas_dest = normalizar_zona(etapa_zona)
        vagao_macro = normalizar_vagao(vagao_raw, servico)
        equipe = normalizar_equipe(equipe_raw, servico)
        
        # Nome amigável da atividade
        nome_atividade = vagao_raw
        if ":" in nome_atividade:
            nome_atividade = nome_atividade.split(":", 1)[1].strip()
            
        # Dias úteis reais dentro do lote de 3 dias
        dias_uteis = []
        cur_d = cal['dt_inicio']
        while cur_d <= cal['dt_fim']:
            if cur_d.weekday() != 6:
                dias_uteis.append(cur_d)
            cur_d += datetime.timedelta(days=1)
            
        # Fluxo Lean Nivelado (Heijunka): se o lote contempla as 3 zonas e 3 dias úteis,
        # a equipe avança sequencialmente 1 dia em cada zona (Z1 -> Z2 -> Z3),
        # garantindo zero sobreposição de equipes e zero conflito espacial.
        if len(zonas_dest) == 3 and len(dias_uteis) == 3:
            for z_i, zona in enumerate(zonas_dest):
                dia = dias_uteis[z_i]
                linhas_lob.append({
                    "LOCAL_PAVIMENTO": zona,
                    "SEQUENCIA": len(linhas_lob) + 1,
                    "VAGAO": vagao_macro,
                    "ATIVIDADE": nome_atividade,
                    "EQUIPE_RESPONSAVEL": equipe,
                    "RITMO_DIAS_POR_LOCAL": 1,
                    "DATA_INICIO": dia.strftime("%d/%m/%Y"),
                    "DATA_FIM": dia.strftime("%d/%m/%Y"),
                    "_dt_ini": dia,
                    "_dt_fim": dia,
                    "_cod_lote": cod_lote,
                    "_headcount": headcount
                })
        elif len(zonas_dest) == 1:
            linhas_lob.append({
                "LOCAL_PAVIMENTO": zonas_dest[0],
                "SEQUENCIA": len(linhas_lob) + 1,
                "VAGAO": vagao_macro,
                "ATIVIDADE": nome_atividade,
                "EQUIPE_RESPONSAVEL": equipe,
                "RITMO_DIAS_POR_LOCAL": len(dias_uteis),
                "DATA_INICIO": cal['str_inicio'],
                "DATA_FIM": cal['str_fim'],
                "_dt_ini": cal['dt_inicio'],
                "_dt_fim": cal['dt_fim'],
                "_cod_lote": cod_lote,
                "_headcount": headcount
            })
        else:
            for z_i, zona in enumerate(zonas_dest):
                dia_idx = min(z_i, len(dias_uteis) - 1)
                dia = dias_uteis[dia_idx]
                linhas_lob.append({
                    "LOCAL_PAVIMENTO": zona,
                    "SEQUENCIA": len(linhas_lob) + 1,
                    "VAGAO": vagao_macro,
                    "ATIVIDADE": nome_atividade,
                    "EQUIPE_RESPONSAVEL": equipe,
                    "RITMO_DIAS_POR_LOCAL": 1,
                    "DATA_INICIO": dia.strftime("%d/%m/%Y"),
                    "DATA_FIM": dia.strftime("%d/%m/%Y"),
                    "_dt_ini": dia,
                    "_dt_fim": dia,
                    "_cod_lote": cod_lote,
                    "_headcount": headcount
                })
            
    df_lob = pd.DataFrame(linhas_lob)
    
    # Ordena por DATA_INICIO real e LOCAL_PAVIMENTO
    df_lob = df_lob.sort_values(by=['_dt_ini', 'LOCAL_PAVIMENTO']).reset_index(drop=True)
    df_lob['SEQUENCIA'] = df_lob.index + 1
    
    cols_salvar = [
        "LOCAL_PAVIMENTO", "SEQUENCIA", "VAGAO", "ATIVIDADE", "EQUIPE_RESPONSAVEL",
        "RITMO_DIAS_POR_LOCAL", "DATA_INICIO", "DATA_FIM"
    ]
    
    out_csv = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "LINHA_DE_BALANCO.csv")
    df_lob[cols_salvar].to_csv(out_csv, sep=';', index=False, encoding='utf-8')
    print(f"[+] LINHA_DE_BALANCO.csv gerada com sucesso em: {out_csv} ({len(df_lob)} tarefas mapeadas nos 4 setores)")
    
    # Sincroniza também com o template se estiver na TMULT
    template_lob = os.path.join(obra_dir, "..", "_TEMPLATE_OBRA_NOVA", "03_PLANEJAMENTO_E_CRONOGRAMA", "TEMPLATE_LINHA_DE_BALANCO.csv")
    if os.path.exists(os.path.dirname(template_lob)):
        df_lob[cols_salvar].to_csv(template_lob, sep=';', index=False, encoding='utf-8')
        print(f"[+] TEMPLATE_LINHA_DE_BALANCO.csv atualizado em: {template_lob}")
        
    return df_lob

def analisar_sobreposicoes_e_efetivo(obra_dir, permitir_sobreposicao=False):
    """
    Analisa a Linha de Balanço e a Esteira quanto a:
    1. Conflito Espacial (duas equipes diferentes trabalhando na mesma Zona no mesmo dia)
    2. Sobreposição de Frentes da mesma disciplina (exigindo duplicação de equipes)
    3. Headcount diário e detecção de sobrecarga em relação ao Histograma
    """
    path_lob = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "LINHA_DE_BALANCO.csv")
    path_curto = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "PROGRAMACAO_CURTO_PRAZO_TMULT.csv")
    
    if not os.path.exists(path_lob):
        print(f"[-] Erro: {path_lob} não encontrado.")
        return
        
    df_lob = pd.read_csv(path_lob, sep=';', encoding='utf-8')
    
    def parse_d(val):
        d, m, y = map(int, str(val).strip().split('/'))
        return datetime.date(y, m, d)
        
    df_lob['dt_ini'] = df_lob['DATA_INICIO'].apply(parse_d)
    df_lob['dt_fim'] = df_lob['DATA_FIM'].apply(parse_d)
    
    min_date = df_lob['dt_ini'].min()
    max_date = df_lob['dt_fim'].max()
    total_days = (max_date - min_date).days + 1
    
    conflitos_espaciais = []
    frentes_simultaneas_disciplina = []
    curva_headcount = {}
    
    # Mapa de headcount estimado por atividade se não tiver lote
    hc_map = {
        "estruturas": 8, "alvenaria": 10, "elétrica": 4, "hidráulica": 4,
        "acabamentos": 6, "pintura": 6, "coberturas": 9, "climatização": 4,
        "topografia": 7, "turnkey": 5
    }
    
    curr = min_date
    while curr <= max_date:
        if curr.weekday() == 6:  # Domingo não conta
            curr += datetime.timedelta(days=1)
            continue
            
        str_curr = curr.strftime("%d/%m/%Y")
        # Tarefas ativas neste dia
        ativas = df_lob[(df_lob['dt_ini'] <= curr) & (df_lob['dt_fim'] >= curr)]
        
        # 1. Checar Conflito Espacial (mesmo setor, lotes/disciplinas concorrentes diferentes)
        setores = ativas['LOCAL_PAVIMENTO'].value_counts()
        for setor, count in setores.items():
            sub_setor = ativas[ativas['LOCAL_PAVIMENTO'] == setor]
            lotes_setor = sub_setor['_cod_lote'].nunique() if '_cod_lote' in sub_setor.columns else sub_setor['ATIVIDADE'].nunique()
            if lotes_setor > 1:
                subs = sub_setor['EQUIPE_RESPONSAVEL'].unique().tolist()
                atvs = sub_setor['ATIVIDADE'].unique().tolist()
                conflitos_espaciais.append({
                    "data": str_curr,
                    "setor": setor,
                    "equipes": subs,
                    "atividades": atvs
                })
                
        # 2. Checar Frentes Simultâneas da Mesma Disciplina (Lotes concorrentes distintos)
        equipes = ativas['EQUIPE_RESPONSAVEL'].value_counts()
        for eq in equipes.index:
            sub_df = ativas[ativas['EQUIPE_RESPONSAVEL'] == eq]
            # Considera duplicação apenas se houver LOTES DISTINTOS ativos no mesmo dia
            lotes_unicos = sub_df['_cod_lote'].nunique() if '_cod_lote' in sub_df.columns else sub_df['ATIVIDADE'].nunique()
            if lotes_unicos > 1 and "Própria" not in eq and "Turnkey" not in eq:
                setores_ocupados = sub_df['LOCAL_PAVIMENTO'].unique().tolist()
                frentes_simultaneas_disciplina.append({
                    "data": str_curr,
                    "equipe": eq,
                    "num_frentes": int(lotes_unicos),
                    "setores": setores_ocupados
                })
                
        # 3. Calcular Headcount estimado do dia
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
    
    # Deduplicar alertas por período
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
    
    # Salva relatório JSON
    out_json = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "RELATORIO_SOBREPOSICAO_LOB.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
    print("\n" + "="*80)
    print(" 📊 RELATÓRIO DE NIVELAMENTO LEAN, CONFLITO ESPACIAL & SOBREPOSIÇÃO (LOB)")
    print("="*80)
    print(f" Obra: {os.path.basename(obra_dir)} | Período: {min_date.strftime('%d/%m/%Y')} a {max_date.strftime('%d/%m/%Y')}")
    print(f" Headcount Diário Médio: {round(media_hc, 1)} operários | Headcount Pico: {pico_hc} operários")
    print("-" * 80)
    
    tem_problema = False
    
    if conflitos_agrupados:
        tem_problema = True
        print("\n⚠️  [ALERTA DE CONFLITO ESPACIAL]:")
        for c in conflitos_agrupados:
            print(f"  • Setor '{c['setor']}': {c['dias_totais']} dias de sobreposição ({c['periodo']})")
            print(f"    Equipes concorrentes: {', '.join(c['equipes'])}")
            print(f"    Atividades: {', '.join(c['atividades'])}")
            
    if frentes_agrupadas:
        tem_problema = True
        print("\n⚠️  [ALERTA DE SOBREPOSIÇÃO DE FRENTES & IMPACTO NO EFETIVO]:")
        for f in frentes_agrupadas:
            print(f"  • Disciplina '{f['equipe']}': {f['frentes_simultaneas']} frentes simultâneas ativas!")
            print(f"    Período: {f['periodo']} ({f['dias_com_sobreposicao']} dias de concorrência)")
            print(f"    Setores: {', '.join(f['setores'])}")
            print(f"    👉 IMPACTO: Requer {f['frentes_simultaneas']}x equipes mobilizadas (+{f['frentes_simultaneas']-1} equipe contratada)")
            
    if not tem_problema:
        print("\n✅ EXCELENTE: Linha de Balanço 100% NIVELADA (Heijunka).")
        print("   - Nenhum conflito espacial em setores.")
        print("   - Fluxo contínuo em série sem duplicação ociosa de subempreiteiros.")
        print("   - Ritmo Takt de 3 dias respeitado rigorosamente.")
    else:
        if permitir_sobreposicao:
            print("\n✔️  [CONCORDÂNCIA REGISTRADA]: Aumento de efetivo e sobreposição autorizados pelo gestor.")
        else:
            print("\n⚠️  [AÇÃO NECESSÁRIA]:")
            print("   Para aprovar o cronograma com frentes aceleradas em paralelo, confirme com:")
            print("   python scripts/sincronizar_esteira_e_lob.py --permitir-sobreposicao")
            print("   Ou mantenha o fluxo contínuo em série sem duplicação de custos de mobilização.")
    print("="*80 + "\n")
    
    return relatorio

def lob_para_esteira(obra_dir, permitir_sobreposicao=False):
    """
    Lê LINHA_DE_BALANCO.csv e atualiza a PROGRAMACAO_CURTO_PRAZO_*.csv.
    Se detectar sobreposição de frentes ou conflito espacial, exige 'permitir_sobreposicao=True'.
    Caso contrário, aborta a sincronização com alerta para proteger o gestor contra aumento indevido de custo.
    """
    path_lob = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "LINHA_DE_BALANCO.csv")
    path_curto = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "PROGRAMACAO_CURTO_PRAZO_TMULT.csv")
    if not os.path.exists(path_curto):
        path_curto = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "PROGRAMACAO_CURTO_PRAZO.csv")
        
    if not os.path.exists(path_lob) or not os.path.exists(path_curto):
        print(f"[-] Arquivos não encontrados para sincronização lob_para_esteira.")
        return False
        
    relatorio = analisar_sobreposicoes_e_efetivo(obra_dir, permitir_sobreposicao)
    
    tem_sobreposicao = (relatorio.get('total_conflitos_espaciais', 0) > 0 or 
                        relatorio.get('total_disciplinas_com_frentes_duplas', 0) > 0)
                        
    if tem_sobreposicao and not permitir_sobreposicao:
        print("\n⛔ [BLOQUEIO LEAN]: Sincronização da Linha de Balanço para o Curto Prazo SUSPENSA!")
        print("   Motivo: Foram detectadas sobreposições de serviços que demandam aumento de headcount.")
        print("   Para aplicar estas alterações na esteira de curto prazo com contratação de equipes adicionais, execute:")
        print("   python scripts/sincronizar_esteira_e_lob.py --obra OBRA_TMULT --modo lob_para_esteira --permitir-sobreposicao\n")
        return False

    df_lob = pd.read_csv(path_lob, sep=';', encoding='utf-8')
    df_curto = pd.read_csv(path_curto, sep=';', encoding='utf-8')
    
    # Atualiza as linhas do curto prazo correspondentes
    for idx, r_lob in df_lob.iterrows():
        if idx < len(df_curto):
            df_curto.at[idx, 'ETAPA_ZONA'] = str(r_lob['LOCAL_PAVIMENTO'])
            df_curto.at[idx, 'EQUIPE_PREVISTA'] = str(r_lob['EQUIPE_RESPONSAVEL'])
            df_curto.at[idx, 'DURACAO_DIAS'] = int(r_lob['RITMO_DIAS_POR_LOCAL'])
            
    df_curto.to_csv(path_curto, sep=';', index=False, encoding='utf-8')
    print(f"[+] PROGRAMACAO_CURTO_PRAZO atualizada com sucesso a partir da Linha de Balanço: {path_curto}")
    return True

def main():
    args = parse_args()
    
    # Determina diretório da obra
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    obra_dir = os.path.join(root_dir, "projetos", args.obra)
    
    if not os.path.exists(obra_dir):
        print(f"[-] Diretório da obra não encontrado: {obra_dir}")
        sys.exit(1)
        
    print(f"[*] Sincronizador Bidirecional Esteira Takt <-> Linha de Balanço | Obra: {args.obra}")
    
    # Se usuário chamou somente --verificar
    if args.verificar:
        analisar_sobreposicoes_e_efetivo(obra_dir, args.permitir_sobreposicao)
        return
        
    if args.modo == "esteira_para_lob":
        esteira_para_lob(obra_dir, args.data_inicio)
        if args.analisar_sobreposicao or True:
            analisar_sobreposicoes_e_efetivo(obra_dir, args.permitir_sobreposicao)
    elif args.modo == "lob_para_esteira":
        lob_para_esteira(obra_dir, args.permitir_sobreposicao)
    elif args.modo == "ambos":
        esteira_para_lob(obra_dir, args.data_inicio)
        analisar_sobreposicoes_e_efetivo(obra_dir, args.permitir_sobreposicao)
    elif args.analisar_sobreposicao:
        analisar_sobreposicoes_e_efetivo(obra_dir, args.permitir_sobreposicao)

if __name__ == "__main__":
    main()
