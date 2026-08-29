# 🏛️ SKILL MÓDULO 01: Fundações

> **Dependência:** Carregar sempre com [SKILL_QUANTIFICACAO_MASTER.md](file:///c:/Users/Alexandre/Workspace/A11_FREE%20LANCER%20ENGENHARIA/skills/quantitativo/SKILL_QUANTIFICACAO_MASTER.md)
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

## 📐 1. Concreto de Fundações (m³)

> ⚠️ **PRECISÃO OBRIGATÓRIA:** 2 casas decimais em todos os volumes. Fck mínimo C30 para fundações em solo com nível d'água ou agressividade média/alta.

### 1.1 Sapata Isolada

```
V_sapata = b × L × h_sapata
V_pedestal = b_ped × h_ped × H_ped
V_total = V_sapata + V_pedestal

Onde:
  b, L = dimensões em planta da sapata (m)
  h_sapata = altura da sapata (m)
  b_ped, h_ped = seção do pedestal (= seção do pilar, m)
  H_ped = altura do pedestal até o topo da sapata (m)
```

### 1.2 Sapata Associada (2 ou mais pilares)

```
V_sapata_assoc = b × L_total × h_sapata
V_pedestais = Σ (b_ped_i × h_ped_i × H_ped_i)
V_total = V_sapata_assoc + V_pedestais
```

### 1.3 Sapata Corrida (sob parede estrutural)

```
V_sap_corrida = b × h × L_total
Onde L_total = comprimento total da parede (m)
```

### 1.4 Bloco de Coroamento sobre Estacas

```
V_bloco = b × L × h_bloco
Onde b, L = dimensões em planta do bloco
     h_bloco = altura do bloco (conforme projeto)
```
> Verificar se o bloco é sobre 2, 3 ou 4 estacas — as dimensões variam conforme o projeto estrutural.

### 1.5 Radier (Fundação em Laje)

```
V_radier = A_projetada × e_radier
A_projetada = Comprimento_total × Largura_total da edificação
e_radier = espessura (tipicamente 15cm a 30cm)

Nervuras sob paredes (se houver):
V_nervura = b_nervura × h_nervura × L_nervura
V_total_radier = V_radier + Σ V_nervuras
```

### 1.6 Viga Baldrame / Cinta de Fundação

```
V_baldrame = b × h × L_total
Onde L_total = comprimento entre eixos dos pilares (m)
```
> O baldrame é medido separadamente das vigas de superestrutura. Sempre incluir na seção de FUNDAÇÕES.

### 1.7 Concreto de Regularização / Lastro (blinding)

```
V_lastro = A_base × e_lastro
e_lastro = 5cm a 10cm (conforme projeto)
Fck mínimo: C10 (não estrutural)
```
> Calcular sob sapatas, blocos e radier individualmente.

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
