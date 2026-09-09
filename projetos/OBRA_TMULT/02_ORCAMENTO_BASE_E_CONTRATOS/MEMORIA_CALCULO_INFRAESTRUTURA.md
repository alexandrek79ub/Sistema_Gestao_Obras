# 🏛️ Memória de Cálculo Auditável: Infraestrutura e Fundações (Sapatas e Baldrames)

**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo  
**Disciplina:** Infraestrutura e Fundações (Sapatas e Baldrames)  
**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-11-EGS-051 a EGS-054`  
**Data da Auditoria:** 08/09/2026  

---

## 🧮 1. Demonstração Matemática Detalhada Sapata por Sapata, Baldrames e Terraplenagem

### 1.1 Escavação Líquida de Cavas de 32 Sapatas + Valas de Baldrames (Geometria Líquida Executiva)
> **Regra da Geometria Líquida Executiva (Checklist 2):** A escavação das valas de baldrames é calculada no comprimento LIVRE ENTRE AS CAVAS DAS SAPATAS, descontando a interseção de nós para evitar dupla contagem. Folga lateral executiva = **20 cm** para cada lado.
- **11 Sapatas S1 (1,00m × 1,00m → Cava 1,40m × 1,40m × 0,70m):** `11 × 1,40m × 1,40m × 0,70m = 15,092 m³`
- **6 Sapatas S3 (1,10m × 1,10m → Cava 1,50m × 1,50m × 0,70m):** `6 × 1,50m × 1,50m × 0,70m = 9,450 m³`
- **9 Sapatas S7 (0,90m × 0,90m → Cava 1,30m × 1,30m × 0,70m):** `9 × 1,30m × 1,30m × 0,70m = 10,647 m³`
- **6 Sapatas SE1 (0,70m × 0,70m → Cava 1,10m × 1,10m × 0,70m):** `6 × 1,10m × 1,10m × 0,70m = 5,082 m³`
- **Subtotal Cavas Sapatas:** `15,092 + 9,450 + 10,647 + 5,082 = 40,271 m³`
- **Valas Vigas Baldrames (54,30m livres × 0,45m × 0,45m):** `54,30m × 0,45m × 0,45m = 11,000 m³`
- **Total Escavação Líquida:** **`51,27 m³`**

---

### 1.2 Apiloamento e Compactação do Fundo de Cava/Vala (m²)
> **Regra Executiva:** Medido na área de fundo que recebe o maço/sapo de compactação, considerando 10cm de projeção de aba para o lastro.
- **11 Sapatas S1 (Fundo 1,20m × 1,20m):** `11 × 1,44 m² = 15,84 m²`
- **6 Sapatas S3 (Fundo 1,30m × 1,30m):** `6 × 1,69 m² = 10,14 m²`
- **9 Sapatas S7 (Fundo 1,10m × 1,10m):** `9 × 1,21 m² = 10,89 m²`
- **6 Sapatas SE1 (Fundo 0,90m × 0,90m):** `6 × 0,81 m² = 4,86 m²`
- **Valas de Baldrames (54,30m livres × 0,35m fundo):** `54,30m × 0,35m = 19,01 m²`
- **Área Total Líquida de Apiloamento:** `15,84 + 10,14 + 10,89 + 4,86 + 19,01 =` **`60,74 m²`**

---

### 1.3 Lastro de Concreto Magro fck 15 MPa (e=5cm)
> **Fórmula:** `V_magro = A_fundo_lastro (60,74 m²) × 0,05 m`
- **Volume Físico de Projeto:** `60,74 m² × 0,05 m = 3,04 m³`
- **Quantidade Comercial UCC (Com Perda 5%):** `3,04 m³ × 1,05 =` **`3,19 m³`** (0,5 betoneira usinada).

---

### 1.4 Concreto fck 30 MPa das 32 Sapatas Isoladas (Prancha EGS-052)
> **Referência Direta de Projeto (Prancha EGS-052):** A tabela técnica oficial da prancha estrutural EGS-052 dimensiona e totaliza o volume de concreto das 32 sapatas isoladas (compostas por rodapé de 20cm e tronco piramidal h=10~15cm até o topo do arranque 30×30cm) em exatamente **`8,55 m³`**.
- **11 Sapatas S1 (1,00m × 1,00m - S1, S2, S6, S11, S16, S17, S19 a S22, S24):** `11 × 0,270 m³ = 2,970 m³`
- **6 Sapatas S3 (1,10m × 1,10m - S3, S4, S5, S9, S10, S23):** `6 × 0,335 m³ = 2,010 m³`
- **9 Sapatas S7 (0,90m × 0,90m - S7, S8, S12 a S15, S18, SE4, SE8):** `9 × 0,240 m³ = 2,160 m³`
- **6 Sapatas SE1 (0,70m × 0,70m - SE1, SE2, SE3, SE5, SE6, SE7):** `6 × 0,235 m³ = 1,410 m³`
- **Volume Geral das 32 Sapatas Isoladas (Fiel à Tabela EGS-052):** `2,970 + 2,010 + 2,160 + 1,410 =` **`8,55 m³`** (Com Perda 5%: **`8,98 m³`** - 2 betoneiras comerciais).

---

### 1.5 Fôrmas Compensadas 17mm das Sapatas (Rodapé 20cm)
> **Fórmula:** `A_fôrma = Perímetro_base × 0,20m`
- **11 Sapatas S1:** `11 × 4,00m × 0,20m = 8,80 m²`
- **6 Sapatas S3:** `6 × 4,40m × 0,20m = 5,28 m²`
- **9 Sapatas S7:** `9 × 3,60m × 0,20m = 6,48 m²`
- **6 Sapatas SE1:** `6 × 2,80m × 0,20m = 3,36 m²`
- **Fôrmas Tronco Piramidal:** `11,96 m²`
- **Total Fôrmas Sapatas:** **`35,88 m²`** → **17 chapas compensado 17mm** (`41,14 m²`).

---

### 1.6 Concreto, Fôrmas e Aço de Arranques e Vigas Baldrames (Pranchas EGS-052, EGS-053 e EGS-054)
- **Concreto fck 30 MPa Arranques de Pilares (P1-P24 h=0,65m):** `24 × (0,30m × 0,30m × 0,65m) = 1,86 m³` (Com Perda 5%: `1,95 m³`).
- **Fôrmas Compensadas dos Arranques de Pilares (P1-P24 e 8xE1 - Prancha EGS-052):** Área oficial de fôrma extraída do projeto estrutural = **`25,76 m²`** (Com Perda 10%: `28,34 m²`) → **12 chapas compensado 17mm** (`29,04 m²`).
- **Concreto fck 30 MPa Vigas Baldrames VB1-VB19 (Soma Vãos Livres L = 140,44m):** `L = 140,44m lineares`. Volume Total: `140,44m × 0,25m × 0,40m = 14,04 m³` (Com Perda 5%: `14,74 m³`).
- **Fôrmas Compensadas Vigas Baldrames:** `2 × 140,44m × 0,40m = 112,35 m²` (Apenas laterais dos vãos livres) → **52 chapas** (`125,84 m²`).
- **Aço CA-50 Ø8,0mm Sapatas Isoladas (Prancha EGS-052):** `256,00 kg` → **68 barras 12m** (`268,8 kg`).
- **Aço CA-50 Ø6,3mm/12,5mm Arranques Pilares (Prancha EGS-052):** `145,70 kg` → **38 barras 12m** (`153,0 kg`).
- **Aço CA-50 Vigas Baldrames VB1 a VB19 (Pranchas EGS-053 + EGS-054):**
  - Prancha EGS-053 (Vigas VB1 a VB6): `694,80 kg`
  - Prancha EGS-054 (Vigas VB7 a VB19): `382,50 kg`
  - **Peso Total Aço CA-50 Vigas Baldrames:** **`1.077,30 kg`** → **199 barras 12m** (`1.131,2 kg` UCC).
- **Arame Recozido BWG 18 (1,5% Aço):** `22,18 kg` → **23 kg** (23 rolos 1kg).
- **Espaçadores de Concreto 40mm/50mm:** `860 unid` → **903 unidades**.

#### 📐 Tabela Mestra Auditável de Detalhamento Viga por Viga (VB1 a VB19):

| Viga | Prancha | Cotas dos Vãos e Apoios Extraídas (cm) | Comprimento Total (m) | Vol. Concreto (m³) | Área Fôrma (m²) |
| :---: | :---: | :--- | :---: | :---: | :---: |
| **VB1** | `EGS-053` | 560 + 560 + 560 + 240 + 295 + 560 (Apenas vãos livres) | **27.75 m** | 2.775 m³ | 22.20 m² |
| **VB2** | `EGS-053` | 380 + 161 + 380 (Apenas vãos livres) | **9.21 m** | 0.921 m³ | 7.37 m² |
| **VB3** | `EGS-053` | 560 + 560 + 560 + 275 + 260 + 560 (Apenas vãos livres) | **27.75 m** | 2.775 m³ | 22.20 m² |
| **VB4** | `EGS-053` | 380 + 161 + 380 (Apenas vãos livres) | **9.21 m** | 0.921 m³ | 7.37 m² |
| **VB5** | `EGS-053` | 380 (Apenas vãos livres) | **3.80 m** | 0.380 m³ | 3.04 m² |
| **VB6** | `EGS-053` | 560 + 240 + 295 (Apenas vãos livres) | **10.95 m** | 1.095 m³ | 8.76 m² |
| **VB7** | `EGS-054` | 380 (Apenas vãos livres) | **3.80 m** | 0.380 m³ | 3.04 m² |
| **VB8** | `EGS-054` | 189 + 346 + 275 + 260 (Apenas vãos livres) | **10.70 m** | 1.070 m³ | 8.56 m² |
| **VB9** | `EGS-054` | 380 (Apenas vãos livres) | **3.80 m** | 0.380 m³ | 3.04 m² |
| **VB10** | `EGS-054` | 385 (Apenas vãos livres) | **3.85 m** | 0.385 m³ | 3.08 m² |
| **VB11** | `EGS-054` | 385 (Apenas vãos livres) | **3.85 m** | 0.385 m³ | 3.08 m² |
| **VB12** | `EGS-054` | 220,5 + 189,5 (Apenas vãos livres) | **4.10 m** | 0.410 m³ | 3.28 m² |
| **VB13** | `EGS-054` | 195,5 + 159,5 (Apenas vãos livres) | **3.55 m** | 0.355 m³ | 2.84 m² |
| **VB14** | `EGS-054` | 189 + 246 (Apenas vãos livres) | **4.35 m** | 0.435 m³ | 3.48 m² |
| **VB15** | `EGS-054` | 164,5 (Apenas vãos livres) | **1.65 m** | 0.165 m³ | 1.32 m² |
| **VB16** | `EGS-054` | 180 (Apenas vãos livres) | **1.80 m** | 0.180 m³ | 1.44 m² |
| **VB17** | `EGS-054` | 262,5 (Apenas vãos livres) | **2.63 m** | 0.263 m³ | 2.10 m² |
| **VB18** | `EGS-054` | 385 (Apenas vãos livres) | **3.85 m** | 0.385 m³ | 3.08 m² |
| **VB19** | `EGS-054` | 385 (Apenas vãos livres) | **3.85 m** | 0.385 m³ | 3.08 m² |
| **TOTAL** | **-** | **Soma dos Vãos Livres (19 Elementos)** | **140.44 m** | **14.04 m³** | **112.35 m²** |

---

### 1.7 Insumos de Apoio e Miudezas Executivas de Canteiro (Fôrmas, Armação, Concretagem e Impermeabilização)
> **Regra de Suprimentos (UCC / SKILL 01):** Miudezas de almoxarifado indispensáveis para garantir zero paralisação na montagem, concretagem, cura e desforma das fundações:
- **Arame Recozido BWG 18 (1,5% sobre o peso total de aço):** `1.479,00 kg aço × 0,015 = 22,18 kg` → **17 rolos de 1 kg**.
- **Espaçadores / Pastilhas de Concreto cobrimento 40mm/50mm (Solo):** `640 unid` (Com Perda 5%: **672 unidades**).
- **Desmoldante Biodegradável para Fôrmas de Madeira (173,99 m²):** `173,99 m² / 25 m²/L = 6,96 L` → **1 balde de 18L** (`18,00 L`).
- **Pregos de Aço com Cabeça 17×27 para Fôrmas (0,05 kg/m²):** `173,99 m² × 0,05 kg/m² = 8,70 kg` (Com Perda 5%: **10 kg** em 1 caixa).
- **Sarrafos de Madeira Pinus 2,5×7,0cm para Gravatas e Travamento de Valas (1,20 m/m²):** `173,99 m² × 1,20 m/m² = 208,80 m` (Com Perda 10%: `229,68 m`) → **77 peças de 3,00m** (`231,00 m`).
- **Lona Plástica Preta e=150µ para Fundo de Vala e Cura Úmida (7 dias NBR/EGS-052):** `120,00 m²` → **1 bobina 4m × 50m** (`200,00 m²`).
- **Acessórios para Pintura Asfáltica (Rolos de Lã 23cm e Trinchas 2"):** `3 rolos de lã + 2 trinchas =` **`5 unidades`**.

---

### 1.8 Impermeabilização Tinta Asfáltica (Topo e Laterais de Baldrames e Sapatas)
> **Fórmula:** `A_imperm = Topo_baldrame + 2 × Laterais_baldrame + Topo_sapatas + Arranques_pilares`
- **Topo das Vigas Baldrames (apoio alvenaria):** `140,44m × 0,25m = 35,11 m²`
- **Laterais das Vigas Baldrames (contato solo):** `2 × 140,44m × 0,40m = 112,35 m²`
- **Topo das 32 Sapatas Isoladas (descontando 0,09m² do pilar):**
  - S1 (11 un × 0,91m² = 10,01 m²) | S3 (6 un × 1,12m² = 6,72 m²)
  - S7 (9 un × 0,72m² = 6,48 m²) | SE1 (6 un × 0,40m² = 2,40 m²)
  - Subtotal Topo Sapatas = `25,61 m²`
- **Arranques de Pilares P1-P24 (Geometria Líquida c/ Desconto de Nós):**
  - Área bruta lateral (24 un h=0,65m): `24 × (4 × 0,30m) × 0,65m = 18,72 m²`
  - Desconto das faces de conexão com as vigas: `44 vãos livres × 2 extremidades = 88 conexões`.
  - Área descontada: `88 × (0,25m larg × 0,40m alt) = 8,80 m²`
  - Área Líquida dos Arranques = `18,72 - 8,80 = 9,92 m²`
- **Área Total de Impermeabilização:** `35,11 (Topo VB) + 112,35 (Lat VB) + 25,61 (Topo Sap) + 9,92 (Arranques) =` **`182,99 m²`**
- **Quantidade Comercial UCC (Com Perda 10% de porosidade):** `182,99 m² × 1,10 = 201,29 m²` → **12 galões de 18L** (`216,00 m²`).

---

### 1.9 Reaterro Compactado e Bota-fora Líquidos
- **Reaterro Compactado c/ Maço/Sapo Líquido:** `51,27 m³ (escavação) - 20,10 m³ (concreto fundações) =` **`31,17 m³`**
- **Bota-fora e Carga de Terra c/ Empolamento 1,25 Líquido:** `20,10 m³ × 1,25 =` **`25,13 m³`** (3 caminhões 12m³).

---

---

## 📊 2. Tabela Consolidada de Quantitativos e Pedido de Compras (UCC)

| Código EAP | Descrição do Insumo / Serviço | Qtd Projeto | Perda (%) | Qtd Comercial UCC | Unidade UCC | Prancha Ref | Preço Unit. | Custo Total |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: |
| **1.1.1** | Escavação Mecanizada/Manual de Cavas e Valas (Geometria Líquida) | 51.27 m³ | 0.0% | **51.27** | `m³` | `AÇU-3.DES-2.3100-11-EGS-051/052` | - | **-** |
| **1.1.2** | Apiloamento e Compactação do Fundo de Cava/Vala Líquido | 60.74 m² | 0.0% | **60.74** | `m²` | `AÇU-3.DES-2.3100-11-EGS-051/052` | - | **-** |
| **1.1.3** | Lastro de Concreto Magro fck 15 MPa e=5cm sob Sapatas e Baldrames | 3.04 m³ | 5.0% | **3.19** | `m³ (0.5 betoneira)` | `AÇU-3.DES-2.3100-11-EGS-051/052` | - | **-** |
| **1.1.4** | Concreto Usinado fck 30 MPa para 32 Sapatas Isoladas (S1-S24 e SE1-SE8) | 8.55 m³ | 5.0% | **8.98** | `m³ (2 betoneiras)` | `AÇU-3.DES-2.3100-11-EGS-052` | - | **-** |
| **1.1.5** | Fôrma Compensado Resinado 17mm para Sapatas Isoladas (Tronco) | 35.88 m² | 10.0% | **17** | `chapas (41.14 m²)` | `AÇU-3.DES-2.3100-11-EGS-052` | - | **-** |
| **1.1.6** | Concreto Usinado fck 30 MPa para Arranques dos Pilares P1-P24 | 1.86 m³ | 5.0% | **1.95** | `m³` | `AÇU-3.DES-2.3100-11-EGS-052` | - | **-** |
| **1.1.7** | Fôrma Compensado Resinado 17mm para Arranques dos Pilares P1-P24 | 25.76 m² | 10.0% | **12** | `chapas (29.04 m²)` | `AÇU-3.DES-2.3100-11-EGS-052` | - | **-** |
| **1.1.8** | Concreto Usinado fck 30 MPa para Vigas Baldrames VB1-VB19 (25x40cm - 140,44m) | 14.04 m³ | 5.0% | **14.74** | `m³ (2 betoneiras)` | `AÇU-3.DES-2.3100-11-EGS-053/054` | - | **-** |
| **1.1.9** | Fôrma Compensado Resinado 17mm para Vigas Baldrames (140,44m) | 112.35 m² | 10.0% | **52** | `chapas (125.84 m²)` | `AÇU-3.DES-2.3100-11-EGS-053/054` | - | **-** |
| **1.1.10** | Armadura CA-50 Ø8,0mm (Armadura das 32 Sapatas Isoladas) | 256.00 kg | 5.0% | **68** | `barras 12m (268.8 kg)` | `AÇU-3.DES-2.3100-11-EGS-052` | - | **-** |
| **1.1.11** | Armadura CA-50 Ø6,3mm / Ø12,5mm (Arranques dos Pilares P1-P24) | 145.70 kg | 5.0% | **38** | `barras 12m (153.0 kg)` | `AÇU-3.DES-2.3100-11-EGS-052` | - | **-** |
| **1.1.12** | Armadura CA-50 Vigas Baldrames VB1-VB19 (EGS-053: 694,8kg + EGS-054: 382,5kg) | 1077.30 kg | 5.0% | **199** | `barras 12m (1131.2 kg)` | `AÇU-3.DES-2.3100-11-EGS-053/054` | - | **-** |
| **1.1.13** | Impermeabilização Tinta Asfáltica (Baldrames e Sapatas) | 183.36 m² | 10.0% | **201.70** | `m² (12 galões 18L)` | `AÇU-3.DES-2.3100-11-EGS-051/054` | - | **-** |
| **1.1.14** | Reaterro Compactado de Cavas e Valas c/ Maço/Sapo Líquido | 31.17 m³ | 0.0% | **31.17** | `m³` | `AÇU-3.DES-2.3100-11-EGS-051/052` | - | **-** |
| **1.1.15** | Bota-fora e Carga de Terra c/ Empolamento 1,25 Líquido | 20.10 m³ | 0.0% | **25.13** | `m³ (3 caminhões 12m³)` | `AÇU-3.DES-2.3100-11-EGS-051/052` | - | **-** |

---

*Data da última atualização:* 08/09/2026
