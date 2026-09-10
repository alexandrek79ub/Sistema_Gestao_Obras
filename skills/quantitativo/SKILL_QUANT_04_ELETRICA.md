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
- **Descidas e Subidas Verticais (ΔZ):** Calculadas obrigatoriamente pela diferença de cota entre o plano de caminhamento (forro/laje ou contrapiso) e a cota de instalação do ponto/caixa:
  - `Tomada Baixa (h = 0,30m do piso):` Descida do teto = `H_pé-direito - 0,30m`.
  - `Tomada Média / Interruptor (h = 1,10m do piso):` Descida do teto = `H_pé-direito - 1,10m`.
  - `Tomada Alta (Chuveiro / Ar-condicionado / Exaustor h = 2,10m a 2,20m):` Descida do teto = `H_pé-direito - 2,10m`.
  - `Prumadas de Shaft / Subestação:` Comprimento vertical da prumada entre pavimentos multiplicada pelo número de andares + travessia de lajes.
- **Taxa de Perda:** Adicionar **10%** sobre o comprimento total calculado.
- **Regra UCC:** Comprar eletrodutos flexíveis sempre em múltiplos de **50 metros** (Rolo padrão). Tubos rígidos em múltiplos de **3 metros**.

### 2.2 Fios e Cabos — Método de Quantificação por Circuito (Fase, Neutro, Terra e Retorno)
A metragem de condutores **NÃO é uma simples multiplicação do comprimento do eletroduto pelo número total de fios**. O levantamento DEVE ser feito **trecho a trecho, circuito por circuito**, multiplicando a extensão real do eletroduto (horizontal + descidas verticais) pela quantidade de condutores de cada função presentes naquele trecho (indicados pela simbologia unifilar: Fase `|`, Neutro `┬`, Terra `┴`, Retorno `/`).

#### A. Algoritmo de Cálculo por Trecho de Eletroduto
Para cada trecho de eletroduto `k` percorrido pelo circuito `c`:
1. **Comprimento do Trecho (Lk):** `Lk = L_horizontal(X,Y) + ΔZ_descida/subida`.
2. **Cálculo da Metragem por Tipo de Condutor (Função e Cor NBR 5410):**
   - **Fase (Preto / Vermelho / Castanho):** `L_fase = Soma(Lk × N_condutores_fase_k)`.
   - **Neutro (Azul Claro — Cor Obrigatória NBR 5410):** `L_neutro = Soma(Lk × N_condutores_neutro_k)`.
   - **Proteção / Terra (Verde ou Verde-Amarelo — Cor Obrigatória NBR 5410):** `L_terra = Soma(Lk × N_condutores_terra_k)`.
   - **Retorno (Amarelo / Branco):** `L_retorno = Soma(Lk × N_condutores_retorno_k)` (trechos entre interruptores e lâmpadas / Three-way / Four-way).

#### B. Sobras de Pontas (Folga Técnica Obrigatória)
Para cada caixa de passagem, tomada, interruptor ou luminária acessada pelo circuito, e no Quadro de Distribuição (QDC), adicionar as sobras para desencapamento e conexão:
- `Caixas de Tomada / Interruptor / Passagem / Luminária:` Adicionar **+0,50 m** por condutor para CADA caixa acessada pelo circuito.
- `Quadro de Distribuição (QDC):` Adicionar **+1,00 m** por condutor dentro do QDC para penteamento e fixação no disjuntor/barramento.

#### C. Fórmula Consolidada por Bitola (mm²) e Cor (UCC)
```
Metragem Total = [ Soma(Lk × Nfios_k) + (Ncaixas × 0,50m) + (NQDC × 1,00m) ] × (1 + 0,05)
```

#### D. Exemplo Didático Ilustrativo de Consolidação de Compras por Bitola e Cor (UCC - Rolos de 100m)

> [!CAUTION]
> **AVISO CRÍTICO DE INTEGRIDADE E ANTI-CONTAMINAÇÃO (NÃO COPIAR OU REUTILIZAR ESTES DADOS):**
> A tabela abaixo é **100% FICTÍCIA E MERAMENTE ILUSTRATIVA**, tendo como único objetivo exemplificar a formatação visual e a aplicação da regra de arredondamento comercial para rolos de 100 metros.
> **É EXPRESSAMENTE PROIBIDO** utilizar, copiar, estimar ou assumir quaisquer números ou circuitos desta tabela em levantamentos reais. Cada obra DEVE extrair seus próprios circuitos, trajetos e bitolas exclusivamente a partir dos seus próprios desenhos e diagramas unifilares executivos.

