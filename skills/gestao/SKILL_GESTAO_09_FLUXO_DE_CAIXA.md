# 💰 SKILL GESTÃO 09: Fluxo de Caixa e Curva de Desembolso

Resolve uma lacuna crítica que o EVM (`SKILL_GESTAO_06`) não cobre: **estar dentro do orçamento
não significa ter caixa disponível no momento certo**. Construtora pequena/média quebra mais por
descasamento de timing entre pagar e receber do que por estouro de custo total.

> Este módulo cruza o cronograma físico-financeiro (quando o custo *deveria* acontecer) com os
> prazos reais de pagamento e recebimento (quando o dinheiro *de fato* sai e entra).

---

## ⚠️ PRÉ-REQUISITO OBRIGATÓRIO — PORTÃO DE QUALIDADE DE DADO
Antes de apresentar **qualquer número, projeção ou recomendação** desta skill, o agente DEVE verificar o nível de confiança de cada dado de entrada consultando a `SKILL_GESTAO_07_CIENCIA_DE_DADOS.md` (Seção 1: Hierarquia de Confiança) ou rodando o script `scripts/calculadoras/portao_qualidade_dado.py`.

Formato obrigatório de declaração antes de qualquer análise:
| Dado | Fonte | Confiança | Observação |
|---|---|---|---|
| [dado usado] | [arquivo/CSV] | 🟢/🟡/🔴 | [caveats] |

**NÃO prosseguir com análise se qualquer dado crítico for 🔴.**

---

## 1. Curva de Desembolso Planejada × Real

```
Desembolso planejado do período = Σ (custo orçado dos serviços previstos no cronograma para
                                      aquele período, considerando prazo de pagamento do
                                      fornecedor/empreiteiro — não a data do serviço em si)
```

**Ponto crítico**: o desembolso não acontece na data em que o serviço é executado — acontece na
data de **vencimento do pagamento** (que pode ser 30, 45, 60 dias depois, dependendo do prazo
negociado). Ignorar essa defasagem é o erro mais comum de projeção de caixa em obra.

| Dado necessário | Fonte |
|---|---|
| Quando o serviço está previsto no cronograma | Cronograma físico (já existente) |
| Prazo de pagamento negociado com cada fornecedor/empreiteiro | Contrato/pedido de compra |
| Quando a medição do empreiteiro é aprovada | Medição (Regra da Trena) |

---

## 2. Se houver receita (incorporação/venda), cruzar também a entrada

Quando a obra tem receita própria (não é só custo puro de execução), a curva de caixa precisa do
lado de entrada também:

```
Saldo de caixa projetado do período = Recebimentos previstos do período − Desembolsos previstos do período
```

- Recebimento de venda/parcela de cliente tem prazo próprio (contrato de venda), raramente
  coincide com o ritmo de desembolso da obra — é exatamente esse descompasso que gera aperto.
- Se a obra é só execução (contratante paga por medição), o "recebimento" é a medição aprovada
  pelo contratante — mesma lógica, prazo de recebimento pode ser diferente do prazo de pagamento
  aos próprios fornecedores.

---

## 3. Alertas obrigatórios

| Situação | Ação |
|---|---|
| Saldo de caixa projetado fica negativo em algum período futuro | 🔴 Alertar com antecedência mínima do maior prazo de pagamento em aberto — não adianta avisar 3 dias antes de um vencimento de 45 dias |
| Concentração de vencimentos na mesma semana/quinzena | 🟡 Sinalizar mesmo que o saldo total do mês feche positivo — pico pontual pode quebrar caixa mesmo com média saudável |
| Atraso de recebimento (medição aprovada mas não paga no prazo) | 🔴 Tratar como risco imediato, recalcular projeção com o atraso já considerado, não manter a data contratual como se fosse certa |

---

## ⚠️ 4. Regras de Ouro

1. Nunca projetar desembolso na data do serviço — sempre na data de vencimento do pagamento.
2. Nunca tratar uma data de recebimento contratual como garantida — histórico de atraso do
   contratante/cliente deve ajustar a projeção (ver protocolo de correlação×causa da
   `SKILL_GESTAO_07` antes de assumir que o próximo recebimento também vai atrasar).
3. Sempre projetar em faixa (otimista/realista/pessimista), nunca em número único — mesma lógica
   de projeção da `SKILL_GESTAO_07`, Seção 5.
4. Alerta de caixa negativo deve vir com antecedência suficiente pra ação corretiva ser possível
   (renegociar prazo, antecipar recebível), não em cima da hora.

---
*Trabalha junto com `SKILL_GESTAO_06_RELATORIOS.md` (cronograma físico-financeiro) e
`SKILL_GESTAO_07_CIENCIA_DE_DADOS.md` (rigor de projeção em faixa).*
