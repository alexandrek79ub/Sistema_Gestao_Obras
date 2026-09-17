# 🏛️ SKILL MÓDULO 01: Fundações

> **Dependência:** Carregar sempre com [SKILL_QUANTIFICACAO_MASTER.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANTIFICACAO_MASTER.md)  
> **Normas:** NBR 6118 (Projeto de estruturas de concreto), NBR 6122 (Projeto e execução de fundações), NBR 14931 (Execução de estruturas de concreto)  
> **Fck mínimo para fundações:** C30 (solo com agressividade II-III conforme NBR 6118)

---

## 🧭 Escopo deste Módulo

Cobre o **levantamento quantitativo físico e geométrico de todos os elementos de fundação** de uma edificação:

- **Fundações diretas:** Sapatas isoladas, associadas e corridas;
- **Fundações profundas:** Estacas pré-moldadas, estacas raiz, trado mecânico, hélice contínua;
- **Blocos de coroamento** sobre estacas;
- **Vigas baldrame** e cintas de fundação;
- **Radier** (fundação em laje maciça ou nervurada);
- **Concreto de regularização** (lastro magro) e lastro de brita;
- **Movimento de terra:** Escavação de cavas/valas, reaterro compactado e terra excedente.

---

## 🚨 DIRETRIZES FUNDAMENTAIS DO LEVANTAMENTO (INVIOLÁVEIS)

### 1. HÍBRIDA NEURO-SIMBÓLICA - ZERO CÁLCULO PELA IA
- **É ESTRITAMENTE PROIBIDO realizar cálculos numéricos geométricos ou tentar resolver expressões matemáticas "de cabeça"**.
- A IA atua **apenas como orquestradora**. Para obter quantidades e aplicar as fórmulas abaixo, **VOCÊ DEVE DELEGAR** a extração ao script determinístico localizado em `scripts/motor_quantitativos/importadores/roteador.py`.
- O Motor Quantitativo possui embarcado o `ParserFundacoes` (em `scripts/motor_quantitativos/importadores/disciplinas/parser_fundacoes.py`), que executará matematicamente as fórmulas que estão documentadas nesta skill. As fórmulas abaixo servem apenas como **Base de Conhecimento e Manual de Engenharia**.

### 2. Proibição de Inserção de Insumos na Skill de Quantitativo
- O papel do Levantamento Quantitativo de Engenharia (Take-off) é apurar estritamente os **Serviços Executivos e Elementos Físicos de Projeto** (ex: Concreto $m^3$, Fôrma $m^2$, Aço $kg$, Escavação $m^3$, Impermeabilização $m^2$).
- **É expressamente PROIBIDO explodir ou calcular insumos miúdos derivados** (arames recozidos, pregos, sarrafos, desmoldantes, espaçadores, fitas, rolos ou trinchas) dentro das memórias de cálculo ou tabelas de quantitativo.
- **Motivo técnico:** As Composições de Preço Unitário (CPUs oficiais como SINAPI e TCPO) **já contêm esses insumos e seus coeficientes de consumo embutidos no custo unitário do serviço**. Inserir esses insumos no quantitativo físico causa **dupla contagem** e infla indevidamente o custo da obra.

### 2. Proibição de Aplicação de Taxas de Perdas ou Fatores de Empolamento
- Todas as quantidades devem ser apuradas em sua **Geometria Líquida Real de Projeto** ($100\%$ nominal conforme as pranchas).
- **É expressamente PROIBIDO aplicar percentuais de perdas** (ex: $5\%$ de concreto, $10\%$ de aço, perdas de madeira) ou coeficientes empíricos de empolamento de solo no quantitativo de projeto.
- **Motivo técnico:** Os coeficientes de perda de materiais pertencem à elaboração das composições de preço e ao planejamento de compras/suprimentos, e não à medição física dos projetos de engenharia.

---

## 📐 1. Matriz de Serviços de Infraestrutura (Geometria Líquida)

Para cada elemento de fundação detalhado em projeto, apuram-se os seguintes serviços de engenharia:

| ID | Serviço de Infraestrutura | Unid. | Regra de Medição Geométrica Líquida |
|:---:|:---|:---:|:---|
| **01** | Locação da Obra e Gabarito | un / m² | Área de projeção da edificação ou unidades locadas conforme planta de locação |
| **02** | Perfuração / Cravação de Estacas | m / un | Comprimento nominal em projeto ($H_{estaca} = \text{Cota Topo} - \text{Cota Apoio}$) ou unidades cravadas |
| **03** | Arrasamento / Descabeçamento | un | Quantidade exata de estacas de projeto a descabeçar até a cota de arrasamento |
| **04** | Escavação de Cavas e Valas | m³ | Volume geométrico da cava: $(b + 2 \times \text{folga}) \times (L + 2 \times \text{folga}) \times h_{escav}$ (folga de 10cm por lado para fôrma) |
| **05** | Apiloamento de Fundo de Vala | m² | Área geométrica da base da cava escavada: $(b + 2 \times \text{folga}) \times (L + 2 \times \text{folga})$ |
| **06** | Lastro de Concreto Magro / Regularização | m³ | Área da base da cava $\times$ espessura nominal de projeto (ex: $e = 0,05\text{m}$) |
| **07** | Fôrma de Madeira / Compensado | m² | Área líquida de contato vertical da peça: Perímetro de contato lateral $\times$ altura da peça |
| **08** | Concreto Estrutural de Fundação | m³ | Volume geométrico nominal da peça (sapatas, blocos, baldrames, fuste de estacas, radier) |
| **09** | Armadura de Fundação (Aço CA-50/60) | kg | **Extraído 100% dos Resumos e Tabelas de Ferro das Pranchas Estruturais** (peso líquido por bitola) |
| **10** | Impermeabilização com Tinta/Manta Asfáltica | m² | Área real de contato com o solo: Topo + faces laterais (descontando encostos e nós de pilaretes) |
| **11** | Drenagem Perimetral de Fundações | m | Extensão linear de dreno executado conforme projeto específico |
| **12** | Reaterro Compactado de Valas | m³ | Volume líquido geométrico: $V_{escavado} - V_{concreto\_enterrado} - V_{lastro}$ |
| **13** | Terra Excedente de Escavação | m³ | Volume geométrico de corte não aproveitado no reaterro: $V_{escavado} - V_{reaterro}$ |

---

## 📋 1.2 Tabela Oficial de Serviços para EAP (Nível 1.3 — Fundações)

> 🛑 **REGRA DE SEGREGAÇÃO:** A EAP e o cronograma contêm exclusivamente **serviços executivos de engenharia**, mensuráveis por avanço físico em campo.

| Código EAP | Pacote de Trabalho / Serviço | Unidade | Predecessora Imediata | Critério de Medição Física |
|:---:|:---|:---:|:---:|:---|
| **1.3.1** | Locação da Obra e Gabarito Topográfico | un / m² | 1.1.2 Mobilização | Área total locada e eixos marcados em gabarito |
| **1.3.2** | Perfuração / Cravação de Estacas | m / un | 1.3.1 Locação | Metros lineares perfurados ou estacas cravadas |
| **1.3.3** | Arrasamento e Descabeçamento de Estacas | un | 1.3.2 Estacas (após cura) | Unidades de estacas descabeçadas e limpas |
| **1.3.4** | Escavação Mecanizada / Manual de Valas e Cavas | m³ | 1.3.1 Locação | Volume geométrico escavado no corte do terreno |
| **1.3.5** | Apiloamento de Fundo da Cava | m² | 1.3.4 Escavação | Área de fundo de cava compactada |
| **1.3.6** | Lastro de Concreto Magro ou Brita Drenante | m³ | 1.3.5 Apiloamento | Volume nominal do lastro executado |
| **1.3.7** | Fôrmas de Sapatas, Blocos e Baldrames | m² | 1.3.6 Lastro | Área real de contato lateral montada |
| **1.3.8** | Armação de Aço CA-50 / CA-60 | kg | 1.3.7 Fôrmas | Peso total de armaduras posicionadas no elemento |
| **1.3.9** | Concretagem Estrutural de Fundação | m³ | 1.3.8 Armação | Volume geométrico de concreto lançado e adensado |
| **1.3.10** | Desforma e Cura Úmida (NBR 14931) | m² | 1.3.9 Concretagem | Área desformada após período normativo de cura |
| **1.3.11** | Impermeabilização de Elementos Enterrados | m² | 1.3.10 Desforma | Área líquida de superfície impermeabilizada |
| **1.3.12** | Drenagem Perimetral de Fundações | m | 1.3.10 Desforma | Metros lineares de tubo dreno e camada drenante instalada |
| **1.3.13** | Reaterro Compactado de Valas | m³ | 1.3.11 Impermeabilização | Volume geométrico de cava preenchido e compactado |
| **1.3.14** | Remoção de Terra Excedente | m³ | 1.3.13 Reaterro | Volume geométrico líquido de terra removida |

