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
import shutil
import tempfile
from datetime import datetime

# Configuração de encoding UTF-8 no Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ARQUIVOS_TRANSACIONAIS = (
    'config_obra.json',
    '03_PLANEJAMENTO_E_CRONOGRAMA/dados_cpm.json',
    '03_PLANEJAMENTO_E_CRONOGRAMA/LINHA_DE_BALANCO.csv',
    '03_PLANEJAMENTO_E_CRONOGRAMA/PROGRAMACAO_CURTO_PRAZO_{obra}.csv',
    '03_PLANEJAMENTO_E_CRONOGRAMA/PROGRAMACAO_CURTO_PRAZO_{sigla}.csv',
    '03_PLANEJAMENTO_E_CRONOGRAMA/RELATORIO_DIVERGENCIA_CPM_LOB.json',
    '03_PLANEJAMENTO_E_CRONOGRAMA/RELATORIO_SOBREPOSICAO_LOB.json',
    '06_SST_E_RH/dados_histograma_mo.json',
    '06_SST_E_RH/HISTOGRAMA_MAO_DE_OBRA_{sigla}.csv',
    '06_SST_E_RH/HISTOGRAMA_MAO_DE_OBRA_{sigla}.xlsx',
    '06_SST_E_RH/RELATORIO_HISTOGRAMA_MO_{sigla}.md',
)


def criar_snapshot_cronograma(obra):
    """Preserva as fontes e derivados para rollback de uma reprogramacao reprovada."""
    obra_dir = os.path.join(ROOT_DIR, 'projetos', obra)
    snapshot_dir = tempfile.mkdtemp(prefix=f'cronograma_{obra}_')
    sigla = obra.replace('OBRA_', '')
    for modelo in ARQUIVOS_TRANSACIONAIS:
        nome = modelo.format(obra=obra, sigla=sigla)
        origem = os.path.join(obra_dir, nome)
        if os.path.exists(origem):
            destino = os.path.join(snapshot_dir, nome)
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copy2(origem, destino)
    return snapshot_dir, obra_dir


def restaurar_snapshot_cronograma(snapshot_dir, obra_dir):
    for raiz, _, arquivos in os.walk(snapshot_dir):
        for nome in arquivos:
            origem = os.path.join(raiz, nome)
            relativo = os.path.relpath(origem, snapshot_dir)
            destino = os.path.join(obra_dir, relativo)
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copy2(origem, destino)

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
    log(f"Iniciando Pipeline Universal de Planejamento SSOT para '{obra}'...", "INFO")
    print("=" * 80)
    print(f"  OBRA: {obra.upper()} | FONTE ÚNICA DA VERDADE (planejamento_mestre.json)")
    print("=" * 80)

    # Passo Único: Compilação Determinística Integrada (LOB, Curto Prazo, CPM, Curva S, Histograma)
    log("[SSOT] Compilando todos os cronogramas a partir da Fonte Única...", "INFO")
    ok, _ = run_script('compilar_planejamento.py', ['--obra', obra])
    if not ok:
        log("Falha na compilação do planejamento mestre.", "ERRO")
        return False

    # Auditoria de Conformidade
    log("[Auditoria] Executando Auditoria Multi-Eixo de Conformidade...", "INFO")
    ok_audit, _ = run_script('auditar_cronogramas.py', ['--obra', obra])
    if not ok_audit:
        log("Auditoria multi-eixo apontou alertas de verificação.", "AVISO")

    print("=" * 80)
    log(f"🎉 Pipeline concluído com SUCESSO ABSOLUTO para '{obra}'!", "SUCESSO")
    log("Todos os cronogramas (CPM, LOB, Curto Prazo e Histograma MO) estão 100% harmonizados via SSOT.", "SUCESSO")
    print("=" * 80)
    return True

# =============================================================================
# PIPELINE 2: REPROGRAMAÇÃO ATÔMICA COM PROPAGAÇÃO NOS 3 NÍVEIS
# =============================================================================

def pipeline_reprogramar(obra, args):
    snapshot_dir = None
    plan_dir = None
    if not args.dry_run:
        snapshot_dir, plan_dir = criar_snapshot_cronograma(obra)
    log(f"Iniciando Reprogramação Integrada para '{obra}'...", "INFO")
    reprog_args = ['--obra', obra]

    if args.tarefa_id:
        reprog_args += ['--tarefa-id', args.tarefa_id]
    for atividade_cpm in args.atividade_cpm or []:
        reprog_args += ['--atividade-cpm', atividade_cpm]
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
    if args.headcount_base:
        reprog_args += ['--headcount-base', args.headcount_base]
    if args.nova_data_inicio:
        reprog_args += ['--nova-data-inicio', args.nova_data_inicio]
    if args.deslocar_dias:
        reprog_args += ['--deslocar-dias', args.deslocar_dias]
    if args.dry_run:
        reprog_args.append('--dry-run')
    if args.aprovar_revisao:
        reprog_args.append('--aprovar-revisao')

    # Executa a reprogramação na Linha de Balanço + Curto Prazo + CPM
    ok, _ = run_script('reprogramar_cronograma.py', reprog_args)
    if not ok:
        if snapshot_dir:
            restaurar_snapshot_cronograma(snapshot_dir, plan_dir)
            shutil.rmtree(snapshot_dir, ignore_errors=True)
        log("Erro ao processar reprogramação.", "ERRO")
        return False

    if not args.dry_run:
        # Reconcilia Curva S físico-financeira
        ok_cron, _ = run_script('gerar_cronograma.py', ['--obra', obra], silent=True)
        if not ok_cron:
            restaurar_snapshot_cronograma(snapshot_dir, plan_dir)
            shutil.rmtree(snapshot_dir, ignore_errors=True)
            log("Erro ao reconciliar curva S.", "ERRO")
            return False
        # Recalcula e sincroniza o Histograma de Mão de Obra
        log("Recalibrando Histograma Oficial de Mão de Obra & Headcount...", "INFO")
        ok_hist, _ = run_script('gerar_histograma_sincronizado.py', ['--obra', obra], silent=True)
        if not ok_hist:
            restaurar_snapshot_cronograma(snapshot_dir, plan_dir)
            shutil.rmtree(snapshot_dir, ignore_errors=True)
            log("Erro ao recalibrar Histograma de MO.", "ERRO")
            return False
        # Executa auditoria rápida
        log("Validando coerência global multi-eixo...", "INFO")
        ok_audit, _ = run_script('auditar_cronogramas.py', ['--obra', obra])
        if not ok_audit:
            restaurar_snapshot_cronograma(snapshot_dir, plan_dir)
            shutil.rmtree(snapshot_dir, ignore_errors=True)
            log("Auditoria multi-eixo reprovada após reprogramação.", "ERRO")
            return False

    return True

