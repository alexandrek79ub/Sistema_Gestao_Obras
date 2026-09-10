# 🔍 SKILL MÓDULO: Auditoria, Verificação e Correção de Quantitativos

> **Finalidade:** Esta skill é o **Filtro Anti-Erro de Leitura e Auditoria de Orçamento**. Ela deve ser executada obrigatoriamente **APÓS** qualquer levantamento quantitativo de projetos em PDF, antes de entregar a memória de cálculo ou salvar o orçamento no banco de dados.

---

## 🎯 Objetivo Principal
Garantir zero erros de leitura visual de pranchas, proibir deduções matemáticas equivocadas (como confundir espessura de parede com espessura de laje), impor a Geometria Líquida Executiva e validar se todas as regras da **[SKILL_QUANTIFICACAO_MASTER.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANTIFICACAO_MASTER.md)** foram rigorosamente seguidas.

> 🔄 **Protocolo Obrigatório de Carga Dinâmica (SSOT):**  
> Ao auditar qualquer disciplina (Fundações, Estrutura, Arquitetura, Elétrica ou Hidráulica), o Agente DEVE obrigatoriamente carregar **esta Skill de Auditoria + a Skill Específica da Disciplina** (ex: `SKILL_QUANT_01_FUNDACOES.md`). A verificação confronta a memória de cálculo contra os 6 checklists de QA universais **E** contra as regras de negócio específicas daquela disciplina.

---

## 🔁 O Loop de QA de Quantificação (5 Etapas de Verificação)

```
 [1. Leitura Inicial do Projeto] ──► [2. Cálculo dos Quantitativos]
                                              │
                                              ▼
 [5. Aprovação e Emissão CSV] ◄── [4. Ajuste & Correção] ◄── [3. Loop de Auditoria (Skill Auditoria)]
```

---

## 📋 1. Checklist 1 — Rastreabilidade de Cotas e Níveis (Anti-Confusão de Pranchas)

Antes de aprovar qualquer dimensão ou altura:

- [ ] **Separação de Elementos:** A espessura usada no cálculo da laje pertence à laje (`h_laje`), e a espessura usada na parede pertence à parede (`esp_parede`). *PROIBIDO usar espessura de alvenaria em cálculo estrutural ou vice-versa.*
- [ ] **Leitura de Níveis (Cotas de Fôrma):** A cota de fundo de laje/viga é a cota direta de fôrma indicada na prancha (`EL. de fôrma`). *PROIBIDO deduzir fundo via `(cota_topo − espessura)` se houver a cota direta no desenho.*
- [ ] **Consistência de Unidades:** Cotas em centímetros (ex: 892 cm, 540 cm) foram convertidas corretamente para metros (8,92m e 5,40m) mantendo a precisão de 2 casas decimais.

---

## 📐 2. Checklist 2 — Geometria Líquida Executiva (Desconto de Cantos e Encontros)

Para vigas baldrame, cintas, vigas de teto e paredes perimétricas:

- [ ] **Desmembramento de Cantos:** O comprimento total NÃO foi calculado por simples soma de eixos (`2×C + 2×L`).
- [ ] **Fórmula da Geometria Executiva Aplicada:**
  `Comprimento Líquido = (2 × L_ext.long.) + 2 × (L_ext.transv. - 2 × e_peça)`
- [ ] **Zero Duplicidade:** O concreto e a fôrma dos 4 cantos de interseção foram contados exatamente 1 única vez.

---

## 🏗️ 3. Checklist 3 — Interface Pilar × Laje × Viga (Sem Dupla Contagem)

Para pilares, pilaretes e elementos verticais:

- [ ] **Altura Livre Correta:** A altura do pilar/pilarete foi medida da **cota superior do piso** até a **face INFERIOR (fundo) da laje ou viga**.
- [ ] **Concreto da Laje:** A espessura da laje é quantificada inteira no item de laje, sem sobreposição com o topo do pilar.
- [ ] **Vigas Invertidas:** Se a viga é invertida (projetada para cima da laje), a altura livre do pilar vai até o fundo da laje. Se a viga for pendente (para baixo), a altura vai até o fundo da viga.

---

## 📦 4. Checklist 4 — Unidade Comercial de Compra (UCC) e Arredondamento

Para a Tabela de Insumos de Compra:

- [ ] **Arredondamento Comercial:** Todos os insumos contáveis (blocos, sacos de cimento/argamassa, latas de tinta, rolos de manta) foram arredondados **para CIMA** para números inteiros.
- [ ] **Barras de Aço:** O peso de aço foi convertido para metros de barras de **12 metros** (para vergalhões) ou rolos.
- [ ] **Taxa de Perda Transparente:** A taxa de perda aplicada está explicitamente descrita na memória de cálculo.

---

## 🎨 5. Checklist 5 — Alvenaria e Revestimentos Externos (Fachadas)

Para alvenaria de vedação e pinturas de fachada:

- [ ] **Desconto de Pilares em Alvenaria:** O volume/área de alvenaria descontou a largura de todos os pilares de concreto embutidos (`Σ b_pilar × H`), pois não há blocos/tijolos onde existe pilar executado.
- [ ] **Desconto de Interseções de Canto de Alvenaria:** A alvenaria perimétrica descontou as 2 espessuras de parede (`2 × e_parede`) no sentido transversal para não duplicar blocos nos 4 cantos.
- [ ] **Pintura Externa da Fachada (Perímetro Bruto):** A área de pintura externa foi calculada sobre o **perímetro bruto externo total da fachada** `2 × (Comp_ext + Larg_ext) × H_fachada`, descontando os vãos de esquadrias externas.

---

## 🔎 6. Checklist 6 — Varredura 360° de Pranchas e Interrogatório Técnico (Regra Universal)

Para garantir zero omissão de detalhes construtivos em qualquer disciplina:

- [ ] **Varredura 100% da Prancha:** Todas as áreas da prancha (plantas baixas, cortes, elevações, quadros de notas, esquemas unifilares/isométricos e detalhes 01 a N) foram varridas exaustivamente. Nenhum detalhe foi esquecido ou omitido.
- [ ] **Mapeamento de Chamadas de Detalhes:** Todas as pranchas de detalhes (callouts) foram rastreadas e vinculadas aos insumos/serviços correspondentes.
- [ ] **Cadeia Completa de Insumos e Miudezas Executivas (Proibição Absoluta de Omissão de Almoxarifado):** Todos os elementos secundários e insumos de apoio de canteiro (desmoldantes de fôrma, pregos, sarrafos de travamento/gravatas, lona plástica de cura/fundo de vala, rolos/trinchas de pintura asfáltica, arame recozido, espaçadores, pingadeiras, rufos, calhas, ralos, conexões, caixas, disjuntores) foram quantificados em 100% de detalhamento granular para compra (UCC). *Nota de Governança:* As miudezas constam na **Tabela de Compras UCC / BOM** vinculadas ao serviço, e **NÃO DEVEM poluir a numeração de pacotes de trabalho da EAP física**. **SE HOUVER OMISSÃO DE MIUDEZAS NA LISTA DE COMPRAS, A AUDITORIA REPROVA O LEVANTAMENTO.**
- [ ] **Interrogatório Técnico (Instrução Ausente na Skill):** Se algum detalhe ou especificação da prancha **não possuir regra direta ou instrução explícita nas Skills**, o agente **PAROU O LEVANTAMENTO E PERGUNTOU AO USUÁRIO** para definir a premissa antes de prosseguir. *PROIBIDO CHUTAR OU ASSUMIR SOBERANAMENTE.*
- [ ] **Auditoria de Omissões de Desenho & Proibição de Estimativas:** Nenhum item ausente ou sem cota nas pranchas foi estimado ou arbitrado. Para 100% dos elementos sem cota, corte ou especificação no projeto, consta obrigatoriamente a observação formal na memória de cálculo: `[NÃO LEVANTADO POR FALTA DE INFORMAÇÃO NO DESENHO]` com identificação da prancha e pendência técnica (RFI) aberta.

---

## 🛒 7. Checklist 7 — Varredura de Kits de Miudezas por Disciplina (Anti-Falta de Almoxarifado)

> 🛑 **REGRA CRÍTICA:** A omissão de qualquer miudeza na Lista de Compras (BOM) causa paralisamento de frente de serviço em obra. Este checklist é obrigatório e deve ser executado antes de emitir o quantitativo final.

Para cada disciplina presente no levantamento, verificar se o Kit de Miudezas correspondente foi integralmente aplicado:

**Alvenaria (SKILL_QUANT_03A §1.6 + §1.8):**
- [ ] Telas metálicas galvanizadas 15×50cm de amarração pilar-alvenaria
- [ ] Pinos de aço c/ arruela cônica + cartuchos de pólvora para finca-pinos
- [ ] Adesivo plastificante para chapisco (0,20 L/m²)
- [ ] **Espuma de Poliuretano Expansiva PU 750ml** para encunhamento no topo das paredes
- [ ] Insumos de argamassa de assentamento (cimento CP II, cal hidratada, areia média) convertidos em sacos/m³
- [ ] Checklist §1.8 da SKILL_QUANT_03A percorrido e assinado

**Pinturas (SKILL_QUANT_03A §5):**
- [ ] Selador acrílico base água (0,10 L/m² de reboco novo)
- [ ] Lixa grossa grão 80/100 (0,05 folha/m² de reboco)
- [ ] Lixa fina grão 150/220 (0,10 folha/m² de massa/gesso)
- [ ] Fita crepe 24mm×50m para proteção de rodapés e caixilhos
- [ ] Lona plástica preta para proteção de pisos assentados (bobinas 100m²)

**Pisos / Revestimentos Cerâmicos (SKILL_QUANT_03B §6):**
- [ ] Cimentcola AC-I/II/III (tipo correto por área seca/úmida/dupla colagem)
- [ ] Rejunte flexível (consumo varia por formato e largura de junta)
- [ ] Espaçadores / cruzetas plásticas (6 un/m²)
- [ ] Clips niveladores (obrigatórios para porcelanato ≥60×60cm)
- [ ] Cunhas niveladoras reutilizáveis (30% dos clips)
- [ ] Primer de contato acrílico (substratos novos e porosos)

