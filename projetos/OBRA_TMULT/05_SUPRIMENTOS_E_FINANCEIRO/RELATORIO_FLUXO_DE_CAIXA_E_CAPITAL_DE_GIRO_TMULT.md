# 💰 Relatório Executivo de Fluxo de Caixa, Curva de Desembolso e Capital de Giro

**Empreendimento:** Edifício Administrativo do Terminal Multiuso (Porto do Açu) — `OBRA_TMULT`
**Área Construída Útil:** 368,40 m² | **Prazo Contratual:** 6 Meses (180 Dias Corridos / 26 Semanas)
**Preço Global Turnkey Contratado:** R$ 1.660.762,28 | **Custo Direto Total:** R$ 1.314.562,67
**Data de Emissão:** 10/09/2026 | **Fase:** Linha de Base 01 (Baseline 01)

---

## 1. Portão de Qualidade de Dados e Nível de Confiança

Em conformidade com a `SKILL_GESTAO_09` (Seção 1) e a `SKILL_GESTAO_07` (Hierarquia de Confiança), declara-se a confiabilidade dos parâmetros de entrada utilizados:

| Parâmetro Financeiro | Fonte / Documento Origem | Nível de Confiança | Observação / Governança |
|---|---|:---:|---|
| **Cronograma Físico-Financeiro** | `CRONOGRAMA_FISICO_FINANCEIRO_TMULT.csv` | 🟢 Alto | 158 itens distribuídos por cálculo CPM de 31 atividades. |
| **Custos Diretos e BDI** | Base Oficial SINAPI SP 07/2026 (`apoio/sinapi_sp/`) | 🟢 Alto | 100% auditado com Códigos CIA e BDI analítico (27,17% / 15,00%). |
| **Retenção Técnica Contratual** | Cláusula 5ª da Proposta Comercial Turnkey | 🟢 Alto | Retenção padrão de 5% sobre faturamento de medição. |
| **Prazos de Recebimento de Medições** | Cláusula 4ª da Proposta Comercial Turnkey | 🟢 Alto | Medição no último dia útil; pagamento em D+15 após NF. |
| **Prazos Comerciais de Fornecedores** | Padrão Comercial da Construção Civil / Curva ABC | 🟢 Alto | Mão de obra no mês; Materiais: 20% à vista e 80% D+30. |
| **Alíquotas Tributárias** | Composição do BDI (Tributos Municipais e Federais) | 🟢 Alto | 8,65% s/ NF (ISS 3%, PIS 0,65%, COFINS 3%, CPRB 2%). |

---

## 2. Resumo Executivo dos Indicadores Financeiros

| Indicador Econômico-Financeiro | Valor Consolidado (R$) | % da Receita Bruta | Impacto / Significado Operacional |
|---|:---:|:---:|---|
| **Faturamento Bruto da Obra (Turnkey)** | **R$ 1.660.762,28** | 100,00% | Preço global contratado fechado (R$ 4.508,04/m² útil). |
| **Retenção Contratual de Garantia (5,0%)** | **R$ 83.038,11** | 5,00% | Retido nas medições M1 a M6; liberado integralmente no Mês 7 (TRD). |
| **Faturamento Líquido de Medições (95%)** | **R$ 1.577.724,17** | 95,00% | Volume financeiro disponível durante o transcorrer da obra civil. |
| **Custo Direto Total da Obra** | **R$ 1.314.562,67** | 79,15% | Custo de execução física (R$ 948k) + Canteiro/Gestão EAP 1.0 (R$ 366k). |
| **Tributos sobre Faturamento (8,65% s/ NF)** | **R$ 143.655,92** | 8,65% | Recolhimento mensal no dia 20 subsequente à emissão de cada nota fiscal. |
| **Administração Central, Seguros e Riscos** | **R$ 98.592,18** | 5,94% | Rateio dos custos indiretos centrais e apólices de seguro da construtora. |
| **LUCRO LÍQUIDO OPERACIONAL REALIZADO** | **R$ 103.951,57** | **6,26%** | Margem líquida real de lucro após todos os tributos e despesas quitados. |
| **NECESSIDADE MÍNIMA DE CAPITAL DE GIRO** | **R$ 180.593,13** | **10,87%** | **Máxima exposição financeira de caixa (atingida no Mês 3).** |
| **Ponto de Equilíbrio do Caixa (Break-even)** | **Mês 7** | — | Ponto em que o caixa torna-se definitivamente superavitário. |

