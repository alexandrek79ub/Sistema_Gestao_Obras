# 📐 SKILL MASTER: Sistema de Quantificação de Engenharia

Este é o **arquivo núcleo** do sistema de quantificação. Ele define os protocolos universais que se aplicam a **todas as disciplinas** (Fundações, Estrutura, Arquitetura, Elétrica, Hidráulica).

> ✅ **Normas de Referência:** NBR 12721, NBR 6118, NBR 14931, TCPO 14ª Edição, SINAPI (IBGE/CEF).
> Toda quantificação deve ser **rastreável, auditável e tecnicamente defensável**.

## 📂 Módulos Disponíveis

| Arquivo | Disciplina | Conteúdo |
|---|---|---|
| [SKILL_QUANT_01_FUNDACOES.md](file:///c:/Users/Alexandre/Workspace/A11_FREE%20LANCER%20ENGENHARIA/skills/quantitativo/SKILL_QUANT_01_FUNDACOES.md) | Fundações | Sapatas, blocos, estacas, radier, baldrame, concreto C30 |
| [SKILL_QUANT_02_ESTRUTURA.md](file:///c:/Users/Alexandre/Workspace/A11_FREE%20LANCER%20ENGENHARIA/skills/quantitativo/SKILL_QUANT_02_ESTRUTURA.md) | Estrutura | Pilares, vigas, lajes, escadas, fôrmas, armadura CA-50/CA-60 |
| [SKILL_QUANT_03_ARQUITETURA.md](file:///c:/Users/Alexandre/Workspace/A11_FREE%20LANCER%20ENGENHARIA/skills/quantitativo/SKILL_QUANT_03_ARQUITETURA.md) | Arquitetura & Acabamentos | Alvenaria, revestimentos, pisos, teto, cobertura, drywall, impermeabilização |
| [SKILL_QUANT_04_ELETRICA.md](file:///c:/Users/Alexandre/Workspace/A11_FREE%20LANCER%20ENGENHARIA/skills/quantitativo/SKILL_QUANT_04_ELETRICA.md) | Instalações Elétricas | *Placeholder — em desenvolvimento* |
| [SKILL_QUANT_05_HIDRAULICA.md](file:///c:/Users/Alexandre/Workspace/A11_FREE%20LANCER%20ENGENHARIA/skills/quantitativo/SKILL_QUANT_05_HIDRAULICA.md) | Instalações Hidráulicas | *Placeholder — em desenvolvimento* |

> **Protocolo de uso:** Sempre carregar este MASTER + o módulo da disciplina necessária. Para quantificação completa de obra, carregar MASTER + todos os módulos.

---

## 🧭 1. Hierarquia Obrigatória de Rastreabilidade

Toda quantidade gerada deve estar vinculada à seguinte cadeia hierárquica, **sem exceções**:

```
OBRA
 └── PAVIMENTO  (ex: Subsolo, Térreo, Mezzanino, Tipo 01..N, Cobertura, Ático)
      └── UNIDADE / SETOR  (ex: Ap 101, Área Comum, Loja 01, Bloco A)
           └── AMBIENTE  (ex: Sala de Estar, Banheiro Social, Varanda)
                └── DISCIPLINA  (Fundações | Estrutura | Arquitetura | Elétrica | Hidráulica)
                     └── SERVIÇO / ELEMENTO  (ex: Emboço de Paredes, Pilar P1, Sapata F3)
                          └── MEMÓRIA DE CÁLCULO  ← Transcrição auditável obrigatória
```

### Código de Identificação de Ambiente (CIA)
Cada ambiente recebe um código único no formato: `[Pav]-[Unidade]-[Abrev]`

| Exemplo | Significado |
|---|---|
| `T-101-SAL` | Térreo, Ap 101, Sala de Estar |
| `T-101-BAN` | Térreo, Ap 101, Banheiro Social |
| `T-101-COZ` | Térreo, Ap 101, Cozinha |
| `TP-201-DOR` | Tipo, Ap 201, Dormitório |
| `COB-AC-PIS` | Cobertura, Área Comum, Piscina |
| `SUB-GAR-PI1` | Subsolo, Garagem, Pilar 1 |
| `FUN-GER-S01` | Fundação, Geral, Sapata 01 |

---

## 📋 2. Modelos Universais de Memória de Cálculo

O Agente DEVE usar um destes modelos para **cada serviço, em cada ambiente**. Não omitir etapas.

### Modelo A — Revestimento de Parede / Teto:
```
╔══════════════════════════════════════════════════════════════════╗
║           MEMÓRIA DE CÁLCULO — [NOME DO SERVIÇO]                ║
╠══════════════════════════════════════════════════════════════════╣
║  OBRA:         [Nome da Obra]                                    ║
║  PAVIMENTO:    [Térreo / Tipo / Cobertura / etc.]                ║
║  UNIDADE:      [Ap 101 / Área Comum / Bloco A / etc.]            ║
║  AMBIENTE:     [Nome do Ambiente]       CIA: [T-101-COZ]         ║
║  DISCIPLINA:   Arquitetura                                       ║
║  SERVIÇO:      [Ex: Emboço de Paredes — espessura 20mm]          ║
╠══════════════════════════════════════════════════════════════════╣
║  DIMENSÕES DO AMBIENTE:                                          ║
║    Comprimento (A):  X,XX m                                      ║
║    Largura (B):      X,XX m                                      ║
║    Pé-direito (H):   X,XX m                                      ║
║                                                                  ║
║  FÓRMULA:                                                        ║
║    A_bruta = (2A + 2B) × H                                       ║
║    A_bruta = (2 × X,XX + 2 × X,XX) × X,XX                       ║
║    A_bruta = (X,XX + X,XX) × X,XX = XX,XX m²                    ║
║                                                                  ║
║  DESCONTO DE VÃOS (NBR 12721):                                   ║
║    [Tag]  [Tipo]  [L×H] = [A_vão] m²  → [Critério] → [Desconto] ║
║    Ex: PA-01  Porta  0,90×2,10 = 1,89 m² < 2,00 → NÃO desconta  ║
║    Ex: JA-02  Janela 1,50×1,80 = 2,70 m² → desconta (2,70-2,00) = 0,70 m² ║
║    Σ Descontos = X,XX m²                                         ║
║                                                                  ║
║  ÁREA LÍQUIDA = XX,XX − X,XX = XX,XX m²                         ║
║  TAXA DE PERDA (X%) = XX,XX × 1,0X = XX,XX m²                   ║
║                                                                  ║
║  ✅ RESULTADO FINAL: XX,XX m²                                    ║
╚══════════════════════════════════════════════════════════════════╝
```

### Modelo B — Revestimento de Piso:
```
╔══════════════════════════════════════════════════════════════════╗
║           MEMÓRIA DE CÁLCULO — REVESTIMENTO DE PISO             ║
╠══════════════════════════════════════════════════════════════════╣
║  OBRA/PAV/UNIDADE/AMBIENTE/CIA: [conforme hierarquia]           ║
║  SERVIÇO:  Piso [Tipo] [Formato] — assentamento [alinhado/diag] ║
╠══════════════════════════════════════════════════════════════════╣
║  A_piso = Comp × Larg = X,XX × X,XX = XX,XX m²                  ║
║  Descontos: pilares embutidos, ralos = X,XX m²                  ║
║  ÁREA LÍQUIDA = XX,XX m²                                        ║
║  TAXA DE PERDA (10%/15%) = XX,XX × 1,1X = XX,XX m²             ║
║                                                                  ║
║  INSUMOS (TCPO §9.10–§9.14 do módulo Arquitetura):             ║
║    Argamassa colante AC-[I/II/III]: XX,XX m² × 5,0 = XX,XX kg  ║
║    Rejunte (junta Xmm): XX,XX m² × X,XX = XX,XX kg             ║
║    Espaçadores: XX,XX m² × 6 = XX unid                         ║
║                                                                  ║
║  ✅ RESULTADO FINAL: XX,XX m² de piso                           ║
╚══════════════════════════════════════════════════════════════════╝
```

### Modelo C — Elemento Estrutural (Concreto + Fôrma + Aço):
```
╔══════════════════════════════════════════════════════════════════╗
║        MEMÓRIA DE CÁLCULO — ELEMENTO ESTRUTURAL                 ║
╠══════════════════════════════════════════════════════════════════╣
║  OBRA:     [Nome]   PAV: [Térreo]   CIA: [SUB-GER-P01]          ║
║  ELEMENTO: [Pilar P1 / Viga V3 / Laje L2 / Sapata F1]           ║
║  DIMENSÕES: b = X,XX m | h = X,XX m | H/L = X,XX m              ║
║  RESISTÊNCIA: Fck = XX MPa  | TIPO AÇO: CA-50 / CA-60           ║
╠══════════════════════════════════════════════════════════════════╣
║  CONCRETO:                                                       ║
║    V = b × h × H = X,XX × X,XX × X,XX = X,XX m³                ║
╠══════════════════════════════════════════════════════════════════╣
║  FÔRMA:                                                          ║
║    A_forma = (2b + 2h) × H = XX,XX m²                           ║
╠══════════════════════════════════════════════════════════════════╣
║  ARMADURA (taxa estimada ou detalhamento):                       ║
║    Taxa: XXX kg/m³ → Peso = X,XX × XXX = XXX,XX kg              ║
║    Arame recozido (1,5%): X,XX kg                                ║
║                                                                  ║
║  ✅ CONCRETO: X,XX m³ | FÔRMA: XX,XX m² | AÇO: XXX,XX kg        ║
╚══════════════════════════════════════════════════════════════════╝
```

### Modelo D — Armadura Detalhada por Bitola:
```
╔══════════════════════════════════════════════════════════════════╗
║        MEMÓRIA DE CÁLCULO — ARMADURA DETALHADA                  ║
╠══════════════════════════════════════════════════════════════════╣
║  ELEMENTO: [Viga V-01]   Pav: [Térreo]   CIA: [T-AC-V01]        ║
╠══════════════════════════════════════════════════════════════════╣
║  ARMADURA LONGITUDINAL:                                          ║
║    Ø 12,5mm (CA-50): 4 barras × (3,80m + 2×0,50m) = 4 × 4,80m  ║
║      → 19,20m × 0,963 kg/m = 18,49 kg                           ║
║    Ø 10,0mm (CA-50): 2 barras × (3,80m + 2×0,40m) = 2 × 4,60m  ║
║      → 9,20m × 0,617 kg/m = 5,68 kg                             ║
║                                                                  ║
║  ARMADURA TRANSVERSAL (Estribos):                                ║
║    Ø 6,3mm (CA-60): 20 estribos × 0,90m = 18,00m                ║
║      → 18,00m × 0,245 kg/m = 4,41 kg                            ║
║                                                                  ║
║  SUBTOTAL = 18,49 + 5,68 + 4,41 = 28,58 kg                      ║
║  TAXA DE PERDA (5%) = 28,58 × 1,05 = 30,01 kg                   ║
║  ARAME RECOZIDO (1,5%) = 30,01 × 0,015 = 0,45 kg                ║
║                                                                  ║
║  ✅ AÇO TOTAL: 30,01 kg + 0,45 kg arame = 30,46 kg              ║
╚══════════════════════════════════════════════════════════════════╝
```

### Modelo E — Impermeabilização:
```
╔══════════════════════════════════════════════════════════════════╗
║           MEMÓRIA DE CÁLCULO — IMPERMEABILIZAÇÃO                ║
╠══════════════════════════════════════════════════════════════════╣
║  OBRA/PAV/UNIDADE/CIA: [conforme hierarquia]                    ║
║  SERVIÇO: Impermeabilização — [Tipo: Manta Asfáltica / Polimérica] ║
╠══════════════════════════════════════════════════════════════════╣
║  A_piso = Comp × Larg = X,XX × X,XX = XX,XX m²                  ║
║  A_arremate (30cm) = Perímetro × 0,30 = XX,XX m²               ║
║  A_box (1,80m, se houver) = Perím_box × 1,80 = X,XX m²          ║
║  ÁREA TOTAL = XX,XX + X,XX + X,XX = XX,XX m²                    ║
║  TAXA DE PERDA (15%) = XX,XX × 1,15 = XX,XX m²                  ║
║                                                                  ║
║  INSUMOS (TCPO §9.14 do módulo Arquitetura):                    ║
║    Manta 3mm: XX,XX × 1,20 = XX,XX m²                           ║
║    Primer: XX,XX × 0,40 = XX,XX L                               ║
║                                                                  ║
║  ✅ RESULTADO FINAL: XX,XX m² impermeabilizados                 ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 📊 3. Estrutura dos Relatórios Finais

### 3.1 Tabela de Resumo — Arquitetura & Acabamentos

| Código | Serviço | Und | Qtd Líq. | % Perda | Qtd Final | Preço Unit. (R$) | Custo Total (R$) | Pavimento |
|---|---|---|---|---|---|---|---|---|
| ARQ-01 | Chapisco de Paredes | m² | — | 5% | — | — | — | — |
| ARQ-02 | Emboço de Paredes | m² | — | 5% | — | — | — | — |
| ARQ-03 | Gesso Liso | m² | — | 5% | — | — | — | — |
| ARQ-04 | Massa Corrida PVA | m² | — | — | — | — | — | — |
| ARQ-05 | Pintura Látex Acrílica | m² | — | 10% | — | — | — | — |
| ARQ-06 | Piso Cerâmico/Porcelanato | m² | — | 10–15% | — | — | — | — |
| ARQ-07 | Argamassa Colante AC-II | kg | — | — | — | — | — | — |
| ARQ-08 | Rejunte | kg | — | — | — | — | — | — |
| ARQ-09 | Impermeabilização | m² | — | 15% | — | — | — | — |
| | | | | | **SUBTOTAL** | | **R$ —** | |
| | | | | | **TOTAL GERAL** | | **R$ —** | |

> Preços preenchidos pelo Engenheiro com base no SINAPI vigente ou cotações locais. O agente NÃO estima preços — apenas quantidades.

### 3.2 Tabela de Resumo — Estrutura

| Elemento | Qtd | Und | Concreto (m³) | Fôrma (m²) | Aço (kg) | Fck | Pavimento | Custo (R$) |
|---|---|---|---|---|---|---|---|---|
| Pilar P1 | — | unid | — | — | — | C25 | — | — |
| Viga V1 | — | unid | — | — | — | C25 | — | — |
| Laje L1 | — | unid | — | — | — | C25 | — | — |
| Sapata F1 | — | unid | — | — | — | C30 | Fundação | — |
| Radier | — | m² | — | — | — | C30 | Fundação | — |
| | | | **TOTAL** | **TOTAL** | **TOTAL** | | | **R$ —** |

### 3.3 Tabela de Insumos para Compra

| Insumo | Und | Qtd Calculada | Coef. TCPO | Qtd para Compra | Preço Unit. (R$) | Custo (R$) |
|---|---|---|---|---|---|---|
| Blocos cerâmicos 9×19×19 | unid | — | 25/m² | Σ m² × 25 × 1,05 ↑ | — | — |
| Cimento CP II (sc 50kg) | sc | — | §9 ARQ | Σ kg / 50 ↑ | — | — |
| Areia média | m³ | — | §9 ARQ | Σ m³ | — | — |
| Cal hidratada (sc 20kg) | sc | — | §9.4 ARQ | Σ kg / 20 ↑ | — | — |
| Argamassa colante AC-II (sc 20kg) | sc | — | 5,0 kg/m² | Σ kg / 20 ↑ | — | — |
| Rejunte (sc 5kg) | sc | — | §9.11 ARQ | Σ kg / 5 ↑ | — | — |
| Massa corrida PVA (lt 25kg) | lata | — | 0,90 kg/m² | Σ kg / 25 ↑ | — | — |
| Tinta látex acrílica (lt 18L) | lata | — | 0,26 L/m² | Σ L / 18 ↑ | — | — |
| Selador acrílico (lt 18L) | lata | — | 0,10 L/m² | Σ L / 18 ↑ | — | — |
| Concreto usinado | m³ | — | — | Σ V_concreto | — | — |
| Aço CA-60 Ø 6,3mm | kg | — | §3.3 EST | Σ kg × 1,03 | — | — |
| Aço CA-50 Ø 8,0mm | kg | — | §3.3 EST | Σ kg × 1,05 | — | — |
| Aço CA-50 Ø 10,0mm | kg | — | §3.3 EST | Σ kg × 1,05 | — | — |
| Aço CA-50 Ø 12,5mm | kg | — | §3.3 EST | Σ kg × 1,05 | — | — |
| Aço CA-50 Ø 16,0mm | kg | — | §3.3 EST | Σ kg × 1,05 | — | — |
| Aço CA-50 Ø 20,0mm | kg | — | §3.3 EST | Σ kg × 1,05 | — | — |
| Arame recozido BWG 18 | kg | — | 1,5% aço | Σ aço × 0,015 | — | — |
| Manta asfáltica 3mm | m² | — | 1,20 m²/m² | Σ m² × 1,20 | — | — |
| Primer asfáltico | L | — | 0,40 L/m² | Σ m² × 0,40 | — | — |
| | | | | **TOTAL GERAL** | | **R$ —** |

> O símbolo **↑** indica arredondamento para cima (compra de unidades inteiras).

---

## 🌳 4. Árvore de Decisão — Qual Módulo Carregar

| Pedido do Usuário | Módulos a Carregar | Seção Aplicável |
|---|---|---|
| "Quantifique revestimento de paredes / piso / teto" | MASTER + ARQ | §1 (parede), §2 (piso), §3 (teto) ARQ |
| "Quanto de concreto no pilar P1 / viga / laje?" | MASTER + EST | §1 a §3 EST |
| "Calcule o aço da viga V-03" | MASTER + EST | §3 EST |
| "Quantifique as fundações (sapatas / radier / estacas)" | MASTER + FUN | §1 a §3 FUN |
| "Quantificação completa de um apartamento" | MASTER + ARQ + EST | Todos §§ |
| "Quantificação completa da obra" | MASTER + FUN + EST + ARQ | Todos §§ |
| "Preciso quantificar a impermeabilização" | MASTER + ARQ | §7.1 + §9.14 ARQ |
| "Parede de drywall / forro" | MASTER + ARQ | §8 ARQ |
| "Quantifique o pavimento tipo multiplicado por N andares" | MASTER + EST | §3.4 EST |
| "Preciso conferir/revisar um quantitativo" | MASTER + módulo da disciplina | §2 MASTER + módulo pertinente |
| "Tenho uma reforma — demolir e reconstruir" | MASTER + ARQ ± EST ± FUN | Etapas separadas |
| "Leia este PDF e quantifique" | MASTER + todos os módulos pertinentes | Skill completa |

---

## ⚠️ 5. Regras de Ouro — O Agente NUNCA deve:

1. **Gerar quantidades sem transcrever a memória de cálculo** — fórmula, valores e critério de desconto de vão obrigatórios.
2. **Misturar serviços de disciplinas diferentes na mesma memória** — Estrutura e Arquitetura são sempre separadas.
3. **Omitir o Código CIA** em qualquer resultado.
4. **Assumir dimensões sem confirmação** — perguntar explicitamente antes de calcular.
5. **Usar taxas de perda sem registrar qual foi aplicada** — a taxa é parte da memória.
6. **Gerar totais globais sem os subtotais por ambiente** — totais são soma auditável dos ambientes.
7. **Arredondar para baixo** — quantitativos arredondam para CIMA na compra.
8. **Misturar área de teto com área de parede** — serviços separados, memórias separadas.
9. **Somar paredes irregulares como 2×C+2×L** — medir cada trecho individualmente (P1, P2...).
10. **Apresentar resultado sem unidade de medida** — m², m³, kg, m, unid são obrigatórios.
11. **Estimar preços** — o agente quantifica, o engenheiro precifica com SINAPI/cotações.

---

## 📏 6. Regras de Precisão e Arredondamento

| Grandeza | Casas Decimais | Regra de Arredondamento Final |
|---|---|---|
| Dimensões lineares (m) | 2 decimais | Usar valor exato do projeto |
| Áreas (m²) | 2 decimais | Arredondar para cima na compra |
| Volumes (m³) | 2 decimais | Arredondar para cima na compra |
| Peso de aço (kg) | 2 decimais | Arredondar para cima na compra |
| Quantidade de blocos (unid) | 0 decimais | Arredondar para cima SEMPRE |
| Sacos de cimento / cal (unid) | 0 decimais | Arredondar para cima SEMPRE |
| Latas de tinta / massa (unid) | 0 decimais | Arredondar para cima SEMPRE |

### Conversão Obrigatória para Unidade Comercial de Compra (UCC)
O quantitativo de engenharia puro (físico/matemático) quase nunca bate com a embalagem do fornecedor. Para a Tabela de Insumos final, o Agente DEVE converter as quantidades para a Unidade Comercial (UCC):
- **Aço (Vergalhão):** Vendido em barras de **12 metros**. Se a obra precisa de 25 metros, deve-se comprar 3 barras (36m).
- **Tubos de PVC (Hidráulica):** Vendidos em barras de **3 metros** ou **6 metros** (dependendo da bitola). Se o projeto pede 14 metros de tubo esgoto 100mm, comprar 3 barras de 6m (18m).
- **Cimento / Argamassa:** Vendidos em sacos de **50kg** (cimento) ou **20kg** (argamassa). Dividir o total de kg pela capacidade do saco e arredondar o número de sacos para CIMA.
- **Pisos / Revestimentos:** Vendidos em **Caixas fechadas**. O Engenheiro deve fornecer o m²/caixa do modelo escolhido para que a divisão resulte em caixas inteiras.

> Resultados intermediários (por ambiente) mantêm 2 casas decimais. A conversão para UCC e o arredondamento para cima ocorrem somente no TOTAL FINAL de compra.

---

## ✅ 7. Checklist Universal de Entrega

Antes de encerrar qualquer levantamento:

- [ ] Hierarquia completa preenchida (Obra > Pavimento > Unidade > Ambiente > Disciplina > Serviço)
- [ ] Código CIA atribuído a cada ambiente
- [ ] Quadro de Esquadrias gerado (se houver serviços de revestimento)
- [ ] Memória de cálculo transcrita para cada serviço em cada ambiente
- [ ] Revestimento de PAREDE separado de TETO
- [ ] Desconto de vãos aplicado (NBR 12721 — tabela de 3 faixas)
- [ ] Taxas de perda explicitadas na memória
- [ ] Pavimento Tipo com multiplicador aplicado (se houver)
- [ ] Tabela Resumo por Disciplina gerada com subtotais
- [ ] Tabela de Insumos para Compra gerada
- [ ] Totais auditáveis (soma dos subtotais por ambiente)
- [ ] Unidades de medida em todos os resultados
- [ ] Precisão decimal: 2 casas para m², m³, kg

---

## 🔒 8. Nota de Responsabilidade

> ⚠️ **AVISO OBRIGATÓRIO:** Todo quantitativo gerado por esta Skill é uma **ferramenta de apoio à engenharia** e deve ser conferido pelo Engenheiro/Arquiteto responsável técnico antes de uso para compra, contratação ou propostas.
>
> O Agente de IA:
> - NÃO substitui o julgamento técnico do profissional habilitado (CREA/CAU)
> - NÃO assume responsabilidade por variações de campo ou mudanças de projeto
> - DEVE alertar quando uma taxa ou coeficiente estiver fora do padrão usual
> - DEVE recomendar conferência humana quando houver ambiguidade nos dados
>
> **O engenheiro responsável deve revisar toda memória de cálculo antes de assinar ART/RRT.**