---

## ⛓️ 1.3 Sequência Executiva e Travas de Qualidade

1. **Cadeia Executiva:**
   ```text
   Locação (1.3.1) → Perfuração/Cravação (1.3.2) → Arrasamento (1.3.3) → Escavação (1.3.4) 
   → Apiloamento (1.3.5) → Lastro Magro (1.3.6) → Fôrmas (1.3.7) → Armação (1.3.8) 
   → Concretagem (1.3.9) → Cura 7 dias (1.3.10) → Desforma → Impermeabilização (1.3.11) 
   → Drenagem (1.3.12) → Reaterro (1.3.13) → Remoção de Terra (1.3.14)
   ```

2. **Portões de Bloqueio Críticos:**
   - 🛑 **Impermeabilização (1.3.11) bloqueia Reaterro (1.3.13):** Jamais reaterrar valas ou cavas antes da cura e liberação formal da impermeabilização.
   - 🛑 **Cura Conforme NBR 14931:** Concretos de fundação em contato com solo exigem período mínimo de **7 dias de cura úmida contínua** antes de receberem esforços ou reaterros precoces.
   - 🛑 **Descabeçamento de Estacas (1.3.3):** Respeitar cura mínima de 5 dias após a concretagem da estaca para evitar danos ao topo do fuste.

---

## 📐 2. Geometrias e Fórmulas de Cálculo Líquido

### 2.1 Sapatas Isoladas, Associadas e Pedestais

```text
Volume de Concreto da Sapata:
V_sapata = b × L × h_sapata

Volume do Pedestal / Arranque:
V_ped = b_ped × h_ped × H_ped

Volume Total de Concreto:
V_total = V_sapata + V_ped

Área de Fôrma:
A_forma_sapata = 2 × (b + L) × h_sapata
A_forma_ped = 2 × (b_ped + h_ped) × H_ped
(Faces laterais verticais — fundo apoia no lastro de concreto magro)
```

### 2.2 Bloco de Coroamento sobre 3 Estacas (Seção Poligonal / Trapezoidal)

```text
Área da Seção em Planta:
A_seção = [(L1 + L2) × H1 / 2] + [(L2 + L3) × H2 / 2]

Volume de Concreto:
V_bloco = A_seção × H_bloco × Quantidade

Área de Fôrma:
A_forma = Perímetro_externo_poligonal × H_bloco
```

### 2.3 Vigas Baldrame / Cintas de Fundação

> 🛑 **REGRA DO NÓ (Desconto de Apoios):**  
> As vigas baldrames devem ser quantificadas em seus **vãos livres** (face a face de apoios/pilaretes), garantindo zero sobreposição de concreto, fôrma ou impermeabilização com os pilaretes já levantados.

```text
Dimensões: b (largura), h (altura), L_vao_livre (comprimento líquido), Quantidade

Volume de Concreto:
V_baldrame = b × h × L_vao_livre × Quantidade

Área de Fôrma (2 laterais, sem fundo se apoiada em lastro):
A_forma = (2 × h) × L_vao_livre × Quantidade

Área de Impermeabilização (Face superior + 2 laterais):
A_impermeab = (b + 2 × h) × L_vao_livre × Quantidade
```

### 2.4 Estacas e Brocas

