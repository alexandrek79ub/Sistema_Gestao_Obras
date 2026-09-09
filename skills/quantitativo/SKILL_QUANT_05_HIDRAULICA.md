# 💧 SKILL 05: Instalações Hidráulicas (MEP)

**Disciplina:** Água Fria, Água Quente, Esgoto e Pluvial.
**Dependência:** `SKILL_QUANTIFICACAO_MASTER.md`

## 1. Escopo de Levantamento
- **Tubos:** PVC Soldável (Água Fria), PPR/CPVC (Água Quente), PVC Série Normal/Reforçada (Esgoto).
- **Conexões:** Joelhos (Cotovelos), Tês, Luvas, Caps, Reduções.
- **Registros e Válvulas:** Registros de Gaveta (Geral), Pressão (Chuveiro), Válvulas de Retenção.
- **Louças e Metais:** Bacias, Cubas, Torneiras, Sifões, Engates flexíveis.

## 2. Regras Matemáticas, Esquemas Isométricos e Detalhamento de Pontos

### 2.1 Leitura Obrigatória de Isométricos e Cálculo de Prumadas Verticais (Eixo Z)
- **Extensão Horizontal (X, Y):** Medição da tubulação em planta baixa (trecho embutido no piso/alvenaria ou aparente).
- **Leitura de Desenhos Isométricos (Subidas e Descidas - $\Delta Z$):** Os trechos verticais **DEVEM ser extraídos diretamente dos Esquemas Isométricos de Água Fria/Quente e Prumadas de Esgoto/Gás**:
  - `Ponto de Chuveiro (h = 2,10m a 2,20m do piso):` Subida vertical do ponto de distribuição ou ramal.
  - `Ponto de Lavatório / Pia de Cozinha (h = 0,60m a 1,10m do piso).`
  - `Ponto de Bacia Sanitária c/ Caixa Acoplada (h = 0,20m do piso) / Válvula de Descarga (h = 1,10m).`
  - `Prumadas Verticais (Shafts):` $L_{\text{prumada}} = (H_{\text{pé-direito}} + e_{\text{laje}}) \times N_{\text{pavimentos}} + \text{Interligação Barrilete/Subsolo}$.
- **Taxa de Perda:** Adicionar **10%** no total medido.
- **Regra UCC:** 
  - Tubos Soldáveis (Água): Barras de **3 metros** ou **6 metros** (arredondar CIMA).
  - Tubos de Esgoto: Barras de **6 metros**.

