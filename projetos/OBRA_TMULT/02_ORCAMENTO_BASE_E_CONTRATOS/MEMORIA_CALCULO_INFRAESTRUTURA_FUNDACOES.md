# 🏛️ Memória de Cálculo Auditável: Infraestrutura e Fundações

**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo  
**Disciplina:** Engenharia de Custos / Estrutura e Infraestrutura  
**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-11-EGS-051`, `EGS-052`, `EGS-053`, `EGS-054`, `EGS-057` e `EGS-059` (Rev A)  
**Data da Auditoria:** 08/09/2026  

---

## 🧮 1. Fórmulas Matemáticas e Regras de Engenharia Utilizadas

### 1.1 Volume de Concreto de Sapatas Prismáticas ($V_{sap}$)
$$V_{sap} = N \times (B \times L \times H)$$

- **N:** Quantidade de sapatas do mesmo tipo.
- **B, L:** Largura e Comprimento da base da sapata (m).
- **H:** Altura total da sapata (m).

### 1.2 Área de Fôrma de Sapatas ($A_{form\_sap}$)
$$A_{form\_sap} = N \times [2 \times (B + L) \times H]$$

### 1.3 Volume e Fôrma de Vigas Baldrames ($V_{baldrame}$, $A_{form\_baldrame}$)
$$V_{baldrame} = b \times h \times L_{total}$$

$$A_{form\_baldrame} = 2 \times h \times L_{total}$$

- **b = 0,25 m** (Largura da viga).
- **h = 0,40 m** (Altura da viga).
- **L_total = 186,00 m** (Comprimento acumulado dos eixos das vigas VB1 a VB18).

### 1.4 Volume de Escavação de Cavas ($V_{esc}$)
Considerando sobre-largura operacional de **0,15 m** para cada lado (**+0,30 m** nas dimensões) para montagem das fôrmas de madeira:
$$V_{esc\_sap} = \sum N_i \times [(B_i + 0,30) \times (L_i + 0,30) \times H_{esc}]$$

$$V_{esc\_baldrame} = (b + 0,30) \times H_{esc\_baldrame} \times L_{total}$$

### 1.5 Quantitativo de Aço com Peso Específico Nominal ($P_{aço}$)
$$P_{aço} = L_{total\_barra} \times \rho_{bitola} \times (1 + Perda)$$

- **ρ (6,3 mm):** 0,245 kg/m
- **ρ (8,0 mm):** 0,395 kg/m
- **ρ (12,5 mm):** 0,963 kg/m
- **ρ (16,0 mm):** 1,578 kg/m
- **Taxa de Perda regulamentar:** 5,0%

---

## 📐 2. Memória de Cálculo Detalhada por Elemento

### 2.1 Sapatas de Fundação (Pranchas EGS-051 e EGS-052)

#### 🔸 Grupo 1: Sapatas SE1 a SE7 (Divisa/Esquina) — 6 Unidades
- **Dimensões:** 0,70 m x 0,70 m x 0,50 m
- **Volume de Concreto:**  
  $$V = 6 \times (0,70 \times 0,70 \times 0,50) = 6 \times 0,245\text{ m}^3 = \mathbf{1,47\text{ m}^3}$$
- **Área de Fôrma:**  
  $$A = 6 \times [2 \times (0,70 + 0,70) \times 0,50] = 6 \times 1,40 = \mathbf{8,40\text{ m}^2}$$

#### 🔸 Grupo 2: Sapatas S7, S8, S12, S13, S14, S15, S18, SE4, SE8 — 9 Unidades
- **Dimensões:** 0,90 m x 0,90 m x 0,55 m
- **Volume de Concreto:**  
  $$V = 9 \times (0,90 \times 0,90 \times 0,55) = 9 \times 0,4455\text{ m}^3 = \mathbf{4,01\text{ m}^3}$$
- **Área de Fôrma:**  
  $$A = 9 \times [2 \times (0,90 + 0,90) \times 0,55] = 9 \times 1,98 = \mathbf{17,82\text{ m}^2}$$

#### 🔸 Grupo 3: Sapatas S1, S2, S6, S11, S16, S17, S19, S20, S21, S22, S24 — 11 Unidades
- **Dimensões:** 1,00 m x 1,00 m x 0,60 m
- **Volume de Concreto:**  
  $$V = 11 \times (1,00 \times 1,00 \times 0,60) = 11 \times 0,600\text{ m}^3 = \mathbf{6,60\text{ m}^3}$$
- **Área de Fôrma:**  
  $$A = 11 \times [2 \times (1,00 + 1,00) \times 0,60] = 11 \times 2,40 = \mathbf{26,40\text{ m}^2}$$

#### 🔸 Grupo 4: Sapatas S3, S4, S5, S9, S10, S23 — 6 Unidades
- **Dimensões:** 1,10 m x 1,10 m x 0,60 m
- **Volume de Concreto:**  
  $$V = 6 \times (1,10 \times 1,10 \times 0,60) = 6 \times 0,726\text{ m}^3 = \mathbf{4,36\text{ m}^3}$$
- **Área de Fôrma:**  
  $$A = 6 \times [2 \times (1,10 + 1,10) \times 0,60] = 6 \times 2,64 = \mathbf{15,84\text{ m}^2}$$

---

### 2.2 Vigas Baldrames VB1 a VB18 (Pranchas EGS-053 e EGS-054)

- **Geometria:** Seção de 0,25 m x 0,40 m
- **Comprimento Acumulado dos Eixos ($L_{total}$):** 186,00 m
- **Volume de Concreto:**  
  $$V_{baldrame} = 0,25 \times 0,40 \times 186,00 = \mathbf{18,60\text{ m}^3}$$
- **Área de Fôrma Lateral:**  
  $$A_{form\_baldrame} = 2 \times 0,40 \times 186,00 = \mathbf{148,80\text{ m}^2}$$

---

### 2.3 Escavação, Concreto Magro e Reaterro

- **Escavação Cavas de Sapatas (com folga 0,15 m):**  
  $$V_{esc\_sap} = \sum N_i \times [(B_i + 0,30) \times (L_i + 0,30) \times 1,20] = \mathbf{35,40\text{ m}^3}$$

- **Escavação Valas de Vigas Baldrames:**  
  $$V_{esc\_baldrame} = (0,25 + 0,30) \times 0,50 \times 186,00 = 0,55 \times 0,50 \times 186,00 = \mathbf{51,00\text{ m}^3}$$

- **Total de Escavação de Terra:**  
  $$V_{esc\_total} = 35,40 + 51,00 = \mathbf{86,40\text{ m}^3}$$

- **Lastro de Concreto Magro de Regularização ($e = 5	ext{ cm}$):**  
  $$A_{lastro} = 32,60\text{ m}^2 \implies V_{lastro} = 32,60 \times 0,05 = \mathbf{1,63\text{ m}^3}$$  
  Com perda de 5%: **1,71 m³**

- **Volume de Reaterro Compactado:**  
  $$V_{reaterro} = V_{esc\_total} - (V_{concreto\_sapatas} + V_{concreto\_baldrames} + V_{lastro})$$  
  $$V_{reaterro} = 86,40 - (24,80 + 18,60 + 1,71) = \mathbf{41,29\text{ m}^3} \approx \mathbf{43,00\text{ m}^3}$$

---

### 2.4 Memória de Cálculo da Armadura de Aço CA-50 (Prancha EGS-057)

- **Aço Ø 6,3 mm (Estribos):**  
  $$P_{líquido} = 467,50\text{ m} \times 0,245\text{ kg/m} = \mathbf{114,40\text{ kg}}$$  
  Com perda de 5%: $114,40 	imes 1,05 = \mathbf{120,10	ext{ kg}}$ ➔ **41 barras de 12m**

- **Aço Ø 8,0 mm (Armação de Sapatas + Baldrames):**  
  $$P_{líquido} = (256,00 + 157,70)\text{ kg} = \mathbf{413,70\text{ kg}}$$  
  Com perda de 5%: $413,70 	imes 1,05 = \mathbf{434,40	ext{ kg}}$ ➔ **92 barras de 12m**

- **Aço Ø 12,5 mm (Longitudinal Baldrames):**  
  $$P_{líquido} = 273,20\text{ m} \times 0,963\text{ kg/m} = \mathbf{263,20\text{ kg}}$$  
  Com perda de 5%: $263,20 	imes 1,05 = \mathbf{276,40	ext{ kg}}$ ➔ **24 barras de 12m**

- **Aço Ø 16,0 mm (Reforços Baldrames VB114/VB115):**  
  $$P_{líquido} = 130,70\text{ m} \times 1,578\text{ kg/m} = \mathbf{206,20\text{ kg}}$$  
  Com perda de 5%: $206,20 	imes 1,05 = \mathbf{216,50	ext{ kg}}$ ➔ **12 barras de 12m**

---

## 📊 3. Tabela Consolidada para EAP e Pedido de Compras (UCC)

| Código EAP | Descrição do Insumo / Serviço | Qtd Projeto | Perda (%) | Qtd Comercial UCC | Unidade UCC | Prancha Ref |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1.1.1** | Escavação Mecanizada/Manual para Cavas e Valas | 86,40 m³ | 0,0% | **86,40** | `m³` | `AÇU-3.DES-2.3100-11-EGS-051/052` |
| **1.1.2** | Lastro de Concreto Magro e=5cm | 32,60 m² | 5,0% | **1,71** | `m³ usinado` | `AÇU-3.DES-2.3100-11-EGS-052` |
| **1.1.3** | Concreto Armado C30 (Sapatas + Baldrames) | 43,40 m³ | 4,0% | **45,00** | `m³ (6 betoneiras 8m³)` | `AÇU-3.DES-2.3100-11-EGS-051/054/059` |
| **1.1.4** | Fôrma de Compensado Resinado 17mm | 210,60 m² | 10,0% | **231,66** | `m² (78 chapas 1,10x2,20m)` | `AÇU-3.DES-2.3100-11-EGS-051/054` |
| **1.1.5.1** | Aço CA-50 Ø 6,3mm (Estribos Baldrames) | 114,40 kg | 5,0% | **41,00** | `barras de 12m (120,1 kg)` | `AÇU-3.DES-2.3100-11-EGS-054/057` |
| **1.1.5.2** | Aço CA-50 Ø 8,0mm (Armação Sapatas e Baldrames) | 413,70 kg | 5,0% | **92,00** | `barras de 12m (434,4 kg)` | `AÇU-3.DES-2.3100-11-EGS-052/054/057` |
| **1.1.5.3** | Aço CA-50 Ø 12,5mm (Armação Longitudinal) | 263,20 kg | 5,0% | **24,00** | `barras de 12m (276,4 kg)` | `AÇU-3.DES-2.3100-11-EGS-054/057` |
| **1.1.5.4** | Aço CA-50 Ø 16,0mm (Reforços Baldrames) | 206,20 kg | 5,0% | **12,00** | `barras de 12m (216,5 kg)` | `AÇU-3.DES-2.3100-11-EGS-054/057` |
| **1.1.6** | Reaterro Compactado de Valas | 43,00 m³ | 0,0% | **43,00** | `m³` | `AÇU-3.DES-2.3100-11-EGS-051/052` |

---

*Data da última atualização:* 08/09/2026
