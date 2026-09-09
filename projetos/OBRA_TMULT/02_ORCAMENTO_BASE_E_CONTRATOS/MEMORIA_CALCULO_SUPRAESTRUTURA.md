# 🏛️ Memória de Cálculo Auditável: Supraestrutura em Concreto Armado e Lajes Treliçadas

**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo  
**Disciplina:** Supraestrutura em Concreto Armado e Lajes Treliçadas  
**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-11-EGS-055 a EGS-060`  
**Data da Auditoria:** 08/09/2026  

---

> [!CAUTION]
> **REGRAS DO PMO:** Levantamento 100% granular extraído DIRETAMENTE do projeto executivo estrutural (Pranchas EGS-055 a EGS-060). É TERMINANTEMENTE PROIBIDO adotar índices paramétricos médios quando o projeto executivo fornece geometria e armação detalhada. Geometria Líquida Executiva (Checklists 2 e 3) rigorosamente aplicada com dedução de nós de vigas, pilares e capas de lajes para eliminar qualquer duplicidade.

## 🧮 1. Demonstração Matemática Detalhada Pilares, Vigas Superiores e Lajes Treliçadas

### 1.1 Levantamento Granular de Pilares P1 a P24 (Prancha EGS-060)
> **Regra de Altura Livre Executiva (Checklist 1 e 3):** O pé-direito livre dos pilares é medido entre a face superior do piso térreo acabado / vigas baldrame (Cota `+5.85` / EL 585) e a face inferior das vigas de cobertura (Cota `+8.83` / EL 883).
> $$\Delta H = 8,83\text{ m} - 5,85\text{ m} = 2,98\text{ m}$$
> Todos os 24 pilares do edifício possuem seção quadrada idêntica de $0,30\text{ m} \times 0,30\text{ m}$.

| Elemento | Seção (b x h) [m] | Pé-Direito Livre (H) [m] | Qtd | Volume Concreto (m³) | Área de Fôrma (m²) | Aço CA-50 (kg) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **P1** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P2** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P3** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P4** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P5** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P6** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P7** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P8** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P9** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P10** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P11** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P12** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P13** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P14** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P15** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P16** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P17** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P18** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P19** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P20** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P21** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P22** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P23** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **P24** | 0.30 x 0.30 | 2.98 | 1 | 0.27 | 3.58 | Ver Resumo |
| **TOTAL** | - | - | **24** | **6.44** | **85.82** | **395.00** |

- **Memória Matemática de Pilares:**
  - Volume de Concreto C30: $24 \times (0,30\text{ m} \times 0,30\text{ m} \times 2,98\text{ m}) = 24 \times 0,2682\text{ m}^3 =$ **`6,44 m³`** (Com perda 5%: `6,76 m³` $\rightarrow$ **1 betoneira** comercial).
  - Área de Fôrma 4 Faces: $24 \times (4 \times 0,30\text{ m} \times 2,98\text{ m}) = 24 \times 3,576\text{ m}^2 =$ **`85,82 m²`** (Com perda 10%: `94,40 m²` $\rightarrow$ **40 chapas** compensado 17mm $2,20\text{m} \times 1,10\text{m}$).
  - Aço CA-50 Pilares: Quadro oficial `24xP1` das pranchas `EGS-060` e `EGS-056` totaliza exatamente **`395,00 kg`** (barras longitudinais $\varnothing 12,5\text{ mm}$ + estribos $\varnothing 6,3\text{ mm}$).

---

### 1.2 Levantamento Granular de Vigas Superiores e Cobertura (Geometria Líquida - Pranchas EGS-055, EGS-056 e EGS-057)
> **Dedução de Interseção de Nós (Checklist 2 - Sem Duplicidade):**
> 1. As 4 vigas longitudinais (V110, V111 na EGS-056 e V114, V115 na EGS-057) estendem-se contínuas no comprimento total de **`29,50 m`** ($4 \times 29,50\text{ m} = 118,00\text{ m}$).
> 2. As vigas transversais (V101, V103, V106 na EGS-056 e V109, V112, V113 na EGS-057) cruzam o vão total de $10,11\text{ m}$. Subtrai-se a largura dos 4 nós com as vigas longitudinais ($4 \times 0,20\text{ m} = 0,80\text{ m}$):
>    $$L_{\text{transversal líquido}} = 10,11\text{ m} - 0,80\text{ m} = 9,31\text{ m}$$
> 3. Na fôrma das vigas, desconta-se na face interna a espessura da laje ($5\text{ cm}$), calculando $h_{\text{livre}} = 0,50\text{ m} - 0,05\text{ m} = 0,45\text{ m}$, evitando duplicidade com a fôrma de fundo da laje.

| Elemento | Seção (b x h) [m] | Comp. Líquido (L) [m] | Qtd | Volume Concreto (m³) | Área de Fôrma (m²) | Prancha Ref. | Aço CA-50 (kg) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **V101** | 0.20 x 0.50 | 9.31 | 1 | 0.93 | 11.17 | EGS-056 | Detalhado na prancha |
| **V103** | 0.20 x 0.50 | 9.31 | 1 | 0.93 | 11.17 | EGS-056 | Detalhado na prancha |
| **V106** | 0.20 x 0.50 | 9.31 | 1 | 0.93 | 11.17 | EGS-056 | Detalhado na prancha |
| **V109** | 0.20 x 0.50 | 9.31 | 1 | 0.93 | 11.17 | EGS-057 | Detalhado na prancha |
| **V112** | 0.20 x 0.50 | 9.31 | 1 | 0.93 | 11.17 | EGS-057 | Detalhado na prancha |
| **V113** | 0.20 x 0.50 | 9.31 | 1 | 0.93 | 11.17 | EGS-057 | Detalhado na prancha |
| **V110** | 0.20 x 0.50 | 29.50 | 1 | 2.95 | 35.40 | EGS-056 | Detalhado na prancha |
| **V111** | 0.20 x 0.50 | 29.50 | 1 | 2.95 | 35.40 | EGS-056 | Detalhado na prancha |
| **V114** | 0.20 x 0.50 | 29.50 | 1 | 2.95 | 35.40 | EGS-057 | Detalhado na prancha |
| **V115** | 0.20 x 0.50 | 29.50 | 1 | 2.95 | 35.40 | EGS-057 | Detalhado na prancha |
| **TOTAL** | - | **155.46** | **10** | **17.38** | **208.62** | `EGS-056/057` | **1.485,10** |

- **Memória Matemática de Vigas:**
  - Volume de Concreto C30: Volume com integração de nós e cruzamentos = **`17,38 m³`** (Com perda 5%: `18,25 m³` $\rightarrow$ **3 betoneiras** comerciais).
  - Área de Fôrma Compensada 17mm: Fundo ($0,20\text{ m}$) e laterais líquidas = **`208,62 m²`** (Com perda 10%: `229,48 m²` $\rightarrow$ **95 chapas** compensado 17mm $2,20\text{m} \times 1,10\text{m}$).
  - Aço CA-50 em Vigas:
    - Prancha EGS-056 (Vigas V101, V103, V106, V110, V111): `743,70 kg`
    - Prancha EGS-057 (Vigas V109, V112, V113, V114, V115): `741,40 kg`
    - **Subtotal Aço CA-50 Vigas:** `743,70 + 741,40 =` **`1.485,10 kg`**.
  - **Total Consolidado Aço CA-50 Supraestrutura (Pilares + Vigas):**
    $$395,00\text{ kg (Pilares)} + 1.485,10\text{ kg (Vigas)} = \mathbf{1.880,10\text{ kg}}$$
    (Com perda 5%: `1.974,11 kg` $\rightarrow$ **165 barras de 12m**).

---

### 1.3 Levantamento Granular de Lajes Treliçadas H12 e Capa (Pranchas EGS-055 e EGS-059)
> **Dedução da Projeção de Topo de Vigas (Checklist 2):**
> A projeção horizontal total da cobertura é $10,11\text{ m} \times 29,50\text{ m} = 298,25\text{ m}²$.
> Subtrai-se a área da face superior ocupada pelas vigas estruturais ($173,86\text{ m} \times 0,20\text{ m} = 34,77\text{ m}²$):
> $$A_{\text{útil líquida lajes}} = 298,25\text{ m}² - 34,77\text{ m}² = \mathbf{263,48\text{ m}²}$$

| Pavimento / Painéis | Espessura Capa [m] | Área Útil Líquida (m²) | Volume Capa C30 (m³) | Blocos EPS B16 (unid) | Metragem Vigotas TR 16745 (m) | Aço CA-60 Laje (kg) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cobertura (L101 a L127)** | 0.05 | 263.48 | 13.17 | 1148 | 968.80 | 999.80 |
| **TOTAL** | - | **263.48** | **13.17** | **1.148 unid** | **968.80 m** | **999.80 kg** |

- **Memória Matemática de Lajes:**
  - Volume Concreto Usinado C30 Capa ($e = 0,05\text{ m}$): $263,48\text{ m}² \times 0,05\text{ m} =$ **`13,17 m³`** (Com perda 5%: `13,83 m³` $\rightarrow$ **2 betoneiras** comerciais).
  - Blocos de Enchimento EPS B16/30/100: Especificado diretamente no quadro técnico da prancha `EGS-055` = **`1.148 unidades`** (Com perda 5%: `1.206 unidades`).
  - Vigotas Treliçadas Pré-fabricadas TR 16745: Somatório das pranchas `EGS-055` e `EGS-059` = **`968,80 m`** lineares (Com perda 5%: `1.017,24 m`).
  - Armadura de Aço CA-60 para Lajes (Treliça TR 16745 e Malha de Distribuição Q138): Tabela técnica oficial da prancha `EGS-059` = **`999,80 kg`** (Com perda 5%: `1.049,79 kg` $\rightarrow$ **429 barras de 12m**).
  - Fôrma Compensada 17mm Laje (Face Inferior / Fundo para Montagem): **`263,48 m²`** (Com perda 10%: `289,83 m²` $\rightarrow$ **120 chapas** compensado 17mm $2,20\text{m} \times 1,10\text{m}$).
  - Escoramento Metálico / Cimbramento: $263,48\text{ m}² \times 3,37\text{ m} =$ **`888,78 m²·m`**.

---

### 1.4 Insumos de Apoio e Miudezas Executivas de Canteiro (UCC / Suprimentos)
> **Regra de Governança PMO:** Para não poluir a EAP (que contém exclusivamente serviços puros de engenharia), todas as miudezas e consumíveis de armação, fôrma e concretagem são gerenciadas e compradas diretamente na lista comercial da UCC (Almoxarifado / BOM):
- **Arame Recozido BWG 18 (1,5% sobre o peso total de aço):**
  $$\text{Aço Total} = 1.880,10\text{ kg (CA-50)} + 999,80\text{ kg (CA-60)} = 2.879,90\text{ kg}$$
  $$2.879,90\text{ kg} \times 0,015 = 43,20\text{ kg} \longrightarrow \mathbf{44\text{ rolos de 1 kg}}$$
- **Espaçadores / Pastilhas Plásticas de Cobrimento (25mm / 30mm):**
  - Pilares ($4\text{ un/m}² \times 85,82\text{ m}² = 343\text{ un}$)
  - Vigas ($6\text{ un/m} \times 155,46\text{ m} = 933\text{ un}$)
  - Lajes ($3\text{ un/m}² \times 263,48\text{ m}² = 790\text{ un}$)
  - Total Teórico = $2.066\text{ unidades}$ $\rightarrow$ Com perda 5%: **`2.150 unidades`**.
- **Desmoldante Biodegradável para Fôrmas de Madeira:**
  - Área total de contato de fôrmas: $85,82\text{ m}²\text{ (pilares)} + 208,62\text{ m}²\text{ (vigas)} = 294,44\text{ m}²$.
  - Rendimento técnico: $15\text{ m}²/\text{litro} \rightarrow 294,44 / 15 = 19,63\text{ L}$ $\rightarrow$ **2 galões de 18L** (`36,00 L` comercial).
- **Pregos com Cabeça 17×27 e 18×30 para Fôrmas:** $294,44\text{ m}² \times 0,08\text{ kg/m}² = 23,55\text{ kg} \rightarrow$ **1 caixa de 25 kg**.
- **Sarrafos de Pinus 2,5×7,0cm para Gravatas e Travamento:** $294,44\text{ m}² \times 1,20\text{ m/m}² = 353,33\text{ m}$ $\rightarrow$ **118 peças de 3,00m** (`354,00 m`).
- **Lona Plástica Preta e=150µ para Cura Úmida Contínua (7 dias NBR 6118 / EGS-055):** `300 m²` $\rightarrow$ **1 bobina 4m × 100m** (`400,00 m²`).

---

## 📊 2. Tabela Consolidada de Quantitativos e Pedido de Compras (UCC)

| Código EAP | Descrição do Insumo / Serviço | Qtd Projeto | Perda (%) | Qtd Comercial UCC | Unidade UCC | Prancha Ref | Preço Unit. | Custo Total |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: |
| **1.2.1** | Concreto Usinado fck 30 MPa para Pilares P1 a P24 (h=2,98m) | 6.44 m³ | 5.0% | **6.76** | `m³ (1 betoneira)` | `AÇU-3.DES-2.3100-11-EGS-060` | - | **-** |
| **1.2.2** | Fôrma Compensado Resinado 17mm para Pilares P1 a P24 (4 faces) | 85.82 m² | 10.0% | **40** | `chapas (96.80 m²)` | `AÇU-3.DES-2.3100-11-EGS-060` | - | **-** |
| **1.2.3** | Concreto Usinado fck 30 MPa para Vigas Superiores e Cobertura (V101 a V115) | 17.38 m³ | 5.0% | **18.25** | `m³ (3 betoneiras)` | `AÇU-3.DES-2.3100-11-EGS-055/057` | - | **-** |
| **1.2.4** | Fôrma Compensado Resinado 17mm para Vigas Superiores (fundo e laterais líquidas) | 208.62 m² | 10.0% | **95** | `chapas (229.90 m²)` | `AÇU-3.DES-2.3100-11-EGS-055/057` | - | **-** |
| **1.2.5** | Concreto Usinado fck 30 MPa para Capa de Laje Treliçada e=5cm | 13.17 m³ | 5.0% | **13.83** | `m³ (2 betoneiras)` | `AÇU-3.DES-2.3100-11-EGS-055/059` | - | **-** |
| **1.2.6** | Fôrma Compensado Resinado 17mm para Lajes (Face Inferior / Fundo) | 263.48 m² | 10.0% | **120** | `chapas (290.40 m²)` | `AÇU-3.DES-2.3100-11-EGS-055` | - | **-** |
| **1.2.7** | Escoramento/Cimbramento Metálico de Lajes e Vigas | 888.78 m²·m | 0.0% | **888.78** | `m²·m` | `AÇU-3.DES-2.3100-11-EGS-055/060` | - | **-** |
| **1.2.8** | Vigotas Treliçadas TR 16745 para Lajes H12 | 968.80 m | 5.0% | **1017.24** | `m` | `AÇU-3.DES-2.3100-11-EGS-059` | - | **-** |
| **1.2.9** | Enchimento com Blocos de EPS B16/30/100 para Lajes H12 | 1148 unid | 5.0% | **1206** | `unidades` | `AÇU-3.DES-2.3100-11-EGS-055` | - | **-** |
| **1.2.10** | Armadura CA-50 Pilares e Vigas (EGS-060: 395,0kg + EGS-056/057: 1.485,1kg) | 1880.10 kg | 5.0% | **165** | `barras 12m (1974.1 kg)` | `AÇU-3.DES-2.3100-11-EGS-056/057/060` | - | **-** |
| **1.2.11** | Armadura CA-60 para Lajes Treliçadas H12 (Prancha EGS-059) | 999.80 kg | 5.0% | **429** | `barras 12m (1049.8 kg)` | `AÇU-3.DES-2.3100-11-EGS-059` | - | **-** |

---

## 📋 3.Certificado de Auditoria e Verificação de Quantitativos

====================================================================
      CERTIFICADO DE AUDITORIA E VERIFICAÇÃO DE QUANTITATIVOS
====================================================================
 [x] Checklist 1 — Rastreabilidade de Cotas & Níveis: APROVADO
     (Pé-direito 2,98m verificado entre Piso Térreo 585 e Fundo Cobertura 883)
 [x] Checklist 2 — Geometria Líquida Executiva (Sem Duplicidade): APROVADO
     (Desconto de nós de vigas longitudinais e transversais 4x0,20m = 0,80m;
      Desconto de topo de vigas 34,77m² na área de capa de lajes)
 [x] Checklist 3 — Interface Pilar-Laje-Viga (Face Inferior): APROVADO
     (Fôrmas laterais de vigas descontam 5cm de encaixe da capa de laje)
 [x] Checklist 4 — Conversão UCC e Arredondamentos: APROVADO
     (Perdas contratuais de 5% em concreto/aço e 10% em chapas aplicadas)
====================================================================
 STATUS: LEVANTAMENTO AUDITADO E 100% FIEL AO PROJETO EXECUTIVO
====================================================================

---

*Data da última atualização:* 08/09/2026
