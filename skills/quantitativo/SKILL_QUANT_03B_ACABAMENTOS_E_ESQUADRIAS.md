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

---

## 📐 2. Esquadrias, Vidros e Derivação de Vergas

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

---

## 📐 3. Rodapés, Peitoris e Soleiras

```
Rodapé líquido (m) = Perímetro_interno − Σ Largura_portas − Σ Largura_nichos
Peitoril (m)       = Σ Largura_janelas
Soleira (m)        = Σ Largura_portas_externas
Baguete de box (m) = Largura_box (contenção de água)
```

---

## 📐 4. Louças, Metais e Cubas

### 4.1 Categorias

| Categoria | Descrição | Unidade |
|---|---|:---:|
| **LOUÇAS** | Bacia c/ cx. acoplada, lavatório c/ coluna, cuba de embutir, tanque | un |
| **CUBAS INOX** | Cuba simples/dupla, tanque inox | un |
| **METAIS** | Torneira de lavatório, torneira pia, misturador, ducha higiênica, chuveiro | un |
| **ACABAMENTOS** | Acabamento reg. gaveta/pressão, sifões, válvulas de escoamento | un |

### 4.2 Fórmula de Multiplicação

```
Qtd_Total_k = Σ (Qtd_Unid_Cômodo × N_ambientes_por_andar × N_andares_repetidos)
```

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

### 6.1 Checklist de Conferência de Serviços — Módulo 03B (🚨 OBRIGATÓRIO)

Antes de finalizar o levantamento de acabamentos:

**Impermeabilização (§1):**
- [ ] Áreas reais líquidas de piso e rodapés virados de banheiros, sacadas e áreas molhadas apuradas conforme projeto (m²).
- [ ] Zero aplicação de perdas percentuais no quantitativo físico.

**Esquadrias (§2):**
- [ ] Contagem exata de portas e janelas confrontada com o Quadro de Esquadrias do projeto de arquitetura (conjuntos).
- [ ] Dimensões de vão (largura × altura) e tipo de abertura conferidos.

**Pisos e Revestimentos Cerâmicos (§6):**
- [ ] Área líquida real de piso por ambiente descontando soleiras e bases fixas (m²).
- [ ] Área de revestimento de parede descontando vãos conforme NBR 12721 (m²).
- [ ] Extensão linear de rodapés descontando os vãos de portas (m).
- [ ] Zero insumos miúdos explodidos (rejunte, colas e espaçadores já compõem as CPUs).



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
