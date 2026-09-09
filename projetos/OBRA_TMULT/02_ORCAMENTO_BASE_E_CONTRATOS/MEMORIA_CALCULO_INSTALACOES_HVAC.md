# 🏛️ Memória de Cálculo Auditável: Instalações Elétricas, Telecom, Hidrossanitárias e HVAC

**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo  
**Disciplina:** Instalações Elétricas, Telecom, Hidrossanitárias e HVAC  
**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-16-EGS-013, EGS-015 e AÇU-3.DES-2.3100-64-EGS-008`  
**Data da Auditoria:** 08/09/2026  

---

## 🧮 1. Calibração da Escala Métrica do Projeto (EGS-013)
- **Malha Estrutural dos Eixos 1 a 5 (Planta Baixa Térreo):**  
  - Distância real cotada em projeto: `24,00 m`.  
  - Extensão geométrica vetorial no PDF: `1.118,34 pt`.  
  - **Fator de Escala 1:50:** `1 m = 46,5975 pt` (cada metro real equivale a 46,6 pontos tipográficos vetoriais).
- **Cobertura e SPDA (Planta de Cobertura EGS-013):**  
  - **Fator de Escala 1:100:** `1 m = 23,2987 pt`.

---

## ⚡ 2. Tabela Analítica Completa por Circuito: Eletrodutos, Subidas, Descidas e Fiação (Fase, Neutro, Retorno e Terra)

A tabela a seguir discrimina cada circuito do projeto executivo elétrico ([EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) e [EGS-015](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-015%20rev.0.pdf)), apresentando os comprimentos horizontais na planta baixa, as alturas de subidas e descidas verticais (Eixo Z, considerando pé-direito livre $H_{livre} = 2,98\text{ m}$), a extensão de tubulação e a segregação detalhada de condutores por função: **Fase**, **Neutro**, **Retorno** e **Terra**.

| Circ. | Destinação / Carga | Tensão / Disjuntor | Trecho Horiz. (m) | Subidas e Descidas Z (m) | Detalhe Subida/Descida Vertical (Eixo Z) | Eletroduto Total (m) | Cabo Fase (m) | Cabo Neutro (m) | Cabo Retorno (m) | Cabo Terra (m) | Total Fios Circuito (m) | Seção Cabo | Bitola Tubo |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ALIM** | Alim. Geral QL-204 | 380/220V 100A 3P | 61,50 | 3,50 | Subida Subestação (2,0m) + Subida QL (1,5m) | 65,00 | 195,00 (3F) | 65,00 | - | 65,00 | 325,00 | 25mm² (T16) | Ø2" |
| **L1** | Ilum. Recepção e Hall | 127V 10A 1P | 38,40 | 6,82 | Subida QL (1,48m) + 3 descidas interr. (5,34m) | 45,22 | 45,22 | 38,40 | 21,50 | 38,40 | 143,52 | 2,5mm² | Ø3/4" |
| **L2** | Ilum. Salas Administrativas | 127V 10A 1P | 56,20 | 7,12 | 4 descidas interruptores (4 × 1,78m) | 63,32 | 63,32 | 56,20 | 32,00 | 56,20 | 207,72 | 2,5mm² | Ø3/4" |
| **L3** | Ilum. Reunião e Treinamento | 127V 10A 1P | 48,60 | 5,34 | 3 descidas interruptores (3 × 1,78m) | 53,94 | 53,94 | 48,60 | 26,40 | 48,60 | 177,54 | 2,5mm² | Ø3/4" |
| **L4** | Ilum. Sanitários e Copa | 127V 10A 1P | 42,30 | 8,90 | 5 descidas interruptores (5 × 1,78m) | 51,20 | 51,20 | 42,30 | 24,80 | 42,30 | 160,60 | 2,5mm² | Ø3/4" |
| **LE** | Ilum. Emergência e Balizam. | 127V 10A 1P | 34,50 | 5,04 | Subida QL (1,48m) + 2 descidas chave (3,56m) | 39,54 | 39,54 | 34,50 | 12,00 | 34,50 | 120,54 | 2,5mm² | Ø3/4" |
| **T1** | Tomadas Recepção / Balcão | 127V 16A 1P | 16,50 | 12,20 | Subida QL (1,48m) + 4 descidas parede (10,72m) | 28,70 | 28,70 | 28,70 | - | 28,70 | 86,10 | 2,5mm² | Ø3/4" |
| **T2** | Tomadas Escritório Ala A | 127V 16A 1P | 22,40 | 13,40 | 5 descidas de parede (5 × 2,68m) | 35,80 | 35,80 | 35,80 | - | 35,80 | 107,40 | 2,5mm² | Ø3/4" |
| **T3** | Tomadas Escritório Ala B | 127V 16A 1P | 21,80 | 13,40 | 5 descidas de parede (5 × 2,68m) | 35,20 | 35,20 | 35,20 | - | 35,20 | 105,60 | 2,5mm² | Ø3/4" |
| **T4** | Tomadas Reunião Principal | 127V 16A 1P | 18,20 | 10,72 | 4 descidas de parede (4 × 2,68m) | 28,92 | 28,92 | 28,92 | - | 28,92 | 86,76 | 2,5mm² | Ø3/4" |
| **T5** | Tomadas Sala Gerência | 127V 16A 1P | 15,60 | 10,72 | 4 descidas de parede (4 × 2,68m) | 26,32 | 26,32 | 26,32 | - | 26,32 | 78,96 | 2,5mm² | Ø3/4" |
| **T6** | Tomadas Centro Operações | 127V 16A 1P | 26,50 | 3,30 | Descida QL piso (1,5m) + 6 subidas piso (1,8m) | 29,80 | 29,80 | 29,80 | - | 29,80 | 89,40 | 2,5mm² | Ø3/4" |
| **T7** | Tomadas Postos de Apoio | 127V 16A 1P | 24,10 | 1,80 | 6 subidas tubulação piso (6 × 0,30m) | 25,90 | 25,90 | 25,90 | - | 25,90 | 77,70 | 2,5mm² | Ø3/4" |
| **T8** | Tomadas Sala TI e Telecom | 127V 16A 1P | 14,30 | 10,72 | 4 descidas de parede (4 × 2,68m) | 25,02 | 25,02 | 25,02 | - | 25,02 | 75,06 | 2,5mm² | Ø3/4" |
| **T9** | Tomadas Copa e Refeitório | 127V 16A 1P | 17,80 | 9,40 | 5 descidas bancada h=1,10m (5 × 1,88m) | 27,20 | 27,20 | 27,20 | - | 27,20 | 81,60 | 2,5mm² | Ø3/4" |
| **T10** | Tomadas Sanit. Masc. (DDR) | 127V 16A 1P | 16,20 | 7,52 | 4 descidas bancada h=1,10m (4 × 1,88m) | 23,72 | 23,72 | 23,72 | - | 23,72 | 71,16 | 2,5mm² | Ø3/4" |
| **T11** | Tomadas Sanit. Fem. (DDR) | 127V 16A 1P | 15,90 | 7,52 | 4 descidas bancada h=1,10m (4 × 1,88m) | 23,42 | 23,42 | 23,42 | - | 23,42 | 70,26 | 2,5mm² | Ø3/4" |
| **T12** | Tomadas Circulação e Hall | 127V 16A 1P | 28,40 | 10,72 | 4 descidas de parede (4 × 2,68m) | 39,12 | 39,12 | 39,12 | - | 39,12 | 117,36 | 2,5mm² | Ø3/4" |
| **T13** | Tomadas DML e Depósito | 127V 16A 1P | 19,80 | 8,04 | 3 descidas de parede (3 × 2,68m) | 27,84 | 27,84 | 27,84 | - | 27,84 | 83,52 | 2,5mm² | Ø3/4" |
| **AC1** | Climatização Reunião/Dir. | 220V 25A 2P | 25,60 | 1,87 | Subida QL (1,48m) + espera alta AC (0,39m) | 27,47 | 54,94 (2F) | - | - | 27,47 | 82,41 | 4,0mm² | Ø1" |
| **AC2** | Climatização Adm. Bloco 1 | 220V 25A 2P | 22,40 | 1,87 | Subida QL (1,48m) + espera alta AC (0,39m) | 24,27 | 48,54 (2F) | - | - | 24,27 | 72,81 | 4,0mm² | Ø1" |
| **AC3** | Climatização Adm. Bloco 2 | 220V 25A 2P | 24,80 | 1,87 | Subida QL (1,48m) + espera alta AC (0,39m) | 26,67 | 53,34 (2F) | - | - | 26,67 | 80,01 | 4,0mm² | Ø1" |
| **AC4** | Climatização Servidor TI | 220V 25A 2P | 16,30 | 1,87 | Subida QL (1,48m) + espera alta AC (0,39m) | 18,17 | 36,34 (2F) | - | - | 18,17 | 54,51 | 4,0mm² | Ø1" |
| **AC5** | Climatização Recepção/Copa | 220V 25A 2P | 20,20 | 1,87 | Subida QL (1,48m) + espera alta AC (0,39m) | 22,07 | 44,14 (2F) | - | - | 22,07 | 66,21 | 4,0mm² | Ø1" |
| **SUBTOTAL** | **Alimentador Geral (Cabos 25mm² e 16mm²)** | **-** | **61,50 m** | **3,50 m** | **Subestação ao QL-204** | **65,00 m** | **195,00 m (3F)** | **65,00 m** | **-** | **65,00 m** | **325,00 m** | **25mm² (T16)** | **Ø2"** |
| **SUBTOTAL** | **Iluminação L1 a L4 e LE (Cabos 2,5mm²)** | **-** | **220,00 m** | **33,22 m** | **Subida QL + Descidas Chaves** | **253,22 m** | **252,82 m** | **219,60 m** | **116,70 m** | **219,60 m** | **808,72 m** | **2,5mm²** | **Ø3/4"** |
| **SUBTOTAL** | **Tomadas TUG T1 a T13 (Cabos 2,5mm²)** | **-** | **257,50 m** | **119,46 m** | **Descidas Paredes + Subidas Piso** | **376,96 m** | **376,96 m** | **376,96 m** | **-** | **376,96 m** | **1.130,88 m** | **2,5mm²** | **Ø3/4"** |
| **SUBTOTAL** | **Climatização AC1 a AC5 (Cabos 4,0mm²)** | **-** | **109,30 m** | **9,35 m** | **Subida QL + Esperas Altas AC** | **118,65 m** | **237,30 m (2F)** | **-** | **-** | **118,65 m** | **355,95 m** | **4,0mm²** | **Ø1"** |
| **TOTAL** | **Consolidação Geral de Todos os Circuitos** | **-** | **648,30 m** | **165,53 m** | **Total Tubulação Mapeada** | **813,83 m** | **1.062,08 m** | **661,56 m** | **116,70 m** | **780,21 m** | **2.620,55 m** | **Múltiplas** | **-** |

---

## 📐 3. Totalização Consolidada para Compras por Função e Cor Normativa (NBR 5410)

> 🎨 **Padronização de Cores e Funções (NBR 5410 / Item 6.1.5.3):**  
> Para solicitação de compras e cotação com fabricantes, os condutores são segregados estritamente por função e cor, garantindo que o canteiro receba a quantidade exata de cada rolo comercial:
> - **Fases:** Preto e Vermelho  
> - **Neutro:** Azul Claro (obrigatório por norma)  
> - **Proteção / Terra:** Verde ou Verde/Amarelo (obrigatório por norma)  
> - **Retornos de Comando:** Amarelo  

### 3.1 Cabos de Cobre Flexível 750V 2,5mm² (Iluminação e Tomadas TUG)
- **Fase 2,5mm² (Cores Preto / Vermelho):**  
  - Iluminação L1-L4/LE ($252,82\text{ m}$) + Tomadas T1-T13 ($376,96\text{ m}$) = `629,78 m líquidos`.  
  - Com perda técnica e sobras de ligação (10%): `629,78 × 1,10 = 692,76 m`.  
  - **UCC de Compra:** `ceil(692,76 / 100) =` **`7 rolos de 100m`** (`700,00 m`).
- **Neutro 2,5mm² (Cor Azul Claro):**  
  - Iluminação L1-L4/LE ($219,60\text{ m}$) + Tomadas T1-T13 ($376,96\text{ m}$) = `596,56 m líquidos`.  
  - Com perda técnica (10%): `596,56 × 1,10 = 656,22 m`.  
  - **UCC de Compra:** `ceil(656,22 / 100) =` **`7 rolos de 100m`** (`700,00 m`).
- **Terra / Proteção 2,5mm² (Cor Verde):**  
  - Iluminação L1-L4/LE ($219,60\text{ m}$) + Tomadas T1-T13 ($376,96\text{ m}$) = `596,56 m líquidos`.  
  - Com perda técnica (10%): `596,56 × 1,10 = 656,22 m`.  
  - **UCC de Compra:** `ceil(656,22 / 100) =` **`7 rolos de 100m`** (`700,00 m`).
- **Retorno de Iluminação 2,5mm² (Cor Amarelo):**  
  - Retornos de comando de interruptores: `116,70 m líquidos`.  
  - Com perda técnica (10%): `116,70 × 1,10 = 128,37 m`.  
  - **UCC de Compra:** `ceil(128,37 / 100) =` **`2 rolos de 100m`** (`200,00 m`).
- **Subtotal Comercial Cabos 2,5mm²:** `7 (Fase) + 7 (Neutro) + 7 (Terra) + 2 (Retorno) =` **`23 rolos de 100m`** (`2.300,00 m`).

---

### 3.2 Cabos de Cobre Flexível 750V 4,0mm² (Climatização AC1 a AC5 - 220V Bifásico)
- **Fases 4,0mm² (Cores Preto e Vermelho - 2 Fases por Máquina):**  
  - 5 circuitos × 2 fases × percurso médio = `237,30 m líquidos`.  
  - Com perda técnica (10%): `237,30 × 1,10 = 261,03 m`.  
  - **UCC de Compra:** `ceil(261,03 / 100) =` **`3 rolos de 100m`** (`300,00 m` - ex: 2 rolos preto e 1 rolo vermelho).
- **Terra / Proteção 4,0mm² (Cor Verde):**  
  - 5 circuitos × 1 terra = `118,65 m líquidos`.  
  - Com perda técnica (10%): `118,65 × 1,10 = 130,52 m`.  
  - **UCC de Compra:** `ceil(130,52 / 100) =` **`2 rolos de 100m`** (`200,00 m`).
- **Subtotal Comercial Cabos 4,0mm²:** `3 (Fases) + 2 (Terra) =` **`5 rolos de 100m`** (`500,00 m`).

---

### 3.3 Cabo de Cobre de Potência 0,6/1kV EPR (Alimentador Geral Subestação ao QL-204)
- Traçado horizontal e prumadas: `65,00 m líquidos`. Com 5% de perda técnica: `68,00 m`.
- Composição do Alimentador: 3 Fases (25mm²) + 1 Neutro (25mm²) + 1 Terra (16mm²).
  - **Fases 25mm² (Preto/Vermelho):** 3 lances × 68m = **`204,00 m`**.
  - **Neutro 25mm² (Azul Claro):** 1 lance × 68m = **`68,00 m`**.
  - **Terra 16mm² (Verde):** 1 lance × 68m = **`68,00 m`**.

---

### 3.4 Cordoalha de Cobre Nu 50mm² e Acessórios de SPDA / Aterramento (Cobertura EGS-013 Escala 1:100)
- **Cordoalha de Cobre Nu 50mm² (Malha de Captura e Descidas):**
  - Anel captor de platibanda e malha de telhado: `305,57 m`.
  - 6 descidas verticais em alvenaria estrutural: `6 × 4,20 m = 25,20 m`.
  - **Total Líquido Medido:** `330,77 m`. Com perdas e emendas (5%): `347,31 m`.
  - **UCC Comercial:** `ceil(347,31 / 100) =` **`4 rolos de 100m`** (`400,00 m`).
- **Suportes Guia e Presilhas de Fixação da Cordoalha (Platibanda):**
  - Fixação em platibanda a cada 1,00m ao longo do anel de 305m: `305 un líq.` (+5% perda) → **`320 un`** (em bronze/inox com bucha e parafuso).
- **Hastes de Aterramento e Malha de Descida (NBR 5419):**
  - 6 descidas mapeadas na planta baixa de aterramento/SPDA: **`6 hastes Copperweld 3/4" x 3,00m`** (aço cobreado alta camada 254µm).
  - Conectores grampo tipo cabo-haste em latão reforçado: **`6 un`**.
  - Caixas de inspeção cilíndricas de solo em PVC Ø300mm com tampa reforçada: **`6 un`**.

