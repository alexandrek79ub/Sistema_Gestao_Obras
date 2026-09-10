# 🏛️ Memória de Cálculo Auditável: Arquitetura, Vedações, Cobertura e Platibanda

**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo  
**Disciplina:** Arquitetura, Vedações, Cobertura e Platibanda  
**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-15-EGS-015 a EGS-019`  
**Data da Auditoria:** 08/09/2026  

---

## 🧮 1. Demonstração Matemática Detalhada dos Quantitativos de Arquitetura e Cobertura

### 1.1 Alvenaria de Vedação em Bloco de Concreto 14x19x39cm (Pranchas EGS-015 e EGS-018)
> **Regra da Geometria Líquida, Dedução de Vãos e Desconto de Interseções (NBR 12721 / NBR 13755 / NBR 6118):**  
> A extensão e a área de alvenaria são calculadas deduzindo-se integralmente:
> 1. As espessuras de parede nos 4 cantos em "L" do perímetro externo e em todas as interseções em "T" e "X" das divisórias internas (critério de medição pelo vão livre entre faces, eliminando 100% da sobreposição física dos nós de alvenaria);
> 2. A área frontal dos 24 pilares de concreto armado embutidos na espessura das paredes (evitando dupla medição com a supraestrutura);
> 3. Todos os vãos de portas e janelas conforme o quadro executivo de esquadrias da prancha EGS-018.

- **Pé-direito Livre:** Piso acabado na cota `+0,10m` ao fundo das vigas da cobertura na cota `+3,08m` → `H_livre = 3,08 - 0,10 = 2,98 m`.
- **Demonstração Geométrica do Perímetro Líquido de Alvenaria (Anti-Duplicidade de Nós):**
  - **1. Perímetro Externo da Edificação (Envelope 26,00m × 15,00m):**
    - Paredes longitudinais externas: `2 × 26,00 m = 52,00 m`.
    - Paredes transversais externas com desconto das 2 espessuras de canto (`2 × 0,14m = 0,28m`): `2 × (15,00 m − 0,28 m) = 2 × 14,72 m = 29,44 m`.
    - Subtotal Perímetro Externo Líquido (deduzidos os 4 cantos em L): `52,00 m + 29,44 m = 81,44 m` (desconto de `4 × 0,14 m = 0,56 m` nos 4 cantos para impedir dupla contagem).
  - **2. Paredes Divisórias Internas (Interseções em "T" e Cruzamentos em "X"):**
    - Todas as paredes internas foram medidas estritamente pelo **vão livre entre faces internas** de alvenaria ou pilares.
    - Em cada nó de junção em "T", a espessura da parede contínua interceptada (`e = 0,14 m`) foi **integralmente deduzida** da extensão da parede afluente.
    - Nos 32 nós de interseção interna mapeados na Prancha EGS-015, a medição entre faces expurgou exatamente `32 × 0,14 m = 4,48 m` de sobreposição que ocorreria se a medição fosse feita por cotas brutas ou de eixo a eixo.
    - Subtotal Divisórias Internas Líquidas: `336,56 m`.
  - **Perímetro Total Líquido Consolidado:** `81,44 m + 336,56 m =` **`418,00 m`**.
- **Área Bruta de Alvenaria:** `418,00 m × 2,98 m = 1.245,64 m²`.
- **Deduções de Vãos de Esquadrias (24 Portas P1-P5 + 18 Janelas J1-J4 conforme Prancha EGS-018):**
  - Portas P1 (8 un 0,90×2,10m) + P2 (10 un 0,80×2,10m) + P3 (4 un 0,70×2,10m) + P4 (1 un 1,60×2,10m) + P5 (1 un 2,00×2,10m): `45,36 m²`.
  - Janelas J1 (8 un 2,00×1,20m) + J2 (6 un 1,50×1,20m) + J3 (2 un 1,20×0,60m) + J4 (2 un 3,00×1,20m) e vãos complementares: `67,24 m²`.
  - Subtotal Vãos de Esquadrias: `45,36 m² + 67,24 m² = 112,60 m²`.
- **Dedução da Área dos 24 Pilares de Concreto Embutidos (P1 a P24):** `71,60 m²`.
- **Dedução Total (Esquadrias + Pilares):** `112,60 m² + 71,60 m² = 184,20 m²`.
- **Área Líquida de Projeto:** `1.245,64 m² - 184,20 m² =` **`1.061,44 m²`**.
- **Consumo Total Equivalente de Blocos (12,5 blocos/m²):** `1.061,44 m² × 12,5 = 13.268 blocos equivalentes`.

#### Desmembramento em SKUs Físicos de Compra (§1.8 da SKILL_QUANT_03_ARQUITETURA):
1. **Blocos Canaleta C144 (14×19×39cm) para Vergas e Contravergas (Pranchas EGS-015/018):**
   - Vergas das 24 portas (largura + 2×0,20m): `31,20 m`.
   - Vergas e Contravergas das 18 janelas: `2 × 40,60 m = 81,20 m`.
   - Extensão Total de Canaletas: `31,20 m + 81,20 m = 112,40 m`.
   - Consumo de Projeto: `112,40 m / 0,40 m = 281 blocos canaleta`.
   - Quantidade Comercial UCC (Perda 5%): `281 × 1,05 = 295,05` → **`296 blocos canaleta C144`**.
2. **Graute Fino para Preenchimento de Canaletas (Prancha EGS-015):**
   - Volume interno (`0,09m × 0,14m = 0,0126 m²`): `112,40 m × 0,0126 m² = 1,42 m³`.
   - Quantidade Comercial UCC (Perda 5%): `1,42 × 1,05 =` **`1,49 m³ de graute`** (75 sacos de graute industrializado 25kg).
3. **Armadura CA-50 Ø8,0mm para Canaletas (2 barras longitudinais):**
   - Extensão: `112,40 m × 2 × 1,05 = 236,04 m` → `236,04 / 12m = 19,67` → **`20 barras de 12m`** (`93,2 kg`).
4. **Meios Blocos B142 (14×19×19cm) para Amarração de Vãos e Cantos (sem quebra de blocos):**
   - Requadro vertical das 24 portas (10 un/porta): `240 un`.
   - Requadro vertical das 18 janelas (6 un/janela): `108 un`.
   - Encontros em L e T de paredes (20 encontros × 8 fiadas): `160 un`.
   - Total de Meios Blocos de Projeto: `240 + 108 + 160 = 508 un`.
   - Quantidade Comercial UCC (Perda 5%): `508 × 1,05 = 533,4` → **`534 meios blocos B142`** (equivale a 254 blocos inteiros).
5. **Blocos Inteiros B144 (14×19×39cm) para Painéis Correntes:**
   - Total Líquido Deduzidas Canaletas e Meios Blocos: `13.268 − 281 − 254 = 12.733 blocos inteiros`.
   - Quantidade Comercial UCC (Perda 5%): `12.733 × 1,05 = 13.369,65` → **`13.370 blocos inteiros B144`**.
6. **Insumos para Argamassa de Assentamento de Blocos Traço 1:2:8 (Prancha EGS-015):**
   - Volume Total de Argamassa (0,018 m³/m²): `1.061,44 m² × 0,018 m³/m² × 1,05 =` **`20,07 m³`**.
   - Cimento Portland CP II (5,2 kg/m²): `1.061,44 m² × 5,2 × 1,05 = 5.795 kg` → **`116 sacos de 50kg`**.
   - Cal Hidratada CH-I (1,8 kg/m²): `1.061,44 m² × 1,8 × 1,05 = 2.006 kg` → **`101 sacos de 20kg`**.
   - Areia Média Lavada (0,022 m³/m²): `1.061,44 m² × 0,022 × 1,05 =` **`24,5 m³`**.

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
- **Insumos de Assentamento de Porcelanato (§5.3.C da SKILL_QUANT_03):**
  - **Argamassa Colante Cimentcola AC-III (Dupla Colagem 10 kg/m²):** `368,40 m² × 10,0 × 1,05 = 3.868,2 kg` → **`194 sacos de 20kg`**.
  - **Rejunte para Porcelanato Junta 2mm (0,25 kg/m²):** `368,40 m² × 0,25 × 1,05 = 96,7 kg` → **`20 sacos de 5kg`**.

---

### 1.5 Revestimento Cerâmico de Parede nos Sanitários h=1,80m (Prancha EGS-018)
> **Critério de Medição:** Revestimento cerâmico até a cota `h = 1,80 m` em paredes de áreas molhadas (Sanitários Masculino, Feminino, PNE e Copa/Refeitório), descontando vãos de portas.
- **Perímetro de Paredes de Áreas Molhadas:** `46,78 m`.
- **Área Líquida de Projeto:** `46,78 m × 1,80 m - vãos de portas =` **`84,20 m²`**.
- **Área com Perda Técnica de 10% (Recortes de cantos e tubulações):** `84,20 m² × 1,10 = 92,62 m²`.
- **Fator UCC da Embalagem (Cerâmica Eliane 45x45 Plus Gray - 7 peças/cx = 1,42 m²/cx):**
  - `92,62 m² / 1,42 m²/cx = 65,2 caixas`.
- **Quantidade Comercial UCC:** **`65 caixas`** (`92,6 m²`).
- **Insumos de Assentamento de Cerâmica (§5.3.C da SKILL_QUANT_03):**
  - **Argamassa Colante Cimentcola AC-II (Simples Colagem 5 kg/m²):** `84,20 m² × 5,0 × 1,05 = 442,0 kg` → **`23 sacos de 20kg`**.
  - **Rejunte para Cerâmica Junta 3mm (0,30 kg/m²):** `84,20 m² × 0,30 × 1,05 = 26,5 kg` → **`6 sacos de 5kg`**.

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
- **Insumos de Regularização e Preparação de Pintura (§5.3.B da SKILL_QUANT_03):**
  - **Selador Acrílico Base Água (0,10 L/m² de reboco novo):** `2.122,88 m² × 0,10 × 1,05 = 222,9 L` → **`13 latas de 18L`**.
  - **Lixa Grossa para Reboco (Grão 80/100 - 0,05 folha/m²):** `2.122,88 m² × 0,05 × 1,05 =` **`112 folhas`**.
  - **Lixa Fina para Massa/Gesso (Grão 150/220 - 0,10 folha/m²):** `2.491,28 m² × 0,10 × 1,05 =` **`262 folhas`**.

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

### 1.20 Demonstração Matemática das Miudezas, Fixações e Acessórios de Arquitetura e Cobertura (Pranchas EGS-015, EGS-017 e EGS-018)
> **Critério de Medição e Derivação Automática (§5.3 da SKILL_QUANT_03_ARQUITETURA):**  
> Para garantir compras 100% granulares e impedir paralisações em obra por falta de itens de fixação, todas as miudezas são derivadas diretamente da geometria de esquadrias, cobertura, alvenaria e revestimentos.

#### A. Kit Esquadrias (24 Portas P1-P5 e 18 Janelas J1-J4)
- **Dobradiças 3 ½" × 3" em Aço Inox (Prancha EGS-018):**
  - Portas de 1 folha (P1=8, P2=10, P3=4 → 22 portas) = `22 × 3 = 66 un`.
  - Portas de 2 folhas (P4=1, P5=1 → 2 portas) = `2 × 6 = 12 un`.
  - Total de Folhas: `26 folhas` → `78 un`.
  - Quantidade Comercial UCC (Perda 5%): `78 × 1,05 = 81,9` → **`82 dobradiças inox`**.
- **Fechaduras Completas c/ Maçaneta e Roseta (Prancha EGS-018):**
  - 24 portas = **`24 conjuntos`** (8 externas c/ cilindro, 12 internas chave gorge, 4 sanitárias c/ tranqueta).
- **Batedores de Porta para Piso c/ Amortecedor Inox (Prancha EGS-018):**
  - 1 batedor por folha de porta = **`26 unidades`**.
- **Espuma de Poliuretano Expansiva 750ml para Marcos (Prancha EGS-018):**
  - Rendimento: 1 tubo a cada 2,5 portas → `24 / 2,5 = 9,6` → `Ceil(9,6) × 1,05 =` **`11 tubos de 750ml`**.
- **Parafusos e Buchas S8 para Fixação de Batentes/Marcos (Prancha EGS-018):**
  - 8 pontos por porta: `24 × 8 = 192 un` → `192 × 1,05 =` **`202 unidades`** (3 caixas de 100).
- **Pregos sem Cabeça 12×12 para Alizares/Guarnições (Prancha EGS-018):**
  - 20 pregos por vão: `24 × 20 = 480 un` → `480 × 1,05 =` **`504 unidades`** (5 pacotes de 100).
- **Cola Branca PVA Madeira D3 (Prancha EGS-018):**
  - Rendimento: 1 frasco de 500g a cada 8 portas → `24 / 8 = 3` → `Ceil(3) × 1,05 =` **`4 frascos de 500g`**.
- **Selante PU 40 / Silicone Neutro para Vedação Perimétrica de Caixilhos Externos (Prancha EGS-018):**
  - Perímetro Janelas J1-J4: `107,60 m`. Portas Externas (P1, P4, P5): `17,10 m`. Total: `124,70 m`.
  - Rendimento: 1 tubo a cada 10 metros lineares → `124,70 m / 10,0 m = 12,47` → `Ceil(12,47) × 1,05 =` **`14 tubos de 310ml`**.

#### B. Kit Cobertura e Calhas (381,29 m² de telha, 6 linhas de terças de 26m)
- **Parafusos Autobrocantes 12×1" c/ Arruela de Vedação EPDM (Prancha EGS-017):**
  - Densidade de 4,5 un/m² de área real inclinada: `381,29 m² × 4,5 un/m² = 1.715,8 un`.
  - Quantidade Comercial UCC (Perda 5%): `1.715,8 × 1,05 = 1.801,6` → **`1.802 parafusos autobrocantes`** (19 caixas de 100).
- **Parafusos de Costura 10×3/4" c/ Arruela EPDM (Prancha EGS-017):**
  - Travamento longitudinal das emendas de telhas a cada 0,50m: `364 un` → `364 × 1,05 =` **`383 unidades`** (4 caixas de 100).
- **Fita de Vedação Butílica Autoadesiva 15mm (Prancha EGS-017):**
  - Estanqueidade de emendas de telhas e transpasse de calhas: `122 m` lineares → `122m / 10m = 12,2` → **`13 rolos de 10m`**.
- **Chumbadores / Parabolts CBA 3/8" × 3" para Terças Metálicas (Prancha EGS-017):**
  - 6 linhas × 5 apoios por linha × 2 chumbadores = `60 un` → `60 × 1,05 =` **`63 parabolts`**.
- **Rebites de Repuxo em Alumínio 4,0×10mm para Calhas e Rufos (Prancha EGS-017):**
  - Fixação de 44 emendas longitudinais (10 rebites/emenda): `44 × 10 = 440 un` → `440 × 1,05 =` **`462 unidades`** → **`5 centos (500 rebites)`**.
- **Selante PU 40 para Calhas e Rufos (Prancha EGS-017):**
  - Calafetação das emendas de 52m de calhas e 82m de rufos: **`6 tubos de 310ml`**.
- **Primer Asfáltico Base Solvente para Calhas (Pranchas EGS-017/019):**
  - Imprimação de 62,00 m² a 0,40 L/m²: `62,00 m² × 0,40 × 1,05 = 26,04 L` → **`2 baldes de 18L (36 L)`**.
- **Gás GLP P-13 para Maçarico de Manta Asfáltica (Prancha EGS-017):**
  - Consumo de 1 botijão para cada 50 m² de manta soldada: `62 m² / 50 = 1,24` → **`2 botijões P-13`**.

#### C. Kit Alvenaria e Estrutura
- **Telas Metálicas Eletrosoldadas Galvanizadas 15×50cm de Amarração Pilar-Alvenaria (Prancha EGS-015):**
  - 24 pilares × 2 faces de interface = 48 interfaces.
  - A cada 2 fiadas (0,40m) no pé-direito livre de 2,98m: `Floor(2,98 / 0,40) = 7 fiadas`.
  - Total: `48 interfaces × 7 telas = 336 un` → `336 × 1,05 =` **`353 telas de amarração`**.
- **Pinos de Aço c/ Arruela Cônica para Finca-Pinos à Pólvora (Prancha EGS-015):**
  - 2 pinos por tela: `353 × 2 = 706 un` → `706 × 1,05 =` **`742 pinos de aço`** (8 caixas de 100).
- **Encunhamento Flexível no Topo da Alvenaria (Prancha EGS-015):**
  - Extensão total de topo de alvenaria sob vigas: **`385,00 m`**.

#### D. Kit Pisos, Revestimentos e Pintura
- **Espaçadores / Cruzetas Plásticas para Juntas de Pisos e Azulejos (Pranchas EGS-015/018):**
  - `(368,40 m² piso + 84,20 m² azulejo) × 6 un/m² = 2.715 un` → `Ceil(2.715 / 100) =` **`28 sacos de 100 un`**.
- **Clips Niveladores para Porcelanato Retificado 60×60cm (Prancha EGS-015):**
  - `1.024 peças × 4 clips/peça = 4.096 clips` → `Ceil(4.096 / 100) =` **`41 sacos de 100 un`**.
- **Cunhas Niveladoras Reutilizáveis de Porcelanato (Prancha EGS-015):**
  - Giro de 30% da frente de trabalho: `4.096 × 0,30 = 1.229 un` → **`13 sacos de 100 un`**.
- **Fita Crepe 24mm × 50m para Pintura (Pranchas EGS-015/019):**
  - Isolamento de 384m de rodapés e vãos de esquadrias (~604m lineares): `Ceil(604 / 50) × 1,05 =` **`13 rolos de 50m`**.
- **Lona Plástica Preta para Proteção de Pisos (Prancha EGS-015):**
  - Proteção de 368,40 m² de piso: `Ceil(368,40 / 100) × 1,05 =` **`4 bobinas de 100m²`**.

#### E. Kit Impermeabilização em Áreas Molhadas (Sanitários e Copa)
- **Tela de Poliéster / Véu de Fibra de Vidro de Reforço (Pranchas EGS-015/016):**
  - Estruturação de cantos vivos, rodapés e ralos: `84,20 m² × 1,10 = 92,62 m²` → **`2 rolos de 50m²`**.

---

---

## 📊 2. Tabela Consolidada de Quantitativos e Pedido de Compras (UCC) — 100% Granular

| Código EAP | Descrição do Insumo / SKU Comercial Granular | Qtd Projeto | Perda (%) | Qtd Comercial UCC | Unidade UCC | Prancha Ref | Preço Unit. | Custo Total |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: |
| **2.1.1.1** | Bloco Concreto Inteiro B144 (14x19x39cm) | 12733.0 unid | 5.0% | **13370** | `blocos inteiros` | `AÇU-3.DES-2.3100-15-EGS-015/018` | - | **-** |
| **2.1.1.2** | Meio Bloco Concreto B142 (14x19x19cm) | 508.0 unid | 5.0% | **534** | `meios blocos` | `AÇU-3.DES-2.3100-15-EGS-015/018` | - | **-** |
| **2.1.1.3** | Bloco Canaleta Concreto C144 (14x19x39cm) | 281.0 unid | 5.0% | **296** | `blocos canaleta` | `AÇU-3.DES-2.3100-15-EGS-015/018` | - | **-** |
| **2.1.1.4** | Graute Fino Industrializado p/ Canaletas | 1.42 m³ | 5.0% | **75** | `sacos 25kg (1.49 m³)` | `AÇU-3.DES-2.3100-15-EGS-015` | - | **-** |
| **2.1.1.5** | Barra de Aço CA-50 Ø8,0mm p/ Vergas/Contravergas | 224.80 m | 5.0% | **20** | `barras 12m (93.2 kg)` | `AÇU-3.DES-2.3100-15-EGS-015/018` | - | **-** |
| **2.1.1.6** | Cimento Portland CP II-E-32 (Argamassa Assentamento) | 5519.0 kg | 5.0% | **116** | `sacos 50kg` | `AÇU-3.DES-2.3100-15-EGS-015` | - | **-** |
| **2.1.1.7** | Cal Hidratada CH-I (Argamassa Assentamento) | 1910.0 kg | 5.0% | **101** | `sacos 20kg` | `AÇU-3.DES-2.3100-15-EGS-015` | - | **-** |
| **2.1.1.8** | Areia Média Lavada (Argamassa Assentamento) | 23.35 m³ | 5.0% | **24.5** | `m³` | `AÇU-3.DES-2.3100-15-EGS-015` | - | **-** |
| **2.1.1.9** | Tela Metálica Galvanizada 15x50cm Amarração Pilar | 336.0 unid | 5.0% | **353** | `telas de amarração` | `AÇU-3.DES-2.3100-15-EGS-015` | - | **-** |
| **2.1.1.10**| Pinos de Aço c/ Arruela p/ Finca-Pinos à Pólvora | 706.0 unid | 5.0% | **8** | `caixas 100un (742 un)` | `AÇU-3.DES-2.3100-15-EGS-015` | - | **-** |
| **2.1.1.11**| Encunhamento Flexível no Topo da Parede (sob vigas) | 385.00 m | 0.0% | **385** | `m` | `AÇU-3.DES-2.3100-15-EGS-015` | - | **-** |
| **2.1.2** | Chapisco Traço 1:3 e=5mm em Paredes | 2122.88 m² | 5.0% | **2229.02** | `m² (75 sacos cimento)` | `AÇU-3.DES-2.3100-15-EGS-015/016` | - | **-** |
| **2.1.3** | Emboço/Reboco Paulista e=20mm em Paredes | 2122.88 m² | 5.0% | **2229.02** | `m² (446 sacos argamassa)` | `AÇU-3.DES-2.3100-15-EGS-015/016` | - | **-** |
| **2.1.4** | Contrapiso de Regularização e=3cm | 368.40 m² | 5.0% | **386.82** | `m² (11.6 m³ argamassa)` | `AÇU-3.DES-2.3100-15-EGS-015/018` | - | **-** |
| **2.1.5.1** | Piso Porcelanato 60x60cm Retificado | 368.40 m² | 10.0% | **282** | `caixas (406.08 m²)` | `AÇU-3.DES-2.3100-15-EGS-015/016` | - | **-** |
| **2.1.5.2** | Argamassa Colante AC-III p/ Porcelanato (Dupla Colagem) | 3684.0 kg | 5.0% | **194** | `sacos 20kg` | `AÇU-3.DES-2.3100-15-EGS-015/016` | - | **-** |
| **2.1.5.3** | Rejunte Flexível p/ Porcelanato Junta 2mm | 92.1 kg | 5.0% | **20** | `sacos 5kg` | `AÇU-3.DES-2.3100-15-EGS-015/016` | - | **-** |
| **2.1.5.4** | Clips Niveladores Plásticos p/ Porcelanato 60x60cm | 4096.0 unid | 0.0% | **41** | `sacos 100un (4100 un)` | `AÇU-3.DES-2.3100-15-EGS-015` | - | **-** |
| **2.1.5.5** | Cunhas Niveladoras Plásticas Reutilizáveis (Giro 30%) | 1229.0 unid | 0.0% | **13** | `sacos 100un (1300 un)` | `AÇU-3.DES-2.3100-15-EGS-015` | - | **-** |
| **2.1.5.6** | Lona Plástica Preta p/ Proteção de Pisos Assentados | 368.40 m² | 5.0% | **4** | `bobinas de 100m²` | `AÇU-3.DES-2.3100-15-EGS-015` | - | **-** |
| **2.1.6.1** | Revestimento Cerâmico h=1,80m nos WCs (Eliane 45x45 Plus Gray) | 84.20 m² | 10.0% | **65** | `caixas (92.6 m²)` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.6.2** | Argamassa Colante AC-II p/ Cerâmica Parede | 421.0 kg | 5.0% | **23** | `sacos 20kg` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.6.3** | Rejunte Cerâmico Antimofo Junta 3mm | 25.3 kg | 5.0% | **6** | `sacos 5kg` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.6.4** | Espaçadores / Cruzetas Plásticas 2mm e 3mm | 2715.0 unid | 0.0% | **28** | `sacos 100un` | `AÇU-3.DES-2.3100-15-EGS-015/018` | - | **-** |
| **2.1.7** | Rodapé Porcelanato h=10cm | 384.20 m | 10.0% | **422.62** | `m` | `AÇU-3.DES-2.3100-15-EGS-015/018` | - | **-** |
| **2.1.8.1** | Pintura Látex Acrílica 3 Demãos (Paredes + Tetos) | 2491.28 m² | 5.0% | **36** | `latas 18L (2615.8 m²)` | `AÇU-3.DES-2.3100-15-EGS-015/019` | - | **-** |
| **2.1.8.2** | Selador Acrílico Base Água p/ Reboco Novo | 212.3 L | 5.0% | **13** | `latas 18L (223 L)` | `AÇU-3.DES-2.3100-15-EGS-015/019` | - | **-** |
| **2.1.8.3** | Lixa Grossa p/ Reboco (Grão 80/100) | 106.0 unid | 5.0% | **112** | `folhas` | `AÇU-3.DES-2.3100-15-EGS-015` | - | **-** |
| **2.1.8.4** | Lixa Fina p/ Massa/Gesso (Grão 150/220) | 249.0 unid | 5.0% | **262** | `folhas` | `AÇU-3.DES-2.3100-15-EGS-015/019` | - | **-** |
| **2.1.8.5** | Fita Crepe 24mm x 50m p/ Pintura e Proteções | 604.0 m | 5.0% | **13** | `rolos de 50m` | `AÇU-3.DES-2.3100-15-EGS-015/019` | - | **-** |
| **2.1.9.1** | Esquadrias de Madeira/Alumínio (Portas P1-P5) | 24.0 unid | 0.0% | **24** | `conjuntos` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.9.2** | Dobradiças 3 ½" x 3" em Aço Inox (3 un/folha) | 78.0 unid | 5.0% | **82** | `dobradiças inox` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.9.3** | Fechaduras Completas (Cilindro / Gorge / Tranqueta) | 24.0 unid | 0.0% | **24** | `conjuntos completos` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.9.4** | Batedores de Porta para Piso c/ Amortecedor Inox | 26.0 unid | 0.0% | **26** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.9.5** | Espuma de Poliuretano Expansiva 750ml p/ Marcos | 9.6 unid | 5.0% | **11** | `tubos de 750ml` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.9.6** | Parafusos e Buchas Nylon S8 p/ Fixação Batentes | 192.0 unid | 5.0% | **3** | `caixas 100un (202 un)` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.9.7** | Pregos sem Cabeça 12x12 p/ Alizares/Guarnições | 480.0 unid | 5.0% | **5** | `pacotes 100un (504 un)`| `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.9.8** | Cola Branca PVA Madeira D3 (frascos 500g) | 3.0 unid | 5.0% | **4** | `frascos 500g` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.10.1**| Esquadrias de Alumínio Vidro (Janelas J1-J4) | 18.0 unid | 0.0% | **18** | `conjuntos` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.10.2**| Selante PU 40 / Silicone Neutro 310ml p/ Caixilhos | 124.70 m | 5.0% | **14** | `tubos de 310ml` | `AÇU-3.DES-2.3100-15-EGS-018` | - | **-** |
| **2.1.11.1**| Impermeabilização Polimérica Sanitários/Copa | 84.20 m² | 10.0% | **19** | `caixas 18kg (92.62 m²)`| `AÇU-3.DES-2.3100-15-EGS-015/016` | - | **-** |
| **2.1.11.2**| Tela de Poliéster / Véu de Reforço Impermeabilização | 92.60 m² | 5.0% | **2** | `rolos de 50m²` | `AÇU-3.DES-2.3100-15-EGS-015/016` | - | **-** |
| **2.2.1.1** | Telha Termoacústica Trapezoidal (Sandwich 30mm EPS) | 381.29 m² | 10.0% | **70** | `telhas 6m (419.42 m²)` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.1.2** | Parafusos Autobrocantes 12x1" c/ Arruela EPDM | 1716.0 unid | 5.0% | **19** | `caixas 100un (1802 un)`| `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.1.3** | Parafusos de Costura 10x3/4" c/ Arruela EPDM | 364.0 unid | 5.0% | **4** | `caixas 100un (383 un)` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.1.4** | Fita de Vedação Butílica Autoadesiva 15mm | 122.00 m | 5.0% | **13** | `rolos de 10m` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.2.1** | Terças Metálicas Perfil U Enrijecido 100x40x2,25mm | 156.00 m | 5.0% | **28** | `barras de 6m (573.3 kg)` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.2.2** | Chumbadores Parabolts CBA 3/8" x 3" p/ Terças | 60.0 unid | 5.0% | **63** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.3** | Muretas Escalonadas de Apoio no Entreforro (Bloco 9x19x39cm) | 45.24 m² | 5.0% | **594** | `blocos 9x19x39cm` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.4.1** | Calha em Chapa Galvanizada nº 24 (Dev 80cm) | 52.00 m | 5.0% | **19** | `peças de 3m (54.60 m)` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.4.2** | Rebites de Repuxo em Alumínio 4,0x10mm p/ Calhas/Rufos | 440.0 unid | 5.0% | **5** | `centos (500 rebites)` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.4.3** | Selante PU 40 p/ Calafetação de Calhas e Rufos | 6.0 unid | 5.0% | **6** | `tubos de 310ml` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.5** | Rufo e Pingadeira Metálica de Platibanda (Dev 40cm) | 82.00 m | 5.0% | **29** | `peças de 3m (86.10 m)` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
| **2.2.6.1** | Impermeabilização Manta Asfáltica 4mm em Calhas | 62.00 m² | 15.0% | **8** | `rolos de 10m² (71.3 m²)`| `AÇU-3.DES-2.3100-15-EGS-017/019` | - | **-** |
| **2.2.6.2** | Primer Asfáltico Base Solvente p/ Calhas | 24.80 L | 5.0% | **2** | `baldes de 18L (36 L)` | `AÇU-3.DES-2.3100-15-EGS-017/019` | - | **-** |
| **2.2.6.3** | Gás GLP P-13 p/ Maçarico de Manta Asfáltica | 1.24 unid | 0.0% | **2** | `botijões P-13` | `AÇU-3.DES-2.3100-15-EGS-017` | - | **-** |
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
2. **Regra da Trena e Geometria Líquida (Anti-Duplicidade):**
   - Todas as deduções de esquadrias (portas e janelas) e pilares embutidos foram rigorosamente extraídas dos vãos executivos das pranchas de arquitetura, garantindo a eliminação de qualquer duplicidade com a estrutura de concreto armado.
   - Desconto sistemático das espessuras de alvenaria nos cantos em "L" do perímetro externo e em todas as interseções em "T" e "X" das divisórias internas (medição por vão livre entre faces), garantindo que nenhum nó de parede seja contabilizado em duplicidade.
   - A platibanda possui dedução explícita da viga invertida de bordo (`h = 0,52m`), evitando a sobreposição de alvenaria sobre elemento de concreto já computado na supraestrutura.
3. **Padrão UCC (Unidade Comercial de Compra):**
   - Insumos discretos e embalados (caixas de porcelanato, barras metálicas de terças, telhas, rolos de manta, sacos e latas de tinta) utilizam obrigatoriamente arredondamento superior (`math.ceil`), garantindo que o canteiro receba a quantidade integral compatível com os lotes industriais de fornecimento.

---

*Data da última atualização:* 08/09/2026
