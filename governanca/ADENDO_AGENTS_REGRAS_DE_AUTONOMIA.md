# ⚙️ ADENDO A agents.md: Regras de Autonomia do Agente

Formaliza o que fica implícito hoje: **o que o agente decide e executa sozinho** (incluindo
commit/push automático) **vs. o que exige pausa e confirmação humana** antes de agir. Isso é
crítico no modo de operação "cliente autônomo" — quando quem interage com o agente é o
engenheiro do cliente, sem o desenvolvedor do sistema no meio pra revisar antes.

> Inserir esta seção diretamente em `agents.md`, como uma seção de primeira classe, não como
> observação lateral — autonomia mal definida é o maior risco operacional do modo autônomo.

---

## 1. Nível de Autonomia por Tipo de Ação

| Ação | Autonomia | Justificativa |
|---|---|---|
| Ler dado, gerar relatório, gerar análise, responder pergunta | 🟢 **Total** — executa e informa depois | Baixo risco, reversível, não altera nenhum registro contábil/contratual |
| Atualizar CSV com dado já validado (ex.: RDO já conferido, medição já aprovada por humano) | 🟢 **Total** — commit/push automático | Dado já passou por validação humana antes de chegar ao agente |
| Classificar nota fiscal com pedido de compra vinculado, casamento óbvio (🟢 na hierarquia de confiança) | 🟢 **Total**, mas registra a classificação de forma auditável | Conciliação de 3 pontas com match claro |
| Classificar nota fiscal **sem** pedido de compra, ou com item ambíguo (🟡/🔴) | 🟠 **Pausa obrigatória** — propõe a classificação, espera confirmação | Erro aqui contamina orçamento/CIA silenciosamente |
| Gerar pedido de compra que excede o saldo a comprar (`SKILL_QUANTIFICACAO_PEDIDO_DE_COMPRA`, Seção 1) | 🟠 **Pausa obrigatória** | Pode ser compra antecipada legítima ou erro — decisão é humana |
| Registrar aditivo de contrato, glosa, ou liberação de retenção de garantia | 🔴 **Nunca autônomo** | Envolve valor contratual e pode gerar disputa — sempre precisa de aprovação explícita registrada |
| Qualquer ação que resulte em pagamento ou autorização de pagamento | 🔴 **Nunca autônomo** | Mesma lógica da Regra da Trena — nunca pagar por avanço presumido nem por decisão só do agente |
| Alterar baseline de orçamento ou cronograma já aprovado | 🔴 **Nunca autônomo** | Baseline existe justamente para medir desvio; alterá-la sem controle destrói a própria métrica de EVM |
| Marcar item do checklist de encerramento de obra como concluído | 🔴 **Nunca autônomo** | Exige evidência documental e assinatura humana, por definição (`SKILL_GESTAO_12`) |

---

## 2. Formato de Pausa para Confirmação

Quando uma ação cair em 🟠 ou 🔴, o agente deve parar e apresentar, nunca decidir e informar depois:

```
⏸️ AÇÃO REQUER CONFIRMAÇÃO
O que o agente quer fazer: [ação específica]
Por que está pausando: [motivo — nível de confiança, valor, tipo de ação]
Dado disponível: [o que já se sabe, incluindo nível de confiança 🟢/🟡/🔴]
Aguardando: [confirmar / corrigir / rejeitar]
```

O agente não deve prosseguir com uma interpretação própria enquanto aguarda — deve efetivamente
parar a ação até resposta humana.

---

## 3. Auditoria de Autonomia

Toda ação tomada em modo 🟢 (autônomo) deve ficar registrada de forma que seja possível, depois,
auditar **o que o agente decidiu sozinho** — isso é o que o Git já resolve bem (commit por commit),
mas deve ser reforçado: mensagens de commit devem indicar claramente quando a ação foi autônoma
vs. quando foi confirmada por humano, para que o histórico sirva como trilha de auditoria real,
não só como controle de versão.

---

## ⚠️ 4. Regra de Ouro

**Na dúvida sobre em qual nível uma ação se enquadra, o agente trata como 🟠 (pausa), nunca como
🟢 (autônomo).** Errar para o lado da cautela custa um segundo de confirmação humana. Errar para o
lado da autonomia pode custar um pagamento indevido, uma classificação errada silenciosa, ou uma
disputa contratual.

---
*Este adendo trabalha junto com todas as skills de gestão e quantitativo — ele define o
"quanto" de autonomia, elas definem o "o quê" da análise em si.*
