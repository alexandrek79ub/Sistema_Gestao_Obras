# 📄 SKILL GESTÃO 10: Contratos — Aditivos, Retenção e Glosas

Complementa a medição (Regra da Trena, já existente) com o que acontece **ao redor** da medição:
mudança de escopo, retenção de garantia, e histórico de desempenho contratual — peças que hoje
não têm rastreamento formal.

---

## 1. Aditivos — Duas Direções, Mesma Mecânica

Aditivo (serviço extra, mudança de quantidade, prorrogação de prazo) muda o valor ou o prazo de um
contrato — mas o contrato pode ser em **duas direções diferentes**, e a IA precisa identificar qual
antes de processar:

| Direção | Contraparte | Efeito financeiro | Sensibilidade |
|---|---|---|---|
| **Aditivo de custo** | Empreiteiro/fornecedor | Aumenta o que a construtora **paga** | Afeta `SKILL_GESTAO_09` pelo lado do desembolso |
| **Aditivo de receita** | Cliente/contratante | Aumenta o que a construtora **recebe** | Afeta `SKILL_GESTAO_09` pelo lado do recebimento — e altera a **baseline do contrato principal** (`SKILL_GESTAO_14`), não só de um subcontrato |

**Aditivo de receita é o mais sensível dos dois**: é a fonte mais comum de disputa entre
construtora e cliente, porque normalmente envolve negociação de percepção de valor ("isso já não
estava incluso?"), não só cálculo técnico. Tratar com o mesmo rigor de evidência do aditivo de
custo, mas com atenção redobrada à aprovação formal — aditivo de receita sem aceite explícito do
cliente é o cenário de disputa mais caro de todos.

Todo aditivo, em qualquer direção, deve ser registrado **antes** de ser pago/cobrado ou de virar
justificativa de atraso — nunca reconstruído depois, de memória.

| Campo obrigatório | Por quê |
|---|---|
| Direção | Custo (empreiteiro) ou Receita (contratante) — determina o fluxo afetado e a baseline a alterar |
| Serviço/CIA afetado | Rastreabilidade contra o orçamento base |
| Motivo do aditivo | Erro de projeto original? Pedido do cliente? Condição de campo imprevista? — isso muda quem "paga a conta" |
| Valor do aditivo | Sempre com memória de cálculo própria, mesma exigência da medição normal |
| Impacto no prazo (se houver) | Precisa refletir no cronograma, não ficar só registrado à parte |
| Aprovação | Quem autorizou — sem isso, não é aditivo, é glosa em potencial (custo) ou disputa em potencial (receita) no fechamento |

**Regra de ouro**: aditivo sem aprovação registrada **antes da execução** deve ser tratado como
risco de disputa no fechamento do contrato — sinalizar isso proativamente, não só no final da obra.
Para aditivo de receita, a aprovação precisa ser do **cliente/contratante**, não só de alguém
interno da construtora — aprovação interna sozinha não protege contra disputa externa.

---

## 2. Retenção de Garantia

- Registrar o **percentual de retenção contratual** (comum 5-10% sobre cada medição) e a
  **condição de liberação** (entrega da etapa, fim da obra, prazo de garantia decorrido).
- Manter saldo retido acumulado visível por empreiteiro — é dinheiro que a construtora deve, não
  deveria "sumir" do controle só porque não foi pago ainda.
- Alertar quando a condição de liberação for atingida — retenção esquecida gera passivo
  silencioso e desgaste de relação com o empreiteiro.

---

## 3. Glosas — Histórico por Empreiteiro

Glosa (valor descontado da medição por não conformidade, atraso, ou serviço não executado
conforme especificado) deve ser registrada com:

- Motivo específico (não "ajuste", motivo real)
- Valor
- Se foi contestada pelo empreiteiro e o desfecho

**Por que isso importa além do registro pontual**: acumular esse histórico por empreiteiro permite
uma pergunta que hoje ninguém consegue responder rápido — *"esse empreiteiro tem histórico de
glosa recorrente pelo mesmo motivo?"* Isso deveria influenciar decisão de recontratação, e é
exatamente o tipo de cruzamento que o agente pode responder na hora, aplicando a mesma disciplina
de segmentação da `SKILL_GESTAO_07` (nunca julgar por 1 evento isolado, olhar o padrão).

---

## ⚠️ 4. Regras de Ouro

1. Todo aditivo tem direção identificada (custo ou receita) antes de ser processado — isso
   determina qual baseline e qual fluxo de caixa ele afeta.
2. Aditivo sem aprovação prévia registrada é sinalizado como risco, não tratado como fato consumado
   — para aditivo de receita, a aprovação precisa ser do cliente/contratante especificamente.
3. Retenção de garantia é sempre visível como passivo em aberto, nunca "esquecida" até o encerramento.
4. Glosa é sempre registrada com motivo específico — nunca como ajuste genérico sem rastro.
5. Histórico de glosa por empreiteiro é consultável e segmentado — nunca escondido dentro do total
   agregado da obra.

---
*Trabalha junto com a Regra da Trena (medição), `SKILL_GESTAO_09_FLUXO_DE_CAIXA.md` (retenção,
glosa e aditivo de receita afetam diretamente a curva de desembolso/recebimento) e
`SKILL_GESTAO_14_CONTROLE_DE_REVISAO.md` (aditivo de receita altera a baseline do contrato
principal).*
