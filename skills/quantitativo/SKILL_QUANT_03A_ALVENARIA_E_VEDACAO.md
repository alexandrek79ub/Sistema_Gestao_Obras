# 🏠 SKILL MÓDULO 03A: Alvenaria, Vedação e Revestimentos Internos

> **Parte de:** [`SKILL_QUANT_03_ARQUITETURA.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANT_03_ARQUITETURA.md) (arquivo índice)
> **Dependência:** Carregar sempre com [`SKILL_QUANTIFICACAO_MASTER.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANTIFICACAO_MASTER.md)
> **Normas:** NBR 12721 (Critérios de medição), TCPO 14ª Edição
> **Ativar quando:** "quantifique alvenaria", "calcule revestimento de parede", "quantifique emboço", "gesso", "cerâmica de parede"

> 🛡️ **BLINDAGEM CONTRA QUANTITATIVOS ESTIMADOS (REGRA INVIOLÁVEL):**
> Todo levantamento DEVE ser 100% embasado em cotas extraídas diretamente das pranchas. É **PROIBIDO** estimar, supor ou inferir qualquer dimensão. Se faltar informação, registrar `⚠️ [ITEM NÃO LEVANTADO POR FALTA DE INFORMAÇÃO NO DESENHO]` e emitir RFI.

---

## 📐 1. Alvenaria e Vedação

### 1.1 Fórmulas de Perímetro e Área Bruta

**Ambiente retangular — 4 paredes:**
```
P_perímetro_externo = 2 × Comp_ext + 2 × (Larg_ext − 2 × e_parede)
P_alvenaria_líquido = P_perímetro_externo − Σ (Largura_pilares_concreto) + Σ (Paredes_divisórias_internas)
A_bruta = P_alvenaria_líquido × H_pé-direito
A_líquida = A_bruta − Σ Descontos de Vãos (NBR 12721 Art. 3)
A_final = A_líquida × (1 + Taxa de Perda)
```

> ⚠️ **Regras Anti-Duplicidade (OBRIGATÓRIAS):**
> 1. **Desconto de Pilares de Concreto:** Subtrair largura de cada pilar (`b_pilar`) do perímetro — não há bloco onde há pilar.
> 2. **Desconto de Cantos em "L":** `P_ext_líquido = 2 × Comp_ext + 2 × (Larg_ext − 2 × e_parede)`.
> 3. **Desconto de Nós "T" e "X" (Divisórias Internas):** Medir vão livre entre faces, nunca de eixo a eixo.

**Ambiente com geometria irregular (L, U, T, recortes):**
```
A_bruta = (P1 + P2 + P3 + ... + Pn) × H_pé-direito
```
> O agente DEVE perguntar o comprimento de cada trecho (P1, P2...) se o ambiente for irregular.

**Pintura Externa da Fachada:**
```
P_fachada_ext = 2 × (Comp_ext + Larg_ext)
A_bruta_fachada = P_fachada_ext × H_fachada
A_líquida_pintura_ext = A_bruta_fachada − Σ Descontos de Vãos de Esquadrias Externas
```

**Emboço sob Forro Rebaixado:**
```
H_emboço_parede = H_forro + 0,10 m (transpasse mínimo de 10 cm)
A_bruta_emboço = P_interno × H_emboço_parede
```

**Pintura sob Forro Rebaixado:**
```
H_pintura_parede = H_forro (altura visível do piso à tabica)
A_bruta_pintura_int = P_interno × H_pintura_parede
```

**Platibanda sobre Viga Invertida:**
```
H_alvenaria_platibanda = H_platibanda_total − h_viga_invertida
A_alvenaria_platibanda = P_líquido_platibanda × H_alvenaria_platibanda
A_pintura_ext_platibanda = P_fachada_ext × H_platibanda_total
A_emboço_int_platibanda = P_líquido_platibanda × H_platibanda_total
```

**Muretas de Apoio de Telhado (entreforro):**
```
A_alvenaria_apoio = Σ (Comprimento_vão × H_mureta_i)
Revestimento_muretas = 0,00 m² (sem emboço no entreforro)
```

---

### 1.2 Regra de Desconto de Vãos — NBR 12721 (DUPLA VISÃO: Material vs. Serviço)

