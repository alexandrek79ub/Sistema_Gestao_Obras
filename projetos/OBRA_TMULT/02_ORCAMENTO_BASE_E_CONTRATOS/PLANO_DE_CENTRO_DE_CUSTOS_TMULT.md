# 📑 PLANO MESTRE DE CENTROS DE CUSTO & APROPRIAÇÃO CONTÁBIL

**Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Porto do Açu (SJB/RJ)
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
| **`CC-200`** | Sintético | **INFRAESTRUTURA & FUNDAÇÕES** | `1.1` | Custo Direto Físico | `4.1.2.01` |
| `CC-201` | Analítico | Escavação Mecanizada/Manual e Compactação de Valas | `1.1.1 e 1.1.2` | Serviço de Terraplenagem | `4.1.2.01.01` |
| `CC-202` | Analítico | Lastro de Concreto Magro fck 15 MPa (e=5cm) | `1.1.3` | Material - Concreto | `4.1.2.01.02` |
| `CC-203` | Analítico | Concreto Usinado fck 30 MPa - Sapatas Isoladas | `1.1.4` | Material - Concreto Usinado | `4.1.2.01.03` |
| `CC-204` | Analítico | Fôrmas Compensado 17mm - Sapatas Isoladas | `1.1.5` | Material - Madeira e Fôrmas | `4.1.2.01.04` |
| `CC-205` | Analítico | Concreto e Fôrmas - Arranques de Pilares P1-P24 | `1.1.6 e 1.1.7` | Material - Concreto e Fôrmas | `4.1.2.01.05` |
| `CC-206` | Analítico | Concreto Usinado fck 30 MPa - Vigas Baldrames | `1.1.8` | Material - Concreto Usinado | `4.1.2.01.06` |
| `CC-207` | Analítico | Fôrmas Compensado 17mm - Vigas Baldrames (140m) | `1.1.9` | Material - Madeira e Fôrmas | `4.1.2.01.07` |
| `CC-208` | Analítico | Armadura CA-50 Cortada/Dobrada - Sapatas Isoladas | `1.1.10` | Material - Aço Estrutural | `4.1.2.01.08` |
| `CC-209` | Analítico | Armadura CA-50 Cortada/Dobrada - Arranques de Pilares | `1.1.11` | Material - Aço Estrutural | `4.1.2.01.09` |
| `CC-210` | Analítico | Armadura CA-50 Cortada/Dobrada - Vigas Baldrames | `1.1.12` | Material - Aço Estrutural | `4.1.2.01.10` |
| `CC-211` | Analítico | Impermeabilização Tinta Asfáltica (Baldrames e Sapatas) | `1.1.13` | Material - Impermeabilizantes | `4.1.2.01.11` |
| `CC-212` | Analítico | Reaterro Compactado e Bota-Fora de Cavas | `1.1.14 e 1.1.15` | Serviço de Terraplenagem | `4.1.2.01.12` |
| **`CC-300`** | Sintético | **SUPRAESTRUTURA (PILARES, VIGAS E LAJES)** | `1.2` | Custo Direto Físico | `4.1.2.02` |
| `CC-301` | Analítico | Concreto Usinado fck 30 MPa - Pilares P1 a P24 | `1.2.1` | Material - Concreto Usinado | `4.1.2.02.01` |
| `CC-302` | Analítico | Fôrmas Compensado 17mm - Pilares P1 a P24 | `1.2.2` | Material - Madeira e Fôrmas | `4.1.2.02.02` |
| `CC-303` | Analítico | Concreto Usinado fck 30 MPa - Vigas Superiores e Cobertura | `1.2.3` | Material - Concreto Usinado | `4.1.2.02.03` |
| `CC-304` | Analítico | Fôrmas Compensado 17mm - Vigas Superiores | `1.2.4` | Material - Madeira e Fôrmas | `4.1.2.02.04` |
| `CC-305` | Analítico | Concreto Usinado fck 30 MPa - Capa de Laje Treliçada e=5cm | `1.2.5` | Material - Concreto Usinado | `4.1.2.02.05` |
| `CC-306` | Analítico | Fôrmas e Escoramento Metálico - Lajes e Vigas | `1.2.6 e 1.2.7` | Locação de Equipamentos / Fôrma | `4.1.2.02.06` |
| `CC-307` | Analítico | Vigotas Treliçadas TR 16745 e EPS para Lajes H12 | `1.2.8 e 1.2.9` | Material - Laje Premoldada | `4.1.2.02.07` |
| `CC-308` | Analítico | Armadura CA-50 Pilares e Vigas + CA-60 Lajes | `1.2.10 e 1.2.11` | Material - Aço Estrutural | `4.1.2.02.08` |
| **`CC-400`** | Sintético | **ARQUITETURA, ALVENARIAS E ACABAMENTOS** | `2.1` | Custo Direto Físico | `4.1.2.03` |
| `CC-401` | Analítico | Alvenaria de Vedação (Blocos de Concreto 14x19x39) | `2.1.1` | Material - Blocos e Argamassas | `4.1.2.03.01` |
| `CC-402` | Analítico | Chapisco e Emboço/Reboco Paulista 20mm | `2.1.2 e 2.1.3` | Material/MO Revestimentos | `4.1.2.03.02` |
| `CC-403` | Analítico | Contrapiso e Porcelanato Retificado 60x60cm | `2.1.4, 2.1.5 e 2.1.7` | Material - Pisos e Argamassas | `4.1.2.03.03` |
| `CC-404` | Analítico | Revestimento Cerâmico de Paredes WCs (45x45) | `2.1.6` | Material - Cerâmica e Argamassa | `4.1.2.03.04` |
| `CC-405` | Analítico | Pintura Látex Acrílica 3 Demãos (Paredes e Tetos) | `2.1.8` | Material - Tintas e Acessórios | `4.1.2.03.05` |
| `CC-406` | Analítico | Esquadrias de Madeira (Portas P1 a P5 completas) | `2.1.9` | Material - Esquadrias Madeira | `4.1.2.03.06` |
| `CC-407` | Analítico | Esquadrias de Alumínio e Vidro (Janelas J1 a J4) | `2.1.10` | Material - Esquadrias Alumínio | `4.1.2.03.07` |
| `CC-408` | Analítico | Impermeabilização Polimérica WCs e Copa | `2.1.11` | Material - Impermeabilizantes | `4.1.2.03.08` |
| **`CC-500`** | Sintético | **COBERTURA, ESTRUTURA METÁLICA E CALHAS** | `2.2` | Custo Direto Físico | `4.1.2.04` |
| `CC-501` | Analítico | Telhas Termoacústicas Sandwich EPS 30mm | `2.2.1` | Material - Cobertura | `4.1.2.04.01` |
| `CC-502` | Analítico | Estrutura Metálica de Apoio (Terças Perfil U) | `2.2.2 e 2.2.3` | Material - Perfis Metálicos | `4.1.2.04.02` |
| `CC-503` | Analítico | Calhas, Rufos e Impermeabilização com Manta 4mm | `2.2.4 a 2.2.7` | Material - Calhas e Mantas | `4.1.2.04.03` |
| `CC-504` | Analítico | Alvenaria e Revestimento de Platibanda | `2.2.8 a 2.2.10` | Material/MO Platibanda | `4.1.2.04.04` |
| **`CC-600`** | Sintético | **INSTALAÇÕES ELÉTRICAS, CABEAMENTO E TELECOM** | `3.1 e 3.3` | Custo Direto Físico | `4.1.2.05` |
| `CC-601` | Analítico | Cabos de Cobre, Eletrodutos e Caixas de Embutir | `3.1.1 a 3.1.7` | Material - Elétrica Básica | `4.1.2.05.01` |
| `CC-602` | Analítico | Quadros QDG/QDF, Disjuntores DIN, DR e DPS | `3.1.8 e 3.1.10` | Material - Dispositivos Elétricos | `4.1.2.05.02` |
| `CC-603` | Analítico | Interruptores, Tomadas e Luminárias LED 60x60 | `3.1.9 e 3.1.11` | Material - Acabamento Elétrico | `4.1.2.05.03` |
| `CC-604` | Analítico | Cabeamento Estruturado Cat6, Rack 12U e Switch | `3.3.1 a 3.3.4` | Material - Redes e Telecom | `4.1.2.05.04` |
| **`CC-700`** | Sintético | **INSTALAÇÕES HIDROSSANITÁRIAS E PLUVIAIS** | `3.2` | Custo Direto Físico | `4.1.2.06` |
| `CC-701` | Analítico | Tubos e Conexões PVC Água Fria, Esgoto e Ventilação | `3.2.1 a 3.2.8` | Material - Tubulações PVC | `4.1.2.06.01` |
| `CC-702` | Analítico | Registros de Gaveta/Pressão e Caixas de Gordura | `3.2.9 e 3.2.10` | Material - Válvulas e Caixas | `4.1.2.06.02` |
| `CC-703` | Analítico | Louças Sanitárias, Cubas, Torneiras e Acessórios | `3.2.11 e 3.2.12` | Material - Louças e Metais | `4.1.2.06.03` |
| `CC-704` | Analítico | Reservatórios de Polietileno 5.000L | `3.2.13` | Material - Reservatórios | `4.1.2.06.04` |
| **`CC-800`** | Sintético | **CLIMATIZAÇÃO E HVAC** | `4.1` | Custo Direto Físico | `4.1.2.07` |
| `CC-801` | Analítico | Aparelhos Split Cassete 36.000 e Hi-Wall Inverter | `4.1.1 e 4.1.2` | Equipamentos de Climatização | `4.1.2.07.01` |
| `CC-802` | Analítico | Linhas Frigorígenas, Cobre e Instalação HVAC | `4.1.3` | Serviço Especializado HVAC | `4.1.2.07.02` |

---

## 🛒 3. Centros de Custo Aplicados aos Suprimentos Críticos do Mês 1

Para os 4 pacotes de compra de partida da obra, os Centros de Custo obrigatórios a constar nas RCs e nos PCs são:

| Pacote / RC | Insumo / Serviço Contratado | Centro de Custo (CC) | Conta Contábil | Orçado Custo Direto |
| :---: | :--- | :---: | :---: | :---: |
| **RC-001/2026** | Aço CA-50 Fundações (Sapatas e Baldrames) | `CC-208` e `CC-210` | 4.1.2.01.08 / 10 | R$ 15.635,66 |
| **RC-002/2026** | Concreto Usinado fck 30 MPa e Lastro | `CC-202`, `CC-203` e `CC-206` | 4.1.2.01.02 / 03 / 06 | R$ 20.252,08 |
| **RC-003/2026** | Compensado 17mm e Fôrmas de Madeira | `CC-204` e `CC-207` | 4.1.2.01.04 / 07 | R$ 20.286,07 |
| **RC-004/2026** | Containers Habitáveis NR-18 (6 Meses) | `CC-103` | 4.1.1.01.03 | R$ 38.299,98 |

---
*Plano auditado e vinculado à Linha de Base SINAPI SP 07/2026.*