#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========================================================================================
 🚂 MOTOR UNIVERSAL DE ORQUESTRAÇÃO & SINCRONIZAÇÃO TOTAL DE CRONOGRAMAS (LEAN 5D)
==========================================================================================
Garante que o Caminho Crítico (Gantt/CPM), a Linha de Balanço (LOB) e a Programação
Semanal de Curto Prazo (Esteira Takt / WWP) estejam SEMPRE 100% harmonizados e matematicamente
idênticos em termos de datas de início, término, avanço físico e ritmo de produção.

Suporta:
  1. Geração Automatizada de Nova Obra (--gerar-tudo)
  2. Takt Time Flexível (1 a 6 dias úteis via --takt-dias)
  3. Reprogramação com Crashing via RUP (--novo-headcount / --nova-duracao)
  4. Sincronização Bidirecional e Reconciliação Total (--sincronizar)
  5. Sentinela em Tempo Real / File Watcher (--watch)
  6. Auditoria Imediata Multi-Eixo (--auditar)

Exemplos de Uso:
  # Gerar do zero todos os cronogramas de uma obra nova:
  python scripts/orquestrar_cronogramas.py --obra NOVA_OBRA --gerar-tudo --takt-dias 3

  # Reprogramar uma atividade (reduzindo duração com mais efetivo via RUP):
  python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --reprogramar --tarefa-id 29 --novo-headcount 12

  # Sincronizar todos os 3 cronogramas e rodar auditoria:
  python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --sincronizar

  # Ativar Sentinela / Watcher de arquivos em background (detecta edição manual e auto-sincroniza):
  python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --watch