```text
Comprimento Útil:
H_estaca = Cota_Apoio − Cota_Topo_Arrasamento

Volume de Concreto do Fuste:
V_estaca = π × (Ø / 2)² × H_estaca × Quantidade

Volume de Escavação / Perfuração:
V_escav_estaca = V_estaca
```

### 2.5 Radier (Fundação em Laje)

```text
Volume de Concreto da Laje:
V_radier = Área_projetada × espessura_radier

Volume de Nervuras / Vigas Invertidas (se houver):
V_nervuras = Σ (b_nervura × h_nervura × L_nervura)

Área de Fôrma de Borda:
A_forma = Perímetro_externo × espessura_radier
```

---

## 🔩 3. Armadura de Fundações (Aço CA-50 e CA-60)

### Regra de Ouro da Armadura de Projeto
- O quantitativo de aço de fundações **DEVE ser extraído diretamente das tabelas de ferro e resumos de aço das pranchas executivas de engenharia** (peso em kg segregado por diâmetro e tipo: CA-50 ou CA-60).
- **PROIBIDO calcular arame recozido ou perdas:** Arame e perdas de ponta de aço são insumos e coeficientes pertencentes às composições de custo e suprimentos, não ao levantamento de projeto.
- **Se a prancha não contiver resumo de ferro:** É dever do agente emitir **RFI formal** solicitando o detalhamento ou resumo do calculista. Nunca inventar ou estimar pesos de armação sem respaldar em prancha.

---

## 🏗️ 4. Movimento de Terra (Escavação, Reaterro e Bota-fora)

Todas as movimentações de terra no levantamento são apuradas pelo seu **Volume Geométrico Líquido no Corte**:

### 4.1 Escavação de Cavas e Valas
```text
Cavas para Sapatas / Blocos:
V_escav = (b + 0,20m) × (L + 0,20m) × h_escav × Quantidade

Valas para Baldrame:
V_escav = (b + 0,20m) × h_escav × L_trecho × Quantidade
(Folga operacional de 0,10m de cada lado para montagem e desforma das peças)
```

### 4.2 Lastro de Concreto Magro / Regularização
```text
V_lastro = Área_base_cava × espessura_lastro (nominal em projeto, ex: 0,05m)
```

### 4.3 Reaterro Compactado de Valas
```text
V_reaterro = V_escavado − V_concreto_enterrado − V_lastro
```

### 4.4 Terra Excedente (Corte para Bota-fora)
```text
V_terra_excedente = V_escavado − V_reaterro
(Volume geométrico em corte. Fatores de empolamento pertencem à composição de transporte)
```

---

## 📦 5. Parâmetros Normativos NBR 6118 e NBR 6122

| Elemento | Fck Mínimo | Classe de Agressividade (CAA) | Cobrimento Nominal ($c_{nom}$) |
|---|:---:|:---:|:---:|
| Lastro de regularização | C10 – C15 | Não estrutural | — |
| Sapatas, Blocos e Baldrames em contato com solo | C30 | CAA II (Urbano / Solo comum) | 45 mm (solo regularizado com lastro) |
| Fundações em solo com agressividade severa | C35 – C40 | CAA III / IV (Industrial / Marinho) | 50 mm |

---

## 🌳 6. Árvore de Decisão — Levantamento de Fundações

| Pedido do Usuário | Procedimento do Agente |
|---|---|
| "Quantifique as sapatas do projeto" | Ler prancha estrutural: dimensões $b$, $L$, $h_{sapata}$, pedestal $b_{ped}$, $h_{ped}$, $H_{ped}$, e resumo de aço da prancha |
| "Quanto concreto para o radier?" | Ler prancha de fôrma: Área projetada, espessura, dimensões das nervuras e desníveis |
| "Calcule o baldrame da obra" | Ler planta de fôrma: seções $b \times h$ e comprimentos de vãos livres (descontando apoios/pilaretes) |
| "Qual o volume de escavação e reaterro?" | Calcular volume geométrico da cava com folga de 10cm, deduzindo o volume do concreto e lastro para o reaterro |
| "Qual a armadura das fundações?" | Localizar a tabela / quadro de resumo de ferro da prancha de fundação e transcrever o peso líquido por bitola |

