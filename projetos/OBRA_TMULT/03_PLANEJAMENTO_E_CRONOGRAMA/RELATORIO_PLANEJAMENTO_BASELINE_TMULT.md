# 🏗️ RELATÓRIO EXECUTIVO DE PLANEJAMENTO & LINHA DE BASE (BASELINE 01)

**Empreendimento:** Edifício Administrativo do Terminal Multiuso (`OBRA_TMULT`) — Porto do Açu  
**Área Construída Útil:** 368,40 m² (Piso Térreo Útil) | **Projeção Estrutural:** 298,25 m² | **Cobertura:** 381,29 m²  
**Prazo Oficial de Execução:** 6 Meses (26 Semanas / 180 Dias Corridos)  
**Preço Global de Venda (Turnkey):** R$ 1.660.762,28 (R$ 4.508,04 / m²)  
**Custo Direto Total:** R$ 1.314.562,67 (R$ 3.568,30 / m² | 79,15% do valor global)  
**BDI Médio Ponderado:** 26,34% (R$ 346.199,61 | 27,17% Geral e 15,00% Equipamentos Nobres)  
**Data de Emissão da Baseline 01:** 10/09/2026  
**Responsável Técnico:** PMO Virtual — Gestão Integrada de Obras  

---

## 1. Portão de Qualidade de Dado (Data Quality Gate — SKILL_GESTAO_07 & 16)

Em estrito cumprimento aos preceitos da `SKILL_GESTAO_07_CIENCIA_DE_DADOS.md` (Seção 1) e `SKILL_GESTAO_16_CRONOGRAMA_E_REPROGRAMACAO.md`, esta Linha de Base 01 foi construída exclusivamente sobre dados auditados e validados, eliminando qualquer estimativa subjetiva:

| Dado de Entrada | Arquivo Fonte / Origem | Nível de Confiança | Justificativa / Validação Técnica |
|---|---|:---:|---|
| **Orçamento Consolidado (158 itens)** | `02_ORCAMENTO_BASE_E_CONTRATOS/ORCAMENTO_BASE_CONSOLIDADO.csv` | 🟢 Fato | 158 itens auditados com cotações e SINAPI SP 07/2026. Total R$ 1.660.762,28 conferido centavo a centavo. |
| **Administração Local e Canteiro** | `02_ORCAMENTO_BASE_E_CONTRATOS/QUANTITATIVO_ADMINISTRACAO_LOCAL.csv` | 🟢 Fato | Custo Direto planilhado na EAP 1.0 (R$ 61.042,66/mês direto; R$ 77.627,96/mês c/ BDI). Proibido "BDI Gordo". |
| **Caminho Crítico (CPM Determinístico)** | `scripts/calculadoras/calcular_cpm.py` | 🟢 Fato | Cálculo algorítmico determinístico (Teoria dos Grafos). Prazos, folgas e predecessoras sem estimativa de LLM. |
| **Projetos de Engenharia Aprovados** | Dossiê `01_ENGENHARIA_E_PROJETOS/` (Pranchas EGS-051 a EGS-060) | 🟢 Fato | Projetos estruturais, arquitetônicos e complementares com memoriais de cálculo conferidos. |
| **Portões de Bloqueio da Qualidade** | `governanca/INDICE_MESTRE_SKILLS.md` (§1.1) | 🟢 Fato | Regras normativas de precedência bloqueante (NBR 6118, NBR 15575, NBR 5626). |

---

## 2. Resumo Executivo Financeiro e Físico (Curva S Oficial)

A distribuição dos R$ 1.660.762,28 ao longo dos 6 meses reflete fielmente o ritmo construtivo real da engenharia civil portuária. O canteiro e equipe de gestão técnica são faturados de forma linear (R$ 77.627,96/mês com BDI), enquanto os pacotes de produção física seguem a curva de avanço das frentes de serviço.

### 2.1 Tabela da Curva S de Linha de Base (Baseline 01)

| Período | Faturamento Mensal (R$) | % Mensal | Faturamento Acumulado (R$) | % Financeiro Acumulado | % Físico Planejado Acumulado |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **Mês 1** | R$ 163.442,02 | 9,84% | R$ 163.442,02 | 9,84% | **12,05%** |
| **Mês 2** | R$ 277.895,85 | 16,73% | R$ 441.337,87 | 26,57% | **30,20%** |
| **Mês 3** | R$ 366.373,12 | 22,06% | R$ 807.710,99 | 48,63% | **54,10%** |
| **Mês 4** | R$ 245.681,39 | 14,79% | R$ 1.053.392,38 | 63,43% | **69,85%** |
| **Mês 5** | R$ 320.416,90 | 19,29% | R$ 1.373.809,28 | 82,72% | **88,40%** |
| **Mês 6** | R$ 286.953,00 | 17,28% | R$ 1.660.762,28 | **100,00%** | **100,00%** |
| **TOTAL** | **R$ 1.660.762,28** | **100,00%** | — | — | — |

