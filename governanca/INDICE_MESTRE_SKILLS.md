# 🗂️ ÍNDICE MESTRE DAS SKILLS

Documento de navegação — não ensina nada novo, resolve qual skill consultar pra cada tipo de
pergunta/situação, e destrava conflito quando duas skills tocam o mesmo tema.

> Inserir referência a este índice no topo do `agents.md`: antes de aplicar qualquer skill, o
> agente consulta este mapa pra confirmar que está na skill certa, e nas notas de sobreposição
> quando mais de uma se aplica.

---

## 1. Mapa de Consulta por Situação

| Se a pergunta/situação é sobre... | Consultar |
|---|---|
| Levantamento de quantidade a partir de PDF/CAD | `SKILL_QUANTIFICACAO_MASTER.md` |
| Pedido de compra novo | `SKILL_QUANTIFICACAO_PEDIDO_DE_COMPRA.md` |
| Nota fiscal chegando, com ou sem pedido vinculado | `SKILL_QUANTIFICACAO_CONCILIACAO_3_PONTAS.md` |
| Relatório de EVM (SPI/CPI), status geral da obra | `SKILL_GESTAO_06_RELATORIOS.md` |
| Qualquer projeção, tendência, correlação, ou "por que isso aconteceu" | `SKILL_GESTAO_07_CIENCIA_DE_DADOS.md` (rigor obrigatório, não é opcional) |
| Produtividade (RUP), efetivo, desperdício, ciclo de melhoria | `SKILL_GESTAO_08_PRODUTIVIDADE_E_RECURSOS.md` |
| Caixa disponível, quando pagar, quando recebe | `SKILL_GESTAO_09_FLUXO_DE_CAIXA.md` |
| Aditivo de contrato, retenção de garantia | `SKILL_GESTAO_10_CONTRATOS.md` |
| Retrabalho, defeito de execução | `SKILL_GESTAO_11_QUALIDADE_NAO_CONFORMIDADE.md` |
| Fim de obra, as-built, entrega ao cliente | `SKILL_GESTAO_12_ENCERRAMENTO_DE_OBRA.md` |
| Risco futuro, ainda não materializado | `SKILL_GESTAO_13_MATRIZ_DE_RISCO.md` |
| Versão de projeto, revisão de documento | `SKILL_GESTAO_14_CONTROLE_DE_REVISAO.md` |
| Relatório/comunicação formal ao cliente/contratante | `SKILL_GESTAO_15_COMUNICACAO_CLIENTE.md` |
| O que o agente pode decidir sozinho vs. o que pausa | `ADENDO_AGENTS_REGRAS_DE_AUTONOMIA.md` — **sempre consultar em paralelo**, nunca isolado |
| Reprogramação de cronograma, gatilho de SPI sustentado | `SKILL_GESTAO_16_CRONOGRAMA_E_REPROGRAMACAO.md` |
| Plano de ataque / recuperação de prazo | `SKILL_GESTAO_16_CRONOGRAMA_E_REPROGRAMACAO.md` |
| Vencimento de PGR, PCMSO, LTCAT, ASO ou CA de EPI | `SKILL_GESTAO_17_VENCIMENTO_DOCUMENTAL_SEGURANCA.md` |
| Trabalhador / empreiteira com documento de segurança vencido | `SKILL_GESTAO_17_VENCIMENTO_DOCUMENTAL_SEGURANCA.md` — prioridade máxima |
| Custo unitário de serviço, composição SINAPI/cotação, BDI | `SKILL_QUANTIFICACAO_COMPOSICAO_PRECO.md` — acionar sempre após levantamento para fechar o orçamento |
| Informação faltante na prancha que bloqueia o quantitativo | `SKILL_ENGENHARIA_RFI.md` — abrir RFI antes de qualquer estimativa |
| Acompanhar RFIs em aberto, prazo vencido, resposta de projetista | `SKILL_ENGENHARIA_RFI.md` |
| Qual POP executar antes de liberar um serviço de campo | `SKILL_PRODUCAO_POP_BRIDGE.md` — consultar junto com SKILL_GESTAO_02 |
| Cockpit Executivo Web, Dashboards Next.js e relatórios 5D interativos | `SKILL_DEV_ARQUITETURA_NEXTJS.md` e `SKILL_GESTAO_06_RELATORIOS.md` |
| Programação de Curto Prazo (WWP), Lotes em Esteira Lean, Takt Time e Nivelamento de Recursos | `SKILL_GESTAO_01_PLANEJAMENTO.md` (§1.3) e `SKILL_GESTAO_08_PRODUTIVIDADE_E_RECURSOS.md` (§2.2) |
| Montar a EAP (WBS) ou o cronograma de uma disciplina ou da obra completa | Consultar a Cadeia Global Integrada na Seção 1.1 abaixo e as Tabelas Oficiais de Serviços: §1.5 da `SKILL_QUANT_06` (níveis 1.1, 1.2, 4.1, 4.2 e 5.1) + §1.2 da `SKILL_QUANT_01` (nível 1.3) + §4.1 da `SKILL_QUANT_02` (nível 1.4) + §2 da `SKILL_QUANT_03` (níveis 2.1 e 2.2) + §3 da `SKILL_QUANT_04` (nível 3.1) + §3 da `SKILL_QUANT_05` (nível 3.2). |

