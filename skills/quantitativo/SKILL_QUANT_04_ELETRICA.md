# ⚡ SKILL 04: Instalações Elétricas (MEP)

**Disciplina:** Elétrica e Lógica
**Dependência:** `SKILL_QUANTIFICACAO_MASTER.md`

## 1. Escopo de Levantamento
O Agente deve extrair quantidades dos projetos unifilares elétricos, separando-os por:
- **Eletrodutos:** Conduítes corrugados (embutidos) e tubos rígidos (aparentes).
- **Condutores:** Fios e Cabos (seção em mm² e cores - Fase, Neutro, Terra, Retorno).
- **Caixas:** Passagem, tomadas e interruptores (4x2, 4x4, octogonais).
- **Quadros:** Quadros de Distribuição (QDC) e Disjuntores (DPS, DR, Termomagnéticos).

## 2. Regras Matemáticas, Descidas Verticais e Tolerâncias

### 2.1 Cálculo de Eletrodutos e Descidas Verticais (Eixo Z)
- **Trecho Horizontal (X, Y):** Medição da projeção em planta baixa do eletroduto no teto, forro ou piso.
- **Descidas e Subidas Verticais ($\Delta Z$):** Calculadas obrigatoriamente pela diferença de cota entre o plano de caminhamento (forro/laje ou contrapiso) e a cota de instalação do ponto/caixa:
  - `Tomada Baixa (h = 0,30m do piso):` Descida do teto = $H_{\text{pé-direito}} - 0,30\text{m}$.
  - `Tomada Média / Interruptor (h = 1,10m do piso):` Descida do teto = $H_{\text{pé-direito}} - 1,10\text{m}$.
  - `Tomada Alta (Chuveiro / Ar-condicionado / Exaustor h = 2,10m a 2,20m):` Descida do teto = $H_{\text{pé-direito}} - 2,10\text{m}$.
  - `Prumadas de Shaft / Subestação:` Comprimento vertical da prumada entre pavimentos multiplicada pelo número de andares $+$ travessia de lajes.
- **Taxa de Perda:** Adicionar **10%** sobre o comprimento total calculado.
- **Regra UCC:** Comprar eletrodutos flexíveis sempre em múltiplos de **50 metros** (Rolo padrão). Tubos rígidos em múltiplos de **3 metros**.

### 2.2 Fios e Cabos — Método de Quantificação por Circuito (Fase, Neutro, Terra e Retorno)
A metragem de condutores **NÃO é uma simples multiplicação do comprimento do eletroduto pelo número total de fios**. O levantamento DEVE ser feito **trecho a trecho, circuito por circuito**, multiplicando a extensão real do eletroduto (horizontal $+$ descidas verticais) pela quantidade de condutores de cada função presentes naquele trecho (indicados pela simbologia unifilar: Fase `|`, Neutro `┬`, Terra `┴`, Retorno `/`).

#### A. Algoritmo de Cálculo por Trecho de Eletroduto
Para cada trecho de eletroduto $k$ percorrido pelo circuito $c$:
1. **Comprimento do Trecho ($L_k$):** $L_k = L_{\text{horizontal}(X,Y)} + \Delta Z_{\text{descida/subida}}$.
2. **Cálculo da Metragem por Tipo de Condutor (Função e Cor NBR 5410):**
   - **Fase (Preto / Vermelho / Castanho):** $L_{\text{fase}} = \sum (L_k \times N_{\text{condutores\_fase}_k})$.
   - **Neutro (Azul Claro — Cor Obrigatória NBR 5410):** $L_{\text{neutro}} = \sum (L_k \times N_{\text{condutores\_neutro}_k})$.
   - **Proteção / Terra (Verde ou Verde-Amarelo — Cor Obrigatória NBR 5410):** $L_{\text{terra}} = \sum (L_k \times N_{\text{condutores\_terra}_k})$.
   - **Retorno (Amarelo / Branco):** $L_{\text{retorno}} = \sum (L_k \times N_{\text{condutores\_retorno}_k})$ (trechos entre interruptores e lâmpadas / Three-way / Four-way).

