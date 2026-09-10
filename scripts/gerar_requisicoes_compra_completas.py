#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador dos Dossiês Formais de Requisições de Compra (Meses 2 a 6)
Completa 100% das 24 RCs da OBRA_TMULT com especificações técnicas, UCC, Centros de Custo e POP 06
"""

import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "projetos", "OBRA_TMULT", "05_SUPRIMENTOS_E_FINANCEIRO")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# MÊS 2: RC-005 a RC-008 (Superestrutura e Laje)
# -------------------------------------------------------------------------
MES2_CONTENT = """# 📋 REQUISIÇÕES DE COMPRA FORMAIS — MÊS 2 (SUPERESTRUTURA E LAJE)

**Empreendimento:** Edifício Administrativo TMULT — Terminal Multiuso (Porto do Açu - SJB/RJ)  
**Gestor do Contrato / Solicitante:** Eng. Alexandre (Engenheiro Residente & PMO Virtual)  
**Data de Emissão:** 05/10/2026 | **Linha de Base:** Baseline 01 (Semanas S05 a S08)  
**Ref. Normativa do Ecossistema:** `POP_05_SOLICITACAO_COMPRAS.md`, `POP_06_RECEBIMENTO.md`, `POP_19_FORMAS_E_CIMBRAMENTO.md`

---

## 🧭 1. Diretrizes Normativas de Emissão e Recebimento
1. **Lead Times Antecipados:** Disparos entre 05/10 e 15/10 para atendimento às concretagens de pilares e laje (S06 a S08);
2. **Conversão em UCC:** Escoramento em m²·m/dia, vigotas treliçadas em m² de laje montada, aço cortado/dobrado por elemento estrutural e concreto usinado com entrega programada minuto a minuto;
3. **Portões de Qualidade (NBR 6118 / NBR 14931):** Conferência de flechas, contra-flecha L/300 e slump test a cada caminhão betoneira.

---

## 📦 RC-005/2026 — Cimbramento e Escoramento Metálico Ajustável

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-005/2026` |
| **Disciplina** | Estruturas de Concreto Armado (Superestrutura) |
| **EAP Vinculada** | `1.2.4, 1.2.6` |
| **Centro de Custo (CC)** | **`CC-302`** |
| **Disparo da RC** | 05/10/2026 |
| **Data Necessária no Canteiro** | **25/10/2026** (Lead: 20d) |
| **Custo Direto Base** | **R$ 14.850,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 5.1 | Escoras metálicas telescópicas reguláveis (2,00m a 3,60m) com pino de segurança | 320,00 | un | **320,00** | `un (locação 45 dias)` | EGS-053/054 |
| 5.2 | Vigas primárias e secundárias metálicas tipo Aluma/Perfil C para vigas V101-V115 | 420,00 | m | **420,00** | `m (locação 45 dias)` | EGS-053/054 |
| 5.3 | Cruzetas, forcados duplos reguláveis e sapatas articuladas de nivelamento | 180,00 | un | **180,00** | `un (locação 45 dias)` | POP 19 |

#### Critério de Recebimento (POP 06):
- Certificado de ensaio de carga e ART do fabricante (Mills/Rohr/SH);
- Verificação de ausência de amassamentos, empenamentos ou roscas espanadas;
- Conferência da altura útil compatível com o pé-direito livre de 3,20m.

---

## 📦 RC-006/2026 — Vigotas Treliçadas Pré-Moldadas TR 16745 e Lajotas de EPS H12

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-006/2026` |
| **Disciplina** | Estruturas / Laje de Cobertura |
| **EAP Vinculada** | `1.2.5` |
| **Centro de Custo (CC)** | **`CC-303`** |
| **Disparo da RC** | 08/10/2026 |
| **Data Necessária no Canteiro** | **28/10/2026** (Lead: 20d) |
| **Custo Direto Base** | **R$ 23.450,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 6.1 | Vigotas de concreto protendido/armado c/ treliça TR 16745 nos vãos de 3,50m a 5,20m | 680,00 | m | **680,00** | `m` | EGS-055 (Planta Laje) |
| 6.2 | Blocos de EPS (Isopor) moldado H12 padrão laje unidirecional (ignífugo autoextinguível) | 1.150,00 | un | **1.180,00** | `un` | NBR 14859 |
| 6.3 | Tela soldada nervurada Q-138 (Ø4,2mm malha 10x10cm) para armadura de distribuição | 368,40 | m² | **400,00** | `m² (painéis)` | NBR 7481 |

#### Critério de Recebimento (POP 06):
- Vigotas com carimbo de fabricação e cura mínima de 14 dias;
- EPS 100% classe F (antichama) com laudo de ensaio IPT;
- Descarregamento manual paletizado para evitar quebras dos cantos do EPS.

---

