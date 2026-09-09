import os
import csv

def main():
    base_dir = r"c:\Users\Alexandre\Workspace\A11_SISTEMA_DE_GESTAO_OBRAS\projetos\OBRA_TMULT\02_ORCAMENTO_BASE_E_CONTRATOS"
    os.makedirs(base_dir, exist_ok=True)

    csv_path = os.path.join(base_dir, "QUANTITATIVO_INSTALACOES_HVAC.csv")
    md_path = os.path.join(base_dir, "MEMORIA_CALCULO_INSTALACOES_HVAC.md")

    # CSV Data
    rows = [
        ["Código EAP", "Item / Descricao", "Disciplina", "Qtd Projeto", "Unidade Proj", "Perda (%)", "Qtd Comercial UCC", "Unidade UCC", "Prancha Referencia"],
        
        # Elétrica
        ["3.1.1", "Cabo de Cobre Flexível 750V 2,5 mm² (Fase/Neutro/Retorno)", "Elétrica", "1850.0", "m", "10.0", "21", "rolos de 100m (2035.0 m)", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.2", "Cabo de Cobre Flexível 750V 4,0 mm² (Circuitos TUG/TUE)", "Elétrica", "640.0", "m", "10.0", "8", "rolos de 100m (704.0 m)", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.3", "Cabo de Cobre Flexível 750V 6,0 mm² (Ar Condicionado/Alimentadores)", "Elétrica", "420.0", "m", "10.0", "5", "rolos de 100m (462.0 m)", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.4", "Cabo de Cobre Sintenax 0,6/1kV 35,0 mm² (Alimentador Geral)", "Elétrica", "120.0", "m", "5.0", "126.0", "m", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.5", "Eletroduto Rígido PVC Ø3/4\" (25mm) com Conexões", "Elétrica", "480.0", "m", "10.0", "176", "varas de 3m (528.0 m)", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.6", "Eletroduto Rígido PVC Ø1\" (32mm) com Conexões", "Elétrica", "210.0", "m", "10.0", "77", "varas de 3m (231.0 m)", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.7", "Quadro de Distribuição Geral (QDG) completo com Barramento 150A", "Elétrica", "1.0", "unid", "0.0", "1", "unidade", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.8", "Quadro de Distribuição de Luz e Tomadas (QDF) 24 Elementos", "Elétrica", "2.0", "unid", "0.0", "2", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.9", "Luminária LED Embutir Painel 60x60cm 40W 4000K", "Elétrica", "68.0", "unid", "5.0", "72", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.10", "Luminária Hermética LED 2x18W (Áreas Técnicas/Externas)", "Elétrica", "16.0", "unid", "5.0", "17", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.11", "Bloco de Iluminação de Emergência LED 2x8W com Bateria", "Elétrica", "14.0", "unid", "0.0", "14", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.12", "Tomada 2P+T 10A / 250V Completa com Espelho", "Elétrica", "86.0", "unid", "5.0", "91", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.13", "Tomada 2P+T 20A / 250V (TUE/Cozinha/Equipamentos)", "Elétrica", "24.0", "unid", "5.0", "26", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.14", "Interruptor Simples / Paralelo 10A Completo", "Elétrica", "28.0", "unid", "5.0", "30", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.15", "Haste de Aterramento Copperweld 3/4\" x 3,00m + Malha 50mm²", "Elétrica", "6.0", "unid", "0.0", "6", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-013"],
        
        # Hidrossanitária e Pluvial
        ["3.2.1", "Tubo PVC Soldável Água Fria Ø25mm (3/4\")", "Hidráulica", "180.0", "m", "10.0", "33", "varas de 6m (198.0 m)", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.2", "Tubo PVC Soldável Água Fria Ø50mm (1.1/2\")", "Hidráulica", "95.0", "m", "10.0", "18", "varas de 6m (108.0 m)", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.3", "Tubo PVC Esgoto Série Normal Ø40mm", "Hidráulica", "64.0", "m", "10.0", "12", "varas de 6m (72.0 m)", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.4", "Tubo PVC Esgoto Série Normal Ø100mm", "Hidráulica", "140.0", "m", "10.0", "26", "varas de 6m (156.0 m)", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.5", "Tubo PVC Pluvial Série Reforçada Ø150mm", "Hidráulica", "110.0", "m", "10.0", "21", "varas de 6m (126.0 m)", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.6", "Reservatório de Água Potável Polietileno 5.000 L", "Hidráulica", "2.0", "unid", "0.0", "2", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.7", "Bacia Sanitária com Caixa Acoplada 3/6L e Assento", "Hidráulica", "10.0", "unid", "0.0", "10", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.8", "Lavatório Louça Branca com Torneira Automática/Bancada", "Hidráulica", "12.0", "unid", "0.0", "12", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.9", "Caixa Sifonada PVC 150x150x50mm Grelha Inox", "Hidráulica", "14.0", "unid", "0.0", "14", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.10", "Caixa de Gordura Pré-moldada de Concreto 100L", "Hidráulica", "2.0", "unid", "0.0", "2", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.11", "Caixa de Inspeção Esgoto Concreto 60x60x60cm com Tampa", "Hidráulica", "6.0", "unid", "0.0", "6", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],

        # HVAC - Climatização e Exaustão
        ["3.3.1", "Aparelho Split Cassete 36.000 BTU/h Inverter R410A (Salas Maiores)", "HVAC", "4.0", "unid", "0.0", "4", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-008"],
        ["3.3.2", "Aparelho Split Hi-Wall 18.000 BTU/h Inverter R410A (Salas Médias)", "HVAC", "6.0", "unid", "0.0", "6", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-008"],
        ["3.3.3", "Aparelho Split Hi-Wall 12.000 BTU/h Inverter R410A (Salas Individuais)", "HVAC", "6.0", "unid", "0.0", "6", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-008"],
        ["3.3.4", "Tubulação de Cobre Flexível Ø3/8\" + Ø5/8\" com Isolamento Elastomérico", "HVAC", "180.0", "m", "10.0", "198.0", "m", "AÇU-3.DES-2.3100-15-EGS-008"],
        ["3.3.5", "Tubo PVC Condensado Ø25mm com Isolamento", "HVAC", "120.0", "m", "10.0", "22", "varas de 6m (132.0 m)", "AÇU-3.DES-2.3100-15-EGS-008"],
        ["3.3.6", "Exaustor Axial de Parede/Teto 150 m³/h (Sanitários/Copa)", "HVAC", "6.0", "unid", "0.0", "6", "unidades", "AÇU-3.DES-2.3100-15-EGS-008"]
    ]

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    # Markdown Content
    md_content = """# ⚡💧❄️ Memória de Cálculo Auditável: Instalações Elétricas, Hidrossanitárias e HVAC

**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo  
**Disciplina:** Engenharia de Custos / Instalações Prediais & Climatização  
**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-15-EGS-013` (Elétrica), `EGS-015` (Hidrosanitária) e `EGS-008` (HVAC)  
**Data da Auditoria:** 08/09/2026  

---

## 🧮 1. Fórmulas Matemáticas e Regras de Engenharia Utilizadas

### 1.1 Instalações Elétricas (Cabeamento e Eletrodutos)
> **Fórmula Metragem de Cabos:** `L_cabo = Σ (L_trajeto × N_condutores) × (1 + Perda)`  
> **Fórmula Eletrodutos:** `L_eletroduto = Σ L_trajeto × (1 + Perda)`
- **Taxa de Ocupação Máxima de Eletrodutos:** `40%` (conforme NBR 5410).
- **Perda estimada para curvaturas e sobras nas caixas (4x2 e QDG):** `10,0%`.

### 1.2 Instalações Hidrossanitárias e Pluviais
> **Fórmula Tubulações:** `L_comercial = CEIL( L_projeto × (1 + Perda) / L_vara ) × L_vara`
- **Comprimento padrão da vara PVC:** `6,00 metros`.
- **Perda estimada por recortes e conexões:** `10,0%`.

### 1.3 Climatização (HVAC)
> **Fórmula Carga Térmica Estimada:** `Q_total = Carga_especifica × Área_útil`  
> `Q_total = 700 BTU/h/m² × 368,40 m² = 257.880 BTU/h`
- **Capacidade instalada dimensionada:** `336.000 BTU/h` (distribuídos em 16 evaporadoras Cassete/Hi-Wall com redundância N+1).

---

## 📐 2. Memória de Cálculo Detalhada por Disciplina

### 2.1 Instalações Elétricas (Prancha EGS-013)
- **Quadros de Distribuição:** 1 QDG-150A + 2 QDF-24 elementos.
- **Cabeamento Flexível 750V 2,5mm²:** `1.850 m projeto` ➔ Com perda 10%: `2.035 m` (**21 rolos de 100m**).
- **Cabeamento Flexível 750V 4,0mm²:** `640 m projeto` ➔ Com perda 10%: `704 m` (**8 rolos de 100m**).
- **Cabeamento Flexível 750V 6,0mm²:** `420 m projeto` ➔ Com perda 10%: `462 m` (**5 rolos de 100m**).
- **Cabeamento Sintenax 35,0mm² (Alimentador Geral):** `120 m projeto` ➔ Com perda 5%: **126,0 m**.
- **Pontos de Iluminação Painel LED 60x60cm 40W:** `68 un projeto` ➔ Com reserva 5%: **72 unidades**.
- **Tomadas TUG/TUE 10A/20A:** `110 un projeto` ➔ Com reserva 5%: **117 unidades**.
- **Sistema de Aterramento:** 6 Hastes Copperweld 3/4" x 3,00m + 80m Cabo Cobre Nu 50mm².

---

### 2.2 Instalações Hidrossanitárias (Prancha EGS-015)
- **Tubulação Água Fria Ø25mm:** `180 m projeto` ➔ Com perda 10%: `198 m` (**33 varas de 6m**).
- **Tubulação Água Fria Ø50mm:** `95 m projeto` ➔ Com perda 10%: `108 m` (**18 varas de 6m**).
- **Tubulação Esgoto Ø40mm:** `64 m projeto` ➔ Com perda 10%: `72 m` (**12 varas de 6m**).
- **Tubulação Esgoto Ø100mm:** `140 m projeto` ➔ Com perda 10%: `156 m` (**26 varas de 6m**).
- **Tubulação Pluvial Ø150mm:** `110 m projeto` ➔ Com perda 10%: `126 m` (**21 varas de 6m**).
- **Reservatórios de Água Potável:** 2 Caixas d'Água Polietileno 5.000 Litros.
- **Louças e Metais:** 10 Bacias Sanitárias C/CA, 12 Lavatórios com torneira automática, 14 Caixas sifonadas 150x150mm.

---

### 2.3 HVAC - Climatização e Exaustão (Prancha EGS-008)
- **Equipamentos Split Cassete 36.000 BTU/h Inverter:** **4 conjuntos** (Salas de reunião e estações integradas).
- **Equipamentos Split Hi-Wall 18.000 BTU/h Inverter:** **6 conjuntos** (Salas gerenciais e coordenação).
- **Equipamentos Split Hi-Wall 12.000 BTU/h Inverter:** **6 conjuntos** (Salas individuais e recepção).
- **Tubulação de Cobre Flexível Ø3/8" + Ø5/8" com Isolamento:** `180 m projeto` ➔ Com perda 10%: **198,0 m**.
- **Dreno de Condensado PVC Ø25mm:** `120 m projeto` ➔ Com perda 10%: `132 m` (**22 varas de 6m**).
- **Exaustores Axiais 150 m³/h:** **6 unidades** (Banheiros e apoio).

---

## 📊 3. Tabela Consolidada para EAP e Pedido de Compras (UCC)

| Código EAP | Descrição do Insumo / Serviço | Qtd Projeto | Perda (%) | Qtd Comercial UCC | Unidade UCC | Prancha Ref |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **3.1.1** | Cabo Cobre Flex 2,5mm² | 1850.0 m | 10.0% | **21** | `rolos 100m (2035m)` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.2** | Cabo Cobre Flex 4,0mm² | 640.0 m | 10.0% | **8** | `rolos 100m (704m)` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.3** | Cabo Cobre Flex 6,0mm² | 420.0 m | 10.0% | **5** | `rolos 100m (462m)` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.4** | Cabo Sintenax 35mm² | 120.0 m | 5.0% | **126,0** | `m` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.5** | Eletroduto PVC Ø3/4" (25mm) | 480.0 m | 10.0% | **176** | `varas de 3m (528m)` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.6** | Painel LED 60x60 40W | 68.0 un | 5.0% | **72** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.7** | Tomadas 10A/20A | 110.0 un | 5.0% | **117** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.2.1** | Tubo PVC Soldável Ø25mm | 180.0 m | 10.0% | **33** | `varas 6m (198m)` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **3.2.2** | Tubo PVC Esgoto Ø100mm | 140.0 m | 10.0% | **26** | `varas 6m (156m)` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **3.2.3** | Reservatório Polietileno 5.000L | 2.0 un | 0.0% | **2** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **3.2.4** | Bacia Sanitária C/ CA | 10.0 un | 0.0% | **10** | `conjuntos` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **3.3.1** | Split Cassete 36.000 BTU/h | 4.0 un | 0.0% | **4** | `conjuntos` | `AÇU-3.DES-2.3100-15-EGS-008` |
| **3.3.2** | Split Hi-Wall 18.000 BTU/h | 6.0 un | 0.0% | **6** | `conjuntos` | `AÇU-3.DES-2.3100-15-EGS-008` |
| **3.3.3** | Split Hi-Wall 12.000 BTU/h | 6.0 un | 0.0% | **6** | `conjuntos` | `AÇU-3.DES-2.3100-15-EGS-008` |
| **3.3.4** | Linha Cobre Flexível Ø3/8"+5/8" | 180.0 m | 10.0% | **198,0** | `m` | `AÇU-3.DES-2.3100-15-EGS-008` |

---

## 🛒 4. Lista Consolidada de Pedido de Compras (UCC) — Instalações & HVAC

1. **Cabo Flexível 750V 2,5 mm²:** **`21 rolos de 100m`**
2. **Cabo Flexível 750V 4,0 mm²:** **`8 rolos de 100m`**
3. **Cabo Flexível 750V 6,0 mm²:** **`5 rolos de 100m`**
4. **Painel LED Embutir 60x60cm 40W:** **`72 unidades`**
5. **Tomadas 10A/20A com Espelho:** **`117 conjuntos`**
6. **Varas Tubo PVC Água Fria Ø25mm (6m):** **`33 varas`**
7. **Varas Tubo PVC Esgoto Ø100mm (6m):** **`26 varas`**
8. **Caixas d'Água Polietileno 5.000 Litros:** **`2 unidades`**
9. **Louças Sanitárias Completas:** **`10 Bacias`** e **`12 Lavatórios`**
10. **Aparelhos Split Ar Condicionado Inverter:** **`4 Cassete 36.000 BTU`**, **`6 Hi-Wall 18.000 BTU`**, **`6 Hi-Wall 12.000 BTU`**

---

*Data da última atualização:* 08/09/2026
"""

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"CSV de Instalações gerado: {csv_path}")
    print(f"Markdown de Instalações gerado: {md_path}")

if __name__ == "__main__":
    main()
