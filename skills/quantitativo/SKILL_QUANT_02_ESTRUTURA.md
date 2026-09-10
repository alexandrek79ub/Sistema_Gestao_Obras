# 🏗️ SKILL MÓDULO 02: Estrutura (Concreto Armado)

> **Dependência:** Carregar sempre com [SKILL_QUANTIFICACAO_MASTER.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANTIFICACAO_MASTER.md)
> **Normas:** NBR 6118 (Projeto de estruturas de concreto), NBR 14931 (Execução), NBR 7480 (Aço CA-50/CA-60)
> **Fck padrão superestrutura:** C25 (CAA II — ambiente urbano normal)

> [!CAUTION]
> **REGRAS ABSOLUTAS DO PMO VIRTUAL (INVIOLÁVEIS)**
> - **ZERO ESTIMATIVA / ZERO CHUTE:** É EXPRESSAMENTE PROIBIDO estimar, inferir ou chutar dimensões, comprimentos, áreas, volumes ou quantitativos de projeto de estruturas.
> - **LEITURA OBRIGATÓRIA:** Toda cota DEVE ser lida 100% diretamente das pranchas. Se faltar cota ou prancha, PARE A EXECUÇÃO E SOLICITE AO USUÁRIO. O orçamento é executivo e a gestão de obras não admite achismos.
> - **GRANULARIDADE 100% (PEÇA A PEÇA):** É PROIBIDO agrupar insumos (ex: "vigas V1 a V18"). O levantamento DEVE quantificar minuciosamente pilar por pilar, viga por viga, detalhando dimensões individuais.
> - **SEGREGAÇÃO MANDATÓRIA EAP vs. UCC (NÃO POLUIR A EAP):** 
>   - **Na EAP de Superestrutura:** Devem constar **exclusivamente serviços puros de engenharia** (Concreto Usinado, Fôrmas, Aço Armado, Vigotas Treliçadas, Blocos de Enchimento EPS, Escoramento Metálico).
>   - **Na UCC (Lista de Compras / BOM / Almoxarifado):** Devem ser discriminadas todas as **miudezas e insumos de apoio executivo** (Arame Recozido BWG 18, Espaçadores Plásticos de cobrimento, Desmoldante para fôrmas, Pregos 17x27/18x30, Sarrafos de madeira para gravatas, Lona de cura úmida). As miudezas NUNCA devem receber código de serviço da EAP.

---

## 🧭 Escopo deste Módulo

Cobre o quantitativo de **toda a superestrutura** em concreto armado:

- Pilares (seção retangular, circular, L, U, T)
- Vigas (simples, contínuas, invertidas)
- Lajes (maciça, nervurada, treliçada, pré-moldada)
- Escadas
- Reservatórios e caixas d'água superiores
- Controle de Pavimento Tipo (andares repetidos)

---

## 📐 1. Concreto — Superestrutura (m³)

> ⚠️ **PRECISÃO OBRIGATÓRIA:** 2 casas decimais. Nunca arredondar volumes intermediários.

### 1.1 Pilares

### 1.1 Pilares

**Seção retangular (com Cotas Nasce / Morre):**
```text
H_pilar = Cota_Morre − Cota_Nasce
V_pilar = seção1 × seção2 × H_pilar
A_forma = (2 × seção1 + 2 × seção2) × H_pilar × (n_lados / 4)
```
> ⚠️ **Regra de Cotas de Elevação (Nasce / Morre):** A memória de cálculo executiva DEVE registrar a cota inferior onde o pilar **nasce** (ex: 0,00m ou +5,40m) e a cota superior onde **morre** (ex: +7,60m ou +8,80m). O pé-direito de forma/concreto é a diferença direta entre essas cotas (`alt = morre - nasce`).

**Seção variável / pilar de transição:**
```
Decompor em trechos: V_total = V_trecho1 + V_trecho2 + ...
```

**Pilar-parede (seção L, U ou T):**
```
V = (Σ áreas dos trechos retangulares da seção) × H_pilar
Seção L: V = (b1×h1 + b2×h2) × H_pilar
Seção T: V = (b1×h1 + b2×h2 + b3×h3) × H_pilar
```

**Pilar circular:**
```
V = π × (D/2)² × H_pilar
```