## 📦 RC-007/2026 — Aço CA-50/60 Cortado e Dobrado (Pilares P1-P24 e Vigas V101-V115)

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-007/2026` |
| **Disciplina** | Estruturas de Concreto Armado |
| **EAP Vinculada** | `1.2.7, 1.2.8` |
| **Centro de Custo (CC)** | **`CC-304`** |
| **Disparo da RC** | 10/10/2026 |
| **Data Necessária no Canteiro** | **30/10/2026** (Lead: 20d) |
| **Custo Direto Base** | **R$ 29.850,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 7.1 | Aço CA-50 Ø12,5mm e Ø16,0mm cortado/dobrado para armadura longitudinal de pilares | 1.420,00 | kg | **1.491,00** | `kg` | EGS-053 (Pilares) |
| 7.2 | Aço CA-50 Ø10,0mm e Ø12,5mm cortado/dobrado para armadura positiva/negativa de vigas | 1.340,00 | kg | **1.407,00** | `kg` | EGS-054 (Vigas) |
| 7.3 | Estribos fechados CA-60 Ø5,0mm e Ø6,3mm com gancho sísmico 135º | 420,00 | kg | **441,00** | `kg` | EGS-053/054 |
| 7.4 | Espaçadores plásticos circulares tipo roseta para pilares (cobrimento c=30mm) | 1.800,00 | un | **1.900,00** | `un` | NBR 6118 |

#### Critério de Recebimento (POP 06):
- Certificado de conformidade Gerdau/Arcelor com identificação de lote e corrida;
- Feixes etiquetados individualmente com tag de código do pilar/viga;
- Armazenamento em cavaletes cobertos a 20cm do solo no canteiro.

---

## 📦 RC-008/2026 — Concreto Usinado fck 30 MPa Bombeável (Superestrutura e Capa de Laje)

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-008/2026` |
| **Disciplina** | Concreto Estrutural |
| **EAP Vinculada** | `1.2.1, 1.2.3, 1.2.5` |
| **Centro de Custo (CC)** | **`CC-305`** |
| **Disparo da RC** | 15/10/2026 |
| **Data Necessária no Canteiro** | **05/11/2026** (Lead: 21d) |
| **Custo Direto Base** | **R$ 32.650,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 8.1 | Concreto usinado fck 30 MPa brita 1 slump 12±2cm (Pilares P1 a P24) | 6,44 | m³ | **7,00** | `m³` | EGS-053 |
| 8.2 | Concreto usinado fck 30 MPa brita 1 slump 14±2cm bombeável (Vigas e Capa de Laje) | 30,55 | m³ | **32,50** | `m³` | EGS-054/055 |
| 8.3 | Serviço de auto-bomba lança 32 metros com operador para concretagem contínua | 1,00 | vb | **1,00** | `vb` | Logística Canteiro |

#### Critério de Recebimento (POP 06 / POP 22):
- Slump test obrigatório no primeiro e no meio de cada caminhão betoneira;
- Moldagem de 6 CPs por caminhão (ensaios aos 7, 14 e 28 dias);
- Tempo de transporte usina-canteiro inferior a 45 minutos (Polimix Porto do Açu).
"""

# -------------------------------------------------------------------------
# MÊS 3: RC-009 a RC-012 (Alvenaria, Fachada e Cobertura)
# -------------------------------------------------------------------------
MES3_CONTENT = """# 📋 REQUISIÇÕES DE COMPRA FORMAIS — MÊS 3 (ALVENARIA E COBERTURA)

**Empreendimento:** Edifício Administrativo TMULT — Terminal Multiuso (Porto do Açu - SJB/RJ)  
**Gestor do Contrato / Solicitante:** Eng. Alexandre (Engenheiro Residente & PMO Virtual)  
**Data de Emissão:** 20/10/2026 | **Linha de Base:** Baseline 01 (Semanas S09 a S12)  
**Ref. Normativa do Ecossistema:** `POP_05_SOLICITACAO_COMPRAS.md`, `POP_06_RECEBIMENTO.md`, `POP_12_ALVENARIA.md`, `POP_24_COBERTURA.md`

---

## 🧭 1. Diretrizes Normativas de Emissão e Recebimento
1. **Prazos Críticos de Cobertura:** Telhas termoacústicas possuem lead time de fabricação de 44 dias (disparo antecipado em 15/10 para entrega em 28/11);
2. **Homologação Portuária:** Telhas com dupla face aluzinc AZ-150 e pintura epóxi anti-corrosão marítima C5-M;
3. **Controle de Alvenaria:** Blocos de concreto com resistência à compressão fbk >= 4,0 MPa e modulação a laser.

---