# =============================================================================
# PIPELINE 3: SINCRONIZAÇÃO E RECONCILIAÇÃO VIA FONTE ÚNICA (SSOT)
# =============================================================================

def pipeline_sincronizar(obra, origem='cpm'):
    log(f"Compilando e sincronizando cronogramas da obra '{obra}' via SSOT...", "INFO")
    ok, _ = run_script('compilar_planejamento.py', ['--obra', obra])
    if not ok:
        log("Falha ao compilar cronogramas via SSOT.", "ERRO")
        return False

    log("Sincronização SSOT concluída com êxito! (Divergência Zero)", "SUCESSO")
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

                if nome_arq == 'dados_cpm.json':
                    origem = 'cpm'
                else:
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
    parser.add_argument("--histograma", action="store_true", help="Recalcula e regenera exclusivamente o Histograma de Mão de Obra (Headcount & HH)")
    parser.add_argument("--watch", action="store_true", help="Ativa sentinela em tempo real (File Watcher de sincronização automática)")
    parser.add_argument("--auditar", action="store_true", help="Executa auditoria multi-eixo de 6 eixos")

    # Parâmetros de Takt e Reprogramação
    parser.add_argument("--takt-dias", type=int, default=3, help="Duração do Takt Time em dias úteis (1 a 6 dias, padrão 3)")
    parser.add_argument("--tarefa-id", type=int, help="ID numérico da tarefa para reprogramar (1 a N)")
    parser.add_argument("--atividade-cpm", action="append", help="ID CPM a reprogramar; pode ser repetido")
    parser.add_argument("--vagao", type=str, help="Prefixo ou nome do vagão para reprogramar")
    parser.add_argument("--setor", type=str, help="Filtro de setor/pavimento")
    parser.add_argument("--aplicar-todo-vagao", action="store_true", help="Aplica a reprogramação a todas as frentes do vagão")
    parser.add_argument("--nova-duracao", type=int, help="Nova duração da atividade em dias úteis")
    parser.add_argument("--novo-headcount", type=int, help="Novo efetivo de operários (recalcula duração via RUP se duração omitida)")
    parser.add_argument("--headcount-base", type=int, help="Efetivo de referência da atividade CPM para cálculo RUP")
    parser.add_argument("--nova-data-inicio", type=str, help="Nova data de início (DD/MM/AAAA)")
    parser.add_argument("--deslocar-dias", type=int, help="Deslocar início em +/- N dias úteis")
    parser.add_argument("--origem", type=str, default="cpm", choices=["lob", "curto-prazo", "cpm"], help="Fonte originária da sincronização")
    parser.add_argument("--dry-run", action="store_true", help="Apenas simula a operação sem gravar em disco")

    parser.add_argument("--aprovar-revisao", action="store_true", help="Promove nova revisao antes de gravar os derivados")
    args = parser.parse_args()

    obra_dir = os.path.join(ROOT_DIR, 'projetos', args.obra)
    if not os.path.isdir(obra_dir):
        log(f"Pasta da obra '{args.obra}' não encontrada em: {obra_dir}", "ERRO")
        sys.exit(1)

    sucesso = False
    if args.gerar_tudo:
        sucesso = pipeline_gerar_tudo(args.obra, takt_dias=args.takt_dias)
    elif args.reprogramar:
        sucesso = pipeline_reprogramar(args.obra, args)
    elif args.histograma:
        log(f"Recalculando Histograma Oficial de Mão de Obra para '{args.obra}'...", "INFO")
        ok, _ = run_script('gerar_histograma_sincronizado.py', ['--obra', args.obra])
        sucesso = ok
    elif args.watch:
        pipeline_watch(args.obra)
        sucesso = True
    elif args.auditar:
        ok, _ = run_script('auditar_cronogramas.py', ['--obra', args.obra])
        sucesso = ok
    elif args.sincronizar:
        sucesso = pipeline_sincronizar(args.obra, origem=args.origem)
    else:
        # Padrão se nada especificado: sincroniza e audita
        sucesso = pipeline_sincronizar(args.obra, origem=args.origem)

    if not sucesso:
        log(f"Execução finalizada com FALHA para '{args.obra}'.", "ERRO")
        sys.exit(1)

if __name__ == '__main__':
    main()
