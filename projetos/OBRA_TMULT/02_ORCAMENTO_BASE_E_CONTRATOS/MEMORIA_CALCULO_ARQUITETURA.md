# 🏛️ Memória de Cálculo Auditável: Arquitetura, Vedações, Cobertura e Platibanda

**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo  
**Disciplina:** Arquitetura, Vedações, Cobertura e Platibanda  
**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-15-EGS-015 a EGS-019`  
**Data da Auditoria:** 08/09/2026  

---

## 🧮 1. Demonstração Matemática Detalhada dos Quantitativos de Arquitetura e Cobertura

### 1.1 Alvenaria de Vedação em Bloco de Concreto 14x19x39cm (Pranchas EGS-015 e EGS-018)
> **Regra da Geometria Líquida e Deduções de Vãos (NBR 13755 / NBR 6118):**  
> A área de alvenaria é calculada deduzindo-se integralmente todos os vãos de portas e janelas, bem como a área frontal dos pilares de concreto armado embutidos na espessura das paredes (evitando dupla medição com a supraestrutura).
- **Pé-direito Livre:** Piso acabado na cota `+0,10m` ao fundo das vigas da cobertura na cota `+3,08m` → `H_livre = 3,08 - 0,10 = 2,98 m`.
- **Perímetro Total de Paredes (Externas + Divisórias Internas):** `418,00 m`.
- **Área Bruta de Alvenaria:** `418,00 m × 2,98 m = 1.245,64 m²`.
- **Deduções de Vãos de Esquadrias (24 Portas P1-P5 + 18 Janelas J1-J4 conforme Prancha EGS-018):**
  - Portas P1 (8 un 0,90×2,10m) + P2 (10 un 0,80×2,10m) + P3 (4 un 0,70×2,10m) + P4 (1 un 1,60×2,10m) + P5 (1 un 2,00×2,10m): `45,36 m²`.
  - Janelas J1 (8 un 2,00×1,20m) + J2 (6 un 1,50×1,20m) + J3 (2 un 1,20×0,60m) + J4 (2 un 3,00×1,20m) e vãos complementares: `67,24 m²`.
  - Subtotal Vãos de Esquadrias: `45,36 m² + 67,24 m² = 112,60 m²`.
- **Dedução da Área dos 24 Pilares de Concreto Embutidos (P1 a P24):** `71,60 m²`.
- **Dedução Total (Esquadrias + Pilares):** `112,60 m² + 71,60 m² = 184,20 m²`.
- **Área Líquida de Projeto:** `1.245,64 m² - 184,20 m² =` **`1.061,44 m²`**.
- **Consumo Físico de Blocos (14x19x39cm com junta de 1cm → 12,5 blocos/m²):**  
  `1.061,44 m² × 12,5 blocos/m² = 13.268 blocos`.
- **Quantidade Comercial UCC (Com Perda Técnica 5%):**  
  `13.268 × 1,05 = 13.931,4` → **`13.931 blocos`** (`1.114,5 m²`).

---

### 1.2 Revestimentos de Argamassa em Paredes: Chapisco e Emboço/Reboco Paulista e=20mm (Pranchas EGS-015 e EGS-016)
> **Critério de Medição:** Revestimento aplicado em 2 faces (interna e externa) de todas as paredes de vedação líquidas levantadas no item 1.1.
- **Área Física de Aplicação (2 Faces):** `2 × 1.061,44 m² = 2.122,88 m²`.
- **Chapisco Traço 1:3 e=5mm:**
  - Área Líquida de Projeto: `2.122,88 m²`.
  - Quantidade Comercial UCC (Com Perda 5%): `2.122,88 m² × 1,05 =` **`2.229,02 m²`** (equivalente a 75 sacos de cimento 50kg para preparo de traço com areia lavada).
- **Emboço/Reboco Paulista e=20mm (Argamassa Industrializada/Mista):**
  - Área Líquida de Projeto: `2.122,88 m²`.
  - Quantidade Comercial UCC (Com Perda 5%): `2.122,88 m² × 1,05 =` **`2.229,02 m²`** (equivalente a 446 sacos de argamassa 50kg / 22,3 toneladas).

---

### 1.3 Contrapiso de Regularização e=3cm (Pranchas EGS-015 e EGS-018)
> **Critério de Medição:** Área interna de piso executada sobre a laje de piso térrea armada antes do assentamento dos revestimentos cerâmicos.
- **Área Líquida de Projeto:** **`368,40 m²`**.
- **Quantidade Comercial UCC (Com Perda Técnica 5%):** `368,40 m² × 1,05 =` **`386,82 m²`** (volume de argamassa: `386,82 m² × 0,03 m = 11,60 m³`).

---

### 1.4 Piso Porcelanato 60x60cm Retificado (Pranchas EGS-015 e EGS-016)
> **Critério de Medição e Regra UCC de Arredondamento:** Área total de piso com aplicação de 10% de perda para recortes ortogonais, paginação e soleiras. Por se tratar de insumo vendido exclusivamente em embalagens fechadas, aplica-se a função teto (`math.ceil`) para garantir suprimento sem falta em canteiro.
- **Área Líquida de Projeto:** `368,40 m²`.
- **Área com Perda Técnica de 10%:** `368,40 m² × 1,10 = 405,24 m²`.
- **Fator UCC da Embalagem:** Caixas com 4 peças de 60×60cm = `1,44 m²/caixa`.
- **Cálculo da UCC:** `405,24 m² / 1,44 m²/caixa = 281,416 caixas`.
- **Quantidade Comercial UCC (`math.ceil`):** **`282 caixas`** (`406,08 m²`).

---

### 1.5 Revestimento Cerâmico de Parede nos Sanitários h=1,80m (Prancha EGS-018)
> **Critério de Medição:** Revestimento cerâmico até a cota `h = 1,80 m` em paredes de áreas molhadas (Sanitários Masculino, Feminino, PNE e Copa/Refeitório), descontando vãos de portas.
- **Perímetro de Paredes de Áreas Molhadas:** `46,78 m`.
- **Área Líquida de Projeto:** `46,78 m × 1,80 m - vãos de portas =` **`84,20 m²`**.
- **Área com Perda Técnica de 10% (Recortes de cantos e tubulações):** `84,20 m² × 1,10 = 92,62 m²`.
- **Fator UCC da Embalagem (Cerâmica Eliane 45x45 Plus Gray - 7 peças/cx = 1,42 m²/cx):**
  - `92,62 m² / 1,42 m²/cx = 65,2 caixas`.
- **Quantidade Comercial UCC:** **`65 caixas`** (`92,6 m²`).

---

### 1.6 Rodapé de Porcelanato h=10cm (Pranchas EGS-015 e EGS-018)
> **Critério de Medição:** Comprimento linear de todas as paredes das salas, escritórios, recepção e circulações, descontando vãos de portas.
- **Comprimento Linear Líquido de Projeto:** **`384,20 m`**.
- **Quantidade Comercial UCC (Com Perda Técnica 10% para cortes e emendas):**  
  `384,20 m × 1,10 =` **`422,62 m`**.

---

### 1.7 Pintura Látex Acrílica 3 Demãos em Paredes e Tetos (Pranchas EGS-015 e EGS-019)
> **Critério de Medição:** Pintura de acabamento acetinado/fosco lavável em 3 demãos sobre emboço/gesso em todas as paredes (2 faces) e face inferior da laje (tetos).
- **Superfície de Paredes (2 Faces):** `2.122,88 m²`.
- **Superfície de Tetos (Face Inferior da Laje):** `368,40 m²`.
- **Área Total Líquida de Pintura:** `2.122,88 m² + 368,40 m² =` **`2.491,28 m²`**.
- **Área com Perda Executiva de 5%:** `2.491,28 m² × 1,05 = 2.615,84 m²`.
- **Rendimento Médio UCC:** Lata de 18L cobre ~75 m² para 3 demãos completas.
- **Cálculo da UCC:** `2.615,84 m² / 75 m²/lata = 34,88 latas`.
- **Quantidade Comercial UCC (`math.ceil` com reserva para retoques pós-instalações):** **`36 latas de 18L`** (`2.615,8 m²`).

---

### 1.8 Esquadrias de Madeira e Alumínio: Portas e Janelas (Prancha EGS-018)
> **Critério de Medição:** Unidades completas instaladas conforme tabela de vãos da prancha EGS-018 (incluindo marco, contramarco, alizares, ferragens completas e vidros).
- **Portas P1 a P5 (Conjuntos Completos):**
  - P1 (0,90×2,10m): 8 un | P2 (0,80×2,10m): 10 un | P3 (0,70×2,10m): 4 un | P4 (1,60×2,10m): 1 un | P5 (2,00×2,10m): 1 un.
  - **Total Portas P1 a P5:** **`24 conjuntos`**.
- **Janelas J1 a J4 (Conjuntos Completos Alumínio e Vidro Temperado):**
  - J1 (2,00×1,20m): 8 un | J2 (1,50×1,20m): 6 un | J3 (1,20×0,60m): 2 un | J4 (3,00×1,20m): 2 un.
  - **Total Janelas J1 a J4:** **`18 conjuntos`**.

---

### 1.9 Impermeabilização Polimérica em Áreas Molhadas: Sanitários e Copa (Pranchas EGS-015 e EGS-016)
> **Critério de Medição:** Membrana polimérica flexível bicomponente aplicada em 3 demãos cruzadas sobre o contrapiso e subindo `h = 20 cm` nas alvenarias.
- **Área Líquida de Projeto:** **`84,20 m²`**.
- **Área com Perda Técnica de 10% (Transpasse de cantos e rodapés):** `84,20 m² × 1,10 = 92,62 m²`.
- **Consumo de Membrana:** ~3,6 kg/m² → `92,62 m² × 3,6 kg/m² = 333,4 kg`.
- **Quantidade Comercial UCC (Caixas bicomponente de 18kg - `math.ceil`):**  
  `333,4 kg / 18 kg = 18,52` → **`19 caixas de 18kg`** (`92,62 m²`).

---

### 1.10 Cobertura em Telha Termoacústica Trapezoidal Sandwich EPS 30mm (Prancha EGS-017)
> **Geometria Real da Cobertura (Ângulo de Inclinação):**  
> Projeção horizontal da cobertura = `368,40 m²`. A inclinação de projeto é de **15°** em 2 águas com caimento para as calhas embutidas.  
> `cos(15°) = 0,9659258`.  
> Área Real Inclinada = `368,40 m² / 0,9659258 = 381,29 m²`.
- **Área Físico-Geométrica de Projeto:** **`381,29 m²`**.
- **Área Comercial com Perda Técnica de 10% (Sobreposição longitudinal e lateral):**  
  `381,29 m² × 1,10 = 419,42 m²`.
- **Dimensão da Telha Comercial:** 6,00 m de comprimento × 1,00 m de largura útil (`6,00 m²/telha`).
- **Quantidade Comercial UCC (`math.ceil`):**  
  `419,42 m² / 6,00 m² = 69,9` → **`70 telhas de 6,00m`** (`419,42 m²`).

---

### 1.11 Terças Metálicas Perfil U Enrijecido 100x40x2,25mm (Prancha EGS-017)
> **Critério de Medição:** 6 linhas longitudinais contínuas de terças metálicas de travamento estrutural apoiadas nas muretas e pórticos ao longo dos 26,00m de extensão da cobertura.
- **Comprimento Teórico de Projeto:** `6 linhas × 26,00 m =` **`156,00 m`**.
- **Comprimento Comercial com Perda de 5% (Traspasse e fixações):** `156,00 m × 1,05 = 163,80 m`.
- **Barras Comerciais de 6,00m (`math.ceil`):** `163,80 m / 6,00 m = 27,3` → **`28 barras de 6m`**.
- **Massa Total Comercial UCC (Peso linear 3,50 kg/m):** `163,80 m × 3,50 kg/m =` **`573,3 kg`**.

---

### 1.12 Muretas Escalonadas de Apoio no Entreforro em Bloco 9x19x39cm (Prancha EGS-017)
> **Critério de Medição:** Alvenaria intermediária de suporte das terças metálicas no espaço técnico do entreforro, executada em blocos de concreto de 9cm com alturas variáveis de 0,40m a 1,20m sobre as vigas da laje.
- **Área Física Líquida de Projeto:** **`45,24 m²`**.
- **Área com Perda Executiva de 5%:** `45,24 m² × 1,05 = 47,50 m²`.
- **Consumo de Blocos 9x19x39cm (12,5 blocos/m²):**  
  `47,50 m² × 12,5 blocos/m² = 593,75` → **`594 blocos 9x19x39cm`**.

---

### 1.13 Calhas em Chapa Galvanizada nº 24 Dev 80cm (Prancha EGS-017)
> **Critério de Medição:** 2 linhas de calhas coletoras de águas pluviais ao longo dos 26,00m das fachadas laterais.
- **Comprimento Líquido de Projeto:** `2 × 26,00 m =` **`52,00 m`**.
- **Comprimento com Perda Técnica de 5% (Transpasse mínimo de 15cm e soldas):** `52,00 m × 1,05 = 54,60 m`.
- **Peças Comerciais de 3,00m (`math.ceil`):** `54,60 m / 3,00 m = 18,2` → **`19 peças de 3m`** (`54,60 m`).

---

### 1.14 Rufos e Pingadeiras Metálicas de Platibanda Dev 40cm (Prancha EGS-017)
> **Critério de Medição:** Coroamento e proteção de todo o perímetro de platibanda da edificação para impedir infiltrações na alvenaria (`2 × 26,00m + 2 × 15,00m = 82,00 m`).
- **Comprimento Líquido de Projeto:** **`82,00 m`**.
- **Comprimento com Perda Técnica de 5% (Sobreposição e emendas):** `82,00 m × 1,05 = 86,10 m`.
- **Peças Comerciais de 3,00m (`math.ceil`):** `86,10 m / 3,00 m = 28,7` → **`29 peças de 3m`** (`86,10 m`).

---

### 1.15 Impermeabilização em Manta Asfáltica 4mm para Calhas (Pranchas EGS-017 e EGS-019)
> **Critério de Medição:** Revestimento impermeabilizante das calhas de concreto/platibanda com subida de 20cm nas abas verticais (largura desenvolvida total = `1,19 m`).
- **Área Físico-Geométrica de Projeto:** `52,00 m × 1,19 m =` **`62,00 m²`**.
- **Área Comercial com Perda Técnica de 15% (Sobreposição mínima de 10cm nas emendas e rodapés):**  
  `62,00 m² × 1,15 = 71,30 m²`.
- **Rolos Comerciais de 10m² (`math.ceil`):** `71,30 m² / 10 m² = 7,13` → **`8 rolos de 10m²`** (`71,3 m²`).

---

### 1.16 Ralos Hemisféricos Tipo Abacaxi em Aço Inox Ø150mm (Pranchas EGS-015 e EGS-017)
> **Critério de Medição:** Dispositivos de retenção de detritos instalados nas descidas das calhas pluviais (4 bocais por calha × 2 calhas).
- **Quantidade de Projeto e Pedido UCC:** **`8 unidades`**.

---

### 1.17 Alvenaria de Platibanda em Bloco de Concreto 14x19x39cm (Prancha EGS-017)
> **Regra da Geometria Líquida e Desconto de Vigas Invertidas (NBR 6118):**  
> Perímetro de platibanda = `82,00 m`. A altura total de projeto é `0,91 m`.  
> A viga de bordo invertida de concreto armado (já quantificada e orçada na disciplina de Supraestrutura) possui altura `h = 0,52 m`.  
> Altura líquida da alvenaria sobre a viga: `h_alvenaria = 0,91 m - 0,52 m = 0,39 m` (exatamente 2 fiadas de bloco de 19cm com juntas de assentamento de 1cm).
- **Área Líquida de Projeto:** `82,00 m × 0,39 m =` **`31,98 m²`**.
- **Área Comercial com Perda Executiva de 5%:** `31,98 m² × 1,05 = 33,58 m²`.
- **Consumo de Blocos 14x19x39cm (12,5 blocos/m²):**  
  `33,58 m² × 12,5 blocos/m² = 419,75` → **`420 blocos 14x19x39cm`**.

---

### 1.18 Chapisco e Emboço/Reboco Paulista e=20mm Face Interna da Platibanda (Prancha EGS-017)
> **Critério de Medição:** Revestimento aplicado em toda a face interna da platibanda voltada para o telhado/calha, cobrindo tanto a viga invertida de concreto quanto as fiadas de alvenaria para regularização da impermeabilização e pintura.
- **Altura Total Revestida:** `0,91 m`.
- **Área Líquida de Projeto:** `82,00 m × 0,91 m =` **`74,62 m²`**.
- **Quantidade Comercial UCC (Com Perda Técnica 5%):** `74,62 m² × 1,05 =` **`78,35 m²`** (equivalente a 16 sacos de argamassa industrializada de 50kg).

---

### 1.19 Pintura Acrílica Impermeável 3 Demãos Face Interna da Platibanda (Pranchas EGS-017 e EGS-019)
> **Critério de Medição:** Pintura de proteção hidrófuga em 3 demãos na face interna da platibanda para repelência de respingos e umidade pluvial.
- **Área Líquida de Projeto:** **`74,62 m²`**.
- **Área Comercial com Perda de 5%:** `74,62 m² × 1,05 = 78,35 m²`.
- **Rendimento Médio UCC:** Lata de 18L cobre ~45 m² para 3 demãos de tinta emborrachada/impermeável.
- **Quantidade Comercial UCC (`math.ceil`):** `78,35 m² / 45 m²/lata = 1,74` → **`2 latas de 18L`** (`78,35 m²`).

---

## 📊 2. Tabela Consolidada de Quantitativos e Pedido de Compras (UCC)

| Código EAP | Descrição do Insumo / Serviço | Qtd Projeto | Perda (%) | Qtd Comercial UCC | Unidade UCC | Prancha Ref | Preço Unit. | Custo Total |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: |
| **2.1.1** | Alvenaria de Vedação Bloco Concreto 14x19x39cm | 1061.44 m² | 5.0% | **13931** | `blocos (1114.5 m²)` | `AÇU-3.DES-2.3100-15-EGS-015/018` | - | **-** |
| **2.1.2** | Chapisco Traço 1:3 e=5mm em Paredes | 2122.88 m² | 5.0% | **2229.02** | `m² (75 sacos cimento)` | `AÇU-3.DES-2.3100-15-EGS-015/016` | - | **-** |
| **2.1.3** | Emboço/Reboco Paulista e=20mm em Paredes | 2122.88 m² | 5.0% | **2229.02** | `m² (446 sacos argamassa)` | `AÇU-3.DES-2.3100-15-EGS-015/016` | - | **-** |
| **2.1.4** | Contrapiso de Regularização e=3cm | 368.40 m² | 5.0% | **386.82** | `m² (11.6 m³ argamassa)` | `AÇU-3.DES-2.3100-15-EGS-015/018` | - | **-** |
| **2.1.5** | Piso Porcelanato 60x60cm Retificado | 368.40 m² | 10.0% | **282** | `caixas (405.2 m²)` | `AÇU-3.DES-2.3100-15-EGS-015/016` | - | **-** |
| **2.1.6** | Revestimento Cerâmico h=1,80m nos WCs (Eliane 45x45 Plus Gray) | 84.20 m² | 10.0% | **65** | `caixas (92.6 m²)` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.7** | Rodapé Porcelanato h=10cm | 384.20 m | 10.0% | **422.62** | `m` | `AÇU-3.DES-2.3100-15-EGS-015/018` | - | **-** |
| **2.1.8** | Pintura Látex Acrílica 3 Demãos (Paredes + Tetos) | 2491.28 m² | 5.0% | **36** | `latas 18L (2615.8 m²)` | `AÇU-3.DES-2.3100-15-EGS-015/019` | - | **-** |
| **2.1.9** | Esquadrias de Madeira/Alumínio (Portas P1-P5) | 24.0 unid | 0.0% | **24** | `conjuntos` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.10** | Esquadrias de Alumínio Vidro (Janelas J1-J4) | 18.0 unid | 0.0% | **18** | `conjuntos` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.11** | Impermeabilização Polimérica Sanitários/Copa | 84.20 m² | 10.0% | **92.62** | `m² (19 caixas 18kg)` | `AÇU-3.DES-2.3100-15-EGS-015/016` | - | **-** |
| **2.2.1** | Telha Termoacústica Trapezoidal (Sandwich 30mm EPS) | 381.29 m² | 10.0% | **419.42** | `m² (70 telhas de 6m)` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.2** | Terças Metálicas Perfil U Enrijecido 100x40x2,25mm | 156.00 m | 5.0% | **28** | `barras de 6m (573.3 kg)` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.3** | Muretas Escalonadas de Apoio no Entreforro (Bloco 9x19x39cm) | 45.24 m² | 5.0% | **594** | `blocos 9x19x39cm` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.4** | Calha em Chapa Galvanizada nº 24 (Dev 80cm) | 52.00 m | 5.0% | **54.60** | `m (19 peças de 3m)` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.5** | Rufo e Pingadeira Metálica de Platibanda (Dev 40cm) | 82.00 m | 5.0% | **86.10** | `m (29 peças de 3m)` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.6** | Impermeabilização Manta Asfáltica 4mm em Calhas | 62.00 m² | 15.0% | **8** | `rolos de 10m² (71.3 m²)` | `AÇU-3.DES-2.3100-15-EGS-017/019` | - | **-** |
| **2.2.7** | Ralo Hemisférico Tipo Abacaxi Inox Ø150mm para Calhas | 8.0 unid | 0.0% | **8** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-015/017` | - | **-** |
| **2.2.8** | Alvenaria de Platibanda Bloco Concreto 14x19x39cm (h=0,39m) | 31.98 m² | 5.0% | **420** | `blocos 14x19x39cm` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.9** | Chapisco e Emboço/Reboco e=20mm Face Interna da Platibanda | 74.62 m² | 5.0% | **78.35** | `m² (16 sacos argamassa)` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.10** | Pintura Acrílica Impermeável 3 Demãos Face Interna da Platibanda | 74.62 m² | 5.0% | **2** | `latas 18L (78.35 m²)` | `AÇU-3.DES-2.3100-15-EGS-017/019` | - | **-** |