## 📦 RC-009/2026 — Blocos de Concreto de Vedação B144 (14x19x39cm)

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-009/2026` |
| **Disciplina** | Alvenaria e Fechamentos |
| **EAP Vinculada** | `1.3.1, 1.3.2` |
| **Centro de Custo (CC)** | **`CC-401`** |
| **Disparo da RC** | 20/10/2026 |
| **Data Necessária no Canteiro** | **15/11/2026** (Lead: 26d) |
| **Custo Direto Base** | **R$ 21.400,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 9.1 | Bloco de concreto estrutural/vedação 14x19x39cm vazado classe B (fbk >= 4,0 MPa) | 12.800,00 | un | **13.440,00** | `un (paletes 105 un)` | ARQ-001 a 004 |
| 9.2 | Meio-bloco de concreto 14x19x19cm para amarração de cantos sem quebra | 850,00 | un | **900,00** | `un` | Modulação EAP |
| 9.3 | Bloco canaleta tipo J e U 14x19x39cm para cintas de amarração, vergas e contravergas | 340,00 | un | **360,00** | `un` | Detalhes Janelas |
| 9.4 | Tela galvanizada eletrosoldada 10x10cm (rolo 50m) para amarração bloco-pilar | 140,00 | m | **150,00** | `m (3 rolos)` | NBR 8545 |

#### Critério de Recebimento (POP 06 / POP 12):
- Blocos paletizados com filme stretch; no máximo 1,5% de blocos fissurados por carga;
- Laudo laboratorial do lote comprovando fbk >= 4,0 MPa e absorção de água < 10%.

---

## 📦 RC-010/2026 — Cimento Portland CP II-E-32, Areia Média e Aditivo Plastificante

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-010/2026` |
| **Disciplina** | Argamassas de Obra |
| **EAP Vinculada** | `1.3.3` |
| **Centro de Custo (CC)** | **`CC-402`** |
| **Disparo da RC** | 02/11/2026 |
| **Data Necessária no Canteiro** | **18/11/2026** (Lead: 16d) |
| **Custo Direto Base** | **R$ 11.250,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 10.1 | Cimento Portland com Escória CP II-E-32 (sacos de 50 kg) | 300,00 | sc | **320,00** | `sc 50kg (paletes)` | NBR 16697 |
| 10.2 | Areia média lavada de rio isenta de cloretos e matéria orgânica | 26,00 | m³ | **28,00** | `m³ (caminhão basc.)` | NBR 7211 |
| 10.3 | Aditivo plastificante e incorporador de ar Vedacit/Sika para argamassa de assentamento | 8,00 | gl | **8,00** | `gl 18L` | NBR 13281 |
| 10.4 | Cal hidratada CH-I para argamassa mista de assentamento | 120,00 | sc | **130,00** | `sc 20kg` | NBR 7175 |

#### Critério de Recebimento (POP 06):
- Sacos de cimento sem empedramento, estocados sobre estrados de madeira a 15cm do piso;
- Areia com certificado de procedência de jazida licenciada pelo INEA/RJ.

---

## 📦 RC-011/2026 — Locação de Andaimes Tubulares Fachadeiros com Linha de Vida (NR-18)

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-011/2026` |
| **Disciplina** | Instalações Provisórias e Segurança em Altura |
| **EAP Vinculada** | `1.3.4` |
| **Centro de Custo (CC)** | **`CC-403`** |
| **Disparo da RC** | 08/11/2026 |
| **Data Necessária no Canteiro** | **25/11/2026** (Lead: 17d) |
| **Custo Direto Base** | **R$ 7.400,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 11.1 | Painéis de andaime fachadeiro tubular com escadas marinheiro e guarda-corpo duplo | 200,00 | m² | **200,00** | `m² (locação 60 dias)` | NR-18 / NR-35 |
| 11.2 | Piso metálico galvanizado antiderrapante com trava de segurança | 120,00 | m | **120,00** | `m` | POP 20 |
| 11.3 | Sapatas reguláveis com placa de base e rodapés metálicos h=20cm | 48,00 | un | **48,00** | `un` | NR-18 |

#### Critério de Recebimento (POP 06 / POP 20):
- Verificação do registro do fabricante no CREA e ART de fabricação;
- Inspeção 100% de travas, soldas e ausência de corrosão acentuada.

---

## 📦 RC-012/2026 — Telhas Termoacústicas Sandwich PIR e Calhas Metálicas Galvanizadas

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-012/2026` |
| **Disciplina** | Cobertura Industrial |
| **EAP Vinculada** | `1.4.1, 1.4.2, 1.4.3` |
| **Centro de Custo (CC)** | **`CC-501`** |
| **Disparo da RC** | 15/10/2026 |
| **Data Necessária no Canteiro** | **28/11/2026** (Lead: 44d) |
| **Custo Direto Base** | **R$ 48.900,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 12.1 | Telha trapezoidal termoacústica sandwich PIR e=30mm chapa aluzinc 0,50mm branca | 381,29 | m² | **395,00** | `m² (peças sob medida)` | COB-001 (Cobertura) |
| 12.2 | Calha metálica corte 50 chapa galvanizada nº 24 dobrada com declividade 1% | 64,00 | m | **68,00** | `m (barras 3m)` | Detalhe Calhas |
| 12.3 | Rufos de platibanda corte 33, cumeeiras articuladas e arremates estanques | 82,00 | m | **86,00** | `m` | Arremates |
| 12.4 | Parafusos autobrocantes com arruela de vedação EPDM de neoprene vulcanizado | 1.850,00 | un | **2.000,00** | `un (cento)` | Fixação Telhas |
| 12.5 | Selante de poliuretano PU-40 para vedação de sobreposições e emendas | 24,00 | un | **24,00** | `tubos 400g` | Estanqueidade |