> ⚠️ Todo orçamento de alvenaria/revestimento DEVE gerar duas quantificações separadas:

| Visão | Regra de Vãos | Para que serve |
|---|---|---|
| **MATERIAL (Suprimentos)** | Desconto físico 100% de todos os vãos | Comprar a quantidade real de blocos/argamassa |
| **SERVIÇO (Empreiteiro/MDO)** | Regra NBR 12721 | Medir e pagar o empreiteiro |

| Área do Vão | NBR 12721 — Critério | Desconto na Medição |
|---|---|---|
| A_vão ≤ 2,00 m² | **NÃO desconta** | 0,00 m² |
| 2,00 < A_vão ≤ 6,00 m² | **Desconta o excedente** | A_vão − 2,00 m² |
| A_vão > 6,00 m² | **Desconta tudo** | A_vão completo |
| Armário embutido / nicho | **Desconta 100%** | A_nicho completo |

---

### 1.3 Taxas de Perda por Serviço de Parede

| Serviço | Taxa de Perda |
|---|---|
| Chapisco | 5% |
| Emboço / Reboco | 5% |
| Gesso liso | 5% |
| Cerâmica / Porcelanato (parede) | 10% |
| Tinta látex acrílica | 10% |
| Massa corrida PVA | 0% (sobre área líquida) |

---

### 1.4 Método Paramétrico (Viabilidade) vs. Executivo com Paginação

#### 🅰️ FASE 1 — Estudo Preliminar (SEM projeto executivo)
Autorizado apenas com aprovação explícita do cliente para estimativa preliminar:
- Estimativa de graute por metros lineares de vergas/contravergas
- Estimativa de graute de pilaretes a cada 1,5m–2,0m de altura
- Encunhamento paramétrico: `Comprimento × Espessura × 0,05m`

#### 🅱️ FASE 2 — Orçamento Executivo (COM paginação de alvenaria estrutural)
Quantificação por Elevação Parede a Parede (`ELEV`). SKUs obrigatórios:

| SKU | Bloco | Dimensões | Função |
|---|---|---|---|
| B144 / B194 | Inteiro de Vedação | 14×19×39 / 19×19×39 cm | Elevação corrente |
| B142 / B192 | Meio Bloco | 14×19×19 / 19×19×19 cm | Amarração de cantos/vãos |
| C144 / C194 | Canaleta Inteiro | 14×19×39 / 19×19×39 cm | Vergas, contravergas, cintas |
| C142 / C192 | Canaleta Meio | 14×19×19 / 19×19×19 cm | Fechamento de amarrações |
| BC94 | Compensador / Japa | Variável | Ajuste fino de módulo |

---

### 1.5 Desmembramento Obrigatório em SKUs Comerciais

> 🛑 **PROIBIDO "bloco genérico"** — todo levantamento DEVE separar:

1. **Blocos Canaleta (vergas + contravergas + cintas):**
```
L_vergas_portas = Σ (Largura_porta + 2 × 0,20m)
L_vergas_janelas = Σ (Largura_janela + 2 × 0,20m)
L_contravergas = Σ (Largura_janela + 2 × 0,20m)
L_cintas = extensão indicada em projeto
N_canaletas = Ceil(L_total / 0,40m) × 1,05
```

2. **Graute para canaletas:**
```
V_graute = L_canaleta_total × 0,0126 m² × 1,05
```

3. **Armadura de vergas/contravergas (CA-50 Ø8,0mm):**
```
L_aço = L_canaleta_total × 2 × 1,05
N_barras_12m = Ceil(L_aço / 12,0m)
Peso = L_aço × 0,395 kg/m
```

4. **Meios blocos (ombreiras de portas/janelas + cantos):**
```
N_meios_portas = Σ [ Floor(H_porta / 0,40m) × 2 ombreiras ]
N_meios_janelas = Σ [ Floor(H_janela / 0,40m) × 2 ombreiras ]
N_meios_cantos = N_encontros × Floor(H_parede / 0,40m)
N_total = (N_meios_portas + N_meios_janelas + N_meios_cantos) × 1,05
```

5. **Blocos inteiros correntes:**
```
N_equiv_total = A_alvenaria_líquida × 12,5 blocos/m²
N_inteiros = [N_equiv_total − N_canaletas − (N_meios / 2)] × 1,05
```

