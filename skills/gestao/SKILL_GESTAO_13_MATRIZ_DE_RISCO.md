# ⚠️ SKILL GESTÃO 13: Matriz de Risco da Obra

Todas as outras skills de gestão são **reativas** — medem desvio depois que ele já aconteceu
(SPI/CPI, RUP fora da meta, caixa negativo). Esta skill é a única **preventiva**: identifica risco
antes de virar problema.

---

## ⚠️ PRÉ-REQUISITO OBRIGATÓRIO — PORTÃO DE QUALIDADE DE DADO
Antes de apresentar **qualquer número, projeção ou recomendação** desta skill, o agente DEVE verificar o nível de confiança de cada dado de entrada consultando a `SKILL_GESTAO_07_CIENCIA_DE_DADOS.md` (Seção 1: Hierarquia de Confiança) ou rodando o script `scripts/calculadoras/portao_qualidade_dado.py`.

Formato obrigatório de declaração antes de qualquer análise:
| Dado | Fonte | Confiança | Observação |
|---|---|---|---|
| [dado usado] | [arquivo/CSV] | 🟢/🟡/🔴 | [caveats] |

**NÃO prosseguir com análise se qualquer dado crítico for 🔴.**

---

## 1. Estrutura do Risco

| Campo | Descrição |
|---|---|
| Descrição do risco | O que pode acontecer, especificamente — não "atraso", e sim "atraso na entrega de esquadrias por ser importado, com prazo histórico de 90 dias" |
| Probabilidade | Alta / Média / Baixa — baseada em histórico real quando existir (mesma disciplina de N mínimo da `SKILL_GESTAO_07`), não em achismo |
| Impacto | Em prazo (dias) e/ou custo (R$) — sempre que possível quantificado, não só "alto/médio/baixo" vago |
| Gatilho de monitoramento | O que observar que indica que o risco está se materializando (ex.: "fornecedor não confirmou pedido em 5 dias úteis") |
| Ação de mitigação | O que fazer **antes** de o risco virar problema — não a ação de contorno depois que já aconteceu |
| Responsável | Quem monitora e quem decide a ação |

---

## 2. De Onde Vêm os Riscos — Não Inventar do Zero

- **Riscos recorrentes já vividos pela própria empresa** (glosa recorrente de um tipo de
  empreiteiro, atraso histórico de um fornecedor específico — dado que já está em
  `SKILL_GESTAO_10`) — esses têm probabilidade calculável, não estimada.
- **Riscos típicos do tipo de obra/etapa atual** (chuva em etapa de fundação/movimento de terra,
  falta de mão de obra especializada em etapa de acabamento) — conhecimento de engenharia, não
  estatística da própria obra.
- **Riscos apontados pelo próprio engenheiro/gestor** em conversa — a IA não deveria só esperar
  pedir pra listar risco, deveria perguntar ativamente no início de cada etapa nova do
  cronograma: "quais riscos você já enxerga nessa próxima fase?"

---

## 3. Cruzamento com o Restante do Sistema

A matriz de risco não é um documento isolado — ela deve ser **revisitada** quando outras skills
detectam sinal:

- `SKILL_GESTAO_07` detecta correlação suspeita → verificar se já existe um risco cadastrado que
  explica isso, ou se é um risco novo a cadastrar.
- `SKILL_GESTAO_09` (fluxo de caixa) projeta saldo negativo → checar se esse risco já estava
  mapeado com antecedência ou se pegou o sistema de surpresa (isso é sinal de que a matriz de
  risco precisa ser mais proativa).

---

## ⚠️ 4. Regras de Ouro

1. Risco sem probabilidade **e** impacto estimado não é priorizável — a IA deve pedir essas duas
   dimensões antes de tratar um risco como relevante.
2. Ação de mitigação é sempre preventiva (antes do gatilho disparar) — ação só depois do gatilho é
   plano de contingência, categoria diferente, também deve ser registrada, mas não confundida com
   mitigação.
3. Todo desvio real que aparecer via outra skill (`06` a `12`) deve ser checado contra a matriz de
   risco: **estava mapeado?** Se não estava, isso é aprendizado que deveria gerar uma linha nova
   de risco pra próxima obra — fechando o ciclo de melhoria contínua também no nível de risco.

---
*Trabalha junto com todas as demais skills de gestão — é a camada que olha para frente enquanto
elas medem o que já aconteceu.*
