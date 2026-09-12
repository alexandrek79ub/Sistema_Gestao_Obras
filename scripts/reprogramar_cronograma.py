#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
MOTOR LEAN DETERMINÍSTICO DE REPROGRAMAÇÃO DE CRONOGRAMA & LINHA DE BALANÇO (LOB)
===============================================================================
Ajusta datas, durações e dimensionamento de equipes (RUP) diretamente nas planilhas
fonte (CSV) com propagação topológica em cascata (DAG) e sincronização com a esteira
de curto prazo (Lotes Takt).

Uso:
  # 1. Ver status geral do cronograma:
  python scripts/reprogramar_cronograma.py --obra OBRA_TMULT --status

  # 2. Listar tarefas com IDs para reprogramar:
  python scripts/reprogramar_cronograma.py --obra OBRA_TMULT --listar

  # 3. Alterar duração de uma tarefa (ex: Tarefa 2 para 7 dias) com cascata e RUP:
  python scripts/reprogramar_cronograma.py --obra OBRA_TMULT --tarefa-id 2 --nova-duracao 7

  # 4. Deslocar um vagão inteiro em +5 dias úteis:
  python scripts/reprogramar_cronograma.py --obra OBRA_TMULT --vagao 02 --deslocar-dias 5 --aplicar-todo-vagao

  # 5. Definir nova data de início:
  python scripts/reprogramar_cronograma.py --obra OBRA_TMULT --tarefa-id 19 --nova-data-inicio 01/12/2026

  # 6. Simular sem alterar arquivos (dry-run):
  python scripts/reprogramar_cronograma.py --obra OBRA_TMULT --tarefa-id 2 --nova-duracao 7 --dry-run