#### Critério de Recebimento (POP 06 / POP 24):
- Medição das peças na trena garantindo montagem sem emendas transversais;
- Teste de queima rápida do núcleo provando classe PIR autoextinguível (não PUR);
- Película plástica de proteção intacta na face superior para evitar riscos.
"""

# -------------------------------------------------------------------------
# MÊS 4: RC-013 a RC-016 (Instalações, Reboco e Esquadrias)
# -------------------------------------------------------------------------
MES4_CONTENT = """# 📋 REQUISIÇÕES DE COMPRA FORMAIS — MÊS 4 (INSTALAÇÕES E ESQUADRIAS)

**Empreendimento:** Edifício Administrativo TMULT — Terminal Multiuso (Porto do Açu - SJB/RJ)  
**Gestor do Contrato / Solicitante:** Eng. Alexandre (Engenheiro Residente & PMO Virtual)  
**Data de Emissão:** 20/11/2026 | **Linha de Base:** Baseline 01 (Semanas S13 a S16)  
**Ref. Normativa do Ecossistema:** `POP_05_SOLICITACAO_COMPRAS.md`, `POP_06_RECEBIMENTO.md`, `POP_15_HIDRAULICA.md`, `POP_16_ELETRICA.md`, `POP_25_ESQUADRIAS.md`

---

## 🧭 1. Diretrizes Normativas de Emissão e Recebimento
1. **Portão de Ouro da Hidráulica (Portão 3 do Índice Mestre):** Tubulações devem ser testadas a 10 bar por 72h antes do fechamento do reboco;
2. **Esquadrias de Longo Lead Time:** Janelas encomendadas em 01/11 com entrega programada em 10/01 para fechamento estanque do prédio;
3. **Argamassa de Projeção Mecânica:** Fornecimento paletizado ensacado para uso imediato nas máquinas de projeção contínua.

---

## 📦 RC-013/2026 — Tubulações e Conexões PVC de Água Fria e Esgoto Predial

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-013/2026` |
| **Disciplina** | Instalações Hidrossanitárias |
| **EAP Vinculada** | `2.1.1, 2.1.2, 2.1.3` |
| **Centro de Custo (CC)** | **`CC-601`** |
| **Disparo da RC** | 20/11/2026 |
| **Data Necessária no Canteiro** | **15/12/2026** (Lead: 25d) |
| **Custo Direto Base** | **R$ 16.800,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 13.1 | Tubo PVC soldável marrom água fria Ø25mm, Ø32mm e Ø50mm (barras 6m) | 240,00 | m | **252,00** | `m (42 barras)` | HID-001 a 003 |
| 13.2 | Tubo PVC esgoto série normal e reforçada Ø50mm, Ø75mm e Ø100mm | 180,00 | m | **192,00** | `m (32 barras)` | SAN-001 a 003 |
| 13.3 | Conexões variadas PVC (joelhos, tês, luvas, buchas de redução, adaptadores) | 180,00 | un | **195,00** | `un` | Isométricos Hidr. |
| 13.4 | Caixas sifonadas 150x150x50mm c/ grelha inox e caixas de gordura/inspeção | 16,00 | un | **16,00** | `un` | Detalhes Sanitários |
| 13.5 | Adesivo plástico para PVC, solução limpadora e pasta lubrificante para anéis | 12,00 | un | **12,00** | `kits montagem` | Consumível Tigre |

#### Critério de Recebimento (POP 06 / POP 15):
- Marcas homologadas: Tigre ou Amanco; selo PBQP-H gravado a laser no tubo;
- Espessura de parede e diâmetros conformes com a NBR 5648 e NBR 5688.

---

## 📦 RC-014/2026 — Eletrodutos Rígidos Roscáveis, Caixas 4x2 e Caixas de Passagem

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-014/2026` |
| **Disciplina** | Infraestrutura Elétrica e Cabeamento |
| **EAP Vinculada** | `2.2.1, 2.2.2` |
| **Centro de Custo (CC)** | **`CC-604`** |
| **Disparo da RC** | 25/11/2026 |
| **Data Necessária no Canteiro** | **18/12/2026** (Lead: 23d) |
| **Custo Direto Base** | **R$ 9.750,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 14.1 | Eletroduto PVC rígido roscável antichama Ø3/4", Ø1" e Ø1.1/2" (barras 3m) | 650,00 | m | **675,00** | `m (225 barras)` | ELE-001 a 004 |
| 14.2 | Caixas de embutir 4x2" em PVC antichama amarela com orelha reforçada | 85,00 | un | **90,00** | `un` | Pontos Tomadas |
| 14.3 | Caixas de passagem octogonais 4x4" para teto e caixas de derivação metálicas | 48,00 | un | **52,00** | `un` | Pontos Iluminação |
| 14.4 | Luvas de emenda roscáveis, curvas 90º longas e conectores box reto | 350,00 | un | **370,00** | `un` | Conexões |

#### Critério de Recebimento (POP 06 / POP 16):
- Tubulações 100% antichama NBR 15465 com gravação visível;
- Caixas com fixadores íntegros sem deformações na rosca dos parafusos.

