# SKILL QUANT 03A — ALVENARIA, VEDAÇÃO E REVESTIMENTOS INTERNOS

> Parte de: `SKILL_QUANT_03_ARQUITETURA.md`
> Dependência: `SKILL_QUANTIFICACAO_MASTER.md`
> Referência: NBR 12721, conforme edição aplicável à obra.

## Limites obrigatórios

- Levantar exclusivamente serviços físicos líquidos comprovados nas pranchas.
- Não aplicar perdas, consumo de materiais, SKUs, embalagens, UCC ou coeficientes de compra.
- Sem cota, detalhe, paginação ou especificação: `PENDENTE_RFI`; nunca estimar.
- Parede, revestimento, piso, teto, pintura e drywall são serviços distintos, com memórias próprias.

## 1. Alvenaria e vedação

### 1.1 Paredes regulares, pilares e divisórias

```text
P_perímetro_externo = soma dos trechos externos indicados
P_paredes_líquido = P_perímetro_externo − Σ larguras de pilares + Σ comprimentos de divisórias
A_bruta = P_paredes_líquido × altura_do_trecho
A_líquida = A_bruta − Σ descontos de vãos aplicáveis
```

Em nós em L, T ou X, medir cada trecho entre faces acabadas ou faces estruturais indicadas. Nunca medir de eixo a eixo quando isso gerar sobreposição de alvenaria.

### 1.2 Geometrias especiais

```text
A_parede_irregular = Σ (comprimento_do_trecho × altura_correspondente)
A_fachada = Σ áreas dos planos externos − Σ vãos
H_alvenaria_platibanda = altura_total_platibanda − altura_da_viga_invertida
A_platibanda = perímetro_líquido × H_alvenaria_platibanda
A_muretas = Σ (comprimento_do_vão × altura_da_mureta)
```

Para parede sob forro, usar a altura executiva indicada no corte. Para forro rebaixado, revestimento e pintura só incluem a face visível especificada em projeto.

### 1.3 Vãos, nichos e aberturas

Aplicar o critério de desconto da NBR 12721 e da contratação da obra ao serviço correspondente. Registrar em memória, para cada vão: código, largura, altura, área, regra aplicada e desconto resultante.

```text
A_vão = largura × altura
A_descontos = Σ desconto_conforme_critério(A_vão, tipo_de_serviço)
```

Nichos, armários embutidos, shafts e aberturas sem execução devem ser descontados quando o projeto e o critério de medição assim determinarem.

## 2. Revestimentos de parede

```text
A_face = comprimento_da_face × altura_revestida
A_revestida = Σ A_face − Σ vãos e áreas não revestidas
```

Chapisco, emboço, reboco, gesso, cerâmica e pintura são linhas separadas somente quando especificados. Em paredes com materiais diferentes, dividir a área por faixa, face ou ambiente conforme o detalhe arquitetônico.

## 3. Pisos, contrapisos e rodapés

```text
A_piso_bruta = decomposição geométrica do ambiente
A_piso_líquida = A_piso_bruta − pilares embutidos − vazios − bases não revestidas
L_rodapé_líquido = perímetro_revestido − vãos sem rodapé
```

Ambientes irregulares devem ser decompostos em retângulos, triângulos ou polígonos identificados na memória. Contrapiso, regularização, impermeabilização e revestimento final são serviços independentes.

## 4. Tetos, forros e drywall

```text
A_teto_bruta = área geométrica da projeção
A_teto_líquida = A_teto_bruta − alçapões − shafts − aberturas não executadas
A_parede_drywall = comprimento × altura_executiva
A_forro_drywall = área de projeção efetivamente forrada
```

Em drywall, registrar separadamente parede simples, dupla, resistente à umidade, resistente ao fogo, isolamento e forro somente quando cada sistema estiver identificado em projeto. Chapas, perfis, parafusos, fitas e massa são composição/BOM, não quantitativo físico.

## 5. Pintura e textura

```text
A_pintura = Σ superfícies especificadas − Σ áreas excluídas
```

Separar paredes internas, paredes externas, tetos, platibandas, esquadrias e elementos metálicos conforme acabamento e faces efetivamente pintadas. O número de demãos não multiplica a área física da EAP.

## 6. Evidência e decisão

Cada item deve preservar prancha, revisão, página, ambiente, elemento, dimensões transcritas, expressão literal, unidade e status.

| Pedido | Método |
|---|---|
| Alvenaria de ambiente | Trechos de parede + altura + vãos + nós estruturais |
| Revestimento de banheiro | Faces revestidas + faixas + vãos + detalhes de acabamento |
| Piso irregular | Decomposição geométrica do ambiente |
| Platibanda ou mureta | Trecho a trecho conforme corte/elevação |
| Drywall | Área executiva por sistema indicado |

Checklist:

- [ ] Plantas, cortes, elevações e detalhes foram confrontados.
- [ ] Nós, pilares, vãos, nichos e shafts não geram duplicidade.
- [ ] Nenhuma perda, SKU, insumo ou embalagem foi incluída.
- [ ] Cada linha possui evidência, expressão, unidade e RFI quando necessário.
