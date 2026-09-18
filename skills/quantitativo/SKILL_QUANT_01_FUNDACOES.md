# SKILL QUANT 01 — FUNDAÇÕES

> Dependência: `SKILL_QUANTIFICACAO_MASTER.md`
> Papel desta skill: definir **o que a LLM deve extrair** e os **critérios de medição** que o motor Python deve aplicar.
> A LLM não calcula resultado final nem cria expressão matemática.

## 1. Separação de responsabilidades

```text
LLM:
PDF -> identifica elemento -> transcreve dimensões -> registra evidências -> informa relações geométricas

Python:
valida -> aplica critérios de medição -> desconta interfaces/interseções -> calcula -> SQLite
```

A simplificação do pipeline não elimina critérios de engenharia. Ela apenas tira esses critérios da execução mental da LLM.

## 2. Regras invioláveis

- Toda dimensão, quantidade, cota e relação geométrica deve ter evidência de prancha, revisão e página.
- Ausência, conflito ou revisão indefinida gera `PENDENTE_RFI`; nunca usar fallback.
- Quantidades são físicas, líquidas e nominais: sem perdas, empolamento comercial ou coeficientes de consumo.
- Aço vem do quadro/resumo de armaduras; não estimar kg/m³.
- Folgas de escavação, taludes, escoramento, espessura de lastro e critérios de impermeabilização só entram quando comprovados no projeto/memorial.
- Geometria não suportada pelo motor deve bloquear o cálculo; a LLM não improvisa fórmula.

## 3. Tipologia de prancha

### Detalhes estruturais
Podem alimentar:
- concreto estrutural;
- fôrmas;
- armaduras;
- dimensões de sapatas, blocos, pedestais, estacas e baldrames.

### Planta de locação / geometria / terraplenagem
É necessária para:
- escavação de cavas e valas;
- apiloamento/compactação do fundo;
- lastro/regularização;
- reaterro;
- remoção/bota-fora;
- análise de interseções entre cavas, valas e elementos.

É proibido quantificar movimentação de terra apenas a partir de um detalhe isolado.

## 4. Critérios oficiais de medição

| Serviço | Unidade | Critério físico líquido |
|---|---:|---|
| Locação/gabarito | un / m² | Eixos/área efetivamente locados |
| Perfuração/cravação | m / un | Comprimento nominal/unidades indicadas |
| Arrasamento | un | Unidades indicadas |
| Escavação | m³ | Volume geométrico líquido das cavas/valas, sem dupla contagem de interseções |
| Apiloamento | m² | Área líquida de fundo preparada, sem sobreposição |
| Lastro/magro | m³ | Área líquida da base × espessura nominal |
| Fôrmas | m² | Área real de contato executada |
| Armaduras | kg | Peso indicado no quadro/resumo |
| Concreto | m³ | Volume geométrico líquido dos elementos |
| Impermeabilização | m² | Superfícies especificadas, descontando encostos/interseções |
| Drenagem | m | Extensão efetivamente projetada |
| Reaterro | m³ | Escavação líquida menos volumes enterrados comprovados |
| Bota-fora | m³ | Escavação líquida menos material reaproveitado no reaterro |

## 5. Regra central anti-duplicidade

### 5.1 Baldrame × sapata/bloco/pedestal

Quando um baldrame encontra uma sapata, bloco, pedestal ou pilarete já quantificado:

- medir o baldrame **face a face** do apoio;
- não prolongar o volume da viga através do apoio;
- o mesmo critério vale para fôrma e impermeabilização quando as superfícies de contato já pertencem ao apoio;
- registrar no JSON qual elemento está no início/fim do trecho e a dimensão do apoio necessária para o desconto.

### 5.2 Baldrame × baldrame

Em encontros em T, cruzamentos ou nós:

- cada volume físico deve existir apenas uma vez;
- a viga secundária deve terminar na face da viga principal quando este for o critério geométrico do projeto;
- em cruzamentos onde ambas são contínuas, o motor deve descontar a região comum uma única vez;
- a LLM deve extrair a geometria do nó, mas não calcular o desconto.

### 5.3 Cava de sapata × vala de baldrame

Para escavação, apiloamento, lastro, reaterro e bota-fora:

- nunca somar simplesmente todas as cavas + todas as valas quando elas se interceptam;
- a região comum entre cava e vala deve ser contabilizada uma única vez;
- a planta de locação/geometria é obrigatória para comprovar essas relações;
- o JSON deve identificar as relações/interseções observadas para o motor consolidar o volume líquido.

### 5.4 Vala de baldrame × vala de baldrame

- interseções de valas em T, L ou cruzamento não podem ser contadas duas vezes;
- a área/volume comum pertence ao conjunto escavado uma única vez;
- o cálculo deve ser consolidado pelo motor, não por soma independente dos trechos.

## 6. Critérios por serviço

### Escavação
`V_escavacao` é o volume geométrico líquido da união das cavas e valas válidas do conjunto. Folgas somente quando explicitamente projetadas.