### 1.2 Vigas

**Viga simples, contínua ou invertida (com controle de Fundo S/N e Lados):**
```text
V_concreto = LARG × ALT × L_livre × QUANT

A_forma_viga = (n_lados_laterais × ALT + (Fundo_SN × LARG)) × L_livre × QUANT
Onde:
  - Vigas suspensas normais: n_lados_laterais = 2, Fundo_SN = 1 (Total = 3 lados de forma)
  - Vigas Baldrame apoiadas no solo: n_lados_laterais = 2, Fundo_SN = 0 (Total = 2 lados de forma, sem fundo)
  - Vigas de borda/parede cega: n_lados_laterais = 1 ou 2 conforme encontros
```

**Vigas Baldrame e Cintas Perimétricas Fechadas (Regra da Geometria Líquida Executiva):**
```text
PROIBIDO medir aproximação simplificada por eixos. Desmembrar os encontros perimétricos sem duplicar cantos:
L_longitudinal_total = 2 × L_externo_longitudinal
L_transversal_líquido = 2 × (L_externo_transversal − 2 × e_viga)
L_total_líquido = L_longitudinal_total + L_transversal_líquido
```

### 1.3 Lajes e Escoramento (Cimbramento)

**Laje Maciça / Pré-Moldada / Nervurada:**
```text
1. Concreto (m³):
   V_laje = A_projetada × e_laje  (ou V_capa + V_vigotas para pré-moldadas)

2. Fôrma de Laje (m²):
   A_forma = A_projetada × coef_fôrma

3. Escoramento / Cimbramento (m² · Pé-Direito):
   V_escoramento = A_forma × Pé_Direito_PD (m)
   (Exemplo: Laje de 35 m² com Pé-Direito PD = 7,00m -> Escoramento = 245 m²·m de cimbramento)

4. Mapeamento por Tipo de Laje e Moldes:
   - Lajes Pré-moldadas / Treliçadas: Especificar vigotas e vigotes (ex: TR20745, H12, H16)
   - Lajes Nervuradas: Mapear área por tipo de molde/cubeta (ex: 80×80×20 cm, 80×40×30 cm)
```

### 1.4 Escadas (Parametrização Desmembrada Laje Rampa + Degraus/Espelhos)

```text
1. Geometria da Laje Piso (Rampa Inclinada):
   A_inclinada = Largura_A × √(Comprimento_B² + H_desnível²)
   V_concreto_rampa = Largura_A × Comprimento_B × Espessura_C × Qtde_D
   A_forma_rampa = A_inclinada × Qtde_D

2. Geometria dos Degraus / Espelhos:
   V_concreto_degraus = n_degraus_H × (0,5 × lar_deg_E × esp_alt_F × Base_G)
   A_forma_degraus = n_degraus_H × (esp_alt_F × Base_G + 2 × espelhos_laterais)

3. Totais Acumulados da Escada:
   V_total_concreto_m3 = (V_concreto_rampa + V_concreto_degraus) × QUANT
   A_total_forma_m2 = (A_forma_rampa + A_forma_degraus) × QUANT
```

### 1.5 Reservatório / Caixa d'água

```
Fundo: V_fundo = b × L × e_fundo
Paredes: V_paredes = 2×(b+L) × H_agua × e_parede
Tampa: V_tampa = b × L × e_tampa (se existir)
V_total = V_fundo + V_paredes + V_tampa
```

---

## 📏 2. Fôrmas — Superestrutura (m²)

### 2.1 Pilares

```
A_forma = Perímetro × H_pilar = (2b + 2h) × H_pilar
Pilar circular: A_forma = π × D × H_pilar
```

### 2.2 Vigas

```
A_forma = (2 × h_viga + b_viga) × L_livre
(face inferior + 2 faces laterais)
```
> Face superior da viga = fundo da laje → não tem fôrma separada.

### 2.3 Lajes

```
A_forma_laje = A_projetada (face inferior apenas)
```
> Escoramento (pontaletes e chapuzes) é medido separadamente em m² de laje ou por unidade.

### 2.4 Escadas

```
A_forma_escada = A_face_inferior + A_laterais + A_espelhos

A_face_inferior = Larg_escada × √(H_desnível² + L_projeção²)
A_laterais = 2 × (Comprimento_inclinado × e_laje)
A_espelhos = n_degraus × Larg_escada × h_espelho
```