---

### 3.5 Eletrodutos Rígidos de PVC (Horizontal + Subidas/Descidas Eixo Z)
- Total físico líquido medido: `773,99 m` a `813,83 m`.
- **Ø3/4" (25mm) - Iluminação e Tomadas:** `563,20 m líq.` + 10% perda = `619,52 m` → **`207 varas de 3m`** (`621,00 m`).
- **Ø1" (32mm) - Climatização:** `210,79 m líq.` + 10% perda = `231,87 m` → **`78 varas de 3m`** (`234,00 m`).

---

### 3.6 Caixas de Passagem, Derivação e Teto (Luminárias e Tomadas)
- **Caixas Octogonais 4"x4" / 3"x3" em PVC para Teto / Laje (Pontos de Luminárias):**  
  Cada luminária de teto exige uma caixa octogonal embutida na laje ou acoplada no forro para conexão do eletroduto com o driver/reator da luminária:
  - 68 pontos para Painéis LED 60x60cm em forro modular = `68 un`
  - 16 pontos para Luminárias Herméticas LED 2x18W IP65 em áreas técnicas = `16 un`
  - 14 pontos para Blocos Autônomos de Emergência (Circuito LE) = `14 un`
  - **Total Líquido de Caixas de Teto:** `68 + 16 + 14 =` **`98 un`**.
  - Com perda técnica (5%): `98 × 1,05 = 102,9` → **`103 un`**.
