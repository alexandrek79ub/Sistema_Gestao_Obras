# 🏠 SKILL MÓDULO 03: Arquitetura & Acabamentos

> **Dependência:** Carregar sempre com [SKILL_QUANTIFICACAO_MASTER.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANTIFICACAO_MASTER.md)
> **Normas:** NBR 12721 (Critérios de medição), TCPO 14ª Edição

> 🛡️ **BLINDAGEM CONTRA QUANTITATIVOS ESTIMADOS (REGRA DE OURO INVIOLÁVEL):**  
> - **PROIBIÇÃO TOTAL DE ESTIMATIVAS:** Todo levantamento quantitativo de arquitetura DEVE ser 100% embasado em cotas, níveis, especificações e detalhes geométricos extraídos diretamente das pranchas do projeto executivo. É **TERMINANTEMENTE PROIBIDO** estimar, supor, adotar médias genéricas ou inferir qualquer dimensão que não esteja comprovada em desenho.  
> - **DEVER OBRIGATÓRIO NA FALTA DE INFORMAÇÃO NO DESENHO:** Se uma informação necessária (cota, espessura, pé-direito, especificação de acabamento, detalhe de pingadeira, soleira, etc.) **NÃO CONSTAR NO DESENHO**, é **DEVER ABSOLUTO E INEGOCIÁVEL** do orçamentista:  
>   1. **NÃO LEVANTAR O ITEM** com base em números inventados, suposições ou estimativas.  
>   2. **INSERIR OBRIGATORIAMENTE UMA OBSERVAÇÃO EXPLÍCITA NA MEMÓRIA DE CÁLCULO E NA PLANILHA:**  
>      `⚠️ [ITEM NÃO LEVANTADO POR FALTA DE INFORMAÇÃO NO DESENHO - Prancha: [Código] / Ambiente: [Nome/CIA] / Elemento: [Descrição] - Necessária emissão de RFI para definição de cota/especificação].`  
>   3. **REGISTRAR NO CSV/ORÇAMENTO COM QUANTIDADE ZERO OU PENDENTE**, acompanhado da ressalva técnica.  
>   4. **EMITIR PENDÊNCIA TÉCNICA (RFI)** formal para cobrança junto aos projetistas ou ao cliente.  
> - **TOLERÂNCIA ZERO NA AUDITORIA:** A inserção de qualquer quantitativo "estimado" sem respaldo direto no desenho acarreta a **REPROVAÇÃO SUMÁRIA** do levantamento pela auditoria de qualidade.

---

## 🧭 Escopo deste Módulo

Cobre o quantitativo de **toda a arquitetura e acabamentos** de uma edificação:

- Alvenaria de vedação (blocos cerâmicos e de concreto)
- Revestimentos de parede (chapisco, emboço, reboco, gesso, cerâmica)
- Revestimentos de teto (gesso, forro PVC, drywall, pintura)
- Pisos e contrapisos
- Cobertura (telhado)
- Impermeabilização
- Esquadrias (portas e janelas)
- Rodapés, peitoris e soleiras
- Drywall (paredes e forros)
- Pinturas (interna e externa)
- Textura / Grafiato (fachada)

---

## 📐 1. Alvenaria e Revestimentos de Parede

> ⚠️ Revestimento de PAREDE e TETO são serviços separados. Parede = área vertical. Teto = área horizontal (§3). Nunca somar na mesma memória.

### 1.1 Fórmulas

**Ambiente retangular — Alvenaria de Vedação / Estrutural (4 paredes):**
```
P_perímetro_externo = 2 × Comp_ext + 2 × (Larg_ext − 2 × e_parede)
P_alvenaria_líquido = P_perímetro_externo − Σ (Largura_pilares_concreto) + Σ (Paredes_divisórias_internas)
A_bruta = P_alvenaria_líquido × H_pé-direito
A_líquida = A_bruta − Σ Descontos de Vãos (NBR 12721 Art. 3)
A_final = A_líquida × (1 + Taxa de Perda)
```
> ⚠️ **Regras Obrigatórias de Alvenaria (Anti-Duplicidade e Geometria Líquida):**
> 1. **Desconto de Pilares de Concreto:** Em estruturas convencionais com pilares de concreto in loco embutidos na alvenaria, a largura de CADA pilar (`b_pilar`) DEVE ser subtraída do perímetro de alvenaria, pois não há tijolos/blocos onde existe concreto.
> 2. **Desconto de Interseções nos Cantos em "L" (Perímetro Externo):** No contorno perimetral, para evitar sobreposição nos 4 cantos, mede-se um dos sentidos de ponta a ponta na face externa e desconta-se a espessura das duas paredes (`2 × e_parede`) no outro sentido: `P_ext_líquido = 2 × Comp_ext + 2 × (Larg_ext − 2 × e_parede)`.
> 3. **Desconto de Interseções em "T" e "X" (Divisórias Internas):** Todas as paredes internas DEVEM ser medidas estritamente pelo **vão livre entre faces** (face interna a face interna de alvenaria ou pilares). A espessura da parede contínua interceptada (`e_parede = 0,14m`) DEVE ser integralmente descontada em cada nó de junção, sendo terminantemente proibido somar extensões de eixo a eixo ou por faces externas sem deduzir os nós.
> 4. **Critério para Revestimentos e Pinturas:** Como os revestimentos de argamassa e pintura cobrem apenas as faces aparentes dos cômodos, as áreas internas dos nós de interseção e amarrações entre blocos NUNCA devem receber dupla camada de revestimento.

**Pintura Externa da Fachada (Perímetro Bruto da Fachada):**
```
P_fachada_ext = 2 × (Comp_ext + Larg_ext)
A_bruta_fachada = P_fachada_ext × H_fachada
A_líquida_pintura_ext = A_bruta_fachada − Σ Descontos de Vãos de Esquadrias Externas
```
> ⚠️ **Regra de Pintura Externa:** A pintura externa reveste a face EXTERNA da edificação de ponta a ponta. Portanto, usa-se o **perímetro bruto externo da fachada** `2 × (Comp_ext + Larg_ext)` sem descontar espessuras de paredes ou cantos internos.

**Emboço e Chapisco de Paredes Internas sob Forro Rebaixado:**
```
H_emboço_parede = H_forro + 0,10 m (transpasse mínimo de 10 cm acima da linha do forro)
A_bruta_emboço = P_interno × H_emboço_parede
A_líquida_emboço = A_bruta_emboço − Σ Descontos de Vãos Internos
```
> ⚠️ **Regra de Emboço sob Forro Rebaixado:** O chapisco e emboço de parede DEVEM ser calculados com acréscimo de **10 cm a 15 cm acima da cota do forro** (`H_forro + 0,10m`) para que o gesseiro fixe a tabica perimétrica sobre superfície lisa e regularizada.

**Pintura de Paredes Internas sob Forro Rebaixado:**
```
H_pintura_parede = H_forro (altura livre visível do piso até a tabica/forro)
A_bruta_pintura_int = P_interno × H_pintura_parede
A_líquida_pintura_int = A_bruta_pintura_int − Σ Descontos de Vãos Internos
```
> ⚠️ **Regra de Pintura sob Forro Rebaixado:** A pintura é executada APÓS o forro já estar instalado. Portanto, a altura de pintura de parede é exatamente a altura visível do piso ao forro (`H_forro`), sem pintar a área oculta acima do gesso.

**Complemento de Alvenaria e Revestimento de Platibanda (Cobertura):**
```
H_alvenaria_platibanda = H_platibanda_total − h_viga_invertida
A_alvenaria_platibanda = P_líquido_platibanda × H_alvenaria_platibanda
A_pintura_ext_platibanda = P_fachada_ext × H_platibanda_total
A_emboço_int_platibanda = P_líquido_platibanda × H_platibanda_total
```
> ⚠️ **Regra de Platibanda sobre Viga Invertida:** Quando a cobertura possuir viga invertida (ex: 52 cm de altura) e platibanda mais alta (ex: 91 cm), o complemento de alvenaria sobre a viga DEVE ser quantificado separadamente (`H_alv = 0,91m - 0,52m = 0,39m` ou 2 fiadas de bloco). Os revestimentos/pinturas de ambas as faces da platibanda cobrem a altura total (`H = 0,91m`).

