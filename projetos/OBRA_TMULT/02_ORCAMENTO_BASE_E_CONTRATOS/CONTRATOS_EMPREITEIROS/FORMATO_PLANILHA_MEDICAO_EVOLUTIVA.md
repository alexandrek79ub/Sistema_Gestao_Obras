# 📊 FORMATO OFICIAL: PLANILHA DE MEDIÇÃO EVOLUTIVA DE EMPREITEIROS

> **Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Terminal Multiuso (Porto do Açu - SJB/RJ)  
> **Padrão Normativo:** Medições Quinzenais Evolutivas (Avanço Físico-Financeiro Acumulado em 12 Ciclos)  
> **Arquivo Excel Disponível:** [`PLANILHA_MEDICAO_QUINZENAL_EMPREITEIROS.xlsx`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/02_ORCAMENTO_BASE_E_CONTRATOS/CONTRATOS_EMPREITEIROS/PLANILHA_MEDICAO_QUINZENAL_EMPREITEIROS.xlsx)

---

## 1. Estrutura Padrão de Colunas (Layout Físico-Financeiro Contínuo)

A planilha de medição evolutiva consolida o contrato e as 12 medições quinzenais numa única tabela contínua com painéis congelados (`Freeze Panes = G6`):

| Col 1 | Col 2 | Col 3 | Col 4 | Col 5 | Col 6 | Col 7 | Col 8 | Col 9 | ... | Col 18 | Col 19 | Col 20 | Col 21 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Item EAP** | **Descrição do Serviço** | **Unid** | **Qtd Contrato** | **Preço Unit.** | **Total Contrato** | **Medição 1** | **Medição 2** | **Medição 3** | `...` | **Medição 12** | **Total Acumulado** | **Saldo a Medir** | **% Avanço** |
| `1.1.1` | Texto do serviço | m³ | `Qtd` | `R$ PU` | `=D*E` | `Qtd Med 1` | `Qtd Med 2` | `Qtd Med 3` | `...` | `Qtd Med 12` | `=SOMA(G:R)` | `=D-S` | `=S/D` |

---

## 2. Demonstração Prática: SUB-01 (Fundações e Estrutura - R$ 195.400,00)

Exemplo com os primeiros itens do contrato e as quantidades medidas nas quinzenas:

| Item EAP | Descrição Pormenorizada | Un | Qtd Contrato | Preço Unit. | Total Contrato | Medição 1 | Medição 2 | Medição 3 | Medição 4 | Total Acumulado | Saldo a Medir | % Concluído |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `1.1.1` | Escavação manual de cavas | m³ | 51,27 | R$ 14,28 | R$ 732,14 | **51,27** | 0,00 | 0,00 | 0,00 | **51,27** | 0,00 | 100,00% |
| `1.1.2` | Apiloamento fundo de cavas | m² | 60,74 | R$ 8,65 | R$ 525,40 | **60,74** | 0,00 | 0,00 | 0,00 | **60,74** | 0,00 | 100,00% |
| `1.1.5` | Fôrmas compensadas sapatas | m² | 35,88 | R$ 55,00 | R$ 1.973,40 | **35,88** | 0,00 | 0,00 | 0,00 | **35,88** | 0,00 | 100,00% |
| `1.1.7` | Fôrmas arranques pilares | m² | 25,76 | R$ 65,00 | R$ 1.674,40 | **25,76** | 0,00 | 0,00 | 0,00 | **25,76** | 0,00 | 100,00% |
| `1.1.9` | Fôrmas vigas baldrames | m² | 112,35 | R$ 55,00 | R$ 6.179,25 | **56,17** | **56,18** | 0,00 | 0,00 | **112,35** | 0,00 | 100,00% |
| `1.1.10` | Armação aço CA-50 sapatas | kg | 256,00 | R$ 4,50 | R$ 1.152,00 | **256,00** | 0,00 | 0,00 | 0,00 | **256,00** | 0,00 | 100,00% |
| `1.1.11` | Armação arranques pilares | kg | 145,70 | R$ 4,50 | R$ 655,65 | **145,70** | 0,00 | 0,00 | 0,00 | **145,70** | 0,00 | 100,00% |
| `1.1.12` | Armação vigas baldrames | kg | 1.077,30 | R$ 4,50 | R$ 4.847,85 | **538,65** | **538,65** | 0,00 | 0,00 | **1.077,30** | 0,00 | 100,00% |
| `1.1.13` | Impermeabilização baldrames | m² | 183,36 | R$ 18,00 | R$ 3.300,48 | 0,00 | **91,68** | **91,68** | 0,00 | **183,36** | 0,00 | 100,00% |
| `...` | *Demais itens estruturais...* | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

