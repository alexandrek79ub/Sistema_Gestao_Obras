# 🏠 SKILL MÓDULO 03B: Pisos Especiais, Impermeabilização, Esquadrias, Louças e Bancadas

> **Parte de:** [`SKILL_QUANT_03_ARQUITETURA.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANT_03_ARQUITETURA.md) (arquivo índice)
> **Dependência:** Carregar sempre com [`SKILL_QUANTIFICACAO_MASTER.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANTIFICACAO_MASTER.md)
> **Normas:** NBR 12721, TCPO 14ª Edição
> **Ativar quando:** "impermeabilização", "esquadrias", "vidros", "fechaduras", "louças", "metais sanitários", "bancadas", "granito", "rodapés", "soleiras", "peitoris"

> 🛡️ **BLINDAGEM ANTI-ESTIMATIVA (INVIOLÁVEL):** Nenhuma dimensão sem respaldo em prancha. Falta de informação → `⚠️ [ITEM NÃO LEVANTADO - RFI]`.

---

## 📐 1. Impermeabilização

### 1.1 Área Molhada (Banheiro, Sacada, Varanda)

```
A_piso = Comp × Larg
A_arremate = Perímetro_interno × 0,30m
A_impermeab = A_piso + A_arremate
A_final = A_impermeab × 1,15  (15% perda)
```

### 1.2 Box de Banheiro

```
A_box_piso = Comp_box × Larg_box
A_box_paredes = Perímetro_box × 1,80m
A_impermeab_box = A_box_piso + A_box_paredes
```

### 1.3 Laje Exposta / Terraço / Reservatório

```
A_impermeab = A_laje + Perímetro × 0,30m (arremate)
A_final = A_impermeab × 1,15
```
> Reservatórios: todas as 6 faces internas (piso + 4 paredes + laje de fundo).

### 1.4 Coeficientes TCPO — Impermeabilização (§9.14)

| Tipo | Insumo | Consumo | Unidade |
|---|---|---|---|
| **Manta asfáltica 3mm** | Manta | 1,20 | m²/m² (sobreposição 10cm) |
| | Primer asfáltico | 0,40 | L/m² |
| **Argamassa polimérica (2 demãos)** | Argamassa polim. | 3,0 | kg/m² |
| | Tela de poliéster (reforço) | 1,10 | m²/m² |

### 1.5 Kit de Impermeabilização (Miudezas Obrigatórias)

| Item | Cálculo | UCC |
|---|---|---|
| Primer asfáltico (baldes 18L) | `A_manta × 0,40` | balde ↑ |
| Tela de poliéster/véu fibra vidro (rolos 50m²) | `A_impermeab × 1,10` | rolo ↑ |
| Fita asfáltica autoadesiva aluminizada (rolos 10m) | `Perim_ralos + juntas / 10` | rolo ↑ |
| Gás GLP P-13 para maçarico de manta | `A_manta / 50` | botijão ↑ |
| Geotêxtil separador Bidim (1,10 m²/m²) | `A_manta_horiz × 1,10` | m² |

---

## 📐 2. Esquadrias, Vidros, Fechaduras e Derivação de Vergas

### 2.1 Quadro Mestre de Tipologias Cadastrais

> ⚠️ O levantamento de esquadrias DEVE ser estruturado em duas etapas: Quadro Mestre + Tabela de Alocação por Ambiente.

| Código | Tipo | Descrição | L (m) | H (m) | A (m²) | Coef. Pintura |
|---|---|---|---|---|---|---|
| **JA01** | Janela Alumínio | Basculante 1F | 0,60 | 0,60 | 0,36 | 1,00 (1 face) |
| **JA02** | Janela Alumínio | Correr 2F | 1,20 | 1,20 | 1,44 | 2,00 (2 faces) |
| **PA01** | Porta Madeira | Lisa c/ batente + alizar | 0,80 | 2,10 | 1,68 | 2,00 (2 faces) |
| **GA01** | Gradil Alumínio | Peitoril sacada H=1,10m | 2,50 | 1,10 | 2,75 | 2,00 (2 faces) |

### 2.2 Derivação Automática de Verga, Contraverga e Área de Pintura

