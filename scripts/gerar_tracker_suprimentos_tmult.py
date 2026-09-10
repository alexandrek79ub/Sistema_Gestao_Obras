#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Gestão do Pipeline de Suprimentos & Tracker de Requisições de Compra (RC)
OBRA_TMULT - Edifício Administrativo (Porto do Açu)

Gera e atualiza:
1. TRACKER_SUPRIMENTOS_RC_TMULT.csv (Base tabular do funil de suprimentos)
2. TRACKER_SUPRIMENTOS_RC_TMULT.md (Painel executivo com Kanban e Semáforos)
3. TEMPLATE_REQUISICAO_DE_COMPRA_RC.md (Minuta oficial para emissão de novas RCs pela Engenharia)
4. TEMPLATE_PEDIDO_DE_COMPRA_PC.md (Minuta oficial de Pedido de Compra de Suprimentos para Fornecedor)

Pipeline Padronizado de 7 Estágios:
1. PENDENTE_SUPRIMENTOS: Obra emitiu a RC técnica e aguarda início do processo pelo Comprador.
2. EM_COTACAO: Comprador disparou a RC para fornecedores cadastrados.
3. COTACOES_RECEBIDAS: Propostas recebidas e aguardando equalização.
4. MAPA_EQUALIZADO: Comprador montou o mapa comparativo de preços e saving vs SINAPI.
5. EM_APROVACAO_DIRETORIA: Submetido à Diretoria/Gestor na alçada da Skill Gestão 03.
6. PEDIDO_EMITIDO_PC: Diretoria aprovou e Suprimentos gerou o Pedido de Compra formal.
7. ENTREGUE_EM_OBRA: Material conferido no canteiro (Conciliação NF x PC x FVS).
"""

import os
import sys
import csv
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Caminhos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "projetos", "OBRA_TMULT", "05_SUPRIMENTOS_E_FINANCEIRO")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# DADOS DO PIPELINE DE SUPRIMENTOS - MÊS 1
# -------------------------------------------------------------

REQUISICOES_TRACKER = [
    {
        "id_rc": "RC-001/2026",
        "pacote": "Aço CA-50 e CA-60 Cortado e Dobrado (Fundações)",
        "centro_custo": "CC-208 / CC-209 / CC-210",
        "disciplina": "Infraestrutura",
        "eap_itens": "1.1.10, 1.1.11, 1.1.12",
        "data_emissao": "12/09/2026",
        "data_necessidade": "28/09/2026",
        "lead_time_dias": 16,
        "estagio_pipeline": "1. PENDENTE_SUPRIMENTOS",
        "responsavel_atual": "Suprimentos (Comprador)",
        "proxima_acao": "Disparar cotação formal para Gerdau, ArcelorMittal e Açofer",
        "semaforo": "🟢 NO PRAZO",
        "orcamento_base_cd": 15635.66,
        "fornecedor_homologado": "Gerdau Aços Longos (Pré-qualificado)",
        "num_pc": "Pendente Abertura",
        "cond_pagamento_alvo": "30 DDL Faturado"
    },
    {
        "id_rc": "RC-002/2026",
        "pacote": "Concreto Usinado fck 30 MPa Bombeável e Lastro fck 15 MPa",
        "centro_custo": "CC-202 / CC-203 / CC-205 / CC-206",
        "disciplina": "Infraestrutura",
        "eap_itens": "1.1.3, 1.1.4, 1.1.6, 1.1.8",
        "data_emissao": "14/09/2026",
        "data_necessidade": "01/10/2026",
        "lead_time_dias": 17,
        "estagio_pipeline": "1. PENDENTE_SUPRIMENTOS",
        "responsavel_atual": "Suprimentos (Comprador)",
        "proxima_acao": "Solicitar proposta de fornecimento e bombeamento para Polimix e Supermix",
        "semaforo": "🟢 NO PRAZO",
        "orcamento_base_cd": 20252.08,
        "fornecedor_homologado": "Polimix Concreto (Central SJB - 14km)",
        "num_pc": "Pendente Abertura",
        "cond_pagamento_alvo": "30 DDL após laudo 7d"
    },
    {
        "id_rc": "RC-003/2026",
        "pacote": "Compensado Resinado 17mm, Madeiramento e Consumíveis de Fôrma",
        "centro_custo": "CC-204 / CC-205 / CC-207",
        "disciplina": "Infraestrutura",
        "eap_itens": "1.1.5, 1.1.7, 1.1.9",
        "data_emissao": "12/09/2026",
        "data_necessidade": "26/09/2026",
        "lead_time_dias": 14,
        "estagio_pipeline": "1. PENDENTE_SUPRIMENTOS",
        "responsavel_atual": "Suprimentos (Comprador)",
        "proxima_acao": "Disparar para Madenorte e Madeireira Real Açu (Atenção ao prazo de 14 dias)",
        "semaforo": "🟡 ATENÇÃO",
        "orcamento_base_cd": 20286.07,
        "fornecedor_homologado": "Madenorte Madeiras (Pré-qualificado)",
        "num_pc": "Pendente Abertura",
        "cond_pagamento_alvo": "30 DDL Boleto"
    },
    {
        "id_rc": "RC-004/2026",
        "pacote": "Locação de Módulos Containers NR-18 e Sanitários Químicos (6 Meses)",
        "centro_custo": "CC-103",
        "disciplina": "Canteiro e Vivência",
        "eap_itens": "1.0.3",
        "data_emissao": "10/09/2026",
        "data_necessidade": "22/09/2026",
        "lead_time_dias": 12,
        "estagio_pipeline": "1. PENDENTE_SUPRIMENTOS",
        "responsavel_atual": "Suprimentos (Comprador)",
        "proxima_acao": "Disparar minuta de contrato para Rentcon e NHJ para entrega urgente no Mês 1",
        "semaforo": "🟡 ATENÇÃO",
        "orcamento_base_cd": 38299.98,
        "fornecedor_homologado": "Rentcon Locações (Base Macaé / Açu)",
        "num_pc": "Pendente Abertura",
        "cond_pagamento_alvo": "Medição Mensal D+30"
    }
]

# -------------------------------------------------------------
# 1. GERAÇÃO DO ARQUIVO CSV DO TRACKER
# -------------------------------------------------------------
def gerar_csv_tracker():
    csv_path = os.path.join(OUTPUT_DIR, "TRACKER_SUPRIMENTOS_RC_TMULT.csv")
    with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([
            "ID_RC", "Pacote_Insumo", "Centro_Custo_CC", "Disciplina", "EAP_Itens",
            "Data_Emissao_Obra", "Data_Necessidade_Canteiro", "Lead_Time_Dias",
            "Estagio_Pipeline", "Responsavel_Atual", "Proxima_Acao_Gargalo",
            "Semaforo_Risco", "Budget_Custo_Direto_R$", "Fornecedor_PreQualificado",
            "Numero_PC", "Condicao_Pagamento_Alvo"
        ])
        for r in REQUISICOES_TRACKER:
            writer.writerow([
                r["id_rc"], r["pacote"], r["centro_custo"], r["disciplina"], r["eap_itens"],
                r["data_emissao"], r["data_necessidade"], r["lead_time_dias"],
                r["estagio_pipeline"], r["responsavel_atual"], r["proxima_acao"],
                r["semaforo"], f"{r['orcamento_base_cd']:.2f}", r["fornecedor_homologado"],
                r["num_pc"], r["cond_pagamento_alvo"]
            ])
    print(f"✅ CSV Tracker gerado com sucesso: {csv_path}")

# -------------------------------------------------------------
# 2. GERAÇÃO DO PAINEL EXECUTIVO EM MARKDOWN COM KANBAN
# -------------------------------------------------------------
def gerar_md_tracker():
    md_path = os.path.join(OUTPUT_DIR, "TRACKER_SUPRIMENTOS_RC_TMULT.md")
    
    linhas = []
    linhas.append("# 📊 PAINEL DE RASTREABILIDADE DE SUPRIMENTOS & TRACKER DE RCs")
    linhas.append("")
    linhas.append("**Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Porto do Açu (SJB/RJ)")
    linhas.append("**Módulo de Gestão:** Suprimentos & Governança de Compras (Pipeline Ágil)")
    linhas.append("**Público-Alvo:** Diretoria, Gestor de Contratos, Engenheiro Residente e Setor de Compras")
    linhas.append(f"**Data da Última Atualização:** {datetime.now().strftime('%d/%m/%Y')} | **Ciclo Atual:** Mês 1 (Partida de Obras)")
    linhas.append("")
    linhas.append("---")
    linhas.append("")
    linhas.append("## 🧭 1. O Funil Operacional de Suprimentos (7 Estágios Padronizados)")
    linhas.append("")
    linhas.append("Para construtoras enxutas, cada compra percorre obrigatoriamente 7 portas de controle para evitar compras erradas, atrasos de canteiro ou furos de caixa:")
    linhas.append("")
    linhas.append("| Estágio do Funil | O que Significa na Prática? | Quem é o 'Dono da Bola'? | Documento Formal |")
    linhas.append("| :---: | :--- | :---: | :---: |")
    linhas.append("| `1. PENDENTE_SUPRIMENTOS` | Obra emitiu a RC técnica com UCC, EAP e data limite no canteiro. | **Comprador** | Requisição de Compra (RC) |")
    linhas.append("| `2. EM_COTAÇÃO` | Comprador disparou a RC para 3 fornecedores e aguarda propostas. | **Fornecedores** | Pedido de Cotação |")
    linhas.append("| `3. COTAÇÕES_RECEBIDAS` | Fornecedores responderam; propostas comerciais sob análise. | **Comprador** | Propostas Comerciais |")
    linhas.append("| `4. MAPA_EQUALIZADO` | Comprador montou o comparativo de preços, frete e saving vs SINAPI. | **Comprador** | Mapa de Cotação |")
    linhas.append("| `5. EM_APROVAÇÃO_DIRETORIA` | Mapa submetido ao Diretor/Gestor para bater o martelo na alçada da Skill 03. | **Diretoria** | Despacho de Aprovação |")
    linhas.append("| `6. PEDIDO_EMITIDO_PC` | Fornecedor vencedor contratado e Pedido de Compra formal despachado. | **Suprimentos / Fornecedor** | Pedido de Compra (PC) |")
    linhas.append("| `7. ENTREGUE_EM_OBRA` | Material descarregado e aprovado pela Engenharia (NF x PC x FVS). | **Engenharia / Almoxarife** | FVS e Canhoto da NF |")
    linhas.append("")
    linhas.append("---")
    linhas.append("")
    linhas.append("## 📋 2. Matriz Viva de Rastreabilidade das Requisições de Compra (RCs) — Mês 1")
    linhas.append("")
    linhas.append("| Nº RC | Pacote de Compra | Centro de Custo (CC) | Data Emissão | Data Limite Canteiro | Estágio Atual no Funil | Responsável Atual | Próxima Ação / Ponto de Atenção | Semáforo Lead Time |")
    linhas.append("| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :---: |")
    
    for r in REQUISICOES_TRACKER:
        linhas.append(
            f"| **{r['id_rc']}** | {r['pacote']} | `{r['centro_custo']}` | {r['data_emissao']} | **{r['data_necessidade']}** | "
            f"`{r['estagio_pipeline']}` | **{r['responsavel_atual']}** | {r['proxima_acao']} | {r['semaforo']} |"
        )
        
    linhas.append("")
    linhas.append("---")
    linhas.append("")
    linhas.append("## 📌 3. Quadro Visual Kanban de Suprimentos")
    linhas.append("")
    linhas.append("```")
    linhas.append("┌───────────────────────────┬───────────────────────────┬───────────────────────────┐")
    linhas.append("│ [1] PENDENTE SUPRIMENTOS  │ [2 e 3] COTAÇÃO & PROPOSTA│ [4 e 5] MAPA & APROVAÇÃO  │")
    linhas.append("├───────────────────────────┼───────────────────────────┼───────────────────────────┤")
    linhas.append("│ • RC-001 (Aço Fundações)  │ (Nenhuma RC nesta coluna) │ (Aguardando propostas     │")
    linhas.append("│ • RC-002 (Concreto 30MPa) │                           │  reais para submeter à    │")
    linhas.append("│ • RC-003 (Fôrmas 17mm)    │                           │  Diretoria)               │")
    linhas.append("│ • RC-004 (Containers Cnt) │                           │                           │")
    linhas.append("└───────────────────────────┴───────────────────────────┴───────────────────────────┘")
    linhas.append("┌───────────────────────────┬───────────────────────────┐")
    linhas.append("│ [6] PEDIDO EMITIDO (PC)   │ [7] ENTREGUE NA OBRA (FVS)│")
    linhas.append("├───────────────────────────┼───────────────────────────┤")
    linhas.append("│ (Aguardando aprovação     │ (Aguardando liberação dos │")
    linhas.append("│  para emissão dos PCs)    │  pedidos de compra)       │")
    linhas.append("└───────────────────────────┴───────────────────────────┘")
    linhas.append("```")
    linhas.append("")
    linhas.append("---")
    linhas.append("")
    linhas.append("## 🚨 4. Critérios de Alerta do Semáforo (Lead Time)")
    linhas.append("")
    linhas.append("- 🟢 **NO PRAZO:** Tempo restante até a necessidade na obra é superior ao dobro do lead time médio de cotação/entrega (sem risco de desabastecimento);")
    linhas.append("- 🟡 **ATENÇÃO:** Tempo restante entre 1x e 2x o lead time. Exige acompanhamento diário do comprador para cobrança dos orçamentos;")
    linhas.append("- 🔴 **CRÍTICO:** Tempo restante inferior ao lead time do fornecedor. Risco iminente de paralisar a frente de serviço do canteiro. A Diretoria deve acionar compras emergenciais ou fornecedores locais com pronta entrega.")
    linhas.append("")
    linhas.append("---")
    linhas.append("")
    linhas.append("*Painel de Governança mantido automaticamente pelo PMO Virtual A11.*")

    with open(md_path, mode="w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
        
    print(f"✅ Painel Tracker MD gerado com sucesso: {md_path}")

# -------------------------------------------------------------
# 3. GERAÇÃO DO TEMPLATE DE REQUISIÇÃO DE COMPRA (RC)
# -------------------------------------------------------------
def gerar_template_rc():
    rc_path = os.path.join(OUTPUT_DIR, "TEMPLATE_REQUISICAO_DE_COMPRA_RC.md")
    
    conteudo = """# 📋 MODELO PADRÃO: REQUISIÇÃO DE COMPRA (RC)
