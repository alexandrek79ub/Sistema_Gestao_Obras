#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Gestão do Pipeline de Suprimentos & Tracker de Requisições de Compra Multi-Obra
Ecossistema de Gestão de Obras & PMO Virtual

Gera e atualiza:
1. TRACKER_SUPRIMENTOS_RC_[SIGLA].csv / TRACKER_SUPRIMENTOS_MESTRE_COMPLETO_[SIGLA].csv
2. TRACKER_SUPRIMENTOS_RC_[SIGLA].md (Painel executivo com Kanban e Semáforos)
3. TEMPLATE_REQUISICAO_DE_COMPRA_RC.md
4. TEMPLATE_PEDIDO_DE_COMPRA_PC.md

Pipeline Padronizado de 7 Estágios:
1. PENDENTE_SUPRIMENTOS
2. EM_COTACAO
3. COTACOES_RECEBIDAS
4. MAPA_EQUALIZADO
5. EM_APROVACAO_DIRETORIA
6. PEDIDO_EMITIDO_PC
7. ENTREGUE_EM_OBRA

Uso:
    python scripts/gerar_tracker_suprimentos.py --obra OBRA_TMULT
    python scripts/gerar_tracker_suprimentos.py --obra RESIDENCIAL_ALPHA
"""

import os
import sys
import csv
import json
import argparse
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def gerar_tracker(obra_nome=None, custom_dir=None):
    base_repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if custom_dir:
        proj_dir = os.path.abspath(custom_dir)
        obra_id = os.path.basename(proj_dir)
    elif obra_nome:
        proj_dir = os.path.join(base_repo_dir, "projetos", obra_nome)
        obra_id = obra_nome
    else:
        raise ValueError("É necessário especificar --obra [NOME_OBRA] ou --dir [CAMINHO].")

    if not os.path.exists(proj_dir):
        raise FileNotFoundError(f"Diretório da obra não encontrado: {proj_dir}")

    # 1. Carregar configuração da obra
    config_path = os.path.join(proj_dir, "config_obra.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {}

    nome_obra = config.get("nome_obra", obra_id)
    sigla_obra = config.get("sigla_obra", obra_id)
    area_m2 = config.get("area_construida_m2", "N/A")

    sup_dir = os.path.join(proj_dir, "05_SUPRIMENTOS_E_FINANCEIRO")
    os.makedirs(sup_dir, exist_ok=True)

    # 2. Carregar dados do tracker
    tracker_file = os.path.join(sup_dir, "dados_tracker_suprimentos.json")
    if not os.path.exists(tracker_file):
        tpl_file = os.path.join(base_repo_dir, "projetos", "OBRA", "05_SUPRIMENTOS_E_FINANCEIRO", "dados_tracker_suprimentos.template.json")
        if os.path.exists(tpl_file):
            with open(tpl_file, "r", encoding="utf-8") as f:
                tracker_data = json.load(f)
        else:
            tracker_data = []
    else:
        with open(tracker_file, "r", encoding="utf-8") as f:
            tracker_data = json.load(f)

    if not tracker_data:
        print(f"[AVISO] Nenhum item no tracker para {obra_id}.")

    # 3. Gerar CSV do Tracker
    csv_name = f"TRACKER_SUPRIMENTOS_MESTRE_COMPLETO_{sigla_obra}.csv"
    csv_path = os.path.join(sup_dir, csv_name)

    headers = [
        "ID_Requisicao", "Tipo_Suprimento", "Pacote_Insumo_Equipamento", "Centro_Custo_CC",
        "Disciplina", "EAP_Itens", "Data_Disparo", "Data_Canteiro", "Lead_Time_Dias",
        "Estagio_Pipeline", "Responsavel", "Semaforo", "Budget_R$"
    ]

    with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(headers)
        for r in tracker_data:
            # Compatibilidade com formatos com campos ligeiramente diferentes
            id_req = r.get("ID_Requisicao", r.get("id_rc", ""))
            tipo = r.get("Tipo_Suprimento", "MATERIAL")
            pacote = r.get("Pacote_Insumo_Equipamento", r.get("pacote", ""))
            cc = r.get("Centro_Custo_CC", r.get("centro_custo", ""))
            disc = r.get("Disciplina", r.get("disciplina", ""))
            eap = r.get("EAP_Itens", r.get("eap_itens", ""))
            disparo = r.get("Data_Disparo", r.get("data_emissao", ""))
            canteiro = r.get("Data_Canteiro", r.get("data_necessidade", ""))
            lead = r.get("Lead_Time_Dias", r.get("lead_time_dias", 15))
            estagio = r.get("Estagio_Pipeline", r.get("estagio_pipeline", "1. PENDENTE_SUPRIMENTOS"))
            resp = r.get("Responsavel", r.get("responsavel_atual", "Suprimentos"))
            semaforo = r.get("Semaforo", r.get("semaforo", "🟢 NO PRAZO"))
            budget = r.get("Budget_R$", r.get("orcamento_base_cd", 0.0))

            writer.writerow([id_req, tipo, pacote, cc, disc, eap, disparo, canteiro, lead, estagio, resp, semaforo, budget])

    print(f"✅ CSV Tracker gerado: {csv_path} ({len(tracker_data)} itens)")

    # Também gera cópia retrocompatível TRACKER_SUPRIMENTOS_RC_TMULT.csv se for TMULT
    if sigla_obra == "TMULT":
        legacy_csv = os.path.join(sup_dir, "TRACKER_SUPRIMENTOS_RC_TMULT.csv")
        with open(legacy_csv, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([
                "ID_RC", "Pacote_Insumo", "Centro_Custo_CC", "Disciplina", "EAP_Itens",
                "Data_Emissao_Obra", "Data_Necessidade_Canteiro", "Lead_Time_Dias",
                "Estagio_Pipeline", "Responsavel_Atual", "Proxima_Acao_Gargalo",
                "Semaforo_Risco", "Budget_Custo_Direto_R$", "Fornecedor_PreQualificado",
                "Numero_PC", "Condicao_Pagamento_Alvo"
            ])
            for r in tracker_data[:4]:
                writer.writerow([
                    r.get("ID_Requisicao", r.get("id_rc", "")),
                    r.get("Pacote_Insumo_Equipamento", r.get("pacote", "")),
                    r.get("Centro_Custo_CC", r.get("centro_custo", "")),
                    r.get("Disciplina", r.get("disciplina", "")),
                    r.get("EAP_Itens", r.get("eap_itens", "")),
                    r.get("Data_Disparo", r.get("data_emissao", "")),
                    r.get("Data_Canteiro", r.get("data_necessidade", "")),
                    r.get("Lead_Time_Dias", r.get("lead_time_dias", 15)),
                    r.get("Estagio_Pipeline", r.get("estagio_pipeline", "1. PENDENTE_SUPRIMENTOS")),
                    r.get("Responsavel", r.get("responsavel_atual", "Suprimentos")),
                    r.get("Proxima_Acao_Gargalo", r.get("proxima_acao", "Acompanhar cotações")),
                    r.get("Semaforo", r.get("semaforo", "🟢 NO PRAZO")),
                    r.get("Budget_R$", r.get("orcamento_base_cd", 0.0)),
                    r.get("fornecedor_homologado", "Pré-qualificado"),
                    r.get("num_pc", "Pendente Abertura"),
                    r.get("cond_pagamento_alvo", "30 DDL")
                ])

    # 4. Gerar Painel Markdown com Kanban
    md_name = f"TRACKER_SUPRIMENTOS_RC_{sigla_obra}.md"
    md_path = os.path.join(sup_dir, md_name)

    linhas = [
        f"# 📊 PAINEL DE RASTREABILIDADE DE SUPRIMENTOS & TRACKER DE RCs",
        "",
        f"**Empreendimento:** {nome_obra} ({area_m2} m²)",
        "**Módulo de Gestão:** Suprimentos & Governança de Compras (Pipeline Ágil)",
        "**Público-Alvo:** Diretoria, Gestor de Contratos, Engenheiro Residente e Setor de Compras",
        f"**Data da Última Atualização:** {datetime.now().strftime('%d/%m/%Y')}",
        "",
        "---",
        "",
        "## 🧭 1. O Funil Operacional de Suprimentos (7 Estágios Padronizados)",
        "",
        "| Estágio do Funil | O que Significa na Prática? | Quem é o 'Dono da Bola'? | Documento Formal |",
        "| :---: | :--- | :---: | :---: |",
        "| `1. PENDENTE_SUPRIMENTOS` | Obra emitiu a RC técnica com UCC, EAP e data limite no canteiro. | **Comprador** | Requisição de Compra (RC) |",
        "| `2. EM_COTAÇÃO` | Comprador disparou a RC para 3 fornecedores e aguarda propostas. | **Fornecedores** | Pedido de Cotação |",
        "| `3. COTAÇÕES_RECEBIDAS` | Fornecedores responderam; propostas comerciais sob análise. | **Comprador** | Propostas Comerciais |",
        "| `4. MAPA_EQUALIZADO` | Comprador montou o comparativo de preços, frete e saving vs SINAPI. | **Comprador** | Mapa de Cotação |",
        "| `5. EM_APROVAÇÃO_DIRETORIA` | Mapa submetido ao Diretor/Gestor para aprovação formal (Skill 03). | **Diretoria** | Despacho de Aprovação |",
        "| `6. PEDIDO_EMITIDO_PC` | Fornecedor vencedor contratado e Pedido de Compra formal despachado. | **Suprimentos / Fornecedor** | Pedido de Compra (PC) |",
        "| `7. ENTREGUE_EM_OBRA` | Material descarregado e aprovado pela Engenharia (NF x PC x FVS). | **Engenharia / Almoxarife** | FVS e Canhoto da NF |",
        "",
        "---",
        "",
        f"## 📋 2. Matriz Viva de Rastreabilidade ({len(tracker_data)} Pacotes)",
        "",
        "| Nº RC/RE | Pacote | Centro de Custo | Data Disparo | Data Canteiro | Estágio Funil | Responsável | Semáforo |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]

    for r in tracker_data:
        id_req = r.get("ID_Requisicao", r.get("id_rc", ""))
        pacote = r.get("Pacote_Insumo_Equipamento", r.get("pacote", ""))
        cc = r.get("Centro_Custo_CC", r.get("centro_custo", ""))
        disparo = r.get("Data_Disparo", r.get("data_emissao", ""))
        canteiro = r.get("Data_Canteiro", r.get("data_necessidade", ""))
        estagio = r.get("Estagio_Pipeline", r.get("estagio_pipeline", ""))
        resp = r.get("Responsavel", r.get("responsavel_atual", ""))
        semaforo = r.get("Semaforo", r.get("semaforo", ""))

        linhas.append(f"| **{id_req}** | {pacote} | `{cc}` | {disparo} | **{canteiro}** | `{estagio}` | **{resp}** | {semaforo} |")

    linhas.extend([
        "",
        "---",
        "",
        "## 📌 3. Quadro Visual Kanban de Suprimentos",
        "",
        "```",
        "┌───────────────────────────┬───────────────────────────┬───────────────────────────┐",
        "│ [1] PENDENTE SUPRIMENTOS  │ [2 e 3] COTAÇÃO & PROPOSTA│ [4 e 5] MAPA & APROVAÇÃO  │",
        "├───────────────────────────┼───────────────────────────┼───────────────────────────┤",
        "│ • Pacotes em abertura     │ • Em cotação com mercado  │ • Equalização e alçadas   │",
        "└───────────────────────────┴───────────────────────────┴───────────────────────────┘",
        "┌───────────────────────────┬───────────────────────────┐",
        "│ [6] PEDIDO EMITIDO (PC)   │ [7] ENTREGUE NA OBRA (FVS)│",
        "├───────────────────────────┼───────────────────────────┤",
        "│ • Aguardando entrega      │ • Baixa por NF e FVS      │",
        "└───────────────────────────┴───────────────────────────┘",
        "```",
        "",
        "---",
        "",
        "*Painel de Governança mantido automaticamente pelo PMO Virtual.*"
    ])

    with open(md_path, mode="w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"✅ Painel Tracker MD gerado: {md_path}")

    # 5. Gerar templates minuta RC e PC se não existirem
    rc_tpl = os.path.join(sup_dir, "TEMPLATE_REQUISICAO_DE_COMPRA_RC.md")
    if not os.path.exists(rc_tpl):
        with open(rc_tpl, "w", encoding="utf-8") as f:
            f.write(f"# 📋 MODELO PADRÃO: REQUISIÇÃO DE COMPRA (RC)\n\n**Empreendimento:** {nome_obra}\n\n| Campo | Preenchimento Obrigatório |\n|---|---|\n| **Número da RC:** | `RC-___ / 2026` |\n| **Data de Emissão:** | `DD/MM/AAAA` |\n| **Data Necessária no Canteiro:** | `DD/MM/AAAA` |\n| **Centro de Custo:** | `CC-___` |\n")

    pc_tpl = os.path.join(sup_dir, "TEMPLATE_PEDIDO_DE_COMPRA_PC.md")
    if not os.path.exists(pc_tpl):
        with open(pc_tpl, "w", encoding="utf-8") as f:
            f.write(f"# 📦 MODELO PADRÃO: PEDIDO DE COMPRA (PC)\n\n**Empreendimento:** {nome_obra}\n\n| Campo | Preenchimento Formal |\n|---|---|\n| **Número do PC:** | `PC-___ / 2026` |\n| **Fornecedor:** | `Razão Social / CNPJ` |\n| **Condição de Pagamento:** | `30 DDL após entrega` |\n")

    return {
        "status": "sucesso",
        "csv_path": csv_path,
        "md_path": md_path,
        "itens_tracker": len(tracker_data)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motor Universal de Tracker de Suprimentos Multi-Obra")
    parser.add_argument("--obra", help="Nome da pasta da obra em /projetos/ (ex: OBRA_TMULT, RESIDENCIAL_ALPHA)")
    parser.add_argument("--dir", help="Caminho direto para a pasta da obra")
    args = parser.parse_args()

    if not args.obra and not args.dir:
        parser.print_help()
        sys.exit(1)

    gerar_tracker(obra_nome=args.obra, custom_dir=args.dir)