```
Qtd_Total = Qtd_por_tipo × Qtd_andares

A_pintura_esq = (Larg × Alt) × Coef_Pintura × Qtd_Total

Verga (topo do vão):       L_verga = (Larg + 2 × 0,20m) × Qtd_Total
Contraverga (base janela): L_contrv = (Larg + 2 × 0,20m) × Qtd_Janelas
```

### 2.3 Kit Esquadrias (Miudezas Obrigatórias)

> 🛑 **PROIBIÇÃO DE ORÇAMENTOS SINTÉTICOS** — quantificar todos os acessórios peça a peça.

| Item | Cálculo | UCC |
|---|---|---|
| Dobradiças aço inox 3½"×3" (3 por folha de abrir) | `N_folhas × 3 × 1,05` | unid |
| Fechaduras completas (máq + cilindro + maçaneta) | `N_portas_total` | unid |
| Batedores de porta de piso c/ amortecedor | `N_folhas_total` | unid |
| Espuma PU 750ml (1 tubo / 2,5 marcos) | `Ceil(N_portas / 2,5) × 1,05` | tubo |
| Parafusos + buchas S8 fixação batente (8/porta) | `N_portas × 8 × 1,05` | unid |
| Pregos s/ cabeça 12×12 para alizares (20/vão) | `N_portas × 20 × 1,05` | unid |
| Cola branca PVA D3 (fr. 500g — 1 a cada 8 portas) | `Ceil(N_portas / 8) × 1,05` | frasco |
| Selante PU40 calafetação caixilhos ext. (10m/tubo) | `Ceil(Perim_ext / 10) × 1,05` | tubo |

---

## 📐 3. Rodapés, Peitoris e Soleiras

```
Rodapé líquido (m) = Perímetro_interno − Σ Largura_portas − Σ Largura_nichos
Peitoril (m)       = Σ Largura_janelas
Soleira (m)        = Σ Largura_portas_externas
Baguete de box (m) = Largura_box (contenção de água)
```

---

## 📐 4. Louças, Metais e Acessórios Sanitários (Matriz por Ambiente × Pavimento)

> ⚠️ O levantamento DEVE ser em matriz de ambientes × repetição de pavimento.

### 4.1 Categorias

| Família | Itens | Unidade |
|---|---|---|
| **LOUÇAS** | Bacia c/ cx. acoplada, lavatório c/ coluna, cuba de embutir, tanque | un |
| **CUBAS INOX** | Cuba simples/dupla, tanque inox | un |
| **METAIS** | Torneira de lavatório, torneira pia, misturador, ducha higiênica, chuveiro | un |
| **ACABAMENTOS** | Acabamento reg. gaveta/pressão, sifões, válvulas de escoamento | un |

### 4.2 Fórmula de Multiplicação

```
Qtd_Total_k = Σ (Qtd_Unid_Cômodo × N_ambientes_por_andar × N_andares_repetidos)
```

### 4.3 Kit Louças/Metais (Miudezas Obrigatórias)

| Item | Cálculo | UCC |
|---|---|---|
| Engates flexíveis aço inox ½"×40cm | `N_bacias + N_torneiras_lav + N_cubas` | unid |
| Sifões universais PP/cromado | `N_cubas + N_lavatórios + N_tanques` | unid |
| Válvulas de escoamento | `= N_sifões` | unid |
| Anel de cera c/ guia (bacia) | `N_bacias_total` | unid |
| Parafusos B10/B12 latão/inox (bacias/lavatórios) | `(N_bacias + N_lavatórios) × par` | par |
| Fita veda rosca PTFE 18mm × 25m | `Ceil((N_torneiras + N_engates + N_reg) / 10)` | rolo |

---

## 📐 5. Bancadas, Tampos e Divisórias em Pedra

### 5.1 Mapeamento por Código de Especificação

| Código | Descrição | Material | Comp × Larg | A Unit (m²) |
|---|---|---|---|---|
| CÓD 1 | Bancada de banheiro c/ cuba | Granito Cinza Corumbá 2cm | 1,00m × 1,00m | 1,00 |
| CÓD 2 | Bancada de cozinha | Granito Preto S. Gabriel 2cm | 1,20m × 0,60m | 0,72 |
| CÓD 3 | Balcão passa-prato | Mármore Branco Social | 1,50m × 0,35m | 0,53 |
| CÓD 4 | Divisória sanitária | Granito Cinza 3cm | 1,60m × 0,80m | 1,28 |