---

## 📦 RC-015/2026 — Argamassa Industrializada de Projeção para Emboço Paulista

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-015/2026` |
| **Disciplina** | Revestimentos de Parede |
| **EAP Vinculada** | `1.5.1, 1.5.2` |
| **Centro de Custo (CC)** | **`CC-405`** |
| **Disparo da RC** | 01/12/2026 |
| **Data Necessária no Canteiro** | **20/12/2026** (Lead: 19d) |
| **Custo Direto Base** | **R$ 12.800,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 15.1 | Argamassa industrializada estabilizada para máquina de projeção contínua | 480,00 | sc | **480,00** | `sc 40kg (paletes)` | NBR 13281 |
| 15.2 | Chapisco rolado industrializado aditivado com polímeros sintéticos (Bianco) | 24,00 | gl | **24,00** | `gl 18L` | Aderência Estrutura |
| 15.3 | Cantoneiras de PVC perfuradas para proteção de cantos vivos e requadros | 180,00 | m | **190,00** | `m (barras 2,5m)` | Acabamento |

#### Critério de Recebimento (POP 06 / POP 13):
- Sacos paletizados secos sem formação de grumos;
- Granulometria controlada para não entupir mangueiras da máquina de projeção.

---

## 📦 RC-016/2026 — Esquadrias de Alumínio Anodizado Preto e Vidros Temperados

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-016/2026` |
| **Disciplina** | Esquadrias e Vidros |
| **EAP Vinculada** | `1.6.1 a 1.6.4` |
| **Centro de Custo (CC)** | **`CC-702`** |
| **Disparo da RC** | 01/11/2026 |
| **Data Necessária no Canteiro** | **10/01/2027** (Lead: 70d) |
| **Custo Direto Base** | **R$ 58.400,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 16.1 | Janela de correr 4 folhas J1 (2,00x1,20m) alumínio preto fosco c/ vidro temperado 8mm | 8,00 | un | **8,00** | `cj completo` | ESQ-001 (Janelas) |
| 16.2 | Janela de correr 2 folhas J2 (1,50x1,20m) alumínio preto fosco c/ vidro temperado 8mm | 6,00 | un | **6,00** | `cj completo` | ESQ-001 |
| 16.3 | Maxim-ar sanitários J3 (0,80x0,60m) alumínio preto fosco c/ vidro mini-boreal 6mm | 4,00 | un | **4,00** | `cj completo` | ESQ-001 |
| 16.4 | Fachada pele de vidro structural glazing c/ vidros laminados refletivos de controle solar | 18,40 | m² | **18,40** | `m² instalado` | Fachada Principal |

#### Critério de Recebimento (POP 06 / POP 25):
- Anodização classe A20 (20 micras) resistente à maresia portuária do Açu;
- Selo de têmpera do INMETRO gravado de forma indelével em cada vidro;
- Acompanhamento dos contramarcos chumbados previamente com nível a laser.
"""

# -------------------------------------------------------------------------
# MÊS 5: RC-017 a RC-020 (Pisos, Portas, Fiação e Quadros)
# -------------------------------------------------------------------------
MES5_CONTENT = """# 📋 REQUISIÇÕES DE COMPRA FORMAIS — MÊS 5 (PISOS, PORTAS E ELÉTRICA)

**Empreendimento:** Edifício Administrativo TMULT — Terminal Multiuso (Porto do Açu - SJB/RJ)  
**Gestor do Contrato / Solicitante:** Eng. Alexandre (Engenheiro Residente & PMO Virtual)  
**Data de Emissão:** 05/12/2026 | **Linha de Base:** Baseline 01 (Semanas S17 a S20)  
**Ref. Normativa do Ecossistema:** `POP_05_SOLICITACAO_COMPRAS.md`, `POP_06_RECEBIMENTO.md`, `POP_16_ELETRICA.md`, `SKILL_GESTAO_05_QUALIDADE.md`

---

## 🧭 1. Diretrizes Normativas de Emissão e Recebimento
1. **Lote Único de Porcelanato:** Compra com 10% de sobra técnica garantindo o mesmo lote e tom em 100% da área útil (368,40 m²);
2. **Kits Porta Pronta em WPC:** Batentes e guarnições resistentes à água para suportar a umidade e a limpeza industrial;
3. **Cobre Eletrolítico Homologado:** Condutores elétricos 100% em conformidade com a NBR 5410 com ensaio de resistência ôhmica.

---