### 2.5 Reservatório

```
A_forma_res = A_fundo + A_faces_laterais + A_tampa
A_fundo = b × L
A_laterais = 2×(b+L) × H_parede (interna + externa se necessário)
```

### 2.6 Taxas de Reaproveitamento

| Material | Reaproveitamento |
|---|---|
| Chapa compensada 17mm | 2 a 3 vezes |
| Compensado plastificado 18mm | 4 a 6 vezes |
| Fôrma metálica (aluguel) | 8 a 12 vezes |
| Fôrma de plástico (laje nervurada) | 10 a 15 vezes |

---

## 🔩 3. Armadura — Aço CA-50 e CA-60 (kg)

### 3.1 Tabela de Pesos Unitários por Bitola (NBR 7480)

| Bitola (Ø mm) | Área da Seção (cm²) | Peso Linear (kg/m) | Uso Típico |
|---|---|---|---|
| Ø 6,3 | 0,312 | 0,245 | Estribos, malha CA-60, distribuição |
| Ø 8,0 | 0,503 | 0,395 | Estribos, laje, pilares pequenos |
| Ø 10,0 | 0,785 | 0,617 | Armadura principal de laje, vigas pequenas |
| Ø 12,5 | 1,227 | 0,963 | Armadura principal de viga, pilar |
| Ø 16,0 | 2,011 | 1,578 | Viga e pilar de carga média |
| Ø 20,0 | 3,142 | 2,466 | Vigas e pilares de carga elevada |
| Ø 25,0 | 4,909 | 3,853 | Pilares de grande seção, vigas principais |
| Ø 32,0 | 8,042 | 6,313 | Pilares e vigas de grande porte |

### 3.2 Fórmula de Cálculo por Barra

```
L_barra = L_líquido + 2 × C_transpasse

C_transpasse ≥ 40 × Ø  (zona de tração, CA-50, concreto C25)
C_transpasse ≥ 25 × Ø  (zona de compressão)
C_transpasse ≥ 60 × Ø  (ambiente agressivo, CAA III)

Peso_barra = L_barra × Peso_linear (kg/m)
Peso_total_bitola = Σ (n_barras × Peso_barra) × (1 + Taxa_perda)
```

### 3.3 Taxas de Perda por Fornecimento

| Fornecimento | Taxa de Perda |
|---|---|
| Aço em vergalhão 12m (CA-50) | 5% |
| Aço em barra curta | 8% |
| Aço em rolo (CA-60 Ø≤10mm) | 3% |

**Arame recozido BWG 18:** 15 a 20 kg por tonelada de aço (1,5% a 2,0%)

### 3.4 Taxas Médias de Consumo por Elemento (referência — quando sem projeto)

| Elemento | Taxa (kg/m³) | Observação |
|---|---|---|
| Laje maciça | 80 a 120 | Aumenta com vão e carga |
| Laje nervurada | 60 a 100 | Menor taxa por m³ (menos concreto) |
| Viga | 120 a 180 | Aumenta com vão e momento |
| Pilar | 150 a 250 | Aumenta com esforço e altura |
| Escada | 100 a 150 | — |
| Reservatório | 80 a 120 | — |

> ⚠️ Taxas médias são apenas estimativas para orçamento preliminar. Para orçamento executivo, usar o detalhamento de armadura do projeto estrutural.

### 🔩 3.5 Matriz Consolidada de Miudezas e Consumíveis da Superestrutura (UCC / BOM)

> 🛑 **REGRA DE OURO DA GOVERNANÇA: EAP É SERVIÇO, UCC É COMPRA!**  
> Estes insumos e consumíveis de canteiro **NÃO recebem código EAP**. São derivados parametricamente dos serviços executivos de fôrmas, armação e concretagem e alocados estritamente na Lista de Compras (BOM / UCC):