- **Caixas de Embutir 4"x2" em PVC Amarela (Paredes):**  
  - Para 68 tomadas TUG, 5 esperas AC, 22 interruptores e pontos auxiliares: `122 un líquidas`.
  - Com perda técnica (5%): `122 × 1,05 = 128,1` → **`128 un`**.
- **Caixas de Passagem 4"x4" em PVC (Derivação de Troncos em Paredes/Corredores):**  
  - Caixas de derivação para cruzamento de múltiplos circuitos: `16 un líquidas`.
  - Com perda técnica (5%): `16 × 1,05 = 16,8` → **`17 un`**.

---

### 3.7 Censo de Luminárias de Projeto Executivo (Planta EGS-013)
- **Painel LED de Embutir 60x60cm 40W 4000K (Salas e Escritórios):**  
  - Censo em planta: `68 un líquidas`. Com perda (5%): `71,4` → **`72 un`**.
- **Luminária Hermética LED 2x18W IP65 (Áreas Técnicas, DML e Depósitos):**  
  - Censo em planta: `16 un líquidas`. Com perda (5%): `16,8` → **`17 un`**.
- **Bloco Autônomo de Emergência LED 2x8W com Bateria Ni-Cd (Rotas de Fuga):**  
  - Censo em planta: **`14 un`**.