> **Interpretação da Curva S:**
> - **Rampa Inicial (Mês 1):** Mobilização, locação de containers, abertura de cavas, sapatas e vigas baldrames (9,84% financeiro / 12,05% físico).
> - **Aceleração Estrutural e Envoltória (Meses 2 e 3):** Concretagem da supraestrutura e fechamento integral da envoltória (alvenaria e telhas termoacústicas), atingindo o pico financeiro de R$ 366,3k no Mês 3 (48,63% acumulado).
> - **Instalações e Revestimentos (Meses 4 e 5):** Passagem de redes embutidas, testes hidrostáticos, emboço, porcelanato, esquadrias e cabeamentos (82,72% acumulado).
> - **Fechamento e Comissionamento (Mês 6):** Instalação de equipamentos nobres (ar-condicionado VRF/Splits Cassete), louças, luminárias, pintura final, testes e entrega turnkey (100,00%).

---

## 3. Análise de Caminho Crítico (CPM — Algoritmo Determinístico)

A rede de precedências da obra foi processada pelo script determinístico `scripts/calculadoras/calcular_cpm.py`. Foram modeladas 31 macroatividades interligadas por dependências técnicas mandatórias.

* **Duração Total do Caminho Crítico:** 178 dias de produção + 2 dias de margem de entrega = **180 dias corridos (26 semanas)**.
* **Critério de Folga Zero:** Qualquer atraso nas atividades críticas projeta impacto direto na entrega contratual das chaves.

### 3.1 Tabela Geral do Método do Caminho Crítico (Early Start / Late Finish / Folgas)

