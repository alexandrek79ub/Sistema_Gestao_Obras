import json
import os

gerador_file = r"c:\Users\Alexandre\Workspace\A11_SISTEMA_DE_GESTAO_OBRAS\scripts\gerador_orcamento_mestre.py"
json_file = r"c:\Users\Alexandre\Workspace\A11_SISTEMA_DE_GESTAO_OBRAS\projetos\OBRA_TMULT\02_ORCAMENTO_BASE_E_CONTRATOS\dados_orcamento_tmult.json"

with open(gerador_file, "r", encoding="utf-8") as f:
    content = f.read()

old_1_6 = """- **Concreto fck 30 MPa Vigas Baldrames VB1-VB19 (Comprimento Total Real L = 146,18m):** `L = 146,18m lineares`. Volume Total: `146,18m × 0,25m × 0,40m = 14,62 m³` (Conforme Leitura de Cotas Pranchas EGS-053/054; Com Perda 5%: `15,35 m³`).
- **Fôrmas Compensadas Vigas Baldrames:** `2 × 146,18m × 0,40m = 116,94 m²` (Conforme Leitura de Cotas Pranchas EGS-053/054) → **53 chapas** (`128,63 m²`)."""

new_1_6 = """- **Concreto fck 30 MPa Vigas Baldrames VB1-VB19 (Soma Vãos Livres L = 140,44m):** `L = 140,44m lineares`. Volume Total: `140,44m × 0,25m × 0,40m = 14,04 m³` (Com Perda 5%: `14,74 m³`).
- **Fôrmas Compensadas Vigas Baldrames:** `2 × 140,44m × 0,40m = 112,35 m²` (Apenas laterais dos vãos livres) → **52 chapas** (`125,84 m²`)."""

old_table = """| **VB1** | `EGS-053` | 560 + 240 + 30 + 295 + 560 + apoios (30+30+30+30+30) cm | **18.35 m** | 1.835 m³ | 14.68 m² |
| **VB2** | `EGS-053` | 380 + 161 + 380 + apoios (30+30+30+30) cm | **10.41 m** | 1.041 m³ | 8.33 m² |
| **VB3** | `EGS-053` | 560 + 560 + 560 + 275 + 260 + 560 + apoios (30+30+30+30+25+30+30) cm | **29.80 m** | 2.980 m³ | 23.84 m² |
| **VB4** | `EGS-053` | 380 + 161 + 380 + apoios (30+30+30+30) cm | **10.41 m** | 1.041 m³ | 8.33 m² |
| **VB5** | `EGS-053` | 380 + apoios (30+30) cm | **4.40 m** | 0.440 m³ | 3.52 m² |
| **VB6** | `EGS-053` | 380 + 161 + 380 + apoios (30+30+30+30) cm | **10.41 m** | 1.041 m³ | 8.33 m² |
| **VB7** | `EGS-054` | 380 + apoios (30+30) cm | **4.40 m** | 0.440 m³ | 3.52 m² |
| **VB8** | `EGS-054` | 189 + 346 + 275 + 260 + apoios (30+25+30+25+30) cm | **12.10 m** | 1.210 m³ | 9.68 m² |
| **VB9** | `EGS-054` | 380 + apoios (30+30) cm | **4.40 m** | 0.440 m³ | 3.52 m² |
| **VB10** | `EGS-054` | 426 + apoios (23+23) cm | **4.72 m** | 0.472 m³ | 3.78 m² |
| **VB11** | `EGS-054` | 426 + apoios (23+23) cm | **4.72 m** | 0.472 m³ | 3.78 m² |
| **VB12** | `EGS-054` | 426 + apoios (31+31) cm | **4.88 m** | 0.488 m³ | 3.90 m² |
| **VB13** | `EGS-054` | 380 + apoios (30+30) cm | **4.40 m** | 0.440 m³ | 3.52 m² |
| **VB14** | `EGS-054` | 426 + apoios (23+23) cm | **4.72 m** | 0.472 m³ | 3.78 m² |
| **VB15** | `EGS-054` | 206 + apoios (23+23) cm | **2.52 m** | 0.252 m³ | 2.02 m² |
| **VB16** | `EGS-054` | 206 + apoios (25+25) cm | **2.56 m** | 0.256 m³ | 2.05 m² |
| **VB17** | `EGS-054` | 304 + apoios (25+25) cm | **3.54 m** | 0.354 m³ | 2.83 m² |
| **VB18** | `EGS-054` | 426 + apoios (23+23) cm | **4.72 m** | 0.472 m³ | 3.78 m² |
| **VB19** | `EGS-054` | 426 + apoios (23+23) cm | **4.72 m** | 0.472 m³ | 3.78 m² |
| **TOTAL** | **-** | **Soma Real dos 19 Elementos** | **146.18 m** | **14.62 m³** | **116.94 m²** |"""

