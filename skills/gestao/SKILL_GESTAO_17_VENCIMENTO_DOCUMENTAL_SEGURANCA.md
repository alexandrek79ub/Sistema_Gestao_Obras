# 🦺 SKILL GESTÃO 17: Controle de Vencimento — Documentação de Segurança

Complementa a `SKILL_GESTAO_04_SEGURANCA.md` e o `POP_23_SESMT_TREINAMENTOS.md`: eles definem
**quais** documentos são obrigatórios (PGR, PCMSO, LTCAT, ASO, ficha de EPI). Esta skill resolve o
que faltava — **alerta automático de vencimento**, na mesma lógica já usada para retenção de
garantia (`SKILL_GESTAO_10`) e checklist de encerramento (`SKILL_GESTAO_12`).

---

## 1. Documentos Controlados e Periodicidade

| Documento | Nível | Periodicidade/Gatilho de Renovação | Consequência do vencimento |
|---|---|---|---|
| **PGR** (ex-PPRA) | Obra (construtora) e cada empreiteira | Anual, ou a cada mudança relevante de fase da obra | Canteiro operando sem mapeamento de risco vigente — exposição legal direta |
| **PCMSO** | Obra e cada empreiteira | Conforme periodicidade definida pelo próprio PGR (varia por risco) | Funcionário sem exame ocupacional válido não pode estar no canteiro |
| **LTCAT** | Obra | Vinculado à vigência do PGR/mudança de condição ambiental | Base para insalubridade/periculosidade fica desatualizada |
| **ASO** (por trabalhador) | Individual | Conforme exame definido no PCMSO; NR-35/NR-33 exigem campo de aptidão específico | Trabalhador não pode executar a atividade de risco sem ASO válido |
| **Ficha de EPI + CA** | Individual | CA do equipamento tem validade própria (definida pelo fabricante/INMETRO) | EPI com CA vencido não conta como proteção válida |

---

## 2. Registro Mínimo por Documento

| Campo | Descrição |
|---|---|
| Tipo de documento | PGR / PCMSO / LTCAT / ASO / EPI |
| Titular | Obra, empreiteira específica, ou trabalhador individual |
| Data de emissão | |
| Data de vencimento | Calculada pela periodicidade ou informada explicitamente (CA de EPI, por exemplo) |
| Status | Vigente / Vencendo (dentro da janela de alerta) / Vencido |

---

## 3. Janela de Alerta — Antecedência, Não Vencimento Estourado

- **PGR/PCMSO/LTCAT** (documentos de obra/empresa): alertar com **30 dias de antecedência** —
  renovação desses documentos normalmente envolve terceiro (médico do trabalho, técnico de
  segurança), não é feito na hora.
- **ASO individual**: alertar com **15 dias de antecedência** — mais simples de agendar, mas ainda
  exige agendamento de exame.
- **CA de EPI**: alertar com **15 dias de antecedência** — tempo de repor o equipamento antes do
  CA vencer.

**Regra**: a IA nunca deve reportar isso só quando já está vencido — o valor real desta skill é
dar tempo de ação antes do problema virar exposição legal ou parada de atividade por falta de
documento válido.

---

## 4. Cruzamento com Onboarding de Terceiros

O `POP_17_ONBOARDING_TERCEIROS.md` já exige PGR/PCMSO da empreiteira e ASO/EPI do trabalhador **na
entrada**. Esta skill estende isso para o **decorrer da obra**: um trabalhador que entrou com ASO
válido há 11 meses pode estar com o documento vencendo **agora**, sem que ninguém tenha pedido
para verificar de novo. A IA deve tratar a validade como algo a monitorar continuamente, não só
checar uma vez na entrada.

---

## 5. Formato de Saída

```
🦺 STATUS DOCUMENTAL DE SEGURANÇA — [Obra/Empreiteira] — [Data]

🔴 VENCIDOS (ação imediata):
   [Documento, titular, dias vencido]

🟡 VENCENDO (dentro da janela de alerta):
   [Documento, titular, dias restantes]

🟢 VIGENTES: [contagem total]
```

---

## ⚠️ 6. Regras de Ouro

1. Nenhum documento de segurança é reportado só quando já vencido — sempre dentro da janela de
   alerta definida na Seção 3.
2. Trabalhador/empreiteira com documento vencido é sinalizado com prioridade máxima — é o tipo de
   pendência com maior exposição legal do sistema inteiro.
3. Validade é monitorada continuamente ao longo da obra, não só checada no onboarding inicial.
4. Renovação de qualquer documento desta skill gera novo registro com nova data de vencimento —
   histórico anterior é mantido, não sobrescrito (mesma disciplina de versionamento da
   `SKILL_GESTAO_14`).

---
*Trabalha junto com `SKILL_GESTAO_04_SEGURANCA.md`, `POP_23_SESMT_TREINAMENTOS.md` e
`POP_17_ONBOARDING_TERCEIROS.md` (fonte da exigência documental que esta skill monitora ao longo
do tempo).*