===============================================================================
"""

import os
import sys
import csv
import math
import argparse
from datetime import datetime, timedelta

# Configuração de encoding UTF-8 no Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Baseline de Headcount por Vagão (para dimensionamento RUP)
HEADCOUNT_PADRAO_VAGAO = {
    "01": 7,   # Topografia & Canteiro
    "02": 7,   # Fundações Sapatas
    "03": 8,   # Vigas Baldrames
    "04": 14,  # Pilares Supraestrutura
    "05": 14,  # Vigas & Laje H12
    "06": 10,  # Alvenaria de Vedação
    "07": 9,   # Cobertura Metálica
    "08": 8,   # Instalações Embutidas
    "09": 8,   # Reboco Paulista
    "10": 10,  # Pisos & Porcelanato
    "11": 6,   # Esquadrias de Alumínio
    "12": 6,   # Climatização HVAC
    "13": 8,   # Acabamentos Elétr./Hidr.
    "14": 8,   # Pintura Acrílica Final
    "15": 12   # Comissionamento & Entrega
}

# =============================================================================
# UTILITÁRIOS DE DATA (CALENDÁRIO DE DIAS ÚTEIS - PULA DOMINGOS)
# =============================================================================

def parse_date_br(d_str):
    """Converte string DD/MM/AAAA para datetime.date."""
    if not d_str:
        return None
    clean = str(d_str).strip().replace('"', '')
    for sep, fmt in [('/', '%d/%m/%Y'), ('-', '%Y-%m-%d')]:
        if sep in clean:
            try:
                return datetime.strptime(clean, fmt).date()
            except ValueError:
                pass
    return None

def format_date_br(d):
    """Converte datetime.date para string DD/MM/AAAA."""
    if not d:
        return ""
    return d.strftime("%d/%m/%Y")

def add_working_days(start_date, days):
    """Adiciona ou subtrai dias úteis (segunda a sábado, pulando domingos)."""
    if days == 0:
        return start_date
    cur = start_date
    step = 1 if days > 0 else -1
    remaining = abs(days)
    while remaining > 0:
        cur += timedelta(days=step)
        if cur.weekday() != 6:  # 6 = Domingo
            remaining -= 1
    return cur

def calculate_end_date(start_date, duration_days):
    """Data final considerando que o primeiro dia já é trabalhado."""
    if duration_days <= 1:
        return start_date
    return add_working_days(start_date, duration_days - 1)

def count_working_days(d_ini, d_fim):
    """Conta quantidade de dias úteis entre d_ini e d_fim (inclusivo)."""
    if not d_ini or not d_fim or d_fim < d_ini:
        return 0
    cur = d_ini
    count = 0
    while cur <= d_fim:
        if cur.weekday() != 6:
            count += 1
        cur += timedelta(days=1)
    return count

# =============================================================================
# CONSTRUÇÃO DO GRAFO DIRIGIDO ACÍCLICO (DAG) & ORDENAÇÃO TOPOLÓGICA
# =============================================================================

def build_lob_dag(rows):
    """
    Constrói as relações de precedência estritas:
    1. Sequência física natural dentro de cada Zona (ordem das linhas no CSV).
    2. Sequência de avanço de equipe (takt) no mesmo Vagão entre zonas sucessivas.
    3. Marco de Cobertura: Vagão 06 (Alvenaria Z3) -> Vagão 07 (Cobertura Metálica Z4).
    4. Marco de Comissionamento: Todas as frentes anteriores -> Vagão 15.
    
    Retorna (adj, rev_adj, topo_order).
    """
    n = len(rows)
    adj = {i: [] for i in range(n)}
    rev_adj = {i: [] for i in range(n)}

    def add_edge(u, v):
        if u == v or u < 0 or v < 0 or u >= n or v >= n:
            return
        if v not in adj[u]:
            adj[u].append(v)
        if u not in rev_adj[v]:
            rev_adj[v].append(u)

    # 1. Sequência intra-zona baseada na ordem física do CSV
    zonas_map = {}
    for idx, r in enumerate(rows):
        pav = (r.get('LOCAL_PAVIMENTO') or '').strip()
        zonas_map.setdefault(pav, []).append(idx)

    for pav, indices in zonas_map.items():
        indices.sort()  # Mantém ordem do arquivo
        for k in range(len(indices) - 1):
            add_edge(indices[k], indices[k + 1])

    # 2. Sequência de esteira da mesma disciplina entre zonas
    vagoes_map = {}
    for idx, r in enumerate(rows):
        vagao = (r.get('VAGAO') or '').strip()
        vagoes_map.setdefault(vagao, []).append(idx)

    for vagao, indices in vagoes_map.items():
        indices.sort()
        for k in range(len(indices) - 1):
            u, v = indices[k], indices[k + 1]
            d_fim_u = parse_date_br(rows[u].get('DATA_FIM'))
            d_ini_v = parse_date_br(rows[v].get('DATA_INICIO'))
            # Vincula se no planejamento original a tarefa v foi programada após ou junto com u
            if d_fim_u and d_ini_v and d_ini_v >= d_fim_u:
                add_edge(u, v)

    # 3. Marco de Cobertura (Alvenaria Z3 libera Cobertura Z4)
    idx_alvenaria_z3 = None
    for idx, r in enumerate(rows):
        if '06.' in (r.get('VAGAO') or '') and 'Zona 03' in (r.get('LOCAL_PAVIMENTO') or ''):
            idx_alvenaria_z3 = idx
            break

    if idx_alvenaria_z3 is not None:
        for idx, r in enumerate(rows):
            if '07.' in (r.get('VAGAO') or '') and 'Zona 04' in (r.get('LOCAL_PAVIMENTO') or ''):
                add_edge(idx_alvenaria_z3, idx)

    # 4. Marco de Comissionamento e Entrega (Vagão 15)
    # Sucessora final de todas as atividades
    indices_comiss = [idx for idx, r in enumerate(rows) if '15.' in (r.get('VAGAO') or '')]
    if indices_comiss:
        primeiro_comiss = min(indices_comiss)
        for idx, r in enumerate(rows):
            if '15.' not in (r.get('VAGAO') or ''):
                d_fim = parse_date_br(r.get('DATA_FIM'))
                d_ini_c = parse_date_br(rows[primeiro_comiss].get('DATA_INICIO'))
                if d_fim and d_ini_c and d_fim <= d_ini_c:
                    add_edge(idx, primeiro_comiss)

    # Kahn's Algorithm para Ordenação Topológica do DAG
    in_degree = {i: len(rev_adj[i]) for i in range(n)}
    queue = [i for i in range(n) if in_degree[i] == 0]
    topo_order = []

    while queue:
        u = queue.pop(0)
        topo_order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    # Garante inclusão de todos os nós caso haja algum desconectado
    if len(topo_order) < n:
        for i in range(n):
            if i not in topo_order:
                topo_order.append(i)

    return adj, rev_adj, topo_order

# =============================================================================
# MOTOR DE PROPAGAÇÃO EM CASCATA FORWARD (TOPOLÓGICA)
# =============================================================================

def propagate_forward_dag(rows, start_indices, adj, topo_order):
    """
    Propaga mudanças para todas as tarefas sucessoras atingíveis exatamente
    na ordem topológica do DAG. Garante zero sobreposição e fluxo contínuo.
    """
    # Encontra nós atingíveis
    reachable = set(start_indices)
    q = list(start_indices)
    while q:
        curr = q.pop(0)
        for nxt in adj[curr]:
            if nxt not in reachable:
                reachable.add(nxt)
                q.append(nxt)

    # Filtra nós atingíveis mantendo ordem topológica estrita
    active_topo = [node for node in topo_order if node in reachable]
    modified_indices = set()

    for u in active_topo:
        row_u = rows[u]
        d_fim_u = parse_date_br(row_u.get('DATA_FIM'))
        if not d_fim_u:
            continue

        for v in adj[u]:
            row_v = rows[v]
            d_ini_v = parse_date_br(row_v.get('DATA_INICIO'))
            dur_v = int(row_v.get('RITMO_DIAS_POR_LOCAL') or '3')
            if not d_ini_v:
                continue

            # Sucessora deve iniciar no primeiro dia útil após o término da predecessora
            min_ini_v = add_working_days(d_fim_u, 1)

            if d_ini_v < min_ini_v:
                row_v['DATA_INICIO'] = format_date_br(min_ini_v)
                row_v['DATA_FIM'] = format_date_br(calculate_end_date(min_ini_v, dur_v))
                modified_indices.add(v)

    return modified_indices

# =============================================================================
# SINCRONIZAÇÃO COM CURTO PRAZO (LOTES TAKT DE 3 DIAS) & RUP
# =============================================================================

def sync_short_term_schedule(base_path, obra, modified_rows, dry_run=False):
    """
    Localiza as planilhas de curto prazo (52 lotes) e atualiza durações e efetivo.
    Calcula o novo Headcount com base na RUP:
        Novo_Headcount = max(1, ceil(Headcount_Base * (Duracao_Base / Nova_Duracao)))
    """
    obra_clean = obra.replace('OBRA_', '')
    possible_files = [
        os.path.join(base_path, '03_PLANEJAMENTO_E_CRONOGRAMA', f'PROGRAMACAO_CURTO_PRAZO_{obra}.csv'),
        os.path.join(base_path, '03_PLANEJAMENTO_E_CRONOGRAMA', f'PROGRAMACAO_CURTO_PRAZO_{obra_clean}.csv'),
        os.path.join(base_path, '03_PLANEJAMENTO_E_CRONOGRAMA', 'PROGRAMACAO_CURTO_PRAZO_OBRA_TMULT.csv'),
        os.path.join(base_path, '03_PLANEJAMENTO_E_CRONOGRAMA', 'PROGRAMACAO_CURTO_PRAZO_TMULT.csv'),
    ]
    
    candidate_files = list(set([f for f in possible_files if os.path.exists(f)]))
    if not candidate_files:
        return 0, []

    total_lotes_sync = 0
    detalhes_sync = []

    for prog_file in candidate_files:
        try:
            with open(prog_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if len(lines) < 2:
                continue

            header_line = lines[0].strip()
            headers = [h.replace('"', '').strip() for h in header_line.split(';')]

            dur_idx = headers.index('DURACAO_DIAS') if 'DURACAO_DIAS' in headers else -1
            hc_idx = headers.index('HEADCOUNT_PREVISTO') if 'HEADCOUNT_PREVISTO' in headers else -1
            ini_idx = headers.index('DATA_INICIO') if 'DATA_INICIO' in headers else -1
            fim_idx = headers.index('DATA_FIM') if 'DATA_FIM' in headers else -1
            vagao_idx = headers.index('VAGAO_ESTEIRA') if 'VAGAO_ESTEIRA' in headers else -1
            zona_idx = headers.index('ETAPA_ZONA') if 'ETAPA_ZONA' in headers else -1
            lote_idx = headers.index('COD_LOTE') if 'COD_LOTE' in headers else 0

            if dur_idx == -1 or hc_idx == -1:
                continue

            file_modified = False
            new_lines = [header_line + '\n']

            for line in lines[1:]:
                if not line.strip():
                    continue
                parts = [p.replace('"', '').strip() for p in line.strip().split(';')]
                if len(parts) < len(headers):
                    new_lines.append(line)
                    continue

                lote_cod = parts[lote_idx]
                lote_vagao = parts[vagao_idx] if vagao_idx != -1 else ''
                lote_zona = parts[zona_idx].lower() if zona_idx != -1 else ''

                # Verifica se corresponde a alguma das tarefas modificadas
                for mod_row in modified_rows:
                    vagao_nome = mod_row.get('VAGAO', '')
                    vagao_prefix = vagao_nome[:2]
                    pav = mod_row.get('LOCAL_PAVIMENTO', '').lower()
                    nova_dur = int(mod_row.get('RITMO_DIAS_POR_LOCAL', 3))
                    novo_hc = mod_row.get('_calc_headcount')

                    match_vagao = vagao_prefix in lote_vagao or (vagao_nome and vagao_nome[3:10].lower() in lote_vagao.lower())
                    
                    match_zona = (
                        ('zona 01' in pav and ('zona 1' in lote_zona or 'etapa 1' in lote_zona)) or
                        ('zona 02' in pav and ('zona 2' in lote_zona or 'etapa 2' in lote_zona)) or
                        ('zona 03' in pav and ('zona 3' in lote_zona or 'etapa 3' in lote_zona)) or
                        ('zona 04' in pav and ('cobertura' in lote_zona or 'platibanda' in lote_zona))
                    )

                    if match_vagao and match_zona:
                        old_dur = int(parts[dur_idx]) if parts[dur_idx].isdigit() else 3
                        old_hc = int(parts[hc_idx]) if parts[hc_idx].isdigit() else 8

                        parts[dur_idx] = str(nova_dur)

                        if novo_hc is None:
                            if old_dur > 0 and nova_dur > 0 and old_dur != nova_dur:
                                calc_hc = max(1, math.ceil(old_hc * (old_dur / nova_dur)))
                            else:
                                calc_hc = old_hc
                        else:
                            calc_hc = int(novo_hc)

                        parts[hc_idx] = str(calc_hc)
                        
                        # Atualiza datas de início e fim no lote de curto prazo
                        if ini_idx != -1 and mod_row.get('DATA_INICIO'):
                            parts[ini_idx] = mod_row.get('DATA_INICIO')
                        if fim_idx != -1 and mod_row.get('DATA_FIM'):
                            parts[fim_idx] = mod_row.get('DATA_FIM')

                        file_modified = True
                        total_lotes_sync += 1
                        detalhes_sync.append(f"{lote_cod} ({lote_vagao[:25]} | {parts[zona_idx][:20]}): Dur {old_dur}d -> {nova_dur}d | Efetivo {old_hc} -> {calc_hc} op. | Datas: {parts[ini_idx] if ini_idx != -1 else ''} .. {parts[fim_idx] if fim_idx != -1 else ''}")
                        break

                new_lines.append(';'.join(f'"{p}"' for p in parts) + '\n')

            if file_modified and not dry_run:
                with open(prog_file, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)

        except Exception as e:
            print(f"[!] Erro ao sincronizar arquivo de curto prazo {prog_file}: {e}")

    return total_lotes_sync, detalhes_sync

def sync_cpm_schedule(base_path, obra, modified_rows, dry_run=False):
    """
    Sincroniza as alterações de frentes da Linha de Balanço diretamente no Caminho Crítico (dados_cpm.json).
    Recalcula Forward/Backward pass determinístico e atualiza datas e folgas do CPM.
    """
    cpm_path = os.path.join(base_path, '03_PLANEJAMENTO_E_CRONOGRAMA', 'dados_cpm.json')
    if not os.path.exists(cpm_path):
        return 0, []

    try:
        import json
        with open(cpm_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        atividades = dados.get('atividades', [])
        cpm_modificados = []

        # Mapeamento do prefixo do vagão para atividades CPM
        VAGAO_PARA_CPM = {
            "01": ["A01_MOB_CANTEIRO"],
            "02": ["A03_SAPATAS_CONC"],
            "03": ["A04_BALDRAMES_CONC"],
            "04": ["A07_PILARES_SUPRA"],
            "05": ["A08_VIGAS_LAJE_FORMA", "A09_CONCRET_LAJE_H12"],
            "06": ["A12_ALVENARIA_EXT", "A12_ALVENARIA_VEDACAO"],
            "07": ["A14_ESTRUT_COBERTURA", "A11_ESTRUT_TERCAS_COB", "A13_TELHAS_SANDWICH_PLAT"],
            "08": ["A17_ELETRICA_EMBUTIDA", "A14_ELET_EMBUTIDA"],
            "09": ["A19_REBOCO_INTERNO", "A17_EMBOCO_REBOCO"],
            "10": ["A20_IMPERM_AREAS_MOLHADAS", "A18_IMPERM_WCS", "A22_PISO_PORCELANATO", "A19_CONTRAPISO"],
            "11": ["A25_ESQUADRIAS_ALUM", "A21_ESQUADRIAS_FIX"],
            "12": ["A26_CLIMATIZACAO_DUTOS", "A20_INFRA_DUTOS_HVAC"],
            "13": ["A27_LOUCAS_METAIS", "A23_FIACAO_TELECOM", "A28_LUMINARIAS_ESPELHOS"],
            "14": ["A29_PINTURA_FINAL", "A25_PINTURA_1A_DEMAO"],
            "15": ["A31_LIMPEZA_ENTREGA", "A30_COMISSIONAMENTO"]
        }

        for mod_row in modified_rows:
            v_nome = mod_row.get('VAGAO', '')
            v_pref = v_nome[:2]
            if v_pref in VAGAO_PARA_CPM:
                cpm_ids = VAGAO_PARA_CPM[v_pref]
                nova_dur = int(mod_row.get('RITMO_DIAS_POR_LOCAL', 3))
                for ativ in atividades:
                    if ativ.get('id') in cpm_ids:
                        old_dur = ativ.get('duracao_dias', 3)
                        if old_dur != nova_dur and nova_dur > 0:
                            ativ['duracao_dias'] = nova_dur
                            cpm_modificados.append(f"{ativ['id']}: {old_dur}d -> {nova_dur}d")

        if cpm_modificados and not dry_run:
            try:
                root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                calc_path = os.path.join(root_dir, 'scripts', 'calculadoras', 'calcular_cpm.py')
                if os.path.exists(calc_path):
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("calcular_cpm", calc_path)
                    mod_cpm = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod_cpm)
                    res_cpm = mod_cpm.calcular_cpm(dados)
                    if res_cpm.get('status') != 'erro':
                        dados['caminho_critico_calculado'] = res_cpm
            except Exception:
                pass

            with open(cpm_path, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)

        return len(cpm_modificados), cpm_modificados
    except Exception as e:
        print(f"[!] Erro ao sincronizar dados_cpm.json: {e}")
        return 0, []

# =============================================================================
# FUNÇÕES DE COMANDO (STATUS, LISTAR, REPROGRAMAR)
# =============================================================================

def get_base_path(obra):
    """Encontra o diretório base do projeto."""
    cur = os.getcwd()
    candidates = [
        os.path.join(cur, 'projetos', obra),
        os.path.join(cur, '..', 'projetos', obra),
        os.path.join(cur, 'projetos', 'OBRA_TMULT'),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    return os.path.abspath(os.path.join(cur, 'projetos', obra))

def load_schedule_csv(csv_path):
    """Lê o arquivo CSV da Linha de Balanço preservando colunas."""
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        rows = list(reader)
        fieldnames = reader.fieldnames
    return rows, fieldnames

def save_schedule_csv(csv_path, rows, fieldnames):
    """Grava as alterações no CSV da Linha de Balanço."""
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for r in rows:
            # Remove campos internos temporários antes de salvar
            clean_r = {k: v for k, v in r.items() if not k.startswith('_')}
            writer.writerow(clean_r)

def print_status(rows, obra):
    """Imprime o resumo de status da Linha de Balanço."""
    print(f"\n==================================================================")
    print(f"  CRONOGRAMA & LINHA DE BALANÇO LEAN - {obra.upper()}")
    print(f"==================================================================")
    print(f"Total de frentes executivas cadastradas: {len(rows)}")

    dates_ini = [parse_date_br(r.get('DATA_INICIO')) for r in rows if parse_date_br(r.get('DATA_INICIO'))]
    dates_fim = [parse_date_br(r.get('DATA_FIM')) for r in rows if parse_date_br(r.get('DATA_FIM'))]

    if dates_ini and dates_fim:
        ini_global = min(dates_ini)
        fim_global = max(dates_fim)
        dias_uteis = count_working_days(ini_global, fim_global)
        dias_corridos = (fim_global - ini_global).days + 1
        semanas = math.ceil(dias_uteis / 6)
        print(f"Início Global do Empreendimento : {format_date_br(ini_global)}")
        print(f"Término Global Previsto         : {format_date_br(fim_global)}")
        print(f"Duração Total                   : {dias_uteis} dias úteis ({dias_corridos} corridos, ~{semanas} semanas)")
    
    print("\nFRENTES POR VAGÃO (ESTEIRA TAKT):")
    print(f"{'Vagão':<32} | {'Frentes':<8} | {'Início':<12} | {'Término':<12} | {'Ritmo (dias)':<12}")
    print("-" * 85)

    vagoes_dict = {}
    for r in rows:
        v = (r.get('VAGAO') or 'Indefinido').strip()
        vagoes_dict.setdefault(v, []).append(r)

    for v, itens in vagoes_dict.items():
        inis = [parse_date_br(r.get('DATA_INICIO')) for r in itens if parse_date_br(r.get('DATA_INICIO'))]
        fims = [parse_date_br(r.get('DATA_FIM')) for r in itens if parse_date_br(r.get('DATA_FIM'))]
        ritmos = [r.get('RITMO_DIAS_POR_LOCAL', '3') for r in itens]
        ritmo_str = "/".join(sorted(set(ritmos)))
        ini_str = format_date_br(min(inis)) if inis else "-"
        fim_str = format_date_br(max(fims)) if fims else "-"
        print(f"{v:<32} | {len(itens):<8} | {ini_str:<12} | {fim_str:<12} | {ritmo_str:<12}")

    print("==================================================================\n")

def list_tasks(rows):
    """Lista todas as tarefas com ID para facilitar a seleção."""
    print(f"\n{'ID':<4} | {'Setor / Pavimento':<30} | {'Vagão / Atividade':<32} | {'Início':<10} | {'Fim':<10} | {'Dias':<4}")
    print("-" * 105)
    for idx, r in enumerate(rows):
        t_id = idx + 1
        pav = r.get('LOCAL_PAVIMENTO', '')[:30]
        vag = (r.get('VAGAO') or r.get('ATIVIDADE', ''))[:32]
        ini = r.get('DATA_INICIO', '')
        fim = r.get('DATA_FIM', '')
        dur = r.get('RITMO_DIAS_POR_LOCAL', '3')
        print(f"{t_id:<4} | {pav:<30} | {vag:<32} | {ini:<10} | {fim:<10} | {dur:<4}")
    print("-" * 105)
    print(f"Total: {len(rows)} tarefas. Use --tarefa-id <ID> para reprogramar.\n")

# =============================================================================
# EXECUÇÃO PRINCIPAL DE REPROGRAMAÇÃO
# =============================================================================

def reprogramar(args):
    obra = args.obra
    base_path = get_base_path(obra)
    csv_path = os.path.join(base_path, '03_PLANEJAMENTO_E_CRONOGRAMA', 'LINHA_DE_BALANCO.csv')

    if not os.path.exists(csv_path):
        print(f"[!] ERRO: Arquivo não encontrado: {csv_path}")
        sys.exit(1)

    rows, fieldnames = load_schedule_csv(csv_path)

    if args.status:
        print_status(rows, obra)
        return

    if args.listar:
        list_tasks(rows)
        return

    # Identificação dos alvos da alteração
    target_indices = []

    if args.tarefa_id:
        target_idx = args.tarefa_id - 1
        if 0 <= target_idx < len(rows):
            target_indices.append(target_idx)
        else:
            print(f"[!] ERRO: Tarefa ID {args.tarefa_id} inválida. Escolha entre 1 e {len(rows)}.")
            sys.exit(1)

    elif args.vagao:
        v_busca = args.vagao.strip().lower()
        for idx, r in enumerate(rows):
            v_nome = (r.get('VAGAO') or '').lower()
            if v_busca in v_nome or v_nome.startswith(v_busca):
                if args.setor:
                    s_busca = args.setor.strip().lower()
                    pav = (r.get('LOCAL_PAVIMENTO') or '').lower()
                    if s_busca in pav:
                        target_indices.append(idx)
                else:
                    target_indices.append(idx)

    if not target_indices:
        print("[!] Nenhuma tarefa especificada para reprogramação.")
        print("    Use --status para visualizar, --listar para ver IDs ou passe --tarefa-id / --vagao.")
        return

    # Se não foi solicitado aplicar em todo o vagão e há múltiplos alvos selecionados por vagão,
    # pega apenas o primeiro a menos que args.aplicar_todo_vagao seja True
    if len(target_indices) > 1 and not args.aplicar_todo_vagao and not args.vagao:
        target_indices = [target_indices[0]]

    # Constrói o DAG e a ordenação topológica
    adj, rev_adj, topo_order = build_lob_dag(rows)

    print(f"\n==================================================================")
    print(f"  EXECUTANDO REPROGRAMAÇÃO LEAN - OBRA: {obra}")
    print(f"  Modo Dry-Run (Simulação): {'SIM' if args.dry_run else 'NÃO (Gravando no CSV)'}")
    print(f"==================================================================")

    modified_initial = []

    for t_idx in target_indices:
        row = rows[t_idx]
        vagao_nome = row.get('VAGAO', '')
        pavimento = row.get('LOCAL_PAVIMENTO', '')
        old_dur = int(row.get('RITMO_DIAS_POR_LOCAL') or '3')
        old_ini = row.get('DATA_INICIO', '')
        old_fim = row.get('DATA_FIM', '')
        old_d_ini = parse_date_br(old_ini)

        # 1. Ajuste de Duração
        nova_dur = old_dur
        if args.nova_duracao is not None and args.nova_duracao > 0:
            nova_dur = args.nova_duracao
            row['RITMO_DIAS_POR_LOCAL'] = str(nova_dur)

        # 2. Ajuste de Data de Início
        if args.nova_data_inicio:
            novo_d_ini = parse_date_br(args.nova_data_inicio)
            if novo_d_ini:
                row['DATA_INICIO'] = format_date_br(novo_d_ini)
                old_d_ini = novo_d_ini

        # 3. Deslocamento relativo em dias úteis
        if args.deslocar_dias:
            if old_d_ini:
                novo_d_ini = add_working_days(old_d_ini, args.deslocar_dias)
                row['DATA_INICIO'] = format_date_br(novo_d_ini)
                old_d_ini = novo_d_ini

        # Recalcula data de fim garantindo dias úteis
        if old_d_ini:
            novo_d_fim = calculate_end_date(old_d_ini, nova_dur)
            row['DATA_FIM'] = format_date_br(novo_d_fim)

        # 4. Dimensionamento RUP de Headcount & Aceleração de Prazo (Crashing)
        vagao_prefix = vagao_nome[:2]
        base_hc = HEADCOUNT_PADRAO_VAGAO.get(vagao_prefix, 8)
        if args.novo_headcount:
            calc_hc = args.novo_headcount
            # Se forneceu novo headcount sem nova duração, calcula nova duração via RUP (Crashing):
            if args.nova_duracao is None and base_hc > 0 and old_dur > 0:
                nova_dur = max(1, math.ceil(old_dur * (base_hc / calc_hc)))
                row['RITMO_DIAS_POR_LOCAL'] = str(nova_dur)
                if old_d_ini:
                    novo_d_fim = calculate_end_date(old_d_ini, nova_dur)
                    row['DATA_FIM'] = format_date_br(novo_d_fim)
        elif nova_dur != old_dur and old_dur > 0:
            calc_hc = max(1, math.ceil(base_hc * (old_dur / nova_dur)))
        else:
            calc_hc = base_hc

        row['_calc_headcount'] = calc_hc

        print(f"\n[+] TAREFA ALTERADA [ID {t_idx + 1}]:")
        print(f"    Setor    : {pavimento}")
        print(f"    Vagão    : {vagao_nome}")
        print(f"    Duração  : {old_dur} dias -> {nova_dur} dias")
        print(f"    Datas    : {old_ini} .. {old_fim}  ===>  {row['DATA_INICIO']} .. {row['DATA_FIM']}")
        print(f"    Headcount: {base_hc} operários -> {calc_hc} operários (RUP recalculada)")

        modified_initial.append(t_idx)

    # Propagação em Cascata pelo DAG
    cascade_modified_indices = set()
    if not args.sem_cascata:
        cascade_modified_indices = propagate_forward_dag(rows, modified_initial, adj, topo_order)
        print(f"\n[+] PROPAGAÇÃO EM CASCATA TOPOLÓGICA (DAG):")
        print(f"    Total de tarefas sucessoras replanejadas automaticamente: {len(cascade_modified_indices)}")
        if cascade_modified_indices:
            print("    Exemplos de frentes movidas para preservar takt contínuo:")
            amostra = list(cascade_modified_indices)[:5]
            for idx in amostra:
                r = rows[idx]
                print(f"      - ID {idx + 1:02d}: {r.get('VAGAO')[:25]} ({r.get('LOCAL_PAVIMENTO')[:20]}) -> Início: {r.get('DATA_INICIO')}, Fim: {r.get('DATA_FIM')}")
            if len(cascade_modified_indices) > 5:
                print(f"      ... e mais {len(cascade_modified_indices) - 5} frentes subsequentes.")

    # Sincronização com Curto Prazo (Lotes Takt)
    all_modified = [rows[i] for i in set(modified_initial).union(cascade_modified_indices)]
    lotes_sync_count = 0
    if not args.sem_curto_prazo:
        lotes_sync_count, detalhes_lotes = sync_short_term_schedule(base_path, obra, all_modified, dry_run=args.dry_run)
        print(f"\n[+] SINCRONIZAÇÃO COM A ESTEIRA DE CURTO PRAZO:")
        print(f"    Total de lotes sincronizados nas planilhas semanais: {lotes_sync_count}")
        for det in detalhes_lotes[:5]:
            print(f"      • {det}")
        if len(detalhes_lotes) > 5:
            print(f"      ... e mais {len(detalhes_lotes) - 5} lotes semanais.")

    # Sincronização com Caminho Crítico (dados_cpm.json)
    cpm_sync_count, detalhes_cpm = sync_cpm_schedule(base_path, obra, all_modified, dry_run=args.dry_run)
    if cpm_sync_count > 0:
        print(f"\n[+] SINCRONIZAÇÃO COM O CAMINHO CRÍTICO (CPM / GANTT):")
        print(f"    Total de atividades CPM recalculadas: {cpm_sync_count}")
        for det in detalhes_cpm:
            print(f"      • {det}")

    # Salva no arquivo CSV da Linha de Balanço se não for dry-run
    if not args.dry_run:
        save_schedule_csv(csv_path, rows, fieldnames)
        print(f"\n[✔] Sucesso! Planilha LINHA_DE_BALANCO.csv salva com integridade absoluta.")
        print(f"    Caminho: {csv_path}")

        # Recalcula sobreposições da LOB e Heijunka automaticamente
        try:
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            sync_script = os.path.join(root_dir, 'scripts', 'sincronizar_esteira_e_lob.py')
            if os.path.exists(sync_script):
                import subprocess
                subprocess.run([sys.executable, sync_script, '--obra', obra, '--analisar-sobreposicao'], capture_output=True)
        except Exception:
            pass
    else:
        print(f"\n[i] Simulação concluída com sucesso. Nenhuma alteração foi gravada em disco.")

    # Exibe novo impacto de término global
    dates_fim = [parse_date_br(r.get('DATA_FIM')) for r in rows if parse_date_br(r.get('DATA_FIM'))]
    dates_ini = [parse_date_br(r.get('DATA_INICIO')) for r in rows if parse_date_br(r.get('DATA_INICIO'))]
    if dates_ini and dates_fim:
        print(f"    Novo Término Previsto da Obra: {format_date_br(max(dates_fim))}")
        print(f"==================================================================\n")

# =============================================================================
# CLI PARSER
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Motor Lean Determinístico de Reprogramação de Cronograma & Linha de Balanço",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de Uso:
  python scripts/reprogramar_cronograma.py --obra OBRA_TMULT --status
  python scripts/reprogramar_cronograma.py --obra OBRA_TMULT --listar
  python scripts/reprogramar_cronograma.py --obra OBRA_TMULT --tarefa-id 2 --nova-duracao 7
  python scripts/reprogramar_cronograma.py --obra OBRA_TMULT --vagao 02 --deslocar-dias 3 --aplicar-todo-vagao
  python scripts/reprogramar_cronograma.py --obra OBRA_TMULT --tarefa-id 19 --nova-duracao 5 --novo-headcount 12
        """
    )

    parser.add_argument("--obra", type=str, default="OBRA_TMULT", help="Identificador da pasta do projeto (padrão: OBRA_TMULT)")
    parser.add_argument("--status", action="store_true", help="Exibe resumo executivo atual do cronograma")
    parser.add_argument("--listar", action="store_true", help="Lista todas as tarefas com respectivos IDs")

    # Alvos
    parser.add_argument("--tarefa-id", type=int, help="Número ID da tarefa (1 a N)")
    parser.add_argument("--vagao", type=str, help="Nome ou número do vagão (ex: 02, 06)")
    parser.add_argument("--setor", type=str, help="Filtro de setor/pavimento (ex: Zona 01)")
    parser.add_argument("--aplicar-todo-vagao", action="store_true", help="Aplica a reprogramação a todas as zonas do vagão")

    # Parâmetros de Mudança
    parser.add_argument("--nova-duracao", type=int, help="Nova duração da atividade em dias úteis")
    parser.add_argument("--nova-data-inicio", type=str, help="Nova data de início (DD/MM/AAAA)")
    parser.add_argument("--deslocar-dias", type=int, help="Deslocar início em +/- N dias úteis")
    parser.add_argument("--novo-headcount", type=int, help="Forçar novo efetivo (se omitido, calcula via RUP)")
    parser.add_argument("--takt-dias", type=int, help="Configura novo ritmo / Takt Time padrão (1 a 6 dias úteis)")

    # Controle de Cascata e Sincronização
    parser.add_argument("--sem-cascata", action="store_true", help="Desativa o recalculo automático em cascata das sucessoras")
    parser.add_argument("--sem-curto-prazo", action="store_true", help="Não sincroniza planilhas de curto prazo")
    parser.add_argument("--dry-run", action="store_true", help="Apenas simula e exibe impactos sem modificar planilhas")

    args = parser.parse_args()
    reprogramar(args)

if __name__ == '__main__':
    main()