> **Origem:** Engenharia de Obra (Campo) ➔ **Destino:** Setor de Suprimentos (Compras)  
> **Referência Normativa:** POP 05, Diretrizes de Governança A11 e Plano de Centros de Custo

---

### 1. DADOS DE CABEÇALHO & CONTROLE

| Campo | Preenchimento Obrigatório |
| :--- | :--- |
| **Número da RC:** | `RC-___ / 2026` |
| **Obra / Contrato:** | `OBRA_TMULT — Edifício Administrativo (Porto do Açu)` |
| **Data de Emissão (Obra):** | `DD/MM/AAAA` |
| **Data Necessária no Canteiro:** | **`DD/MM/AAAA`** *(Respeitar Lead Time mínimo do POP 05)* |
| **Disciplina / EAP Vinculada:** | `Ex: Infraestrutura — EAP 1.1.4 e 1.1.8` |
| **Centro de Custo (CC):** | **`Ex: CC-200 (Infraestrutura) / Analítico: CC-203 e CC-206`** |
| **Local Exato de Aplicação (CIA):**| `Ex: Fundações — Sapatas Isoladas S1 a S24` |
| **Engenheiro Solicitante:** | `Nome e CREA` |

---

### 2. ESPECIFICAÇÃO TÉCNICA E QUANTIDADES EM UCC (Unidade Comercial de Compra)