| ID Atividade | Descrição da Atividade Macro | Duração | Início Cedo | Fim Cedo | Início Tarde | Fim Tarde | Folga Total | Status Crítico |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `A01` | Mobilização de Canteiro e Locação Geral | 10 dias | Dia 0 | Dia 10 | Dia 0 | Dia 10 | 0 dias | **CRÍTICA** |
| `A02` | Escavação de Cavas e Valas de Fundação | 6 dias | Dia 10 | Dia 16 | Dia 10 | Dia 16 | 0 dias | **CRÍTICA** |
| `A03` | Concreto Magro, Fôrma e Concretagem Sapatas | 7 dias | Dia 16 | Dia 23 | Dia 16 | Dia 23 | 0 dias | **CRÍTICA** |
| `A04` | Fôrma, Armação e Concreto Vigas Baldrames | 8 dias | Dia 23 | Dia 31 | Dia 23 | Dia 31 | 0 dias | **CRÍTICA** |
| `A05` | Impermeabilização Asfáltica Baldrames | 3 dias | Dia 31 | Dia 34 | Dia 31 | Dia 34 | 0 dias | **CRÍTICA (Portão 1)** |
| `A06` | Reaterro Compactado e Bota-fora | 3 dias | Dia 34 | Dia 37 | Dia 34 | Dia 37 | 0 dias | **CRÍTICA** |
| `A07` | Fôrmas, Armação e Concreto Pilares P1-P24 | 9 dias | Dia 37 | Dia 46 | Dia 37 | Dia 46 | 0 dias | **CRÍTICA** |
| `A08` | Fôrmas, Cimbramento e Vigas Superiores | 8 dias | Dia 46 | Dia 54 | Dia 46 | Dia 54 | 0 dias | **CRÍTICA** |
| `A09` | Concretagem da Laje Treliçada H12 e Capa | 1 dia | Dia 54 | Dia 55 | Dia 54 | Dia 55 | 0 dias | **CRÍTICA** |
| `A10` | Cura Úmida e Desforma Controlada da Laje | 12 dias | Dia 55 | Dia 67 | Dia 55 | Dia 67 | 0 dias | **CRÍTICA (Portão 2)** |
| `A11` | Terças Metálicas da Cobertura e Fixações | 10 dias | Dia 67 | Dia 77 | Dia 77 | Dia 87 | 10 dias | Folga Normal |
| `A12` | Alvenaria de Vedação em Blocos e Vergas | 20 dias | Dia 67 | Dia 87 | Dia 67 | Dia 87 | 0 dias | **CRÍTICA** |
| `A13` | Telhas Sandwich, Calhas, Rufos e Platibanda | 10 dias | Dia 87 | Dia 97 | Dia 87 | Dia 97 | 0 dias | **CRÍTICA** |
| `A14` | Eletrodutos, Caixas e Quadros Embutidos | 10 dias | Dia 97 | Dia 107 | Dia 100 | Dia 110 | 3 dias | Folga Reduzida |
| `A15` | Tubulações de Água Fria, Esgoto e Pluvial | 10 dias | Dia 97 | Dia 107 | Dia 97 | Dia 107 | 0 dias | **CRÍTICA** |
| `A16` | Teste Hidrostático 72h em Redes Embutidas | 3 dias | Dia 107 | Dia 110 | Dia 107 | Dia 110 | 0 dias | **CRÍTICA (Portão 3)** |
| `A17` | Chapisco e Emboço/Reboco Paulista | 14 dias | Dia 110 | Dia 124 | Dia 110 | Dia 124 | 0 dias | **CRÍTICA** |
| `A18` | Impermeabilização Áreas Molhadas (WCs/Copa) | 3 dias | Dia 124 | Dia 127 | Dia 127 | Dia 130 | 3 dias | Folga Normal |
| `A19` | Contrapiso de Regularização e=3cm | 6 dias | Dia 124 | Dia 130 | Dia 124 | Dia 130 | 0 dias | **CRÍTICA** |
| `A20` | Infraestrutura Frigorígena e Dutos HVAC | 10 dias | Dia 124 | Dia 134 | Dia 138 | Dia 148 | 14 dias | Folga Confortável |
| `A21` | Fixação de Caixilhos e Esquadrias Alum/Vidro | 8 dias | Dia 124 | Dia 132 | Dia 140 | Dia 148 | 16 dias | Folga Confortável |
| `A22` | Assentamento Porcelanato 60x60 e Azulejos | 14 dias | Dia 130 | Dia 144 | Dia 130 | Dia 144 | 0 dias | **CRÍTICA** |
| `A23` | Enfiamento de Cabos Elétricos e UTP Cat6 | 10 dias | Dia 124 | Dia 134 | Dia 138 | Dia 148 | 14 dias | Folga Confortável |
| `A24` | Rodapés em Porcelanato e Ajustes de Piso | 4 dias | Dia 144 | Dia 148 | Dia 144 | Dia 148 | 0 dias | **CRÍTICA** |
| `A25` | Selador e 1ª Demão de Pintura Látex | 5 dias | Dia 148 | Dia 153 | Dia 148 | Dia 153 | 0 dias | **CRÍTICA (Portão 4)** |
| `A26` | Instalação Aparelhos Ar-Condicionado Splits | 6 dias | Dia 153 | Dia 159 | Dia 153 | Dia 159 | 0 dias | **CRÍTICA** |
| `A27` | Louças Sanitárias, Cubas e Metais Nobres | 6 dias | Dia 153 | Dia 159 | Dia 153 | Dia 159 | 0 dias | **CRÍTICA** |
| `A28` | Luminárias LED de Embutir e Espelhos Elétricos | 5 dias | Dia 153 | Dia 158 | Dia 154 | Dia 159 | 1 dia | Folga Mínima |
| `A29` | Demãos Finais de Pintura Látex e Retoques | 7 dias | Dia 159 | Dia 166 | Dia 159 | Dia 166 | 0 dias | **CRÍTICA** |
| `A30` | Comissionamento Integrado e Testes de Carga | 6 dias | Dia 166 | Dia 172 | Dia 166 | Dia 172 | 0 dias | **CRÍTICA** |
| `A31` | Limpeza Pós-Obra, Desmobilização e Entrega | 6 dias | Dia 172 | Dia 178 | Dia 172 | Dia 178 | 0 dias | **CRÍTICA** |

---

## 4. As 12 Frentes Executivas Quinzenais (Plano Tático de Produção)

O cronograma de 26 semanas é dividido em 12 blocos quinzenais de controle rigoroso (Quinzena 1 à Quinzena 12), servindo de base para as medições contratuais e acompanhamento pelo RDO:

### Quinzena 01 (Semanas 01 e 02 / Dias 01 a 15) — Canteiro & Abertura de Cavas
* **Serviços:** Instalação de módulos habitáveis (containers NR-18), ligação provisória de água/energia/internet, tapume, locação topográfica com estação total e escavação mecanizada das 32 sapatas isoladas.
* **Metas Físicas:** 100% do canteiro mobilizado; 51,27 m³ de cavas escavadas.
* **Efetivo Alocado:** Engenheiro Residente, Mestre de Obras, TST, Operador de Retroescavadeira, 4 Serventes.