## 📦 RC-017/2026 — Porcelanato Retificado 60x60cm e Argamassa Colante AC-III

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-017/2026` |
| **Disciplina** | Pisos e Revestimentos Cerâmicos |
| **EAP Vinculada** | `1.7.1, 1.7.2` |
| **Centro de Custo (CC)** | **`CC-704`** |
| **Disparo da RC** | 10/12/2026 |
| **Data Necessária no Canteiro** | **15/01/2027** (Lead: 36d) |
| **Custo Direto Base** | **R$ 35.200,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 17.1 | Porcelanato esmaltado acetinado 60x60cm retificado borda reta PEI-4 cor cinza claro | 368,40 | m² | **410,00** | `m² (caixas 1,80m²)` | PIS-001 (Paginação) |
| 17.2 | Rodapé porcelanato h=10cm cortado e biselado em fábrica | 180,00 | m | **195,00** | `m` | Acabamentos |
| 17.3 | Argamassa colante industrializada tipo AC-III flexível para porcelanato grandes formatos | 80,00 | sc | **85,00** | `sc 20kg (paletes)` | NBR 14081 |
| 17.4 | Rejunte porcelanato resinado impermeável anti-fungo (junta 1,5mm) | 45,00 | kg | **50,00** | `pcts 1kg` | Cores Cinza Platina |
| 17.5 | Rejunte bicomponente epóxi para áreas molhadas (sanitários e copa) | 18,00 | kg | **20,00** | `baldes 1kg` | Áreas Úmidas |

#### Critério de Recebimento (POP 06):
- Conferência rigorosa do código de tonalidade e calibre em todas as caixas descarregadas;
- Assentamento por dupla colagem com desempenadeira denteada 8x8mm.

---

## 📦 RC-018/2026 — Kits Porta Pronta de Madeira Melamínica e Fechaduras em Inox

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-018/2026` |
| **Disciplina** | Esquadrias de Madeira |
| **EAP Vinculada** | `1.6.5` |
| **Centro de Custo (CC)** | **`CC-701`** |
| **Disparo da RC** | 05/12/2026 |
| **Data Necessária no Canteiro** | **20/01/2027** (Lead: 46d) |
| **Custo Direto Base** | **R$ 17.800,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 18.1 | Kit porta pronta 0,80x2,10m melamínica branca c/ batente WPC regulável e guarnições | 10,00 | un | **10,00** | `kits completos` | ARQ-005 (Portas) |
| 18.2 | Kit porta pronta 0,90x2,10m PNE acessibilidade NBR 9050 c/ batente regulável | 2,00 | un | **2,00** | `kits completos` | Portas Acessíveis |
| 18.3 | Kit porta pronta 0,70x2,10m para cabines sanitárias | 2,00 | un | **2,00** | `kits completos` | Sanitários |
| 18.4 | Fechaduras de embutir completas com maçaneta tipo alavanca em aço inox 304 | 14,00 | un | **14,00** | `un (La Fonte/Pado)` | Ferragens Inox |

#### Critério de Recebimento (POP 06):
- Folhas de porta seladas em plástico bolha; ausência de lascas ou riscos nas bordas;
- Batentes em WPC polímero resistente à água para evitar estufamento por umidade.

---

## 📦 RC-019/2026 — Cabos Elétricos de Cobre Flexível 750V / 1kV (1,5 a 50 mm²)

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-019/2026` |
| **Disciplina** | Instalações Elétricas (Cabeamento e Fiação) |
| **EAP Vinculada** | `2.2.3, 2.2.4` |
| **Centro de Custo (CC)** | **`CC-605`** |
| **Disparo da RC** | 05/01/2027 |
| **Data Necessária no Canteiro** | **25/01/2027** (Lead: 20d) |
| **Custo Direto Base** | **R$ 31.200,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 19.1 | Cabo de cobre flexível 750V antichama BWF 2,5mm² (Azul, Preto, Vermelho, Verde) | 2.200,00 | m | **2.400,00** | `m (24 rolos 100m)` | ELE-003 (Circuitos) |
| 19.2 | Cabo de cobre flexível 750V antichama BWF 4,0mm² e 6,0mm² (Ar-condicionado e Copa) | 950,00 | m | **1.000,00** | `m (10 rolos 100m)` | ELE-003 |
| 19.3 | Cabo de cobre flexível 1kV antichama 16mm² e 50mm² (Alimentadores dos Quadros) | 380,00 | m | **400,00** | `m (bobinas)` | ELE-002 (Prumada) |
| 19.4 | Cabo de rede telecom Cat6 U/UTP 4 pares azul 100% cobre homologado Anatel | 850,00 | m | **1.000,00** | `m (3 caixas 305m)` | TEL-001 (Dados) |

#### Critério de Recebimento (POP 06 / POP 16):
- Fabricantes homologados: Prysmian, Sil ou Corfio com selo INMETRO;
- Proibido cabo de cobre recozido ferro-cobre (ensaiado com ímã de neodímio e micrômetro).

---

## 📦 RC-020/2026 — Quadros QDG/QDF, Disjuntores DIN, DPS, Tomadas e Luminárias LED

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-020/2026` |
| **Disciplina** | Painéis Elétricos e Aparelhagem Terminal |
| **EAP Vinculada** | `2.2.5, 2.2.6, 2.2.7` |
| **Centro de Custo (CC)** | **`CC-606`** |
| **Disparo da RC** | 10/01/2027 |
| **Data Necessária no Canteiro** | **28/01/2027** (Lead: 18d) |
| **Custo Direto Base** | **R$ 15.900,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 20.1 | Quadro de Distribuição Geral QDG 36 disjuntores metálico de embutir c/ barramento | 1,00 | un | **1,00** | `un completo` | ELE-004 (Diagrama) |
| 20.2 | Quadro de Força e Ar-Condicionado QDF 24 disjuntores com barramento bifásico | 1,00 | un | **1,00** | `un completo` | ELE-004 |
| 20.3 | Disjuntores termomagnéticos DIN curva C (10A, 16A, 20A, 32A e 63A tetrapolar) | 48,00 | un | **52,00** | `un (Schneider)` | Diagrama Unifilar |
| 20.4 | Dispositivos DPS Classe II 45kA 275V e Interruptores Diferenciais DR 30mA | 8,00 | un | **8,00** | `un` | Proteção NBR 5410 |
| 20.5 | Conjuntos modulares placa 4x2 tomadas 10A/20A, interruptores e RJ-45 | 85,00 | un | **90,00** | `un (Pial/Schneider)` | Acabamento |
| 20.6 | Luminárias de embutir LED 60x60cm 40W 4000K (Luz Neutra) alto rendimento | 48,00 | un | **48,00** | `un` | ILU-001 (Iluminação) |

