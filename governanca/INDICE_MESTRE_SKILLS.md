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
| Aditivo de contrato, retenção de garantia | `SKILL_GESTAO_10_CONTRATOS_EMPREITEIROS.md` |
| Retrabalho, defeito de execução | `SKILL_GESTAO_11_QUALIDADE_NAO_CONFORMIDADE.md` |
| Fim de obra, as-built, entrega ao cliente | `SKILL_GESTAO_12_ENCERRAMENTO_DE_OBRA.md` |
| Risco futuro, ainda não materializado | `SKILL_GESTAO_13_MATRIZ_DE_RISCO.md` |
| Versão de projeto, revisão de documento | `SKILL_GESTAO_14_CONTROLE_DE_REVISAO.md` |
| Relatório/comunicação formal ao cliente/contratante | `SKILL_GESTAO_15_COMUNICACAO_CLIENTE.md` |
| O que o agente pode decidir sozinho vs. o que pausa | `ADENDO_AGENTS_REGRAS_DE_AUTONOMIA.md` — **sempre consultar em paralelo**, nunca isolado |

---

## 2. Situações com Sobreposição — Qual Skill Manda

| Situação | Skills envolvidas | Como resolver |
|---|---|---|
| Glosa por não conformidade | `SKILL_GESTAO_11` (identifica e investiga a causa) + `SKILL_GESTAO_10` (registra o efeito contratual/financeiro) | `11` decide **se** vira glosa (causa é erro de execução do empreiteiro); `10` registra o valor e o histórico. Nunca aplicar as duas de forma independente sobre o mesmo evento. |
| Retrabalho afetando RUP | `SKILL_GESTAO_11` (registra o retrabalho e seu custo separado) + `SKILL_GESTAO_08` (RUP não deve ser contaminado pelo retrabalho) | Custo e horas de retrabalho **saem** do cálculo de RUP normal do serviço — ver Seção 2 da `SKILL_GESTAO_11`. |
| Encerramento de obra revisitando tudo | `SKILL_GESTAO_12` consome dado de `08`, `09`, `10`, `11` | `12` não recalcula nada sozinha — só consolida o que as outras já apuraram ao longo da obra. |
| Nota fiscal sem pedido, precisa classificar | `SKILL_QUANTIFICACAO_CONCILIACAO_3_PONTAS` (fluxo principal) → cai em `SKILL_QUANTIFICACAO_PEDIDO_DE_COMPRA` (fluxo de exceção) | Conciliação é sempre tentada primeiro; só cai na classificação "do zero" quando não há PO. |

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
   de qualquer outra skill — nenhuma skill de conteúdo está isenta da hierarquia de confiança.
3. Skills de quantitativo (fonte do dado bruto) têm precedência sobre skills de gestão (que
   consomem esse dado) em caso de divergência de número — a gestão nunca "corrige" um
   quantitativo por conta própria, sinaliza a divergência de volta pra quantificação.

---
*Este índice deve ser atualizado toda vez que uma skill nova for criada ou uma sobreposição nova
for identificada durante o uso real do sistema.*