**Esquadrias (SKILL_QUANT_03B §2.3):**
- [ ] Dobradiças aço inox 3½"×3" (3 por folha de abrir)
- [ ] Fechaduras completas (máquina + cilindro + maçaneta)
- [ ] Batedores de porta de piso c/ amortecedor inox
- [ ] Espuma PU 750ml para marcos (1 tubo a cada 2,5 portas)
- [ ] Parafusos + buchas nylon S8 para batentes (8/porta)
- [ ] Pregos s/ cabeça 12×12 para alizares (20/vão)
- [ ] Cola branca PVA D3 (1 frasco de 500g a cada 8 portas)
- [ ] Selante PU 40 / silicone neutro para caixilhos externos

**Impermeabilização (SKILL_QUANT_03B §1.5):**
- [ ] Primer asfáltico base solvente (0,40 L/m² de manta)
- [ ] Tela de poliéster / véu de fibra de vidro (reforço de cantos e ralos)
- [ ] Fita asfáltica autoadesiva aluminizada (rolos 10m) para juntas e emendas
- [ ] Gás GLP P-13 para maçarico de manta asfáltica (1 botijão/50m²)

**Cobertura (SKILL_QUANT_03C):**
- [ ] Parafusos autobrocantes c/ arruela EPDM (4,5 un/m² real inclinado)
- [ ] Parafusos de costura c/ arruela EPDM (emendas longitudinais)
- [ ] Fita de vedação butílica autoadesiva (transpasse de telhas e calhas)
- [ ] Chumbadores / parabolts para terças metálicas (2/apoio)
- [ ] Rebites de repuxo em alumínio para calhas e rufos
- [ ] Selante PU 40 para calafetação de calhas, rufos e emendas

---

## 🛑 Red Flags — Erros Críticos que Cancelam a Emissão do Quantitativo

Se o relatório contiver qualquer um destes erros, a verificação **REPROVA** o levantamento e exige correção imediata:

1. ❌ Usar cota de topo de laje em vez de cota de fundo para calcular altura livre de pilares.
2. ❌ Confundir espessura de alvenaria (ex: 14cm) com espessura de laje (ex: 12cm).
3. ❌ Calcular vigas/cintas fechadas pelo perímetro de eixos sem desmembrar a espessura dos cantos.
4. ❌ Apresentar resultado numérico sem a notação limpa de engenharia (com caracteres de programação/LaTeX).
5. ❌ Omitir a fórmula ou as cotas lidas da prancha na memória de cálculo.
6. ❌ Apresentar quantitativos resumidos, agrupados ou sintetizados omitindo conexões, caixas, disjuntores ou micro-componentes.
7. ❌ **Quantificar qualquer item com base em estimativa, suposição ou média paramétrica sem respaldo direto no desenho.**
8. ❌ **Omitir a observação obrigatória na memória de cálculo informando que o item NÃO foi levantado por falta de informação no desenho.**
9. ❌ **Emitir Tabela Consolidada sem a Tabela de Serviços / EAP** — lista de compras sem mapeamento de serviços é documento incompleto e não pode ser usado para cronograma ou contratos de empreitada.
10. ❌ **Linha da Tabela Consolidada sem memória de cálculo correspondente** (linha órfã) — todo insumo na BOM deve ter expressão algébrica documentada na Seção 1.
11. ❌ **Fechar a BOM sem percorrer o Checklist 7 de miudezas** — a omissão de kits de miudezas implica em reprovação automática da auditoria.


---

## 📝 Protocolo de Emissão do Certificado de Auditoria de Quantitativos

Após a verificação, o Agente de Auditoria deve emitir o seguinte bloco no relatório:

```text
====================================================================
      CERTIFICADO DE AUDITORIA E VERIFICAÇÃO DE QUANTITATIVOS
====================================================================
 [x] Checklist 1 — Rastreabilidade de Cotas & Níveis: APROVADO
 [x] Checklist 2 — Geometria Líquida Executiva (Sem Duplicidade): APROVADO
 [x] Checklist 3 — Interface Pilar-Laje-Viga (Face Inferior): APROVADO
 [x] Checklist 4 — Conversão UCC e Arredondamentos: APROVADO
 [x] Checklist 5 — Blindagem Anti-Estimativa e Registro de Omissões de Projeto: APROVADO
 [x] Checklist 6 — Varredura 360° de Pranchas e Interrogatório Técnico: APROVADO
 [x] Checklist 7 — Varredura de Kits de Miudezas por Disciplina: APROVADO
 [x] Memória de Cálculo: toda linha da BOM rastreada para sua expressão algébrica: APROVADO
 [x] Tabela de Serviços / EAP gerada e vinculada à BOM: APROVADO
====================================================================
 STATUS: LEVANTAMENTO AUDITADO E LIBERADO PARA O ORÇAMENTO BASE
====================================================================
```
