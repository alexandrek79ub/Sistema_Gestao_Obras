# 🏠 SKILL MÓDULO 03C: Fachadas, Cobertura, Muros e Pavimentação Externa

> **Parte de:** [`SKILL_QUANT_03_ARQUITETURA.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANT_03_ARQUITETURA.md) (arquivo índice)
> **Dependência:** Carregar sempre com [`SKILL_QUANTIFICACAO_MASTER.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANTIFICACAO_MASTER.md)
> **Ativar quando:** "fachada", "cobertura", "telhado", "calha", "rufo", "muro de divisa", "fechamento perimetral", "portão", "pavimentação externa", "paver", "passeio público"

> 🛡️ **BLINDAGEM ANTI-ESTIMATIVA (INVIOLÁVEL):** Dimensões só de pranchas. Falta de informação → `⚠️ [ITEM NÃO LEVANTADO - RFI]`.

---

## 📐 1. Revestimentos Externos por Panos de Fachada

> ⚠️ **REGRA DE FACHADA:** É **PROIBIDO** medir fachada por perímetro interno ou simplificação. O orçamento DEVE ser desmembrado por **Panos de Fachada (`PANO 01, PANO 02...`)**, considerando reentrâncias, sacadas, platibandas, frisos e molduras.

### 1.1 Parâmetros de Entrada por Pano

| Parâmetro | Unidade | Descrição |
|---|---|---|
| Comprimento do Pano | m | Extensão horizontal contínua do trecho |
| Altura (PD do Pano) | m | Da base/balancim até o topo/platibanda |
| Vãos Total | m² | Soma das esquadrias e aberturas externas |
| Vãos p/ Desconto NBR (> 2,00 m²) | m² | Excedente para contrato de fachadistas |
| Frisos e Faixas | m | Juntas de dilatação, frisos decorativos, pingadeiras |
| Requadros e Molduras | m | Requadramento de janelas e sacadas |

### 1.2 Fórmulas de Fachada

```
1. Chapisco e Massa Única MAT (m²):
   A_fachada_MAT = (Comprimento × Altura) − Vãos_Total

2. Chapisco e Massa Única MDO / Balancim (m²):
   A_fachada_MDO = (Comprimento × Altura) − Vãos_p/ Desconto_NBR

3. Frisos, Juntas de Dilatação e Pingadeiras (m):
   L_frisos = Σ (metros lineares no pano)

4. Requadro de Molduras e Peitoris Externos (m):
   L_requadro = Σ (Perímetro dos vãos requadrados na fachada)
```

### 1.3 Coeficientes TCPO — Fachada

| Serviço | Insumo | Consumo | Unidade |
|---|---|---|---|
| **Textura acrílica lisa (rolo)** | Textura | 1,0 | kg/m² |
| **Textura acrílica projetada** | Textura | 2,5 | kg/m² |
| **Grafiato (riscada)** | Grafiato | 2,5 | kg/m² |
| | Selador acrílico | 0,10 | L/m² |

---

## 📐 2. Cobertura (Telhado)

### 2.1 Fórmula — Área Inclinada

```
A_inclinada = A_horizontal / cos(θ)
```

### 2.2 Fatores de Inclinação

| Inclinação | cos(θ) | Fator Multiplicador |
|---|---|---|
| 15° | 0,966 | 1,035 |
| 22° | 0,927 | 1,079 |
| 30° | 0,866 | 1,155 |
| 45° | 0,707 | 1,414 |

**Acréscimos lineares (medidos em metros):**
- Beiral: projeção horizontal × fator de inclinação
- Calhas e rufos: m linear
- Cumeeiras: m linear

### 2.3 Kit Cobertura (Miudezas Obrigatórias)

> 🛑 **PROIBIDO orçar telhado sem os acessórios de fixação e estanqueidade.**

| Item | Cálculo | UCC |
|---|---|---|
| Parafusos autobrocantes 12×1"/2" c/ arruela EPDM | `Ceil(A_real × 4,5) × 1,05` | unid |
| Parafusos de costura (stitch) 10×3/4" (a 0,50m na emenda) | `Ceil(L_terças × N_linhas / 0,50) × 1,05` | unid |
| Fita butílica autoadesiva 15mm (rolos 10m) | `Ceil(L_emendas / 10) × 1,05` | rolo |
| Chumbadores parabolts CBA 3/8"×3" fixação terças (2/apoio) | `N_linhas × N_muretas × 2 × 1,05` | unid |
| Rebites de repuxo alumínio 4,0×10mm (10/m de emenda) | `Ceil(N_emendas × 10) × 1,05` | cento |
| Selante PU 40 calhas/rufos (1 tubo / 5m de junta) | `Ceil(L_emendas_calha / 5,0) × 1,05` | tubo |