**Muretas Escalonadas de Apoio de Telhado e Terças Metálicas:**
```
L_total_perfis_terça = Num_linhas_apoio × Comprimento_vão
A_alvenaria_apoio = Σ (Comprimento_vão × H_mureta_i)  (Blocos 9x19x39 cm)
Revestimento_muretas_apoio = 0,00 m² (Sem emboço/chapisco no entreforro)
```
> ⚠️ **Regra de Muretas de Apoio de Cobertura:** Verificar no corte da cobertura a quantidade de linhas de apoio da telha (ex: 3 muretas escalonadas h=0,39m, 0,58m e 0,77m para a inclinação de 9%). As muretas internas no entreforro **NÃO recebem emboço/pintura**, sendo computadas apenas como alvenaria de bloco aparente/bruta.

**Ambiente com geometria irregular (L, U, T, recortes):**
```
A_bruta = (P1 + P2 + P3 + ... + Pn) × H_pé-direito
Onde P1..Pn = comprimento medido de CADA trecho de parede individualmente descontando pilares e cantos
A_líquida = A_bruta − Σ Descontos de Vãos
A_final = A_líquida × (1 + Taxa de Perda)
```
> O agente DEVE perguntar se o ambiente é retangular ou irregular. Se irregular, solicitar comprimento de cada trecho (P1, P2, P3...).

### 1.2 Regra de Desconto de Vãos — NBR 12721 Art. 3 (Material vs. Serviço)

> ⚠️ **DUPLA VISÃO DE QUANTITATIVOS (COMPRAS vs. EMPREITEIRO):**
> No PMO Virtual, todo orçamento de alvenaria e revestimentos DEVE gerar duas quantificações separadas para evitar desperdício de material e pleitos contratuais:

| Visão de Engenharia | Regra de Desconto de Vãos | Objetivo Operacional | Exemplo Portaria 02 |
|---|---|---|---|
| **1. VISÃO MATERIAL (Suprimentos)** | **Desconto Físico 100%** de todos os vãos (portas e janelas) | Comprar a quantidade real de blocos, cimento e argamassa (+ perda comercial) | **49,84 m²** (~680 blocos) |
| **2. VISÃO SERVIÇO (Empreiteiro)** | **Regra NBR 12721** (vãos ≤ 2,00m² medidos cheios; > 2,00m² desconta excedente) | Medir e pagar o empreiteiro remunerando o requadramento sem pagar item extra | **59,48 m²** (boletim de medição) |

| Área do Vão (A_vão) | Critério NBR 12721 (Serviço) | Desconto na Medição de Serviço |
|---|---|---|
| A_vão ≤ 2,00 m² | **NÃO desconta** | 0,00 m² (remunera requadros e bonecas) |
| 2,00 m² < A_vão ≤ 6,00 m² | **Desconta o excedente** | A_vão − 2,00 m² |
| A_vão > 6,00 m² | **Desconta tudo** | A_vão completo |
| Armário embutido / nicho | **Desconta 100%** | A_nicho completo |

### 1.3 Taxas de Perda por Serviço de Parede

| Serviço | Taxa de Perda |
|---|---|
| Chapisco | 5% |
| Emboço / Reboco | 5% |
| Gesso liso | 5% |
| Cerâmica / Porcelanato (parede) | 10% |
| Tinta látex acrílica | 10% |
| Massa corrida PVA | 0% (aplicada sobre área líquida) |

---

### 1.4 Métodos de Quantificação de Alvenaria: Paramétrico (Sem Paginação) vs. Executivo (Com Paginação)

> ⚠️ **REGRAS DE MATURIDADE DO PROJETO:** O PMO Virtual deve identificar a fase do projeto antes de iniciar o levantamento de alvenaria.
> 
> 🛑 **ALERTA ABSOLUTO — PROJETO EXECUTIVO NÃO ADMITE ESTIMATIVAS:** Se existirem pranchas de arquitetura e desenhos executivos fornecidos, é **TERMINANTEMENTE VEDADO** usar estimativas paramétricas. Havendo omissão de cotas ou detalhes no desenho, o item **NÃO DEVE SER LEVANTADO**, registrando-se formalmente a observação de falta de informação no desenho na memória de cálculo e abrindo-se RFI.

#### 🅰️ FASE 1: Estudo Preliminar / Viabilidade (SEM PROJETO EXECUTIVO APENAS)
Quando o projeto estrutural e de arquitetura executivo **AINDA NÃO EXISTEM** (fase inicial de estudo de viabilidade ou EVTE puro, com autorização expressa do cliente para estimativa preliminar):

1. **Dupla Visão de Vãos (MAT vs. MDO):**
   - `MAT (Desconto Físico 100%):` Subtrai a área real total de portas e janelas para compra exata de blocos.
   - `MDO (Desconto NBR 12721):` Aplica as regras de desconto parcial (vãos ≤ 2m² medidos cheios) para remuneração do empreiteiro/pedreiro.
2. **Estimativas de Graute Paramétrico:**
   - `Graute Canal (m³):` Estimado por metros lineares de vergas, contravergas e cintas superiores (`L_cinta × A_calha`).
   - `Graute Pilaretes (m³):` Estimado pela quantidade de prumos verticalizados a cada 1,5m a 2,0m (`N_prumos × H_parede × A_alvéolo`).
3. **Encunhamento Paramétrico (m³):**
   - Calculado pela extensão linear no topo da parede quando houver encunhamento com argamassa expansiva (`Comprimento × Espessura × 0,05m`).

#### 🅱️ FASE 2: Orçamento Executivo / Com Paginação (Método por Elevação e SKU)
Quando as pranchas de paginação de alvenaria estrutural **ESTÃO DISPONÍVEIS** (projetos tipo Engesique), abandona-se o m² genérico e quantifica-se por **Elevação Parede a Parede (`ELEV`)**:

##### A. Tabela de Mapeamento de SKUs de Blocos Modulados
| Código SKU | Descrição do Bloco | Dimensões (cm) | Área de Face (m²) | Função Principal |
|---|---|---|---|---|
| **B144 / B194** | Bloco Inteiro de Vedação/Estrutural | 14×19×39 / 19×19×39 | 0,080 | Elevação corrente dos painéis |
| **B142 / B192** | Meio Bloco | 14×19×19 / 19×19×19 | 0,040 | Amarração de cantos e vãos sem corte |
| **C144 / C194** | Bloco Canaleta Inteiro | 14×19×39 / 19×19×39 | 0,080 | Cinta de amarração, vergas e contravergas |
| **C142 / C192** | Bloco Canaleta Meio | 14×19×19 / 19×19×19 | 0,040 | Fechamento de amarrações de cinta |
| **BC94 / BC99** | Bloco Compensador / Japa | 14×19×9 ou variável | 0,008 a 0,018 | Ajuste fino de módulo e fiada de transição |
| **CC146 / CC1415** | Bloco de Canto / Especial | Variável | 0,012 a 0,030 | Encontro de paredes em L, T ou Z |

##### B. Fórmulas de Quantificação Executiva de Alvenaria Estrutural
```text
1. Quantidade de Blocos por Tipo em cada Elevação (ELEV_i):
   N_bloco_k = Σ (Blocos do tipo k na elevação paginada ELEV_i)

2. Volume de Graute Executivo (m³):
   V_graute = (N_alvéolos_grauteados × A_alvéolo × H_elevação) + (N_canaletas × A_calha_canaleta × L_canaleta)

3. Armadura Vertical (kg) e Horizontal (kg):
   Peso_aço_vert = N_prumos_grauteados × (H_pé-direito + C_transpasse) × Peso_linear(Ø)
   Peso_aço_horiz = Σ (L_cinta × N_barras × Peso_linear(Ø))

4. Agrupamento Logístico em Kit-Paletes com QR Code:
   N_paletes_eixo = Ceil( Σ N_blocos_eixo / Capacidade_palete_padrão )
   Etiqueta QR Code = { Obra, Pavimento, Eixo/Apto, Qtd_B144, Qtd_B142, Qtd_C144, Qtd_Graute_m3, Prancha_Desenho_URL }
```

---

### 1.5 Matriz Mestra de Revestimentos e Acabamentos por Ambiente (Método Room-by-Room)

> ⚠️ **PADRÃO DE PLANILHA MATRIX:** O levantamento de revestimentos internos DEVE ser estruturado em colunas por **Nº do Ambiente (Ambiente 1, 2, 3...)**, derivando automaticamente as áreas de materiais (MAT) e mão de obra (MDO) a partir dos atributos geométricos do cômodo.