#### B. Sobras de Pontas (Folga Técnica Obrigatória)
Para cada caixa de passagem, tomada, interruptor ou luminária acessada pelo circuito, e no Quadro de Distribuição (QDC), adicionar as sobras para desencapamento e conexão:
- `Caixas de Tomada / Interruptor / Passagem / Luminária:` Adicionar **$+0,50 \, \text{m}$** por condutor para CADA caixa acessada pelo circuito.
- `Quadro de Distribuição (QDC):` Adicionar **$+1,00 \, \text{m}$** por condutor dentro do QDC para penteamento e fixação no disjuntor/barramento.

#### C. Fórmula Consolidada por Bitola ($\text{mm}^2$) e Cor (UCC)
$$\text{Metragem Total}_{\text{bitola, cor}} = \left[ \sum_{k} (L_k \times N_{\text{fios}_k}) + (N_{\text{caixas}} \times 0,50\text{m}) + (N_{\text{QDC}} \times 1,00\text{m}) \right] \times (1 + \text{Taxa de Perda 5\%})$$

#### D. Tabela de Consolidação de Compras por Bitola e Cor (UCC - Rolos de 100m)
| Circuito | Função do Circuito | Seção ($\text{mm}^2$) | Tipo | Cor do Isolamento | Metragem Líquida (m) | + Perda 5% (m) | Compras UCC (Rolos de 100m) |
|---|---|---|---|---|---|---|---|
| **Circ. 01** | Iluminação | 1,5 mm² | Fase | Preto | 142,50 m | 149,63 m | 2 Rolos (200m) |
| **Circ. 01** | Iluminação | 1,5 mm² | Neutro | Azul Claro | 110,00 m | 115,50 m | 2 Rolos (200m) |
| **Circ. 01** | Iluminação | 1,5 mm² | Retorno | Amarelo | 68,00 m | 71,40 m | 1 Rolo (100m) |
| **Circ. 01** | Iluminação | 1,5 mm² | Terra | Verde | 142,50 m | 149,63 m | 2 Rolos (200m) |
| **Circ. 02** | Tomadas TUG | 2,5 mm² | Fase | Vermelho | 215,00 m | 225,75 m | 3 Rolos (300m) |
| **Circ. 02** | Tomadas TUG | 2,5 mm² | Neutro | Azul Claro | 215,00 m | 225,75 m | 3 Rolos (300m) |
| **Circ. 02** | Tomadas TUG | 2,5 mm² | Terra | Verde | 215,00 m | 225,75 m | 3 Rolos (300m) |
| **Circ. 03** | Chuveiro TUE | 6,0 mm² | Fase (2x) | Vermelho/Preto | 54,00 m | 56,70 m | 1 Rolo (100m) |
| **Circ. 03** | Chuveiro TUE | 6,0 mm² | Terra | Verde | 27,00 m | 28,35 m | Fracionado ou 1 Rolo |

### 2.3 Detalhamento Meticuloso de Pontos Elétricos (Caixas, Placas, Suportes, Módulos e Luminárias)
Toda caixa de ponto de elétrica deve ser decomposta individualmente nos seus componentes de compra:
- **Caixas de Embutir / Passagem:**
  - `Caixa 4x2" PVC Amarela / Termoplástica (unid):` Para pontos de tomadas e interruptores de parede.
  - `Caixa 4x4" PVC (unid):` Para conjuntos de 4 ou 6 módulos ou blocos de tomada reforçados.
  - `Caixa Octogonal 3x3" / 4x4" c/ Fundo Móvel para Teto (unid):` Para pontos de iluminação de laje/forro.
- **Placas, Suportes e Espelhos (Linha de Acabamento):**
  - `Suporte 4x2" / 4x4" c/ Parafusos (unid):` Estrutura de fixação dos módulos.
  - `Placa 4x2" Cega / 1 Posto / 2 Postos / 3 Postos (unid):` Espelho de acabamento frontal.
  - `Placa 4x4" 2 Postos / 4 Postos / 6 Postos (unid):` Espelho quadrado frontal.