### 5.2 Fórmula

```
A_total_local  = A_unit × Qtd_peças_no_local
A_total_COD_k = Σ (A_total_local para todas as ocorrências do CÓD k)
```

---

## 📐 6. Kit de Pisos — Miudezas de Assentamento

> 🛑 **Proibido omitir acessórios de assentamento.**

| Item | Cálculo | UCC |
|---|---|---|
| Cimentcola (sacos 20kg) | `A × consumo (5 ou 10 kg/m²)` | saco 20kg ↑ |
| Rejunte (sacos 5kg) | `A × consumo por §9.11` | saco 5kg ↑ |
| Espaçadores/cruzetas (sacos 100un) | `A_total × 6 / 100` | saco ↑ |
| Clips niveladores (sacos 100un — porcelanato ≥60×60) | `N_peças × 4 / 100` | saco ↑ |
| Cunhas niveladoras (30% dos clips) | `N_clips × 0,30 / 100` | saco ↑ |
| **Primer de contato acrílico** (substrato poroso / contrapiso absorvente antes da cimentcola) | `A × 0,15 L/m²` | lata 18L ↑ |
| **Argamassa de regularização / nivelamento local** (faixas mestre ou caimento forçado em pisos molhados) | conforme indicado em projeto | saco 20kg ↑ |
| Lã de róckwool / junta de dilatacão PE expandido 5mm (porçat./grês > 3m lineares) | `Perím_amb × 1,05` | rolo 10m ↑ |

> ⚠️ **Regra Primer:** Aplicar primer de contato sempre que o substrato (contrapiso ou concreto) for novo e poroso. Se o projeto não especificar, perguntar ao responsável antes de orçar ou omitir.

---

### 6.1 Checklist Anti-Omissão de Miudezas — Módulo 03B (🚨 OBRIGATÓRIO)

Antes de fechar a Tabela Consolidada de qualquer serviço coberto por este módulo:

**Impermeabilização (§1):**
- [ ] Primer asfáltico base solvente calculado e na tabela (0,40 L/m²)
- [ ] Tela de poliéster / véu de fibra de vidro calculado e na tabela
- [ ] Fita asfáltica autoadesiva aluminizada (juntas e arremates) calculada e na tabela
- [ ] Gás GLP P-13 para maçarico de manta (se manta asfáltica) calculado e na tabela

**Esquadrias (§2.3):**
- [ ] Dobradiças em aço inox (3 por folha) calculadas e na tabela
- [ ] Fechaduras completas (máq + cilindro + maçaneta) calculadas e na tabela
- [ ] Batedores de porta c/ amortecedor calculados e na tabela
- [ ] Espuma PU 750ml para marcos calculada e na tabela
- [ ] Parafusos + buchas S8 para batentes calculados e na tabela
- [ ] Pregos s/ cabeça para alizares calculados e na tabela
- [ ] Cola branca PVA D3 calculada e na tabela
- [ ] Selante PU 40 / silicone neutro para caixilhos externos calculado e na tabela

**Pisos e Revestimentos Cerâmicos (§6):**
- [ ] Cimentcola AC-I/II/III calculada (escolher conforme área seca/úmida/dupla colagem)
- [ ] Rejunte calculado (consumo varia por tipo de peça e junta)
- [ ] Espaçadores/cruzetas calculados
- [ ] Clips niveladores calculados (obrigatórios para porcelanato ≥60×60cm)
- [ ] Cunhas niveladoras calculadas (30% dos clips)
- [ ] Primer de contato avaliado (necessário em substratos absorventes)


---

## 🌳 Árvore de Decisão — SKILL 03B

| Pedido | Ação | Seção |
|---|---|---|
| "Quantifique a impermeabilização do banheiro" | Solicitar: Comp, Larg, Perímetro, se tem box | §1 |
| "Quantifique o telhado" | → SKILL 03C (cobertura) | — |
| "Quantifique esquadrias" | Montar Quadro Mestre → derivar vergas e kit | §2 |
| "Rodapé e soleira do apartamento" | Solicitar: Perímetro, largura de portas/janelas | §3 |
| "Quantifique louças e metais" | Montar matriz de ambientes × pavimentos | §4 |
| "Quantifique bancadas de granito" | Tabela por CÓD de especificação | §5 |