#### A. Parâmetros de Entrada por Ambiente
| Atributo do Ambiente | Unidade | Descrição Técnica / Aplicação |
|---|---|---|
| `Área Piso` | m² | Área útil interna do cômodo |
| `Área Teto` | m² | Área útil de gesso/forro/pintura de teto |
| `Perímetro` | m | Perímetro bruto interno de paredes |
| `Pé-Direito Revestimento (H_revest)` | m | Altura bruta do piso até acima do forro (chapisco/emboço) |
| `Pé-Direito Acabamento (H_acab)` | m | Altura livre visível do piso até a tabica/forro (pintura/massa) |
| `Vãos Total` | m² | Soma da área de TODOS os vãos (portas/janelas/aberturas) |
| `Vãos p/ Desconto NBR (>2,00m²)` | m² | Soma do excedente de vãos com área $> 2,00 \, m²$ |
| `Desconto Rodapé` | m | Soma das larguras de portas (aberturas onde não vai rodapé) |
| `Sanca` | m | Extensão linear de sancas/cortineiros de gesso |

#### B. Fórmulas Derivadas por Coluna de Ambiente
```text
1. Parede - Revestimento MAT (m²):
   A_revest_MAT = (Perímetro × H_revest) − Vãos_Total

2. Parede - Revestimento MDO / Gesso (m²):
   A_revest_MDO = (Perímetro × H_revest) − Vãos_p/ Desconto_NBR

3. Parede - Acabamento MAT (m²):
   A_acab_MAT = (Perímetro × H_acab) − Vãos_Total

4. Parede - Acabamento MDO / Pintura (m²):
   A_acab_MDO = (Perímetro × H_acab) − Vãos_p/ Desconto_NBR

5. Impermeabilização com Virada de 20cm (Áreas Frias - m²):
   A_impermeab_virada = Área_Piso + (Perímetro × 0,20m)

6. Rodapé Líquido (m):
   L_rodapé = Perímetro − Desconto_Rodapé
```

#### C. Consolidação no Resumo Mestre (Summary Sheet por Pavimento)
As colunas dos ambientes (`PLAN01`, `PLAN02`, `PLAN04`...) são somadas automaticamente no **Resumo Geral de Revestimentos e Acabamentos**, agrupando por disciplinas:
- **Impermeabilização e Isolamento Térmico:** Áreas frias (nivelamento, polimérica, proteção mecânica), terraços/varandas, poço de elevador, reservatórios e coberturas/calhas.
- **Revestimentos de Parede e Teto:** Emboço, gesso liso, cerâmica, pinturas e rodapés.

---

### 1.6 Revestimentos Externos por Panos de Fachada (Panos, Frisos & Molduras)

> ⚠️ **REGRA DE FACHADA:** É **PROIBIDO** medir fachada por perímetro interno ou aproximação simplificada. O orçamento de revestimento externo DEVE ser desmembrado por **Panos de Fachada (`PANO 01, PANO 02...`)**, considerando reentrâncias, sacadas, platibandas, frisos e molduras.

#### A. Estrutura por Panos Geométricos de Fachada (`DESCRIÇÃO DO PANO`)
| Parâmetro | Unidade | Aplicação / Cálculo |
|---|---|---|
| `Comprimento do Pano` | m | Extensão horizontal contínua do trecho de fachada |
| `Altura (PD do Pano)` | m | Altura total do plano (da base/balancim até o topo/platibanda) |
| `Vãos Total` | m² | Soma total da área de esquadrias e aberturas externas |
| `Vãos p/ Desconto NBR (>2,00m²)` | m² | Excedente de vãos para contrato de fachadistas/balancim |
| `Frisos e Faixas` | m | Metros lineares de juntas de dilatação, frisos decorativos e pingadeiras |
| `Requadros e Molduras` | m | Metros lineares de requadramento de molduras de janelas e sacadas |

#### B. Fórmulas de Fachada
```text
1. Chapisco e Massa Única MAT (m²):
   A_fachada_MAT = (Comprimento × Altura) − Vãos_Total

2. Chapisco e Massa Única MDO / Balancim (m²):
   A_fachada_MDO = (Comprimento × Altura) − Vãos_p/ Desconto_NBR

3. Frisos, Juntas de Dilatação e Pingadeiras (m):
   L_frisos = Σ (Metros lineares de frisos e juntas no pano)

4. Requadro de Molduras e Peitoris Externos (m):
   L_requadro = Σ (Perímetro dos vãos requadrados na fachada)
```

---

### 1.7 Protocolo de Registro de Omissão de Desenho e Padrão de Observação na Memória

Sempre que uma informação necessária para a quantificação não estiver expressa nas pranchas (ex: falta de cota de peitoril, acabamento não especificado no memorial de acabamentos, falta de corte para altura de forro/platibanda):

1. **Procedimento Técnico Imediato:**
   - **NÃO chutar nem arbitrar dimensões.**
   - O item não recebe quantidade fictícia (quantidade permanece `0` ou `PENDENTE`).
2. **Modelo Obrigatório de Observação na Memória de Cálculo:**
   ```text
   > ⚠️ OBSERVAÇÃO DE AUDITORIA — ITEM NÃO LEVANTADO POR FALTA DE INFORMAÇÃO NO DESENHO:
   > - Serviço/Elemento: [Ex: Rodapé em Porcelanato 10cm / Peitoril em Granito]
   > - Ambiente / Localização: [Ex: Guarita Térreo / CIA T-001-GUA]
   > - Prancha de Referência Analisada: [Ex: Prancha AÇU-3.DES-2.3100-15-EGS-018 Rev 01]
   > - Motivo da Não Quantificação: Cota de vão e espessura do peitoril não indicadas na prancha de esquadrias nem no corte longitudinal.
   > - Ação Requerida: Emissão de RFI (Pedido de Informação) nº [XX] para definição pelo projetista. O item será incorporado na revisão orçamentária após emissão de prancha revisada.
   ```

---

### 1.8 Algoritmo de Desmembramento Obrigatório de Alvenaria em SKUs Comerciais (B144, B142, C144) e Insumos Estruturais

> 🛑 **PROIBIÇÃO ABSOLUTA DE "BLOCO GENÉRICO":**  
> É expressamente proibido orçar alvenaria de blocos de concreto como um item monolítico de "bloco 14x19x39cm". Uma obra que compra apenas blocos inteiros sofre desperdício catastrófico por quebra manual de blocos em cantos e vãos, ou paralisa por falta de canaletas para vergas e contravergas.  
> O quantitativo de alvenaria DEVE ser desmembrado nos seguintes SKUs físicos:

1. **Blocos Canaleta Inteiros (C144: 14×19×39cm ou C194: 19×19×39cm):**  
   Calculados pela extensão linear total de **Vergas** (portas e janelas), **Contravergas** (janelas) e **Cintas de Amarração**:
   ```text
   L_vergas_portas = Σ (Largura_porta + 2 × 0,20m)
   L_vergas_janelas = Σ (Largura_janela + 2 × 0,20m)
   L_contravergas_janelas = Σ (Largura_janela + 2 × 0,20m)
   L_cintas_amarração = Extensão linear de cintas indicadas em projeto
   L_canaleta_total = L_vergas_portas + L_vergas_janelas + L_contravergas_janelas + L_cintas_amarração
   N_canaletas_C144 = Ceil( L_canaleta_total / 0,40m ) × 1,05
   ```
2. **Graute Fino para Preenchimento de Canaletas (m³):**  
   Volume interno da calha das canaletas preenchidas (`A_calha ≈ 0,09m × 0,14m = 0,0126 m²`):
   ```text
   V_graute = L_canaleta_total × 0,0126 m² × 1,05
   ```
3. **Armadura CA-50 de Vergas e Contravergas (kg e barras 12m):**  
   2 barras longitudinais CA-50 Ø8,0mm por canaleta:
   ```text
   L_aço_canaleta = L_canaleta_total × 2 × 1,05
   N_barras_12m = Ceil( L_aço_canaleta / 12,0m )
   Peso_aço_canaleta = L_aço_canaleta × 0,395 kg/m
   ```
