# 🔒 EXTENSÃO AO ADENDO DE AUTONOMIA: Cadeia de Validação em Camadas

Aplica-se **exclusivamente** às ações classificadas como 🟠 (pausa obrigatória) ou 🔴 (nunca
autônomo) no `ADENDO_AGENTS_REGRAS_DE_AUTONOMIA.md`. Ações 🟢 seguem seu fluxo normal, sem esta
cadeia — adicionar camada de revisão onde o risco já é baixo só gera lentidão sem ganho real de
segurança.

> **Alerta de design, para não perder o objetivo**: múltiplas camadas do mesmo modelo de IA,
> olhando o mesmo dado, tendem a repetir o mesmo julgamento, não a se corrigir mutuamente. Esta
> cadeia só funciona se cada camada checar **algo objetivamente diferente** da anterior — nunca
> "revise se está tudo bem" repetido três vezes.

---

## 1. As Quatro Camadas

### Camada 1 — Executor (propõe)
Aplica a skill técnica relevante (quantitativo, conciliação, contrato, etc.) e produz uma proposta
estruturada:
```
Ação proposta: [o quê, exatamente]
Nível de confiança: [🟢/🟡/🔴, conforme SKILL_GESTAO_07]
Evidência usada: [de onde vem cada dado]
Justificativa: [por que esta é a ação correta]
```

### Camada 2 — Revisor (audita contra critério objetivo, não reavalia por julgamento livre)
**Não** pergunta "isso parece certo?" — verifica uma lista fechada de critérios, e só isso:
- A matemática/cálculo bate, recalculando de forma independente? (não confiar no número do
  Executor, recalcular do zero a partir da mesma evidência)
- O Portão de Qualidade de Dado (`SKILL_GESTAO_07`, Seção 1) foi de fato aplicado antes da proposta?
- O nível de confiança declarado (🟢/🟡/🔴) está correto pela definição da skill, ou o Executor
  classificou errado (ex.: chamou de 🟢 algo que deveria ser 🟡 pela própria regra da skill)?
- Toda evidência citada existe e é rastreável (não inventada)?
- **Instrução explícita ao Revisor**: procurar ativamente um motivo para reprovar, não confirmar
  por padrão — postura adversarial deliberada, para não virar carimbo automático.

Se qualquer item falhar → devolve para o Executor com o motivo específico, não segue adiante.

### Camada 3 — Pré-autorizador (aplica regra de negócio, decide se escala)
Não reavalia o conteúdo técnico — aplica política já definida pelo CEO **previamente**:
- Valor da ação está dentro de um teto pré-aprovado para este tipo de ação?
- Envolve fornecedor/empreiteiro novo (sem histórico) ou já conhecido?
- A Camada 2 aprovou sem ressalva, ou aprovou com alguma observação registrada?

Resultado possível:
- **Dentro da política + aprovado sem ressalva pela Camada 2** → segue para execução registrada
  (ainda assim logada para auditoria, nunca silenciosa).
- **Qualquer dúvida, exceção à política, ou ressalva da Camada 2** → escala direto para a Camada 4,
  sem tentar decidir sozinho.

### Camada 4 — Você (validação final humana)
Só recebe o que realmente precisa de decisão humana — não o volume total de ações 🟠/🔴, só o que
passou por exceção na Camada 3. Chega com o histórico completo das camadas anteriores, não como
pergunta em branco:
```
Proposta original (Camada 1) + Auditoria (Camada 2) + Por que escalou (Camada 3)
Decisão necessária: Aprovar / Rejeitar / Pedir mais informação
```

---

## 2. Critério de Escalonamento Imediato (pula direto para você)

Independente de qual camada está processando, os seguintes casos vão direto para a Camada 4,
sem esperar o fluxo normal:

- Qualquer item classificado 🔴 pela `SKILL_GESTAO_07` em qualquer camada
- Valor acima de um teto que você define previamente
- Fornecedor/empreiteiro sem histórico prévio no sistema
- Divergência entre o que o Executor propôs e o que o Revisor recalculou

---

## 3. Por Que Isso Não Substitui a Trava Técnica (MCP)

Esta cadeia reduz erro de julgamento correlacionado, mas **três agentes de IA concordando ainda
não é o mesmo que a ferramenta de pagamento não existir no sistema**. Ela é uma camada adicional de
segurança de processo — a trava técnica real (servidor MCP sem ferramenta de escrita para ações
críticas, discutida anteriormente) continua sendo a defesa mais forte e deve ser priorizada quando
o backend for construído. Até lá, esta cadeia é o melhor controle disponível dentro da arquitetura
atual (repositório + Antigravity).

---

## ⚠️ 4. Regras de Ouro

1. Camada 2 nunca reavalia por julgamento livre — só contra checklist objetivo e recálculo
   independente.
2. Qualquer reprovação em qualquer camada é registrada com motivo específico, nunca descartada
   silenciosamente.
3. A Camada 4 só recebe exceções reais, nunca o volume bruto de toda ação 🟠/🔴 — senão o CEO vira
   gargalo e a cadeia perde o propósito.
4. Esta cadeia se aplica só a 🟠/🔴 — nunca adicionar a ações já classificadas 🟢, sob risco de
   lentidão sem ganho de segurança proporcional.

---
*Extensão de `ADENDO_AGENTS_REGRAS_DE_AUTONOMIA.md`. Trabalha junto com
`SKILL_GESTAO_07_CIENCIA_DE_DADOS.md` (fonte da hierarquia de confiança usada pela Camada 2).*