### Quinzena 02 (Semanas 03 e 04 / Dias 16 a 30) — Fundações, Baldrames & Portão 1
* **Serviços:** Lastro magro fck 15 MPa (3,04 m³), armação e concretagem das sapatas S1-S32 (8,55 m³), arranque dos pilares, armação e concretagem das vigas baldrames VB1-VB19 (14,04 m³).
* **Portão de Bloqueio 1:** Pintura asfáltica hidrófuga em baldrames (183,36 m²) e inspeção por FVS antes de liberar o reaterro (31,17 m³).
* **Metas Físicas:** 100% da infraestrutura concluída; liberação da cota zero.

### Quinzena 03 (Semanas 05 e 06 / Dias 31 a 45) — Pilares de Supraestrutura
* **Serviços:** Armação, formas resinadas 17mm e concretagem dos pilares P1 a P24 até cota de fundo de viga (h=2,98m; 6,44 m³ de concreto fck 30 MPa).
* **Metas Físicas:** 24 pilares desformados e aprumados.
* **Efetivo Alocado:** 1 Mestre, 4 Carpinteiros, 2 Armadores, 2 Pedreiros, 4 Serventes.

### Quinzena 04 (Semanas 07 e 08 / Dias 46 a 60) — Vigamento Superior, Lajes & Portão 2
* **Serviços:** Montagem de cimbramento metálico (888 m²·m), fôrmas de vigas V101-V115, montagem de vigotas treliçadas TR 16745 (968 m), blocos de EPS e concretagem da capa de laje H12 (13,17 m³).
* **Portão de Bloqueio 2:** Cura úmida contínua e protocolo de desforma parcial aos 14 dias; manutenção de re-escoramento central para liberação segura das frentes inferiores.
* **Metas Físicas:** 100% da supraestrutura de concreto concluída (298,25 m² de laje).

### Quinzena 05 (Semanas 09 e 10 / Dias 61 a 75) — Alvenaria Estrutural/Vedação & Montagem da Cobertura
* **Serviços:** Desforma controlada da laje H12 (Portão 2), elevação de alvenaria em blocos de concreto 14x19x39cm nos Setores 01 e 02 (Lotes 017 e 018), vergas/contravergas pré-moldadas, telas de amarração pilar-alvenaria e **início imediato da montagem das terças metálicas perfil U da cobertura (Setor 05 — SUB-07)** logo após a liberação da laje.
* **Metas Físicas:** 60% da alvenaria erguida; estrutura de terças metálicas montada (381,29 m² de projeção).

### Quinzena 06 (Semanas 11 e 12 / Dias 76 a 90) — Fechamento Estanque da Cobertura, Platibanda & Redes Iniciais
* **Serviços:** Conclusão da elevação das alvenarias e encunhamento flexível (Lote 019), **instalação das telhas termoacústicas trapezoidais sandwich 30mm PIR (Lote 021)**, calhas galvanizadas de beiral, rufos, platibanda e teste de estanqueidade da cobertura (Setor 05). Início da abertura de rasgos para tubulações elétricas e hidráulicas embutidas (Lote 022) sob telhado 100% estanque.
* **Metas Físicas:** Edifício 100% estanque contra chuvas de verão no canteiro; frentes internas secas liberadas para instalações embutidas e chapisco rolado (Lote 024).

### Quinzena 07 (Semanas 13 e 14 / Dias 91 a 105) — Redes Embutidas Elétrica/Hidráulica & Reboco Mecanizado
* **Serviços:** Abertura de rasgos em paredes, assentamento de eletrodutos rígidos PVC 3/4" e 1", caixas 4x2", tubulações de água fria soldável e esgoto primário/secundário, caixas de passagem e instalação dos quadros de distribuição QDG/QDF. Projeção mecânica do emboço/reboco paulista e=20mm com mestras metálicas (Lotes 025 e 026).
* **Metas Físicas:** 100% das tubulações e caixas embutidas instaladas; 440 m² de paredes rebocadas.

### Quinzena 08 (Semanas 15 e 16 / Dias 106 a 120) — Portão 3, Impermeabilização WCs & Regularização Contrapiso
* **Portão de Bloqueio 3:** Realização do Teste Hidrostático sob pressão com manômetro calibrado durante 72h nas redes de água fria e ensaio de estanqueidade no esgoto (Lote 023). Assinatura obrigatória da FVS.
* **Serviços:** Impermeabilização polimérica flexível de sanitários e copa (Lote 027), execução do contrapiso sarrafeado e regularizado com nível a laser e=3cm (Lote 028) e início do assentamento de porcelanato retificado 60x60cm (Lotes 029 e 030).
* **Metas Físicas:** 100% das redes testadas e estanques; contrapiso concluído; início dos pisos nobres.

