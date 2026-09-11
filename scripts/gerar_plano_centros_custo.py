#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Centros de Custo & Apropriação Contábil Multi-Obra
Ecossistema de Gestão de Obras & PMO Virtual

Gera a amarração unívoca entre:
- Código EAP (Serviço Físico)
- Centro de Custo Contábil / Gerencial (CC)
- Natureza de Gasto (Material, Equipamento, Mão de Obra, Subcontrato)
- Requisição de Compra (RC) e Pedido de Compra (PC)
- Chave de Lançamento de Nota Fiscal (NF-e) para Conciliação de 3 Pontas

Uso:
    python scripts/gerar_plano_centros_custo.py --obra OBRA_TMULT
    python scripts/gerar_plano_centros_custo.py --obra RESIDENCIAL_ALPHA
"""

import os
import sys
import csv
import json
import argparse

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def gerar_plano_centros_custo(obra_nome=None, custom_dir=None):
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

    # 1. Carregar configuração
    config_path = os.path.join(proj_dir, "config_obra.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {}

    nome_obra = config.get("nome_obra", obra_id)
    sigla_obra = config.get("sigla_obra", obra_id)
    area_m2 = config.get("area_construida_m2", "N/A")

    orc_dir = os.path.join(proj_dir, "02_ORCAMENTO_BASE_E_CONTRATOS")
    os.makedirs(orc_dir, exist_ok=True)

    cc_file = os.path.join(orc_dir, "estrutura_centros_custo.json")
    if not os.path.exists(cc_file):
        # Tenta carregar do template
        tpl_cc = os.path.join(base_repo_dir, "projetos", "_TEMPLATE_OBRA_NOVA", "02_ORCAMENTO_BASE_E_CONTRATOS", "estrutura_centros_custo.json")
        if not os.path.exists(tpl_cc):
            tpl_cc = os.path.join(base_repo_dir, "projetos", "_TEMPLATE_OBRA_NOVA", "02_ORCAMENTO_BASE_E_CONTRATOS", "estrutura_centros_custo.template.json")
        if os.path.exists(tpl_cc):
            with open(tpl_cc, "r", encoding="utf-8") as f:
                centros_de_custo = json.load(f)
        else:
            raise FileNotFoundError(f"Estrutura de centros de custo não encontrada em {cc_file}")
    else:
        with open(cc_file, "r", encoding="utf-8") as f:
            centros_de_custo = json.load(f)

    # 3. Gerar CSV
    csv_filename = f"PLANO_DE_CENTRO_DE_CUSTOS_{sigla_obra}.csv"
    csv_path = os.path.join(orc_dir, csv_filename)
    with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Codigo_CC", "Nivel", "Descricao_Centro_Custo", "EAP_Macro_Vinculada", "Natureza_Gasto", "Conta_Contabil"])
        for c in centros_de_custo:
            writer.writerow([c["cc_codigo"], c["nivel"], c["descricao"], c["eap_macro"], c["natureza"], c["conta_contabil"]])
    print(f"✅ CSV Plano de Centros de Custo gerado: {csv_path}")

    # 4. Gerar Markdown
    md_filename = f"PLANO_DE_CENTRO_DE_CUSTOS_{sigla_obra}.md"
    md_path = os.path.join(orc_dir, md_filename)
    linhas = [
        "# 📑 PLANO MESTRE DE CENTROS DE CUSTO & APROPRIAÇÃO CONTÁBIL",
        "",
        f"**Empreendimento:** {nome_obra} ({area_m2} m²)",
        "**Função:** Rastreabilidade unívoca de Requisições de Compra (RC), Pedidos de Compra (PC) e Notas Fiscais (NF-e)",
        "**Padrão do Ecossistema:** SKILL_QUANTIFICACAO_CONCILIACAO_3_PONTAS & SKILL_GESTAO_03_ADMINISTRATIVO",
        "",
        "---",
        "",
        "## 🎯 1. Por que o Centro de Custo (CC) é Obrigatório na RC e no PC?",
        "",
        "Em construtoras organizadas, **nenhum material é comprado e nenhuma nota fiscal é paga** sem a indicação formal do Centro de Custo:",
        "1. **Eliminação do 'Lixo Contábil':** Impede que o financeiro jogue notas de concreto ou aço em 'Despesas Gerais de Obra';",
        "2. **Orçado vs. Realizado em Tempo Real:** Permite ao Diretor confrontar na hora se a despesa lançada na NF-e está estourando a verba orçada daquela EAP;",
        "3. **Conciliação de 3 Pontas Automática:** Quando o fornecedor emite a NF-e com o número do Pedido de Compra e o Centro de Custo no corpo da nota, o sistema confere e aprova o pagamento com segurança máxima.",
        "",
        "---",
        "",
        "## 📊 2. Estrutura Canônica de Centros de Custo (EAP × CC × Contabilidade)",
        "",
        "| Centro de Custo (CC) | Nível | Descrição / Objeto da Despesa | EAP Vinculada | Natureza de Gasto | Conta Contábil |",
        "| :---: | :---: | :--- | :---: | :--- | :---: |"
    ]

    for c in centros_de_custo:
        destaque = "**" if c["nivel"] == "Sintético" else ""
        linhas.append(
            f"| {destaque}`{c['cc_codigo']}`{destaque} | {c['nivel']} | {destaque}{c['descricao']}{destaque} | "
            f"`{c['eap_macro']}` | {c['natureza']} | `{c['conta_contabil']}` |"
        )

    linhas.extend([
        "",
        "---",
        "*Plano auditado e vinculado à Linha de Base e Governança do Ecossistema.*"
    ])

    with open(md_path, mode="w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"✅ Relatório Plano de Centros de Custo gerado: {md_path}")

    return {
        "status": "sucesso",
        "csv_path": csv_path,
        "md_path": md_path,
        "centros_custo_total": len(centros_de_custo)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motor Universal de Centros de Custo Multi-Obra")
    parser.add_argument("--obra", help="Nome da pasta da obra em /projetos/ (ex: OBRA_TMULT, RESIDENCIAL_ALPHA)")
    parser.add_argument("--dir", help="Caminho direto para a pasta da obra")
    args = parser.parse_args()

    if not args.obra and not args.dir:
        parser.print_help()
        sys.exit(1)

    gerar_plano_centros_custo(obra_nome=args.obra, custom_dir=args.dir)