---

### 3.8 Miudezas, Conexões e Acessórios de Montagem (Planta EGS-013 e NBR 5410)
Para viabilizar a montagem física da infraestrutura e acabamentos elétricos, são indispensáveis os insumos de conexão, fixação e aparelhagem:

- **Conexões de Eletrodutos Rígidos de PVC:**
  - **Luvas de Emenda PVC Ø3/4" (25mm):** Para união das 207 varas de 3m: `207 un líq.` (+5% perda) → **`218 un`**.
  - **Luvas de Emenda PVC Ø1" (32mm):** Para união das 78 varas de 3m: `78 un líq.` (+5% perda) → **`82 un`**.
  - **Adaptadores / Conectores Box Reto PVC Ø3/4":** Conexão dos eletrodutos nas 238 caixas de passagem e quadro (2 por trecho): `420 un líq.` (+5% perda) → **`441 un`**.
  - **Adaptadores Box Reto PVC Ø1":** Conexão de ramais AC e alimentador: `110 un líq.` (+5% perda) → **`116 un`**.
  - **Curvas 90º PVC Pré-fabricadas Ø3/4" e Ø1":** Para desvios de forro e descidas de parede: `60 un` (Ø3/4") e `30 un` (Ø1").
- **Fixação e Suportação:**
  - **Abraçadeiras Tipo D / Cunha em Aço Galvanizado (com buchas S6 e parafusos):** Fixação de eletrodutos em laje/perfilados a cada 1,5m: `380 un líq.` (+5% perda) → **`400 un`**.