new_table = """| **VB1** | `EGS-053` | 560 + 560 + 560 + 240 + 295 + 560 (Apenas vãos livres) | **27.75 m** | 2.775 m³ | 22.20 m² |
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
| **TOTAL** | **-** | **Soma dos Vãos Livres (19 Elementos)** | **140.44 m** | **14.04 m³** | **112.35 m²** |"""

old_imperm = """- **Topo das Vigas Baldrames (apoio alvenaria):** `96,90m × 0,25m = 24,23 m²`
- **Laterais das Vigas Baldrames (contato solo):** `2 × 96,90m × 0,40m = 77,52 m²`
- **Topo das 32 Sapatas Isoladas (descontando 0,09m² do pilar):**
  - S1 (11 un × 0,91m² = 10,01 m²) | S3 (6 un × 1,12m² = 6,72 m²)
  - S7 (9 un × 0,72m² = 6,48 m²) | SE1 (6 un × 0,40m² = 2,40 m²)
  - Subtotal Topo Sapatas = `25,61 m²`
- **Arranques de Pilares (24 un h=0,35m enterrados):** `24 × 1,20m × 0,35m = 10,29 m²`
- **Área Total de Impermeabilização:** `24,23 + 77,52 + 25,61 + 10,29 =` **`137,65 m²`**
- **Quantidade Comercial UCC (Com Perda 10% de porosidade):** `137,65 m² × 1,10 = 151,42 m²` → **9 galões de 18L** (`162,00 m²`)."""

new_imperm = """- **Topo das Vigas Baldrames (apoio alvenaria):** `140,44m × 0,25m = 35,11 m²`
- **Laterais das Vigas Baldrames (contato solo):** `2 × 140,44m × 0,40m = 112,35 m²`
- **Topo das 32 Sapatas Isoladas (descontando 0,09m² do pilar):**
  - S1 (11 un × 0,91m² = 10,01 m²) | S3 (6 un × 1,12m² = 6,72 m²)
  - S7 (9 un × 0,72m² = 6,48 m²) | SE1 (6 un × 0,40m² = 2,40 m²)
  - Subtotal Topo Sapatas = `25,61 m²`
- **Arranques de Pilares (24 un h=0,35m enterrados):** `24 × 1,20m × 0,35m = 10,29 m²`
- **Área Total de Impermeabilização:** `35,11 + 112,35 + 25,61 + 10,29 =` **`183,36 m²`**
- **Quantidade Comercial UCC (Com Perda 10% de porosidade):** `183,36 m² × 1,10 = 201,70 m²` → **12 galões de 18L** (`216,00 m²`)."""

content = content.replace(old_1_6, new_1_6)
content = content.replace(old_table, new_table)
content = content.replace(old_imperm, new_imperm)

with open(gerador_file, "w", encoding="utf-8") as f:
    f.write(content)

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

for row in data["disciplinas"]["infraestrutura"]["rows"]:
    if row[0] == "1.1.7":
        row[1] = "Concreto Usinado fck 30 MPa para Vigas Baldrames VB1-VB19 (25x40cm - 140,44m)"
        row[3] = "14.04"
        row[6] = "14.74"
    elif row[0] == "1.1.8":
        row[1] = "Fôrma Compensado Resinado 17mm para Vigas Baldrames (140,44m)"
        row[3] = "112.35"
        row[6] = "52"
        row[7] = "chapas (125.84 m²)"
    elif row[0] == "1.1.14":
        row[3] = "183.36"
        row[6] = "201.70"
        row[7] = "m² (12 galões 18L)"

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Patch concluded successfully.")