> ⚠️ **Regra Inviolável:** A Engenharia levanta em unidade de projeto, mas converte obrigatoriamente para a embalagem comercial da indústria (barras de 12m, sacos de 50kg, chapas inteiras, m³ dosado em central). Toda linha carrega o Centro de Custo analítico para apropriação contábil.

| Item | Centro de Custo (CC) | Descrição Técnica Completa e Normativa | Qtd Projeto | Und Proj | % Perda | Qtd Compra | Und UCC | Prancha Executiva / Ref. |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 01 | `CC-___` | [Especificação exata: marca de ref., bitola, classe] | | | | | | |
| 02 | `CC-___` | | | | | | | |
| 03 | `CC-___` | | | | | | | |

---

### 3. REQUISITOS TÉCNICOS DE RECEBIMENTO NO CANTEIRO (POP 06)
- **Ensaios Obrigatórios na Entrega:** (Ex: Slump test para concreto / Laudo de ensaio de tração para aço / Selo FSC para madeira);
- **Condição de Frete Exigida:** CIF Canteiro com descarga mecânica/manual por conta do fornecedor;
- **Horário Permitido para Descarga:** Segunda a Sexta, das 07h30 às 16h30 (Portão Portuário TMULT).

---

### 4. CARIMBOS DE DESPACHO E PROTOCOLO

