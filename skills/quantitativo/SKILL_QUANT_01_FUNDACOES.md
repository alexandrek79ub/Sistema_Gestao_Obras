# 🏛️ SKILL MÓDULO 01: Fundações

> **Dependência:** Carregar sempre com [SKILL_QUANTIFICACAO_MASTER.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANTIFICACAO_MASTER.md)
> **Normas:** NBR 6118, NBR 6122 (Projeto e execução de fundações), NBR 14931, TCPO 14ª Ed.
> **Fck mínimo para fundações:** C30 (solo com agressividade II-III)

---

## 🧭 Escopo deste Módulo

Cobre o quantitativo de **todos os elementos de fundação** de uma edificação:

- Fundações diretas: Sapatas isoladas, sapatas associadas, sapatas corridas
- Fundações profundas: Estacas pré-moldadas, estacas raiz, estacas hélice contínua
- Blocos de coroamento (sobre estacas)
- Vigas baldrame / cintas de fundação
- Radier (fundação em laje)
- Concreto de regularização (lastro)
- Escavação e reaterro

---

## 📐 1. Matriz Consolidada de Serviços de Infraestrutura (10 Serviços Integrados)

> ⚠️ **REGRA DE OURO DA INFRAESTRUTURA:** Para CADA elemento de fundação (sapata, bloco, baldrame, estaca), o PMO Virtual DEVE derivar até **10 serviços integrados de canteiro**:

| Service ID | Serviço de Infraestrutura | Unidade | Fórmula Base de Derivação |
|---|---|---|---|
| **01** | Escavação de Cava / Vala | m³ | `(b + folga) × (L + folga) × h_escav × Quant` |
| **02** | Apiloamento do Fundo da Cava | m² | `(b + folga) × (L + folga) × Quant` (compactação da base) |
| **03** | Lastro de Concreto Magro | m³ | `A_cava × e_lastro_conc` (tipicamente e = 0,05m) |
| **04** | Lastro de Brita / Pedra Drenante | m³ | `A_cava × e_brita` (quando especificado no projeto) |
| **05** | Fôrma de Fundação | m² | Perímetro lateral da peça `× h_peça × Quant` |
| **06** | Concreto Estrutural de Fundação | m³ | Volume líquido geométrico do elemento |
| **07** | Armadura de Fundação (Aço) | kg | `V_concreto × Taxa_Aço (kg/m³)` ou detalhamento de prancha |
| **08** | Impermeabilização (Tinta Asfáltica) | m² | Face superior + faces laterais. **🛑 REGRA DO NÓ:** Descontar rigorosamente a seção exata das vigas nas faces dos pilaretes onde há encosto, evitando dupla contagem de área envelopada. |
| **09** | Reaterro Compactado | m³ | `V_escavado − V_concreto_ocupado` |
| **10** | Bota-fora / Remoção de Terra | m³ | `V_escavado − V_reaterro` (aplicar empolamento 1,25 a 1,35) |

### 🔩 1.1 Matriz de Suprimentos: Miudezas e Insumos de Apoio (Exclusivo da Lista UCC / BOM)

