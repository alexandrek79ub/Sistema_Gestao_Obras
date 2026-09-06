# 🔗 SKILL QUANTIFICAÇÃO: Conciliação de 3 Pontas (Pedido × Nota Fiscal × Recebimento)

Formaliza o fluxo principal de entrada de material discutido com o usuário: quando existe um
pedido de compra vinculado, a tarefa do agente é **conciliar**, não classificar do zero. Trabalha
junto com `SKILL_QUANTIFICACAO_PEDIDO_DE_COMPRA.md` (que cobre o pedido em si) e a Hierarquia de
Afirmações da `SKILL_GESTAO_07`.

---

## 1. As Três Pontas

| Ponta | O que confirma |
|---|---|
| **Pedido de Compra (PO)** | O que foi solicitado — item, quantidade, preço negociado, centro de custo/CIA |
| **Nota Fiscal (NF)** | O que o fornecedor diz ter entregue — item, quantidade, preço cobrado |
| **Recebimento físico** | O que **de fato** chegou na obra, conferido por alguém no canteiro — não é automático só porque a NF chegou |

**Regra central**: só se considera a compra "fechada" quando as três pontas batem. NF sem
confirmação de recebimento físico é uma ponta em aberto, não uma conclusão.

---

## 2. Fluxo Principal — Match Direto

Quando PO existe e é claro:

1. Casar NF ao PO por fornecedor + itens + faixa de valor esperada.
2. Se **item, quantidade e preço batem** dentro de uma margem razoável (definir tolerância, ex.:
   ±2% por arredondamento) → 🟢 concilia automaticamente, usa o CIA já definido no PO.
3. Se houver **mais de um PO aberto para o mesmo fornecedor ao mesmo tempo** → não escolher pelo
   nome do fornecedor sozinho; casar por data mais próxima + itens mais compatíveis, e se ainda
   houver ambiguidade real, marcar 🟡 e perguntar.

---

## 3. Exceções — Sempre Sinalizar, Nunca Fechar Silenciosamente

| Exceção | Tratamento |
|---|---|
| **Entrega parcial** (NF com quantidade menor que o PO) | PO permanece "parcialmente atendido" — saldo continua em aberto para a próxima entrega, nunca fechado como concluído |
| **Divergência de preço** (NF cobra valor diferente do negociado no PO) | 🟡/🔴 conforme o tamanho do desvio — sempre gera alerta, nunca é absorvido silenciosamente no custo do CIA (contamina o CPI do serviço, ver `SKILL_GESTAO_07`) |
| **Item substituído** (fornecedor entrega material similar, não o exato do PO) | 🔴 — exige confirmação humana; agente não decide sozinho se o substituto é aceitável tecnicamente |
| **NF sem PO correspondente** | Cai no fluxo de "classificação do zero" da `SKILL_QUANTIFICACAO_PEDIDO_DE_COMPRA` (compra emergencial/informal) — tratado como exceção, não como regra geral |
| **Recebimento físico não confirmado** | Compra permanece em aberto mesmo com NF e PO batendo — a conferência física é a ponta que efetivamente autoriza o lançamento como material disponível em obra |

---

## 4. Formato de Saída

```
🔗 CONCILIAÇÃO — NF [número] — [Data]

PO vinculado: [número ou "não encontrado"]
Match de item/quantidade/preço: [🟢 total / 🟡 parcial — detalhar / 🔴 divergente — detalhar]
Recebimento físico confirmado: [sim/não/pendente]
Status final: [Fechado / Parcialmente atendido — saldo em aberto / Pendente de confirmação humana]
```

---

## ⚠️ 5. Regras de Ouro

1. NF nunca fecha uma compra sozinha — precisa do recebimento físico confirmado.
2. Divergência de preço entre PO e NF nunca é absorvida silenciosamente no custo do serviço —
   sempre gera alerta visível.
3. Entrega parcial mantém o PO com saldo em aberto, nunca é tratada como pedido concluído.
4. Múltiplos PO abertos para o mesmo fornecedor exigem match por data+itens, nunca só por nome do
   fornecedor.
5. Esta skill segue o mesmo nível de autonomia definido no `ADENDO_AGENTS_REGRAS_DE_AUTONOMIA.md`
   — match 🟢 é autônomo, tudo abaixo disso exige pausa.

---
*Trabalha junto com `SKILL_QUANTIFICACAO_PEDIDO_DE_COMPRA.md`, `SKILL_GESTAO_07_CIENCIA_DE_DADOS.md`
e `ADENDO_AGENTS_REGRAS_DE_AUTONOMIA.md`.*