#### Critério de Recebimento (POP 06):
- Disjuntores e DPS de linha profissional (Schneider Electric ou Siemens);
- Luminárias com driver eletrônico isolado bivolt e fator de potência > 0,95.
"""

# -------------------------------------------------------------------------
# MÊS 6: RC-021 a RC-024 (Louças, Climatização, Pintura e Entrega)
# -------------------------------------------------------------------------
MES6_CONTENT = """# 📋 REQUISIÇÕES DE COMPRA FORMAIS — MÊS 6 (FINALIZAÇÃO E CLOSEOUT)

**Empreendimento:** Edifício Administrativo TMULT — Terminal Multiuso (Porto do Açu - SJB/RJ)  
**Gestor do Contrato / Solicitante:** Eng. Alexandre (Engenheiro Residente & PMO Virtual)  
**Data de Emissão:** 15/01/2027 | **Linha de Base:** Baseline 01 (Semanas S21 a S26)  
**Ref. Normativa do Ecossistema:** `POP_05_SOLICITACAO_COMPRAS.md`, `POP_06_RECEBIMENTO.md`, `POP_18_ASBUILT_DATABOOK.md`

---

## 🧭 1. Diretrizes Normativas de Emissão e Recebimento
1. **Climatização Sustentável:** Aparelhos Split Inverter com fluido ecológico R-32 e selo Procel A de eficiência energética;
2. **Louças e Metais Economizadores:** Válvulas Duo 3/6L e torneiras hidromecânicas temporizadas atendendo metas ESG do Porto do Açu;
3. **Pintura e Tratamento de Superfície:** Tintas laváveis antimofo resistentes a intempéries e maresia.

---

## 📦 RC-021/2026 — Louças Sanitárias Deca e Metais Temporizados Docol

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-021/2026` |
| **Disciplina** | Aparelhos Sanitários e Metais |
| **EAP Vinculada** | `2.1.4, 2.1.5` |
| **Centro de Custo (CC)** | **`CC-603`** |
| **Disparo da RC** | 20/01/2027 |
| **Data Necessária no Canteiro** | **15/02/2027** (Lead: 26d) |
| **Custo Direto Base** | **R$ 23.400,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 21.1 | Bacia sanitária com caixa acoplada Deca Vogue Plus sistema descarga Duo 3/6 litros | 6,00 | un | **6,00** | `cj completo c/ assento` | SAN-002 |
| 21.2 | Lavatório de coluna suspensa Deca Izy em louça branca brilhante com ladrão | 6,00 | un | **6,00** | `un c/ fixadores` | SAN-002 |
| 21.3 | Cuba de embutir em aço inox 304 escovado (50x40cm) para bancada da copa | 2,00 | un | **2,00** | `un (Tramontina)` | Detalhe Copa |
| 21.4 | Torneira de mesa temporizada antivandalismo Docol PressMatic fechamento aut. 6s | 8,00 | un | **8,00** | `un cromada` | NBR 10281 |
| 21.5 | Válvulas de escoamento em metal cromado, sifões articulados e rabichos flexíveis inox | 12,00 | un | **12,00** | `kits de ligação` | Conexões Finais |

#### Critério de Recebimento (POP 06):
- Louças 100% brancas sem trincas, quebras ou defeitos de esmalte;
- Metais em embalagens lacradas com garantia de 10 anos do fabricante.

---

## 📦 RC-022/2026 — Aparelhos de Ar-Condicionado Split Inverter R-32 (12k a 24k BTU)

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-022/2026` |
| **Disciplina** | Climatização e Ventilação Mecânica |
| **EAP Vinculada** | `2.3.1, 2.3.2` |
| **Centro de Custo (CC)** | **`CC-608`** |
| **Disparo da RC** | 05/01/2027 |
| **Data Necessária no Canteiro** | **20/02/2027** (Lead: 46d) |
| **Custo Direto Base** | **R$ 38.900,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 22.1 | Ar-Condicionado Split Hi-Wall Inverter 12.000 BTU/h Quente/Frio Procel A R-32 | 4,00 | un | **4,00** | `un completa (Daiki/LG)` | CLIM-001 |
| 22.2 | Ar-Condicionado Split Hi-Wall Inverter 18.000 BTU/h Quente/Frio Procel A R-32 | 2,00 | un | **2,00** | `un completa` | CLIM-001 |
| 22.3 | Ar-Condicionado Split Cassete 4 Vias Inverter 24.000 BTU/h para Sala Reunião | 2,00 | un | **2,00** | `un completa` | Sala Diretoria |
| 22.4 | Tubulação de cobre sem costura isolada elastomérica e suportes condensadoras | 160,00 | m | **160,00** | `m linhas prontas` | Tubos Cobre |

