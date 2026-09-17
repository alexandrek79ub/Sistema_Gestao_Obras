# SKILL QUANT 01 — FUNDAÇÕES

> Dependência: `SKILL_QUANTIFICACAO_MASTER.md`
> Referências: NBR 6118, NBR 6122 e NBR 14931, conforme edição aplicável à obra.

Esta skill contém a lógica de levantamento físico líquido de fundações. Não contém dimensões, nomes de elementos, referências de prancha ou resultados de nenhuma obra.

## 1. Escopo

Abrange fundações diretas (sapatas isoladas, associadas e corridas), fundações profundas (estacas e brocas), blocos de coroamento, pedestais, vigas baldrame, cintas, radier, lastro, escavação, reaterro, drenagem e remoção de terra quando comprovados nas pranchas executivas.

## 2. Regras invioláveis

- A IA extrai dimensões e monta expressões; o motor determinístico calcula o resultado.
- Toda entrada (`b`, `L`, `h`, diâmetro, comprimento, cota e quantidade) deve ter evidência de prancha, revisão e página.
- Ausência, conflito ou revisão indefinida gera `PENDENTE_RFI`; nunca usar valor padrão ou fallback.
- Quantidades são físicas, líquidas e nominais: sem perdas, empolamento, arredondamento comercial ou coeficientes de consumo.
- Arame, pregos, espaçadores, desmoldante, madeira de consumo, embalagens e demais consumíveis pertencem exclusivamente à CPU/BOM posterior.
- Aço deve ser extraído do quadro/resumo de armaduras da prancha, por elemento e bitola; não usar taxa genérica de kg/m³.

## 3. Matriz de serviços e critérios de medição

| Serviço | Unidade | Critério físico líquido |
|---|---:|---|
| Locação e gabarito | un / m² | Eixos e área efetivamente locados conforme planta |
| Perfuração ou cravação de estacas | m / un | Comprimento nominal ou unidades indicadas |
| Arrasamento/descabeçamento | un | Unidades explicitamente indicadas |
| Escavação de cavas e valas | m³ | Volume geométrico da seção de projeto |
| Apiloamento/compactação de fundo | m² | Área de fundo efetivamente preparada |
| Lastro/regularização | m³ | Área da base × espessura nominal indicada |
| Fôrmas | m² | Área real de contato executada |
| Armaduras | kg | Peso do quadro/resumo de aço da prancha |
| Concreto estrutural | m³ | Volume geométrico nominal das peças |
| Desforma/cura, quando EAP medir o serviço | m² / un | Área ou unidade liberada conforme projeto e controle de qualidade |
| Impermeabilização | m² | Superfícies especificadas, descontando encostos e interseções documentados |
| Drenagem perimetral | m | Extensão indicada em projeto específico |
| Reaterro compactado | m³ | Volume líquido após liberação da impermeabilização |
| Remoção de terra excedente | m³ | Volume de corte não aproveitado no reaterro |

## 4. EAP e portões

| Código | Serviço | Unidade |
|---|---|---:|
| 1.3.1 | Locação e gabarito topográfico | un / m² |
| 1.3.2 | Perfuração/cravação de estacas | m / un |
| 1.3.3 | Arrasamento/descabeçamento | un |
| 1.3.4 | Escavação de valas e cavas | m³ |
| 1.3.5 | Apiloamento de fundo | m² |
| 1.3.6 | Lastro ou regularização | m³ |
| 1.3.7 | Fôrmas de fundações | m² |
| 1.3.8 | Armaduras CA-50/CA-60 | kg |
| 1.3.9 | Concretagem estrutural | m³ |
| 1.3.10 | Desforma/cura, quando prevista | m² / un |
| 1.3.11 | Impermeabilização | m² |
| 1.3.12 | Drenagem perimetral, quando projetada | m |
| 1.3.13 | Reaterro compactado | m³ |
| 1.3.14 | Remoção de terra excedente | m³ |

O portão 1.3.11 bloqueia 1.3.13. A liberação depende de inspeção e evidência de impermeabilização conforme projeto.

## 5. Sequência executiva e interfaces

```text
Locação → escavação/perfuração → preparo do fundo → lastro
→ fôrmas → armaduras → concretagem → cura/desforma
→ impermeabilização → drenagem → reaterro → remoção de excedente
```

A sequência real deve respeitar o projeto, o plano de inspeção e os portões da EAP. Não usar prazos normativos como quantidade ou como substituto de evidência.

## 6. Fórmulas de cálculo

### 6.1 Sapata, pedestal e bloco prismático

```text
V_sapata = b_sapata × L_sapata × h_sapata
V_pedestal = b_pedestal × L_pedestal × h_pedestal
V_concreto = Σ volumes das partes comprovadas
A_fôrma_lateral = Σ (perímetro_de_contato × altura_da_parte)
```

### 6.2 Bloco de coroamento irregular

```text
A_seção = Σ áreas das figuras que compõem a seção em planta
V_bloco = A_seção × altura_do_bloco
A_fôrma = perímetro_externo_de_contato × altura_do_bloco
```

### 6.3 Baldrame ou cinta

```text
V_baldrame = Σ (largura_da_seção × altura_da_seção × comprimento_do_trecho)
A_fôrma = Σ (faces_de_contato × comprimento_do_trecho)
A_impermeabilização = Σ superfícies especificadas no detalhe
```

Trechos devem ser medidos face a face dos apoios quando o critério de interface estiver documentado, evitando duplicidade com pilares, pilaretes ou blocos.

### 6.4 Estaca ou broca

```text
H_estaca = cota_de_apoio − cota_de_topo_ou_arrasamento
V_estaca_unitária = π × (diâmetro / 2)² × H_estaca
V_estacas = V_estaca_unitária × quantidade
```

### 6.5 Radier e nervuras

```text
V_radier = área_projetada × espessura_nominal
V_nervuras = Σ (largura × altura × comprimento)
V_concreto_total = V_radier + V_nervuras + demais volumes desenhados
A_fôrma_lateral = perímetro_externo × espessura (quando aplicável)
```

### 6.6 Escavação, preparo, lastro e terra

```text
V_escavação = volume geométrico da cava ou vala conforme seção de projeto
A_apiloamento = área de fundo efetivamente preparada
V_lastro = área_base × espessura_nominal_de_projeto
V_reaterro = V_escavação − volumes enterrados comprovados
V_excedente = V_escavação − V_reaterro
```

Folgas, taludes, escoramentos e volumes auxiliares só entram quando dimensões e critérios estiverem expressos na prancha ou memorial.

### 6.7 Armaduras

```text
P_aço_elemento = peso indicado no quadro/resumo de aço da prancha
P_aço_total = Σ P_aço_elemento por elemento e bitola
```

## 7. Memória, evidência e auditoria

Cada item deve conter obra, prancha, revisão, página, elemento, dimensões transcritas, expressão literal, regra aplicada, resultado do motor, unidade e status (`VALIDADO`, `PENDENTE_RFI` ou `BLOQUEADO`).

Checklist:

- [ ] Todas as dimensões vieram de pranchas executivas.
- [ ] Nenhum valor de exemplo ou fallback foi utilizado.
- [ ] Nenhuma perda, empolamento ou consumível foi aplicado.
- [ ] Armaduras vieram do quadro/resumo de aço.
- [ ] Interfaces e descontos não duplicam elementos.
- [ ] Reaterro respeita o portão de impermeabilização.
- [ ] Cada resultado possui expressão, unidade e evidência.