### 2.2 Detalhamento Meticuloso de Registros, Conexões e Kits de Terminais
Toda prumada ou kit de ponto hidráulico deve ser decomposto individualmente nos seus componentes de compra:
- **Registros e Válvulas de Controle:**
  - `Registro de Gaveta Bruto / c/ Canopla (unid):` Registro de fecho geral de ambiente (DN 20mm/25mm/32mm / 3/4", 1", 1 1/4") c/ acabamento cromado.
  - `Registro de Pressão p/ Chuveiro c/ Canopla (unid):` Registro de regulagem de vazão de chuveiro (DN 20mm / 3/4") c/ acabamento cromado.
  - `Válvula de Retenção Vertical / Horizontal (unid):` Para prevenção de refluxo em saídas de reservatórios e recalques.
  - `Válvula Redutora de Pressão - VRP (unid):` Para pavimentos inferiores com pressão manométrica acima de $40\text{ mca}$ (NBR 5626).
- **Conexões Detalhadas do Isométrico (Peça por Peça):**
  - `Joelho / Cotovelo 90º e 45º (Soldável, PPR, Esgoto c/ Bolsa - unid).`
  - `Joelho 90º c/ Bucha de Latão (unid):` Para transição soldável $\to$ roscável nas pontas de torneiras, chuveiros e duchas higiênicas ($25mm \times 1/2"$ / $20mm \times 1/2"$).
  - `Tê 90º Igual / Tê de Redução / Tê c/ Bucha de Latão (unid).`
  - `Luva de Redução / Luva de Correr (unid).`
  - `Curva de Transposição (unid):` Peça especial para transpor cruzamento de tubulações embutidas sem colisão.
- **Kits de Ligação e Terminais Sanitários:**
  - `Engate Flexível Inox / PVC (unid):` Rabicho flexível $40\text{cm} / 50\text{cm}$ (DN 1/2") para lavatórios, pias e bacias sanitárias.
  - `Sifão Sanfonado Universal / Sifão de Copo Cromado (unid):` Sifão para lavatório e pia de cozinha c/ adaptador rígido.
  - `Válvula de Escoamento / Ralo de Pia (unid):` Válvula inox $7/8"$ / $1 1/2"$ / $3 1/2"$ c/ tampão.
  - `Fita Veda-Rosca PTFE (rolo):` Rolos de $18\text{mm} \times 50\text{m}$ (1 rolo a cada 15 pontos roscados).

## 3. Modelo de Memória de Cálculo (Hidráulica)
```text
╔══════════════════════════════════════════════════════════════════╗
║        MEMÓRIA DE CÁLCULO — INSTALAÇÕES HIDRÁULICAS             ║
╠══════════════════════════════════════════════════════════════════╣
║  AMBIENTE: [T-101-BAN]   SISTEMA: [Esgoto Sanitário]            ║
╠══════════════════════════════════════════════════════════════════╣
║  TUBULAÇÃO (PVC Esgoto Série Normal DN 100mm):                  ║
║    Trecho horizontal: X,XX m | Prumada: X,XX m                  ║
║    Subtotal: X,XX m + Perda 10% = X,XX m                        ║
║                                                                  ║
║  CONEXÕES E ACESSÓRIOS:                                          ║
║    Joelho 90º DN 100mm: 2 unid                                   ║
║    Junção Y 100x50mm: 1 unid                                     ║
║    Ralo Sifonado 150x150x50mm: 1 unid                            ║
║    Vaso Sanitário com Caixa Acoplada: 1 conjunto                 ║
╚══════════════════════════════════════════════════════════════════╝
```

## 4. Tabela Final de Compra (UCC)
O relatório final deve somar o total em metros e transformar em barras inteiras.
Exemplo: Se a obra precisa de 21 metros de Tubo Soldável 25mm, e a barra fornecida pela Tigre/Amanco é de 6 metros, a solicitação de compra final será de **4 Barras** (24m).

---

## 5. Caixas Enterradas de Infraestrutura Hidráulica/Elétrica (Concreto vs. Alvenaria)

> ⚠️ **REGRA DE CAIXAS ENTERRADAS:** O quantitativo de caixas de inspeção, passagem, gordura, sabão, retenção e drenagem DEVE derivar automaticamente todos os insumos de escavação, **talude de segurança (NR-18 para $H > 1,25m$)**, fôrmas internas/externas, concreto, aço, emboço interno, impermeabilização e tampas.

### 5.1 Geometria e Parâmetros de Entrada da Caixa
| Parâmetro | Descrição Técnica | Aplicação Geométrica |
|---|---|---|
| $A, C$ | Dimensões Internas em Planta (m) | Largura útil ($A$) e Comprimento útil ($C$) da caixa |
| $B, D$ | Dimensões Externas em Planta (m) | $B = A + 2 \cdot E$ e $D = C + 2 \cdot E$ (inclui espessuras) |
| $E$ | Espessura das Paredes da Caixa (m) | Tipicamente 0,10m a 0,15m (concreto) ou 0,12m/0,25m (alvenaria) |
| $F$ | Espessura da Laje de Fundo (m) | Laje de fundo em concreto (tipicamente 0,08m a 0,15m) |
| $G$ | Altura Interna Útil (m) | Projeção vertical útil do fluxo/inspeção |
| $H$ | Altura Total Externa da Cava (m) | $H = G + F + I$ (profundidade total de escavação) |
| $I$ | Espessura da Tampa de Concreto (m) | Tampa superior estrutural (tipicamente 0,07m a 0,10m) |

### 5.2 Fórmulas Integradas de Derivação de Serviços (Caixa de Concreto)
```text
1. Escavação da Cava com Folga Lateral (m³):
   V_escav = [(B + 2 × folga) × (D + 2 × folga)] × H

2. Talude de Segurança NR-18 (para profundidade H > 1,25 m - m³):
   V_talude = [(B + folga) + (D + folga) × (H − 1,25) / 4] × (H − 1,25)²

3. Apiloamento do Fundo (m²) e Lastro de Concreto/Brita (m³):
   A_apiloam = (B + 0,10m) × (D + 0,10m)
   V_lastro = A_apiloam × e_lastro  (e = 0,05m a 0,10m)

4. Reaterro Compactado (m³) e Bota-Fora (m³):
   V_reaterro = (V_escav + V_talude) − (B × D × H)
   V_bota_fora = (V_escav + V_talude) − V_reaterro

5. Fôrma Dupla Face e Fôrma da Tampa (m²):
   A_forma_ext = (B + D) × 2 × H   (fôrma externa)
   A_forma_int = (A + C) × 2 × G   (fôrma interna)
   A_forma_tampa = (B × D) + 2 × (B + D) × I  (fôrma da tampa)
   A_forma_total = A_forma_ext + A_forma_int + A_forma_tampa

6. Concreto Estrutural da Caixa e Tampa (m³):
   V_concreto_fundo = B * D * F
   V_concreto_paredes = 2 * (C + B) * E * G
   V_concreto_tampa = B * D * I
   V_concreto_total = V_concreto_fundo + V_concreto_paredes + V_concreto_tampa

7. Revestimento Interno e Impermeabilização (m²):
   A_imperm_int = (A * C * G) + (A * C)

8. Armadura Aço CA-50 (kg):
   Peso_aço = V_concreto_total * Taxa_Aço
```

### 5.3 Comparativo Executivo: Caixa de Concreto vs. Caixa de Alvenaria

#### A. Caixa de Concreto Armado (Moldada in loco / Pré-moldada)
- **Aplicação:** Cavas profundas (H > 1,00m), solo com nível d'água ou áreas sujeitas a tráfego de veículos.
- **Consumo de Paredes:** Paredes de Concreto Armado (m³) + Fôrmas Dupla Face (m²).

#### B. Caixa de Alvenaria (Tijolo Maciço ou Bloco de Concreto)
- **Aplicação:** Caixas rasas a médias (H <= 1,00m) em passeios, jardins e áreas de pedestres.
- **Sem Fôrma de Parede:** Elimina fôrmas nas paredes verticais.
- **Fórmula de Paredes de Alvenaria (m²):**
  `A_alvenaria_parede = 2 * (B + C) * G`
  *(Onde B e C são as dimensões em planta das paredes e G é a altura útil).*
- **Insumos Derivados de Caixa de Alvenaria:**
  1. Escavação com Folga (m³) + Talude NR-18 (m³)
  2. Apiloamento (m²) + Lastro de Concreto Magro / Brita (m³)
  3. Laje de Fundo em Concreto (m³) + Fôrma da Laje de Fundo (m²)
  4. Paredes em Alvenaria de Tijolo Maciço ou Bloco (m²)
  5. Revestimento Interno / Impermeabilização (m²)
  6. Tampa de Concreto Armado ou Ferro Fundido (FoFo)
  7. Reaterro Compactado (m³) vs. Bota-Fora (m³)

---

## 6. Redes Subterrâneas e Tubulações de Água, Esgoto, Incêndio e Gás Combustível

> ⚠️ **SISTEMAS MEP ENTERRADOS E ESPECIAIS:** Além das caixas, o levantamento DEVE quantificar as tubulações enterradas e especiais para Água, Esgoto, Incêndio e Gás (Cobre Rígido, Cobre Recozido Flexível e Multicamada PEX-Gas).

### 6.1 Redes Enterradas de Água, Esgoto e Drenagem (PVC, PEAD, Corrugado Dreno)
- **Valas de Tubulação Subterrânea:**
  - `Escavação de Vala (m³):` $V_{\text{escav}} = (\text{Diâmetro} + 0,30m) \times \text{Profundidade\_H} \times L_{\text{tubo}}$
  - `Colchão de Areia Lavada (m³):` $V_{\text{areia}} = (\text{Diâmetro} + 0,30m) \times (0,10m_{\text{inferior}} + \text{Diâmetro} + 0,10m_{\text{superior}}) \times L_{\text{tubo}}$
  - `Reaterro e Bota-fora (m³):` $V_{\text{reaterro}} = V_{\text{escav}} - V_{\text{areia}} - V_{\text{tubo}}$
  - `Fita Sinalizadora (m):` Fita azul (Água) ou Fita marrom (Esgoto) a 30cm abaixo da superfície.
- **Regra UCC:** Tubos rígidos em barras de 6m (PVC Soldável/Série Normal/Reforçada) ou rolos de 50m/100m (PEAD).

### 6.2 Rede de Combate a Incêndio Enterrada e Aparente (NBR 13714 / NBR 5580 / NBR 5590)
- **Tubulações de Aço Carbono:**
  - `Aço Galvanizado c/ Costura / Sem Costura:` Diâmetros 2 1/2", 3", 4", 6" (conexões ranhuradas *Grooved* ou rosqueadas NPT/BSP em barras de 6m).
  - `Proteção de Tubo de Incêndio Enterrado:` Pintura epóxi/antiferrugem + fita anticorrosiva de proteção mecânica (Fita Denso/Petrotape em $m$) + envelopamento de areia ou concreto magro.
- **Equipamentos de Hidrante:**
  - `Abrigos de Hidrante (unid):` Caixas de embutir/sobrepor em aço c/ visor vermelho e vidro.
  - `Válvulas Angulares 45º (unid), Mangueiras Tipo 2/3 (lanços de 15m) e Esguichos Reguláveis (unid).`
  - `Válvula de Governo e Alarme (VGA) e Chaves de Fluxo (unid).`

### 6.3 Rede de Gás Combustível GLP / Gás Natural (NBR 15526 / NBR 15358) — Cobre Rígido, Flexível & Multicamada
- **Tipologias de Tubulação de Gás:**
  1. `Tubo de Cobre Rígido (Classe I / Classe A):` Barras de 5m ou 6m (diâmetros 15mm, 22mm, 28mm, 35mm, 42mm, 54mm) unidas por brasagem/solda foscoper/prata c/ conexões de cobre/latão.
  2. `Tubo Multicamada PEX-AL-PEX / PE-AL-PE (Amarelo Gás):` Tubo flexível com alma de alumínio em rolos de 50m ou 100m (diâmetros 16mm, 20mm, 26mm, 32mm) c/ conexões de prensagem/crimpagem (*Press Fitting*).
  3. `Tubo de Cobre Recozido Flexível (Rolo):` Para ligações de reguladores de pressão, chicotes e pontas de fogão/aquecedor.
  4. `Tubo de Aço Carbono Schedule 40:` Para prumadas de alta vazão e média pressão.
- **Camisa de Proteção (Tubo-Luva Obrigatório em PVC/Aço):**
  - `Tubo-Luva Ventilado (m):` Em travessias de paredes, lajes ou trechos embutidos sem ventilação direta, a norma exige a passagem da tubulação de gás por dentro de uma **Camisa de Proteção em PVC (Tubo-Luva)** de diâmetro superior, com extremidades abertas para o exterior para escoamento de eventual vazamento.
- **Segurança de Gás Enterrado:**
  - `Fita Advertência Amarela ("CUIDADO GÁS COMBUSTÍVEL"):` Instalada sobre o leito de areia da vala de gás.
  - `Reguladores de Pressão (1º e 2º Estágio), Válvulas de Esfera Gás 300 PSI (unid) e Central de GLP (P-45, P-190 ou Tanque Estacionário).`

---

## 7. Entrada de Água Potável, Cavalete, Cisternas, Caixas D'Água e Castelo D'Água Elevado (NBR 5626 / NBR 12218)

### 7.1 Cavalete e Padrão de Entrada da Concessionária de Água
- `Abrigo de Hidrômetro / Cavalete (unid):` Nicho em alvenaria revestida ou caixa pré-fabricada em policarbonato c/ porta em alumínio e grade.
- `Conjunto Cavalete e Registro Concessionária (unid):` Tubulação em tubos de ferro fundido / PPR / PVC Soldável DN 25mm a 75mm + registro de gaveta + torneira de tomada de ensaio + conexões de padrão de concessionária local (ex: Sabesp, Sanepar, Copasa, Cedae).

### 7.2 Reservatório Inferior (Cisterna) e Caixas D'Água
- `Reservatório Inferior de Concreto Armado / Cisterna (m³ / m²):` Cava de escavação ($m³$) + estrutura de concreto armado C30 c/ aditivo impermeabilizante ($m³$) + fôrmas ($m²$) + armadura ($kg$) + impermeabilização dupla em argamassa polimérica flexível / resina termoplástica ($m²$).
- `Reservatórios em Polietileno / Fibra de Vidro (PRFV) / Aço Inox (unid ou volume m³):` Reservatórios industrializados de 500L, 1000L, 2000L, 5000L, 10.000L c/ tampas roscadas herméticas.
- `Acessórios de Reservatórios (unid):` Torneira de boia de alto fluxo em latão (DN 3/4" a 2"), tubo extravasor (ladrão) em PVC, tubo de limpeza de fundo c/ registro de esfera e respiro de respiro c/ tela mosquiteira.

### 7.3 Castelo D'Água Elevado e Reservatórios de Torre
- `Castelo D'Água Metálico Prismático / Taça (unid):` Reservatório metálico elevado em chapa de aço carbono c/ revestimento interno epóxi alimentício (atóxico) e pintura externa poliuretana ($5.000L$ a $100.000L$).
- `Castelo D'Água Elevado em Concreto Armado (m³ / m²):` Pilar central/fuste de elevação + reservatório superior duplo (compartimento de Água Potável + Reserva Técnica de Incêndio - RTI).
- `Acessórios de Torre e Segurança (unid ou m):`
  - Escada marinheiro metálica galvanizada c/ gaiola de proteção contra queda (NR-12 / NR-35).
  - Escada interna de inspeção em inox.
  - Para-raios de topo (Franklin) + iluminação de sinalização noturna de obstáculo para aviação (FAA/ICAO).
  - Medidor de nível / chave de nível de boia automática para acionamento de bombas.

### 7.4 Medição Individualizada por Unidade Habitacional (Água e Gás por Apartamento/Casa/Loja)
- **Kit de Medição Individualizada de Água (1 unid por Unidade Habitacional):**
  - `Hidrômetro Individual da Unidade (unid):` Hidrômetro monojato/multijato DN 15mm ($1/2"$) ou DN 20mm ($3/4"$) c/ emissor de pulsos / leitor para telemetria sem fio (radiofrequência).
  - `Caixa de Embutir de Medição no Hall / Shaft (unid):` Caixa em inox/metálica/plástica de sobrepor ou embutir no hall de circulação do andar.
  - `Registros de Corte e Conexões do Kit (unid):` Registro de esfera monobloco c/ borboleta + porca giratória c/ furo para lacre da concessionária/administração.
- **Kit de Medição Individualizada de Gás Combustível (1 unid por Unidade Habitacional):**
  - `Medidor de Gás Diafragma / Eletrônico da Unidade (unid):` Medidor residencial de vazão $1,5m³/h$ a $2,5m³/h$ (G1.6 / G2.5) especificando se é para GLP ou Gás Natural.
  - `Regulador de Pressão de 2º Estágio (unid):` Regulador individual $kPa \to mmca$ (especificado para $2,8\text{ kPa}$ / $280\text{ mmca}$).
  - `Válvula de Esfera c/ Trava de Segurança (unid):` Válvula de fecho rápido para corte individual c/ furação para lacre.
  - `Chicote / Flexível de Latão de Ligação (unid):` Flexível metálico para acoplamento no medidor.