6. **Argamassa de assentamento:**
```
V_argamassa = A_alvenaria_líquida × 0,018 m³/m² × 1,05
Cimento = A_alvenaria_líquida × 5,2 kg/m² × 1,05
Cal = A_alvenaria_líquida × 1,8 kg/m² × 1,05
Areia = A_alvenaria_líquida × 0,022 m³/m² × 1,05
```

---

### 1.6 Kit de Acessórios de Alvenaria (Miudezas Obrigatórias)

| Item | Cálculo | UCC |
|---|---|---|
| Telas de amarração galvanizadas (a cada 2 fiadas) | `N_interfaces_pilar × Floor(H/0,40m) × 1,05` | unid |
| Pinos finca-pinos + cartuchos | `N_telas × 2 × 1,05` | unid |
| Adesivo plastificante (0,20 L/m² de chapisco) | `A_chapisco × 0,20` | lata 18L ↑ |
| Encunhamento (espuma/argamassa exp.) no topo das paredes | `L_total_paredes_topo` | m |

---

### 1.7 Coeficientes TCPO — Alvenaria

| Serviço | Insumo | Consumo | Unidade |
|---|---|---|---|
| **Bloco cerâmico 9×19×19** | Blocos | 25,00 | unid/m² |
| | Argamassa (1:2:8) | 0,022 | m³/m² |
| | Cimento CP II | 3,8 | kg/m² |
| **Bloco cerâmico 14×19×19** | Blocos | 25,00 | unid/m² |
| | Argamassa (1:2:8) | 0,030 | m³/m² |
| | Cimento CP II | 5,2 | kg/m² |
| **Chapisco** | Cimento CP II | 3,0 | kg/m² |
| | Areia grossa | 0,006 | m³/m² |
| **Emboço 20mm** | Cimento CP II | 5,8 | kg/m² |
| | Areia média | 0,030 | m³/m² |
| | Cal hidratada | 1,2 | kg/m² |
| **Gesso liso** | Gesso em pó | 2,5 | kg/m² |

---

## 📐 2. Pisos, Contrapisos e Revestimentos de Piso

### 2.1 Fórmulas

**Retangular:**
```
A_piso = Comp_interno × Larg_interno
A_piso_líq = A_piso − pilares embutidos − ralos/grelhas
A_final = A_piso_líq × (1 + Taxa de Perda)
```

**Irregular:** decompor em retângulos/triângulos, somar as áreas parciais.

### 2.2 Taxas de Perda por Tipo de Piso

| Tipo de Piso | Perda |
|---|---|
| Cerâmica / Porcelanato alinhado | 10% |
| Cerâmica / Porcelanato diagonal | 15% |
| Laminado / Vinílico plank | 10% |
| Piso natural (mármore, granito) | 10% |
| Contrapiso de regularização | 5% |
| Concreto polido | 3% |

### 2.3 Coeficientes TCPO — Pisos e Contrapisos

| Serviço | Insumo | Consumo | Unidade |
|---|---|---|---|
| **Contrapiso 50mm** | Cimento CP II | 9,0 | kg/m² |
| | Areia grossa | 0,038 | m³/m² |
| **Argamassa colante AC-I (áreas secas)** | Cimentcola | 5,0 | kg/m² |
| **AC-II (úmidas/externas)** | Cimentcola | 5,0 | kg/m² |
| **AC-III dupla colagem (≥ 60×60cm)** | Cimentcola | 10,0 | kg/m² |
| **Rejunte (cerâmica 45×45cm, junta 3mm)** | Rejunte | 0,35 | kg/m² |
| **Rejunte (porcelanato 60×60cm, junta 2mm)** | Rejunte | 0,25 | kg/m² |
| **Espaçadores/cruzetas** | Espaçador | 6,0 | unid/m² |

---

## 📐 3. Revestimento de Teto

> ⚠️ **SEPARAÇÃO OBRIGATÓRIA:** Teto é serviço separado da parede. Memórias de cálculo independentes.