> 🛑 **REGRA DE OURO DA GOVERNANÇA: EAP É SERVIÇO, UCC É COMPRA!**  
> Para **NÃO POLUIR A EAP**, as miudezas e insumos de apoio **NÃO SÃO CODIFICADOS COMO ITENS DE SERVIÇO NA EAP**.  
> - **Na EAP (Cronograma e Medição):** Mantêm-se estritamente os **Pacotes de Trabalho / Serviços Executivos de Engenharia** (ex: *1.1.4 Concreto de Sapatas*, *1.1.5 Fôrma de Sapatas*, *1.1.10 Armação de Aço*). É por esses serviços que se afere o avanço físico e se paga a mão de obra/empreiteiro.  
> - **Na Lista de Compras UCC (Bill of Materials - BOM):** O Agente DEVE OBRIGATORIAMENTE explodir e quantificar todas as **Miudezas e Insumos de Canteiro** derivados de cada serviço da EAP, garantindo que o almoxarifado/compras emita as Ordens de Compra completas sem compras emergenciais ou paralisações de frente de serviço:
>
> 1. **Vinculado aos Serviços de Armação (CA-50/CA-60):**
>    - **Arame Recozido BWG 18:** 1,5% a 2,0% do peso total de aço (kg ou rolos de 1 kg).
>    - **Espaçadores / Pastilhas de Concreto (Solo 40/50mm):** 4 a 6 un/m² de fundo de sapata/bloco ou 2 a 3 un/m linear de viga baldrame (garantia de cobrimento NBR 6118 em contato com o solo).
> 2. **Vinculado aos Serviços de Fôrmas de Madeira (Compensado):**
>    - **Desmoldante para Fôrmas de Madeira:** Consumo paramétrico de 25 a 30 m²/litro sobre a área total de fôrmas (baldes/bombonas de 18L ou galões de 3,6L).
>    - **Pregos com Cabeça para Fôrmas (17×27 ou 18×30):** 0,04 a 0,05 kg por m² de fôrma de compensado (caixas de 10 kg ou pacotes de 1 kg).
>    - **Sarrafos de Travamento e Gravatas (Pinus 2,5 × 7,0 cm ou 2,5 × 10 cm):** 1,0 a 1,2 m lineares por m² de fôrma para contenção do empuxo nas vigas e sapatas (metros lineares ou dúzias de peças de 3,00m).
> 3. **Vinculado aos Serviços de Concretagem e Cura:**
>    - **Lona Plástica Preta (Polietileno e=150µ a 200µ):** Forração de fundo de vala/lastro e proteção de cura úmida contínua de 7 dias exigida pelas notas de projeto estrutural (bobinas de 4m × 50m = 200 m²).
> 4. **Vinculado aos Serviços de Impermeabilização:**
>    - **Acessórios de Pintura Asfáltica:** 1 rolo de lã de carneiro 23cm a cada 80 m² impermeabilizados + trinchas de 2" para recorte de cantos e nós.

### 📋 1.2 Tabela Oficial de Serviços para EAP e Cronograma (Nível 1.3 — Fundações)

> 🛑 **REGRA DE SEGREGAÇÃO:** Esta tabela contém **exclusivamente pacotes de trabalho e serviços executivos de engenharia**. As miudezas e insumos de apoio (pregos, arames, desmoldantes, espaçadores, fitas) NÃO recebem código EAP e pertencem à lista UCC/BOM derivada descrita na Seção 1.1 e Seção 1.4.

| Código EAP | Pacote de Trabalho | Unid. Avanço Físico | Predecessora Imediata | Insumos BOM Derivados |
|:---:|:---|:---:|:---:|:---|
| **1.3.1** | Locação da Obra e Gabarito Topográfico | un | 1.1.2 Mobilização | Estacas de madeira, arame galvanizado, cal virgem (traçado), nível laser, trena |
| **1.3.2** | Perfuração / Cravação de Estacas Pré-moldadas ou Raiz | un / m | 1.3.1 | Estacas pré-moldadas (un), graute estrutural, ponteiras de aço, nata de cimento, camisas metálicas |
| **1.3.3** | Arrasamento e Descabeçamento de Estacas | un | 1.3.2 FF+5d cura | Ponteiros, marteletes, argamassa de reconstituição de topo |
| **1.3.4** | Escavação Mecanizada / Manual de Valas e Cavas | m³ | 1.3.1 | — |
| **1.3.5** | Apiloamento de Fundo da Cava | m² | 1.3.4 | — |
| **1.3.6** | Lastro de Concreto Magro (C10/C15) ou Brita Drenante | m³ | 1.3.5 | Concreto magro C10 (m³), brita nº 1, lona plástica preta 200µ para separação |
| **1.3.7** | Fôrmas de Sapatas, Blocos e Baldrames | m² | 1.3.6 | Chapas de compensado 17mm, sarrafos de gravata pinus (m), desmoldante (L), pregos 17×27 (kg), escoras |
| **1.3.8** | Armação de Aço CA-50 / CA-60 | kg | 1.3.7 | Aço CA-50 (barras/kg), arame recozido BWG 18 (kg), espaçadores pastilha de solo 40/50mm (un) |
| **1.3.9** | Concretagem Estrutural C30 | m³ | 1.3.8 | Concreto usinado fck ≥ 30 MPa (m³), vibrador de imersão, controle tecnológico (slump/corpos de prova) |
| **1.3.10** | Desforma, Cura Úmida e Retirada de Escoramento | m² | 1.3.9 FF+3d | Lona plástica 200µ (bobinas), água de cura contínua, desmoldante de reaproveitamento |
| **1.3.11** | Impermeabilização com Emulsão/Tinta Asfáltica | m² | 1.3.10 | Emulsão/tinta asfáltica (baldes 18L), rolos de lã de carneiro 23cm, trinchas 2" |
| **1.3.12** | Drenagem Perimetral de Fundações | m | 1.3.10 | Tubo dreno corrugado perfurado DN 100mm (m), manta geotêxtil Bidim (m²), brita drenante nº 1 (m³) |
| **1.3.13** | Reaterro Compactado com Controle de Camadas | m³ | 1.3.11 | Solo selecionado para reaterro (m³), soquete compactador mecânico |
| **1.3.14** | Bota-fora de Terra Excedente | m³ | 1.3.13 | Transporte e bota-fora de terra empolada (m³) |

