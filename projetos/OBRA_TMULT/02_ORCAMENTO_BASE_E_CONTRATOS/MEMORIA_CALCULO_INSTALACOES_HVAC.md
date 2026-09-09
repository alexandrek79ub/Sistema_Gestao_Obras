# 🏛️ Memória de Cálculo Auditável: Instalações Elétricas, Telecom, Hidrossanitárias e HVAC

**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo  
**Disciplina:** Instalações Elétricas, Telecom, Hidrossanitárias e HVAC  
**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-16-EGS-013, EGS-015 e AÇU-3.DES-2.3100-64-EGS-008`  
**Data da Auditoria:** 08/09/2026  

---

## 🧮 1. Demonstração Matemática Detalhada dos Quantitativos de Instalações e HVAC

### 1.1 Instalações Elétricas e Telecomunicações (Prancha EGS-013 e Arquitetura EGS-015/EGS-018)
> **Metodologia de Cálculo Tridimensional (NBR 5410 / Skill MEP 04):**  
> Os quantitativos lineares de condutores e eletrodutos resultam do somatório dos percursos horizontais no forro/laje (Eixos X e Y) com as descidas e subidas verticais nas paredes até a cota de cada aparelho (Eixo Z), multiplicados pelo número de condutores por circuito e acrescidos das sobras de ponta em caixas e quadros.

- **Alimentador Geral de Força (Cabo de Cobre Sintenax 0,6/1kV 35mm²):**
  - Percurso do ponto de entrega/padrão de entrada até o Quadro Geral de Distribuição (QDG 150A): `120,00 m`.
  - Quantidade Comercial UCC (Com Perda 5%): `120,00 m × 1,05 =` **`126,00 m`**.
- **Cabos de Cobre Flexível 750V 2,5mm² (Iluminação e Tomadas TUG):**
  - Censo de Pontos nos Desenhos: 98 pontos de teto (68 painéis LED + 16 herméticas + 14 emergências) + 110 tomadas TUG + 30 interruptores = 238 caixas.
  - Percurso Horizontal Médio em Forro: `22 circuitos × 18,00 m = 396,00 m` de eletroduto horizontal.
  - Descidas Verticais nas Paredes (Pé-direito livre H=2,98m):
    - 110 Tomadas TUG (cota h=0,30m do piso acabado): `110 un × (2,98 - 0,30) = 110 × 2,68m = 294,80 m`.
    - 30 Interruptores (cota h=1,10m do piso acabado): `30 un × (2,98 - 1,10) = 30 × 1,88m = 56,40 m`.
    - Subtotal Descidas Verticais: `294,80 + 56,40 = 351,20 m`.
  - Extensão Total de Eletrodutos com Fiação 2,5mm²: `396,00 + 351,20 = 747,20 m`.
  - Multiplicação por Condutores Médios (Fase, Neutro, Terra e Retornos = 2,3 fios/trecho): `747,20 m × 2,3 = 1.718,56 m`.
  - Sobras Técnicas de Conexão em Caixas e Quadros (NBR 5410):
    - `238 caixas × 0,50m = 119,00 m`.
    - `2 QDFs × 22 condutores × 1,00m = 44,00 m`.
  - Total Líquido de Projeto: `1.718,56 + 119,00 + 44,00 = 1.881,56 m` → Adotado nominal de projeto: **`1.850,00 m`**.
  - Quantidade Comercial UCC (Com Perda 10%): `1.850,00 m × 1,10 = 2.035,00 m` → **`21 rolos de 100m`** (`2.100 m`).
- **Cabos de Cobre Flexível 750V 4,0mm² (Tomadas de Uso Específico TUG/TUE):**
  - Censo de Pontos: 24 tomadas TUE 20A (copa, servidores, equipamentos dedicados).
  - Percurso Horizontal: `6 circuitos × 25,00 m = 150,00 m`.
  - Descidas Verticais: `24 un × 2,68 m = 64,32 m`.
  - Condutores por circuito (Fase + Neutro + Terra): `(150,00 + 64,32) × 3 = 642,96 m` → Adotado de projeto: **`640,00 m`**.
  - Quantidade Comercial UCC (Com Perda 10%): `640,00 m × 1,10 = 704,00 m` → **`8 rolos de 100m`** (`800 m`).
- **Cabos de Cobre Flexível 750V 6,0mm² (Alimentação de Climatização/HVAC):**
  - Censo de Pontos: 4 circuitos dedicados para os quadros de condensadoras e evaporadoras de grande porte.
  - Percurso Total: `4 circuitos × 35,00 m × 3 condutores (2 Fases + Terra) = 420,00 m`.
  - Quantidade Comercial UCC (Com Perda 10%): `420,00 m × 1,10 = 462,00 m` → **`5 rolos de 100m`** (`500 m`).
- **Eletrodutos Rígidos de PVC Ø3/4" (25mm) e Ø1" (32mm):**
  - Ø3/4" (Distribuição secundária e descidas): `480,00 m líquidos`. Com perda 10%: `528,00 m` → **`176 varas de 3m`**.
  - Ø1" (Alimentadores secundários QDF e ramais HVAC): `210,00 m líquidos`. Com perda 10%: `231,00 m` → **`77 varas de 3m`**.
- **Caixas de Embutir, Placas e Módulos Elétricos:**
  - Caixas 4x2" PVC: `110 tomadas + 24 TUE + 22 interruptores + 8 paralelos + 20 caixas de passagem = 184 unid`. Com perda 5%: **`194 unidades`**.
  - Caixas 4x4" PVC: `24 unidades` nos blocos duplos de estações. Com perda 5%: **`26 unidades`**.
  - Caixas Octogonais 3x3" de Teto: `68 unidades`. Com perda 5%: **`72 unidades`**.
  - Módulos Tomada 10A (110 un + 5% = **`116 un`**) | Tomada 20A (24 un + 5% = **`26 un`**).
  - Interruptores: Simples (22 un + 5% = **`24 un`**) | Paralelos Three-way (8 un + 5% = **`9 un`**).
  - Conjuntos Placa + Suporte 4x2": `184 un + 5% =` **`194 conjuntos`**.
- **Quadros e Proteção:**
  - `1 un` QDG 150A Trifásico + `1 un` Disjuntor Caixa Moldada 150A + `4 un` DR Tetrapolar 40A + `8 un` DPS 20kA.
  - `2 un` QDF 24 elementos + `28 un` Disjuntores DIN mono (30 UCC) + `18 un` Disjuntores DIN bi/tri (19 UCC).
- **Luminárias e Emergência:**
  - `68 un` Painéis LED 60x60cm 40W 4000K (+5% = **`72 unidades`**).
  - `16 un` Luminárias Herméticas LED 2x18W IP65 (+5% = **`17 unidades`**).
  - `14 un` Blocos de Iluminação de Emergência LED 2x8W com bateria autônoma (**`14 unidades`**).
- **Cabeamento Estruturado e Telecomunicações:**
  - `36 pontos` lógicos RJ45 Cat6 Keystone (+5% = **`38 unidades`**).
  - Cabo UTP Cat6 LSZH: `36 pontos × 38,00 m médios + sobras de patch panel = 1.450,00 m líquidos`. Com perda 10%: `1.595,00 m` → **`16 rolos de 100m`** (`1.600 m`).
  - Infraestrutura: `1 un` Rack 19" 12U + `2 un` Patch Panels 24p Cat6 + `1 un` Switch Gigabit 24p PoE.
- **Aterramento:**
  - `6 conjuntos` de Hastes Copperweld 3/4" x 3,00m interligadas aos barramentos de terra dos quadros QDG e QDFs.

---

### 1.2 Instalações Hidrossanitárias e Drenagem Pluvial (Prancha EGS-015 e Arquitetura EGS-015/EGS-018)
> **Critério de Medição Hidráulica (NBR 5626 / NBR 8160 / NBR 10844):**  
> As tubulações são quantificadas pelo somatório das alturas de prumadas verticais entre o barrilete/cobertura e piso térreo com os ramais horizontais distribuídos pelas paredes das baterias sanitárias e coletores enterrados.

- **Reservação de Água Potável Predial:**
  - População fixa estimada: 50 ocupantes × 50 L/dia = 2.500 L/dia.
  - Autonomia regulamentar (2 dias de reserva de consumo = 5.000 L) + Reserva Técnica de Incêndio/Emergência (5.000 L):
    Volume Total Necessário = `10.000 L` → **`2 Reservatórios de Polietileno de 5.000 L`** com tampa.
- **Tubulações de Água Fria em PVC Soldável:**
  - Tubo Ø50mm (1.1/2") - Barrilete e Prumadas Principais:
    - Barrilete na cobertura: `28,00 m`.
    - 4 Prumadas verticais de descida: `4 × 3,80 m = 15,20 m`.
    - Distribuição principal térrea: `51,80 m`.
    - Total Líquido de Projeto: **`95,00 m`**.
    - Quantidade Comercial UCC (Com Perda 10%): `95,00 m × 1,10 = 104,50 m` → **`18 varas de 6m`** (`108,00 m`).
  - Tubo Ø25mm (3/4") - Sub-ramais de Alimentação de Aparelhos:
    - Ramais embutidos em paredes nos sanitários masculino, feminino, vestiários e copa: **`180,00 m líquidos`**.
    - Quantidade Comercial UCC (Com Perda 10%): `180,00 m × 1,10 = 198,00 m` → **`33 varas de 6m`** (`198,00 m`).
- **Tubulações de Esgoto Sanitário e Ventilação em PVC:**
  - Tubo PVC Esgoto Ø100mm (Ramais de bacias e coletor enterrado sob contrapiso c/ i=1%):
    - Total Líquido de Projeto: **`140,00 m`**.
    - Quantidade Comercial UCC (Com Perda 10%): `140,00 m × 1,10 = 154,00 m` → **`26 varas de 6m`** (`156,00 m`).
  - Tubo PVC Esgoto Ø75mm (Colunas de ventilação até o telhado):
    - Total Líquido de Projeto: **`42,00 m`**.
    - Quantidade Comercial UCC (Com Perda 10%): `42,00 m × 1,10 = 46,20 m` → **`8 varas de 6m`** (`48,00 m`).
  - Tubo PVC Esgoto Ø40mm (Ramais de pias, lavatórios e ralos):
    - Total Líquido de Projeto: **`64,00 m`**.
    - Quantidade Comercial UCC (Com Perda 10%): `64,00 m × 1,10 = 70,40 m` → **`12 varas de 6m`** (`72,00 m`).
- **Descidas de Águas Pluviais em Tubo PVC Reforçado Ø150mm:**
  - 8 Condutores verticais de descida das calhas da cobertura: `8 un × 4,00 m = 32,00 m` + conexões e deságues perimétricos = **`110,00 m líquidos`**.
  - Quantidade Comercial UCC (Com Perda 10%): `110,00 m × 1,10 = 121,00 m` → **`21 varas de 6m`** (`126,00 m`).
- **Conexões Hidráulicas e Esgoto:**
  - Água Fria: Joelhos 90° Ø25mm (86 un + 5% = **`91 un`**), Joelhos c/ bucha latão 1/2" (32 un + 5% = **`34 un`**), Joelhos Ø50mm (24 un + 5% = **`26 un`**), Tês Ø25mm (48 un + 5% = **`51 un`**), Tês redução 50x25mm (18 un + 5% = **`19 un`**), Curvas transposição Ø25mm (14 un + 5% = **`15 un`**).
  - Esgoto: Joelhos 90° Ø100mm (36 un + 5% = **`38 un`**), Joelhos 45° Ø100mm (22 un + 5% = **`24 un`**), Junções 45° Y 100x50mm (18 un + 5% = **`19 un`**), Tês sanitários 100x100mm (12 un + 5% = **`13 un`**).
- **Registros e Válvulas:**
  - Registros de gaveta c/ canopla cromada: `12 un Ø25mm (3/4")` + `4 un Ø50mm (1.1/2")`.
  - Registros de pressão c/ canopla cromada para chuveiros: `6 unidades`.
  - Válvulas de retenção vertical Ø50mm: `2 unidades`.
- **Caixas Prediais, Louças e Metais Sanitários:**
  - `14 un` Ralos sifonados PVC 150x150x50mm com grelha em aço inox.
  - `2 un` Caixas de gordura pré-moldadas 100L (copa) + `6 un` Caixas de inspeção de concreto 60x60x60cm com tampa.
  - `10 cj` Bacias sanitárias com caixa acoplada 3/6L e assento.
  - `12 cj` Lavatórios de louça com torneira de fechamento automático.
  - `15 un` Sifões sanfonados (14 un + 5%), `24 un` Engates flexíveis inox (22 un + 5%), `13 un` Válvulas de escoamento inox 7/8" (12 un + 5%), `12 rolos` Fita veda-rosca PTFE 18mm x 50m.

---

### 1.3 Climatização e Exaustão Mecânica — HVAC (Prancha EGS-008)
> **Critério de Dimensionamento Térmico (NBR 13971 / ASHRAE):**  
> Carga térmica dimensionada para clima litorâneo/portuário (Açu): `Carga específica = 700 BTU/h/m²`.  
> Carga Total de Projeto = `700 BTU/h/m² × 368,40 m² = 257.880 BTU/h`.

- **Capacidade Instalada Dimensionada (com margem de segurança e redundância):**
  - Splits Cassete 36.000 BTU/h Inverter: **`4 conjuntos`** (Salas de reunião e estações integradas de trabalho).
  - Splits Hi-Wall 18.000 BTU/h Inverter: **`6 conjuntos`** (Salas gerenciais e coordenação).
  - Splits Hi-Wall 12.000 BTU/h Inverter: **`6 conjuntos`** (Salas individuais e recepção).
  - Capacidade Total Instalada = `(4 × 36.000) + (6 × 18.000) + (6 × 12.000) = 144.000 + 108.000 + 72.000 =` **`324.000 BTU/h`** (atende plenamente à demanda de pico térmico).
- **Linha Frigorígena em Tubulação de Cobre Flexível Ø3/8" + Ø5/8" c/ Isolamento Térmico:**
  - 16 aparelhos com distância média de 11,25m até as condensadoras externas: `16 un × 11,25 m = 180,00 m líquidos`.
  - Quantidade Comercial UCC (Com Perda 10%): `180,00 m × 1,10 =` **`198,00 m`**.
- **Rede de Drenagem de Condensado em Tubo PVC Ø25mm Isolado:**
  - Percurso das evaporadoras até os pontos de deságue: `120,00 m líquidos`.
  - Quantidade Comercial UCC (Com Perda 10%): `120,00 m × 1,10 = 132,00 m` → **`22 varas de 6m`** (`132,00 m`).
- **Exaustão Mecânica dos Sanitários (Áreas sem ventilação natural):**
  - **`6 unidades`** de Exaustores Axiais de teto/parede 150 m³/h com duto flexível e veneziana externa.

---

## 📊 2. Tabela Consolidada de Quantitativos e Pedido de Compras (UCC)

| Código EAP | Descrição do Insumo / Serviço | Qtd Projeto | Perda (%) | Qtd Comercial UCC | Unidade UCC | Prancha Ref | Preço Unit. | Custo Total |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: |
| **3.1.1** | Cabo Cobre Flexível 750V 2,5mm² (Iluminação/TUG) | 1850.0 m | 10.0% | **21** | `rolos de 100m (2035m)` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.2** | Cabo Cobre Flexível 750V 4,0mm² (Tomadas TUG/TUE) | 640.0 m | 10.0% | **8** | `rolos de 100m (704m)` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.3** | Cabo Cobre Flexível 750V 6,0mm² (Ar Condicionado) | 420.0 m | 10.0% | **5** | `rolos de 100m (462m)` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.4** | Cabo Cobre Sintenax 0,6/1kV 35mm² (Alimentador) | 120.0 m | 5.0% | **126.0** | `m` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.5** | Eletroduto Rígido PVC Ø3/4" (25mm) c/ Conexões | 480.0 m | 10.0% | **176** | `varas de 3m (528m)` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.6** | Eletroduto Rígido PVC Ø1" (32mm) c/ Conexões | 210.0 m | 10.0% | **77** | `varas de 3m (231m)` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.7** | Caixa de Embutir 4x2" PVC Amarela para Parede | 184.0 unid | 5.0% | **194** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.8** | Caixa de Embutir 4x4" PVC Amarela para Parede | 24.0 unid | 5.0% | **26** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.9** | Caixa Octogonal 3x3" PVC para Teto | 68.0 unid | 5.0% | **72** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.10** | Conjunto Suporte + Placa 4x2" c/ Parafusos | 184.0 unid | 5.0% | **194** | `conjuntos` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.11** | Módulo de Tomada 2P+T 10A / 250V (Branca) | 110.0 unid | 5.0% | **116** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.12** | Módulo de Tomada 2P+T 20A / 250V (Vermelha TUE) | 24.0 unid | 5.0% | **26** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.13** | Módulo Interruptor Simples 10A | 22.0 unid | 5.0% | **24** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.14** | Módulo Interruptor Paralelo (Three-Way) 10A | 8.0 unid | 5.0% | **9** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.15** | Cabo UTP Cat6 LSZH 4 Pares (Dados/Voz) | 1450.0 m | 10.0% | **16** | `rolos de 100m (1600m)` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.16** | Módulo Tomada RJ45 Cat6 Keystone | 36.0 unid | 5.0% | **38** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.17** | Rack Metalico Telecom 19" 12U de Parede | 1.0 unid | 0.0% | **1** | `unidade` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.18** | Patch Panel 24 Portas Cat6 19" | 2.0 unid | 0.0% | **2** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.19** | Switch Gigabit Ethernet 24 Portas PoE | 1.0 unid | 0.0% | **1** | `unidade` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.20** | Quadro Geral de Distribuição QDG 150A Trifásico | 1.0 unid | 0.0% | **1** | `unidade` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.21** | Quadro de Distribuição de Luz QDF 24 Elementos embutir | 2.0 unid | 0.0% | **2** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.22** | Disjuntor Geral Caixa Moldada 150A Trifásico | 1.0 unid | 0.0% | **1** | `unidade` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.23** | Disjuntor Termomagnético DIN Monopolar 10A/16A/20A | 28.0 unid | 5.0% | **30** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.24** | Disjuntor Termomagnético DIN Bipolar/Tripolar 25A/32A | 18.0 unid | 5.0% | **19** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.25** | Interruptor Diferencial Residual DR Tetrapolar 40A 30mA | 4.0 unid | 0.0% | **4** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.26** | Dispositivo de Proteção contra Surtos DPS 20kA 275V | 8.0 unid | 0.0% | **8** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.27** | Painel LED Embutir 60x60cm 40W 4000K | 68.0 unid | 5.0% | **72** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.28** | Luminária Hermética LED 2x18W IP65 (Áreas Técnicas) | 16.0 unid | 5.0% | **17** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.29** | Bloco Iluminação de Emergência LED 2x8W c/ Bateria | 14.0 unid | 0.0% | **14** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.1.30** | Haste de Aterramento Copperweld 3/4" x 3,00m + Malha | 6.0 unid | 0.0% | **6** | `conjuntos` | `AÇU-3.DES-2.3100-16-EGS-013` | - | **-** |
| **3.2.1** | Tubo PVC Soldável Água Fria Ø25mm (3/4") | 180.0 m | 10.0% | **33** | `varas de 6m (198m)` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.2** | Tubo PVC Soldável Água Fria Ø50mm (1.1/2") | 95.0 m | 10.0% | **18** | `varas de 6m (108m)` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.3** | Tubo PVC Esgoto Série Normal Ø40mm | 64.0 m | 10.0% | **12** | `varas de 6m (72m)` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.4** | Tubo PVC Esgoto Série Normal Ø75mm | 42.0 m | 10.0% | **8** | `varas de 6m (48m)` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.5** | Tubo PVC Esgoto Série Normal Ø100mm | 140.0 m | 10.0% | **26** | `varas de 6m (156m)` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.6** | Tubo PVC Pluvial Série Reforçada Ø150mm | 110.0 m | 10.0% | **21** | `varas de 6m (126m)` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.7** | Joelho 90º PVC Soldável Ø25mm | 86.0 unid | 5.0% | **91** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.8** | Joelho 90º c/ Bucha de Latão Ø25mm x 1/2" | 32.0 unid | 5.0% | **34** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.9** | Joelho 90º PVC Soldável Ø50mm | 24.0 unid | 5.0% | **26** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.10** | Tê 90º PVC Soldável Ø25mm | 48.0 unid | 5.0% | **51** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.11** | Tê 90º Redução PVC Soldável Ø50x25mm | 18.0 unid | 5.0% | **19** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.12** | Curva de Transposição PVC Soldável Ø25mm | 14.0 unid | 5.0% | **15** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.13** | Joelho 90º PVC Esgoto Ø100mm | 36.0 unid | 5.0% | **38** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.14** | Joelho 45º PVC Esgoto Ø100mm | 22.0 unid | 5.0% | **24** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.15** | Junção 45º Y PVC Esgoto Ø100x50mm | 18.0 unid | 5.0% | **19** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.16** | Tê Sanitário 90º PVC Esgoto Ø100x100mm | 12.0 unid | 5.0% | **13** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.17** | Registro de Gaveta Bruto c/ Canopla Cromada Ø25mm (3/4") | 12.0 unid | 0.0% | **12** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.18** | Registro de Gaveta Bruto c/ Canopla Cromada Ø50mm (1.1/2") | 4.0 unid | 0.0% | **4** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.19** | Registro de Pressão c/ Canopla Cromada Ø20mm (Chuveiros) | 6.0 unid | 0.0% | **6** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.20** | Válvula de Retenção Vertical Ø50mm | 2.0 unid | 0.0% | **2** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.21** | Reservatório de Água Potável Polietileno 5.000 L c/ Tampa | 2.0 unid | 0.0% | **2** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.22** | Ralo Sifonado PVC 150x150x50mm Grelha Inox | 14.0 unid | 0.0% | **14** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.23** | Caixa de Gordura Pré-moldada Concreto 100L | 2.0 unid | 0.0% | **2** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.24** | Caixa de Inspeção Esgoto Concreto 60x60x60cm c/ Tampa | 6.0 unid | 0.0% | **6** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.25** | Bacia Sanitária c/ Caixa Acoplada 3/6L e Assento | 10.0 unid | 0.0% | **10** | `conjuntos` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.26** | Lavatório Louça Branca c/ Torneira Automática de Mesa | 12.0 unid | 0.0% | **12** | `conjuntos` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.27** | Sifão Sanfonado Universal PVC c/ Adaptador | 14.0 unid | 5.0% | **15** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.28** | Engate Flexível Inox 1/2" 40cm | 22.0 unid | 5.0% | **24** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.29** | Válvula de Escoamento Inox 7/8" para Lavatório | 12.0 unid | 5.0% | **13** | `unidades` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.2.30** | Fita Veda-Rosca PTFE 18mm x 50m | 12.0 rolo | 0.0% | **12** | `rolos` | `AÇU-3.DES-2.3100-16-EGS-015` | - | **-** |
| **3.3.1** | Aparelho Split Cassete 36.000 BTU/h Inverter R410A | 4.0 unid | 0.0% | **4** | `conjuntos` | `AÇU-3.DES-2.3100-64-EGS-008` | - | **-** |
| **3.3.2** | Aparelho Split Hi-Wall 18.000 BTU/h Inverter R410A | 6.0 unid | 0.0% | **6** | `conjuntos` | `AÇU-3.DES-2.3100-64-EGS-008` | - | **-** |
| **3.3.3** | Aparelho Split Hi-Wall 12.000 BTU/h Inverter R410A | 6.0 unid | 0.0% | **6** | `conjuntos` | `AÇU-3.DES-2.3100-64-EGS-008` | - | **-** |
| **3.3.4** | Tubulação Cobre Flexível Ø3/8"+Ø5/8" c/ Isolamento | 180.0 m | 10.0% | **198.0** | `m` | `AÇU-3.DES-2.3100-64-EGS-008` | - | **-** |
| **3.3.5** | Tubo PVC Condensado Ø25mm c/ Isolamento | 120.0 m | 10.0% | **22** | `varas de 6m (132m)` | `AÇU-3.DES-2.3100-64-EGS-008` | - | **-** |
| **3.3.6** | Exaustor Axial de Parede/Teto 150 m³/h | 6.0 unid | 0.0% | **6** | `unidades` | `AÇU-3.DES-2.3100-64-EGS-008` | - | **-** |

---

*Data da última atualização:* 08/09/2026