---

## 3. Rodapé de Fechamento Automático de Cada Medição

Embaixo de **CADA coluna de medição** (Medição 1 a 12), a planilha calcula dinamicamente os totalizadores financeiros da quinzena:

| Linha de Fechamento por Quinzena | Fórmula no Excel | Medição 1 (Q01) | Medição 2 (Q02) | Medição 3 (Q03) | Medição 4 (Q04) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **TOTAL BRUTO MEDIDO NO MÊS/QUINZENA:** | `=SUMPRODUCT($E$6:$E$22, Col$6:Col$22)` | **R$ 9.370,82** | **R$ 7.164,06** | **R$ 38.647,07** | **R$ 140.218,05** |
| **TOTAL ACUMULADO ATÉ A MEDIÇÃO:** | `=SUM(G$23:Col$23)` | **R$ 9.370,82** | **R$ 16.534,88** | **R$ 55.181,95** | **R$ 195.400,00** |
| **SALDO REMANESCENTE DO CONTRATO:** | `=$F$23 - Col$24` | **R$ 186.029,18** | **R$ 178.865,12** | **R$ 140.218,05** | **R$ 0,00** |
| **% AVANÇO ACUMULADO NO CONTRATO:** | `=Col$24 / $F$23` | **4,80%** | **8,46%** | **28,24%** | **100,00%** |
| **(-) RETENÇÃO TÉCNICA DE GARANTIA (5%):** | `=Col$23 * 0,05` | **- R$ 468,54** | **- R$ 358,20** | **- R$ 1.932,35** | **- R$ 7.010,90** |
| **(=) VALOR LÍQUIDO A LIBERAR NA NF-e:** | `=Col$23 - Col$27` | **R$ 8.902,28** | **R$ 6.805,86** | **R$ 36.714,72** | **R$ 133.207,15** |

---

## 4. Estrutura de Abas da Pasta de Trabalho Excel

O arquivo [`PLANILHA_MEDICAO_QUINZENAL_EMPREITEIROS.xlsx`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/02_ORCAMENTO_BASE_E_CONTRATOS/CONTRATOS_EMPREITEIROS/PLANILHA_MEDICAO_QUINZENAL_EMPREITEIROS.xlsx) conta com 9 abas integradas:

1. **`Painel Geral 12 Medições`**: Dashboard Master com os 8 empreiteiros consolidados, valor total do contrato (R$ 564.700,00), valores medidos em cada quinzena, saldo a pagar e retenção técnica acumulada;
2. **`SUB-01 Estrutura`**: 17 itens de fundações e estrutura de concreto (R$ 195.400,00);
3. **`SUB-02 Alvenaria`**: 6 itens de alvenaria em blocos e rebocos projetados (R$ 138.600,00);
4. **`SUB-03 Cobertura`**: 5 itens de estrutura metálica e telhas PIR (R$ 42.500,00);
5. **`SUB-04 Pisos`**: 5 itens de contrapiso, porcelanatos e rodapés (R$ 36.800,00);
6. **`SUB-05 Eletrica`**: 7 itens de eletrodutos, fiação, quadros QDG e luminárias (R$ 48.200,00);
7. **`SUB-06 Hidraulica`**: 6 itens de água fria, esgoto, caixas e louças (R$ 38.900,00);
8. **`SUB-07 Climatizacao`**: 5 itens de tubulações frigorígenas e aparelhos HVAC (R$ 24.800,00);
9. **`SUB-08 Pintura`**: 5 itens de selador, massa corrida e látex acrílico (R$ 39.500,00).

---

## 5. Principais Diferenciais de Governança

- **Congelamento Inteligente:** As colunas 1 a 6 (Item, Descrição, Unidade, Qtd, PU e Total Contrato) ficam fixas na tela enquanto você rola horizontalmente pelas 12 medições;
- **Cálculo Preciso por SOMARPRODUTO:** A medição física (m³, m², kg, un) é digitada na coluna da quinzena e o Excel calcula o valor em R$ automaticamente;
- **Travamento de Saldo:** Impede faturamento superior a 100% da quantidade contratada;
- **Retenção Técnica 5% Automática:** Garante a provisão da caução contratual para liberação após o Termo de Recebimento Definitivo.