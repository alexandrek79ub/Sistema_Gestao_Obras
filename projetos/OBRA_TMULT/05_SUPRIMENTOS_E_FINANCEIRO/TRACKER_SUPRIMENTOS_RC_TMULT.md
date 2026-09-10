# 📊 PAINEL DE RASTREABILIDADE DE SUPRIMENTOS & TRACKER DE RCs

**Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Porto do Açu (SJB/RJ)
**Módulo de Gestão:** Suprimentos & Governança de Compras (Pipeline Ágil)
**Público-Alvo:** Diretoria, Gestor de Contratos, Engenheiro Residente e Setor de Compras
**Data da Última Atualização:** 10/09/2026 | **Ciclo Atual:** Mês 1 (Partida de Obras)

---

## 🧭 1. O Funil Operacional de Suprimentos (7 Estágios Padronizados)

Para construtoras enxutas, cada compra percorre obrigatoriamente 7 portas de controle para evitar compras erradas, atrasos de canteiro ou furos de caixa:

| Estágio do Funil | O que Significa na Prática? | Quem é o 'Dono da Bola'? | Documento Formal |
| :---: | :--- | :---: | :---: |
| `1. PENDENTE_SUPRIMENTOS` | Obra emitiu a RC técnica com UCC, EAP e data limite no canteiro. | **Comprador** | Requisição de Compra (RC) |
| `2. EM_COTAÇÃO` | Comprador disparou a RC para 3 fornecedores e aguarda propostas. | **Fornecedores** | Pedido de Cotação |
| `3. COTAÇÕES_RECEBIDAS` | Fornecedores responderam; propostas comerciais sob análise. | **Comprador** | Propostas Comerciais |
| `4. MAPA_EQUALIZADO` | Comprador montou o comparativo de preços, frete e saving vs SINAPI. | **Comprador** | Mapa de Cotação |
| `5. EM_APROVAÇÃO_DIRETORIA` | Mapa submetido ao Diretor/Gestor para bater o martelo na alçada da Skill 03. | **Diretoria** | Despacho de Aprovação |
| `6. PEDIDO_EMITIDO_PC` | Fornecedor vencedor contratado e Pedido de Compra formal despachado. | **Suprimentos / Fornecedor** | Pedido de Compra (PC) |
| `7. ENTREGUE_EM_OBRA` | Material descarregado e aprovado pela Engenharia (NF x PC x FVS). | **Engenharia / Almoxarife** | FVS e Canhoto da NF |

---

## 📋 2. Matriz Viva de Rastreabilidade das Requisições de Compra (RCs) — Mês 1

| Nº RC | Pacote de Compra | Data Emissão | Data Limite Canteiro | Estágio Atual no Funil | Responsável Atual | Próxima Ação / Ponto de Atenção | Semáforo Lead Time |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: |
| **RC-001/2026** | Aço CA-50 e CA-60 Cortado e Dobrado (Fundações) | 12/09/2026 | **28/09/2026** | `1. PENDENTE_SUPRIMENTOS` | **Suprimentos (Comprador)** | Disparar cotação formal para Gerdau, ArcelorMittal e Açofer | 🟢 NO PRAZO |
| **RC-002/2026** | Concreto Usinado fck 30 MPa Bombeável e Lastro fck 15 MPa | 14/09/2026 | **01/10/2026** | `1. PENDENTE_SUPRIMENTOS` | **Suprimentos (Comprador)** | Solicitar proposta de fornecimento e bombeamento para Polimix e Supermix | 🟢 NO PRAZO |
| **RC-003/2026** | Compensado Resinado 17mm, Madeiramento e Consumíveis de Fôrma | 12/09/2026 | **26/09/2026** | `1. PENDENTE_SUPRIMENTOS` | **Suprimentos (Comprador)** | Disparar para Madenorte e Madeireira Real Açu (Atenção ao prazo de 14 dias) | 🟡 ATENÇÃO |
| **RC-004/2026** | Locação de Módulos Containers NR-18 e Sanitários Químicos (6 Meses) | 10/09/2026 | **22/09/2026** | `1. PENDENTE_SUPRIMENTOS` | **Suprimentos (Comprador)** | Disparar minuta de contrato para Rentcon e NHJ para entrega urgente no Mês 1 | 🟡 ATENÇÃO |

---

## 📌 3. Quadro Visual Kanban de Suprimentos

```
┌───────────────────────────┬───────────────────────────┬───────────────────────────┐
│ [1] PENDENTE SUPRIMENTOS  │ [2 e 3] COTAÇÃO & PROPOSTA│ [4 e 5] MAPA & APROVAÇÃO  │
├───────────────────────────┼───────────────────────────┼───────────────────────────┤
│ • RC-001 (Aço Fundações)  │ (Nenhuma RC nesta coluna) │ (Aguardando propostas     │
│ • RC-002 (Concreto 30MPa) │                           │  reais para submeter à    │
│ • RC-003 (Fôrmas 17mm)    │                           │  Diretoria)               │
│ • RC-004 (Containers Cnt) │                           │                           │
└───────────────────────────┴───────────────────────────┴───────────────────────────┘
┌───────────────────────────┬───────────────────────────┐
│ [6] PEDIDO EMITIDO (PC)   │ [7] ENTREGUE NA OBRA (FVS)│
├───────────────────────────┼───────────────────────────┤
│ (Aguardando aprovação     │ (Aguardando liberação dos │
│  para emissão dos PCs)    │  pedidos de compra)       │
└───────────────────────────┴───────────────────────────┘
```

---

## 🚨 4. Critérios de Alerta do Semáforo (Lead Time)

- 🟢 **NO PRAZO:** Tempo restante até a necessidade na obra é superior ao dobro do lead time médio de cotação/entrega (sem risco de desabastecimento);
- 🟡 **ATENÇÃO:** Tempo restante entre 1x e 2x o lead time. Exige acompanhamento diário do comprador para cobrança dos orçamentos;
- 🔴 **CRÍTICO:** Tempo restante inferior ao lead time do fornecedor. Risco iminente de paralisar a frente de serviço do canteiro. A Diretoria deve acionar compras emergenciais ou fornecedores locais com pronta entrega.

---

*Painel de Governança mantido automaticamente pelo PMO Virtual A11.*