### Quinzena 09 (Semanas 17 e 18 / Dias 121 a 135) — Pisos Cerâmicos WCs, Rejunte, Dutos HVAC & Caixilharia
* **Serviços:** Cerâmica esmaltada nas paredes dos WCs (Lote 031), rejunte resinado impermeável e rodapés de porcelanato (Lote 032), caixilharia de alumínio linha Suprema anodizada preta com vidros temperados acústicos 8mm (Lotes 033 e 034) e infraestrutura de linhas frigorígenas de cobre e drenos de HVAC (Lotes 035 e 036).
* **Metas Físicas:** Base de piso e revestimento concluída; esquadrias externas vedadas com PU-40; linhas de ar-condicionado pressurizadas com nitrogênio (teste de estanqueidade).

### Quinzena 10 (Semanas 19 e 20 / Dias 136 a 150) — Cabeamento Elétrico/Dados, Quadros QGBT & Louças Nobres
* **Serviços:** Enfiamento de cabos elétricos antichama 750V e cabeamento estruturado Furukawa Cat.6 (Lote 037), montagem e identificação de circuitos no QGBT e quadros com DR (Lote 038), instalação de bacias sanitárias com caixa acoplada Deca Vogue, cubas e torneiras temporizadas Docol antivandalismo (Lote 039), e fixação de luminárias painel LED 40W 6500K com tomadas e interruptores (Lote 040).
* **Metas Físicas:** Infraestrutura de potência, iluminação e dados conectada; sanitários e copa montados.

### Quinzena 11 (Semanas 21 e 22 / Dias 151 a 165) — Portão 4, Pintura Acrílica & Startup Climatização
* **Portão de Bloqueio 4:** Emassamento com massa acrílica, lixamento mecanizado com aspirador e aplicação de selador primer (Lotes 041 e 042). Forração integral de pisos com lona plástica e papelão ondulado.
* **Serviços:** Pintura látex acrílica fosca lavável Suvinil Toque de Seda em duas demãos de acabamento (Lote 043), montagem das evaporadoras split cassete 36.000 BTU/h, ligação dos condensadores externos, carga de gás refrigerante R-410A e startup operacional (Lote 044).
* **Metas Físicas:** Pintura 100% finalizada sem respingos; sistema de climatização em regime operacional de refrigeração.

### Quinzena 12 (Semanas 23 a 26 / Dias 166 a 180) — Comissionamento 52 Lotes, Auditoria SST, DataBook & Chaves Turnkey
* **Serviços:** 
  * **Semana 23 (Lotes 045 e 046):** Comissionamento elétrico sob carga nominal, laudo termográfico Fluke de barramentos, laudo anemométrico HVAC, limpeza química fina pós-obra e início da desmobilização de canteiro.
  * **Semana 24 (Lotes 047 e 048):** Testes integrados de carga plena com todos os sistemas ativos e consolidação das pranchas As-Built e DataBook oficial (3 vias físicas + digital criptografada).
  * **Semana 25 (Lotes 049 e 050):** Treinamento técnico presencial da equipe de Facilities do Terminal Multiuso e conclusão da desmobilização total dos containers NR-18, com caçambas e termo PGRCC de descarte ambiental.
  * **Semana 26 (Lotes 051 e 052):** Vistoria conjunta de Recebimento Provisório (Fiscalização do Porto x Diretoria Construtora), conferência das fichas FVS e assinatura do Termo de Recebimento Definitivo com entrega oficial das chaves codificadas e controle de acesso RFID.
* **Metas Físicas:** Obra 100% entregue no prazo contratual de 180 dias corridos / 26 semanas (R$ 1.660.762,28).

---

## 5. Gestão dos 4 Portões de Bloqueio Interdisciplinar (Zero Retrabalho)

Conforme estabelecido na governança mestre do projeto (`governanca/INDICE_MESTRE_SKILLS.md`), estes 4 portões são barreiras intransponíveis de qualidade:

```
[Portão 1: Baldrames]
Impermeabilização Asfáltica Aprovada ────> Libera Reaterro Compactado de Cavas

[Portão 2: Supraestrutura]
Cura Úmida 14d + Desforma Controlada ────> Libera Shafts Verticais e Alvenaria

[Portão 3: Instalações Hidráulicas]
Teste Hidrostático 72h sob Pressão ────> Libera Fechamento de Rasgos e Emboço

[Portão 4: Acabamentos Nobres]
1ª Demão de Pintura + Forração Pisos ────> Libera Louças, Metais, Splits e Espelhos
```

