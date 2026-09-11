# 📑 PLANO MESTRE DE CENTROS DE CUSTO & APROPRIAÇÃO CONTÁBIL

**Empreendimento:** Residencial Alpha — Condomínio Fechado (220.0 m²)
**Função:** Rastreabilidade unívoca de Requisições de Compra (RC), Pedidos de Compra (PC) e Notas Fiscais (NF-e)
**Padrão do Ecossistema:** SKILL_QUANTIFICACAO_CONCILIACAO_3_PONTAS & SKILL_GESTAO_03_ADMINISTRATIVO

---

## 🎯 1. Por que o Centro de Custo (CC) é Obrigatório na RC e no PC?

Em construtoras organizadas, **nenhum material é comprado e nenhuma nota fiscal é paga** sem a indicação formal do Centro de Custo:
1. **Eliminação do 'Lixo Contábil':** Impede que o financeiro jogue notas de concreto ou aço em 'Despesas Gerais de Obra';
2. **Orçado vs. Realizado em Tempo Real:** Permite ao Diretor confrontar na hora se a despesa lançada na NF-e está estourando a verba orçada daquela EAP;
3. **Conciliação de 3 Pontas Automática:** Quando o fornecedor emite a NF-e com o número do Pedido de Compra e o Centro de Custo no corpo da nota, o sistema confere e aprova o pagamento com segurança máxima.

---

## 📊 2. Estrutura Canônica de Centros de Custo (EAP × CC × Contabilidade)

| Centro de Custo (CC) | Nível | Descrição / Objeto da Despesa | EAP Vinculada | Natureza de Gasto | Conta Contábil |
| :---: | :---: | :--- | :---: | :--- | :---: |
| **`CC-100`** | Sintético | **CANTEIRO DE OBRAS & ADMINISTRAÇÃO LOCAL** | `1.0` | Custo Direto Canteiro | `4.1.1.01` |
| `CC-101` | Analítico | Gestão Técnica de Obra (Eng. Residente e Mestre) | `1.0.1` | Mão de Obra Indireta | `4.1.1.01.01` |
| `CC-102` | Analítico | Apoio e Segurança (TST, Almoxarife, Vigia) | `1.0.2` | Mão de Obra Indireta | `4.1.1.01.02` |
| `CC-103` | Analítico | Locação de Containers Habitáveis e Sanitários Químicos | `1.0.3` | Locação de Equipamentos | `4.1.1.01.03` |
| `CC-104` | Analítico | Contas de Consumo Canteiro (Energia, Água Pipa, Fibra) | `1.0.4` | Utilidades e Serviços | `4.1.1.01.04` |
| `CC-105` | Analítico | Vivência, Alimentação (16 operários) e Transporte | `1.0.5` | Benefícios Operacionais | `4.1.1.01.05` |
| `CC-106` | Analítico | SST, PGR/PCMSO, EPIs, Caçambas e Apoio | `1.0.6` | Segurança e Descarte | `4.1.1.01.06` |

---
*Plano auditado e vinculado à Linha de Base e Governança do Ecossistema.*