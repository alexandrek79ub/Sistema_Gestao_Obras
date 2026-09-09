import os
import csv

dest_dir = r'c:\Users\Alexandre\Workspace\A11_SISTEMA_DE_GESTAO_OBRAS\projetos\OBRA_TMULT\02_ORCAMENTO_BASE_E_CONTRATOS'
os.makedirs(dest_dir, exist_ok=True)

# 1. WRITE CSV
csv_path = os.path.join(dest_dir, 'QUANTITATIVO_SUPRAESTRUTURA.csv')
items = [
    {'eap': '1.2.1', 'item': 'Concreto Armado C30 para Pilares P1 a P24 (h=2,98m)', 'unidade': 'm³', 'qtd_projeto': 7.15, 'perda_pct': 4.0, 'qtd_comercial_ucc': 7.44, 'unidade_ucc': 'm³ usinado', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-060'},
    {'eap': '1.2.2', 'item': 'Fôrma de Compensado Resinado 17mm para Pilares P1 a P24 (4 faces)', 'unidade': 'm²', 'qtd_projeto': 92.98, 'perda_pct': 10.0, 'qtd_comercial_ucc': 102.28, 'unidade_ucc': 'm² (35 chapas 1,10x2,20m)', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-060'},
    {'eap': '1.2.3', 'item': 'Concreto Armado C30 para Vigas Elevadas e Cobertura (V101 a V115)', 'unidade': 'm³', 'qtd_projeto': 14.20, 'perda_pct': 4.0, 'qtd_comercial_ucc': 14.77, 'unidade_ucc': 'm³ usinado', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-055/060'},
    {'eap': '1.2.4', 'item': 'Fôrma de Compensado Resinado 17mm para Vigas Elevadas (fundo e laterais)', 'unidade': 'm²', 'qtd_projeto': 149.10, 'perda_pct': 10.0, 'qtd_comercial_ucc': 164.01, 'unidade_ucc': 'm² (56 chapas 1,10x2,20m)', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-055/060'},
    {'eap': '1.2.5', 'item': 'Concreto Armado C30 para Capa e Nervuras de Lajes L1 e L2', 'unidade': 'm³', 'qtd_projeto': 31.31, 'perda_pct': 4.0, 'qtd_comercial_ucc': 32.56, 'unidade_ucc': 'm³ usinado', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-055/056'},
    {'eap': '1.2.6', 'item': 'Fôrma/Forma de Lajes Nervuradas (L1 e L2)', 'unidade': 'm²', 'qtd_projeto': 368.40, 'perda_pct': 10.0, 'qtd_comercial_ucc': 405.24, 'unidade_ucc': 'm² (135 chapas 1,10x2,20m)', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-055/056'},
    {'eap': '1.2.7', 'item': 'Escoramento e Cimbramento Metálico para Lajes e Vigas (h=2,98m)', 'unidade': 'm²', 'qtd_projeto': 368.40, 'perda_pct': 0.0, 'qtd_comercial_ucc': 368.40, 'unidade_ucc': 'm² mês', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-055/056'},
    {'eap': '1.2.8.1', 'item': 'Aço CA-50 Ø 6.3mm (Estribos Pilares e Vigas Elevadas)', 'unidade': 'kg', 'qtd_projeto': 164.90, 'perda_pct': 5.0, 'qtd_comercial_ucc': 59.00, 'unidade_ucc': 'barras de 12m (173.1kg)', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-057/060'},
    {'eap': '1.2.8.2', 'item': 'Aço CA-50 Ø 8.0mm (Armação Auxiliar Vigas Elevadas)', 'unidade': 'kg', 'qtd_projeto': 112.60, 'perda_pct': 5.0, 'qtd_comercial_ucc': 25.00, 'unidade_ucc': 'barras de 12m (118.2kg)', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-055/057'},
    {'eap': '1.2.8.3', 'item': 'Aço CA-50 Ø 12.5mm (Armação Longitudinal Pilares e Vigas)', 'unidade': 'kg', 'qtd_projeto': 388.20, 'perda_pct': 5.0, 'qtd_comercial_ucc': 36.00, 'unidade_ucc': 'barras de 12m (407.6kg)', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-055/057/060'},
    {'eap': '1.2.8.4', 'item': 'Aço CA-50 Ø 16.0mm (Armação Principal Pilares e Vigas)', 'unidade': 'kg', 'qtd_projeto': 361.30, 'perda_pct': 5.0, 'qtd_comercial_ucc': 21.00, 'unidade_ucc': 'barras de 12m (379.3kg)', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-055/057/060'},
    {'eap': '1.2.8.5', 'item': 'Aço CA-60 Treliça TR16745 (Lajes Nervuradas L1 e L2)', 'unidade': 'kg', 'qtd_projeto': 999.80, 'perda_pct': 5.0, 'qtd_comercial_ucc': 968.80, 'unidade_ucc': 'metros lineares (1049.8kg)', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-059'}
]

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['eap', 'item', 'unidade', 'qtd_projeto', 'perda_pct', 'qtd_comercial_ucc', 'unidade_ucc', 'ref_prancha'])
    writer.writeheader()
    writer.writerows(items)

print('CSV gerado:', csv_path)

# 2. WRITE MARKDOWN (NATIVE MARKDOWN FORMAT)
md_path = os.path.join(dest_dir, 'MEMORIA_CALCULO_SUPRAESTRUTURA.md')

md_content = """# 🏛️ Memória de Cálculo Auditável: Supraestrutura (Pilares, Vigas e Lajes)

**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo  
**Disciplina:** Engenharia de Custos / Estrutura de Concreto Armado  
**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-11-EGS-055`, `EGS-056`, `EGS-057`, `EGS-059` e `EGS-060` (Rev A)  
**Data da Auditoria:** 08/09/2026  

---

## 🧮 1. Fórmulas Matemáticas e Regras de Engenharia Utilizadas

### 1.1 Volume de Concreto de Pilares (V_pilar)
> **Fórmula:** `V_pilar = N × (b × h × H_útil)`
- **N:** 24 Pilares (`P1` a `P24`).
- **b, h:** Seção transversal do pilar (`0,25 m × 0,40 m`).
- **H_útil:** Pé-direito de andar (`2,98 m` - Nível Térreo `585` até Cobertura `883`).

### 1.2 Área de Fôrma de Pilares (4 Faces)
> **Fórmula:** `A_forma_pilar = N × [2 × (b + h) × H_útil]`

### 1.3 Volume e Fôrma de Vigas Elevadas e Cobertura (V101 a V115)
> **Fórmula Volume:** `V_viga = b × h × L_eixos`  
> **Fórmula Fôrma (fundo + 2 laterais):** `A_forma_viga = (b + 2 × h) × L_eixos`
- **b:** `0,25 m` | **h:** `0,40 m` | **L_eixos:** `142,00 m` (Comprimento total das vigas elevadas).

### 1.4 Volume e Fôrma de Lajes Nervuradas (L1 e L2)
> **Fórmula Volume Capa + Nervuras:** `V_laje = A_planta × e_equivalente` (e_equivalente = `0,085 m`)  
> **Fórmula Cimbramento:** `A_cimbramento = A_planta` (`368,40 m²`)

---

## 📐 2. Memória de Cálculo Detalhada por Elemento

### 2.1 Pilares P1 a P24 (Prancha EGS-060)

- **Quantidade:** 24 Pilares retangulares
- **Seção transversal:** `0,25 m × 0,40 m` (Área de seção = `0,10 m²`)
- **Pé-direito livre:** `2,98 m`
- **Cálculo do Volume de Concreto C30:**  
  `V_pilares = 24 × (0,25 m × 0,40 m × 2,98 m) = 24 × 0,298 m³` ➔ **7,15 m³**
- **Cálculo da Área de Fôrma (4 faces):**  
  `A_forma_pilares = 24 × [2 × (0,25 m + 0,40 m) × 2,98 m] = 24 × (1,30 × 2,98)` ➔ **92,98 m²**

---

### 2.2 Vigas Elevadas V101 a V115 (Pranchas EGS-055 e EGS-060)

- **Geometria:** Seção de `0,25 m × 0,40 m`
- **Comprimento Acumulado dos Eixos (L_total):** `142,00 m`
- **Cálculo do Volume de Concreto C30:**  
  `V_vigas = 0,25 m × 0,40 m × 142,00 m` ➔ **14,20 m³**
- **Cálculo da Área de Fôrma (fundo 0,25m + 2 laterais 0,40m = 1,05m perimetral):**  
  `A_forma_vigas = (0,25 m + 2 × 0,40 m) × 142,00 m = 1,05 m × 142,00 m` ➔ **149,10 m²**

---

### 2.3 Lajes L1 e L2 / Cobertura (Pranchas EGS-055, EGS-056 e EGS-059)

- **Área Total em Planta (L1 Térreo/Tipo + L2 Cobertura):** `368,40 m²`
- **Espessura equivalente de concreto (capa 6cm + nervuras):** `0,085 m`
- **Cálculo do Volume de Concreto C30:**  
  `V_lajes = 368,40 m² × 0,085 m` ➔ **31,31 m³**
- **Área de Fôrmas/Cubotas/Nervuras:** `368,40 m²` (Com perda 10%: **405,24 m²**)
- **Escoramento / Cimbramento Metálico:** `368,40 m²`

---

### 2.4 Memória de Cálculo do Aço CA-50 e CA-60 (Pranchas EGS-057 e EGS-059)

#### 🔸 Armadura CA-50 Pilares e Vigas Elevadas
- **Aço Ø 6,3 mm (Estribos Pilares e Vigas):**  
  `P_líquido = 164,90 kg` ➔ Com perda 5%: `164,90 × 1,05 = 173,10 kg` ➔ **59 barras de 12m**
- **Aço Ø 8,0 mm (Armação Auxiliar Vigas):**  
  `P_líquido = 112,60 kg` ➔ Com perda 5%: `112,60 × 1,05 = 118,20 kg` ➔ **25 barras de 12m**
- **Aço Ø 12,5 mm (Longitudinal Pilares e Vigas):**  
  `P_líquido = 388,20 kg` ➔ Com perda 5%: `388,20 × 1,05 = 407,60 kg` ➔ **36 barras de 12m**
- **Aço Ø 16,0 mm (Longitudinal Principal Pilares):**  
  `P_líquido = 361,30 kg` ➔ Com perda 5%: `361,30 × 1,05 = 379,30 kg` ➔ **21 barras de 12m**

#### 🔸 Armadura CA-60 Treliçada para Lajes (Prancha EGS-059)
- **Treliça TR16745 (L1 e L2):**  
  `P_líquido = 999,80 kg` (Comprimento total = `968,80 m`)  
  Com perda 5%: `999,80 × 1,05 = 1.049,80 kg` ➔ **968,8 metros lineares de treliças**

---

## 📊 3. Tabela Consolidada para EAP e Pedido de Compras (UCC)

| Código EAP | Descrição do Insumo / Serviço | Qtd Projeto | Perda (%) | Qtd Comercial UCC | Unidade UCC | Prancha Ref |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1.2.1** | Concreto Armado C30 para Pilares P1 a P24 | 7,15 m³ | 4,0% | **7,44** | `m³ usinado` | `AÇU-3.DES-2.3100-11-EGS-060` |
| **1.2.2** | Fôrma de Compensado Resinado 17mm para Pilares | 92,98 m² | 10,0% | **102,28** | `m² (35 chapas 1,10x2,20m)` | `AÇU-3.DES-2.3100-11-EGS-060` |
| **1.2.3** | Concreto Armado C30 para Vigas Elevadas V101-V115 | 14,20 m³ | 4,0% | **14,77** | `m³ usinado` | `AÇU-3.DES-2.3100-11-EGS-055/060` |
| **1.2.4** | Fôrma de Compensado Resinado para Vigas Elevadas | 149,10 m² | 10,0% | **164,01** | `m² (56 chapas 1,10x2,20m)` | `AÇU-3.DES-2.3100-11-EGS-055/060` |
| **1.2.5** | Concreto Armado C30 para Capa de Lajes L1 e L2 | 31,31 m³ | 4,0% | **32,56** | `m³ usinado` | `AÇU-3.DES-2.3100-11-EGS-055/056` |
| **1.2.6** | Fôrma/Forma de Lajes Nervuradas (L1 e L2) | 368,40 m² | 10,0% | **405,24** | `m² (135 chapas 1,10x2,20m)` | `AÇU-3.DES-2.3100-11-EGS-055/056` |
| **1.2.7** | Escoramento e Cimbramento Metálico | 368,40 m² | 0,0% | **368,40** | `m² mês` | `AÇU-3.DES-2.3100-11-EGS-055/056` |
| **1.2.8.1** | Aço CA-50 Ø 6,3mm (Estribos) | 164,90 kg | 5,0% | **59,00** | `barras de 12m (173,1 kg)` | `AÇU-3.DES-2.3100-11-EGS-057/060` |
| **1.2.8.2** | Aço CA-50 Ø 8,0mm (Vigas Elevadas) | 112,60 kg | 5,0% | **25,00** | `barras de 12m (118,2 kg)` | `AÇU-3.DES-2.3100-11-EGS-055/057` |
| **1.2.8.3** | Aço CA-50 Ø 12,5mm (Longitudinal) | 388,20 kg | 5,0% | **36,00** | `barras de 12m (407,6 kg)` | `AÇU-3.DES-2.3100-11-EGS-055/057/060` |
| **1.2.8.4** | Aço CA-50 Ø 16,0mm (Longitudinal Principal) | 361,30 kg | 5,0% | **21,00** | `barras de 12m (379,3 kg)` | `AÇU-3.DES-2.3100-11-EGS-055/057/060` |
| **1.2.8.5** | Aço CA-60 Treliça TR16745 (Lajes) | 999,80 kg | 5,0% | **968,80** | `m lineares (1.049,8 kg)` | `AÇU-3.DES-2.3100-11-EGS-059` |

---

## 🛒 4. Lista Consolidada de Pedido de Compras (UCC) — Supraestrutura

1. **Concreto Usinado C30 (Pilares + Vigas + Lajes):** **`56 m³`** *(Pedir 7 caminhões betoneira de 8 m³ com fck 30 MPa e slump 12±2 cm)*
2. **Aço Total CA-50 / CA-60:** **`2,13 toneladas` (2.128,0 kg)**:
   - Aço $\varnothing$ 6,3mm: **59 barras de 12m** (173,1 kg)
   - Aço $\varnothing$ 8,0mm: **25 barras de 12m** (118,2 kg)
   - Aço $\varnothing$ 12,5mm: **36 barras de 12m** (407,6 kg)
   - Aço $\varnothing$ 16,0mm: **21 barras de 12m** (379,3 kg)
   - Treliça CA-60 TR16745: **968,8 metros lineares** (1.049,8 kg)
3. **Fôrmas de Compensado Resinado 17mm (Pilares + Vigas + Lajes):** **`672 m²`** *(Pedir 226 chapas de 1,10m x 2,20m)*
4. **Escoramento e Cimbramento Metálico:** **`369 m²`** *(Locação para 1 mês de escoramento)*
5. **Arame Recozido Nº 18:** **`32 kg`** *(Consumo médio para armação de pilares e vigas)*

---

*Data da última atualização:* 08/09/2026
"""

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print('Markdown de Supraestrutura gerado:', md_path)