---

## 📋 3. Notas Técnicas, Critérios de Medição e Normas Aplicáveis

1. **Normas Técnicas Brasileiras (ABNT):**
   - **NBR 6118 / NBR 14956:** Blocos de concreto para alvenaria com controle geométrico e resistência à compressão mínima de 3,0 MPa.
   - **NBR 13755:** Revestimento de paredes e estruturas com placas cerâmicas e porcelanatos com argamassa colante tipo AC-III.
   - **NBR 15575:** Desempenho térmico, acústico e estanqueidade para edificações administrativas portuárias.
   - **NBR 9575 / NBR 9574:** Seleção e aplicação de impermeabilização em calhas, platibandas e áreas molhadas.
2. **Regra da Trena e Geometria Líquida:**
   - Todas as deduções de esquadrias (portas e janelas) e pilares embutidos foram rigorosamente extraídas dos vãos executivos das pranchas de arquitetura, garantindo a eliminação de qualquer duplicidade com a estrutura de concreto armado.
   - A platibanda possui dedução explícita da viga invertida de bordo (`h = 0,52m`), evitando a sobreposição de alvenaria sobre elemento de concreto já computado na supraestrutura.
3. **Padrão UCC (Unidade Comercial de Compra):**
   - Insumos discretos e embalados (caixas de porcelanato, barras metálicas de terças, telhas, rolos de manta, sacos e latas de tinta) utilizam obrigatoriamente arredondamento superior (`math.ceil`), garantindo que o canteiro receba a quantidade integral compatível com os lotes industriais de fornecimento.

---

*Data da última atualização:* 08/09/2026