| Insumo Consumível / Miudeza | Fórmula de Consumo Paramétrico | Unidade de Compra (UCC) |
|:---|:---|:---:|
| **Espaçadores circulares tipo roda/estrela com garra (Pilares)** | 3 a 4 un/m² de área lateral de pilar (garantia de cobrimento NBR 6118) | Caixa 100 un |
| **Espaçadores tipo cadeira/garra lateral (Vigas)** | 4 un/m linear de viga (2 no fundo + 2 nas laterais) | Caixa 100 un |
| **Espaçadores tipo centopeia/torre (Lajes)** | 2 a 3 un/m² de laje (armadura positiva e negativa) | Caixa 100 un |
| **Arame Recozido BWG 18** | $1,5\%$ a $2,0\%$ do peso total de aço CA-50/CA-60 ($kg$) | Rolo 1 kg |
| **Desmoldante para Compensado Resinado** | 1 L para cada 25 a 30 m² de fôrma de madeira | Bombona 18 L |
| **Desmoldante para Compensado Plastificado** | 1 L para cada 35 a 40 m² de chapa plastificada | Bombona 18 L |
| **Pregos com Cabeça 17×27 e 18×30** | 0,05 kg por m² de fôrma de compensado | Caixa 10 kg |
| **Sarrafos Pinus 2,5×7,0cm (gravatas e contenção de pilares)** | 1,2 m lineares por m² de fôrma de pilar e viga | Dúzia de barras 3m |
| **Fita Adesiva Crepe Larga 48mm×50m (vedação de emendas)** | 1 rolo a cada 40 m² de fôrma (evita fuga de pasta/bicheiras) | Rolo 50 m |
| **Membrana de Cura Química Líquida (aspersão — Sika Antisol)** | 1 L para cada 6 m² de laje ou viga exposta | Frasco 3,6 L / Balde 18 L |
| **Lona Plástica Preta 200µ (cura úmida / proteção de lajes)** | 1 bobina (200 m²) a cada 200 m² de laje concretada | Bobina 200 m² |
| **Agulhas / Tensores de Barra Roscada 1/2" c/ Porca Borboleta** | 2 tensores por m² de face de pilar alto ($H > 3,00\text{m}$) | Barra 1m + porcas |

---

## 🔄 4. Cronograma, EAP e Controle de Pavimento Tipo (Nível 1.4)

### 📋 4.1 Tabela Oficial de Serviços para EAP e Cronograma (Nível 1.4 — Ciclo de Pavimento Tipo)

> 🛑 **REGRA DE SEGREGAÇÃO:** Esta tabela estrutura a linha de balanço e o ciclo executivo de cada pavimento da superestrutura. Miudezas e consumíveis constam exclusivamente da UCC (§3.5 e §4.2).

| Código EAP | Pacote de Trabalho (Ciclo de Pavimento) | Unid. Avanço | Predecessora Imediata | Prazo Mínimo Normativo (NBR 14931) |
|:---:|:---|:---:|:---:|:---:|
| **1.4.1** | Fôrmas de Pilares | m² | 1.3.11 (térreo) ou 1.4.11 pav anterior | — |
| **1.4.2** | Armação de Pilares (CA-50/CA-60) | kg | 1.4.1 | — |
| **1.4.3** | Concretagem de Pilares | m³ | 1.4.2 | — |
| **1.4.4** | Cimbramento e Fôrma de Fundo de Vigas e Lajes | m² | 1.4.3 FF+16h | Mínimo 16h antes de apoiar cimbramento sobre pilares |
| **1.4.5** | Armação de Vigas | kg | 1.4.4 | — |
| **1.4.6** | Armação de Lajes (positiva e negativa) | kg | 1.4.5 | — |
| **1.4.7** | Fôrmas Laterais de Vigas e Bordas de Laje | m² | 1.4.6 | — |
| **1.4.8** | Concretagem de Vigas e Lajes (Monolítica) | m³ | 1.4.7 | — |
| **1.4.9** | Cura Contínua (úmida 7 dias ou membrana química) | m² | 1.4.8 FF+0d | Mínimo 7 dias ininterruptos (NBR 14931) |
| **1.4.10** | Desforma Lateral de Pilares e Vigas | m² | 1.4.8 FF+3d | Mínimo 3 dias de cura |
| **1.4.11** | Desforma de Fundo de Vigas e Lajes + Re-escoramento | m² | 1.4.8 FF+14d | Mínimo 14 dias com re-escoramento mantido |
| **1.4.12** | Alívio Total de Escoramento (Retirada definitiva) | m² | 1.4.8 FF+28d | Mínimo 28 dias ($100\%$ do Fck alcançado) |

