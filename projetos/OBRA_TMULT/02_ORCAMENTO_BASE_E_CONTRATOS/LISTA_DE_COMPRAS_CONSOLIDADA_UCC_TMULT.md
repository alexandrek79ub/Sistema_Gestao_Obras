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
| **Alvenaria/Vedação**| Bloco Concreto Inteiro B144 (14x19x39cm)| **13.790** | `blocos inteiros` | Vedação (13.370 un) + Platibanda (420 un) |
| **Alvenaria/Vedação**| Meio Bloco Concreto B142 (14x19x19cm) | **534** | `meios blocos` | Amarração de cantos e vãos sem quebra de blocos |
| **Alvenaria/Vedação**| Bloco Canaleta Concreto C144 (14x19x39cm)| **296** | `blocos canaleta` | Vergas e contravergas de portas e janelas |
| **Alvenaria/Vedação**| Graute Fino Industrializado p/ Canaletas | **75** | `sacos 25kg` | Preenchimento estrutural de canaletas (1,49 m³) |
| **Alvenaria/Vedação**| Barra de Aço CA-50 Ø8,0mm p/ Vergas | **20** | `barras 12m` | Armadura longitudinal de vergas/contravergas (93,2 kg) |
| **Alvenaria/Vedação**| Tela Metálica Galvanizada 15x50cm | **353** | `telas de amarração`| Amarração pilar-alvenaria a cada 2 fiadas |
| **Alvenaria/Vedação**| Pinos de Aço c/ Arruela p/ Finca-Pinos | **8** | `caixas 100un` | Fixação das telas de amarração nos pilares (742 un) |
| **Alvenaria/Vedação**| Cimento Portland CP II-E-32 (Assentamento) | **116** | `sacos 50kg` | Argamassa de assentamento traço 1:2:8 |
| **Alvenaria/Vedação**| Cal Hidratada CH-I (Assentamento) | **101** | `sacos 20kg` | Argamassa de assentamento traço 1:2:8 |
| **Alvenaria/Vedação**| Areia Média Lavada (Assentamento) | **24,5** | `m³` | Areia para argamassa de assentamento |
| **Alvenaria/Vedação**| Encunhamento Flexível no Topo | **385** | `m lineares` | Fechamento elástico topo alvenaria sob vigas |
| **Alvenaria/Vedação**| Bloco Concreto 9x19x39cm (Muretas) | **594** | `blocos 9x19x39cm` | Muretas escalonadas de apoio de terças no entreforro |
| **Alvenaria/Vedação**| Contrapiso de Regularização e=3cm | **386,82** | `m²` | 11,6 m³ de argamassa sobre laje térrea |
| **Pisos/Acabamentos**| Porcelanato Retificado 60x60cm | **282** | `caixas` | Área útil com 10% perda (406,08 m²) |
| **Pisos/Acabamentos**| Argamassa Colante AC-III (Porcelanato) | **194** | `sacos 20kg` | Dupla colagem 10 kg/m² |
| **Pisos/Acabamentos**| Rejunte Flexível Porcelanato Junta 2mm | **20** | `sacos 5kg` | Rejuntamento de porcelanato retificado |
| **Pisos/Acabamentos**| Clips Niveladores Plásticos 60x60cm | **41** | `sacos 100un` | Assentamento e nivelamento de porcelanato (4.100 un) |
| **Pisos/Acabamentos**| Cunhas Niveladoras Reutilizáveis | **13** | `sacos 100un` | Giro de 30% da frente de trabalho (1.300 un) |
| **Pisos/Acabamentos**| Revestimento Cerâmico WCs 45x45 Eliane | **65** | `caixas` | Paredes sanitários/copa h=1,80m (92,6 m²) |
| **Pisos/Acabamentos**| Argamassa Colante AC-II (Parede) | **23** | `sacos 20kg` | Assentamento cerâmico de parede |
| **Pisos/Acabamentos**| Rejunte Cerâmico Antimofo Junta 3mm | **6** | `sacos 5kg` | Rejuntamento de paredes molhadas |
| **Pisos/Acabamentos**| Espaçadores / Cruzetas Plásticas 2/3mm | **28** | `sacos 100un` | Juntas de assentamento cerâmico e pisos |
| **Pisos/Acabamentos**| Rodapé de Porcelanato h=10cm | **422,62** | `m` | Rodapé com 10% de perda |
| **Pisos/Acabamentos**| Lona Plástica Preta Proteção de Piso | **4** | `bobinas 100m²` | Proteção de pisos acabados contra danos |
| **Pintura** | Tinta Acrílica Premium (Latas 18L) | **38** | `latas 18L` | Paredes/tetos (36) + Platibanda impermeável (2) |
| **Pintura** | Selador Acrílico Base Água (Latas 18L)| **13** | `latas 18L` | Preparação e selagem de reboco novo (223 L) |
| **Pintura** | Lixa Grossa p/ Reboco (Grão 80/100) | **112** | `folhas` | Desbaste de reboco paulista |
| **Pintura** | Lixa Fina p/ Massa/Gesso (Grão 150/220)| **262** | `folhas` | Acabamento fino pré-pintura |
| **Pintura** | Fita Crepe Proteção 24mm x 50m | **13** | `rolos 50m` | Isolamento de rodapés, caixilhos e vidros |
| **Esquadrias** | Portas P1 a P5 Madeira/Alumínio | **24** | `conjuntos` | Conjuntos executivos de portas completas |
| **Esquadrias** | Dobradiças 3 ½" x 3" em Aço Inox | **82** | `dobradiças inox`| 3 un por folha de abrir (26 folhas) |
| **Esquadrias** | Fechaduras Completas (Cil/Gorge/Tranq)| **24** | `conjuntos` | Máquina, cilindro, maçaneta e roseta |
| **Esquadrias** | Batedores de Porta de Piso Inox | **26** | `unidades` | Batedor com amortecedor emborrachado |
| **Esquadrias** | Espuma de Poliuretano Expansiva 750ml | **11** | `tubos 750ml` | Fixação e calafetação de marcos/batentes |
| **Esquadrias** | Parafusos e Buchas Nylon S8 Batente | **3** | `caixas 100un` | Fixação mecânica de batentes (202 un) |
| **Esquadrias** | Pregos sem Cabeça 12x12 p/ Alizares | **5** | `pacotes 100un`| Fixação de guarnições e alizares (504 un) |
| **Esquadrias** | Cola Branca PVA Madeira D3 (500g) | **4** | `frascos 500g` | Colagem de esquadrias e alizares |
| **Esquadrias** | Janelas J1 a J4 Alumínio e Vidro | **18** | `conjuntos` | Janelas completas de correr e basculantes |
| **Esquadrias** | Selante PU 40 Neutro Caixilhos (310ml)| **14** | `tubos 310ml` | Vedação perimétrica externa de caixilhos |
| **Impermeabilização**| Membrana Polimérica Flexível WCs/Copa | **19** | `caixas 18kg` | 3 demãos cruzadas em áreas molhadas (92,62 m²) |
| **Impermeabilização**| Tela de Poliéster / Véu de Reforço | **2** | `rolos 50m²` | Estruturação de cantos vivos, meias-canas e ralos |
| **Impermeabilização**| Manta Asfáltica Poliéster 4mm Calhas | **8** | `rolos 10m²` | Impermeabilização de calhas pluviais (71,3 m²) |
| **Impermeabilização**| Primer Asfáltico Base Solvente Calhas | **2** | `baldes 18L` | Imprimação para manta asfáltica (36 L) |
| **Impermeabilização**| Gás GLP P-13 p/ Maçarico de Manta | **2** | `botijões P-13` | Aplicação a fogo da manta asfáltica |
| **Cobertura/Metálica**| Telha Termoacústica Sandwich EPS 30mm | **70** | `telhas 6m` | Telha trapezoidal inclinação 15° (419,42 m²) |
| **Cobertura/Metálica**| Parafuso Auto-brocante 12x1" c/ EPDM | **19** | `caixas 100un` | Fixação de telhas nas terças (1.802 un) |
| **Cobertura/Metálica**| Parafuso Costura 10x3/4" c/ EPDM | **4** | `caixas 100un` | Travamento longitudinal de emendas de telhas (383 un) |
| **Cobertura/Metálica**| Fita Vedação Butílica 15mm (rolos 10m) | **13** | `rolos 10m` | Estanqueidade de emendas de telhas e calhas |
| **Cobertura/Metálica**| Terça Metálica Perfil U 100x40x2,25mm | **28** | `barras 6m` | Estrutura metálica de apoio (573,3 kg) |
| **Cobertura/Metálica**| Chumbadores Parabolts CBA 3/8" x 3" | **63** | `unidades` | Ancoragem mecânica das terças nas muretas |
| **Cobertura/Metálica**| Calha Galvanizada nº 24 Dev 80cm | **19** | `peças 3m` | Captação pluvial com abas (54,6 m) |
| **Cobertura/Metálica**| Rebites de Repuxo Alumínio 4,0x10mm | **5** | `centos (500un)`| Fixação de emendas de calhas e rufos |
| **Cobertura/Metálica**| Selante PU 40 p/ Calhas e Rufos | **6** | `tubos 310ml` | Calafetação e estanqueidade de calhas |
| **Cobertura/Metálica**| Rufo/Pingadeira Galvanizada Dev 40cm | **29** | `peças 3m` | Topo de platibanda (86,1 m) |
| **Cobertura/Metálica**| Ralo Hemisférico Abacaxi Inox Ø150mm | **8** | `unidades` | Bocais de descida pluvial de calhas |
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
