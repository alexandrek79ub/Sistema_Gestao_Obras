# 🔍 SKILL MÓDULO: Auditoria, Verificação e Correção de Quantitativos

> **Finalidade:** Esta skill é o **Filtro Anti-Erro de Leitura e Auditoria de Orçamento**. Ela deve ser executada obrigatoriamente **APÓS** qualquer levantamento quantitativo de projetos em PDF, antes de entregar a memória de cálculo ou salvar o orçamento no banco de dados.

---

## 🎯 Objetivo Principal
Garantir zero erros de leitura visual de pranchas, proibir deduções matemáticas equivocadas (como confundir espessura de parede com espessura de laje), impor a Geometria Líquida Executiva e validar se todas as regras da **[SKILL_QUANTIFICACAO_MASTER.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANTIFICACAO_MASTER.md)** foram rigorosamente seguidas.

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
  $$\text{Comprimento Líquido} = (2 \times L_{\text{ext.long.}}) + 2 \times (L_{\text{ext.transv.}} - 2 \times e_{\text{peça}})$$
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
- [ ] **Pintura Externa da Fachada (Envelope):** A área de pintura externa foi calculada sobre o **envelope externo bruto total** `2 × (Comp_ext + Larg_ext) × H_fachada`, descontando os vãos de esquadrias externas.

---

## 🛑 Red Flags — Erros Críticos que Cancelam a Emissão do Quantitativo

Se o relatório contiver qualquer um destes erros, a verificação **REPROVA** o levantamento e exige correção imediata:

1. ❌ Usar cota de topo de laje em vez de cota de fundo para calcular altura livre de pilares.
2. ❌ Confundir espessura de alvenaria (ex: 14cm) com espessura de laje (ex: 12cm).
3. ❌ Calcular vigas/cintas fechadas pelo perímetro de eixos sem desmembrar a espessura dos cantos.
4. ❌ Apresentar resultado numérico sem a notação limpa de engenharia (com caracteres de programação/LaTeX).
5. ❌ Omitir a fórmula ou as cotas lidas da prancha na memória de cálculo.

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
====================================================================
 STATUS: LEVANTAMENTO AUDITADO E LIBERADO PARA O ORÇAMENTO BASE
====================================================================
```
