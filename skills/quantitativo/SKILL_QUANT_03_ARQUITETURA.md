# 🏠 SKILL MÓDULO 03: Arquitetura & Acabamentos

> **Dependência:** Carregar sempre com [SKILL_QUANTIFICACAO_MASTER.md](file:///c:/Users/Alexandre/Workspace/A11_FREE%20LANCER%20ENGENHARIA/skills/quantitativo/SKILL_QUANTIFICACAO_MASTER.md)
> **Normas:** NBR 12721 (Critérios de medição), TCPO 14ª Edição

---

## 🧭 Escopo deste Módulo

Cobre o quantitativo de **toda a arquitetura e acabamentos** de uma edificação:

- Alvenaria de vedação (blocos cerâmicos e de concreto)
- Revestimentos de parede (chapisco, emboço, reboco, gesso, cerâmica)
- Revestimentos de teto (gesso, forro PVC, drywall, pintura)
- Pisos e contrapisos
- Cobertura (telhado)
- Impermeabilização
- Esquadrias (portas e janelas)
- Rodapés, peitoris e soleiras
- Drywall (paredes e forros)
- Pinturas (interna e externa)
- Textura / Grafiato (fachada)

---

## 📐 1. Alvenaria e Revestimentos de Parede

> ⚠️ Revestimento de PAREDE e TETO são serviços separados. Parede = área vertical. Teto = área horizontal (§3). Nunca somar na mesma memória.

### 1.1 Fórmulas

**Ambiente retangular — Alvenaria de Vedação / Estrutural (4 paredes):**
```
P_perímetro_externo = 2 × Comp_ext + 2 × (Larg_ext − 2 × e_parede)
P_alvenaria_líquido = P_perímetro_externo − Σ (Largura_pilares_concreto) + Σ (Paredes_divisórias_internas)
A_bruta = P_alvenaria_líquido × H_pé-direito
A_líquida = A_bruta − Σ Descontos de Vãos (NBR 12721 Art. 3)
A_final = A_líquida × (1 + Taxa de Perda)
```
> ⚠️ **Regras Obrigatórias de Alvenaria:**
> 1. **Desconto de Pilares de Concreto:** Em estruturas convencionais com pilares de concreto in loco embutidos na alvenaria, a largura de CADA pilar (`b_pilar`) DEVE ser subtraída do perímetro de alvenaria, pois não há tijolos/blocos onde existe concreto.
> 2. **Desconto de Interseções de Canto:** No contorno de alvenaria, considera-se a dimensão externa em um dos sentidos (longitudinal ou transversal) e descontam-se as 2 espessuras de parede (`2 × e_parede`) no outro sentido, evitando sobreposição dos 4 cantos.

**Pintura Externa da Fachada (Perímetro Bruto da Fachada):**
```
P_fachada_ext = 2 × (Comp_ext + Larg_ext)
A_bruta_fachada = P_fachada_ext × H_fachada
A_líquida_pintura_ext = A_bruta_fachada − Σ Descontos de Vãos de Esquadrias Externas
```
> ⚠️ **Regra de Pintura Externa:** A pintura externa reveste a face EXTERNA da edificação de ponta a ponta. Portanto, usa-se o **perímetro bruto externo da fachada** `2 × (Comp_ext + Larg_ext)` sem descontar espessuras de paredes ou cantos internos.

**Emboço e Chapisco de Paredes Internas sob Forro Rebaixado:**
```
H_emboço_parede = H_forro + 0,10 m (transpasse mínimo de 10 cm acima da linha do forro)
A_bruta_emboço = P_interno × H_emboço_parede
A_líquida_emboço = A_bruta_emboço − Σ Descontos de Vãos Internos
```
> ⚠️ **Regra de Emboço sob Forro Rebaixado:** O chapisco e emboço de parede DEVEM ser calculados com acréscimo de **10 cm a 15 cm acima da cota do forro** (`H_forro + 0,10m`) para que o gesseiro fixe a tabica perimétrica sobre superfície lisa e regularizada.

**Pintura de Paredes Internas sob Forro Rebaixado:**
```
H_pintura_parede = H_forro (altura livre visível do piso até a tabica/forro)
A_bruta_pintura_int = P_interno × H_pintura_parede
A_líquida_pintura_int = A_bruta_pintura_int − Σ Descontos de Vãos Internos
```
> ⚠️ **Regra de Pintura sob Forro Rebaixado:** A pintura é executada APÓS o forro já estar instalado. Portanto, a altura de pintura de parede é exatamente a altura visível do piso ao forro (`H_forro`), sem pintar a área oculta acima do gesso.

**Ambiente com geometria irregular (L, U, T, recortes):**
```
A_bruta = (P1 + P2 + P3 + ... + Pn) × H_pé-direito
Onde P1..Pn = comprimento medido de CADA trecho de parede individualmente descontando pilares e cantos
A_líquida = A_bruta − Σ Descontos de Vãos
A_final = A_líquida × (1 + Taxa de Perda)
```
> O agente DEVE perguntar se o ambiente é retangular ou irregular. Se irregular, solicitar comprimento de cada trecho (P1, P2, P3...).

### 1.2 Regra de Desconto de Vãos — NBR 12721 Art. 3

| Área do Vão (A_vão) | Critério | Desconto |
|---|---|---|
| A_vão ≤ 2,00 m² | **NÃO desconta** | 0,00 m² (compensa arremates) |
| 2,00 m² < A_vão ≤ 6,00 m² | **Desconta o excedente** | A_vão − 2,00 m² |
| A_vão > 6,00 m² | **Desconta tudo** | A_vão completo |
| Armário embutido / nicho | **Desconta 100%** | A_nicho completo |

### 1.3 Taxas de Perda por Serviço de Parede

| Serviço | Taxa de Perda |
|---|---|
| Chapisco | 5% |
| Emboço / Reboco | 5% |
| Gesso liso | 5% |
| Cerâmica / Porcelanato (parede) | 10% |
| Tinta látex acrílica | 10% |
| Massa corrida PVA | 0% (aplicada sobre área líquida) |

---

## 📐 2. Pisos, Contrapisos e Revestimentos de Piso

### 2.1 Fórmulas

**Ambiente retangular:**
```
A_piso = Comprimento_interno × Largura_interna
A_piso_líq = A_piso − Área de pilares embutidos − Área de ralos/grelhas
A_final = A_piso_líq × (1 + Taxa de Perda)
```

**Ambiente com geometria irregular (L, U, T):**
```
A_piso = Σ (áreas parciais decompostas em retângulos ou triângulos)
A_piso_líq = A_piso − descontos
A_final = A_piso_líq × (1 + Taxa de Perda)
```
> O agente DEVE decompor plantas irregulares em retângulos menores.

### 2.2 Taxas de Perda por Tipo de Piso

| Tipo de Piso | Taxa de Perda |
|---|---|
| Cerâmica / Porcelanato alinhado | 10% |
| Cerâmica / Porcelanato diagonal | 15% |
| Laminado / Vinílico plank | 10% |
| Piso natural (mármore, granito) | 10% |
| Contrapiso de regularização | 5% |
| Concreto polido | 3% |

---

## 📐 3. Revestimento de Teto (Forro / Gesso / Pintura)

> ⚠️ SEPARAÇÃO OBRIGATÓRIA: O teto é um serviço separado da parede. Memórias de cálculo independentes.

### 3.1 Fórmula

```
A_teto = Comprimento_interno × Largura_interna
A_teto_líq = A_teto − Aberturas (alçapão, shaft, luminária grande)
A_final = A_teto_líq × (1 + Taxa de Perda)
```

### 3.2 Taxas de Perda — Teto

| Serviço | Taxa |
|---|---|
| Gesso liso (sarrafeado) | 5% |
| Forro de gesso acartonado (Drywall) | 10% |
| Forro PVC | 10% |
| Pintura de teto | 10% |

---

## 📐 4. Cobertura (Telhado)

### 4.1 Fórmula Área Inclinada

```
A_inclinada = A_horizontal / cos(θ)
Onde θ = inclinação do plano em graus
```

### 4.2 Fatores de Inclinação

| Inclinação | cos(θ) | Fator Multiplicador |
|---|---|---|
| 15° (telha plan, fibrocimento) | 0,966 | 1,035 |
| 22° (telha romana, colonial) | 0,927 | 1,079 |
| 30° (metálica, fibrocimento) | 0,866 | 1,155 |
| 45° (chapa metálica íngreme) | 0,707 | 1,414 |

**Acréscimos lineares (medidos em metros):**
- Beiral: projeção horizontal × fator de inclinação
- Calhas e rufos: m linear
- Cumeeiras: m linear

---

## 📐 5. Esquadrias — Quadro de Portas e Janelas

O agente DEVE gerar tabela de vãos associada a cada memória de revestimento:

| Tag | Tipo | Largura (m) | Altura (m) | Área (m²) | Pavimento | CIA | Observação |
|---|---|---|---|---|---|---|---|
| PA-01 | Porta interna | 0,80 | 2,10 | 1,68 | Térreo | T-101-SAL | Madeira — 1 folha |
| PA-02 | Porta externa | 0,90 | 2,10 | 1,89 | Térreo | T-101-ENT | Madeira c/ batente |
| JA-01 | Janela basculante | 0,60 | 0,60 | 0,36 | Térreo | T-101-BAN | Alumínio s/ peitoril |
| JA-02 | Janela de correr 2F | 1,20 | 1,20 | 1,44 | Térreo | T-101-COZ | Alumínio c/ peitoril |

---

## 📐 6. Rodapés, Peitoris e Soleiras (m)

```
Rodapé = Perímetro_interno − Σ Largura_portas − Σ Largura_nichos
Peitoril = Σ Largura_janelas
Soleira = Σ Largura_portas_externas
```

---

## 📐 7. Impermeabilização

### 7.1 Área Molhada (Banheiro, Sacada, Varanda)

```
A_piso = Comp × Larg
A_arremate = Perímetro_interno × 0,30m
A_impermeab = A_piso + A_arremate
A_final = A_impermeab × (1 + 15% perda)
```

### 7.2 Box de Banheiro

```
A_box_piso = Comp_box × Larg_box
A_box_paredes = Perímetro_box × 1,80m
A_impermeab_box = A_box_piso + A_box_paredes
```

### 7.3 Laje Exposta / Terraço

```
A_impermeab = A_laje + Perímetro × 0,30m (arremate)
A_final = A_impermeab × (1 + 15% perda)
```

- Reservatórios: todas as 6 faces internas (piso + 4 paredes + laje de fundo)
- Piscinas: todas as faces internas + juntas de dilatação

---

## 📐 8. Paredes e Forros de Drywall (Gesso Acartonado)

### 8.1 Paredes de Drywall

```
A_drywall = Comprimento_parede × H_pé-direito
A_final = A_drywall × (1 + 10% perda)
```
> Parede simples = 1 chapa por face (2 chapas por m² linear). Dupla = 2 chapas por face.

**Insumos por m² (parede simples):**

| Insumo | Consumo | Unidade |
|---|---|---|
| Chapa gesso ST 12,5mm (1,20×1,80m) | 2,08 | chapa/m² |
| Montante 48mm (a cada 0,60m) | 1,67 | m/m² |
| Guia 48mm (piso + teto) | 0,67 | m/m² |
| Parafuso drywall | 24 | unid/m² |
| Fita microperfurada | 1,50 | m/m² |
| Massa de rejunte drywall | 0,50 | kg/m² |
| Lã de vidro/rocha (se especificado) | 1,00 | m²/m² |

### 8.2 Forro de Drywall

```
A_forro = Comprimento × Largura
A_final = A_forro × (1 + 10% perda)
```

| Insumo | Consumo | Unidade |
|---|---|---|
| Chapa gesso ST 12,5mm | 1,04 | chapa/m² |
| Perfil canaleta 48mm | 2,50 | m/m² |
| Pendural regulável | 1,00 | unid/m² |
| Parafuso | 12 | unid/m² |

---

## 📦 9. Coeficientes de Consumo TCPO — Arquitetura

### 9.1 Alvenaria — Bloco Cerâmico 9×19×19 (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Blocos cerâmicos 9×19×19 | 25,00 | unid/m² |
| Argamassa de assentamento (1:2:8) | 0,022 | m³/m² |
| Cimento Portland CP II | 3,8 | kg/m² |
| Areia média | 0,018 | m³/m² |

### 9.2 Alvenaria — Bloco Cerâmico 14×19×19 (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Blocos cerâmicos 14×19×19 | 25,00 | unid/m² |
| Argamassa de assentamento (1:2:8) | 0,030 | m³/m² |
| Cimento Portland CP II | 5,2 | kg/m² |

### 9.3 Chapisco (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Cimento CP II | 3,0 | kg/m² |
| Areia grossa | 0,006 | m³/m² |
| Água | 1,2 | L/m² |

### 9.4 Emboço Paulista — esp. 20mm (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Cimento CP II | 5,8 | kg/m² |
| Areia média | 0,030 | m³/m² |
| Cal hidratada | 1,2 | kg/m² |
| Água | 8,5 | L/m² |

### 9.5 Reboco Fino — esp. 5mm (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Cimento branco ou CP II | 2,0 | kg/m² |
| Areia fina peneirada | 0,006 | m³/m² |

### 9.6 Gesso Liso (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Gesso em pó | 2,5 | kg/m² |
| Água | 1,0 | L/m² |

### 9.7 Pintura Látex Acrílico (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Selador acrílico | 0,10 | L/m² |
| Tinta látex 1ª demão | 0,13 | L/m² |
| Tinta látex 2ª demão | 0,13 | L/m² |
| **Total tinta** | **0,26** | **L/m²** |

### 9.8 Contrapiso — esp. 50mm (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Cimento CP II | 9,0 | kg/m² |
| Areia grossa | 0,038 | m³/m² |
| Água | 12,0 | L/m² |

### 9.9 Massa Corrida PVA (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Massa corrida PVA (1ª demão) | 0,50 | kg/m² |
| Massa corrida PVA (2ª demão) | 0,40 | kg/m² |
| **Total (2 demãos)** | **0,90** | **kg/m²** |
| Lixa grão 150 | 0,10 | folha/m² |

### 9.10 Argamassa Colante para Cerâmica/Porcelanato (por m²)

| Tipo | Consumo | Aplicação |
|---|---|---|
| AC-I | 5,0 kg/m² | Pisos internos, áreas secas |
| AC-II | 5,0 kg/m² | Pisos externos, áreas úmidas, fachadas |
| AC-III | 5,0 kg/m² | Porcelanatos grandes, fachadas altas |
| AC-IIIE | 5,0 kg/m² | Lajes aquecidas, fachadas |

> **Dupla colagem** (peças ≥ 60×60cm ou fachadas): **10,0 kg/m²**

### 9.11 Rejunte para Cerâmica/Porcelanato (por m²)

| Peça | Junta | Consumo |
|---|---|---|
| Cerâmica até 30×30cm | 3mm | 0,50 kg/m² |
| Cerâmica 45×45cm | 3mm | 0,35 kg/m² |
| Porcelanato 60×60cm | 2mm | 0,25 kg/m² |
| Porcelanato 80×80cm+ | 2mm | 0,20 kg/m² |
| Cerâmica de parede 30×60cm | 2mm | 0,30 kg/m² |

### 9.12 Assentamento de Piso — Composição Completa (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Piso cerâmico/porcelanato | 1,00 | m²/m² (+ taxa perda §2.2) |
| Argamassa colante | 5,0 (ou 10,0 dupla colagem) | kg/m² |
| Rejunte | conforme §9.11 | kg/m² |
| Espaçador (cruzeta) | 6,0 | unid/m² |

### 9.13 Textura Acrílica / Grafiato — Acabamento Externo (por m²)

| Insumo | Consumo | Unidade |
|---|---|---|
| Textura acrílica lisa (rolo) | 1,0 | kg/m² |
| Textura acrílica projetada | 2,5 | kg/m² |
| Grafiato (textura riscada) | 2,5 | kg/m² |
| Selador acrílico (base) | 0,10 | L/m² |

### 9.14 Impermeabilização (por m²)

| Tipo | Consumo | Unidade |
|---|---|---|
| Manta asfáltica 3mm (c/ feltro) | 1,20 | m²/m² (sobreposição 10cm) |
| Manta asfáltica 4mm (c/ feltro) | 1,20 | m²/m² (sobreposição 10cm) |
| Primer asfáltico (imprimação) | 0,40 | L/m² |
| Argamassa polimérica (2 demãos) | 3,0 | kg/m² |
| Tela de poliéster (reforço) | 1,10 | m²/m² (sobreposição 5cm) |

---

## 🌳 10. Árvore de Decisão — Arquitetura

| Pedido do Usuário | Ação do Agente | Seção |
|---|---|---|
| "Quantifique o revestimento de parede do banheiro" | Solicitar: Comp, Larg, H, vãos (porta/janela: L×H), tipo de revestimento | §1 |
| "Quantifique o piso da cozinha" | Solicitar: Comp, Larg, geometria, tipo de piso, peças de pilares embutidos | §2 + §9.10–9.12 |
| "Quantifique o teto da sala" | Solicitar: Comp, Larg, tipo de acabamento (gesso/pintura/drywall) | §3 |
| "Quantifique a impermeabilização do banheiro" | Solicitar: Comp, Larg, Perímetro, se tem box (dim do box) | §7.1 + §7.2 + §9.14 |
| "Paredes de drywall da área gourmet" | Solicitar: comprimento de cada parede, pé-direito, simples/dupla | §8.1 |
| "Quantifique a cobertura" | Solicitar: área projetada em planta, inclinação (°), tipo de telha | §4 |
| "Quantifique a alvenaria do apartamento" | Para cada ambiente: Comp, Larg, H, vãos — calcular §1 e aplicar §9.1/9.2 | §1 + §9.1 |
| "Quantifique a pintura de toda a obra" | Paredes (§1) + Teto (§3) → aplicar coef. pintura §9.7 | §1+§3+§9.7 |