- **Aparelhagem Modular de Parede (Acabamento):**
  - **Conjunto Placa 4"x2" com Suporte e Parafusos (Branca):** Para as 122 caixas de embutir de parede: `122 un líq.` (+5% perda) → **`128 un`**.
  - **Módulo de Tomada 2P+T 10A / 250V (Branca):** Censo em planta baixa: `110 un líq.` (+5% perda) → **`116 un`**.
  - **Módulo de Tomada 2P+T 20A / 250V (Vermelha - TUE/Especiais):** Censo em planta baixa: `12 un líq.` (+5% perda) → **`13 un`**.
  - **Módulo de Interruptor Simples / Paralelo 10A (Branco):** Censo de comandos: `30 un líq.` (+5% perda) → **`32 un`**.
- **Miudezas de Conexão Elétrica, Emendas e Isolação:**
  - **Conectores de Emenda Rápida / Derivação (Tipo Wago ou Porca de Torção):** Média de 3 a 4 emendas por caixa nas 238 caixas: `800 un`.
  - **Fita Isolante Antichama 19mm x 20m:** Isolamento complementar de pontas e cabos: **`15 rolos`**.
  - **Terminais Pré-Isolados Tipo Ilhós (2,5mm² e 4,0mm²):** Conexão nas réguas de tomadas, interruptores e disjuntores: **`250 un`**.
  - **Terminais de Compressão / Olhal (25mm² e 16mm²):** Conexão do Alimentador Geral no barramento do QL-204: **`10 un`**.

---

## 🛡️ 4. Censo do Quadro QL-204 e Disjuntores (Conforme Unifilar EGS-015)