4. **Meios Blocos (B142: 14×19×19cm ou B192: 19×19×19cm):**  
   Utilizados na amarração vertical de requadros de portas e janelas (1 meio bloco a cada 2 fiadas em cada ombreira) e em cantos/encontros em T sem corte:
   ```text
   N_meios_portas = Σ [ Floor( H_porta / 0,40m ) × 2 ombreiras ]
   N_meios_janelas = Σ [ Floor( H_janela / 0,40m ) × 2 ombreiras ]
   N_meios_cantos = N_encontros_L_T × Floor( H_parede / 0,40m )
   N_meios_blocos_B142 = (N_meios_portas + N_meios_janelas + N_meios_cantos) × 1,05
   ```
5. **Blocos Inteiros Correntes (B144: 14×19×39cm ou B194: 19×19×39cm):**  
   Dedução direta da equivalência de área das canaletas e meios blocos em relação ao total de blocos equivalentes da parede:
   ```text
   N_blocos_total_equivalente = A_alvenaria_líquida × 12,5 blocos/m²
   N_blocos_inteiros_B144 = [ N_blocos_total_equivalente − N_canaletas_C144 − (N_meios_blocos_B142 / 2) ] × 1,05
   ```
6. **Argamassa de Assentamento dos Blocos (m³ ou sacos de cimento/cal):**  
   Consumo normativo: 0,018 m³ de argamassa mista 1:2:8 por m² de alvenaria:
   ```text
   V_argamassa_assent = A_alvenaria_líquida × 0,018 m³/m² × 1,05
   Cimento_assentamento = A_alvenaria_líquida × 5,2 kg/m² × 1,05 (sacos 50kg)
   Cal_hidratada = A_alvenaria_líquida × 1,8 kg/m² × 1,05 (sacos 20kg)
   Areia_média = A_alvenaria_líquida × 0,022 m³/m² × 1,05 (m³)
   ```

---

## 📐 2. Pisos, Contrapisos e Revestimentos de Piso

### 2.1 Fórmulas

**Ambiente retangular:**
```
A_piso = Comprimento_interno × Largura_interna
A_piso_líq = A_piso − Área de pilares embutidos − Área de ralos/grelhas
A_final = A_piso_líq × (1 + Taxa de Perda)
```

**Ambiente com geometria irregular (L, U, T):**
```
A_piso = Σ (áreas parciais decompostas em retângulos ou triângulos)
A_piso_líq = A_piso − descontos
A_final = A_piso_líq × (1 + Taxa de Perda)
```
> O agente DEVE decompor plantas irregulares em retângulos menores.

### 2.2 Taxas de Perda por Tipo de Piso

| Tipo de Piso | Taxa de Perda |
|---|---|
| Cerâmica / Porcelanato alinhado | 10% |
| Cerâmica / Porcelanato diagonal | 15% |
| Laminado / Vinílico plank | 10% |
| Piso natural (mármore, granito) | 10% |
| Contrapiso de regularização | 5% |
| Concreto polido | 3% |

---

## 📐 3. Revestimento de Teto (Forro / Gesso / Pintura)

> ⚠️ SEPARAÇÃO OBRIGATÓRIA: O teto é um serviço separado da parede. Memórias de cálculo independentes.

### 3.1 Fórmula

```
A_teto = Comprimento_interno × Largura_interna
A_teto_líq = A_teto − Aberturas (alçapão, shaft, luminária grande)
A_final = A_teto_líq × (1 + Taxa de Perda)
```

### 3.2 Taxas de Perda — Teto

| Serviço | Taxa |
|---|---|
| Gesso liso (sarrafeado) | 5% |
| Forro de gesso acartonado (Drywall) | 10% |
| Forro PVC | 10% |
| Pintura de teto | 10% |

---

## 📐 4. Cobertura (Telhado)

### 4.1 Fórmula Área Inclinada

```
A_inclinada = A_horizontal / cos(θ)
Onde θ = inclinação do plano em graus
```

### 4.2 Fatores de Inclinação

| Inclinação | cos(θ) | Fator Multiplicador |
|---|---|---|
| 15° (telha plan, fibrocimento) | 0,966 | 1,035 |
| 22° (telha romana, colonial) | 0,927 | 1,079 |
| 30° (metálica, fibrocimento) | 0,866 | 1,155 |
| 45° (chapa metálica íngreme) | 0,707 | 1,414 |

**Acréscimos lineares (medidos em metros):**
- Beiral: projeção horizontal × fator de inclinação
- Calhas e rufos: m linear
- Cumeeiras: m linear

---

## 📐 5. Esquadrias, Vidros, Fechaduras e Derivação Automática de Vergas/Contravergas

> ⚠️ **REGRA DE ESQUADRIAS:** O levantamento de esquadrias DEVE ser estruturado em **duas etapas interligadas**: um **Quadro Mestre Cadastral de Tipologias** e uma **Tabela de Alocação por Ambiente** que deriva automaticamente pintura e vergas/contravergas.

### 5.1 Quadro Mestre de Tipologias Cadastrais (`CÓD` `JA01`, `PA01`, `GA01`)
| Código | Tipo / Disciplina | Descrição Técnica | Largura (m) | Altura (m) | Área Unid (m²) | Vidro / Fechadura | Coef. Pintura |
|---|---|---|---|---|---|---|---|
| **JA01** | Janela Alumínio | Basculante 1 Folha | 0,60 | 0,60 | 0,36 | Vidro Foco 4mm | 1,00 (1 face) |
| **JA02** | Janela Alumínio | Correr 2 Folhas | 1,20 | 1,20 | 1,44 | Vidro Incolor 4mm | 2,00 (2 faces) |
| **PA01** | Porta Madeira | Lisa c/ Batente e Alizar | 0,80 | 2,10 | 1,68 | Fechadura Soprano | 2,00 (2 faces) |
| **GA01** | Gradil Alumínio | Peitoril Sacada H=1,10m | 2,50 | 1,10 | 2,75 | — | 2,00 (2 faces) |

### 5.2 Tabela de Alocação por Ambiente e Derivação Automática
```text
1. Vínculo de Quantidades por Pavimento:
   Qtd_Total_Esquadria = Qtd_por_tipo × Qtd_andares

2. Área Total de Pintura de Esquadria/Batente (m²):
   A_pintura_esq = (Largura × Altura) × Coef_Pintura × Qtd_Total
   (Coef_Pintura = 1,00 para 1 face; 2,00 para 2 faces/ambas as vistas)

3. Derivação Automática de Verga e Contraverga (m):
   - Verga (Topo do Vão): L_verga = (Largura + 2 × 0,20m) × Qtd_Total
   - Contraverga (Base da Janela): L_contraverga = (Largura + 2 × 0,20m) × Qtd_Janelas
```

### 5.3 Algoritmo Matemático de Derivação Automática de Miudezas, Fixações e Acessórios de Arquitetura (Kits de Montagem 360°)

> 🛑 **PROIBIÇÃO DE ORÇAMENTOS SINTÉTICOS:** Conforme a [SKILL_QUANTIFICACAO_AUDITORIA_E_CORRECAO.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANTIFICACAO_AUDITORIA_E_CORRECAO.md), é terminantemente vedado orçar esquadrias, revestimentos, pinturas ou coberturas apenas por blocos agregados (ex: "conjuntos completos", "área global de pintura") omitindo parafusos, dobradiças, fechaduras, lixas, seladores, espaçadores, argamassas colantes, espumas expansivas, telas de amarração e insumos de fixação. Toda obra requer suprimentos granulares para não paralisar frentes de serviço.
> 
> As miudezas e kits de montagem **DEVEM ser calculados automaticamente por derivação matemática direta** dos elementos principais da arquitetura:

#### A. Kit Esquadrias (Portas de Madeira/Alumínio e Janelas)
1. **Dobradiças em Aço Inox / Zincado 3 ½" × 3" c/ Parafusos (unid):**  
   Portas de abrir de 1 folha utilizam 3 dobradiças; portas de folha dupla utilizam 6 dobradiças (3 por folha):
   ```text
   N_dobradiças = Σ (3 × N_folhas_abrir) × 1,05
   ```
2. **Fechaduras Completas (Máquina + Cilindro/Chaves + Maçanetas + Rosetas/Espelhos - unid):**  
   1 conjunto completo por porta, diferenciando tipologia (Externa com cilindro, Interna chave gorge ou WC tranqueta livre/ocupado):
   ```text
   N_fechaduras = N_portas_total
   ```
3. **Batedores de Porta de Piso c/ Amortecedor em Inox (unid):**  
   1 batedor por folha de porta para proteção de alvenarias e marcenarias:
   ```text
   N_batedores = N_folhas_total
   ```