- **Módulos de Tomadas e Interruptores:**
  - `Módulo de Tomada 2P+T 10A - 250V (unid):` Tomada NBR 14136 de uso geral (branca).
  - `Módulo de Tomada 2P+T 20A - 250V (unid):` Tomada de pino grosso para TUE (vermelha ou c/ identificação 20A).
  - `Módulo de Tomada USB (unid):` Módulo carregador USB Tipo A / Tipo C 5V.
  - `Módulo de Interruptor Simples 10A (unid).`
  - `Módulo de Interruptor Paralelo (Three-Way) 10A (unid):` Para comando de 2 pontos (escadas/corredores).
  - `Módulo de Interruptor Intermediário (Four-Way) 10A (unid):` Para comando de 3 ou mais pontos.
  - `Módulo Pulsador de Campainha / Minuteria (unid).`
- **Pontos de Iluminação e Luminárias:**
  - `Luminária Painel LED Plafon de Embutir / Sobrepor (unid):` Especificar formato e potência ($18\text{W}, 24\text{W}, 32\text{W}, 48\text{W}$ / $30\times30\text{cm}, 60\times60\text{cm}, 30\times120\text{cm}$).
  - `Spot LED Dicroica / PAR20 / Mini AR111 de Embutir (unid):` Spot direcionável c/ lâmpada/módulo LED.
  - `Fita de LED 12V / 24V c/ Fonte Driver (m / unid):` Fita LED flexível para sancas/marcenaria $+$ fonte driver dimerizável/convencional.

## 3. Modelo de Memória de Cálculo (Elétrica)
```text
╔══════════════════════════════════════════════════════════════════╗
║        MEMÓRIA DE CÁLCULO — INSTALAÇÕES ELÉTRICAS               ║
╠══════════════════════════════════════════════════════════════════╣
║  AMBIENTE: [T-101-SAL]   CIRCUITO: [Circuito 03 - Tomadas]      ║
╠══════════════════════════════════════════════════════════════════╣
║  ELETRODUTO (PVC Flexível 25mm - 3/4"):                         ║
║    Teto: X,XX m | Descidas (3x): X,XX m                         ║
║    Subtotal: X,XX m + Perda 10% = X,XX m                        ║
║                                                                  ║
║  CONDUTORES (Cabo Flex 2,5mm² - Fase/Neutro/Terra):             ║
║    Trecho embutido: X,XX m × 3 = XX,XX m                        ║
║    Pontas (4 caixas × 0,5m × 3 cabos): 6,00 m                   ║
║    Ponta QDC (1,0m × 3 cabos): 3,00 m                           ║
║    Subtotal: XX,XX m + Perda 5% = XX,XX m (Por Cor)             ║
║                                                                  ║
║  CAIXAS E MÓDULOS:                                               ║
║    Caixa 4x2 PVC: 4 unid                                         ║
║    Tomada Dupla 10A: 4 unid                                      ║
╚══════════════════════════════════════════════════════════════════╝
```

## 4. Tabela Final de Compra (UCC)
O relatório final deve arredondar para cima usando a UCC. Se a soma do projeto exigir 112 metros de cabo flexível azul 2,5mm², a SC (Solicitação de Compra) final será de **2 Rolos de 100m** (200m).

---

## 5. Caixas Enterradas de Infraestrutura Elétrica, Aterramento e Telecom (Concreto vs. Alvenaria)

> 🛑 **REGRA RÍGIDA DE SEPARAÇÃO FÍSICA:** É **PROIBIDO POR NORMA (NBR 5410 / NBR 8160)** passar tubulações hidráulicas e condutores elétricos dentro da mesma caixa ou vala. As redes elétricas e hidráulicas são **FISICAMENTE SEPARADAS E INDEPENDENTES**.
> 
> 🧮 **O QUE É COMPARTILHADO:** Apenas a **fórmula matemática (algoritmo de cálculo de cavas, alvenaria, concreto, lastro e tampas)** para derivação quantitativa no sistema.

