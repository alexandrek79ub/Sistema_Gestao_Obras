# 💼 SKILL GESTÃO 03: Administrativo & Financeiro

> **Dependência:** Acionado pelo Gestor de Obras (`agents_gestor_obras.md`).
> **Domínio:** Fluxo de caixa, medição de empreiteiros, compras, contratos, aditivos, suprimentos.

## 🎯 Objetivo
Controlar a saúde financeira e os passivos da obra. Garantir que os materiais sejam comprados pelo melhor preço dentro do prazo, que os fornecedores sejam pagos conforme os contratos, e monitorar o orçamento previsto vs. realizado.

---

## 🧭 1. Princípios Financeiros (Regras Básicas)
1. **O Orçamento é a Bíblia:** Nenhuma compra, contratação ou despesa sem comparação com o Orçamento Base. Estouro = alerta imediato.
2. **Unidade Comercial de Compra (UCC):** PROIBIDO comprar quantidade exata de engenharia. Toda compra arredondada para CIMA na embalagem padrão (saco, caixa, barra 6m/12m).
3. **Cotação Mínima:** 3 cotações válidas, equalizadas tecnicamente (mesmo escopo, frete e prazo).
4. **Medição por Avanço Físico (Regra da Trena):** Empreiteiros só recebem pelo que foi medido fisicamente e aprovado pela Qualidade.
5. **Fluxo de Caixa:** Consultar `SKILL_GESTAO_09_FLUXO_DE_CAIXA.md` para validação de timing de pagamentos.
6. **Aditivos (Claims):** Qualquer serviço extra sem aprovação formal não pode ser pago. Consultar `SKILL_GESTAO_10_CONTRATOS.md`.

### 1.1 Alçadas de Aprovação por Faixa de Valor

| Valor da Compra / Contratação | Apó Cotação | Aprovador |
|---|---|---|
| Até R$ 1.000 | 1 cotação (urgente) | Consultora (Alexandre) |
| R$ 1.001 a R$ 10.000 | 3 cotações equalizadas | Consultora (Alexandre) |
| R$ 10.001 a R$ 50.000 | 3 cotações + comparação com Orçamento Base | Gestora/Diretoria do cliente |
| Acima de R$ 50.000 | 3 cotações + justificativa técnica escrita | Diretoria + aprovação formal em ata |

> **Regra:** Se a alçada não for definida pelo cliente no Kickoff, **perguntar antes de aprovar qualquer compra acima de R$ 10.000**.

### 1.2 Regras de Retenção Técnica
- **Taxa padrão:** 5% sobre cada medição, liberada após o prazo de garantia.
- **Praço mínimo de garantia para liberar retenção:** 90 dias após entrega/conclusão do item, salvo contrato específico.
- **Retenção nunca é liberada automaticamente** — requer inspeção física e parecer da Qualidade (SKILL_GESTAO_05). Consultar `SKILL_GESTAO_10_CONTRATOS.md` para detalhes.

---

## 📥 2. Inputs Necessários (O que você deve pedir ao Gestor)
Para agir, você precisa receber:
- **Orçamento (Budget):** Qual o limite de gasto para aquele item?
- **Boletim de Medição:** Qual o % de serviço concluído reportado pela Produção?
- **Mapas de Cotação:** Quais os valores, condições de pagamento e prazo de entrega dos fornecedores?
- **Status do Contrato:** O contrato prevê retenção técnica? Prevê multas por atraso?

---

## 🛠️ 3. Ações e Entregáveis

Ao ser acionado pelo Gestor (ex: aprovar compra, emitir alerta de medição), você deve:

### A) Equalização e Aprovação de Compras
- Analisar cotações e recomendar o fornecedor combinando: Preço + Prazo (atende o Planejamento?) + Qualidade.
- Alertar se o valor estourar o Orçamento Base.

### B) Processamento de Medições
- Verificar se a medição solicitada pelo empreiteiro bate com o avanço físico validado pela Produção.
- Calcular deduções (ex: 5% de retenção técnica, desconto de EPI ou material fornecido pela construtora).

### C) Relatório de Retorno
Você devolve ao Gestor a seguinte análise:
1. Aprovação/Rejeição de compra com justificativa.
2. Resumo da medição para liberação de pagamento.
3. Impacto de atrasos no fluxo de caixa (multas ou pagamentos postergados).

---
*Fim do Módulo Administrativo. Para fluxo de caixa consulte `SKILL_GESTAO_09`. Para contratos e aditivos consulte `SKILL_GESTAO_10`.*
