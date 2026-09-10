# 📊 PAINEL VIVO DE SUPRIMENTOS & TRACKER DE RCs (OBRA_TMULT)

> **Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Porto do Açu  
> **Ciclo Ativo:** Mês 1 (Partida da Obra) | **Horizonte Monitorado:** 24 Requisições de Compra (M1 a M6)  
> **Data da Atualização:** 10/09/2026 | **Governança:** Skill Gestão 03 & POP 05

---

## 🧭 1. Funil Kanban de Suprimentos (Status Atual das 24 RCs)

```
┌────────────────────────────┬────────────────────────────┬────────────────────────────┐
│ [1] PENDENTE SUPRIMENTOS   │ [2 e 3] COTAÇÃO & PROPOSTA │ [4 e 5] MAPA & APROVAÇÃO   │
├────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ • RC-001 (Aço Fundações)   │ (Nenhuma RC nesta coluna)  │ (Aguardando propostas      │
│ • RC-002 (Concreto 30MPa)  │                            │  reais para submeter à     │
│ • RC-003 (Fôrmas 17mm)     │                            │  Diretoria)                │
│ • RC-004 (Containers Cnt)  │                            │                            │
└────────────────────────────┴────────────────────────────┴────────────────────────────┘
┌────────────────────────────┬────────────────────────────┬────────────────────────────┐
│ [6] PEDIDO EMITIDO (PC)    │ [7] ENTREGUE NA OBRA (FVS) │ [0] PLANEJADAS (M2 A M6)   │
├────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ (Aguardando aprovação      │ (Aguardando liberação      │ • 20 RCs (RC-005 a RC-024) │
│  para emissão dos PCs)     │  dos pedidos de compra)    │   com datas gatilho travadas│
└────────────────────────────┴────────────────────────────┴────────────────────────────┘
```

---

## 📋 2. Matriz Viva de Rastreabilidade das 24 RCs