---

## 3. Diagnóstico do Capital de Giro e Timing de Desembolso

> 💡 **A Regra de Ouro do PMO:** *Estar dentro do orçamento não significa ter liquidez no momento certo.* O descasamento temporal entre os pagamentos a fornecedores/folha e o recebimento das medições é a principal causa de mortalidade de empresas de construção.

No cenário realista da `OBRA_TMULT`, a construtora experimenta sua **máxima exposição financeira no Mês 3**, atingindo um saldo acumulado negativo de **-R$ 180.593,13**:

1. **Mês 1 (Mobilização e Fundações):** A construtora mobiliza 14 operários, aluga 4 containers habitáveis e adquire aço, madeira e concreto para as sapatas e baldrames. Desembolso de **R$ 105.458,24** sem qualquer receita (já que a 1ª medição física é aferida no final de M1 e paga em M2). Saldo M1: **-R$ 105.458,24**.
2. **Mês 2 (Superestrutura):** Entra a 1ª medição líquida (R$ 155.269,92). No entanto, ocorrem os desembolsos de formas e concreto da supraestrutura + faturas a 30 dias de materiais de M1 + primeiro recolhimento de impostos. Saldo M2: **-R$ 152.369,27**.
3. **Mês 3 (Alvenaria e Cobertura — Ponto Crítico):** Coincide com o pico da Curva S (execução da cobertura sanduíche e alvenaria de blocos). O desembolso mensal atinge R$ 292.224,96 contra uma receita líquida de R$ 264.001,06, levando o saldo acumulado ao seu vale histórico: **-R$ 180.593,13**.
4. **Mês 4 em diante (Recuperação):** O recebimento da volumosa medição do Mês 3 (R$ 348.054,46) estanca a sangria, e a curva de caixa inicia sua trajetória ascendente.
5. **Mês 7 (Liquidação e Entrega):** Ocorre o recebimento da última medição (R$ 272.605,35) somado à **devolução integral da retenção técnica de 5% (R$ 83.038,11)**, totalizando uma entrada de R$ 355.643,46, quitando os tributos e contas residuais de M6 e consolidando o **Lucro Líquido Realizado de R$ 103.951,49**.

---

## 4. Demonstrativo do Fluxo de Caixa Mensal (Cenário Realista Base)

