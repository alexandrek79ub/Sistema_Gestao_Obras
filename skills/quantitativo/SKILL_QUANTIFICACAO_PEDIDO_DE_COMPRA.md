# 🛒 SKILL QUANTIFICAÇÃO: Pedido de Compra com Análise Técnica

Cobre a dor de "pedido de compra feito de achismo" — sem lastro no quantitativo, sem checar se a
etapa da obra já chegou naquele item, e com erro de conversão de unidade. Complementa a
`SKILL_QUANTIFICACAO_MASTER.md` (já tem a regra de UCC — comprar unidade comercial fechada, não
fracionada) e a conciliação de 3 pontas (PO × NF × recebimento) discutida com o usuário.

> **Princípio central**: todo pedido de compra nasce de uma pergunta — *"quanto ainda falta
> comprar deste item, e faz sentido comprar isso agora?"* — nunca de "o mestre de obra pediu".

---

## 1. Saldo a Comprar — a base de todo pedido

```
Saldo a comprar = Quantidade orçada (do quantitativo/CIA)
                   − Quantidade já comprada (soma de pedidos anteriores, não só entregues)
                   − Estoque em canteiro (se houver controle de estoque)
```

- Um pedido de compra **nunca deveria ser gerado maior que o saldo a comprar** sem justificativa
  explícita (ex.: compra antecipada por vencimento de preço, frete consolidado). Se o pedido
  excede o saldo, a IA deve sinalizar 🟡 antes de aprovar/registrar, não deixar passar silencioso.
- Se não existir quantitativo lançado pra aquele item/CIA ainda, o pedido **não tem lastro** —
  marcar 🔴 e pedir confirmação humana antes de seguir, porque não há como validar se a
  quantidade pedida é razoável.

---

## 2. Análise Técnica de Pertinência — o item faz sentido pra etapa atual?

Antes de aprovar/processar um pedido, cruzar contra o cronograma:

| Situação | O que fazer |
|---|---|
| Item pedido corresponde à etapa atual ou à próxima etapa do cronograma (ex.: cimento numa obra em fase de estrutura) | 🟢 Segue normal |
| Item pedido é de etapa **futura distante** (ex.: telha numa obra ainda em fundação) | 🟡 Sinalizar — pode ser compra antecipada estratégica (preço, prazo de entrega longo) ou erro de digitação/pedido — perguntar antes de aprovar |
| Item pedido é de etapa **já concluída e fechada** (ex.: pedir mais forma de fundação numa obra já na alvenaria) | 🔴 Sinalizar com prioridade — forte sinal de erro ou retrabalho não identificado, meritório de investigação |

Essa checagem usa a mesma hierarquia de confiança da `SKILL_GESTAO_07` — nunca bloquear
automaticamente, sempre expor o alerta pra decisão humana, exceto quando a política explícita do
cliente autorizar bloqueio automático de itens fora de etapa.

---

## 3. Conversão de Unidade — erro clássico que passa despercebido

Regra: **toda conversão usada num pedido deve ser registrada explicitamente** (fator e fonte),
nunca aplicada silenciosamente. Casos mais comuns de erro no setor:

| Material | Armadilha comum |
|---|---|
| **Cimento** | Orçado em kg, comprado em saco de 50kg (ou 25kg/40kg dependendo do fornecedor) — confirmar peso do saco daquele fornecedor específico, não assumir 50kg sempre |
| **Aço** | Orçado em kg, comprado em barra de 12m por bitola — peso por metro varia por bitola (tabela de peso linear por diâmetro), nunca assumir peso genérico |
| **Areia/Brita** | Orçado em m³, comprado por "caçamba" ou "viagem de caminhão" — capacidade real varia por transportador e nem sempre é o volume nominal anunciado; exigir conferência de nota fiscal em m³, não confiar só no número de viagens |
| **Concreto usinado** | Pedido em m³, mas perda de lançamento (sobra de caminhão, limpeza de calha) precisa ser considerada — não é erro de conversão, é perda técnica esperada, documentar separado |
| **Tinta** | Orçada por m² de área a pintar, comprada em litros — depende do rendimento por demão declarado pelo fabricante daquela tinta específica, não de um rendimento genérico de mercado |

**Regra de ouro**: se a IA não tem certeza do fator de conversão correto pra aquele fornecedor/
produto específico, ela **pergunta**, não aplica um fator "típico" e apresenta como exato — um
fator de conversão errado se propaga silenciosamente pra todo o quantitativo e o orçamento.

---

## 4. Formato de Saída — Pedido de Compra Analisado

```
🛒 PEDIDO DE COMPRA — [Item] — [Data]

1. SALDO A COMPRAR
   Orçado: [X] | Já comprado: [Y] | Estoque: [Z] | Saldo: [X-Y-Z]

2. QUANTIDADE PEDIDA vs. SALDO
   [🟢 dentro do saldo / 🟡 excede saldo — justificar / 🔴 sem lastro no quantitativo]

3. ADERÊNCIA À ETAPA DO CRONOGRAMA
   [🟢 / 🟡 / 🔴 conforme Seção 2]

4. CONVERSÃO DE UNIDADE APLICADA
   [Fator usado + fonte — ex.: "1 saco = 50kg, conforme especificação do fornecedor X"]

5. RECOMENDAÇÃO
   [Aprovar / Aprovar com ressalva / Pausar para confirmação humana]
```

---

## ⚠️ 5. Regras de Ouro

1. Nenhum pedido é processado sem cálculo explícito do saldo a comprar contra o quantitativo.
2. Pedido de item de etapa já concluída é sempre sinalizado com prioridade alta — é o indício mais
   forte de erro ou retrabalho oculto.
3. Toda conversão de unidade usada é registrada com fator e fonte — nunca aplicada silenciosamente.
4. Na dúvida sobre fator de conversão específico do fornecedor, a IA pergunta — não assume um
   valor "típico de mercado" e apresenta como exato.
5. Excesso sobre o saldo a comprar sempre gera alerta, mesmo que a compra seja tecnicamente
   justificável (antecipação estratégica) — a decisão de aceitar isso é humana, não automática.

---
*Este módulo trabalha junto com `SKILL_QUANTIFICACAO_MASTER.md` (regra de UCC e fonte do
quantitativo orçado) e com a lógica de conciliação de 3 pontas (Pedido × Nota Fiscal ×
Recebimento) já definida para o fluxo de compras.*