#### Critério de Recebimento (POP 06):
- Verificação da carga ecológica R-32 e nota fiscal com indicação dos números de série;
- Teste de vácuo profundo < 500 microns e estanqueidade pressurizado a N2 400 psi antes da carga final.

---

## 📦 RC-023/2026 — Tintas Acrílicas Premium, Massa Corrida e Textura

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-023/2026` |
| **Disciplina** | Pintura e Tratamento de Superfícies |
| **EAP Vinculada** | `1.8.1, 1.8.2` |
| **Centro de Custo (CC)** | **`CC-706`** |
| **Disparo da RC** | 25/01/2027 |
| **Data Necessária no Canteiro** | **18/02/2027** (Lead: 24d) |
| **Custo Direto Base** | **R$ 14.200,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 23.1 | Tinta látex acrílico premium acabamento fosco lavável cor Branco Neve (galões 18L) | 32,00 | lt | **32,00** | `latas 18L` | PIN-001 |
| 23.2 | Tinta acrílica para piso de alta resistência cor Cinza Médio (áreas técnicas) | 10,00 | lt | **10,00** | `latas 18L` | Sala de Máquinas |
| 23.3 | Massa acrílica exterior resistente à intempérie e umidade | 16,00 | bd | **16,00** | `baldes 18L (28kg)` | Fachada |
| 23.4 | Massa corrida PVA interior para alvenarias de drywall e reboco liso | 12,00 | bd | **12,00** | `baldes 18L (28kg)` | Salas e Escritórios |
| 23.5 | Fundo preparador de paredes à base d'água e selador acrílico pigmentado | 14,00 | lt | **14,00** | `latas 18L` | Fundo Selador |

#### Critério de Recebimento (POP 06):
- Fabricantes homologados: Suvinil, Coral ou Sherwin-Williams;
- Latas hermeticamente lacradas, sem ferrugem nas tampas e com lote de fabricação recente (< 6 meses).

---

## 📦 RC-024/2026 — Limpeza Fina Pós-Obra, Testes Globais e Desmobilização

| Campo de Governança | Detalhamento Operacional |
| :--- | :--- |
| **Número da RC** | `RC-024/2026` |
| **Disciplina** | Entrega da Obra e Closeout |
| **EAP Vinculada** | `1.9.1, 1.9.2` |
| **Centro de Custo (CC)** | **`CC-105`** |
| **Disparo da RC** | 05/02/2027 |
| **Data Necessária no Canteiro** | **25/02/2027** (Lead: 20d) |
| **Custo Direto Base** | **R$ 9.400,00** |

### Itens Técnicos e UCC
| Item | Descrição Técnica Normativa | Qtd Proj | Und Proj | Qtd Compra | Und UCC | Prancha Ref. |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 24.1 | Serviço especializado de limpeza fina de piso porcelanato, vidros e esquadrias | 368,40 | m² | **368,40** | `m² (equipe c/ enceradeira)`| POP 18 |
| 24.2 | Produtos químicos biodegradáveis decapantes e neutralizadores de cimento | 1,00 | vb | **1,00** | `kit químico industrial` | Sem Danos ao Vidro |
| 24.3 | Desmobilização geral de containers, caçambas e recomposição final de canteiro | 1,00 | vb | **1,00** | `vb` | Encerramento Obra |

#### Critério de Recebimento (POP 06 / POP 18):
- Inspeção por luz rasante: ausência total de respingos de tinta, cimento ou poeira;
- Entrega das chaves etiquetadas e emissão do Termo de Recebimento Provisório sem pendências.
"""

def gerar_todos_dossies():
    arquivos = [
        ("REQUISICOES_DE_COMPRA_MES2_TMULT.md", MES2_CONTENT),
        ("REQUISICOES_DE_COMPRA_MES3_TMULT.md", MES3_CONTENT),
        ("REQUISICOES_DE_COMPRA_MES4_TMULT.md", MES4_CONTENT),
        ("REQUISICOES_DE_COMPRA_MES5_TMULT.md", MES5_CONTENT),
        ("REQUISICOES_DE_COMPRA_MES6_TMULT.md", MES6_CONTENT),
    ]
    for nome, conteudo in arquivos:
        caminho = os.path.join(OUTPUT_DIR, nome)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print(f"Gerado: {caminho}")

if __name__ == "__main__":
    gerar_todos_dossies()