4. **Espuma de Poliuretano Expansiva 750ml para Fixação de Marcos/Batentes (tubos):**  
   Fixação, isolamento termoacústico e preenchimento de folgas entre alvenaria e batente de porta (1 tubo rende a instalação de 2 a 3 marcos):
   ```text
   N_tubos_PU = Ceil( N_portas / 2,5 ) × 1,05
   ```
5. **Parafusos e Buchas S8 para Fixação de Batentes e Contramarcos (unid):**  
   8 pontos de fixação mecânica por porta (4 por ombreira):
   ```text
   N_parafusos_marco = N_portas × 8 × 1,05
   ```
6. **Pregos de Aço sem Cabeça 12×12 ou 10×10 para Guarnições/Alizares (unid ou kg):**  
   Fixação dos alizares de acabamento nos batentes (20 pregos por vão de porta):
   ```text
   N_pregos_alizar = N_portas × 20 × 1,05
   ```
7. **Cola Branca PVA D3 para Madeira (frascos 500g):**  
   Colagem e travamento das meias-esquadrias (cortes em 45°) dos alizares (1 frasco a cada 8 portas):
   ```text
   N_frascos_cola = Ceil( N_portas / 8,0 ) × 1,05
   ```
8. **Selante PU 40 / Silicone Neutro para Calafetação Perimétrica de Caixilhos (tubos 310ml):**  
   Vedação hidrófuga em todo o contorno perimétrico externo de janelas e portas externas contra infiltração pluvial (1 cartucho rende ~10 metros lineares de junta 5×5mm):
   ```text
   Perímetro_caixilhos_ext = Σ [ 2 × (Largura + Altura) ] das esquadrias externas
   N_tubos_selante = Ceil( Perímetro_caixilhos_ext / 10,0m ) × 1,05
   ```

#### B. Kit Pintura, Regularização e Proteção de Superfícies
1. **Selador Acrílico Base Água (L ou latas 18L):**  
   Aplicação obrigatória como fundo selador sobre reboco novo ou alvenaria bruta antes da massa/tinta (consumo normativo: 0,10 L/m²):
   ```text
   V_selador = A_parede_nova × 0,10 L/m²
   N_latas_selador = Ceil( V_selador / 18,0L ) × 1,05
   ```
2. **Fundo Preparador de Paredes (L ou latas 18L):**  
   Aplicação em superfícies calcinadas, gesso liso ou drywall para aglutinar partículas e uniformizar absorção (consumo normativo: 0,10 L/m²):
   ```text
   V_fundo_prep = (A_gesso_liso + A_drywall) × 0,10 L/m²
   N_latas_fundo_prep = Ceil( V_fundo_prep / 18,0L ) × 1,05
   ```
3. **Massa Corrida PVA (Interna Seca) ou Massa Acrílica (Externa / Áreas Úmidas - kg ou latas 25kg):**  
   Regularização para pintura lisa acetinada em 2 demãos (consumo médio: 0,90 kg/m² para PVA; 1,20 kg/m² para Acrílica):
   ```text
   Massa_total = A_líquida_massa × Consumo_específico (kg/m²)
   N_latas_massa = Ceil( Massa_total / 25,0kg ) × 1,05
   ```
4. **Lixas para Parede / Massa (folhas):**  
   - **Lixa Grossa (Grão 80/100):** Quebra de arestas e grãos do reboco antes do selador (consumo: 0,05 folha/m²).  
   - **Lixa Fina (Grão 150/220):** Lixamento entre demãos de massa corrida e acabamento final (consumo: 0,10 folha/m²):
   ```text
   N_folhas_lixa_grossa = Ceil( A_reboco × 0,05 ) × 1,05
   N_folhas_lixa_fina = Ceil( A_massa_corrida × 0,10 ) × 1,05
   ```
5. **Fita Crepe 24mm e 48mm × 50m para Isolamento e Pintura (rolos):**  
   Proteção de esquadrias, vidros, rodapés e peitoris contra respingos de tinta (1 rolo a cada 50 metros lineares protegidos):
   ```text
   L_proteção = Perímetro_rodapé + Perímetro_esquadrias + Perímetro_peitoris
   N_rolos_crepe = Ceil( L_proteção / 50,0m ) × 1,05
   ```
6. **Lona Plástica Preta / Transparente para Proteção de Pisos (bobinas 100m²):**  
   Forração de 100% dos pisos acabados durante os serviços de emboço, gesso e pintura:
   ```text
   N_bobinas_lona = Ceil( A_piso_útil / 100,0m² ) × 1,05
   ```
7. **Solvente / Aguarrás Mineral (litros):**  
   Diluição de tintas esmalte sintético em portas e estruturas metálicas e limpeza de ferramentas (1 litro a cada 10 litros de esmalte):
   ```text
   V_aguarrás = Ceil( V_esmalte_sintético / 10,0L )
   ```

#### C. Kit Pisos, Contrapisos e Revestimentos Cerâmicos
1. **Argamassa Colante / Cimentcola (sacos 20kg):**  
   - Tipo AC-I (áreas secas internas): 5,0 kg/m² simples.  
   - Tipo AC-II (áreas molhadas/externas): 5,0 kg/m² simples.  
   - Tipo AC-III (porcelanatos grandes formatos ≥ 60×60cm ou fachadas - Dupla Colagem obrigatória): 10,0 kg/m²:
   ```text
   Peso_cimentcola = Σ [ A_revest_k × Consumo_k (5 ou 10 kg/m²) ]
   N_sacos_cimentcola = Ceil( Peso_cimentcola / 20,0kg ) × 1,05
   ```
2. **Rejunte Cimentício / Acrílico / Epóxi (sacos 1kg ou 5kg):**  
   Conforme especificação e tamanho de junta (consumo médio: 0,25 kg/m² para porcelanato junta 2mm; 0,50 kg/m² para cerâmica junta 3mm):
   ```text
   Peso_rejunte = Σ [ A_revest_k × Consumo_rejunte_k ]
   N_sacos_rejunte = Ceil( Peso_rejunte / 5,0kg ) × 1,05
   ```
3. **Espaçadores / Cruzetas Plásticas (sacos com 100 unid):**  
   Alinhamento de juntas de assentamento de pisos e azulejos (consumo normativo: 6 un/m²):
   ```text
   N_sacos_espaçador = Ceil( (A_piso_líq + A_azulejo_líq) × 6 / 100 )
   ```
4. **Clips e Cunhas Niveladoras para Porcelanatos Retificados (sacos com 100 unid):**  
   Nivelamento de peças retificadas (formato ≥ 60×60cm: 4 clips por placa; cunhas reutilizáveis a 30% do total de clips para giro de frente):
   ```text
   N_peças = A_piso_porcelanato / A_peça
   N_sacos_clips = Ceil( N_peças × 4 / 100 )
   N_sacos_cunhas = Ceil( (N_peças × 4 × 0,30) / 100 )
   ```
5. **Soleiras e Peitoris em Granito/Mármore (metros lineares):**  
   - Soleiras: transição de pisos sob portas (`L_soleira = Σ Largura_portas`).  
   - Baguetes de Box: contenção de água no box do banheiro (`L_baguete = Largura_box`).  
   - Peitoris: arremate inferior externo de janelas com pingadeira (`L_peitoril = Σ Largura_janelas + 0,10m`).

#### D. Kit Impermeabilização e Estanqueidade
1. **Primer Asfáltico / Emulsão Asfáltica de Imprimação (litros ou baldes 18L):**  
   Pintura de aderência prévia para aplicação de mantas asfálticas (consumo normativo: 0,40 L/m²):
   ```text
   V_primer = A_impermeab_manta × 0,40 L/m²
   N_baldes_primer = Ceil( V_primer / 18,0L ) × 1,05
   ```
2. **Tela de Poliéster / Véu de Fibra de Vidro para Reforço Estrutural (m² ou rolos 50m²):**  
   Reforço elástico de cantos, meias-canas, ralos e juntas de dilatação em impermeabilização líquida polimérica ou asfáltica (consumo: 1,10 m²/m² em áreas críticas):
   ```text
   A_tela_reforço = A_impermeab_líquida × 1,10
   N_rolos_tela = Ceil( A_tela_reforço / 50,0m² )
   ```