### ⛓️ 1.3 Sequência Lógica Construtiva e Predecessoras Críticas

1. **Cadeia Executiva Contínua:**
   ```text
   Locação (1.3.1) → Escavação (1.3.4) → Apiloamento (1.3.5) → Lastro Magro (1.3.6) → Fôrmas (1.3.7) → Armação (1.3.8) → Concretagem (1.3.9)
   → Cura 7 dias NBR 14931 (1.3.10) → Desforma → Impermeabilização (1.3.11) → Drenagem (1.3.12) → Reaterro (1.3.13) → Bota-fora (1.3.14)
   ```

2. **Predecessoras Críticas e Travas de Qualidade:**
   - 🛑 **A impermeabilização (1.3.11) é PREDECESSORA BLOQUEANTE do reaterro (1.3.13):** Jamais autorizar o reaterro de valas ou cavas sobre fundações sem a conclusão e liberação da pintura/manta asfáltica pela fiscalização de obra.
   - 🛑 **Regra NBR 14931 (Cura e Desforma):** Concretos de fundação em contato com solo agressivo (Classes de Agressividade Ambiental II a IV) exigem período mínimo de **7 dias de cura úmida contínua** (ou aplicação de membrana de cura líquida) antes da liberação de cargas ou retirada de contenções laterais críticas.
   - 🛑 **Descabeçamento de Estacas (1.3.3):** Exige no mínimo 5 dias de cura após a moldagem da estaca para evitar fissuração do fuste pelo martelete ou ponteiro.

### 🛡️ 1.4 Checklist Anti-Omissão de SKUs de Infraestrutura (12 SKUs Obrigatórios na UCC/BOM)

> Antes de emitir o relatório de quantitativo e a lista de compras da infraestrutura, o PMO Virtual DEVE auditar e certificar a presença de todos os seguintes 12 insumos consumíveis na BOM:

- [ ] **Arame Recozido BWG 18:** 1,5% a 2,0% do peso total de aço estrutural (kg).
- [ ] **Espaçadores de Solo Tipo Pastilha 40mm ou 50mm:** 4 a 6 un/m² de sapata/bloco; 2 a 3 un/m linear de viga baldrame.
- [ ] **Desmoldante para Fôrmas de Madeira:** 1 L a cada 25 a 30 m² de área de contato de fôrma (bombonas de 18L).
- [ ] **Pregos com Cabeça 17×27 ou 18×30:** 0,04 a 0,05 kg/m² de fôrma de compensado (caixas de 10 kg).
- [ ] **Sarrafos de Travamento e Gravatas Pinus 2,5×7,0cm:** 1,0 a 1,2 m lineares por m² de fôrma.
- [ ] **Lona Plástica Preta 200µ:** Forração de fundo de cava/lastro + cobertura de proteção para cura úmida (bobinas de 200 m²).
- [ ] **Emulsão Asfáltica 45% ou Tinta Asfáltica:** 1 L a cada 1,5 m² de superfície de concreto enterrada (latas de 18L).
- [ ] **Rolos de Lã de Carneiro 23cm:** 1 rolo a cada 80 m² de impermeabilização executada.
- [ ] **Trinchas de 2":** Para recortes de nós, arestas e cantos de vigas baldrames e pilaretes.
- [ ] **Tubo Dreno Corrugado Perfurado DN 100mm (Dreno-flex):** 1 metro por metro linear de baldrame periférico projetado.
- [ ] **Manta Geotêxtil Não-Tecida Bidim OP-30:** 1,20 m de largura por metro linear de dreno (envelopamento completo com transpasse de 20cm).
- [ ] **Brita Drenante Nº 1:** Volume de envelopamento da vala drenante (m³).

---

## 📐 2. Elementos de Fundação e Geometrias Especiais

### 2.1 Bloco de Coroamento sobre 3 Estacas (Seção Poligonal / Trapezoidal)

```text
Geometria da Seção Trapezoidal do Bloco de 3 Estacas:
Dimensões em planta: L1, L2, L3 (larguras) | H1, H2 (alturas dos trapézios)

Área da Seção (m²):
A_seção = [(L1 + L2) × H1 / 2] + [(L2 + L3) × H2 / 2]

Volume de Concreto (m³):
V_bloco_3estacas = A_seção × H_altura_bloco × QUANT
```