| Instância | Responsável | Data | Parecer / Assinatura |
| :--- | :--- | :---: | :--- |
| **Emissão de Campo:** | Eng. Residente | DD/MM/AAAA | [ ] Aprovado para Cotação |
| **Recebimento Suprimentos:** | Comprador | DD/MM/AAAA | [ ] Aberto no Pipeline de Compras |
| **Status Atual no Tracker:** | `[ ] 1. PENDENTE` `[ ] 2. EM COTAÇÃO` `[ ] 3. PROPOSTAS RECEBIDAS` |
"""
    with open(rc_path, mode="w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"✅ Template RC gerado com sucesso: {rc_path}")

# -------------------------------------------------------------
# 4. GERAÇÃO DO TEMPLATE DE PEDIDO DE COMPRA (PC)
# -------------------------------------------------------------
def gerar_template_pc():
    pc_path = os.path.join(OUTPUT_DIR, "TEMPLATE_PEDIDO_DE_COMPRA_PC.md")
    
    conteudo = """# 🛒 MODELO PADRÃO: PEDIDO DE COMPRA (PC / PO)
> **Origem:** Setor de Suprimentos ➔ **Destino:** Fornecedor Vencedor (c/ cópia para Almoxarifado e Financeiro)  
> **Vínculo:** Autorizado pela Diretoria conforme Mapa de Cotação Equalizado

