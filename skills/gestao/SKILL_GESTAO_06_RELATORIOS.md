# 📊 SKILL GESTÃO 06: Relatórios Gerenciais e Dashboard Preditivo

Este módulo dita as regras de como a Inteligência Artificial e a Diretoria devem compilar, cruzar e apresentar o *Status Report* (Relatório de Saúde da Obra). O foco aqui não é mostrar dados puros, mas sim gerar **Inteligência Acionável (Action Plans)**.

## 1. Fontes de Alimentação (Onde buscar os dados)
Para gerar o Relatório Gerencial em tempo real, o sistema DEVE cruzar informações das seguintes pastas do Dossiê da Obra (`/projetos/[NOME_DA_OBRA]/`):

*   **A Referência (Baseline):**
    *   📂 `02_ORCAMENTO_BASE_E_CONTRATOS/` -> Orçamento fechado (Custo Esperado - PV/BCWS).
    *   📂 `03_PLANEJAMENTO_E_CRONOGRAMA/` -> Cronograma Mestre (Prazo Esperado).
*   **A Realidade (O Campo):**
    *   📂 `04_PRODUCAO_E_AVANCO/` -> RDO e Planilhas de Avanço Físico (Volume Realizado - EV/BCWP).
    *   📂 `05_SUPRIMENTOS_E_FINANCEIRO/` -> Fluxo de Caixa / NFs (Custo Real - AC/ACWP).
    *   📂 `06_SST_E_RH/` -> Efetivo/Headcount diário (Horas-Homem reais).

## 2. Métricas Inegociáveis (KPIs)
O relatório deve obrigatoriamente calcular e exibir a saúde da obra através da Gestão de Valor Agregado (EVM - *Earned Value Management*):

*   **SPI (Índice de Prazo):** Avanço Físico Realizado / Avanço Físico Planejado.
    *   *SPI = 1.0 (No Prazo) | SPI > 1.0 (Adiantado) | SPI < 1.0 (Atrasado)*
*   **CPI (Índice de Custo):** Orçamento Base do que foi feito / Custo Real do que foi feito.
    *   *CPI = 1.0 (No Orçamento) | CPI > 1.0 (Economia) | CPI < 1.0 (Estouro de Verba)*
*   **Produtividade (Índice Humano):** Produção Diária (ex: m²) / Efetivo Alocado (ex: 5 pedreiros).

## 3. Estrutura Padrão do Relatório Gerencial
Todo relatório gerencial gerado pela IA ou pelo Coordenador deve seguir a estrutura de leitura executiva abaixo:

### 🚦 A. Farol da Obra (Executive Summary)
- [🟢/🟡/🔴] **PRAZO:** (Ex: Atraso de 4 dias no caminho crítico).
- [🟢/🟡/🔴] **CUSTO:** (Ex: Estouro de 5% no orçamento de concreto).
- [🟢/🟡/🔴] **QUALIDADE:** (Ex: 100% das FVS assinadas).

### 📈 B. Curva S e Previsões (Machine Learning)
- Projeção de Término (EAC - *Estimate at Completion*): Baseado no ritmo atual das últimas 2 semanas, quando a obra vai acabar de fato?
- Projeção de Custo Final: Baseado nas NFs já pagas, qual será o custo total da obra?

### 🎯 C. O Plano de Ação Autônomo (O Obrigatório)
Se o Farol de Prazo ou Custo estiver Amarelo ou Vermelho, a IA DEVE sugerir um Plano de Ação para recuperar a Baseline. 
O Plano deve envolver:
1.  **Ação Logística:** (Ex: "Comprar argamassa ensacada para ganhar tempo de mistura").
2.  **Ação de RH:** (Ex: "Fazer hora extra no sábado ou contratar +2 gesseiros").
3.  **Custo da Ação:** (Qual será o impacto financeiro de adotar a solução proposta?).

---
*Regra de Ouro: Um relatório gerencial sem Plano de Ação é apenas um atestado de falha. A IA sempre deve entregar o diagnóstico junto com o remédio.*