### 2.2 Viga Baldrame / Cinta com Folga de Escavação e Impermeabilização

> 🛑 **REGRA DO NÓ (Desconto de Apoios):** As vigas baldrames DEVEM ser calculadas APENAS em seus vãos livres (face a face dos pilaretes). É terminantemente proibido passar o comprimento do baldrame reto pelos apoios se os pilaretes/arranques já estão sendo levantados em sua altura total, para evitar duplicidade de concreto, fôrma e impermeabilização.

```text
1. Dimensões da Peça: LARG, ALTURA, COMP_VAO_LIVRE, QUANT
2. Folgas Operacionais de Vala: folga_larg = 0,20m, folga_alt = 0,20m

3. Serviços Derivados de Baldrame:
   - V_escavação = (LARG + 0,20m) × (ALTURA + 0,20m) × COMP_VAO_LIVRE × QUANT
   - A_apiloamento = (LARG + 0,20m) × COMP × QUANT
   - V_lastro_conc = (LARG + 0,20m) × 0,05m × COMP × QUANT
   - A_forma = (2 × ALTURA) × COMP × QUANT  (2 lados, sem fundo)
   - V_concreto = LARG × ALTURA × COMP × QUANT
   - A_impermeab = (LARG + 2 × ALTURA) × COMP × QUANT  (Topo + 2 laterais)
   - V_reaterro = V_escavação − V_concreto − V_lastro_conc
   - V_bota_fora = V_escavação − V_reaterro
```

### 2.3 Estacas e Brocas por Cotas de Apoio e Arrasamento

```text
H_estaca = Cota_Apoio − Cota_Topo_Arrasamento
V_concreto_estaca = π × (Ø / 2)² × H_estaca × QUANT
V_escavação_estaca = V_concreto_estaca
V_bota_fora_estaca = V_escavação_estaca × Fator_Empolamento (1,25)
Peso_aço_estaca = V_concreto_estaca × Taxa_Aço (kg/m³)
```

### 2.4 Sapata Isolada, Associada e Corrida

```text
V_sapata = b × L × h_sapata
V_pedestal = b_ped × h_ped × H_ped
V_total_sapata = V_sapata + V_pedestal
A_forma_sapata = 2 × (b + L) × h_sapata
```

### 2.5 Radier (Fundação em Laje)

```text
V_radier = A_projetada × e_radier
V_nervuras = Σ (b_nervura × h_nervura × L_nervura)
A_forma_radier = Perímetro_externo × e_radier
```

---

## 📏 2. Fôrmas de Fundação (m²)

### 2.1 Sapatas

```
A_forma_sapata = 2 × (b + L) × h_sapata
(faces laterais — fundo não tem fôrma, apoia no solo)
```

### 2.2 Pedestal

```
A_forma_ped = (2 × b_ped + 2 × h_ped) × H_ped
```

### 2.3 Bloco de Coroamento

```
A_forma_bloco = 2 × (b + L) × h_bloco
```

### 2.4 Viga Baldrame

```
A_forma_baldrame = (2 × h + b) × L_total
(face inferior + 2 faces laterais)
```
> Se a viga baldrame está apoiada no solo, a face inferior não tem fôrma — usar apenas as 2 faces laterais: `2 × h × L_total`.

### 2.5 Radier

```
A_forma_radier = Perímetro_externo × e_radier
(apenas faces laterais da borda)
```

---

## 🔩 3. Armadura de Fundações — Aço CA-50 (kg)

### Tabela de Referência de Consumo (taxa estimada):

| Elemento | Taxa média (kg/m³) |
|---|---|
| Sapata isolada | 60 a 100 |
| Bloco sobre estacas | 80 a 120 |
| Viga baldrame | 80 a 120 |
| Radier (sem nervuras) | 60 a 80 |
| Radier (com nervuras) | 80 a 120 |
| Pedestal | 120 a 180 |

> Quando o projeto fornece o detalhamento da armadura, calcular barra a barra usando as fórmulas do Módulo Estrutura (§3.3 EST).

### Transpasse mínimo em fundações:

```
C_transpasse ≥ 40 × Ø (CA-50, concreto C30, zona de tração)
C_transpasse ≥ 60 × Ø (ambientes agressivos — mar, solo químico)
```

---

## 🏗️ 4. Escavação e Reaterro (m³)

### 4.1 Escavação de Valas para Baldrame