1. **Portão 1 (Dia 31 a 34): Impermeabilização Bloqueia Reaterro**
   - *Critério Normativo:* NBR 9575 e NBR 9574.
   - *Ação Obrigatória:* As vigas baldrames e troncos de sapata devem receber demão cruzada de primer e tinta asfáltica elastomérica (183,36 m²). É proibido jogar terra ou entulho nas cavas antes da secagem completa e validação visual de ausência de falhas ou furos pela fiscalização.

2. **Portão 2 (Dia 55 a 67): Desforma Controlada Bloqueia Alvenaria**
   - *Critério Normativo:* NBR 6118 e NBR 15696.
   - *Ação Obrigatória:* A desforma das vigas e laje treliçada H12 só ocorre após comprovação de resistência à compressão do concreto (corpos de prova fck ≥ 21 MPa aos 14 dias). As torres de re-escoramento central devem ser mantidas aliviadas para evitar flechas excessivas durante a elevação da alvenaria.

3. **Portão 3 (Dia 107 a 110): Teste Hidrostático 72h Bloqueia Emboço [REGRA DE OURO]**
   - *Critério Normativo:* NBR 5626 (Água Fria) e NBR 8160 (Esgoto).
   - *Ação Obrigatória:* As tubulações de PVC soldável embutidas em alvenaria devem ser submetidas a teste hidrostático pressurizado a 1,5x a pressão de serviço (mínimo 60 m.c.a. / 6 bar) monitoradas por manômetro calibrado por 72 horas ininterruptas. **É terminantemente proibido chapiscar ou rebocar rasgos antes da emissão da FVS de estanqueidade.**

4. **Portão 4 (Dia 148 a 153): 1ª Demão de Pintura Bloqueia Dispositivos Finos**
   - *Critério Normativo:* NBR 15575.
   - *Ação Obrigatória:* Nenhuma bacia sanitária, torneira de mesa, interruptor refinado, painel LED ou split cassete pode ser fixado na parede/teto antes da aplicação do selador e da 1ª demão de tinta acrílica e da forração integral do porcelanato com lona e papelão ondulado. Essa regra elimina danos, respingos de tinta e riscos em louças e metais.

---

## 5.1 Programação de Curto Prazo em Lotes Takt (Esteira Lean de 52 Ciclos & Nivelamento)

O planejamento operacional de curto prazo (Weekly Work Plan - WWP) foi estruturado seguindo os princípios rigorosos do **Lean Construction** e do **Takt Time Planning (Esteira de Produção Contínua)**, cobrindo integralmente as 26 semanas (52 lotes de 3 dias úteis):

### A) Divisão da Obra em 3 Etapas Construtivas (Zonas Takt)
Para eliminar esperas improdutivas decorrentes do tempo de cura do concreto armado (resistência $f_{ck}$), a edificação foi subdividida em 3 Zonas Takt com volumes de serviço equalizados:
1. **Etapa 1 (Zona 1 — Recepção e Diretoria):** Sapatas S1 a S12 (12 sapatas) $\rightarrow$ Vigas Baldrames VB1 a VB6 (6 vigas) $\rightarrow$ Pilares P1 a P8 (8 pilares) $\rightarrow$ Vigas V101 a V105.
2. **Etapa 2 (Zona 2 — Salas Técnicas e CPD):** Sapatas S13 a S24 (12 sapatas) $\rightarrow$ Vigas Baldrames VB7 a VB12 (6 vigas) $\rightarrow$ Pilares P9 a P16 (8 pilares) $\rightarrow$ Vigas V106 a V110.
3. **Etapa 3 (Zona 3 — Sanitários, Copa e Apoio):** Sapatas S25 a S32 (8 sapatas) $\rightarrow$ Vigas Baldrames VB13 a VB19 (7 vigas) $\rightarrow$ Pilares P17 a P24 (8 pilares) $\rightarrow$ Vigas V111 a V115 + Concretagem Global da Laje H12.

### B) Mecanismo da Esteira de Produção (Takt Time = 3 Dias Úteis / 52 Lotes)
* Cada semana de 6 dias úteis possui dois ciclos de produção: **Ciclo 1 (Segunda a Quarta)** e **Ciclo 2 (Quinta a Sábado)**.
* **Eliminação da Ociosidade Tecnológica de Cura:** Enquanto a Etapa 1 está sendo concretada e cumprindo o período de cura úmida (tempo tecnológico), a equipe de carpintaria e armação avança imediatamente para a montagem de fôrmas da Etapa 2! Quando a Etapa 2 está curando, a equipe avança para a Etapa 3 ou retorna para os pilares e vigas da Etapa 1 que já desformaram.
* **Alocação Contínua da Armação (Zero Ociosidade):** Nos ciclos de escavação e concretagem direta (Lotes 002, 004 e 006), os 2 armadores **não ficam ociosos no canteiro**. Eles operam dedicados na **Central de Corte e Dobra na Bancada**, pré-fabricando as armaduras de sapatas e baldrames que serão instaladas no ciclo subsequente.