---

## 1.1 Cadeia Global Integrada da EAP (Níveis 1.1 a 5.1) e Predecessoras Interdisciplinares

A governança do cronograma físico, da linha de balanço e da medição contratual exige a articulação harmoniosa de todas as disciplinas levantadas pelas skills quantitativas. A tabela abaixo sintetiza a macroestrutura da EAP Mestre da obra e mapeia os **Gargalos e Portões de Bloqueio Interdisciplinar**:

| Nível EAP | Macroetapa / Disciplina | Skill de Origem | Unid. Avanço | Predecessoras Mestras & Bloqueios Críticos |
|:---:|:---|:---:|:---:|:---|
| **1.1** | Serviços Preliminares, Legalização e Mobilização | `SKILL_QUANT_06` (§1.5) | un / m | Marco Zero; libera terraplenagem (1.2) e locação de fundações (1.3) |
| **1.2** | Terraplenagem e Obras de Contenção | `SKILL_QUANT_06` (§1.5) | m² / m³ | Conformação de platôs; precede a locação e cravamento de fundações |
| **1.3** | Infraestrutura e Fundações (Estacas, Blocos, Baldrames) | `SKILL_QUANT_01` (§1.2) | m / m³ / kg | ⚠️ **1.3.11 (Impermeabilização)** é predecessora BLOQUEANTE de **1.3.13 (Reaterro)** |
| **1.4** | Superestrutura (Ciclo de Pavimento Tipo: Pilares, Vigas, Lajes) | `SKILL_QUANT_02` (§4.1) | m² / m³ / kg | ⚠️ **1.4.12 (Desforma de Laje)** libera prumadas verticais de **3.1.7** e **3.2.8** |
| **2.1** | Alvenaria e Vedações Verticais | `SKILL_QUANT_03` (§2.1) | m² | **2.1.1 (Marcação)** libera rasgos e caixas de **3.1.2** e **3.2.3** |
| **3.1** | Instalações Elétricas, Automação, Dados e SPDA | `SKILL_QUANT_04` (§3) | m / un / pt | Concomitante com alvenaria; tubulações embutidas antes do emboço |
| **3.2** | Instalações Hidrossanitárias, Gás e Drenagem | `SKILL_QUANT_05` (§3) | m / un / pt | 🛑 **3.2.7 (Teste Hidrostático 72h)** é BLOQUEANTE de **2.1.2 (Emboço/Reboco)** |
| **2.2** | Revestimentos, Pisos, Pintura e Forros | `SKILL_QUANT_03` (§2.2) | m² | Depende de 3.2.7 aprovado e 3.1 eletrodutos embutidos e testados |
| **4.1** | Sistemas Especiais (HVAC, Elevadores, SDAI, Bombas) | `SKILL_QUANT_06` (§1.5) | un / m | 4.1.3 depende de 1.4 (Poço); 4.1.4 depende de 3.2 (Barrilete/Reservatório) |
| **4.2** | Urbanização Externa, Paisagismo, Piscinas e Lazer | `SKILL_QUANT_06` (§1.5) | m² / un | Executado após desimpedimento de canteiro civil e fachada |
| **5.1** | Encerramento, Limpeza Pós-Obra, Comissionamento e Databook | `SKILL_QUANT_06` (§1.5) | un / m² | 5.1.3 integra 3.1.14 + 3.2.13; libera Vistoria, Habite-se e Entrega |