### 🛡️ 4.2 Checklist Anti-Omissão de Superestrutura (10 SKUs Obrigatórios na UCC/BOM)

> Antes do fechamento do lote de compras ou requisição de materiais da superestrutura, auditar a inclusão mandatória de:

- [ ] **Espaçadores de Pilar (tipo roda/estrela com garra):** 3 a 4 un/m² de pilar concretado.
- [ ] **Espaçadores de Viga (tipo cadeira/garra):** 4 un/m linear de viga estrutural.
- [ ] **Espaçadores de Laje (tipo centopeia/torre):** 2 a 3 un/m² de laje.
- [ ] **Arame Recozido BWG 18:** $1,5\%$ a $2,0\%$ do peso total de aço ($kg$).
- [ ] **Desmoldante para Fôrmas:** Tipo apropriado ao compensado (resinado ou plastificado), conforme taxa de consumo paramétrica.
- [ ] **Pregos com Cabeça 17×27 / 18×30:** 0,05 kg por m² de fôrma.
- [ ] **Sarrafos de Gravata e Travamento:** 1,2 m lineares por m² de fôrma de pilar/viga.
- [ ] **Fita Adesiva Crepe para Vedação de Emendas:** 1 rolo de 50m a cada 40 m² de fôrma montada.
- [ ] **Agulhas / Tensores de Barra Roscada:** Para contenção de fôrmas em pilares de pé-direito superior a 3,00m.
- [ ] **Membrana de Cura Química ou Lona Plástica 200µ:** Quantidade total proporcional à área de lajes e topos de vigas para cumprimento integral da NBR 14931.

### 🏢 4.3 Controle de Pavimento Tipo (Andares Repetidos)

Quando N andares possuem layout estrutural idêntico:

```text
Qtd_Total_Obra = Qtd_PavTipo × N_andares + Qtd_Pavimentos_Especiais
```

A memória de cálculo DEVE registrar:
> *"Pavimentos Tipo 01 a 08 — Multiplicador: 8× aplicado. Quantitativo base = 1 pavimento tipo."*

**Pavimentos que geralmente NÃO são repetidos:**
- Térreo (pé-direito duplo, uso comercial, garagem)
- Cobertura (caixa d'água, casa de máquinas, barrilete)
- Subsolo (rampa, impermeabilização especial)

---

## 📊 5. Tabela Resumo — Estrutura

| Elemento | Tag | Qtd | Concreto (m³) | Fôrma (m²) | Aço (kg) | Fck | Pavimento |
|---|---|---|---|---|---|---|---|
| Pilar | P1 | 8 | — | — | — | C25 | Tipo |
| Viga | V1 | 4 | — | — | — | C25 | Tipo |
| Laje maciça | L1 | 1 | — | — | — | C25 | Tipo |
| Escada | ESC-01 | 1 | — | — | — | C25 | Térreo |
| Reservatório | CX-01 | 1 | — | — | — | C25 | Cobertura |
| | | | **TOTAL** | **TOTAL** | **TOTAL** | | |

---

## 🌳 6. Árvore de Decisão — Estrutura

| Pedido do Usuário | Ação do Agente | Seção |
|---|---|---|
| "Volume de concreto do pilar P1" | Solicitar b, h, H_pilar líquido; perguntar se seção é regular ou especial | §1.1 |
| "Fôrma da viga V-03" | Solicitar b, h, L_livre | §2.2 |
| "Calcule o aço da viga V-03 (com projeto)" | Solicitar detalhamento: n° barras × Ø × comprimento + estribos | §3.2 |
| "Estime o aço da laje L1 sem projeto" | Usar taxa de 80–120 kg/m³ e alertar que é estimativa | §3.4 |
| "Quantifique a escada" | Solicitar: Larg, H_desnível, L_projeção, n°_degraus, e_laje | §1.4 + §2.4 |
| "Quantifique todos os pilares do tipo" | Calcular 1 pavimento tipo → multiplicar por N andares | §4 |
| "Quantifique a laje nervurada" | Solicitar: A_projetada, e_total, dimensões do caixote/cubeta | §1.3 |