3. **Fita Asfáltica Autoadesiva Aluminizada (Fita Multiuso 10cm/20cm - rolos 10m):**  
   Arremate de vedação estanque em calhas, rufos, tubulações passantes e transpasses de platibanda:
   ```text
   L_arremates = Σ (Perímetro de ralos passantes + juntas de calhas/rufos)
   N_rolos_fita_asfáltica = Ceil( L_arremates / 10,0m ) × 1,05
   ```
4. **Gás GLP em Botijão P-13 / P-45 para Maçarico de Manta Asfáltica (unid):**  
   Consumo de combustível térmico para soldagem de manta asfáltica armada (rendimento: 1 botijão P-13 para cada ~50 m² de manta instalada):
   ```text
   N_botijões_P13 = Ceil( A_manta_asfáltica / 50,0m² )
   ```
5. **Camada Separadora / Geotêxtil Não-Tecido (tipo Bidim RT-08 ou filme de polietileno - m²):**  
   Camada de dessolidarização entre a manta impermeabilizante e o contrapiso de proteção mecânica (consumo: 1,10 m²/m²):
   ```text
   A_separadora = A_manta_horizontal × 1,10
   ```

#### E. Kit Alvenaria (Amarração Pilar-Parede, Encunhamento e Aditivos)
1. **Telas Metálicas Eletrosoldadas Galvanizadas 15×50cm de Amarração (unid):**  
   Travamento mecânico anti-fissura entre pilares de concreto armado e alvenaria de blocos, instaladas a cada 2 fiadas (a cada 0,40m de altura) em todas as interfaces pilar-parede:
   ```text
   N_fiadas_tela = Floor( H_livre / 0,40m )
   N_telas_amarração = N_interfaces_pilar_alvenaria × N_fiadas_tela × 1,05
   ```
2. **Pinos de Aço c/ Arruela Cônica e Cartuchos de Festim para Finca-Pinos (unid):**  
   2 pinos de aço e 2 disparos de cartucho festim por tela de amarração:
   ```text
   N_pinos_finca = N_telas_amarração × 2 × 1,05
   N_cartuchos_festim = N_pinos_finca
   ```
3. **Encunhamento Flexível no Topo da Alvenaria (m):**  
   Fechamento da folga de deformação no encontro do topo da alvenaria com o fundo de vigas/lajes (usando argamassa com aditivo expansor ou espuma adesiva estrutural para alvenaria):
   ```text
   L_encunhamento = Comprimento_total_paredes_topo (m)
   ```
4. **Aditivo Plastificante e Adesivo para Argamassas (tipo Bianco / Vedalit - baldes 18L):**  
   Melhorador de aderência para chapiscos rolados e retenção de água de emboços (consumo médio: 0,20 L/m² de chapisco):
   ```text
   V_adesivo = A_chapisco × 0,20 L/m²
   N_baldes_adesivo = Ceil( V_adesivo / 18,0L ) × 1,05
   ```

#### F. Kit Cobertura (Telhas Sandwich, Terças, Calhas e Rufos)
1. **Parafusos Autobrocantes 12×1" ou 12×2" c/ Arruela EPDM/Neoprene (unid):**  
   Fixação das telhas termoacústicas trapezoidais nas terças metálicas (densidade média: 4,5 parafusos por m² de área real de cobertura):
   ```text
   N_autobrocantes = Ceil( A_real_cobertura × 4,5 ) × 1,05
   ```
2. **Parafusos de Costura (Stitch) 10×3/4" c/ Arruela EPDM (unid):**  
   Fixação e travamento da sobreposição lateral longitudinal das telhas (espaçados a cada 0,50 m na emenda):
   ```text
   N_costura = Ceil( L_terças × N_linhas_sobreposição / 0,50m ) × 1,05
   ```
3. **Fita de Vedação Butílica Autoadesiva 15mm (rolos de 10m):**  
   Estanqueidade das sobreposições longitudinais de telhas e transpasse de calhas e rufos:
   ```text
   L_emendas = Comprimento_calhas + (N_linhas_telha × Extensão_transpasse)
   N_rolos_butílica = Ceil( L_emendas / 10,0m ) × 1,05
   ```
4. **Chumbadores / Parabolts CBA 3/8" × 3" para Fixação de Terças Metálicas (unid):**  
   Fixação das bases das terças de perfil U nas muretas escalonadas de alvenaria/concreto (2 por ponto de apoio):
   ```text
   N_parabolts = N_linhas_terças × N_muretas_apoio × 2 × 1,05
   ```
5. **Rebites de Repuxo em Alumínio 4,0×10mm para Calhas e Rufos (cento/milheiro):**  
   União mecânica das emendas sobrepostas de chapas galvanizadas de calhas e rufos (10 rebites por metro de emenda):
   ```text
   N_rebites = Ceil( N_emendas_calha_rufo × 10 ) × 1,05
   ```
6. **Selante PU 40 / Mastique de Calha para Calafetação (tubos 310ml):**  
   Vedação hidrófuga nas costuras rebitadas e junções de calhas e rufos (1 tubo a cada 5 metros lineares de junta):
   ```text
   N_tubos_selante_calha = Ceil( L_emendas_calha_rufo / 5,0m ) × 1,05
   ```

#### G. Kit Louças e Metais (Conexões e Acessórios Hidráulicos de Arquitetura)
1. **Engates Flexíveis em Aço Inox Trançado 1/2" × 40cm (unid):**  
   Alimentação de água fria/quente para lavatórios, bacias com caixa acoplada, pias de cozinha e bebedouros:
   ```text
   N_engates = N_bacias_cx_acoplada + (N_torneiras_lavatório) + (N_cubas_cozinha)
   ```
2. **Sifões Universais Sanfonados em Polipropileno / Metal Cromado (unid):**  
   Escoamento de águas servidas de cubas, lavatórios, tanques e mictórios:
   ```text
   N_sifões = N_cubas + N_lavatórios + N_tanques + N_mictórios
   ```
3. **Válvulas de Escoamento (Click / Americana / Comum - unid):**  
   1 válvula por ralo de cuba de lavatório, pia ou tanque:
   ```text
   N_válvulas = N_sifões
   ```
4. **Anel de Vedação de Cera com Guia Plástica para Bacia Sanitária (unid):**  
   Vedação hermética anti-odor entre a saída da bacia e o tubo de esgoto de 100mm:
   ```text
   N_anéis_vedação = N_bacias_sanitárias_total
   ```
5. **Parafusos e Buchas em Latão / Inox B10/B12 para Fixação de Bacias e Lavatórios (pares):**  
   Fixação no contrapiso/parede resistente à corrosão por urina e umidade (1 par por bacia e por lavatório com coluna):
   ```text
   N_pares_parafusos_wc = N_bacias + N_lavatórios
   ```
6. **Fita Veda Rosca PTFE 18mm × 25m (rolos):**  
   Vedação de roscas macho de engates, torneiras e niples:
   ```text
   N_rolos_veda_rosca = Ceil( (N_torneiras + N_engates + N_registros) / 10 )
   ```

#### H. Kit Drywall e Forros de Gesso Acartonado (quando aplicável)
1. **Parafusos Drywall Ponta Agulha GN 25 / GN 35 (cento/milheiro):**  
   Fixação das placas de gesso acartonado nos perfis metálicos (consumo médio: 25 parafusos por m² de placa):
   ```text
   N_parafusos_GN = Ceil( A_placa_drywall × 25 ) × 1,05
   ```
2. **Parafusos Metal-Metal Ponta Broca LB 4,2×13mm (cento/milheiro):**  
   Estruturação e união entre montantes verticais e guias horizontais (consumo: 6 parafusos por metro linear de montante):
   ```text
   N_parafusos_LB = Ceil( L_montantes × 6 ) × 1,05
   ```
3. **Fita de Papel Microperfurada ou Fita Telada de Fibra de Vidro (rolos 50m/150m):**  
   Tratamento anti-trinca das juntas entre placas de gesso e forros (consumo: 1,50 metros lineares de fita por m² de drywall):
   ```text
   L_fita_drywall = A_drywall × 1,50 m/m²
   N_rolos_fita_drywall = Ceil( L_fita_drywall / 50,0m ) × 1,05
   ```
4. **Massa Pronta para Tratamento de Juntas de Drywall (baldes 20kg):**  
   Preenchimento e regularização das emendas com fita (consumo normativo: 0,50 kg/m² de placa):
   ```text
   Peso_massa_drywall = A_drywall × 0,50 kg/m²
   N_baldes_massa_drywall = Ceil( Peso_massa_drywall / 20,0kg ) × 1,05
   ```
