# 🔍 SKILL MÓDULO: Auditoria, Verificação e Correção de Quantitativos

> **Pré-requisito obrigatório:** Antes de aplicar esta skill, leia `SKILL_QUANTIFICACAO_MASTER.md` e siga o fluxo, as responsabilidades e as regras universais definidos nele. Esta skill complementa o MASTER e não substitui suas diretrizes.

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

- [ ] **Separação por Tipologia de Prancha:** Pranchas de Detalhes Estruturais (armação, cortes de peças isoladas) respondem estritamente por Concreto Estrutural, Fôrmas e Aço CA-50/CA-60. A movimentação de terra (escavação, lastro, reaterro, bota-fora) só pode ser aprovada se confrontada e ancorada na **Planta de Locação/Geometria de Fundações** e nas cotas do **Platô de Terraplenagem**. *PROIBIDO calcular cavas no vácuo de pranchas de detalhes de armadura.*
- [ ] **Separação de Elementos:** A espessura usada no cálculo da laje pertence à laje (`h_laje`), e a espessura usada na parede pertence à parede (`esp_parede`). *PROIBIDO usar espessura de alvenaria em cálculo estrutural ou vice-versa.*
- [ ] **Leitura de Níveis (Cotas de Fôrma):** A cota de fundo de laje/viga é a cota direta de fôrma indicada na prancha (`EL. de fôrma`). *PROIBIDO deduzir fundo via `(cota_topo − espessura)` se houver a cota direta no desenho.*
- [ ] **Consistência de Unidades:** Cotas em centímetros (ex: 892 cm, 540 cm) foram convertidas corretamente para metros (8,92m e 5,40m) mantendo a precisão de 2 casas decimais.

---

## 📐 2. Checklist 2 — Geometria Líquida Executiva (Desconto de Cantos e Encontros)

Para vigas baldrame, cintas, vigas de teto e paredes perimétricas:

- [ ] **Interferência Cava de Sapata × Vala de Baldrame:** Se houver vigas baldrames interligando sapatas ou blocos de coroamento, a escavação da vala do baldrame desconta a área da cava da sapata (ou vice-versa), eliminando duplicidade na medição de escavação, reaterro e bota-fora.
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

## 📦 4. Checklist 4 — Blindagem de Geometria Líquida Nominal (Zero Perdas e Zero Insumos Avulsos)

Para o levantamento físico de engenharia:

- [ ] **Zero Aplicação de Perdas:** O quantitativo reflete 100% a geometria nominal do projeto. Nenhuma taxa empírica de perda de concreto, aço, fôrma, argamassa ou empolamento de terra foi embutida.
- [ ] **Zero Insumos Miúdos / Secundários:** É proibido explodir miudezas (arames, pregos, sarrafos, desmoldantes, espaçadores, fitas, tintas avulsas). Esses insumos já constam das Composições de Preço Unitário (CPUs/SINAPI).
- [ ] **Armadura Fiel às Pranchas:** O peso de aço CA-50 / CA-60 foi extraído diretamente das tabelas/resumos de ferro de projeto, sem taxas estimadas de consumo.

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
- [ ] **Mapeamento de Chamadas de Detalhes:** Todas as pranchas de detalhes (callouts) foram rastreadas e vinculadas aos serviços executivos correspondentes.
- [ ] **Fidelidade Físico-Executiva:** Todos os serviços necessários à execução integral da disciplina foram contemplados em seus respectivos pacotes de trabalho da EAP, sem aglutinações indevidas.
- [ ] **Interrogatório Técnico (Instrução Ausente na Skill):** Se algum detalhe ou especificação da prancha **não possuir regra direta ou instrução explícita nas Skills**, o agente **PAROU O LEVANTAMENTO E PERGUNTOU AO USUÁRIO** para definir a premissa antes de prosseguir. *PROIBIDO CHUTAR OU ASSUMIR SOBERANAMENTE.*
- [ ] **Auditoria de Omissões de Desenho & Proibição de Estimativas:** Nenhum item ausente ou sem cota nas pranchas foi estimado ou arbitrado. Para 100% dos elementos sem cota, corte ou especificação no projeto, consta obrigatoriamente a observação formal na memória de cálculo: `[NÃO LEVANTADO POR FALTA DE INFORMAÇÃO NO DESENHO]` com identificação da prancha e pendência técnica (RFI) aberta.

---

## 📋 7. Checklist 7 — Alinhamento dos Serviços da EAP e Rastreabilidade Física

> 🛑 **REGRA CRÍTICA:** Todo levantamento de quantitativos deve estar 100% ancorado nos pacotes de serviços executivos da EAP física da obra.

Para cada disciplina presente no levantamento, verificar se os critérios executivos foram atendidos:

- [ ] **Mapeamento EAP:** Todos os serviços levantados possuem códigos e pacotes de trabalho alinhados à EAP (níveis 1.1 a 5.1).
- [ ] **Geometria Líquida Nominal:** O quantitativo é estritamente geométrico, sem aplicação de perdas ou coeficientes de consumo adicionais.
- [ ] **Memória de Cálculo Completa:** Cada linha da tabela de serviços possui fórmula algébrica auditável correspondente.
- [ ] **Zero Insumos Miúdos / Secundários:** Não foram geradas linhas avulsas para arames, pregos, sarrafos, desmoldantes, espaçadores ou consumíveis (itens embutidos nas composições SINAPI/CPU).
- [ ] **Travas de Qualidade e Predecessoras:** As interdependências críticas (ex: impermeabilização antes do reaterro, teste hidrostático antes do reboco) estão registradas.

---

## 🛑 Red Flags — Erros Críticos que Cancelam a Emissão do Quantitativo

Se o relatório contiver qualquer um destes erros, a verificação **REPROVA** o levantamento e exige correção imediata:

1. ❌ Usar cota de topo de laje em vez de cota de fundo para calcular altura livre de pilares.
2. ❌ Confundir espessura de alvenaria (ex: 14cm) com espessura de laje (ex: 12cm).
3. ❌ Calcular vigas/cintas fechadas pelo perímetro de eixos sem desmembrar a espessura dos cantos.
4. ❌ Apresentar resultado numérico sem a notação limpa de engenharia (com caracteres de programação/LaTeX).
5. ❌ Omitir a fórmula ou as cotas lidas da prancha na memória de cálculo.
6. ❌ Apresentar quantitativos com taxas de perda embutidas ou insumos miúdos explodidos na tabela de serviços.
7. ❌ **Quantificar qualquer item com base em estimativa, suposição ou média paramétrica sem respaldo direto no desenho.**
8. ❌ **Omitir a observação obrigatória na memória de cálculo informando que o item NÃO foi levantado por falta de informação no desenho.**
9. ❌ **Emitir Quantitativo sem a Tabela de Serviços / EAP** — levantamento sem mapeamento de serviços da EAP é documento incompleto.
10. ❌ **Linha da Tabela de Serviços sem memória de cálculo correspondente** (linha órfã).

---

## 📝 Protocolo de Emissão do Certificado de Auditoria de Quantitativos

Após a verificação, o Agente de Auditoria deve emitir o seguinte bloco no relatório. O bloco é um modelo vazio: nenhuma obra pode ser marcada como APROVADA sem evidências, revisão da prancha e identificação da obra/revisão.

```text
====================================================================
      CERTIFICADO DE AUDITORIA E VERIFICAÇÃO DE QUANTITATIVOS
====================================================================
 [x] Checklist 1 — Rastreabilidade de Cotas & Níveis: APROVADO
 [x] Checklist 2 — Geometria Líquida Executiva (Sem Duplicidade): APROVADO
 [x] Checklist 3 — Interface Pilar-Laje-Viga (Face Inferior): APROVADO
 [x] Checklist 4 — Geometria Líquida Nominal (Zero Perdas e Sem Insumos Avulsos): APROVADO
 [x] Checklist 5 — Alvenaria e Revestimentos Externos: APROVADO
 [x] Checklist 6 — Varredura 360° de Pranchas e Interrogatório Técnico: APROVADO
 [x] Checklist 7 — Alinhamento dos Serviços da EAP e Rastreabilidade Física: APROVADO
 [x] Memória de Cálculo: toda linha de serviço rastreada para sua expressão algébrica: APROVADO
 [x] Tabela de Serviços / EAP gerada: APROVADO
====================================================================
 STATUS: LEVANTAMENTO AUDITADO E LIBERADO PARA O ORÇAMENTO BASE
====================================================================
```

---

## 🚀 Próximo Passo: Ingestão no SQLite Oficial e Compilação dos Artefatos

Com o certificado de auditoria emitido e o JSON estruturado validado:
1. **Executar a ingestão no SQLite SSOT:**
   ```bash
   python scripts/motor_quantitativos/cli.py caminho/para/dados_obra.json
   ```
2. **Artefatos Derivados Compilados Automaticamente:**
   - 📊 `ORCAMENTO_BASE_CONSOLIDADO.xlsx` (Caderno Master com 6 abas e fórmulas dinâmicas)
   - 📑 `ORCAMENTO_BASE_CONSOLIDADO.csv` e `QUANTITATIVO_MESTRE.csv`
   - 📝 `MEMORIA_CALCULO_[DISCIPLINA].md` com checksum SHA-256 e rastreabilidade absoluta