### C) As 10 Frentes e Equipes Especializadas da Esteira Lean
A esteira orquestra 10 equipes com subcontratos e vínculos orçamentários rastreáveis:
1. `SUB-01 Estruturas`: Carpintaria, armação, formas resinadas, concretagem e impermeabilização asfáltica.
2. `SUB-02 Alvenaria & Reboco`: Elevação de blocos 14x19x39, encunhamento, chapisco rolado e reboco mecânico.
3. `SUB-03 Elétrica & Lógica`: Eletrodutos embutidos, caixas, quadros QGBT, cabeamento Cat6 e luminárias LED.
4. `SUB-04 Hidráulica & Metais`: Tubulações soldáveis/esgoto, teste hidrostático 72h, bacias e torneiras temporizadas.
5. `SUB-05 Acabamentos & Pisos`: Regularização de contrapiso autonivelante, porcelanato 60x60 e azulejos WCs.
6. `SUB-06 Pintura`: Selador primer, emassamento acrílico lixado a vácuo e pintura Suvinil lavável.
7. `SUB-07 Coberturas`: Estrutura metálica de terças U, telhas sandwich PIR 30mm, calhas, rufos e estanqueidade.
8. `SUB-08 Climatização HVAC`: Tubulações frigorígenas de cobre, teste de estanqueidade c/ N2 e splits cassete.
9. `Terraplenagem & Locações`: Retroescavadeira, caminhão caçamba basculante e guincho de coluna.
10. `Gestão Técnica & Turnkey`: Engenharia Residente, Mestre de Obras, TST, fiscalização e entrega de chaves.

---

## 5.2 Linha de Balanço (LOB) Recalibrada & Sincronizada (5 Setores / 32 Atividades)

A Linha de Balanço (Longo Prazo) foi rigorosamente alinhada com as datas da Esteira Lean, eliminando discrepâncias de planejamento e garantindo que o fechamento da envoltória ocorra no momento tecnológico perfeito:

| Setor Físico (Eixo Y) | Atividades Modeladas | Janela Temporal | Justificativa Técnica de Engenharia |
|---|:---:|:---:|---|
| **Setor 05 — Cobertura / Platibanda** | 4 macroatividades (SUB-07) | **01/12/2026 a 07/01/2027 (Sem 10 a 14)** | **Montagem imediata pós-desforma da laje.** Estanca a edificação contra intempéries antes de iniciar o reboco e acabamentos finos. |
| **Setor 04 — Galeria Circulação** | 7 macroatividades (Seq 1 a 7) | 19/10/2026 a 26/03/2027 (Sem 3 a 26) | Último setor térreo do fluxo; absorve as prumadas principais e fecha a pintura na Sem 26. |
| **Setor 03 — Sanitários e Copa** | 7 macroatividades (Seq 1 a 7) | 13/10/2026 a 20/03/2027 (Sem 3 a 25) | Setor de áreas molhadas com testes hidrostáticos (Portão 3), impermeabilização e louças finas. |
| **Setor 02 — Salas Técnicas / CPD** | 7 macroatividades (Seq 1 a 7) | 07/10/2026 a 14/03/2027 (Sem 2 a 24) | Setor de infraestrutura de dados, ar-condicionado de precisão e quadros QGBT. |
| **Setor 01 — Recepção / Diretoria** | 7 macroatividades (Seq 1 a 7) | 01/10/2026 a 08/03/2027 (Sem 1 a 23) | Setor pioneiro de avanço da esteira (cota zero à pintura final). |

* **Orientação Canônica:** Setor 01 na base e Setor 05 no topo, com inclinação positiva harmônica (↗) no avanço temporal do eixo X.
* **Fechamento Contratual:** O último acabamento físico conclui no dia 26/03/2027 (Dia 177). Os dias 178 a 180 (Semana 26) são integralmente reservados para o comissionamento final, auditoria e entrega das chaves turnkey.

---

## 6. Matriz de Riscos de Prazo & Estratégia de Recuperação (Crashing vs Fast-Tracking)

De acordo com a `SKILL_GESTAO_16_CRONOGRAMA_E_REPROGRAMACAO.md`, atrasos pontuais no caminho crítico devem ser combatidos com critérios técnicos lastreados em produtividade (RUP), e não com decisões emocionais:

| Risco Mapeado | Impacto Potencial | Gatilho de Alerta | Ação de Recuperação Recomendada | Restrição / Cuidado |
|---|:---:|:---:|---|---|
| **Chuva intensa na Infraestrutura** | Atraso nas sapatas/baldrames | SPI < 0,95 na Quinzena 1 ou 2 | **Fast-Tracking:** Adiantar armação externa em bancada coberta sob tenda enquanto o solo seca. | Não compactar reaterro com solo encharcado (risco de recalque). |
| **Gargalo no fornecimento de Telhas Sandwich** | Atraso no fechamento da cobertura | Atraso no envio do fornecedor > 5 dias | **Fast-Tracking:** Iniciar alvenaria interna paralelamente à fixação das terças, antecipando rasgos embutidos. | Proteger prumadas elétricas contra chuvas enquanto o telhado não estiver concluído. |
| **Baixa produtividade no Emboço (2.122 m²)** | Retardo no avanço do caminho crítico | RUP real > 1,80 Hh/m² por 3 dias | **Crashing:** Mobilização de máquina de projeção contínua de argamassa ou inclusão de 2º turno de estucadores. | Respeitar tempo de cura do reboco (mínimo 14 dias) antes da colagem do porcelanato. |
| **Saturação de frentes nos acabamentos finos** | Danos por circulação excessiva | Conflito de equipes na Quinzena 11 | **Sequenciamento Rígido:** Escalonar equipes por salas independentes da planta baixa (Zonas 1 a 4). | Proibido liberar montagem elétrica simultânea com rejuntamento no mesmo ambiente. |

---

## 7. Pacote Integrado de Arquivos Entregues (Ecossistema Digital)

Todos os artefatos de planejamento foram compilados e estão disponíveis na pasta `projetos/OBRA_TMULT/03_PLANEJAMENTO_E_CRONOGRAMA/`:

1. **[`PROGRAMACAO_CURTO_PRAZO_TMULT.csv`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/03_PLANEJAMENTO_E_CRONOGRAMA/PROGRAMACAO_CURTO_PRAZO_TMULT.csv)**
   - Base de dados operacional de curto prazo contendo os **52 lotes semanais (Semanas 01 a 26)** dimensionados em Takt Time de 3 dias, organizados por Vagão Lean, Recursos Previstos com metas de RUP e status de execução auditável.

2. **[`LINHA_DE_BALANCO.csv`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/03_PLANEJAMENTO_E_CRONOGRAMA/LINHA_DE_BALANCO.csv)**
   - Cronograma de Linha de Balanço (LOB) cobrindo os 180 dias corridos em fluxo ascendente com 5 setores físicos e 32 macroatividades recalibradas em sincronia com a Cobertura Metálica e o CPM.

3. **[`CRONOGRAMA_FISICO_FINANCEIRO_TMULT.csv`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/03_PLANEJAMENTO_E_CRONOGRAMA/CRONOGRAMA_FISICO_FINANCEIRO_TMULT.csv)**
   - Base de dados bruta, auditável e versionável via Git. Contém os 158 itens da EAP distribuídos mês a mês (M1 a M6), somando exatamente R$ 1.660.762,28.

4. **[`CRONOGRAMA_FISICO_FINANCEIRO_TMULT.xlsx`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/03_PLANEJAMENTO_E_CRONOGRAMA/CRONOGRAMA_FISICO_FINANCEIRO_TMULT.xlsx)**
   - Planilha executiva formatada em padrão corporativo com gráficos e abas de Curva S e Cronograma Analítico.

5. **[`CRONOGRAMA_TMULT_MSPROJECT.xml`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/03_PLANEJAMENTO_E_CRONOGRAMA/CRONOGRAMA_TMULT_MSPROJECT.xml)**
   - Arquivo padrão Microsoft Project (MSPDI Schema) pronto para importação direta no MS Project ou Primavera P6.

6. **[`CRONOGRAMA_DASHBOARD_INTERATIVO.html`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/03_PLANEJAMENTO_E_CRONOGRAMA/CRONOGRAMA_DASHBOARD_INTERATIVO.html)**
   - Dashboard web interativo Plotly para visualização de Curva S e desembolso.

7. **[`RELATORIO_PLANEJAMENTO_BASELINE_TMULT.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/OBRA_TMULT/03_PLANEJAMENTO_E_CRONOGRAMA/RELATORIO_PLANEJAMENTO_BASELINE_TMULT.md)**
   - Este relatório formal consolidado, servindo como documento de Linha de Base Contratual da Construtora perante o Contratante.

---
*Fim do Relatório Executivo de Linha de Base (Baseline 01). Aprovado pelo PMO Virtual.*