### Apiloamento / compactação de fundo
Área líquida efetivamente preparada. Interseções de fundos de valas/cavas contam uma vez.

### Lastro / concreto magro
Área líquida de base × espessura indicada. Não duplicar lastro onde cava e vala compartilham a mesma região.

### Fôrmas
Somente faces com contato real de fôrma. Fundo apoiado no solo não recebe fôrma. Faces encostadas em outro elemento já executado não são duplicadas.

### Concreto estrutural
Somar volumes líquidos dos elementos. Interfaces devem obedecer ao critério face-a-face ou desconto de região comum definido pelo projeto.

### Impermeabilização
Somente superfícies especificadas. Descontar faces de encosto e áreas de interseção já pertencentes a outro elemento.

### Reaterro
```text
V_reaterro = V_escavacao_liquida - volumes_enterrados_comprovados
```

Os volumes enterrados podem incluir concreto estrutural, lastro e outros elementos permanentes explicitamente comprovados.

### Bota-fora / excedente
```text
V_excedente_nominal = V_escavacao_liquida - V_reaterro
```

Empolamento não pertence ao quantitativo físico líquido; se necessário para logística/orçamento, é aplicado em camada posterior.

## 7. Formato de saída da LLM

A LLM envia dados e relações, nunca resultados:

```json
{
  "schema_version": 1,
  "disciplina": "FUNDACOES",
  "fonte": {
    "arquivo": "EGS-051.pdf",
    "revisao": "A",
    "pagina": 1,
    "tipo_prancha": "LOCACAO_GEOMETRIA"
  },
  "medicoes": [
    {
      "elemento": "VB01",
      "tipo_elemento": "BALDRAME",
      "regra_id": "FUN.BALDRAME.CONCRETO.V1",
      "inputs": {
        "largura_m": 0.20,
        "altura_m": 0.40,
        "comprimento_m": 3.80
      },
      "interfaces": {
        "inicio": {"elemento": "S01", "tipo": "SAPATA"},
        "fim": {"elemento": "S02", "tipo": "SAPATA"}
      },
      "evidencias": {
        "largura_m": {"raw_text": "20", "region": "DET. VB"},
        "altura_m": {"raw_text": "40", "region": "DET. VB"},
        "comprimento_m": {"raw_text": "3,80", "region": "PLANTA"}
      }
    }
  ],
  "intersecoes": [
    {
      "elemento_a": "VALA_VB01",
      "elemento_b": "CAVA_S01",
      "tipo": "ESCAVACAO",
      "evidencia": {"raw_text": "interseção visível em planta", "region": "EIXO A/1"}
    }
  ]
}
```

## 8. Campos proibidos na saída da LLM

Nunca incluir:
- `quantidade_liquida`;
- `resultado`;
- `expressao_matematica`;
- volume de interseção calculado;
- preço, BDI ou custo.

## 9. Regras disponíveis no motor atual

| regra_id | Serviço |
|---|---|
| `FUN.SAPATA.CONCRETO.V1` | Concreto de sapata |
| `FUN.SAPATA.FORMA.V1` | Fôrma de sapata |
| `FUN.PEDESTAL.CONCRETO.V1` | Concreto de pedestal |
| `FUN.PEDESTAL.FORMA.V1` | Fôrma de pedestal |
| `FUN.BLOCO.CONCRETO.V1` | Concreto de bloco prismático |
| `FUN.BLOCO.FORMA.V1` | Fôrma de bloco |
| `FUN.BALDRAME.CONCRETO.V1` | Concreto de baldrame |
| `FUN.BALDRAME.FORMA_2_FACES.V1` | Fôrma de baldrame |
| `FUN.ESTACA.CONCRETO.V1` | Concreto de estaca |
| `FUN.ESTACA.PERFURACAO.V1` | Perfuração/cravação |
| `FUN.RADIER.CONCRETO.V1` | Concreto de radier |
| `FUN.RADIER.FORMA.V1` | Fôrma de radier |
| `FUN.ARMADURA.PESO.V1` | Armadura por peso comprovado |
| `FUN.LASTRO.VOLUME.V1` | Lastro/regularização |
| `FUN.ESCAVACAO.RETANGULAR.V1` | Escavação retangular simples |
| `FUN.APILOAMENTO.AREA.V1` | Apiloamento |
| `FUN.IMPERMEABILIZACAO.AREA.V1` | Impermeabilização |
| `FUN.DRENAGEM.COMPRIMENTO.V1` | Drenagem |

> Importante: as regras simples acima **não autorizam** ignorar interfaces. Quando existir interseção/nó, o motor deve usar uma regra de consolidação apropriada ou bloquear até ela existir.

## 10. Pendências

Se a informação necessária para eliminar duplicidade não estiver disponível:

```text
PENDENTE_RFI — geometria de interface insuficiente para calcular o volume líquido sem dupla contagem.
```

Não aceitar uma soma bruta como resultado final.