| Circuito (Exemplo Fictício) | Função Ilustrativa | Seção ($\text{mm}^2$) | Tipo | Cor do Isolamento | Metragem Líquida (m) | + Perda 5% (m) | Compras UCC (Rolos de 100m) |
|---|---|---|---|---|---|---|---|
| **Circ. Exemplo A** | Iluminação (Exemplo) | 1,5 mm² | Fase | Preto | 142,50 m | 149,63 m | 2 Rolos (200m) |
| **Circ. Exemplo A** | Iluminação (Exemplo) | 1,5 mm² | Neutro | Azul Claro | 110,00 m | 115,50 m | 2 Rolos (200m) |
| **Circ. Exemplo A** | Iluminação (Exemplo) | 1,5 mm² | Retorno | Amarelo | 68,00 m | 71,40 m | 1 Rolo (100m) |
| **Circ. Exemplo A** | Iluminação (Exemplo) | 1,5 mm² | Terra | Verde | 142,50 m | 149,63 m | 2 Rolos (200m) |
| **Circ. Exemplo B** | Tomadas TUG (Exemplo) | 2,5 mm² | Fase | Vermelho | 215,00 m | 225,75 m | 3 Rolos (300m) |
| **Circ. Exemplo B** | Tomadas TUG (Exemplo) | 2,5 mm² | Neutro | Azul Claro | 215,00 m | 225,75 m | 3 Rolos (300m) |
| **Circ. Exemplo B** | Tomadas TUG (Exemplo) | 2,5 mm² | Terra | Verde | 215,00 m | 225,75 m | 3 Rolos (300m) |
| **Circ. Exemplo C** | Carga Especial (Exemplo) | 6,0 mm² | Fase (2x) | Vermelho/Preto | 54,00 m | 56,70 m | 1 Rolo (100m) |
| **Circ. Exemplo C** | Carga Especial (Exemplo) | 6,0 mm² | Terra | Verde | 27,00 m | 28,35 m | Fracionado ou 1 Rolo |

### 2.3 Detalhamento Meticuloso de Pontos Elétricos (Caixas, Placas, Suportes, Módulos e Luminárias)
Toda caixa de ponto de elétrica deve ser decomposta individualmente nos seus componentes de compra:
- **Caixas de Embutir / Passagem:**
  - `Caixa 4x2" PVC Amarela / Termoplástica (unid):` Para pontos de tomadas e interruptores de parede.
  - `Caixa 4x4" PVC (unid):` Para conjuntos de 4 ou 6 módulos, blocos reforçados ou caixas de passagem e derivação de troncos em alvenaria.
  - `Caixa Octogonal 3x3" / 4x4" c/ Fundo Móvel para Teto (unid):` **REGRA OBRIGATÓRIA (100% dos Pontos de Iluminação):** Toda e qualquer luminária de teto (painéis LED 60x60, sobrepor, plafons, luminárias herméticas industriais ou blocos autônomos de emergência) exige **obrigatoriamente 1 caixa octogonal de teto** para interligação mecânica dos eletrodutos e abrigo seguro dos drivers e conexões. Quantidade total: $N_{\text{caixas teto}} = \sum (\text{Luminárias de teto}) \times 1,05$.
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
  - `Luminária Painel LED Plafon de Embutir / Sobrepor (unid):` Especificar formato e potência ($18\text{W}, 24\text{W}, 32\text{W}, 40\text{W}, 48\text{W}$ / $30\times30\text{cm}, 60\times60\text{cm}, 30\times120\text{cm}$).
  - `Luminária Hermética Industrial LED IP65 (unid):` Para áreas técnicas, depósitos e garagens ($2\times18\text{W}$ ou $2\times9\text{W}$).
  - `Bloco de Iluminação de Emergência LED Autônomo c/ Bateria (unid):` Para rotas de fuga e saídas de emergência (Circuito LE).
  - `Spot LED Dicroica / PAR20 / Mini AR111 de Embutir (unid):` Spot direcionável c/ lâmpada/módulo LED.
  - `Fita de LED 12V / 24V c/ Fonte Driver (m / unid):` Fita LED flexível para sancas/marcenaria $+$ fonte driver dimerizável/convencional.