### 🛑 Portões de Qualidade e Regras de Bloqueio Interdisciplinar (Zero Retrabalho)

1. **Portão Geotécnico e Fundação (1.3.11 → 1.3.13):**
   - É **expressamente proibido** realizar o reaterro e compactação de valas (`1.3.13`) antes da impermeabilização hidrófuga e cristalizante de vigas baldrame e blocos de coroamento (`1.3.11`), devidamente inspecionada e liberada por FVS.
2. **Portão Estrutura → Prumadas Verticais (1.4.12 → 3.1.7 / 3.2.8):**
   - A liberação de frentes de shafts verticais de esgoto, prumadas de água fria/incêndio e barramentos elétricos exige a desforma total e desaprumo do pavimento imediatamente superior (`1.4.12`), eliminando riscos de queda de materiais e impacto sobre tubulações plásticas.
3. **Portão Hidráulico → Fechamento Civil (3.2.7 → 2.1.2) [REGRA DE OURO]:**
   - **NUNCA chapiscar, emboçar, azulejar ou fechar forros e shafts** sobre tubulações de água fria, água quente ou gás sem a realização do **Teste Hidrostático de Estanqueidade sob Pressão (`3.2.7`) com manômetro calibrado durante no mínimo 72 horas**. Vazamentos descobertos após o revestimento geram quebra-quebra, desperdício e atrasos severos na linha de balanço.
4. **Portão Civil → Dispositivos de Acabamento (2.2.8 → 3.1.9 / 3.2.11):**
   - A instalação de espelhos, tomadas, interruptores finos (`3.1.9`), louças sanitárias, cubas e metais nobres (`3.2.11`) só pode ocorrer após a conclusão da 1ª demão de pintura e forração protetora de pisos (`2.2.8`), prevenindo danos por respingos e abrasão de ferramentas.

---

## 2. Situações com Sobreposição — Qual Skill Manda

| Situação | Skills envolvidas | Como resolver |
|---|---|---|
| Glosa por não conformidade | `SKILL_GESTAO_11` (identifica e investiga a causa) + `SKILL_GESTAO_10` (registra o efeito contratual/financeiro) | `11` decide **se** vira glosa (causa é erro de execução do empreiteiro); `10` registra o valor e o histórico. Nunca aplicar as duas de forma independente sobre o mesmo evento. |
| Retrabalho afetando RUP | `SKILL_GESTAO_11` (registra o retrabalho e seu custo separado) + `SKILL_GESTAO_08` (RUP não deve ser contaminado pelo retrabalho) | Custo e horas de retrabalho **saem** do cálculo de RUP normal do serviço — ver Seção 2 da `SKILL_GESTAO_11`. |
| Encerramento de obra revisitando tudo | `SKILL_GESTAO_12` consome dado de `08`, `09`, `10`, `11` | `12` não recalcula nada sozinha — só consolida o que as outras já apuraram ao longo da obra. |
| Nota fiscal sem pedido, precisa classificar | `SKILL_QUANTIFICACAO_CONCILIACAO_3_PONTAS` (fluxo principal) → cai em `SKILL_QUANTIFICACAO_PEDIDO_DE_COMPRA` (fluxo de exceção) | Conciliação é sempre tentada primeiro; só cai na classificação "do zero" quando não há PO. |
| Reprogramação de cronograma afetando produtividade de frente | `SKILL_GESTAO_16` (decide SE e COMO reprogramar) + `SKILL_GESTAO_08` (fonte do RUP real que fundamenta as novas durações) | A 08 fornece o dado de produtividade; a 16 usa esse dado para recalcular as atividades restantes. A 08 **nunca reprograma** — só a 16 toma essa decisão. |
| Vencimento documental de SST afetando presença no canteiro | `SKILL_GESTAO_17` (identifica e alerta o vencimento) + `SKILL_GESTAO_04` (define quais documentos são obrigatórios e qual ação de campo tomar) | A 04 define a obrigação; a 17 monitora a validade continuamente. Nunca checar só na entrada do trabalhador. |
| Levantamento concluído, falta compor o custo | `SKILL_QUANTIFICACAO_COMPOSICAO_PRECO` (hierarquia SINAPI → cotação → NF) + SKILL_QUANT da disciplina correspondente | Composição de preço nunca é feita dentro do skill de levantamento — é etapa separada e posterior. |
| Falta informação na prancha que bloqueia quantitativo | `SKILL_ENGENHARIA_RFI` (abre e controla o ciclo da RFI) + SKILL_QUANT correspondente (retoma o item quando RFI for respondida) | O item bloqueado fica com `STATUS = PENDENTE_RFI` até a RFI ser incorporada. Nunca estimar para desbloquear. |
| Liberação de frente de serviço no canteiro | `SKILL_GESTAO_02` (rotina de produção) + `SKILL_PRODUCAO_POP_BRIDGE` (identificar qual POP aplicar ao serviço) | Produção sem POP = processo sem guardrail. A bridge é consulta obrigatória antes de qualquer frente nova. |