---

## 📋 7. Modelo de Memória de Cálculo — Sapata Isolada

```
╔══════════════════════════════════════════════════════════════════╗
║        MEMÓRIA DE CÁLCULO — FUNDAÇÃO: SAPATA ISOLADA            ║
╠══════════════════════════════════════════════════════════════════╣
║  OBRA:        [Nome da Obra]         CIA: [FUN-GER-F01]          ║
║  ELEMENTO:    Sapata S-01            PILAR: P-01                 ║
║  PRANCHA REF: [Identificação da Prancha de Fundação / Rev]      ║
║  ESPECIF.:    Concreto fck = 30 MPa | Aço CA-50                  ║
╠══════════════════════════════════════════════════════════════════╣
║  1. ESCAVAÇÃO GEOMÉTRICA DA CAVA (m³):                           ║
║     Dimensões com folga: (b + 0,20) × (L + 0,20) × h_cava        ║
║     V_escav = (1,40 + 0,20) × (1,40 + 0,20) × 1,20 = 3,07 m³    ║
║                                                                  ║
║  2. APILOAMENTO DE FUNDO (m²):                                   ║
║     A_apiloamento = 1,60 × 1,60 = 2,56 m²                        ║
║                                                                  ║
║  3. LASTRO DE CONCRETO MAGRO (e = 0,05m):                        ║
║     V_lastro = 1,60 × 1,60 × 0,05 = 0,13 m³                      ║
║                                                                  ║
║  4. CONCRETO ESTRUTURAL LÍQUIDO (m³):                            ║
║     Sapata: b × L × h = 1,40 × 1,40 × 0,50 = 0,98 m³             ║
║     Pedestal: 0,30 × 0,30 × 0,65 = 0,06 m³                       ║
║     V_concreto_total = 0,98 + 0,06 = 1,04 m³                     ║
║                                                                  ║
║  5. FÔRMA VERTICAL DE CONTATO (m²):                              ║
║     Sapata: 2 × (1,40 + 1,40) × 0,50 = 2,80 m²                   ║
║     Pedestal: 2 × (0,30 + 0,30) × 0,65 = 0,78 m²                 ║
║     A_forma_total = 2,80 + 0,78 = 3,58 m²                        ║
║                                                                  ║
║  6. ARMADURA CA-50 (kg — Quadro de Ferro da Prancha):            ║
║     Malha da sapata (N1 Ø 10.0mm): 18,40 kg                      ║
║     Arranque do pilar (N2 Ø 12.5mm): 12,20 kg                    ║
║     Estribos do arranque (N3 Ø 6.3mm): 3,10 kg                   ║
║     Peso Total de Aço CA-50 = 33,70 kg                           ║
║                                                                  ║
║  7. IMPERMEABILIZAÇÃO ASFÁLTICA (m²):                            ║
║     Topo sapata + faces laterais (descontando arranque): 3,69 m² ║
║                                                                  ║
║  8. REATERRO COMPACTADO (m³):                                    ║
║     V_reaterro = 3,07 - 1,04 (concreto) - 0,13 (lastro) = 1,90 m³║
║                                                                  ║
║  9. TERRA EXCEDENTE PARA BOTA-FORA (m³):                         ║
║     V_excedente = 3,07 - 1,90 = 1,17 m³                          ║
╠══════════════════════════════════════════════════════════════════╣
║  ✅ RESUMO QUANTITATIVO NOMINAL DE PROJETO:                      ║
║     • Concreto Estrutural C30:   1,04 m³                         ║
║     • Fôrmas de Madeira:         3,58 m²                         ║
║     • Aço CA-50 Nominal:         33,70 kg                        ║
║     • Escavação Mecânica/Manual: 3,07 m³                         ║
║     • Lastro de Concreto Magro:  0,13 m³                         ║
║     • Impermeabilização:         3,69 m²                         ║
║     • Reaterro Compactado:       1,90 m³                         ║
║     • Terra Excedente:           1,17 m³                         ║
╚══════════════════════════════════════════════════════════════════╝
```