---

### 2.4 Algoritmo Matemático de Derivação Automática de Miudezas e Conexões (Kits de Montagem)
Para eliminar omissões e esquecimentos no orçamento de compras, as miudezas de fixação e conexão **DEVEM ser calculadas automaticamente por derivação matemática direta** dos elementos principais:

1. **Luvas de Emenda para Eletroduto Rígido PVC (unid):**  
   Os eletrodutos rígidos são fornecidos em varas de 3 metros. Cada vara requer 1 luva de união:
   $$N_{\text{luvas}} = \lceil L_{\text{eletroduto}} / 3,00\text{m} \rceil \times 1,05$$
2. **Adaptadores Box Reto em PVC para Caixas e Quadros (unid):**  
   Cada caixa de parede/teto e cada chegada no quadro de distribuição exige adaptadores com rosca e porca para travamento mecânico:
   $$N_{\text{adaptadores box}} = [ 2 \times (N_{\text{caixas 4x2}} + N_{\text{caixas 4x4}} + N_{\text{caixas octogonais}}) + N_{\text{circuitos QDC}} ] \times 1,05$$
3. **Abraçadeiras Tipo D em Aço Galvanizado c/ Cunha e Parafusos/Buchas S6 (unid):**  
   Para tubulações aparentes em teto, laje, entreforro ou perfilados, a fixação deve ocorrer no máximo a cada $1,50\text{ m}$:
   $$N_{\text{abraçadeiras}} = \lceil L_{\text{eletroduto aparente/forro}} / 1,50\text{m} \rceil \times 1,05$$
4. **Conectores de Emenda Rápida por Alavanca (tipo Wago / Derivação - unid):**  
   Nas caixas de passagem e derivação de múltiplos circuitos:
   $$N_{\text{conectores rápidos}} = 3 \times N_{\text{caixas de passagem e derivação}} + 2 \times N_{\text{luminárias de teto}}$$
5. **Terminais Pré-Isolados Tipo Ilhós (Cobre Estanhado - unid):**  
   Para terminação de condutores de 2,5mm² e 4,0mm² nos bornes de disjuntores e módulos de tomadas:
   $$N_{\text{terminais ilhós}} = (2 \times N_{\text{polos de disjuntores}}) + (3 \times N_{\text{módulos de tomada}})$$
6. **Fita Isolante Antichama 19mm x 20m (rolos):**  
   $$N_{\text{rolos fita}} = \lceil (N_{\text{pontos elétricos total}}) / 50 \rceil \text{ rolos (mínimo 2 rolos por obra)}$$
7. **Parafusos Chipboard e Buchas de Nylon S6 / S8 (unid):**  
   Fixação de todas as caixas de embutir (4×2, 4×4, octogonais), quadros de distribuição e suportes de luminárias:
   $$N_{\text{buchas}} = [ 2 \times (N_{\text{caixas 4x2}} + N_{\text{caixas 4x4}} + N_{\text{caixas octogonais}} + N_{\text{luminárias}}) + 4 \times N_{\text{quadros QDC}} ] \times 1,05$$
8. **Talco Industrial / Vaselina Líquida Neutra para Puxamento de Cabos:**  
   Facilitador de deslizamento para alimentação de circuitos pesados e longos sem danificar a isolação:
   $$N_{\text{frascos 500mL}} = \lceil L_{\text{cabos } \ge 6\text{mm}^2} / 200\text{m} \rceil$$
9. **Guia de Tração (Passa-fio de Nylon/Aço Maleável com Ponteira Metálica):**  
   1 unidade por equipe de eletricistas (insumo/ferramental de canteiro, registrado na logística de obra).
10. **Fita de Autofusão 19mm × 10m (Isolação de Alta Confiabilidade / Áreas Úmidas):**  
    Para impermeabilização e recomposição de isolação em caixas de passagem enterradas, poços e áreas molhadas:
    $$N_{\text{rolos autofusão}} = \max(2; \, \lceil N_{\text{emendas subterrâneas}} / 5 \rceil)$$
11. **Prensa-cabos Termoplásticos / Latão Rosca PG/Métrico IP68 (unid):**  
    Vedação estanque em cada entrada e saída de eletrodutos em caixas externas e quadros de força:
    $$N_{\text{prensa-cabos}} = N_{\text{chegadas de eletroduto nos quadros e caixas externas}}$$
