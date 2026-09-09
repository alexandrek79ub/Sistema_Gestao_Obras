# 🛒 Lista Consolidada de Pedido de Compras (UCC) com Miudezas & Consumíveis de Canteiro

**Empreendimento:** TMULT - Terminal Multiuso (Porto do Açu)  
**Edificação:** Edifício Administrativo (368,40 m²)  
**Objetivo:** Suprimentos / Emissão de Pedidos de Compra sem Omissão de Consumíveis  
**Data da Emissão:** 08/09/2026  
**Ref. Normativa:** `SKILL_QUANTIFICACAO_PEDIDO_DE_COMPRA.md` e TCPO / SINAPI  

---

## 📌 1. Por que esta Lista Inclui as "Miudezas"?

Um dos maiores gargalos de canteiro é a paralisação por **falta de insumos consumíveis de montagem** (pregos, arames, desmoldantes, adesivo PVC, abraçadeiras, parafusos, buchas, discos de corte, fita isolante).

Esta lista foi gerada derivando deterministicamente os insumos principais da estrutura, alvenaria, cobertura e instalações com os **coeficientes de consumo TCPO/SINAPI**, garantindo a emissão de Pedidos de Compra 100% realistas para o setor de Suprimentos.

---

## 📋 2. Tabela Mestre de Solicitação de Compras (Insumos + Consumíveis)

