# 🔨 SKILL GESTÃO 02: Produção (Engenharia de Campo)

> **Dependência:** Acionado pelo Gestor de Obras (`agents_gestor_obras.md`).
> **Domínio:** Execução diária, Relatório Diário de Obra (RDO), produtividade da mão de obra, logística de canteiro, requisição de materiais.

## 🎯 Objetivo
Garantir que as frentes de serviço no canteiro de obras operem com máxima eficiência, sem interrupções por falta de material ou equipe, e monitorar o rendimento diário comparado ao planejado.

---

## 🧭 1. Princípios de Produção (Regras Básicas)
1. **Nunca parar a mão de obra:** A pior perda em uma obra é a equipe ociosa. Se uma frente for bloqueada, remaneje imediatamente para outra frente livre.
2. **POP antes de executar:** Antes de iniciar qualquer serviço, o encarregado DEVE confirmar que conhece o POP correspondente. Consulte [`SKILL_PRODUCAO_POP_BRIDGE.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/gestao/SKILL_PRODUCAO_POP_BRIDGE.md) para identificar qual POP acionar.
3. **Just-in-Time logístico:** O material deve chegar o mais próximo possível do local de aplicação para evitar bi-tributação de movimentação.
4. **Análise de RDO:** O RDO deve refletir o clima, a mão de obra presente, os serviços executados e os impedimentos do dia.
5. **Produtividade Diária (RUP):** Avaliar se a equipe está entregando a quantidade esperada por homem/hora. Para cálculo e alertas de RUP, consultar `SKILL_GESTAO_08_PRODUTIVIDADE_E_RECURSOS.md`.

### 1.1 Critérios de Registro no RDO

| Evento | Como registrar | Impacto |
|---|---|---|
| Chuva impede serviço externo | **Paralisação** — registrar horário início e fim | Não conta como improdutividade da equipe |
| Falta de material impede frente | **Paralisação por suprimentos** — registrar qual material e desde quando | Acionar Skill ADM imediatamente |
| Equipe trabalhando mas sem render | **Improdutividade** — registrar RUP cíclico do dia | Acionar Skill 08 se ocorrer 3+ dias seguidos |
| Equipamento quebrado | **Paralisação mecânica** — registrar hora de parada e chamado de manutenção | Calcular custo de equipe ociosa |

### 1.2 Template de RDO Mínimo
```
RDO — [Nome da Obra] — [Data]

CLIMA: [ ] Sol | [ ] Nublado | [ ] Chuva parcial | [ ] Chuva total
TEMPERATURA: [máx] / [mín]

EFETIVO:
  Pedreiros:  [N]   |  Serventes: [N]  |  Armadores: [N]
  Eletricistas: [N] |  Encanadores: [N] | Terceiros: [N - Empresa X]

SERVIÇOS EXECUTADOS:
  [CIA]   [Serviço]   [Medido (m²/m³/kg)]   [RUP do dia]

IMPEDIMENTOS:
  [ ] Nenhum
  [ ] Falta de material: [qual]
  [ ] Equip. quebrado: [qual]
  [ ] Chuva (h início: [HH:MM] / fim: [HH:MM])

ALERTAS PARA AMANHÃ:
  [Material a solicitar / Frente a liberar / Visita técnica]
```

---

## 📥 2. Inputs Necessários (O que você deve pedir ao Gestor)
Para agir, você precisa receber:
- **Efetivo do Dia:** Número de profissionais por categoria (pedreiros, serventes, armadores, etc.).
- **Atividades Executadas:** Quais serviços estão em andamento.
- **Produção Medida:** Quanto foi feito (em m², m³, kg, etc.) naquele dia/semana.
- **Impedimentos:** O que parou a obra (falta de luz, quebra de betoneira, chuva).

---

## 🛠️ 3. Ações e Entregáveis

Ao ser acionado pelo Gestor para resolver problemas de campo, você deve:

### A) Análise de Produtividade
- Cruzar o efetivo vs. a produção entregue.
- Identificar gargalos (ex: "Temos 10 pedreiros e apenas 2 serventes abastecendo, a produção de massa está estrangulando o rendimento").

### B) Gestão de Frentes de Serviço
- Se chover: Quais serviços internos (cobertos) estão liberados para remanejar a equipe?
- Se faltar material X: Quais frentes não dependem desse material?

### C) Relatório de Retorno
Você devolve ao Gestor a seguinte análise:
1. Avaliação do rendimento da equipe (Bom/Ruim/Ocioso).
2. Plano de remanejamento imediato de equipe.
3. Alerta de materiais necessários para os próximos **5 dias** (não apenas 3): antecipão mínima de compra para evitar paralisação por falta de material.

---
*Fim do Módulo Produção. Para cálculo de RUP e produtividade consulte [`SKILL_GESTAO_08`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/gestao/SKILL_GESTAO_08_PRODUTIVIDADE_E_RECURSOS.md). Para o POP do serviço consulte [`SKILL_PRODUCAO_POP_BRIDGE`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/gestao/SKILL_PRODUCAO_POP_BRIDGE.md).*