12. **Tirantes Roscados 1/4" × 1m c/ Porcas, Arruelas e Chumbadores (unid):**  
    Sustentação suspensa de perfilados perfurados e eletrocalhas metálicas sob lajes:
    $$N_{\text{tirantes}} = \lceil L_{\text{eletrocalha / perfilado}} / 1,20\text{m} \rceil \times 1,05$$
13. **Anilhas Plásticas Marcadoras Numeradas / Marcadores de Circuitos:**  
    Identificação padronizada de condutores nos barramentos e disjuntores: 1 jogo completo por QDC instalado.
14. **Fita Plástica de Advertência Enterrada "PERIGO: REDE ELÉTRICA":**  
    Sinalização preventiva instalada 30cm acima do banco de dutos ou cabos diretamente enterrados:
    $$L_{\text{fita}} = L_{\text{valas de dutos subterrâneos}} \times 1,10\text{ m}$$

### 🛡️ 2.5 Checklist Anti-Omissão de SKUs de Instalações Elétricas (15 SKUs Obrigatórios na UCC/BOM)

> Antes de fechar o quantitativo e a requisição de compras de instalações elétricas, o PMO Virtual DEVE auditar e confirmar a presença de todos os 15 SKUs na BOM:

- [ ] **Luvas de Emenda para Eletroduto Rígido PVC:** 1 luva por vara de 3m ($\lceil L_{\text{eletroduto}} / 3\text{m} \rceil \times 1,05$).
- [ ] **Adaptadores Box Reto PVC c/ Rosca e Porca:** 2 por caixa 4×2/4×4/octogonal + chegadas de circuitos no QDC.
- [ ] **Abraçadeiras Tipo D c/ Cunha e Buchas S6:** 1 a cada 1,50m de eletroduto aparente ou em entreforro.
- [ ] **Conectores Rápidos por Alavanca (Wago ou similar):** 3 por caixa de passagem/derivação + 2 por ponto de iluminação.
- [ ] **Terminais Pré-Isolados Tipo Ilhós:** $(2 \times \text{polos de disjuntores}) + (3 \times \text{módulos de tomada})$.
- [ ] **Fita Isolante Antichama 19mm × 20m:** 1 rolo a cada 50 pontos elétricos (mínimo 2 rolos por obra).
- [ ] **Parafusos Chipboard + Buchas S6/S8:** 2 por caixa embutida / suporte de luminária.
- [ ] **Talco / Vaselina Líquida para Puxamento:** 1 frasco de 500mL a cada 200m de cabos de bitola $\ge 6\text{ mm}^2$.
- [ ] **Fita de Autofusão 19mm × 10m:** Mínimo 2 rolos por obra; 1 rolo extra a cada 5 emendas em caixas subterrâneas.
- [ ] **Prensa-cabos Termoplásticos IP68:** 1 por chegada de eletroduto nos quadros QDC/QG e caixas externas.
- [ ] **Tirantes Roscados 1/4" + Porcas + Arruelas:** 1 conjunto a cada 1,20m de eletrocalha ou perfilado suspenso.
- [ ] **Anilhas Numeradas / Marcadores de Identificação:** 1 estojo/jogo completo por QDC instalado.
- [ ] **Espaçadores Plásticos Pente para Banco de Dutos:** 1 pente a cada 1,50m de vala por camada de tubos.
- [ ] **Fita Plástica de Advertência Enterrada "REDE ELÉTRICA":** Metragem linear igual ao comprimento total de valas subterrâneas $+ 10\%$.
- [ ] **Cartuchos de Solda Exotérmica e Moldes de Grafite (SPDA):** 1 cartucho por conexão de cabo de cobre na malha/hastes.

---

## 📋 3. Tabela Oficial de Serviços para EAP e Cronograma de Elétrica (Nível 3.1 — 5 Fases Civis)

> 🛑 **REGRA DE SEGREGAÇÃO:** Esta tabela contém **exclusivamente pacotes de trabalho e serviços executivos de engenharia**. Os consumíveis (luvas, adaptadores box, conectores rápidos, fitas, terminais, talco) NÃO recebem código EAP e pertencem à lista UCC/BOM derivada (§2.4 e §2.5).