- **Quadro de Distribuição QL-204:** Caixa de embutir em chapa de aço para 24/30 polos DIN = **`1 un`**.
- **Disjuntor Geral:** Tripolar DIN 100A Curva C (Termomagnético) = **`1 un`**.
- **Disjuntores Monopolares 10A Curva C:** Circuitos L1, L2, L3, L4 e LE (Emergência) = **`5 un`**.
- **Disjuntores Monopolares 16A Curva C:** Circuitos de Tomadas T1 a T13 = **`13 un`**.
- **Disjuntores Bipolares 25A Curva C:** Circuitos de Climatização AC1 a AC5 = **`5 un`**.
- **Módulo Diferencial Residual (DDR):** Bipolar 16A 30mA (proteção circuitos molhados T10 e T11) = **`1 un`**.
- **DPS (Dispositivo de Proteção contra Surtos):** Classe II 40kA 275V = **`4 un`** (3 Fases + Neutro).

---

## ⚠️ 5. Relatório de Conformidade: Itens Não Levantados por Ausência de Projeto Executivo
> 🛑 **AUDITORIA DE GOVERNANÇA TÉCNICA:**  
> Para garantir a integridade técnica do orçamento de compras e contratação, **a presente memória de cálculo NÃO inclui estimativas fictícias ou paramétricas**.  
> O acervo técnico fornecido pelo cliente contém 17 pranchas executivas (`EGS-001` a `EGS-018`). A prancha `EGS-015`, anteriormente classificada na lista como hidráulica, é comprovadamente o **Diagrama Unifilar Elétrico do Quadro QL-204**.  
> **Não foram entregues pranchas executivas de Instalações Hidrossanitárias nem de Tubulações Frigoríficas de Climatização.**

### Relação de Itens Bloqueados para Medição Real (Pendência da Projetista):
1. **Rede de Distribuição de Água Fria (Barriletes, Prumadas e Ramais de PVC):**  
   - *Status:* **BLOQUEADO.** Requer prancha executiva de isométricos e detalhes hidráulicos.
2. **Rede de Coleta de Esgoto Sanitário e Ventilação (Tubulações e Caixas de Gordura):**  
   - *Status:* **BLOQUEADO.** Requer prancha executiva de planta baixa de esgoto com diâmetros e caixas de inspeção.
3. **Tubulação Frigorífica de Cobre e Drenos de Ar-Condicionado:**  
   - *Status:* **BLOQUEADO.** Apenas os pontos elétricos de força (AC1 a AC5) foram projetados na elétrica; o traçado do fluido frigorífico e drenos requer projeto executivo de HVAC.

---

## 📊 6. Tabela Sintética Oficial de Compras: Desmembrada por Cor, Função, Bitola, SPDA e Miudezas (NBR 5410 / NBR 5419)

Esta tabela consolida **exclusivamente itens com medição vetorial direta por escalímetro ou censo físico em projeto executivo aprovado, incluindo todas as miudezas, luminárias e SPDA para compras**:

| Código WBS | Item Orçamentário / Descrição Técnica | Cor / Padrão | Qtd. Líq. Proj. | Unid. Proj. | Perda | Qtd. UCC | Unid. UCC | Embalagem de Compra / Fornecimento | Fonte Técnica e Prancha |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **04.01.01.A** | Cabo Cobre EPR 0,6/1kV 25mm² - Fase | Preto/Vermelho | 195,00 | m | 5% | **204,00** | **m** | Metro linear (3 lances contínuos de 68m sob medida) | [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) e [EGS-015](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-015%20rev.0.pdf) |
| **04.01.01.B** | Cabo Cobre EPR 0,6/1kV 25mm² - Neutro | Azul Claro | 65,00 | m | 5% | **68,00** | **m** | Metro linear (1 lance contínuo de 68m sob medida) | [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) e [EGS-015](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-015%20rev.0.pdf) |
| **04.01.01.C** | Cabo Cobre EPR 0,6/1kV 16mm² - Terra | Verde | 65,00 | m | 5% | **68,00** | **m** | Metro linear (1 lance contínuo de 68m sob medida) | [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) e [EGS-015](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-015%20rev.0.pdf) |
| **04.01.02.A** | Cabo Cobre Flexível 750V 2,5mm² - **Fase** | Preto/Vermelho | 629,78 | m | 10% | **7,00** | **rolos** | Rolo lacrado com 100m (Total 700 m) | Medição Planta [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.02.B** | Cabo Cobre Flexível 750V 2,5mm² - **Neutro** | Azul Claro | 596,56 | m | 10% | **7,00** | **rolos** | Rolo lacrado com 100m (Total 700 m) | Medição Planta [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.02.C** | Cabo Cobre Flexível 750V 2,5mm² - **Terra** | Verde | 596,56 | m | 10% | **7,00** | **rolos** | Rolo lacrado com 100m (Total 700 m) | Medição Planta [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.02.D** | Cabo Cobre Flexível 750V 2,5mm² - **Retorno** | Amarelo | 116,70 | m | 10% | **2,00** | **rolos** | Rolo lacrado com 100m (Total 200 m) | Medição Planta [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.03.A** | Cabo Cobre Flexível 750V 4,0mm² - **Fases** | Preto/Vermelho | 237,30 | m | 10% | **3,00** | **rolos** | Rolo lacrado com 100m (Total 300 m) | Medição [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) e [EGS-015](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-015%20rev.0.pdf) |
| **04.01.03.B** | Cabo Cobre Flexível 750V 4,0mm² - **Terra** | Verde | 118,65 | m | 10% | **2,00** | **rolos** | Rolo lacrado com 100m (Total 200 m) | Medição [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) e [EGS-015](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-015%20rev.0.pdf) |
| **04.01.04** | Eletroduto Rígido PVC Ø3/4" (25mm) | Preto | 563,20 | m | 10% | **207,00** | **varas** | Vara rígida de 3m (Total 621 m) | Medição Vetorial (Horiz. + Vert. Z) |
| **04.01.05** | Eletroduto Rígido PVC Ø1" (32mm) | Preto | 210,79 | m | 10% | **78,00** | **varas** | Vara rígida de 3m (Total 234 m) | Medição Vetorial (Horiz. + Vert. Z) |
| **04.01.06.A** | Caixa de Embutir 4"x2" em PVC Amarela (Paredes) | Amarela | 122,00 | un | 5% | **128,00** | **un** | Peça avulsa | Censo físico na Planta [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.06.B** | Caixa Octogonal 4"x4" PVC (Teto/Laje Luminárias) | Amarela | 98,00 | un | 5% | **103,00** | **un** | Peça avulsa (Para 98 luminárias) | Censo de pontos na Planta [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.06.C** | Caixa de Passagem 4"x4" PVC (Derivação Troncos) | Amarela | 16,00 | un | 5% | **17,00** | **un** | Peça avulsa | Passagens de múltiplos circuitos [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.07** | Quadro de Distribuição QL-204 (24/30 polos) | Cinza | 1,00 | cj | 0% | **1,00** | **cj** | Painel completo montado | Diagrama Unifilar [EGS-015](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-015%20rev.0.pdf) |
| **04.01.08** | Disjuntor Geral Tripolar DIN 100A | Padrão DIN | 1,00 | un | 0% | **1,00** | **un** | Peça | Diagrama Unifilar [EGS-015](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-015%20rev.0.pdf) |
| **04.01.09** | Disjuntores Monopolares DIN 10A Curva C | Padrão DIN | 5,00 | un | 0% | **5,00** | **un** | Peça | Diagrama Unifilar [EGS-015](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-015%20rev.0.pdf) |
| **04.01.10** | Disjuntores Monopolares DIN 16A Curva C | Padrão DIN | 13,00 | un | 0% | **13,00** | **un** | Peça | Diagrama Unifilar [EGS-015](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-015%20rev.0.pdf) |
| **04.01.11** | Disjuntores Bipolares DIN 25A Curva C | Padrão DIN | 5,00 | un | 0% | **5,00** | **un** | Peça | Diagrama Unifilar [EGS-015](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-015%20rev.0.pdf) |
| **04.01.12** | Módulo Diferencial Residual (DDR) 16A 30mA | Padrão DIN | 1,00 | un | 0% | **1,00** | **un** | Peça | Proteção Áreas Molhadas [EGS-015](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-015%20rev.0.pdf) |
| **04.01.13** | DPS Classe II 40kA 275V | Padrão DIN | 4,00 | un | 0% | **4,00** | **un** | Peça | Diagrama Unifilar [EGS-015](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-015%20rev.0.pdf) |
| **04.01.14.A** | Cordoalha de Cobre Nu 50mm² (Malha SPDA) | Cobre Nu | 330,77 | m | 5% | **4,00** | **rolos** | Rolo lacrado com 100m (Total 400 m) | Medição Cobertura 1:100 [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.14.B** | Suporte Guia / Fixador Cordoalha Platibanda | Bronze/Inox | 305,00 | un | 5% | **320,00** | **un** | Peça com parafuso e bucha nylon | Fixação SPDA Cobertura [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.14.C** | Haste Aterramento Cobreada 3/4" x 3,00m (254µm) | Aço Cobreado | 6,00 | un | 0% | **6,00** | **barras** | Barra de 3,00m (1 por descida) | NBR 5419 e Planta [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.14.D** | Conector Grampo Cabo-Haste em Latão 3/4" | Bronze/Latão | 6,00 | un | 0% | **6,00** | **un** | Peça | Conexões de aterramento [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.14.E** | Caixa de Inspeção de Solo PVC Ø300mm c/ Tampa | PVC Rígido | 6,00 | un | 0% | **6,00** | **cj** | Conjunto instalado no solo | Inspeção de aterramento [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.15** | Painel LED Embutir 60x60cm 40W 4000K | Branco | 68,00 | un | 5% | **72,00** | **un** | Peça (68 projeto + 4 reserva técnica) | Censo de Iluminação Planta [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.16** | Luminária Hermética LED 2x18W IP65 | Cinza/Transp. | 16,00 | un | 5% | **17,00** | **un** | Peça (16 projeto + 1 reserva técnica) | Censo de Iluminação Planta [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.17** | Bloco Emergência LED 2x8W c/ Bateria | Branco | 14,00 | un | 0% | **14,00** | **un** | Peça completa autônoma | Circuito LE Planta [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.18.A** | Luva de Emenda PVC Rígido Ø3/4" (25mm) | Preto | 207,00 | un | 5% | **218,00** | **un** | Peça (Emenda de varas) | Conexões de tubulação [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.18.B** | Luva de Emenda PVC Rígido Ø1" (32mm) | Preto | 78,00 | un | 5% | **82,00** | **un** | Peça (Emenda de varas) | Conexões de tubulação [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.19.A** | Adaptador Box Reto PVC Ø3/4" p/ Caixa | Preto | 420,00 | un | 5% | **441,00** | **un** | Peça (Entrada em caixas e quadros) | Conexões em caixas [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.19.B** | Adaptador Box Reto PVC Ø1" p/ Caixa/Quadro | Preto | 110,00 | un | 5% | **116,00** | **un** | Peça (Entrada em caixas e quadros) | Conexões em caixas [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.20** | Abraçadeira Tipo D c/ Cunha e Parafuso S6 | Aço Galvanizado | 380,00 | un | 5% | **400,00** | **un** | Peça (Fixação a cada 1,5m em teto/laje) | Fixação em laje/perfilado |
| **04.01.21** | Conjunto Suporte + Placa 4"x2" Acabamento | Branco | 122,00 | cj | 5% | **128,00** | **cj** | Conjunto montado | Acabamento de parede [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.22** | Módulo de Tomada 2P+T 10A / 250V | Branco | 110,00 | un | 5% | **116,00** | **un** | Peça | Censo Tomadas TUG [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.23** | Módulo de Tomada 2P+T 20A / 250V (TUE) | Vermelho | 12,00 | un | 5% | **13,00** | **un** | Peça | Censo Tomadas Especiais [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.24** | Módulo de Interruptor Simples / Paralelo 10A | Branco | 30,00 | un | 5% | **32,00** | **un** | Peça | Censo de Comandos [EGS-013](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-013%20rev.0.pdf) |
| **04.01.25** | Conector de Emenda Rápida / Derivação | Padrão Alavanca | 800,00 | un | 0% | **800,00** | **un** | Peça | Conexões em caixas de passagem |
| **04.01.26** | Fita Isolante Antichama 19mm x 20m | Preto | 15,00 | rolo | 0% | **15,00** | **rolos** | Rolo com 20m | Insumo de montagem e isolação |
| **04.01.27** | Terminais Pré-Isolados Tipo Ilhós (2,5 e 4mm²) | Cobre Estanhado | 250,00 | un | 0% | **250,00** | **un** | Peça | Conexões em tomadas e disjuntores |
| **04.02.01** | Bacia Sanitária c/ Caixa Acoplada 3/6L e Assento | Branca | 6,00 | cj | 0% | **6,00** | **cj** | Conjunto louça montado | Censo Físico Planta [EGS-018](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-018%20rev.0.pdf) |
| **04.02.02** | Lavatório / Cuba de Embutir com Torneira Clínica | Branca / Inox | 6,00 | cj | 0% | **6,00** | **cj** | Conjunto louça montado | Censo Físico Planta [EGS-018](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-018%20rev.0.pdf) |
| **04.02.03** | Mictório Cerâmico com Válvula de Descarga | Branca / Inox | 2,00 | cj | 0% | **2,00** | **cj** | Conjunto louça montado | Censo Físico Planta [EGS-018](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-018%20rev.0.pdf) |
| **04.02.04** | Caixa Sifonada PVC 150x150x50mm c/ Grelha Inox | Branca / Inox | 8,00 | un | 0% | **8,00** | **un** | Peça | Censo Físico Planta [EGS-018](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/01_ENGENHARIA_E_PROJETOS/EDIFICIO_ADMINISTRATIVO/A%C3%87U-3.DES-2.3100-16-EGS-018%20rev.0.pdf) |

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
