#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador do Plano de Contas e Centros de Custo (CC) da OBRA_TMULT
Gera a amarração unívoca entre:
- Código EAP (Serviço Físico)
- Centro de Custo Contábil / Gerencial (CC)
- Natureza de Gasto (Material, Equipamento, Mão de Obra, Subcontrato)
- Requisição de Compra (RC) e Pedido de Compra (PC)
- Chave de Lançamento de Nota Fiscal (NF-e) para Conciliação de 3 Pontas

Gera:
1. PLANO_DE_CENTRO_DE_CUSTOS_TMULT.csv (em 02_ORCAMENTO_BASE_E_CONTRATOS)
2. PLANO_DE_CENTRO_DE_CUSTOS_TMULT.md (em 02_ORCAMENTO_BASE_E_CONTRATOS)
"""

import os
import sys
import csv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORC_DIR = os.path.join(BASE_DIR, "projetos", "OBRA_TMULT", "02_ORCAMENTO_BASE_E_CONTRATOS")
SUP_DIR = os.path.join(BASE_DIR, "projetos", "OBRA_TMULT", "05_SUPRIMENTOS_E_FINANCEIRO")
os.makedirs(ORC_DIR, exist_ok=True)
os.makedirs(SUP_DIR, exist_ok=True)

CENTROS_DE_CUSTO = [
    # GRUPO 1: CANTEIRO E GESTÃO LOCAL
    {"cc_codigo": "CC-100", "nivel": "Sintético", "descricao": "CANTEIRO DE OBRAS & ADMINISTRAÇÃO LOCAL", "eap_macro": "1.0", "natureza": "Custo Direto Canteiro", "conta_contabil": "4.1.1.01"},
    {"cc_codigo": "CC-101", "nivel": "Analítico", "descricao": "Gestão Técnica de Obra (Eng. Residente e Mestre)", "eap_macro": "1.0.1", "natureza": "Mão de Obra Indireta", "conta_contabil": "4.1.1.01.01"},
    {"cc_codigo": "CC-102", "nivel": "Analítico", "descricao": "Apoio e Segurança (TST, Almoxarife, Vigia)", "eap_macro": "1.0.2", "natureza": "Mão de Obra Indireta", "conta_contabil": "4.1.1.01.02"},
    {"cc_codigo": "CC-103", "nivel": "Analítico", "descricao": "Locação de Containers Habitáveis e Sanitários Químicos", "eap_macro": "1.0.3", "natureza": "Locação de Equipamentos", "conta_contabil": "4.1.1.01.03"},
    {"cc_codigo": "CC-104", "nivel": "Analítico", "descricao": "Contas de Consumo Canteiro (Energia, Água Pipa, Fibra)", "eap_macro": "1.0.4", "natureza": "Utilidades e Serviços", "conta_contabil": "4.1.1.01.04"},
    {"cc_codigo": "CC-105", "nivel": "Analítico", "descricao": "Vivência, Alimentação (16 operários) e Transporte", "eap_macro": "1.0.5", "natureza": "Benefícios Operacionais", "conta_contabil": "4.1.1.01.05"},
    {"cc_codigo": "CC-106", "nivel": "Analítico", "descricao": "SST, PGR/PCMSO, EPIs, Caçambas e Apoio", "eap_macro": "1.0.6", "natureza": "Segurança e Descarte", "conta_contabil": "4.1.1.01.06"},

    # GRUPO 2: INFRAESTRUTURA E FUNDAÇÕES
    {"cc_codigo": "CC-200", "nivel": "Sintético", "descricao": "INFRAESTRUTURA & FUNDAÇÕES", "eap_macro": "1.1", "natureza": "Custo Direto Físico", "conta_contabil": "4.1.2.01"},
    {"cc_codigo": "CC-201", "nivel": "Analítico", "descricao": "Escavação Mecanizada/Manual e Compactação de Valas", "eap_macro": "1.1.1 e 1.1.2", "natureza": "Serviço de Terraplenagem", "conta_contabil": "4.1.2.01.01"},
    {"cc_codigo": "CC-202", "nivel": "Analítico", "descricao": "Lastro de Concreto Magro fck 15 MPa (e=5cm)", "eap_macro": "1.1.3", "natureza": "Material - Concreto", "conta_contabil": "4.1.2.01.02"},
    {"cc_codigo": "CC-203", "nivel": "Analítico", "descricao": "Concreto Usinado fck 30 MPa - Sapatas Isoladas", "eap_macro": "1.1.4", "natureza": "Material - Concreto Usinado", "conta_contabil": "4.1.2.01.03"},
    {"cc_codigo": "CC-204", "nivel": "Analítico", "descricao": "Fôrmas Compensado 17mm - Sapatas Isoladas", "eap_macro": "1.1.5", "natureza": "Material - Madeira e Fôrmas", "conta_contabil": "4.1.2.01.04"},
    {"cc_codigo": "CC-205", "nivel": "Analítico", "descricao": "Concreto e Fôrmas - Arranques de Pilares P1-P24", "eap_macro": "1.1.6 e 1.1.7", "natureza": "Material - Concreto e Fôrmas", "conta_contabil": "4.1.2.01.05"},
    {"cc_codigo": "CC-206", "nivel": "Analítico", "descricao": "Concreto Usinado fck 30 MPa - Vigas Baldrames", "eap_macro": "1.1.8", "natureza": "Material - Concreto Usinado", "conta_contabil": "4.1.2.01.06"},
    {"cc_codigo": "CC-207", "nivel": "Analítico", "descricao": "Fôrmas Compensado 17mm - Vigas Baldrames (140m)", "eap_macro": "1.1.9", "natureza": "Material - Madeira e Fôrmas", "conta_contabil": "4.1.2.01.07"},
    {"cc_codigo": "CC-208", "nivel": "Analítico", "descricao": "Armadura CA-50 Cortada/Dobrada - Sapatas Isoladas", "eap_macro": "1.1.10", "natureza": "Material - Aço Estrutural", "conta_contabil": "4.1.2.01.08"},
    {"cc_codigo": "CC-209", "nivel": "Analítico", "descricao": "Armadura CA-50 Cortada/Dobrada - Arranques de Pilares", "eap_macro": "1.1.11", "natureza": "Material - Aço Estrutural", "conta_contabil": "4.1.2.01.09"},
    {"cc_codigo": "CC-210", "nivel": "Analítico", "descricao": "Armadura CA-50 Cortada/Dobrada - Vigas Baldrames", "eap_macro": "1.1.12", "natureza": "Material - Aço Estrutural", "conta_contabil": "4.1.2.01.10"},
    {"cc_codigo": "CC-211", "nivel": "Analítico", "descricao": "Impermeabilização Tinta Asfáltica (Baldrames e Sapatas)", "eap_macro": "1.1.13", "natureza": "Material - Impermeabilizantes", "conta_contabil": "4.1.2.01.11"},
    {"cc_codigo": "CC-212", "nivel": "Analítico", "descricao": "Reaterro Compactado e Bota-Fora de Cavas", "eap_macro": "1.1.14 e 1.1.15", "natureza": "Serviço de Terraplenagem", "conta_contabil": "4.1.2.01.12"},

    # GRUPO 3: SUPRAESTRUTURA
    {"cc_codigo": "CC-300", "nivel": "Sintético", "descricao": "SUPRAESTRUTURA (PILARES, VIGAS E LAJES)", "eap_macro": "1.2", "natureza": "Custo Direto Físico", "conta_contabil": "4.1.2.02"},
    {"cc_codigo": "CC-301", "nivel": "Analítico", "descricao": "Concreto Usinado fck 30 MPa - Pilares P1 a P24", "eap_macro": "1.2.1", "natureza": "Material - Concreto Usinado", "conta_contabil": "4.1.2.02.01"},
    {"cc_codigo": "CC-302", "nivel": "Analítico", "descricao": "Fôrmas Compensado 17mm - Pilares P1 a P24", "eap_macro": "1.2.2", "natureza": "Material - Madeira e Fôrmas", "conta_contabil": "4.1.2.02.02"},
    {"cc_codigo": "CC-303", "nivel": "Analítico", "descricao": "Concreto Usinado fck 30 MPa - Vigas Superiores e Cobertura", "eap_macro": "1.2.3", "natureza": "Material - Concreto Usinado", "conta_contabil": "4.1.2.02.03"},
    {"cc_codigo": "CC-304", "nivel": "Analítico", "descricao": "Fôrmas Compensado 17mm - Vigas Superiores", "eap_macro": "1.2.4", "natureza": "Material - Madeira e Fôrmas", "conta_contabil": "4.1.2.02.04"},
    {"cc_codigo": "CC-305", "nivel": "Analítico", "descricao": "Concreto Usinado fck 30 MPa - Capa de Laje Treliçada e=5cm", "eap_macro": "1.2.5", "natureza": "Material - Concreto Usinado", "conta_contabil": "4.1.2.02.05"},
    {"cc_codigo": "CC-306", "nivel": "Analítico", "descricao": "Fôrmas e Escoramento Metálico - Lajes e Vigas", "eap_macro": "1.2.6 e 1.2.7", "natureza": "Locação de Equipamentos / Fôrma", "conta_contabil": "4.1.2.02.06"},
    {"cc_codigo": "CC-307", "nivel": "Analítico", "descricao": "Vigotas Treliçadas TR 16745 e EPS para Lajes H12", "eap_macro": "1.2.8 e 1.2.9", "natureza": "Material - Laje Premoldada", "conta_contabil": "4.1.2.02.07"},
    {"cc_codigo": "CC-308", "nivel": "Analítico", "descricao": "Armadura CA-50 Pilares e Vigas + CA-60 Lajes", "eap_macro": "1.2.10 e 1.2.11", "natureza": "Material - Aço Estrutural", "conta_contabil": "4.1.2.02.08"},

    # GRUPO 4: ARQUITETURA, VEDAÇÃO E ACABAMENTOS
    {"cc_codigo": "CC-400", "nivel": "Sintético", "descricao": "ARQUITETURA, ALVENARIAS E ACABAMENTOS", "eap_macro": "2.1", "natureza": "Custo Direto Físico", "conta_contabil": "4.1.2.03"},
    {"cc_codigo": "CC-401", "nivel": "Analítico", "descricao": "Alvenaria de Vedação (Blocos de Concreto 14x19x39)", "eap_macro": "2.1.1", "natureza": "Material - Blocos e Argamassas", "conta_contabil": "4.1.2.03.01"},
    {"cc_codigo": "CC-402", "nivel": "Analítico", "descricao": "Chapisco e Emboço/Reboco Paulista 20mm", "eap_macro": "2.1.2 e 2.1.3", "natureza": "Material/MO Revestimentos", "conta_contabil": "4.1.2.03.02"},
    {"cc_codigo": "CC-403", "nivel": "Analítico", "descricao": "Contrapiso e Porcelanato Retificado 60x60cm", "eap_macro": "2.1.4, 2.1.5 e 2.1.7", "natureza": "Material - Pisos e Argamassas", "conta_contabil": "4.1.2.03.03"},
    {"cc_codigo": "CC-404", "nivel": "Analítico", "descricao": "Revestimento Cerâmico de Paredes WCs (45x45)", "eap_macro": "2.1.6", "natureza": "Material - Cerâmica e Argamassa", "conta_contabil": "4.1.2.03.04"},
    {"cc_codigo": "CC-405", "nivel": "Analítico", "descricao": "Pintura Látex Acrílica 3 Demãos (Paredes e Tetos)", "eap_macro": "2.1.8", "natureza": "Material - Tintas e Acessórios", "conta_contabil": "4.1.2.03.05"},
    {"cc_codigo": "CC-406", "nivel": "Analítico", "descricao": "Esquadrias de Madeira (Portas P1 a P5 completas)", "eap_macro": "2.1.9", "natureza": "Material - Esquadrias Madeira", "conta_contabil": "4.1.2.03.06"},
    {"cc_codigo": "CC-407", "nivel": "Analítico", "descricao": "Esquadrias de Alumínio e Vidro (Janelas J1 a J4)", "eap_macro": "2.1.10", "natureza": "Material - Esquadrias Alumínio", "conta_contabil": "4.1.2.03.07"},
    {"cc_codigo": "CC-408", "nivel": "Analítico", "descricao": "Impermeabilização Polimérica WCs e Copa", "eap_macro": "2.1.11", "natureza": "Material - Impermeabilizantes", "conta_contabil": "4.1.2.03.08"},

    # GRUPO 5: COBERTURA TERMOACÚSTICA
    {"cc_codigo": "CC-500", "nivel": "Sintético", "descricao": "COBERTURA, ESTRUTURA METÁLICA E CALHAS", "eap_macro": "2.2", "natureza": "Custo Direto Físico", "conta_contabil": "4.1.2.04"},
    {"cc_codigo": "CC-501", "nivel": "Analítico", "descricao": "Telhas Termoacústicas Sandwich EPS 30mm", "eap_macro": "2.2.1", "natureza": "Material - Cobertura", "conta_contabil": "4.1.2.04.01"},
    {"cc_codigo": "CC-502", "nivel": "Analítico", "descricao": "Estrutura Metálica de Apoio (Terças Perfil U)", "eap_macro": "2.2.2 e 2.2.3", "natureza": "Material - Perfis Metálicos", "conta_contabil": "4.1.2.04.02"},
    {"cc_codigo": "CC-503", "nivel": "Analítico", "descricao": "Calhas, Rufos e Impermeabilização com Manta 4mm", "eap_macro": "2.2.4 a 2.2.7", "natureza": "Material - Calhas e Mantas", "conta_contabil": "4.1.2.04.03"},
    {"cc_codigo": "CC-504", "nivel": "Analítico", "descricao": "Alvenaria e Revestimento de Platibanda", "eap_macro": "2.2.8 a 2.2.10", "natureza": "Material/MO Platibanda", "conta_contabil": "4.1.2.04.04"},

    # GRUPO 6: INSTALAÇÕES MEP & HVAC
    {"cc_codigo": "CC-600", "nivel": "Sintético", "descricao": "INSTALAÇÕES ELÉTRICAS, CABEAMENTO E TELECOM", "eap_macro": "3.1 e 3.3", "natureza": "Custo Direto Físico", "conta_contabil": "4.1.2.05"},
    {"cc_codigo": "CC-601", "nivel": "Analítico", "descricao": "Cabos de Cobre, Eletrodutos e Caixas de Embutir", "eap_macro": "3.1.1 a 3.1.7", "natureza": "Material - Elétrica Básica", "conta_contabil": "4.1.2.05.01"},
    {"cc_codigo": "CC-602", "nivel": "Analítico", "descricao": "Quadros QDG/QDF, Disjuntores DIN, DR e DPS", "eap_macro": "3.1.8 e 3.1.10", "natureza": "Material - Dispositivos Elétricos", "conta_contabil": "4.1.2.05.02"},
    {"cc_codigo": "CC-603", "nivel": "Analítico", "descricao": "Interruptores, Tomadas e Luminárias LED 60x60", "eap_macro": "3.1.9 e 3.1.11", "natureza": "Material - Acabamento Elétrico", "conta_contabil": "4.1.2.05.03"},
    {"cc_codigo": "CC-604", "nivel": "Analítico", "descricao": "Cabeamento Estruturado Cat6, Rack 12U e Switch", "eap_macro": "3.3.1 a 3.3.4", "natureza": "Material - Redes e Telecom", "conta_contabil": "4.1.2.05.04"},

    {"cc_codigo": "CC-700", "nivel": "Sintético", "descricao": "INSTALAÇÕES HIDROSSANITÁRIAS E PLUVIAIS", "eap_macro": "3.2", "natureza": "Custo Direto Físico", "conta_contabil": "4.1.2.06"},
    {"cc_codigo": "CC-701", "nivel": "Analítico", "descricao": "Tubos e Conexões PVC Água Fria, Esgoto e Ventilação", "eap_macro": "3.2.1 a 3.2.8", "natureza": "Material - Tubulações PVC", "conta_contabil": "4.1.2.06.01"},
    {"cc_codigo": "CC-702", "nivel": "Analítico", "descricao": "Registros de Gaveta/Pressão e Caixas de Gordura", "eap_macro": "3.2.9 e 3.2.10", "natureza": "Material - Válvulas e Caixas", "conta_contabil": "4.1.2.06.02"},
    {"cc_codigo": "CC-703", "nivel": "Analítico", "descricao": "Louças Sanitárias, Cubas, Torneiras e Acessórios", "eap_macro": "3.2.11 e 3.2.12", "natureza": "Material - Louças e Metais", "conta_contabil": "4.1.2.06.03"},
    {"cc_codigo": "CC-704", "nivel": "Analítico", "descricao": "Reservatórios de Polietileno 5.000L", "eap_macro": "3.2.13", "natureza": "Material - Reservatórios", "conta_contabil": "4.1.2.06.04"},

    {"cc_codigo": "CC-800", "nivel": "Sintético", "descricao": "CLIMATIZAÇÃO E HVAC", "eap_macro": "4.1", "natureza": "Custo Direto Físico", "conta_contabil": "4.1.2.07"},
    {"cc_codigo": "CC-801", "nivel": "Analítico", "descricao": "Aparelhos Split Cassete 36.000 e Hi-Wall Inverter", "eap_macro": "4.1.1 e 4.1.2", "natureza": "Equipamentos de Climatização", "conta_contabil": "4.1.2.07.01"},
    {"cc_codigo": "CC-802", "nivel": "Analítico", "descricao": "Linhas Frigorígenas, Cobre e Instalação HVAC", "eap_macro": "4.1.3", "natureza": "Serviço Especializado HVAC", "conta_contabil": "4.1.2.07.02"}
]

def gerar_arquivos():
    csv_path = os.path.join(ORC_DIR, "PLANO_DE_CENTRO_DE_CUSTOS_TMULT.csv")
    with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Codigo_CC", "Nivel", "Descricao_Centro_Custo", "EAP_Macro_Vinculada", "Natureza_Gasto", "Conta_Contabil"])
        for c in CENTROS_DE_CUSTO:
            writer.writerow([c["cc_codigo"], c["nivel"], c["descricao"], c["eap_macro"], c["natureza"], c["conta_contabil"]])
    print(f"✅ CSV Plano de Centros de Custo gerado: {csv_path}")

    md_path = os.path.join(ORC_DIR, "PLANO_DE_CENTRO_DE_CUSTOS_TMULT.md")
    linhas = [
        "# 📑 PLANO MESTRE DE CENTROS DE CUSTO & APROPRIAÇÃO CONTÁBIL",
        "",
        "**Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Porto do Açu (SJB/RJ)",
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

    for c in CENTROS_DE_CUSTO:
        destaque = "**" if c["nivel"] == "Sintético" else ""
        linhas.append(
            f"| {destaque}`{c['cc_codigo']}`{destaque} | {c['nivel']} | {destaque}{c['descricao']}{destaque} | "
            f"`{c['eap_macro']}` | {c['natureza']} | `{c['conta_contabil']}` |"
        )

    linhas.extend([
        "",
        "---",
        "",
        "## 🛒 3. Centros de Custo Aplicados aos Suprimentos Críticos do Mês 1",
        "",
        "Para os 4 pacotes de compra de partida da obra, os Centros de Custo obrigatórios a constar nas RCs e nos PCs são:",
        "",
        "| Pacote / RC | Insumo / Serviço Contratado | Centro de Custo (CC) | Conta Contábil | Orçado Custo Direto |",
        "| :---: | :--- | :---: | :---: | :---: |",
        "| **RC-001/2026** | Aço CA-50 Fundações (Sapatas e Baldrames) | `CC-208` e `CC-210` | 4.1.2.01.08 / 10 | R$ 15.635,66 |",
        "| **RC-002/2026** | Concreto Usinado fck 30 MPa e Lastro | `CC-202`, `CC-203` e `CC-206` | 4.1.2.01.02 / 03 / 06 | R$ 20.252,08 |",
        "| **RC-003/2026** | Compensado 17mm e Fôrmas de Madeira | `CC-204` e `CC-207` | 4.1.2.01.04 / 07 | R$ 20.286,07 |",
        "| **RC-004/2026** | Containers Habitáveis NR-18 (6 Meses) | `CC-103` | 4.1.1.01.03 | R$ 38.299,98 |",
        "",
        "---",
        "*Plano auditado e vinculado à Linha de Base SINAPI SP 07/2026.*"
    ])

    with open(md_path, mode="w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"✅ Relatório Plano de Centros de Custo gerado: {md_path}")

if __name__ == "__main__":
    gerar_arquivos()