| Código EAP | Pacote de Trabalho | Unid. Avanço Físico | Predecessora Civil | Observação Executiva |
|:---:|:---|:---:|:---:|:---|
| **3.1.1** | Eletrodutos em Lajes (embutidos antes da concretagem) | m | 1.4.7 — Fôrma Lateral de Laje | Imediatamente antes de 1.4.8 Concretagem |
| **3.1.2** | Rasgos em Paredes de Alvenaria para Eletrodutos | m | 2.1.1 — Alvenaria concluída | Após cura da argamassa de assentamento |
| **3.1.3** | Instalação de Caixas 4×2, 4×4 e Octogonais em Parede | un | 3.1.2 | Antes do chapisco/emboço das paredes |
| **3.1.4** | Passagem de Eletrodutos em Paredes e Chumbamento | m | 3.1.3 | Antes do chapisco — predecessora de 2.1.2 |
| **3.1.5** | Bancos de Dutos e Envelopamento Subterrâneo | m | 1.2 — Terraplenagem | Executar preferencialmente junto com a fundação |
| **3.1.6** | Caixas de Passagem Elétrica Enterradas (Concreto/Alvenaria) | un | 3.1.5 | Derivar escavação, lastro, alvenaria e tampa |
| **3.1.7** | Prumadas em Shafts e Instalação de Eletrocalhas | m / m² | 1.4.12 — Desforma total de lajes | Após lajes liberadas para carga |
| **3.1.8** | Enfiação de Cabos Alimentadores ($\ge 16\text{ mm}^2$) | m | 3.1.5 + 3.1.7 | Lances contínuos sem emendas (NBR 5410) |
| **3.1.9** | Enfiação de Circuitos Terminais (Fase, Neutro, Terra, Retorno) | m | 2.1.8 — Pintura (1ª demão) | Evita danos e manchas na fiação |
| **3.1.10** | Montagem e Conexão de Quadros (QDC, QG, QGVT) | un | 3.1.8 | Após alimentadores enfiados |
| **3.1.11** | Instalação de Suportes, Módulos de Tomadas e Interruptores | un | 3.1.9 + 2.1.9 — Esquadrias | Após pintura final e portas montadas |
| **3.1.12** | Instalação de Luminárias, Painéis LED e Refletores | un | 3.1.11 | Após conclusão dos forros e pintura de teto |
| **3.1.13** | Malha de Aterramento, SPDA e Hastes Copperweld | m / un | 1.3.4 — Escavação | Antes do reaterro de fundação / valas |
| **3.1.14** | Testes de Isolamento, Continuidade e Energização Final | un | 3.1.10 + 3.1.12 + 3.1.13 | Marco de comissionamento elétrico |

---

## 4. Modelo de Memória de Cálculo Analítica por Circuito (Elétrica)
O levantamento elétrico DEVE ser estruturado em **Tabela Analítica Circuito a Circuito**, identificando:
- Identificação do Circuito (ex: ALIM, L1-L4, T1-T13, AC1-AC5)
- Destinação e Tensão / Amperagem do Disjuntor
- Trecho Horizontal Medido em Planta (m)
- Subidas e Descidas Verticais Eixo Z detalhadas (m)
- Comprimento Total de Eletroduto (m)
- Condutores discriminados individualmente por função: **Fase**, **Neutro**, **Retorno** e **Terra** (m)

---

## 5. Tabela Oficial de Compras: Padronização das Unidades Comerciais (UCC)

> 🛑 **REGRA RÍGIDA DE SEPARAÇÃO DE UCC PARA CONDUTORES E TUBULAÇÕES:**  
> A unidade comercial de faturamento varia estritamente conforme o tipo de insumo e seu método de instalação:

1. **Cabos de Potência / Alimentadores Pesados ($\ge 16\text{ mm}^2$, EPR 0,6/1kV):**  
   * **Unidade Comercial:** **METRO LINEAR (`m`)**.  
   * **Critério Técnico:** O fornecedor industrial corta e fatura a metragem exata fracionada de grandes bobinas. **A NBR 5410 proíbe emendas intermediárias em alimentadores subterrâneos**.  
   * É estritamente **proibido arredondar para rolos fechados de 100m**, pois isso geraria lances picados inutilizáveis ou sobras caras de cobre de grande seção.
