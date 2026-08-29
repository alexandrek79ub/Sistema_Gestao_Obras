# 🏗️ SKILL MÓDULO 02: Estrutura (Concreto Armado)

> **Dependência:** Carregar sempre com [SKILL_QUANTIFICACAO_MASTER.md](file:///c:/Users/Alexandre/Workspace/A11_FREE%20LANCER%20ENGENHARIA/skills/quantitativo/SKILL_QUANTIFICACAO_MASTER.md)
> **Normas:** NBR 6118 (Projeto de estruturas de concreto), NBR 14931 (Execução), NBR 7480 (Aço CA-50/CA-60)
> **Fck padrão superestrutura:** C25 (CAA II — ambiente urbano normal)

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

**Seção retangular:**
```
V_pilar = b × h × H_pilar
H_pilar = H_pé-direito − h_viga (altura livre entre faces das vigas)
```
> Se pilar atravessa mais de um pavimento sem viga intermediária, usar H_pilar = altura total.

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

**Viga simples (2 apoios):**
```
V_viga = b × h × L_livre
L_livre = vão entre faces dos pilares (m)
```

**Viga contínua (>2 apoios):**
```
V_viga = b × h × L_total
L_total = comprimento total entre extremos dos apoios
```

**Viga invertida (abaixo da laje):**
```
V_viga_inv = b × (h_total − e_laje) × L_livre
(descontar a espessura da laje que ocupa o topo da viga)
```

### 1.3 Lajes

**Laje Maciça:**
```
V_laje = A_projetada × e_laje
A_projetada = área em planta (descontar aberturas de shaft, escada, etc.)
```

**Laje Nervurada / Treliçada (com cubetas EPS ou cerâmica):**
```
V_total = A_laje × e_total
V_cubetas = n_cubetas × b_caixote × h_caixote × L_caixote
V_laje_líq = V_total − V_cubetas
```
> Solicitar do projeto: dimensões do caixote (cubeta), espaçamento entre nervuras, largura da nervura, altura total da laje.

**Laje pré-moldada (vigotas + tavelas):**
```
Volume de capeamento (capa de concreto in loco):
V_capa = A_laje × e_capa
e_capa = tipicamente 3 a 5 cm
```

### 1.4 Escadas

```
V_escada = Largura × A_inclinada × e_laje + V_degraus

A_inclinada = Larg_escada × √(H_desnível² + L_projeção²)
V_degraus = n_degraus × (0,5 × b_degrau × h_degrau × Larg_escada)
(triângulo de concreto de cada degrau)
```
> Solicitar: Largura da escada, Altura total (desnível), Projeção horizontal, N° de degraus, Espessura da laje.

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

---

## 🔄 4. Controle de Pavimento Tipo (Andares Repetidos)

Quando N andares possuem layout estrutural idêntico:

```
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