---

### 1. IDENTIFICAÇÃO DO PEDIDO DE COMPRA

| Campo | Detalhamento |
| :--- | :--- |
| **Número do PC:** | `PC-___ / 2026` |
| **Número da RC de Origem:** | `RC-___ / 2026` |
| **Centro de Custo (CC):** | **`Ex: CC-200 (Infraestrutura) / Conta: 4.1.2.01`** |
| **Data de Emissão:** | `DD/MM/AAAA` |
| **Data Agendada para Entrega:**| **`DD/MM/AAAA`** *(Impreterível)* |
| **Comprador Responsável:** | `Nome e Contato Direto` |
| **Aprovador (Diretoria):** | `Nome do Diretor / Alçada Skill 03` |

---

### 2. DADOS DO FORNECEDOR CONTRATADO

- **Razão Social:** `________________________________________________`
- **Nome Fantasia:** `_______________________________________________`
- **CNPJ:** `__.__.___/____-__` | **Inscrição Estadual:** `____________`
- **Endereço da Empresa:** `__________________________________________`
- **Contato Comercial / Vendedor:** `________________________________`
- **Telefone / WhatsApp:** `(  ) ________-________` | **E-mail:** `____`

---

### 3. ITENS CONTRATADOS & CONDIÇÕES COMERCIAIS

| Item | Centro de Custo (CC) | Código / Descrição Detalhada do Produto | Und | Qtd Contratada | Preço Unit. (R$) | Preço Total (R$) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| 01 | `CC-___` | | | | | |
| 02 | `CC-___` | | | | | | |
| **TOTAL**| | **VALOR TOTAL DO PEDIDO DE COMPRA (FATURAMENTO BRUTO):** | | | | **R$ ____________** |

---

### 4. CONDIÇÕES FINANCEIRAS, LOGÍSTICAS E CONTRATUAIS

1. **Condição de Pagamento:** `[ ] 30 DDL Faturado` `[ ] 28 DDL` `[ ] Medição Mensal` `[ ] Outro: ________`
2. **Dados Bancários para Boleto / Depósito:** Banco: ____ | Ag: _____ | CC: _________ | Chave PIX: _________
3. **Tipo de Frete:** `[X] CIF Canteiro de Obras (Incluso no Preço)`
4. **Endereço Completo de Entrega:**  
   Terminal Multiuso TMULT (Porto do Açu), Estrada RJ-240, km 22, Canteiro Edifício Administrativo, São João da Barra / RJ.
5. **Instruções Obrigatórias de Faturamento (Nota Fiscal):**  
   ⚠️ *A Nota Fiscal Eletrônica (NF-e) deve constar OBRIGATORIAMENTE no campo Dados Adicionais / Informações Complementares:*  
   **`"Material destinado à OBRA_TMULT - Centro de Custo: [INSERIR CC AQUI] - Pedido de Compra PC-___/2026"`**.  
   *Notas fiscais sem a indicação do Pedido de Compra e do Centro de Custo NÃO serão aceitas nem liberadas para pagamento pelo financeiro.*
6. **Penalidades por Atraso:**  
   Multa moratória de 0,5% por dia útil de atraso injustificado sobre o valor total do pedido, dedutível na duplicata/faturamento.

---

### 5. ASSINATURAS E CIÊNCIA

| Pela Construtora (Diretoria / Suprimentos) | Pelo Fornecedor Contratado (Aceite Comercial) |
| :---: | :---: |
| __________________________________________ | __________________________________________ |
| Nome / Cargo / Data | Nome do Representante Legal / Data |
"""
    with open(pc_path, mode="w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"✅ Template PC gerado com sucesso: {pc_path}")

# -------------------------------------------------------------
# EXECUÇÃO PRINCIPAL
# -------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Gerando Tracker de Suprimentos & Templates de RC e PC...")
    gerar_csv_tracker()
    gerar_md_tracker()
    gerar_template_rc()
    gerar_template_pc()
    print("🎯 Pipeline de Suprimentos implantado com 100% de sucesso!")