---

## 📐 3. Muros de Divisa e Fechamentos Perimetrais

### 3.1 Elementos do Muro (por metro linear L_muro)

**Escavação do baldrame/sapata:**
```
V_escav = L_muro × B_sapata × H_cava (m³)
```

**Viga baldrame/sapata de concreto armado:**
```
V_concreto = L_muro × b_viga × h_viga (m³)
A_forma = L_muro × (2h + b) (m²)
Aço = V_concreto × taxa (kg/m³)
```

**Alvenaria do muro:**
```
A_muro = L_muro × H_muro (m²)  [Blocos 14×19×39 cm]
```

**Pilaretes de travamento (a cada 2,50–3,00m):**
```
N_pilaretes = Ceil(L_muro / 2,75m)
V_pilarete = 0,14 × 0,19 × H_muro × N_pilaretes (m³)
```

**Cinta de coroamento (topo):**
```
V_cinta = L_muro × A_calha_canaleta (m³)
[Blocos canaleta no topo do muro]
```

**Chapim / Pingadeira (proteção de topo):**
```
L_chapim = L_muro (m linear)
```

**Revestimento (ambas as faces quando couber):**
```
A_revest = 2 × A_muro (m²)
[Chapisco + Emboço + Pintura Acrílica / Textura]
```

**Concertina / Cerca Elétrica (quando especificada):**
```
L_concertina = L_muro (m) — Lança dupla espiral ∅30cm/45cm
L_cerca_eletrica = L_muro (m) — 6 fios c/ hastes de alumínio
```

---

## 📐 4. Portões de Acesso

### 4.1 Portões de Veículos e Automação

| Item | Unidade | Observação |
|---|---|---|
| Portão basculante / deslizante / pivotante | m² ou unid | Alumínio anodizado / aço galvanizado c/ pintura epóxi |
| Motor automatizador (cremalheira / fuso) | unid | 1/3 HP ou 1/2 HP com fotoelétrica e controles |
| Cancela automatizada de garagem (haste 3–4m) | unid | Controle de fluxo de garagem |

### 4.2 Portões de Pedestres e Controle de Acesso

| Item | Unidade | Observação |
|---|---|---|
| Portão social de pedestres | unid | c/ fechadura eletroímã 150/280 kgf |
| Catracas / torniquetes inox | unid | c/ biometria / RFID / pânico |

---

## 📐 5. Pavimentação Externa, Passeios e Meio-Fio

| Serviço | Unidade | Observação técnica |
|---|---|---|
| Regularização e compactação de solo | m² | Compactador mecânico (sapo) |
| Sub-base de BGS (Brita Graduada Simples) | m³ | e = 10–20cm (camada drenante/estrutural) |
| Piso intertravado / Paver | m² | e = 6cm (pedestre) / e = 8cm (veicular) + colchão areia 5cm |
| Guia / Meio-fio pré-moldado | m | Padrão prefeitura 15×30×100cm |
| Sarjeta moldada in loco | m | Concreto C20, L=30cm, e=8cm |
| Piso tátil alerta e direcional | m² ou m | ABNT NBR 9050 — placas 25×25 / 30×30cm |

---

## 📐 6. Protocolo de Registro de Omissão — Padrão Obrigatório

Sempre que uma informação necessária não constar nas pranchas:

```
> ⚠️ OBSERVAÇÃO DE AUDITORIA — ITEM NÃO LEVANTADO:
> - Serviço/Elemento: [Ex: Pingadeira de concreto no topo do muro]
> - Localização: [Ex: Muro Norte — trecho 01]
> - Prancha de Referência: [Ex: Prancha AÇU-3.DES-A100 Rev 01]
> - Motivo: Cota da pingadeira e especificação do material não indicadas na prancha.
> - Ação: RFI nº [XX] emitida. Item será incorporado após resposta.
```

---

## 🌳 Árvore de Decisão — SKILL 03C

| Pedido | Ação | Seção |
|---|---|---|
| "Quantifique o revestimento de fachada" | Desmembrar por panos (PANO 01, 02...) | §1 |
| "Quantifique a cobertura / telhado" | Solicitar: área horizontal, inclinação (°), tipo de telha | §2 |
| "Quantifique o muro de divisa" | Solicitar: L_muro, H_muro, B_sapata, H_cava, tipo de muro | §3 |
| "Quantifique portões / automação" | Identificar tipo + dimensões + automação | §4 |
| "Quantifique a pavimentação externa" | Levantar sub-base + piso + meio-fio + acessibilidade | §5 |