### 5.1 Especificidades da Infraestrutura Elétrica Enterrada
| Tipo de Caixa Elétrica | Função Principal | Particularidade Construtiva |
|---|---|---|
| **Caixa de Passagem Elétrica** | Passagem de cabos alimentadores subterrâneos | Concreto ou Alvenaria c/ impermeabilização e tampa cega ("ELÉTRICA") |
| **Caixa de Haste de Aterramento** | Inspeção da malha de aterramento (SPDA) | Fundo em **Lastro de Brita Drenante** ($m³$) sem laje de concreto no fundo |
| **Caixa de Entrada Concessionária** | Ponto de entrega de energia (Média/Baixa Tensão) | Exige especificações da concessionária local e tampa reforçada FoFo |
| **Caixa de Telecom / Lógica** | Passagem de cabos de fibra óptica e telefonia | Separada obrigatoriamente das caixas de energia (evitar interferência) |

### 5.2 Algoritmo de Derivação Automática de Serviços (Concreto vs. Alvenaria)
As caixas de passagem elétrica utilizam a mesma memória de cálculo geométrica de [SKILL_QUANT_05_HIDRAULICA.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANT_05_HIDRAULICA.md#L98):
1. **Caixa de Concreto:** Paredes em concreto armado ($m³$) $+$ fôrmas dupla face ($m²$).
2. **Caixa de Alvenaria:** Paredes em tijolo maciço/bloco ($A_{\text{alvenaria}} = 2 \cdot (B + C) \cdot G$ em $m²$) sem fôrmas nas paredes verticais.
3. **Escavação e Talude NR-18 (quando $H > 1,25m$)**
4. **Apiloamento do Fundo e Lastro Magro / Brita Drenante**
5. **Revestimento Interno / Impermeabilização Interna ($m²$)**
6. **Reaterro Compactado vs. Bota-Fora**
7. **Tampas Estruturais (Concreto ou Ferro Fundido - FoFo c/ inscrição "ELÉTRICA" ou "TELECOM")**

---

## 6. Banco de Dutos e Envelopamento Elétrico Subterrâneo (NBR 5410 / NBR 14039)

> ⚠️ **REGRA DE BANCO DE DUTOS:** A tubulação elétrica enterrada em valas DEVE ser quantificada a partir do **Corte Geométrico do Banco de Dutos (Corte 1, Corte 2... Corte 6)**, derivando os eletrodutos, o volume de envelopamento de concreto (ou colchão de areia), fôrmas laterais, proteção mecânica e fita de advertência.

### 6.1 Métodos Construtivos de Infraestrutura de Dutos Subterrâneos

#### 🅰️ Método A: Envelopamento em Concreto (Banco de Dutos de Alta/Média Tensão e Tráfego Pesado)
Utilizado para vias de tráfego de veículos, travessias sob arruamento, pátios ou redes de alta capacidade (bancos com até 30 eletrodutos Ø3" / Ø4").

```text
1. Volume de Concreto de Envelopamento (m³):
   V_concreto_env = [ (Largura_Envelope × Altura_Envelope) − Σ (π × D_i² / 4) ] × Comprimento_Vala

2. Fôrmas Laterais do Envelope (m²):
   A_forma_env = 2 × Altura_Envelope × Comprimento_Vala

3. Escavação de Vala de Banco de Dutos (m³):
   V_escav_banco = (Largura_Envelope + 2 × 0,15m) × Profundidade_H × Comprimento_Vala

4. Eletrodutos e Espaçadores Plásticos (Pentes):
   - Extensão Total Eletrodutos (m): L_total_dutos = N_eletrodutos × Comprimento_Vala × (1 + 10% perda)
   - Espaçadores Plásticos Pentes (unid): N_pentes = (Comprimento_Vala / 1,50m) × N_fileiras
```

#### 🅱️ Método B: Leito de Areia com Proteção Mecânica (Valas de Baixa Tensão e Passeios)
Utilizado para alimentadores em áreas gramadas ou passeios com pouca carga superficial.

```text
1. Colchão e Envelopamento em Areia Lavada (m³):
   V_areia = Largura_Vala × (Espessura_Inferior_10cm + Altura_Dutos + Espessura_Superior_10cm) × Comprimento_Vala

2. Proteção Mecânica em Tijolos Maciços / Placas de Concreto (m²):
   A_proteção_mecânica = Largura_Vala × Comprimento_Vala

3. Fita Plástica de Advertência "PERIGO ALTA TENSÃO" (m):
   L_fita_aviso = Comprimento_Vala  (instalada a 30 cm abaixo do nível do terreno)

4. Reaterro Compactado e Bota-fora de Vala (m³):
   V_reaterro = V_escavado − (V_areia + V_proteção_mecânica + Volume_Dutos)
   V_bota_fora = V_escavado − V_reaterro
```

---

## 7. Sistema de Proteção contra Descargas Atmosféricas (SPDA & Aterramento - NBR 5419)

> ⚠️ **REGRA DE SPDA E ATERRAMENTO:** O levantamento de SPDA DEVE desmembrar os **3 subsistemas normativos**: Captação Aérea, Descidas de Prumada e Malha de Aterramento Enterrada com Hastes de Cobre e Solda Exotérmica.

### 7.1 Subsistema de Captação Aérea (Cobertura e Platibanda)
- **Método Gaiola de Faraday (Malha de Platibanda):**
  - `Fita de Alumínio / Cobre Plana (25×3mm) ou Cabo Cobre Nu 35mm²/50mm² (m):` $L_{\text{captação}} = \text{Perímetro Platibanda} + \text{Linhas Intermediárias} \times (1 + 10\%\text{ perda})$.
  - `Isoladores / Presilhas de Suporte (unid):` Espaçamento máximo de $1,00 \, m$ ao longo de toda a malha.
  - `Terminais Aéreos de Aterramento (unid):` Haste de captação em inox/latão $h=30\text{cm}$ a $50\text{cm}$ nos cantos da edificação.
- **Método Franklin (Pára-raios de Mastro):**
  - `Mastro de Aço Galvanizado a Fogo:` 2" $\times$ 6m com sapata de fixação, estais de aço inoxidável e sinalizador noturno de obstáculo.
  - `Captor Franklin 4 Pontas (unid):` Captor em latão cromado/cobre.

### 7.2 Subsistema de Descidas (Prumadas e Fachadas)
- **Descidas Aparentes (Cabo Cobre Nu 35mm² / 50mm² ou Fita de Alumínio):**
  - `Comprimento de Descida (m):` $L_{\text{descida}} = N_{\text{prumadas}} \times H_{\text{edificação}} \times (1 + 10\%)$.
  - `Presilhas de Fixação de Descida (unid):` Espaçadas a cada $1,00 \, m$ a $1,50 \, m$ na fachada.
  - `Proteção Mecânica de Base (unid):` Tubo de proteção em PVC rígido ou aço galvanizado $h=2,50 \, m$ na base de cada descida.
  - `Junta de Medição / Conector de Ensaio (unid):` Caixa de desconexão para teste de continuidade e resistência.
- **Descidas Estruturais (Rebar / Armadura dos Pilares):**
  - Conectores de pressão tipo C / Solda para amarração no aço estrutural antes da concretagem dos pilares.

### 7.3 Subsistema de Aterramento Enterrado (Anel Perimetral, Hastes & Solda Exotérmica)
- **Anel Perimetral de Aterramento Enterrado:**
  - `Cabo de Cobre Nu 50mm² / 70mm² Enterrado (m):` $L_{\text{anel}} = \text{Perímetro Externo do Edifício} \times (1 + 10\%)$ enterrado a $h=0,50 \, m$ no solo.
- **Hastes de Aterramento Cobreadas (Copperweld):**
  - `Hastes de Cobre Ø5/8" ou Ø3/4" × 2,40m / 3,00m (unid):` Cravadas verticalmente nos vértices do anel perimetral.
- **Solda Exotérmica e Conexões:**
  - `Cartuchos de Carga de Solda Exotérmica (unid):` Cargas nº 65, nº 90, nº 115 para fusão de conexões Tê, Cruzeta e Haste-Cabo.
  - `Alicate de Prensa + Moldes de Grafite (unid):` Moldes específicos por tipo de derivação.
- **Caixas de Inspeção de Aterramento:**
  - `Caixas de Inspeção de Solo (unid):` Caixas c/ tampa em ferro fundido ou concreto com **fundo em Lastro de Brita Drenante ($m³$)** para medição da resistência ($\le 10 \, \Omega$).
- **Barramentos de Equipotencialização (BEP / BEL):**
  - Barramento de cobre embutido em caixa metálica para interligação de todas as massas da obra.

---

## 8. Entrada de Energia, Padrão Concessionária, Subestação e Muro de Medidores (NBR 14039 / NBR 5410)

### 8.1 Padrão de Entrada e Poste da Concessionária
- `Poste Particular da Concessionária (unid):` Poste de concreto armado (Duplo T de 9m / 11m, classe 300daN a 1000daN) ou poste metálico galvanizado c/ cabeçote e roldanas.
- `Ramal de Entrada Subterrâneo / Aéreo em BT ou MT (m):` Cabos alimentadores de entrada de energia (Cobre ou Alumínio XLPE 0,6/1kV para Baixa Tensão ou 15kV/25kV para Média Tensão).
- `Chaves Seccionadoras e Fusíveis Matheus / Base C (unid):` Chaves fusíveis de proteção de MT no topo do poste.

### 8.2 Subestação Abrigada / Aérea e Transformador
- `Transformador de Potência (unid):` Transformador trifásico (a óleo mineral/vegetal ou a seco em resina epóxi) especificando a potência ($45\text{kVA}, 75\text{kVA}, 112.5\text{kVA}, 150\text{kVA}, 225\text{kVA}, 300\text{kVA}, 500\text{kVA}, 750\text{kVA}, 1000\text{kVA}$) e tensões ($13.8\text{kV} / 380-220\text{V}$ ou $220-127\text{V}$).
- `Para-raios de Média Tensão (unid):` Para-raios de polímero / óxido metálico para proteção do transformador.
- `Alvenaria e Portões da Subestação Abrigada (m² / unid):` Cubículo em alvenaria estrutural/concreto c/ portas de tela metálica galvanizada de proteção, canaletas para cabos c/ tampas pré-moldadas e iluminação blindada.
- `Malha de Aterramento de Subestação (m / unid):` Malha de alta confiabilidade em cabo de cobre nu $50\text{mm}^2 / 70\text{mm}^2$ c/ hastes cravadas $3/4" \times 2,40m$ e conexões exotérmicas ($\le 5 \, \Omega$).

### 8.3 Muro de Medidores e Centro de Medição (QTM / QDCA)
- `Muro de Medidores / Centro de Medição Agrupado (unid ou m²):` Muro em alvenaria revestida c/ nichos para caixas de medição da concessionária local (ex: Enel, CPFL, Light, Cemig, Copel).
- `Caixas de Medição Monofásica / Trifásica / Policarbonato (unid):` Caixas padronizadas tipo M, T, N, H c/ visores de policarbonato e fecho de padrão concessionária.
- `Barramento Blindado / Bus-way / Barramento de Cobre Nu (m ou kg):` Barramento de distribuição trifásica de alta amperagem c/ isoladores de epóxi.
- `Disjuntor Geral de Entrada em Caixa Moldada (unid):` Disjuntor termomagnético ajustável / fixo ($100A, 150A, 225A, 400A, 630A, 800A, 1000A$).

### 8.4 Quadros Elétricos Individuais por Unidade Habitacional vs. Quadros Gerais
- **Quadros Elétricos por Unidade Habitacional (QDC da Unidade — 1 unid por Apartamento/Casa/Loja):**
  - `Quadro de Distribuição de Embutir (QDC da Unidade):` Quadro termoplástico/metálico c/ porta branca/fumê (especificado pela capacidade: 12, 18, 24, 36 ou 48 disjuntores DIN) $+$ barramentos isolados de Fase, Neutro e Terra.
  - `Disjuntor Geral da Unidade (unid):` Disjuntor Bipolar ou Tripolar ($40A, 50A, 63A, 70A, 80A$).
  - `Dispositivos DR (Diferencial Residual) da Unidade (unid):` Interruptor DR Bipolar ou Tetrapolar 30mA (NBR 5410) para proteção contra choques elétricos em áreas molhadas.
  - `Dispositivos DPS (Surto Elétrico) da Unidade (unid):` DPS Classe II $20\text{kA} / 45\text{kA}$ para proteção dos equipamentos da unidade.
  - `Disjuntores Monopolares / Bipolares DIN (unid):` Disjuntores de $10A, 15A, 20A, 25A, 32A, 40A$ para iluminação, TUGs e TUEs (chuveiros, ar-condicionado, cooktop).
- **Quadros Gerais de Uso Comum e Serviços (Gerais da Obra):**
  - `QGVT / QG (Quadro Geral de Distribuição do Prédio):` Quadro autoportante ou de sobrepor metálico de grande capacidade.
  - `QDC-AC (Quadro de Áreas Comuns — 1 por Edifício/Bloco):` Distribuição de iluminação dos halls, garagens, portaria e bombas de recalque.
  - `QTA (Quadro de Transferência Automática Gerador/Rede - unid):` Chave comutadora motorizada intertravada c/ lógica de partida do Grupo Gerador.

---

## 9. Cabeamento Estruturado, Telefonia, Dados, Fibra Óptica, CFTV e Interfonia (ANSI/TIA/EIA-568)

### 9.1 Cabeamento Estruturado, Racks e Dados
- `Rack Telecom 19" de Parede ou Piso (unid):` Rack metálico c/ porta de acrílico/vidro (12U, 24U, 36U, 44U) especificando profundidade ($570mm / 800mm$).
- `Patch Panels 24 ou 48 Portas Cat6 / Cat6A (unid):` Painel de conexão c/ guias de cabos horizontais e organizadores.
- `Switches Gigabit Ethernet PoE (unid):` Switch de 24/48 portas 10/100/1000Mbps c/ portas PoE (Power over Ethernet) para alimentação de câmeras e pontos Wi-Fi AP.
- `Nobreak para Rack de Telecom (unid):` Nobreak senoidal de rack (1kVA, 2kVA, 3kVA) c/ banco de baterias seladas.
- `Cabo UTP Cat6 / Cat6A LSZH (m):` Cabo de pares trançados 4 pares $23\text{ AWG}$ homologado Anatel c/ capa retardante de chama/zero halogênio ($L = \text{Trajeto} \times 1,10 + \text{Pontas } 1,50m$).
- `Tomadas de Dados / Voz RJ45 Cat6 (unid):` Módulos Keystone RJ45 c/ espelho $4\times2"$.

### 9.2 Backbone de Fibra Óptica e Prumada de Telecom
- `Cabo de Fibra Óptica Monomodo / Multimodo OM3/OM4 (m):` Cabo dielétrico auto-sustentado (Tight Buffer ou Loose) para prumadas de shaft e conexão entre blocos.
- `Distribuidor Interno Óptico - DIO 24/48 Fibras (unid):` Caixa metálica de terminação óptica c/ extensões (pig-tails), acopladores LC/SC e bandejas de fusão.
- `Cordões Ópticos / Patch Cords (unid):` Cordões de manobra LC-LC / SC-LC.

### 9.3 Circuito Fechado de TV (CFTV IP) e Controle de Acesso
- `Câmeras IP Dome / Bullet Full HD / 4K (unid):` Câmeras de segurança c/ filtro IR night-vision, lente $2.8mm / 3.6mm$, carcaça IP66 antivandalismo (IK10).
- `Gravador NVR IP 16/32/64 Canais (unid):` Gravador digital IP c/ discos rígidos corporativos (HDs Surveillance 4TB / 8TB / 12TB).
- `Monitores Industriais de Guarita (unid):` Monitores LED 24"/32" para vídeo-wall da portaria.

### 9.4 Interfonia Predial e Vídeo Porteiro IP
- `Central de Interfonia Predial IP / PABX Digital (unid):` Central de comunicação IP c/ placas de ramais para todas as unidades.
- `Porteiro Eletrônico Exterior c/ Câmera / Leitor Facial (unid):` Terminal de acesso de rua c/ câmera HD, teclado e leitor de Tag.
- `Terminais de Interfone de Apartamento (unid):` Aparelho de interfone de parede c/ segredo / moradia (1 por unidade habitacional).