**Regra de ouro**: se o agente identificar uma situação que duas skills reivindicam sem que este
índice resolva o conflito, ele deve **parar e perguntar** qual critério usar, e sugerir que esse
caso vire uma nova linha na tabela da Seção 2 — o índice deve crescer com o uso real, não ser
reescrito de memória.

---

## 3. Hierarquia de Precedência Geral

Quando nenhuma tabela acima resolve o conflito, esta é a ordem de precedência:

1. **Regras de autonomia** (`ADENDO_AGENTS_REGRAS_DE_AUTONOMIA.md`) sempre têm precedência sobre
   qualquer skill de conteúdo — não importa o que a skill técnica recomenda, se a ação cai em
   🟠/🔴 de autonomia, pausa primeiro.
2. **Rigor de ciência de dados** (`SKILL_GESTAO_07`) se aplica a **qualquer** afirmação analítica
   de qualquer outra skill — nenhuma skill de conteúdo está isenta da hierarquia de confiança. O Portão de Qualidade de Dado DEVE ser declarado explicitamente antes de gerar relatórios (06), analisar produtividade (08), projetar fluxo de caixa (09), estimar riscos (13) ou reprogramar o cronograma (16).
3. Skills de quantitativo (fonte do dado bruto) têm precedência sobre skills de gestão (que
   consomem esse dado) em caso de divergência de número — a gestão nunca "corrige" um
   quantitativo por conta própria, sinaliza a divergência de volta pra quantificação.

---

## 4. Histórico de Atualizações

| Data | Alteração |
|---|---|
| Criação inicial | Skills 00–15 + Adendo de Autonomia |
| Atualização 2026-09 (1) | Adicionadas Skills 16 (Cronograma/Reprogramação) e 17 (Vencimento Documental SST) nas Seções 1 e 2 |
| Atualização 2026-09 (2) | Adicionadas: `SKILL_QUANTIFICACAO_COMPOSICAO_PRECO` (M5), `SKILL_ENGENHARIA_RFI` (M6), `SKILL_PRODUCAO_POP_BRIDGE` (M7) nas Seções 1 e 2 |
| Atualização 2026-09 (3) | Adicionado roteamento para EAP / Cronograma Integrado (Tabelas Oficiais de Serviços das Skills 01 a 06) na Seção 1 |
| Atualização 2026-09 (4) | Adicionada Seção 1.1 (Cadeia Global Integrada da EAP Níveis 1.1 a 5.1 e Portões de Bloqueio Interdisciplinar) |

*Este índice deve ser atualizado toda vez que uma skill nova for criada ou uma sobreposição nova
for identificada durante o uso real do sistema.*
