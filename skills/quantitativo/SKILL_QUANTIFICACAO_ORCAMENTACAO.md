# 💵 SKILL QUANTIFICAÇÃO: Orçamentação (CCU + BDI)

Transforma a **quantidade** já produzida pela `SKILL_QUANTIFICACAO_MASTER` em **valor (R$)** —
etapa que faltava para fechar o ciclo completo do quantitativo. O link entre as duas skills é o
**código CIA**: toda linha do quantitativo já carrega o CIA do elemento; a orçamentação usa esse
mesmo código como chave para buscar o custo unitário correspondente.

---

## 1. O Link — Código CIA como Chave Única

```
Quantitativo (SKILL_QUANTIFICACAO_MASTER)      Tabela de Custo Unitário (CCU)
┌─────────┬──────────────┬───────────┐         ┌─────────┬───────────────────┐
│ CIA     │ Descrição    │ Quantidade│   ──►   │ CIA     │ Custo Unitário R$  │
│ 02.01.03│ Alvenaria    │ 145 m²    │  match  │ 02.01.03│ 68,40              │
└─────────┴──────────────┴───────────┘  por CIA└─────────┴───────────────────┘
```

- Nenhuma quantidade é orçada sem que exista uma linha correspondente na tabela de CCU com o
  **mesmo código CIA** — se não houver match, a IA sinaliza 🔴 (custo não definido para este
  item), nunca estima um valor "de cabeça" para preencher a lacuna.
- Se o CIA do quantitativo tiver um nível de detalhe que a tabela de CCU não tem (ex.:
  quantitativo por ambiente, CCU só por tipo de serviço agregado), a IA deve agregar a
  quantidade ao nível que a CCU suporta antes de multiplicar — nunca aplicar o custo unitário
  errado por descuido de nível hierárquico.

---

## 2. De Onde Vem o Custo Unitário (CCU) — Ordem de Prioridade

1. **Histórico da própria empresa** (cotação real recente, mesmo fornecedor/região) — mais
   confiável, reflete a realidade de compra atual.
2. **SINAPI/TCPO como referência de mercado** — usar quando não há histórico próprio, sempre
   declarando a data-base da tabela usada (preço de referência desatualizado é uma fonte comum de
   erro silencioso).
3. **Nunca "estimar" custo unitário sem fonte** — se não há nem histórico nem referência
   disponível para um item, a IA para e pede ao usuário, marcando esse CIA como pendente na
   aba de premissas do orçamento.

---

## 3. Composição do Custo Unitário — Não é Só o Material

Cada custo unitário, idealmente, é decomposto em:

| Componente | Descrição |
|---|---|
| Material | Custo do insumo, incluindo índice de perda de referência (`SKILL_GESTAO_08`, Seção 3.1) já embutido |
| Mão de obra | Custo de Hh × RUP de referência (link natural com `SKILL_GESTAO_08`, Seção 1.2) |
| Equipamento | Se aplicável ao serviço (ex.: betoneira, grua) |

Quando a CCU está disponível só como valor único (sem essa decomposição), a orçamentação segue
normalmente, mas a IA deve registrar essa limitação — orçamento sem decomposição não permite
análise de desvio por componente depois (não dá pra saber se o estouro veio de material ou mão de
obra).

---

## 4. BDI (Bonificação e Despesas Indiretas)

```
Valor final do item = (Quantidade × Custo Unitário Direto) × (1 + BDI%)
```

- BDI é aplicado **sobre o custo direto total**, nunca item a item de forma isolada com taxas
  diferentes sem justificativa — inconsistência de BDI entre itens é sinal de erro de planilha.
- O percentual de BDI usado deve ser sempre declarado explicitamente no orçamento final (não
  fica "escondido" dentro do preço) — é prática de mercado e facilita auditoria/negociação.

---

## 5. Formato de Saída — Orçamento Vinculado ao Quantitativo

```
💵 ORÇAMENTO — [CIA] — [Descrição]

Quantidade (do quantitativo): [valor + unidade]
Custo unitário direto: [R$] — Fonte: [histórico próprio / SINAPI data-base X / etc.]
Custo direto total: [Quantidade × Custo unitário]
BDI aplicado: [%]
Valor final do item: [Custo direto × (1+BDI)]

⚠️ Itens sem custo unitário definido: [lista de CIAs pendentes, se houver]
```

---

## ⚠️ 6. Regras de Ouro

1. Todo item orçado tem rastreabilidade até a linha exata do quantitativo que gerou a
   quantidade (mesmo CIA) — orçamento nunca existe desconectado do quantitativo que o originou.
2. Nenhum custo unitário é estimado sem fonte declarada (histórico próprio ou referência com
   data-base) — ausência de fonte gera pendência, não estimativa.
3. BDI é sempre declarado explicitamente, nunca embutido silenciosamente no preço unitário.
4. Mudança de revisão do quantitativo (`SKILL_GESTAO_14`) que altera quantidade deve refletir
   automaticamente no orçamento vinculado — orçamento não fica "congelado" enquanto o
   quantitativo muda por baixo.

---
*Trabalha junto com `SKILL_QUANTIFICACAO_MASTER.md` (fonte da quantidade, via código CIA),
`SKILL_GESTAO_08_PRODUTIVIDADE_E_RECURSOS.md` (RUP como componente de mão de obra do CCU) e
`SKILL_GESTAO_14_CONTROLE_DE_REVISAO.md` (propagação de mudança de quantidade).*