| Categoria | Descrição do Insumo / Miudeza | Qtd Comercial UCC | Unidade UCC | Aplicação / Observação Técnica |
| :--- | :--- | :---: | :---: | :--- |
| **Estrutura/Fôrmas** | Chapa Compensado Resinado 17mm | **552** | `chapas` | Infraestrutura (129) + Supraestrutura (423) |
| **Estrutura/Fôrmas** | Prego c/ Cabeça 17x27mm (Fôrmas) | **120** | `kg (6 caixas)` | Consumo 0,20 kg/m² de fôrma (597 m² fôrmas) |
| **Estrutura/Fôrmas** | Prego c/ Cabeça 18x30mm (Gravatas) | **80** | `kg (4 caixas)` | Travamento de pilares e vigas |
| **Estrutura/Fôrmas** | Desmoldante Biodegradável Fôrmas | **90** | `L (5 galões 18L)` | Consumo 0,15 L/m² de fôrma |
| **Estrutura/Fôrmas** | Tábua 3ª 2,5x30cm (Varas 3m) | **120** | `varas` | Gravatas, sarrafos e alinhamento de fôrmas |
| **Aço/Armadura** | Aço CA-50 (10/12,5/16mm) | **988** | `barras 12m` | Infraestrutura (302 bar) + Supra (686 bar) |
| **Aço/Armadura** | Aço CA-60 (5/6,3mm Estribos) | **1282** | `barras 12m` | Infraestrutura (373 bar) + Supra (909 bar) |
| **Aço/Armadura** | Arame Recozido BWG 18 | **215** | `kg (rolos 1kg)` | Consumo 1,5% do peso de aço (14.856 kg) |
| **Aço/Armadura** | Espaçador/Pastilha Cobrimento 40mm | **1.313** | `unidades` | Fundações e baldrames |
| **Aço/Armadura** | Espaçador Plástico Cobrimento 25/30mm | **2.993** | `unidades` | Pilares, vigas e lajes |
| **Concreto/Solo** | Concreto Usinado fck 30 MPa | **124** | `m³ (16 betoneiras)` | Infraestrutura (45m³) + Supra (79m³) |
| **Concreto/Solo** | Concreto Magro fck 15 MPa (Lastro) | **10** | `m³ (2 betoneiras)` | Lastro das cavas de fundação |
| **Concreto/Solo** | Argamassa Pronta Emboço (sacos 20kg) | **462** | `sacos` | Paredes internas e platibanda |
| **Concreto/Solo** | Cimento CP II-Z-32 (sacos 50kg) | **75** | `sacos` | Chapisco e regularização |
| **Alvenaria/Cobert**| Bloco Concreto 14x19x39cm | **14.351** | `unidades` | Paredes (13.931) + Platibanda (420) |
| **Alvenaria/Cobert**| Bloco Concreto 9x19x39cm | **594** | `unidades` | Muretas escalonadas entreforro |
| **Alvenaria/Cobert**| Telha Termoacústica Sandwich 30mm | **70** | `telhas 6m` | Cobertura 419,4 m² |
| **Alvenaria/Cobert**| Terça Metálica U 100x40x2,25mm | **28** | `barras 6m` | Estrutura metálica de apoio (573 kg) |
| **Alvenaria/Cobert**| Calha Galvanizada dev 80cm | **19** | `peças 3m` | Captação pluvial com abas |
| **Alvenaria/Cobert**| Rufo/Pingadeira Galvanizada dev 40cm | **29** | `peças 3m` | Topo de platibanda |
| **Alvenaria/Cobert**| Impermeabilização Manta Asfáltica 4mm | **8** | `rolos 10m²` | Calhas e calhetões |
| **Alvenaria/Cobert**| Parafuso Auto-brocante 5.5 x 75mm | **850** | `unid (9 caixas)` | Fixação das telhas termoacústicas nas terças |
| **Acabamento/Piso** | Porcelanato Retificado 60x60cm | **281** | `caixas (405,2 m²)` | Área útil com 10% perda |
| **Acabamento/Piso** | Argamassa Colante AC-II (sacos 20kg) | **105** | `sacos` | Assentamento de porcelanato (5kg/m²) |
| **Acabamento/Piso** | Rejunte Flexível Porcelanato | **21** | `sacos 5kg` | Junta de 2mm |
| **Acabamento/Piso** | Espaçador/Nivelador 2mm c/ Cunhas | **2.500** | `unid (25 pacotes)` | Assentamento de porcelanato |
| **Acabamento/Piso** | Tinta Acrílica Premium (Latas 18L) | **38** | `latas 18L` | Paredes/tetos (36) + Platibanda (2) |
| **Acabamento/Piso** | Selador Acrílico (Latas 18L) | **14** | `latas 18L` | Preparação de pintura |
| **Acabamento/Piso** | Lixa para Massa Grão 150/220 | **250** | `folhas` | Lixamento de paredes e tetos |
| **Acabamento/Piso** | Fita Crepe Proteção 48mm x 50m | **40** | `rolos` | Proteção de esquadrias e rodapés |
| **Elétrica/Telecom**| Cabos Cobre Flex (2.5/4.0/6.0mm²) | **34** | `rolos 100m` | 21 flex 2,5 + 8 flex 4,0 + 5 flex 6,0 |
| **Elétrica/Telecom**| Eletroduto Rígido PVC Ø3/4" (3m) | **176** | `varas 3m` | Infraestrutura teto/parede |
| **Elétrica/Telecom**| Caixas Embutir PVC (4x2, 4x4, Octogonal)| **292** | `unidades` | 194 caixas 4x2 + 26 caixas 4x4 + 72 octogonais |
| **Elétrica/Telecom**| Módulos Tomada/Interruptor/Placas | **369** | `peças` | 142 tomadas + 33 interruptores + 194 placas |
| **Elétrica/Telecom**| Cabo UTP Cat6 LSZH Dados/Voz | **16** | `rolos 100m` | Cabeamento de rede estruturada |
| **Elétrica/Telecom**| Kit Telecom (Rack 12U + Patch + Switch)| **1** | `kit completo` | Infraestrutura de TI |
| **Elétrica/Telecom**| Disjuntores DIN + DRs + DPSs | **61** | `dispositivos` | 30 monopolares + 19 bipolares + 4 DRs + 8 DPS |
| **Elétrica/Telecom**| Fita Isolante 3M 20m | **30** | `rolos` | Isolamento elétrico de caixas |
| **Elétrica/Telecom**| Abraçadeira Enforca-Gato 200x4,8mm | **20** | `pcts (2.000un)` | Organização de cabos no rack |
| **Elétrica/Telecom**| Abraçadeira Tipo D 3/4" Galvanizada | **150** | `unidades` | Fixação de eletrodutos |
| **Elétrica/Telecom**| Parafuso c/ Bucha Nylon S8 | **10** | `cx 100un (1.000un)`| Fixação de quadros, luminárias e calhas |
| **Hidráulica/Esgoto**| Tubos PVC Soldável/Esgoto/Pluvial | **118** | `varas 6m` | 51 varas água fria + 67 varas esgoto/pluvial |
| **Hidráulica/Esgoto**| Conexões PVC Soldável (Joelhos, Tês) | **217** | `unidades` | Peça a peça (91 joelhos 90° Ø25 + 34 c/ latão...) |
| **Hidráulica/Esgoto**| Conexões PVC Esgoto (Joelhos, Junções)| **94** | `unidades` | Peça a peça (38 joelhos 90° Ø100 + 24 45°...) |
| **Hidráulica/Esgoto**| Registros c/ Canopla Cromada | **22** | `registros` | 12 gaveta 3/4" + 4 gaveta 1.1/2" + 6 pressão |
| **Hidráulica/Esgoto**| Reservatórios Polietileno 5.000L | **2** | `unidades` | Caixa d'água c/ tampa roscada |
| **Hidráulica/Esgoto**| Kits Louças + Metais + Sifões | **73** | `itens` | 10 bacias + 12 lavatórios + 51 sifões/engates |
| **Hidráulica/Esgoto**| Fita Veda-Rosca PTFE 18mmx50m | **12** | `rolos` | Vedação de conexões roscadas |
| **Hidráulica/Esgoto**| Adesivo Plástico p/ PVC (Frascos 850g)| **8** | `frascos 850g` | Colagem de tubos e conexões de água/esgoto |
| **Hidráulica/Esgoto**| Solução Preparadora PVC (850ml) | **6** | `frascos 850ml` | Limpeza e preparação de tubos |
| **Consumíveis** | Disco Corte Diamantado 110mm | **15** | `unidades` | Corte de blocos, azulejo e porcelanato |
| **Consumíveis** | Disco Corte Aço 7" Esmerilhadeira | **25** | `unidades` | Corte de vergalhões e terças metálicas |
| **Consumíveis** | Lona Preta Proteção 4x50m | **2** | `rolos` | Proteção de canteiro e cura de concreto |

---

*Lista gerada e homologada pelo PMO Virtual & Suprimentos A11 em:* 08/09/2026
