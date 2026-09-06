# ✅ SKILL GESTÃO 11: Controle de Qualidade e Não Conformidade

Cobre uma fonte de perda que não aparece em nenhuma outra skill: **retrabalho por erro de
execução** (não é desperdício de material puro, nem baixa produtividade — é serviço que foi feito
e precisou ser refeito).

---

## 1. Registro de Não Conformidade (NC)

| Campo | Descrição |
|---|---|
| Serviço/CIA afetado | |
| Descrição da não conformidade | O que estava fora do especificado (prumo, esquadro, acabamento, especificação de material trocada) |
| Quem identificou | Fiscalização própria, cliente, ou o próprio empreiteiro |
| Causa apontada | Preencher só depois de investigar — nunca assumir causa na hora do registro |
| Custo do retrabalho | Material + mão de obra gasta refazendo, tratado como custo separado do orçamento original do serviço |
| Responsável pelo custo | Empreiteiro (erro de execução) ou construtora (erro de especificação/projeto) — isso determina se vira glosa |

---

## 2. Custo de Retrabalho — por que separar do custo normal do serviço

Se o custo de refazer um serviço é somado ao custo normal do mesmo CIA, o quantitativo e o CPI
daquele item ficam **contaminados** — parecem mais caros do que o serviço realmente custa quando
bem executado, escondendo o problema real (qualidade) atrás de um número de custo genérico.

**Regra**: custo de retrabalho é sempre lançado numa categoria própria ("Retrabalho — [CIA
original]"), nunca dentro do custo normal do serviço. Isso permite responder "quanto a obra está
perdendo com retrabalho, no total e por empreiteiro" — pergunta que hoje fica escondida dentro do
CPI geral.

---

## 3. Padrão de Recorrência — aplicar a mesma disciplina de segmentação

Uma NC isolada é normal em qualquer obra. O que exige ação é o **padrão**:

- Mesma NC, mesmo empreiteiro, repetindo → problema de capacitação/método da equipe, não evento
  isolado.
- Mesma NC, empreiteiros diferentes, mesmo tipo de serviço → possível problema de especificação
  de projeto ou material, não da mão de obra.

Essa distinção só aparece se a IA segmentar por empreiteiro E por tipo de serviço (mesma lógica da
Seção 6 da `SKILL_GESTAO_07`) — nunca aceitar a primeira hipótese sem checar contra os dois cortes.

---

## ⚠️ 4. Regras de Ouro

1. Causa da não conformidade nunca é assumida no momento do registro — só depois de investigação
   mínima (aplicar o protocolo de correlação×causa da `SKILL_GESTAO_07`).
2. Custo de retrabalho é sempre lançado separado do custo normal do serviço, nunca misturado.
3. NC isolada não gera alerta de padrão — só recorrência (mesmo empreiteiro ou mesmo tipo de
   serviço) justifica ação estrutural.
4. Toda NC atribuída a erro de execução do empreiteiro deve alimentar o histórico de glosa da
   `SKILL_GESTAO_10`, mantendo consistência entre as duas skills.

---
*Trabalha junto com `SKILL_GESTAO_10_CONTRATOS_EMPREITEIROS.md` (glosa por não conformidade) e
`SKILL_GESTAO_08_PRODUTIVIDADE_E_RECURSOS.md` (retrabalho distorce RUP se não for separado).*