### 3.1 Fórmula
```
A_teto = Comp_interno × Larg_interno
A_teto_líq = A_teto − alçapão / shaft / luminária grande
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

## 📐 4. Paredes e Forros de Drywall

### 4.1 Parede de Drywall
```
A_drywall = Comprimento × H_pé-direito
A_final = A_drywall × (1 + 10% perda)
```
> Parede simples = 2 chapas por m² linear. Dupla = 4 chapas.

| Insumo | Consumo | Unidade |
|---|---|---|
| Chapa gesso ST 12,5mm (1,20×1,80m) | 2,08 | chapa/m² |
| Montante 48mm | 1,67 | m/m² |
| Guia 48mm | 0,67 | m/m² |
| Parafuso drywall GN 25/35 | 24 | unid/m² |
| Fita microperfurada | 1,50 | m/m² |
| Massa de rejunte | 0,50 | kg/m² |

### 4.2 Forro de Drywall
```
A_forro = Comp × Larg
A_final = A_forro × (1 + 10%)
```

| Insumo | Consumo | Unidade |
|---|---|---|
| Chapa gesso ST 12,5mm | 1,04 | chapa/m² |
| Perfil canaleta 48mm | 2,50 | m/m² |
| Pendural regulável | 1,00 | unid/m² |
| Parafuso | 12 | unid/m² |

### 4.3 Acessórios de Drywall (Obrigatórios)

| Item | Cálculo | UCC |
|---|---|---|
| Paraf. metal-metal LB 4,2×13 (montante × guia) | `L_montantes × 6 × 1,05` | cento ↑ |
| Fita telada fibra de vidro | `A_drywall × 1,50 m/m²` | rolo 50m ↑ |
| Massa para juntas (baldes 20kg) | `A_drywall × 0,50 kg/m²` | balde ↑ |
| Banda acústica EVA (sob guias) | `Perímetro_guias` | rolo 10m ↑ |

---

## 📐 5. Pinturas — Coeficientes TCPO

| Serviço | Insumo | Consumo | Unidade |
|---|---|---|---|
| **Pintura Látex Acrílico** | Selador acrílico | 0,10 | L/m² |
| | Tinta (2 demãos) | 0,26 | L/m² |
| **Massa Corrida PVA (2 demãos)** | Massa PVA | 0,90 | kg/m² |
| | Lixa grão 150 | 0,10 | folha/m² |
| **Textura Acrílica Lisa** | Textura | 1,0 | kg/m² |
| **Grafiato (textura riscada)** | Grafiato | 2,5 | kg/m² |
| | Selador acrílico | 0,10 | L/m² |

### Kit de Pintura (Miudezas Obrigatórias)

| Item | Cálculo | UCC |
|---|---|---|
| Selador acrílico (18L) | `A_nova × 0,10 L/m²` | lata ↑ |
| Fundo preparador (18L) | `(A_gesso + A_drywall) × 0,10` | lata ↑ |
| Massa PVA / Acrílica (25kg) | `A × consumo kg/m²` | lata ↑ |
| Lixa grossa gr.80 | `A_reboco × 0,05` | folha ↑ |
| Lixa fina gr.150 | `A_massa × 0,10` | folha ↑ |
| Fita crepe 24mm × 50m | `Perim_proteção / 50m` | rolo ↑ |
| Lona plástica (bobinas 100m²) | `A_piso / 100` | bobina ↑ |
| Aguarrás mineral (L) | `V_esmalte / 10` | litro ↑ |

---

## 🌳 Árvore de Decisão — SKILL 03A

| Pedido | Ação | Seção |
|---|---|---|
| "Quantifique o revestimento de parede do banheiro" | Solicitar: Comp, Larg, H, vãos (L×H), tipo | §1 |
| "Quantifique a alvenaria do apartamento" | Para cada ambiente: Comp, Larg, H, vãos → §1 e §9 | §1.1 + §1.5 |
| "Quantifique o piso da cozinha" | Solicitar: Comp, Larg, geometria, tipo de piso | §2 |
| "Quantifique o teto da sala" | Solicitar: Comp, Larg, tipo de acabamento | §3 |
| "Paredes de drywall da área gourmet" | Solicitar: comp. de cada parede, pé-direito, simples/dupla | §4 |
| "Quantifique a pintura de toda a obra" | §1 (paredes) + §3 (teto) → aplicar §5 | §1+§3+§5 |