| Nº RC | Pacote de Insumo | Centro de Custo | Data Gatilho | Entrega no Canteiro | Estágio Atual no Funil | Responsável Atual | Próxima Ação / Ponto Crítico | Semáforo |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **RC-001/2026** | Aço CA-50/60 Cortado e Dobrado (Fundações e Baldrames) | `CC-208 / CC-209 / CC-210` | 12/09/2026 | **28/09/2026** | `1. PENDENTE_SUPRIMENTOS` | **Suprimentos (Comprador)** | Disparar para 3 fornecedores cadastrados | 🟢 NO PRAZO |
| **RC-002/2026** | Concreto Usinado fck 30 MPa Bombeável e Lastro fck 15 MPa | `CC-202 / CC-203 / CC-205 / CC-206` | 14/09/2026 | **01/10/2026** | `1. PENDENTE_SUPRIMENTOS` | **Suprimentos (Comprador)** | Disparar para 3 fornecedores cadastrados | 🟢 NO PRAZO |
| **RC-003/2026** | Compensado Resinado 17mm, Pontaletes e Consumíveis de Fôrma | `CC-204 / CC-205 / CC-207` | 12/09/2026 | **26/09/2026** | `1. PENDENTE_SUPRIMENTOS` | **Suprimentos (Comprador)** | Disparar para 3 fornecedores cadastrados | 🟡 ATENÇÃO |
| **RC-004/2026** | Locação de Módulos Habitáveis Containers NR-18 e Sanitários Químicos | `CC-103` | 10/09/2026 | **22/09/2026** | `1. PENDENTE_SUPRIMENTOS` | **Suprimentos (Comprador)** | Disparar para 3 fornecedores cadastrados | 🟡 ATENÇÃO |
| **RC-005/2026** | Cimbramento e Escoramento Metálico Ajustável | `CC-302` | 05/10/2026 | **25/10/2026** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 05/10/2026 | ⚪ PLANEJADO |
| **RC-006/2026** | Vigotas Treliçadas Pré-moldadas TR 16745 e EPS H12 | `CC-303` | 08/10/2026 | **28/10/2026** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 08/10/2026 | ⚪ PLANEJADO |
| **RC-007/2026** | Aço CA-50/60 Cortado e Dobrado (Pilares P1-P24 e Vigas V101-V115) | `CC-304` | 10/10/2026 | **30/10/2026** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 10/10/2026 | ⚪ PLANEJADO |
| **RC-008/2026** | Concreto Usinado fck 30 MPa Bombeável (Pilares, Vigas e Capa da Laje) | `CC-305` | 15/10/2026 | **05/11/2026** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 15/10/2026 | ⚪ PLANEJADO |
| **RC-009/2026** | Blocos de Concreto Estrutural/Vedação B144 (14x19x39cm) | `CC-401` | 20/10/2026 | **15/11/2026** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 20/10/2026 | ⚪ PLANEJADO |
| **RC-010/2026** | Cimento Portland CP II-E-32, Areia Média Lavada e Aditivos | `CC-402` | 02/11/2026 | **18/11/2026** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 02/11/2026 | ⚪ PLANEJADO |
| **RC-011/2026** | Locação de Andaimes Tubulares Fachadeiros c/ Guarda-Corpo | `CC-403` | 08/11/2026 | **25/11/2026** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 08/11/2026 | ⚪ PLANEJADO |
| **RC-012/2026** | Telhas Termoacústicas Sandwich PIR e Calhas Metálicas Galvanizadas | `CC-501` | 15/10/2026 | **28/11/2026** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 15/10/2026 | ⚪ PLANEJADO |
| **RC-013/2026** | Tubulações e Conexões PVC Rígido Água Fria e Esgoto Predial | `CC-601` | 20/11/2026 | **15/12/2026** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 20/11/2026 | ⚪ PLANEJADO |
| **RC-014/2026** | Eletrodutos Rígidos Roscáveis, Caixas 4x2 e Caixas de Passagem | `CC-604` | 25/11/2026 | **18/12/2026** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 25/11/2026 | ⚪ PLANEJADO |
| **RC-015/2026** | Argamassa Industrializada de Projeção para Emboço Paulista | `CC-405` | 01/12/2026 | **20/12/2026** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 01/12/2026 | ⚪ PLANEJADO |
| **RC-016/2026** | Esquadrias de Alumínio Anodizado Preto e Vidros Temperados | `CC-702` | 01/11/2026 | **10/01/2027** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 01/11/2026 | ⚪ PLANEJADO |
| **RC-017/2026** | Porcelanato Esmaltado Retificado 60x60cm e Argamassa AC-III | `CC-704` | 10/12/2026 | **15/01/2027** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 10/12/2026 | ⚪ PLANEJADO |
| **RC-018/2026** | Kits Porta Pronta de Madeira Melamínica com Fechaduras Inox | `CC-701` | 05/12/2026 | **20/01/2027** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 05/12/2026 | ⚪ PLANEJADO |
| **RC-019/2026** | Cabos Elétricos de Cobre Flexível 750V / 1kV (1,5 a 50 mm²) | `CC-605` | 05/01/2027 | **25/01/2027** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 05/01/2027 | ⚪ PLANEJADO |
| **RC-020/2026** | Quadros QDG/QDF, Disjuntores DIN, DPS, Tomadas e Interruptores | `CC-606` | 10/01/2027 | **28/01/2027** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 10/01/2027 | ⚪ PLANEJADO |
| **RC-021/2026** | Louças Sanitárias, Cubas de Inox e Metais com Sensor/Pressômetro | `CC-603` | 20/01/2027 | **15/02/2027** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 20/01/2027 | ⚪ PLANEJADO |
| **RC-022/2026** | Aparelhos de Ar-Condicionado Split Inverter (12k a 24k BTU) e Tubulação | `CC-608` | 05/01/2027 | **20/02/2027** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 05/01/2027 | ⚪ PLANEJADO |
| **RC-023/2026** | Tintas Acrílicas Laváveis Premium, Selador Acrílico e Massa PVA | `CC-706` | 25/01/2027 | **18/02/2027** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 25/01/2027 | ⚪ PLANEJADO |
| **RC-024/2026** | Limpeza Fina Pós-Obra, Testes Globais e Desmobilização Geral | `CC-105` | 05/02/2027 | **25/02/2027** | `0. PLANEJADO` | **Engenharia (Campo)** | Aguardar gatilho em 05/02/2027 | ⚪ PLANEJADO |

---

*Tracker atualizado e integrado ao ERP e ao Cronograma Físico-Financeiro.*