5. **Banda Acústica Autoadesiva em EVA (rolos 10m):**  
   Isolamento acústico e estanqueidade sob as guias metálicas perimétricas no contato com piso, teto e paredes:
   ```text
   L_banda_acústica = Perímetro_guias_drywall
   N_rolos_banda = Ceil( L_banda_acústica / 10,0m ) × 1,05
   ```

---

## 📐 6. Rodapés, Peitoris e Soleiras (m)

```
Rodapé = Perímetro_interno − Σ Largura_portas − Σ Largura_nichos
Peitoril = Σ Largura_janelas
Soleira = Σ Largura_portas_externas
```

---

## 📐 8. Louças, Metais e Acessórios Sanitários (Matriz por Ambiente × Pavimento Repetido)

> ⚠️ **REGRA DE LOUÇAS E METAIS:** O levantamento de aparelhos sanitários, torneiras, misturadores, cubas e acabamentos de registro DEVE ser realizado em **Matriz de Ambientes por Pavimento Repetido**, multiplicando a quantidade unitária do cômodo pelo multiplicador de repetição da torre.

### 8.1 Categorização Mestra por Família de Equipamentos
| Família | Insumos / Itens Mapeados | Unidade | Aplicação Típica |
|---|---|---|---|
| **LOUÇAS** | Bacia sanitária c/ caixa acoplada, Lavatório c/ coluna, Cuba de embutir, Cuba de sobrepor, Tanque | un | Banheiros, lavabos, suítes, áreas de serviço |
| **CUBAS INOX** | Cuba de aço inox simples, Cuba de aço inox dupla, Tanque de inox | un | Cozinhas, varandas gourmet, lavanderias |
| **METAIS** | Torneira de lavatório, Torneira de pia de cozinha, Misturador monocomando, Ducha higiênica, Chuveiro | un | Pontos de água fria/quente dos ambientes |
| **ACABAMENTOS** | Acabamento de registro de gaveta, Acabamento de registro de pressão, Sifões, Válvulas de escoamento | un | Registros gerais e saídas de esgoto de peças |

### 8.2 Fórmula de Multiplicação Matricial
```text
Qtd_Total_Insumo_k = Σ (Qtd_Unid_Cômodo × N_ambientes_por_andar × N_andares_repetidos)

Exemplo (Bacia c/ Cx Acoplada em Edifício de 16 Andares com 4 Aptos por andar):
  - Banho Social: 1 un/cômodo × 4 aptos/andar × 16 andares = 64 un
  - Lavabo:       1 un/cômodo × 4 aptos/andar × 16 andares = 64 un
  - Total Bacias da Obra = 64 + 64 = 128 unidades
```

---

## 📐 9. Bancadas, Tampos e Divisórias (Mármores, Granitos e Pedras)

> ⚠️ **REGRA DE BANCADAS E PEDRAS:** O levantamento de bancadas de cozinha, tampos de lavatório, balcões e divisórias sanitárias em pedra DEVE ser parametrizado por **Código de Especificação (`CÓD`)**, calculando a área unitária ($m²$) por peça e multiplicando pela repetição nos locais.

### 9.1 Mapeamento por Código de Especificação da Pedra
| Código | Descrição do Insumo | Material / Acabamento | Dimensões Unit. (Comp × Larg) | Área Unitária (m²) |
|---|---|---|---|---|
| **CÓD 1** | Bancada de Banheiro c/ Cuba | Granito Cinza Corumbá 2cm | 1,00m × 1,00m | 1,00 m² |
| **CÓD 2** | Bancada de Cozinha / Copa | Granito Preto São Gabriel 2cm | 1,20m × 0,60m | 0,72 m² |
| **CÓD 3** | Balcão Passa-Prato | Mármore Branco Social | 1,50m × 0,35m | 0,53 m² |
| **CÓD 4** | Divisória Sanitária | Granito Cinza / Granilite 3cm | 1,60m × 0,80m | 1,28 m² |

### 9.2 Fórmulas de Derivação e Consolidação
```text
1. Área Unitária da Peça (m²):
   A_unit = Comprimento × Largura

2. Área Total do Local (m²):
   A_total_local = A_unit × Quantidade_Peças_no_Local

3. Consolidação no Resumo Geral (m²):
   A_acumulada_COD_k = Σ (A_total_local para todas as ocorrências do CÓD k na obra)
```

---

## 📐 7. Impermeabilização

### 7.1 Área Molhada (Banheiro, Sacada, Varanda)

```
A_piso = Comp × Larg
A_arremate = Perímetro_interno × 0,30m
A_impermeab = A_piso + A_arremate
A_final = A_impermeab × (1 + 15% perda)
```

### 7.2 Box de Banheiro

```
A_box_piso = Comp_box × Larg_box
A_box_paredes = Perímetro_box × 1,80m
A_impermeab_box = A_box_piso + A_box_paredes
```

### 7.3 Laje Exposta / Terraço

```
A_impermeab = A_laje + Perímetro × 0,30m (arremate)
A_final = A_impermeab × (1 + 15% perda)
```

- Reservatórios: todas as 6 faces internas (piso + 4 paredes + laje de fundo)
- Piscinas: todas as faces internas + juntas de dilatação

---

## 📐 8. Paredes e Forros de Drywall (Gesso Acartonado)

### 8.1 Paredes de Drywall

```
A_drywall = Comprimento_parede × H_pé-direito
A_final = A_drywall × (1 + 10% perda)
```
> Parede simples = 1 chapa por face (2 chapas por m² linear). Dupla = 2 chapas por face.

**Insumos por m² (parede simples):**

| Insumo | Consumo | Unidade |
|---|---|---|
| Chapa gesso ST 12,5mm (1,20×1,80m) | 2,08 | chapa/m² |
| Montante 48mm (a cada 0,60m) | 1,67 | m/m² |
| Guia 48mm (piso + teto) | 0,67 | m/m² |
| Parafuso drywall | 24 | unid/m² |
| Fita microperfurada | 1,50 | m/m² |
| Massa de rejunte drywall | 0,50 | kg/m² |
| Lã de vidro/rocha (se especificado) | 1,00 | m²/m² |

### 8.2 Forro de Drywall

```
A_forro = Comprimento × Largura
A_final = A_forro × (1 + 10% perda)
```

| Insumo | Consumo | Unidade |
|---|---|---|
| Chapa gesso ST 12,5mm | 1,04 | chapa/m² |
| Perfil canaleta 48mm | 2,50 | m/m² |
| Pendural regulável | 1,00 | unid/m² |
| Parafuso | 12 | unid/m² |

---

## 📦 9. Coeficientes de Consumo TCPO — Arquitetura

### 9.1 Alvenaria — Bloco Cerâmico 9×19×19 (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Blocos cerâmicos 9×19×19 | 25,00 | unid/m² |
| Argamassa de assentamento (1:2:8) | 0,022 | m³/m² |
| Cimento Portland CP II | 3,8 | kg/m² |
| Areia média | 0,018 | m³/m² |

### 9.2 Alvenaria — Bloco Cerâmico 14×19×19 (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Blocos cerâmicos 14×19×19 | 25,00 | unid/m² |
| Argamassa de assentamento (1:2:8) | 0,030 | m³/m² |
| Cimento Portland CP II | 5,2 | kg/m² |

### 9.3 Chapisco (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Cimento CP II | 3,0 | kg/m² |
| Areia grossa | 0,006 | m³/m² |
| Água | 1,2 | L/m² |

### 9.4 Emboço Paulista — esp. 20mm (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Cimento CP II | 5,8 | kg/m² |
| Areia média | 0,030 | m³/m² |
| Cal hidratada | 1,2 | kg/m² |
| Água | 8,5 | L/m² |

### 9.5 Reboco Fino — esp. 5mm (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Cimento branco ou CP II | 2,0 | kg/m² |
| Areia fina peneirada | 0,006 | m³/m² |

### 9.6 Gesso Liso (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Gesso em pó | 2,5 | kg/m² |
| Água | 1,0 | L/m² |

### 9.7 Pintura Látex Acrílico (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Selador acrílico | 0,10 | L/m² |
| Tinta látex 1ª demão | 0,13 | L/m² |
| Tinta látex 2ª demão | 0,13 | L/m² |
| **Total tinta** | **0,26** | **L/m²** |