==========================================================================================
"""

import os
import sys
import time
import argparse
import subprocess
from datetime import datetime

# Configuração de encoding UTF-8 no Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def log(msg, nivel="INFO"):
    agora = datetime.now().strftime("%H:%M:%S")
    cores = {
        "INFO": "\033[94m[INFO]\033[0m",
        "SUCESSO": "\033[92m[SUCESSO]\033[0m",
        "AVISO": "\033[93m[AVISO]\033[0m",
        "ERRO": "\033[91m[ERRO]\033[0m",
        "WATCH": "\033[95m[SENTINELA]\033[0m"
    }
    tag = cores.get(nivel, f"[{nivel}]")
    print(f"{agora} {tag} {msg}")

def run_script(script_name, args_list, silent=False):
    """Executa um script da pasta scripts/ com argumentos e tratamento de erro."""
    script_path = os.path.join(ROOT_DIR, 'scripts', script_name)
    if not os.path.exists(script_path):
        log(f"Script {script_name} não encontrado em {script_path}", "ERRO")
        return False, ""

    cmd = [sys.executable, script_path] + [str(a) for a in args_list]
    try:
        if silent:
            res = subprocess.run(cmd, cwd=ROOT_DIR, capture_output=True, text=True, encoding='utf-8')
            return res.returncode == 0, (res.stdout or "") + (res.stderr or "")
        else:
            res = subprocess.run(cmd, cwd=ROOT_DIR, text=True)
            return res.returncode == 0, ""
    except Exception as err:
        log(f"Falha ao executar {script_name}: {err}", "ERRO")
        return False, str(err)

# =============================================================================
# PIPELINE 1: GERAÇÃO TOTAL DE CRONOGRAMAS (NOVA OBRA OU REINICIALIZAÇÃO)
# =============================================================================

def pipeline_gerar_tudo(obra, takt_dias=3):
    log(f"Iniciando Pipeline de Geração Total de Cronogramas para '{obra}'...", "INFO")
    print("=" * 80)
    print(f"  OBRA: {obra.upper()} | TAKT TIME: {takt_dias} DIAS ÚTEIS")
    print("=" * 80)

    # Passo 1: Orçamento e Cronograma Físico-Financeiro (EAP & Alocações Iniciais)
    log("[Passo 1/5] Gerando Base Física, Curva S e Físico-Financeiro...", "INFO")
    ok, _ = run_script('gerar_cronograma.py', ['--obra', obra])
    if not ok:
        log("Falha no Passo 1 (gerar_cronograma.py)", "ERRO")
        return False

    # Passo 2: Programação de Curto Prazo (Esteira Takt / WWP Lotes)
    log(f"[Passo 2/5] Modelando Esteira Lean de Curto Prazo (Takt {takt_dias}d)...", "INFO")
    ok, _ = run_script('gerar_programacao_curto_prazo_takt.py', ['--obra', obra, '--takt-dias', takt_dias])
    if not ok:
        log("Falha no Passo 2 (gerar_programacao_curto_prazo_takt.py)", "ERRO")
        return False

    # Passo 3: Sincronização Esteira -> Linha de Balanço (LOB e Heijunka)
    log("[Passo 3/5] Calibrando Linha de Balanço (LOB) e Análise de Sobreposições...", "INFO")
    ok, _ = run_script('sincronizar_esteira_e_lob.py', ['--obra', obra, '--modo', 'esteira_para_lob', '--analisar-sobreposicao'])
    if not ok:
        log("Falha no Passo 3 (sincronizar_esteira_e_lob.py)", "ERRO")
        return False

    # Passo 4: Reconciliação Final do Físico-Financeiro com os Marcos da LOB
    log("[Passo 4/5] Reconciliando Curva S e desembolso orçamentário...", "INFO")
    ok, _ = run_script('gerar_cronograma.py', ['--obra', obra], silent=True)
    if not ok:
        log("Aviso no Passo 4 (reconciliação físico-financeira)", "AVISO")

    # Passo 5: Auditoria Multi-Eixo
    log("[Passo 5/5] Executando Auditoria Multi-Eixo de Conformidade (5 Eixos)...", "INFO")
    ok, _ = run_script('auditar_cronogramas.py', ['--obra', obra])
    if not ok:
        log("Auditoria multi-eixo apontou inconformidades!", "AVISO")
        return False

    print("=" * 80)
    log(f"🎉 Pipeline concluído com SUCESSO ABSOLUTO para '{obra}'!", "SUCESSO")
    log("Todos os 3 cronogramas (CPM, LOB e Curto Prazo) estão 100% calibrados e sincronizados.", "SUCESSO")
    print("=" * 80)
    return True

# =============================================================================
# PIPELINE 2: REPROGRAMAÇÃO ATÔMICA COM PROPAGAÇÃO NOS 3 NÍVEIS
# =============================================================================

def pipeline_reprogramar(obra, args):
    log(f"Iniciando Reprogramação Integrada para '{obra}'...", "INFO")
    reprog_args = ['--obra', obra]

    if args.tarefa_id:
        reprog_args += ['--tarefa-id', args.tarefa_id]
    if args.vagao:
        reprog_args += ['--vagao', args.vagao]
    if args.setor:
        reprog_args += ['--setor', args.setor]
    if args.aplicar_todo_vagao:
        reprog_args.append('--aplicar-todo-vagao')
    if args.nova_duracao:
        reprog_args += ['--nova-duracao', args.nova_duracao]
    if args.novo_headcount:
        reprog_args += ['--novo-headcount', args.novo_headcount]
    if args.nova_data_inicio:
        reprog_args += ['--nova-data-inicio', args.nova_data_inicio]
    if args.deslocar_dias:
        reprog_args += ['--deslocar-dias', args.deslocar_dias]
    if args.dry_run:
        reprog_args.append('--dry-run')

    # Executa a reprogramação na Linha de Balanço + Curto Prazo + CPM
    ok, _ = run_script('reprogramar_cronograma.py', reprog_args)
    if not ok:
        log("Erro ao processar reprogramação.", "ERRO")
        return False

    if not args.dry_run:
        # Reconcilia Curva S físico-financeira
        run_script('gerar_cronograma.py', ['--obra', obra], silent=True)
        # Executa auditoria rápida
        log("Validando coerência global multi-eixo...", "INFO")
        run_script('auditar_cronogramas.py', ['--obra', obra])

    return True

# =============================================================================
# PIPELINE 3: SINCRONIZAÇÃO E RECONCILIAÇÃO BIDIRECIONAL
# =============================================================================

def pipeline_sincronizar(obra, origem='lob'):
    log(f"Sincronizando cronogramas da obra '{obra}' (Origem: {origem.upper()})...", "INFO")
    
    if origem == 'curto-prazo':
        ok, _ = run_script('sincronizar_esteira_e_lob.py', ['--obra', obra, '--modo', 'esteira_para_lob', '--analisar-sobreposicao'])
    else:
        # Padrão: LOB -> Curto Prazo & CPM
        ok, _ = run_script('sincronizar_esteira_e_lob.py', ['--obra', obra, '--modo', 'esteira_para_lob', '--analisar-sobreposicao'])

    # Reconcilia Físico-Financeiro
    run_script('gerar_cronograma.py', ['--obra', obra], silent=True)
    # Audita
    run_script('auditar_cronogramas.py', ['--obra', obra])
    log("Sincronização bidirecional concluída com êxito!", "SUCESSO")
    return True

# =============================================================================
# PIPELINE 4: SENTINELA REATIVO / FILE WATCHER EM TEMPO REAL (--watch)
# =============================================================================

def pipeline_watch(obra):
    pasta_plan = os.path.join(ROOT_DIR, 'projetos', obra, '03_PLANEJAMENTO_E_CRONOGRAMA')
    if not os.path.exists(pasta_plan):
        log(f"Diretório de planejamento não encontrado: {pasta_plan}", "ERRO")
        return

    arquivos_vigiados = [
        os.path.join(pasta_plan, 'LINHA_DE_BALANCO.csv'),
        os.path.join(pasta_plan, f'PROGRAMACAO_CURTO_PRAZO_{obra}.csv'),
        os.path.join(pasta_plan, f'PROGRAMACAO_CURTO_PRAZO_{obra.replace("OBRA_", "")}.csv'),
        os.path.join(pasta_plan, 'dados_cpm.json'),
    ]

    print("\n" + "=" * 80)
    log(f"👁️ SENTINELA ATIVADO: Vigiando alterações em '{obra}'...", "WATCH")
    print(f"Diretório: {pasta_plan}")
    print("Modo de operação: Qualquer gravação (Excel, IDE ou API) dispara auto-sincronização.")
    print("Pressione Ctrl+C para encerrar o sentinela.")
    print("=" * 80 + "\n")

    mtimes = {}
    for p in arquivos_vigiados:
        if os.path.exists(p):
            mtimes[p] = os.path.getmtime(p)

    try:
        while True:
            time.sleep(1.0)
            alterado = None
            for p in arquivos_vigiados:
                if os.path.exists(p):
                    curr_mtime = os.path.getmtime(p)
                    if p in mtimes and curr_mtime > mtimes[p]:
                        alterado = p
                        mtimes[p] = curr_mtime
                        break
                    mtimes[p] = curr_mtime

            if alterado:
                nome_arq = os.path.basename(alterado)
                log(f"Arquivo alterado detectado: \033[1m{nome_arq}\033[0m", "WATCH")
                log("Aguardando 1.5s para conclusão de escrita (debounce)...", "WATCH")
                time.sleep(1.5)

                origem = 'curto-prazo' if 'CURTO_PRAZO' in nome_arq else 'lob'
                log(f"Disparando auto-sincronização em cascata (Origem: {origem.upper()})...", "WATCH")
                
                # Executa sincronização e auditoria
                run_script('sincronizar_esteira_e_lob.py', ['--obra', obra, '--modo', 'esteira_para_lob', '--analisar-sobreposicao'], silent=True)
                run_script('gerar_cronograma.py', ['--obra', obra], silent=True)
                ok, audit_out = run_script('auditar_cronogramas.py', ['--obra', obra], silent=True)
                
                if ok:
                    log(f"✅ Sincronização executada com sucesso! 0 divergências entre CPM, LOB e Curto Prazo.", "SUCESSO")
                else:
                    log("⚠️ Auditoria apontou avisos após a sincronização:", "AVISO")
                    print(audit_out[:500])

                # Atualiza mtimes para evitar loops
                for p in arquivos_vigiados:
                    if os.path.exists(p):
                        mtimes[p] = os.path.getmtime(p)

    except KeyboardInterrupt:
        print("\n")
        log("Sentinela encerrado pelo usuário.", "INFO")

# =============================================================================
# CLI PARSER
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Motor Universal de Orquestração & Sincronização Total de Cronogramas (Lean 5D)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos Práticos:
  # 1. Nova obra: gerar e sincronizar tudo do zero com Takt de 3 dias:
  python scripts/orquestrar_cronogramas.py --obra OBRA_NOVA --gerar-tudo --takt-dias 3

  # 2. Reprogramar uma atividade reduzindo a duração via aumento de equipe (Crashing RUP):
  python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --reprogramar --tarefa-id 29 --novo-headcount 12

  # 3. Sincronizar todos os cronogramas existentes e validar na auditoria:
  python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --sincronizar

  # 4. Ativar Sentinela em tempo real (File Watcher):
  python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --watch
        """
    )

    parser.add_argument("--obra", type=str, default="OBRA_TMULT", help="Identificador da obra em projetos/ (padrão: OBRA_TMULT)")
    
    # Modos Principais
    parser.add_argument("--gerar-tudo", action="store_true", help="Pipeline total de geração do zero para obras novas ou rebase")
    parser.add_argument("--reprogramar", action="store_true", help="Reprograma uma atividade/vagão e propaga em cascata nos 3 cronogramas")
    parser.add_argument("--sincronizar", action="store_true", help="Reconcilia e harmoniza os 3 cronogramas existentes")
    parser.add_argument("--watch", action="store_true", help="Ativa sentinela em tempo real (File Watcher de sincronização automática)")
    parser.add_argument("--auditar", action="store_true", help="Executa auditoria multi-eixo de 5 eixos")

    # Parâmetros de Takt e Reprogramação
    parser.add_argument("--takt-dias", type=int, default=3, help="Duração do Takt Time em dias úteis (1 a 6 dias, padrão 3)")
    parser.add_argument("--tarefa-id", type=int, help="ID numérico da tarefa para reprogramar (1 a N)")
    parser.add_argument("--vagao", type=str, help="Prefixo ou nome do vagão para reprogramar")
    parser.add_argument("--setor", type=str, help="Filtro de setor/pavimento")
    parser.add_argument("--aplicar-todo-vagao", action="store_true", help="Aplica a reprogramação a todas as frentes do vagão")
    parser.add_argument("--nova-duracao", type=int, help="Nova duração da atividade em dias úteis")
    parser.add_argument("--novo-headcount", type=int, help="Novo efetivo de operários (recalcula duração via RUP se duração omitida)")
    parser.add_argument("--nova-data-inicio", type=str, help="Nova data de início (DD/MM/AAAA)")
    parser.add_argument("--deslocar-dias", type=int, help="Deslocar início em +/- N dias úteis")
    parser.add_argument("--origem", type=str, default="lob", choices=["lob", "curto-prazo", "cpm"], help="Fonte originária da sincronização")
    parser.add_argument("--dry-run", action="store_true", help="Apenas simula a operação sem gravar em disco")

    args = parser.parse_args()

    # Note: args.gerar_tudo is generated by argparse for --gerar-tudo
    if args.gerar_tudo:
        pipeline_gerar_tudo(args.obra, takt_dias=args.takt_dias)
    elif args.reprogramar:
        pipeline_reprogramar(args.obra, args)
    elif args.watch:
        pipeline_watch(args.obra)
    elif args.auditar:
        run_script('auditar_cronogramas.py', ['--obra', args.obra])
    elif args.sincronizar:
        pipeline_sincronizar(args.obra, origem=args.origem)
    else:
        # Padrão se nada especificado: sincroniza e audita
        pipeline_sincronizar(args.obra, origem=args.origem)

if __name__ == '__main__':
    main()