2. **Condutores Prediais Flexíveis 750V ($\le 10\text{ mm}^2$ - 1,5mm², 2,5mm², 4,0mm², 6,0mm²):**  
   * **Unidade Comercial:** **ROLOS LACRADOS DE 100 METROS (`rolos`)**.  
   * **Critério Técnico:** A indústria não vende metragem fracionada avulsa para circuitos prediais. Toda solicitação de compra DEVE ser arredondada para cima pela função teto:
     $$\text{Qtd. UCC (rolos)} = \lceil L_{\text{líquido}} \times (1 + \text{perda}) / 100 \rceil$$
3. **Eletrodutos Rígidos de PVC:**  
   * **Unidade Comercial:** **VARAS DE 3 METROS (`varas`)**. Arredondamento: $\lceil L_{\text{líquido}} \times (1 + \text{perda}) / 3 \rceil$.
4. **Formatação da Tabela de Compras (Sem Ambiguidade):**  
   A tabela de compras DEVE conter **obrigatoriamente duas colunas de unidade separadas**:
   * `Unid. Proj.` (unidade da medição física líquida em metros ou unidades)
   * `Qtd. UCC` (quantidade numérica da embalagem de fornecimento)
   * `Unid. UCC` (unidade da embalagem comercial: `m`, `rolos`, `varas`, `un`, `cj`)
   * `Embalagem de Fornecimento / Detalhe` (ex: "Metro linear sob medida", "Rolo lacrado de 100m", "Vara rígida de 3m")

---

## 6. Caixas Enterradas de Infraestrutura Elétrica, Aterramento e Telecom (Concreto vs. Alvenaria)

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

## 7. Banco de Dutos e Envelopamento Elétrico Subterrâneo (NBR 5410 / NBR 14039)

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

## 8. Sistema de Proteção contra Descargas Atmosféricas (SPDA & Aterramento - NBR 5419)

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

### 7.4 Tabela de Compra e Embalagem Comercial de SPDA (UCC)
| Insumo SPDA | Unidade Medida | Critério de Quantificação | Unidade UCC | Embalagem de Compra |
|---|---|---|---|---|
| **Cordoalha Cobre Nu 50mm²** | m | Captação + Descidas + 5% perda | rolos | Rolos lacrados com 100m ($\lceil L / 100 \rceil$) |
| **Presilhas / Suportes Guia Platibanda** | unid | 1 un a cada 1,00m de perímetro platibanda | un | Peça em bronze/inox c/ parafuso e bucha |
| **Hastes de Aterramento Copperweld 3/4" x 3,00m** | unid / barra | 1 haste por prumada de descida de SPDA (camada 254µm) | barras | Barra de 3,00m |
| **Conectores Grampo Cabo-Haste em Latão 3/4"** | unid | 1 conector por haste instalada | un | Peça em bronze/latão reforçado |
| **Caixas de Inspeção de Solo PVC Ø300mm** | unid / cj | 1 conjunto por haste instalada | cj | Conjunto cilíndrico PVC c/ tampa reforçada |

---

## 9. Entrada de Energia, Padrão Concessionária, Subestação e Muro de Medidores (NBR 14039 / NBR 5410)

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

## 10. Cabeamento Estruturado, Telefonia, Dados, Fibra Óptica, CFTV e Interfonia (ANSI/TIA/EIA-568)

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

---

## 11. Diretriz Rígida de Governança Técnica: Proibição de Estimativas Fictícias e Bloqueio Formal

> 🛑 **REGRA DE OURO CONTRA RETRABALHO E CHUTES PARAMÉTRICOS:**  
> 1. O Agente **NUNCA DEVE INVENTAR QUANTITATIVOS OU EXECUTAR ESTIMATIVAS PARAMÉTRICAS POR MÉDIA** caso a disciplina não possua prancha executiva aprovada e entregue no acervo técnico da obra.
> 2. Se uma disciplina não foi desenhada (ex: tubulações hidrossanitárias sem prancha isométrica, ou linhas frigoríficas de climatização sem projeto executivo de HVAC), o Agente **DEVE REGISTRAR OS ITENS FORMALMENTE COMO BLOQUEADOS / PENDÊNCIA TÉCNICA DA PROJETISTA (RFI)**.
> 3. Essa diretriz blinda o orçamento, impede distorções em compras, elimina revisões desnecessárias e garante que cada linha da memória de cálculo seja 100% auditável por prancha e escala.