| Rubrica Financeira | Mês 1 | Mês 2 | Mês 3 | Mês 4 | Mês 5 | Mês 6 | Mês 7 | Total Consolidado (R$) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1. ENTRADAS DE CAIXA** | | | | | | | | |
| 1.1 Faturamento Bruto Previsto | R$ 163.442,02 | R$ 277.895,85 | R$ 366.373,12 | R$ 245.681,39 | R$ 320.416,90 | R$ 286.953,00 | R$ 0,00 | **R$ 1.660.762,28** |
| 1.2 Retenção Contratual (5,0%) | R$ 8.172,10 | R$ 13.894,79 | R$ 18.318,66 | R$ 12.284,07 | R$ 16.020,84 | R$ 14.347,65 | R$ 0,00 | **R$ 83.038,11** |
| 1.3 Faturamento Líquido (95%) | R$ 155.269,92 | R$ 264.001,06 | R$ 348.054,46 | R$ 233.397,32 | R$ 304.396,06 | R$ 272.605,35 | R$ 0,00 | **R$ 1.577.724,17** |
| 1.4 Recebimento Efetivo (D+15) | R$ 0,00 | R$ 155.269,92 | R$ 264.001,06 | R$ 348.054,46 | R$ 233.397,32 | R$ 304.396,06 | R$ 272.605,35 | **R$ 1.577.724,17** |
| 1.5 Devolução da Retenção (M7) | R$ 0,00 | R$ 0,00 | R$ 0,00 | R$ 0,00 | R$ 0,00 | R$ 0,00 | R$ 83.038,11 | **R$ 83.038,11** |
| **TOTAL ENTRADAS (A)** | R$ 0,00 | R$ 155.269,92 | R$ 264.001,06 | R$ 348.054,46 | R$ 233.397,32 | R$ 304.396,06 | R$ 355.643,46 | **R$ 1.660.762,28** |
| **2. SAÍDAS DE CAIXA** | | | | | | | | |
| 2.1 Equipe Gestão (Eng/Mestre/TST) | R$ 29.300,00 | R$ 29.300,00 | R$ 29.300,00 | R$ 29.300,00 | R$ 29.300,00 | R$ 29.300,00 | R$ 0,00 | **R$ 175.800,00** |
| 2.2 Vivência e Alimentação (16 op.) | R$ 23.009,33 | R$ 23.009,33 | R$ 23.009,33 | R$ 23.009,33 | R$ 23.009,33 | R$ 23.009,33 | R$ 0,00 | **R$ 138.055,98** |
| 2.3 Mão de Obra de Campo (Físico) | R$ 23.588,70 | R$ 55.068,46 | R$ 79.403,54 | R$ 46.208,08 | R$ 67.467,21 | R$ 60.171,36 | R$ 0,00 | **R$ 331.907,35** |
| 2.4 Materiais (À Vista no Pedido) | R$ 8.761,52 | R$ 20.454,00 | R$ 29.492,74 | R$ 17.163,00 | R$ 25.059,25 | R$ 22.349,36 | R$ 0,00 | **R$ 123.279,87** |
| 2.5 Materiais (A Prazo D+30) | R$ 0,00 | R$ 35.046,06 | R$ 81.815,99 | R$ 117.970,97 | R$ 68.652,02 | R$ 100.237,01 | R$ 89.397,44 | **R$ 493.119,49** |
| 2.6 Containers NR-18 e Sanitários | R$ 3.191,66 | R$ 6.383,32 | R$ 6.383,32 | R$ 6.383,32 | R$ 6.383,32 | R$ 6.383,32 | R$ 3.191,66 | **R$ 38.299,92** |
| 2.7 Consumo Canteiro (Água/Luz/Net) | R$ 1.175,00 | R$ 2.350,00 | R$ 2.350,00 | R$ 2.350,00 | R$ 2.350,00 | R$ 2.350,00 | R$ 1.175,00 | **R$ 14.100,00** |
| 2.8 Tributos s/ Faturamento (8,65%) | R$ 0,00 | R$ 14.137,73 | R$ 24.037,99 | R$ 31.691,27 | R$ 21.251,44 | R$ 27.716,06 | R$ 24.821,43 | **R$ 143.655,92** |
| 2.9 Custos Indiretos Centrais BDI | R$ 16.432,03 | R$ 16.432,03 | R$ 16.432,03 | R$ 16.432,03 | R$ 16.432,03 | R$ 16.432,03 | R$ 0,00 | **R$ 98.592,18** |
| **TOTAL SAÍDAS (B)** | R$ 105.458,24 | R$ 202.180,93 | R$ 292.224,94 | R$ 290.508,00 | R$ 259.904,60 | R$ 287.948,47 | R$ 118.585,53 | **R$ 1.556.810,71** |
| **3. SALDO E RESULTADO** | | | | | | | | |
| **3.1 Saldo Operacional Líquido** | -R$ 105.458,24 | -R$ 46.911,01 | -R$ 28.223,88 | R$ 57.546,46 | -R$ 26.507,28 | R$ 16.447,59 | R$ 237.057,93 | **R$ 103.951,57** |
| **3.2 Saldo de Caixa Acumulado** | -R$ 105.458,24 | -R$ 152.369,25 | -R$ 180.593,13 | -R$ 123.046,67 | -R$ 149.553,95 | -R$ 133.106,36 | R$ 103.951,57 | **R$ 103.951,57** |