### 9.8 Contrapiso — esp. 50mm (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Cimento CP II | 9,0 | kg/m² |
| Areia grossa | 0,038 | m³/m² |
| Água | 12,0 | L/m² |

### 9.9 Massa Corrida PVA (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Massa corrida PVA (1ª demão) | 0,50 | kg/m² |
| Massa corrida PVA (2ª demão) | 0,40 | kg/m² |
| **Total (2 demãos)** | **0,90** | **kg/m²** |
| Lixa grão 150 | 0,10 | folha/m² |

### 9.10 Argamassa Colante para Cerâmica/Porcelanato (por m²)

| Tipo | Consumo | Aplicação |
|---|---|---|
| AC-I | 5,0 kg/m² | Pisos internos, áreas secas |
| AC-II | 5,0 kg/m² | Pisos externos, áreas úmidas, fachadas |
| AC-III | 5,0 kg/m² | Porcelanatos grandes, fachadas altas |
| AC-IIIE | 5,0 kg/m² | Lajes aquecidas, fachadas |

> **Dupla colagem** (peças ≥ 60×60cm ou fachadas): **10,0 kg/m²**

### 9.11 Rejunte para Cerâmica/Porcelanato (por m²)

| Peça | Junta | Consumo |
|---|---|---|
| Cerâmica até 30×30cm | 3mm | 0,50 kg/m² |
| Cerâmica 45×45cm | 3mm | 0,35 kg/m² |
| Porcelanato 60×60cm | 2mm | 0,25 kg/m² |
| Porcelanato 80×80cm+ | 2mm | 0,20 kg/m² |
| Cerâmica de parede 30×60cm | 2mm | 0,30 kg/m² |

### 9.12 Assentamento de Piso — Composição Completa (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Piso cerâmico/porcelanato | 1,00 | m²/m² (+ taxa perda §2.2) |
| Argamassa colante | 5,0 (ou 10,0 dupla colagem) | kg/m² |
| Rejunte | conforme §9.11 | kg/m² |
| Espaçador (cruzeta) | 6,0 | unid/m² |

### 9.13 Textura Acrílica / Grafiato — Acabamento Externo (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Textura acrílica lisa (rolo) | 1,0 | kg/m² |
| Textura acrílica projetada | 2,5 | kg/m² |
| Grafiato (textura riscada) | 2,5 | kg/m² |
| Selador acrílico (base) | 0,10 | L/m² |

### 9.14 Impermeabilização (por m²)

| Tipo | Consumo | Unidade |
|---|---|---|
| Manta asfáltica 3mm (c/ feltro) | 1,20 | m²/m² (sobreposição 10cm) |
| Manta asfáltica 4mm (c/ feltro) | 1,20 | m²/m² (sobreposição 10cm) |
| Primer asfáltico (imprimação) | 0,40 | L/m² |
| Argamassa polimérica (2 demãos) | 3,0 | kg/m² |
| Tela de poliéster (reforço) | 1,10 | m²/m² (sobreposição 5cm) |

---

## 🌳 10. Árvore de Decisão — Arquitetura

| Pedido do Usuário | Ação do Agente | Seção |
|---|---|---|
| "Quantifique o revestimento de parede do banheiro" | Solicitar: Comp, Larg, H, vãos (porta/janela: L×H), tipo de revestimento | §1 |
| "Quantifique o piso da cozinha" | Solicitar: Comp, Larg, geometria, tipo de piso, peças de pilares embutidos | §2 + §9.10–9.12 |
| "Quantifique o teto da sala" | Solicitar: Comp, Larg, tipo de acabamento (gesso/pintura/drywall) | §3 |
| "Quantifique a impermeabilização do banheiro" | Solicitar: Comp, Larg, Perímetro, se tem box (dim do box) | §7.1 + §7.2 + §9.14 |
| "Paredes de drywall da área gourmet" | Solicitar: comprimento de cada parede, pé-direito, simples/dupla | §8.1 |
| "Quantifique a cobertura" | Solicitar: área projetada em planta, inclinação (°), tipo de telha | §4 |
| "Quantifique a alvenaria do apartamento" | Para cada ambiente: Comp, Larg, H, vãos — calcular §1 e aplicar §9.1/9.2 | §1 + §9.1 |
| "Quantifique a pintura de toda a obra" | Paredes (§1) + Teto (§3) → aplicar coef. pintura §9.7 | §1+§3+§9.7 |

---

## 🏗️ 11. Muros de Divisa, Fechamentos Perimetrais, Portões de Acesso e Pavimentação Externa

### 11.1 Muros de Divisa e Fechamentos Perimetrais
- **Estrutura e Alvenaria do Muro (por metro linear $L_{\text{muro}}$):**
  - `Escavação de Baldrame / Sapata do Muro (m³):` $V_{\text{escav}} = L_{\text{muro}} \times B_{\text{sapata}} \times H_{\text{cava}}$.
  - `Viga Baldrame / Sapata de Concreto Armado (m³ / m² / kg):` Concreto C25/C30 ($m³$) + Fôrma ($m²$) + Aço CA-50 ($kg$).
  - `Alvenaria de Vedação / Estrutural do Muro (m²):` $A_{\text{muro}} = L_{\text{muro}} \times H_{\text{muro}}$ (Blocos de concreto ou cerâmicos $14\times19\times39cm$).
  - `Pilaretes de Travamento do Muro (unid ou m³):` Pilaretes de concreto armado a cada $2,50m$ a $3,00m$ ($0,14 \times 0,19 \times H_{\text{muro}}$).
  - `Cinta de Coroamento Superior (m³ / m² / kg):` Cinta em bloco canaleta no topo do muro.
  - `Chapim / Pingadeira de Concreto / Rufo Metálico (m):` Proteção contra infiltração de topo do muro.
  - `Revestimento do Muro (Chapisco + Emboço + Pintura Acrílica / Textura - m²):` $A_{\text{revest}} = 2 \times A_{\text{muro}}$ (ambas as faces, quando couber).
  - `Concertina / Cerca Elétrica de Segurança (m):` Lança concertina dupla espiral $\varnothing 30cm / 45cm$ ou cerca elétrica 6 fios c/ hastes de alumínio.

### 11.2 Portões de Acesso de Veículos e Pedestres
- **Portões de Veículos e Automação:**
  - `Portão de Veículos Basculante / Deslizante / Pivotante (m² ou unid):` Estrutura em alumínio anodizado / aço galvanizado c/ pintura eletrostática epóxi.
  - `Motor Automatizador de Portão Rápido (unid):` Motor cremalheira / fuso de alta frequência ($1/3\text{ HP}$ ou $1/2\text{ HP}$) c/ placa de comando inverter, fotoelétrica de segurança e controles remotos.
  - `Cancela Automatizada de Garagem (unid):` Cancela c/ haste articulada/reta $3m$ a $4m$ para controle de fluxo de garagem.
- **Portões de Pedestres e Controle de Acesso de Guarita:**
  - `Portão Social de Pedestres (unid ou m²):` Portão metálico/alumínio c/ fechadura eletroímã / e-Lock de embutir $150kgf / 280kgf$.
  - `Catracas / Torniquetes de Acesso (unid):` Catraca pedestal inox / torniquete de altura inteira c/ leitor de biometria / reconhecimento facial / leitor de Tag RFID e comutador de pânico.

### 11.3 Pavimentação Externa, Passeios e Meio-Fio
- `Regularização e Compactação de Solo de Passeio (m²):` Preparação de leito com sapo/compactador mecânico.
- `Sub-base de Brita Graduada Simples - BGS (m³):` Camada de base drenante e estrutural ($e=10cm$ a $20cm$).
- `Piso Intertravado de Concreto / Paver (m²):` Blocos retangulares/holandeses/sextavados ($e=6cm$ para pedestres / $e=8cm$ para veículos) + colchão de assentamento de areia/pó de pedra ($e=5cm$).
- `Guia / Meio-fio de Concreto Pré-moldado (m):` Guias de concreto reto ou curvo Padrão Prefeitura ($15\times30\times100cm$).
- `Sarjeta de Concreto Moldada in loco (m):` Sarjeta em concreto C20 ($L=30cm$, $e=8cm$).
- `Piso Tátil Alerta e Direcional (m² ou m):` Placas cimentícias ou de PVC auto-adesivo $25\times25cm$ / $30\times30cm$ conforme norma ABNT NBR 9050 (acessibilidade).