```
V_escav = (b_vala + 0,20m folga) × h_escav × L_total
Onde folga de 0,20m (10cm por lado) para execução das fôrmas
```

### 4.2 Escavação de Cavas para Sapatas e Blocos

```
V_escav = (b + 0,20m) × (L + 0,20m) × h_escav
```

### 4.3 Volume de Reaterro

```
V_reaterro = V_escavado − V_concreto_fundação
(o volume de concreto ocupa parte da cava)
```

### 4.4 Carga de Terra para Bota-Fora

```
V_bota_fora = V_escavado − V_reaterro
Fator de empolamento: multiplicar por 1,25 a 1,35 (terra argilosa)
```

---

## 📦 5. Coeficientes TCPO — Fundações

### 5.1 Concreto Usinado — Resistências Mínimas

| Elemento | Fck mínimo | CAA (Agressividade) |
|---|---|---|
| Lastro / Regularização | C10–C15 | Não estrutural |
| Baldrame, sapata, bloco | C30 | CAA II (urbano normal) |
| Fundação litorânea / industrial | C35–C40 | CAA III–IV |

### 5.2 Consumo de Aço — Arame Recozido

```
Arame recozido = 1,5% a 2,0% do peso total de aço
```

### 5.3 Consumo de Madeira para Fôrmas de Fundação

| Material | Consumo | Reaproveitamento |
|---|---|---|
| Tábua comum (2,5cm) | 0,040 m³/m² de fôrma | 1 a 2 vezes |
| Compensado 17mm | 0,018 m³/m² | 2 a 3 vezes |
| Fôrma metálica (aluguel) | — | 8 a 12 vezes |

---

## 🌳 6. Árvore de Decisão — Fundações

| Pedido do Usuário | Ação do Agente | Seção |
|---|---|---|
| "Quantifique as sapatas do projeto" | Solicitar: b, L, h_sapata, b_ped, h_ped, H_ped de CADA sapata | §1.1 |
| "Quanto concreto para o radier?" | Solicitar: Comp_total, Larg_total, espessura, se há nervuras | §1.5 |
| "Calcule o volume do baldrame" | Solicitar: b, h, L_total de cada trecho | §1.6 |
| "Qual a escavação total da obra?" | Solicitar: tipo de fundação, dimensões de cada cava/vala, profundidade | §4 |
| "Estimativa de aço das fundações" | Usar taxa de 60–100 kg/m³ e registrar como estimativa | §3 |

---

## 📋 7. Modelo de Memória de Cálculo — Sapata Isolada

```
╔══════════════════════════════════════════════════════════════════╗
║        MEMÓRIA DE CÁLCULO — FUNDAÇÃO: SAPATA ISOLADA            ║
╠══════════════════════════════════════════════════════════════════╣
║  OBRA:     [Nome da Obra]        CIA: [FUN-GER-F01]              ║
║  ELEMENTO: Sapata F-01           PILAR: P-01                     ║
║  RESIST.:  Fck = 30 MPa  CA-50   CAA: II                         ║
╠══════════════════════════════════════════════════════════════════╣
║  SAPATA:                                                         ║
║    b = X,XX m   L = X,XX m   h = X,XX m                         ║
║    V_sapata = b × L × h = X,XX × X,XX × X,XX = X,XX m³          ║
║                                                                  ║
║  PEDESTAL:                                                       ║
║    b_ped = X,XX m   h_ped = X,XX m   H_ped = X,XX m             ║
║    V_ped = X,XX × X,XX × X,XX = X,XX m³                         ║
║                                                                  ║
║  FÔRMA:                                                          ║
║    Sapata: 2×(X,XX+X,XX)×X,XX = X,XX m²                         ║
║    Pedestal: (2×X,XX+2×X,XX)×X,XX = X,XX m²                     ║
║    Total fôrma = X,XX m²                                         ║
║                                                                  ║
║  ARMADURA (taxa estimada ou detalhada):                          ║
║    Taxa: 80 kg/m³ → X,XX × 80 = XX,XX kg                        ║
║    Arame (1,5%): X,XX kg                                         ║
║                                                                  ║
║  LASTRO (C10, e=7cm):                                            ║
║    V_lastro = (X,XX+0,20)×(X,XX+0,20)×0,07 = X,XX m³            ║
║                                                                  ║
║  ✅ CONCRETO SAPATA: X,XX m³ | FÔRMA: X,XX m² | AÇO: XX,XX kg   ║
║     LASTRO: X,XX m³                                              ║
╚══════════════════════════════════════════════════════════════════╝
```