---

## 5. Análise de Sensibilidade — Comparativo em 3 Cenários

Seguindo a diretriz obrigatória da `SKILL_GESTAO_07` de nunca apresentar projeções em número único, projetamos 3 cenários operacionais:

| Mês | Cenário Otimista (c/ Adiantamento 10%) | Cenário Realista (Base Contratual) | Cenário Estresse (Atraso Medição 30d) |
|:---:|:---:|:---:|:---:|
| Mês 1 | R$ 60.617,99 | -R$ 105.458,24 | -R$ 105.458,24 |
| Mês 2 | -R$ 27.812,08 | -R$ 152.369,25 | -R$ 307.639,17 |
| Mês 3 | -R$ 97.555,02 | -R$ 180.593,13 | -R$ 444.594,19 |
| Mês 4 | -R$ 81.527,62 | -R$ 123.046,67 | -R$ 471.101,13 |
| Mês 5 | -R$ 149.553,96 | -R$ 149.553,95 | -R$ 382.951,27 |
| Mês 6 | -R$ 133.106,37 | -R$ 133.106,36 | -R$ 437.502,42 |
| Mês 7 | R$ 103.951,56 | R$ 103.951,57 | -R$ 251.691,89 |
| Mês 8 | — | — | R$ 103.951,57 |
| **PICO MÁXIMO DE EXPOSIÇÃO** | **-R$ 149.553,96** | **-R$ 180.593,13** | **-R$ 471.101,13** |
| **Saldo Final Realizado** | **R$ 103.951,57** | **R$ 103.951,57** | **R$ 103.951,57** |

### 🔍 Insights dos Cenários:
- **No Cenário Otimista:** A negociação de um **Adiantamento Contratual de Mobilização de 10% (R$ 166.076,23)** no Dia Zero (amortizado em 4 parcelas nas primeiras medições) mantém o caixa positivo em +R$ 60.617,99 logo no primeiro mês, mitigando significativamente o risco inicial da construtora.
- **No Cenário Realista:** A construtora precisa ter assegurada uma linha de liquidez / capital de giro de **R$ 180.593,16** (recomendando-se um fundo de contingência de **R$ 200.000,00** para cobrir flutuações pontuais).
- **No Cenário de Estresse (Atraso de Medição):** Se o cliente atrasar a liberação de cada medição em 30 dias (pagamento em D+45 em vez de D+15), a exposição máxima salta para **-R$ 471.101,13 (no Mês 4)**. Isso demonstra cabalmente o risco de descasamento e justifica as cláusulas de proteção e multas moratórias incluídas na Proposta Comercial.

---

## 6. Recomendações Estratégicas do Engenheiro Chefe / PMO
1. **Constituição de Fundo de Capital de Giro de R$ 200.000,00:** Provisionar o aporte inicial antes do início das escavações para suportar o ciclo financeiro até o recebimento da 3ª medição.
2. **Negociação Comercial de Fornecedores Chave (Curva A):**
   - Telhas Termoacústicas (R$ 86k no M3): Negociar pagamento 50% em 30 dias e 50% em 60 dias da entrega da carga no Porto do Açu.
   - Climatização Split / VRF (R$ 78k no M5): Faturar direto com distribuidor em 30/60 dias.
   - Aço e Concreto Usinado: Homologar fornecedores locais com faturamento quinzenal e prazo de 28 dias.
3. **Gestão Rigorosa do Protocolo de Medição:**
   - Protocolar a Folha de Medição impreterivelmente no dia 25 de cada mês junto à fiscalização do Terminal Multiuso para garantir que a NF seja emitida no dia 01 e paga até o dia 15.
4. **Devolução da Retenção Técnica (Mês 7):**
   - Concluir o DataBook e as pranchas As-Built (EAP 5.1 e POP 18) com 15 dias de antecedência para homologar o Termo de Recebimento Definitivo (TRD) no 1º dia útil do Mês 7, destravando a devolução imediata dos **R$ 83.038,11** retidos.
