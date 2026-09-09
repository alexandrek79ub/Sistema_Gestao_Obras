import os
import csv

def main():
    base_dir = r"c:\Users\Alexandre\Workspace\A11_SISTEMA_DE_GESTAO_OBRAS\projetos\OBRA_TMULT\02_ORCAMENTO_BASE_E_CONTRATOS"
    os.makedirs(base_dir, exist_ok=True)

    # ----------------------------------------------------
    # 1. INFRAESTRUTURA E FUNDAÇÕES (100% GRANULAR)
    # ----------------------------------------------------
    infra_csv_path = os.path.join(base_dir, "QUANTITATIVO_INFRAESTRUTURA_FUNDACOES.csv")
    infra_md_path = os.path.join(base_dir, "MEMORIA_CALCULO_INFRAESTRUTURA_FUNDACOES.md")

    infra_rows = [
        ["Código EAP", "Item / Descricao", "Disciplina", "Qtd Projeto", "Unidade Proj", "Perda (%)", "Qtd Comercial UCC", "Unidade UCC", "Prancha Referencia"],
        ["1.1.1", "Escavação Mecanizada/Manual de Cavas e Valas", "Infraestrutura", "148.50", "m³", "0.0", "148.50", "m³", "AÇU-3.DES-2.3100-11-EGS-051/052"],
        ["1.1.2", "Apiloamento e Compactação do Fundo de Vala", "Infraestrutura", "182.40", "m²", "0.0", "182.40", "m²", "AÇU-3.DES-2.3100-11-EGS-051/052"],
        ["1.1.3", "Lastro de Concreto Magro fck 15 MPa e=5cm", "Infraestrutura", "9.12", "m³", "5.0", "9.58", "m³ (1.2 betoneiras)", "AÇU-3.DES-2.3100-11-EGS-051/052"],
        ["1.1.4", "Fôrma Compensado Resinado 17mm para Blocos e Baldrame", "Infraestrutura", "284.60", "m²", "10.0", "129", "chapas (313.06 m²)", "AÇU-3.DES-2.3100-11-EGS-051/053"],
        ["1.1.5", "Concreto Usinado fck 30 MPa para Blocos B1-B6 e Baldrames VB1-VB12", "Infraestrutura", "42.80", "m³", "5.0", "44.94", "m³ (6 betoneiras 8m³)", "AÇU-3.DES-2.3100-11-EGS-051/054"],
        ["1.1.6", "Estaca Escavada Ø40cm (Profundidade 12m - 18 un)", "Infraestrutura", "216.00", "m", "0.0", "216.00", "m", "AÇU-3.DES-2.3100-11-EGS-051/052"],
        ["1.1.7", "Estaca Escavada Ø50cm (Profundidade 14m - 12 un)", "Infraestrutura", "168.00", "m", "0.0", "168.00", "m", "AÇU-3.DES-2.3100-11-EGS-051/052"],
        ["1.1.8", "Arrasamento e Preparação do Topo das Estacas", "Infraestrutura", "30.00", "unid", "0.0", "30", "unidades", "AÇU-3.DES-2.3100-11-EGS-051/052"],
        ["1.1.9", "Armadura CA-50 Ø10,0mm / Ø12,5mm (Blocos e Baldrames)", "Infraestrutura", "3450.00", "kg", "5.0", "302", "barras 12m (3622.5 kg)", "AÇU-3.DES-2.3100-11-EGS-053/054"],
        ["1.1.10", "Armadura CA-60 Ø6,3mm (Estribos Baldrame/Blocos)", "Infraestrutura", "870.00", "kg", "5.0", "373", "barras 12m (913.5 kg)", "AÇU-3.DES-2.3100-11-EGS-053/054"],
        ["1.1.11", "Arame Recozido BWG 18 para Amarrações de Fundação", "Infraestrutura", "64.80", "kg", "0.0", "65.00", "kg (65 rolos 1kg)", "AÇU-3.DES-2.3100-11-EGS-053/057"],
        ["1.1.12", "Espaçadores/Pastilhas de Concreto cobrimento 40mm", "Infraestrutura", "1250.00", "unid", "5.0", "1313", "unidades", "AÇU-3.DES-2.3100-11-EGS-051/054"],
        ["1.1.13", "Impermeabilização Tinta Asfáltica (Topo e Laterais Baldrame)", "Infraestrutura", "214.20", "m²", "10.0", "235.62", "m² (13 galões 18L)", "AÇU-3.DES-2.3100-11-EGS-051/054"],
        ["1.1.14", "Reaterro Compactado de Cavas e Valas c/ Maço/Sapo", "Infraestrutura", "96.58", "m³", "0.0", "96.58", "m³", "AÇU-3.DES-2.3100-11-EGS-051/052"],
        ["1.1.15", "Bota-fora e Carga de Terra c/ Empolamento 1,25", "Infraestrutura", "64.90", "m³", "0.0", "81.13", "m³ (7 caminhões 12m³)", "AÇU-3.DES-2.3100-11-EGS-051/052"]
    ]

    with open(infra_csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(infra_rows)

    infra_md_content = """# 🏛️ Memória de Cálculo Auditável: Infraestrutura e Fundações Completa

**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo  
**Disciplina:** Engenharia de Custos / Infraestrutura, Fundações & Terraplenagem  
**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-11-EGS-051` a `EGS-054` (Sapatas, Estacas, Baldrames e Armações)  
**Data da Auditoria:** 08/09/2026  

---

## 🧮 1. Fórmulas Matemáticas e Regras de Engenharia Utilizadas

### 1.1 Estacas Escavadas e Arrasamento
- **18 Estacas Ø40cm (Profundidade 12m):** `V = 18 × π × (0,20)² × 12 = 27,14 m³`.
- **12 Estacas Ø50cm (Profundidade 14m):** `V = 12 × π × (0,25)² × 14 = 32,99 m³`.
- **Arrasamento:** 30 cabeças de estacas rebaixadas e preparadas para topo de bloco.

### 1.2 Os 10 Serviços Integrados de Cava e Baldrame
- **Escavação de Valas/Cavas:** `148,50 m³`.
- **Apiloamento do Fundo de Vala:** `182,40 m²`.
- **Lastro de Concreto Magro e=5cm:** `9,12 m³` (Com perda 5%: `9,58 m³`).
- **Concreto fck 30 MPa (Blocos B1-B6 + Baldrames VB1-VB12):** `42,80 m³` (Com perda 5%: `44,94 m³`).
- **Fôrmas Compensadas Resinadas 17mm:** `284,60 m²` (Com perda 10%: `129 chapas`).
- **Armadura CA-50/60 (3.450kg CA-50 + 870kg CA-60):** `4.320 kg` + `65 kg arame recozido BWG 18` + `1.313 espaçadores 40mm`.
- **Impermeabilização Tinta Asfáltica Baldrames:** `214,20 m²` (13 galões 18L).
- **Reaterro Compactado:** `96,58 m³` | **Bota-fora (Empolamento 1,25):** `81,13 m³`.

---

## 📊 2. Tabela Consolidada de Pedido de Compras (UCC) — Fundações

1. **Concreto Usinado fck 30 MPa:** **`44,94 m³`** (6 betoneiras de 8m³)
2. **Concreto Magro fck 15 MPa (Lastro):** **`9,58 m³`**
3. **Chapas Compensado Resinado 17mm:** **`129 chapas`** (2,20m x 1,10m)
4. **Aço CA-50 Ø10,0mm / Ø12,5mm:** **`302 barras de 12m`** (3.622,5 kg)
5. **Aço CA-60 Ø6,3mm (Estribos):** **`373 barras de 12m`** (913,5 kg)
6. **Arame Recozido BWG 18:** **`65 kg`**
7. **Espaçadores de Concreto 40mm:** **`1.313 unidades`**
8. **Tinta Asfáltica Impermeável (Galões 18L):** **`13 galões`**

---

*Data da última atualização:* 08/09/2026
"""
    with open(infra_md_path, 'w', encoding='utf-8') as f:
        f.write(infra_md_content)

    # ----------------------------------------------------
    # 2. SUPRAESTRUTURA (100% GRANULAR)
    # ----------------------------------------------------
    supra_csv_path = os.path.join(base_dir, "QUANTITATIVO_SUPRAESTRUTURA.csv")
    supra_md_path = os.path.join(base_dir, "MEMORIA_CALCULO_SUPRAESTRUTURA.md")

    supra_rows = [
        ["Código EAP", "Item / Descricao", "Disciplina", "Qtd Projeto", "Unidade Proj", "Perda (%)", "Qtd Comercial UCC", "Unidade UCC", "Prancha Referencia"],
        ["1.2.1", "Concreto Usinado fck 30 MPa Pilares (P1 a P24 h=2,98m)", "Supraestrutura", "18.60", "m³", "5.0", "19.53", "m³ (3 betoneiras)", "AÇU-3.DES-2.3100-15-EGS-007/008"],
        ["1.2.2", "Concreto Usinado fck 30 MPa Vigas Superiores (V1 a V18)", "Supraestrutura", "34.20", "m³", "5.0", "35.91", "m³ (5 betoneiras)", "AÇU-3.DES-2.3100-15-EGS-009/010"],
        ["1.2.3", "Concreto Usinado fck 30 MPa Laje Treliçada/Maciça (Capela/Capa e=5cm)", "Supraestrutura", "22.10", "m³", "5.0", "23.21", "m³ (3 betoneiras)", "AÇU-3.DES-2.3100-15-EGS-011/012"],
        ["1.2.4", "Fôrma Compensado Resinado 17mm Pilares (P1 a P24)", "Supraestrutura", "248.00", "m²", "10.0", "113", "chapas (272.80 m²)", "AÇU-3.DES-2.3100-15-EGS-007/008"],
        ["1.2.5", "Fôrma Compensado Resinado 17mm Vigas Superiores (3 Lados)", "Supraestrutura", "312.40", "m²", "10.0", "142", "chapas (343.64 m²)", "AÇU-3.DES-2.3100-15-EGS-009/010"],
        ["1.2.6", "Fôrma Compensado Resinado 17mm Laje (Face Inferior)", "Supraestrutura", "368.40", "m²", "10.0", "168", "chapas (405.24 m²)", "AÇU-3.DES-2.3100-15-EGS-011/012"],
        ["1.2.7", "Escoramento/Cimbramento Metálico de Lajes e Vigas (PD=3,20m)", "Supraestrutura", "1178.88", "m²·m", "0.0", "1178.88", "m²·m", "AÇU-3.DES-2.3100-15-EGS-009/012"],
        ["1.2.8", "Laje Treliçada H12 TR8645 c/ Enchimento EPS", "Supraestrutura", "368.40", "m²", "5.0", "386.82", "m² (Vigotas+Vigotes)", "AÇU-3.DES-2.3100-15-EGS-011/012"],
        ["1.2.9", "Armadura CA-50 Ø10,0mm / Ø12,5mm / Ø16,0mm (Pilares, Vigas, Laje)", "Supraestrutura", "7840.00", "kg", "5.0", "686", "barras 12m (8232.0 kg)", "AÇU-3.DES-2.3100-15-EGS-007/012"],
        ["1.2.10", "Armadura CA-60 Ø5,0mm / Ø6,3mm (Estribos e Malha Negativa)", "Supraestrutura", "2120.00", "kg", "5.0", "909", "barras 12m (2226.0 kg)", "AÇU-3.DES-2.3100-15-EGS-007/012"],
        ["1.2.11", "Arame Recozido BWG 18 para Amarrações de Superestrutura", "Supraestrutura", "149.40", "kg", "0.0", "150.00", "kg (150 rolos 1kg)", "AÇU-3.DES-2.3100-15-EGS-007/012"],
        ["1.2.12", "Espaçadores/Pastilhas Plásticas de Cobrimento 25mm/30mm", "Supraestrutura", "2850.00", "unid", "5.0", "2993", "unidades", "AÇU-3.DES-2.3100-15-EGS-007/012"],
        ["1.2.13", "Desmoldante Biodegradável para Fôrmas de Concreto", "Supraestrutura", "45.00", "L", "0.0", "3", "galões de 18L (54L)", "AÇU-3.DES-2.3100-15-EGS-007/012"]
    ]

    with open(supra_csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(supra_rows)

    supra_md_content = """# 🏗️ Memória de Cálculo Auditável: Supraestrutura Completa

**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo  
**Disciplina:** Engenharia de Custos / Supraestrutura em Concreto Armado  
**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-15-EGS-007` a `EGS-012`  
**Data da Auditoria:** 08/09/2026  

---

## 🧮 1. Fórmulas Matemáticas e Regras de Engenharia Utilizadas

### 1.1 Concreto e Fôrmas de Pilares, Vigas e Lajes
- **Pilares (P1 a P24 h=2,98m):** Concreto `18,60 m³` (Com perda 5%: `19,53 m³`) | Fôrmas `248,00 m²` (113 chapas).
- **Vigas Superiores (V1 a V18):** Concreto `34,20 m³` (Com perda 5%: `35,91 m³`) | Fôrmas `312,40 m²` (142 chapas).
- **Laje Treliçada H12 e Capa e=5cm:** Concreto Capa `22,10 m³` (Com perda 5%: `23,21 m³`) | Fôrmas `368,40 m²` (168 chapas) | Vigotas H12 EPS `386,82 m²`.
- **Cimbramento/Escoramento (PD=3,20m):** `368,40 m² × 3,20 m = 1.178,88 m²·m`.

### 1.2 Armadura, Arame e Acessórios de Cobrimento
- **Aço CA-50 (Pilares, Vigas, Laje):** `7.840 kg` (Com perda 5%: `686 barras 12m`).
- **Aço CA-60 (Estribos e Malha Negativa):** `2.120 kg` (Com perda 5%: `909 barras 12m`).
- **Arame Recozido BWG 18:** `150 kg` (1,5% do peso de aço).
- **Espaçadores Plásticos 25mm/30mm:** `2.993 unidades`.
- **Desmoldante Biodegradável para Fôrmas:** `3 galões de 18L` (54L).

---

## 📊 2. Tabela Consolidada de Pedido de Compras (UCC) — Supraestrutura

1. **Concreto Usinado fck 30 MPa:** **`78,65 m³`** (10 betoneiras de 8m³)
2. **Chapas Compensado Resinado 17mm:** **`423 chapas`** (2,20m x 1,10m)
3. **Escoramento Metálico Cimbramento:** **`1.178,88 m²·m`**
4. **Laje Treliçada H12 EPS:** **`386,82 m²`**
5. **Aço CA-50 (10,0/12,5/16,0mm):** **`686 barras de 12m`** (8.232,0 kg)
6. **Aço CA-60 (5,0/6,3mm):** **`909 barras de 12m`** (2.226,0 kg)
7. **Arame Recozido BWG 18:** **`150 kg`**
8. **Espaçadores Plásticos 25mm/30mm:** **`2.993 unidades`**
9. **Desmoldante Biodegradável Fôrmas (Galões 18L):** **`3 galões`**

---

*Data da última atualização:* 08/09/2026
"""
    with open(supra_md_path, 'w', encoding='utf-8') as f:
        f.write(supra_md_content)

    print(f"Fundações Completa e Granular gerada: {infra_csv_path}")
    print(f"Supraestrutura Completa e Granular gerada: {supra_csv_path}")

if __name__ == "__main__":
    main()
