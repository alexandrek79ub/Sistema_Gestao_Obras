# SKILL QUANT 01 — FUNDAÇÕES

> Dependência: `SKILL_QUANTIFICACAO_MASTER.md`
> Papel desta skill: orientar a LLM multimodal sobre **o que ler no projeto** e **como medir** cada serviço de fundações.
> A LLM aplica os critérios visuais de medição e entrega inputs líquidos com evidência. O Python valida e faz somente a matemática final.

## 1. Separação de responsabilidades

```text
Skill:
define o que procurar -> define como medir -> define critérios anti-duplicidade

LLM multimodal:
PDF -> identifica elementos -> interpreta relações -> aplica critérios -> extrai inputs líquidos + evidências -> JSON

Python:
valida JSON -> aplica fórmula cadastrada -> gera expressão auditável -> SQLite
```

O Python não lê o PDF e não descobre interseções. Toda decisão que dependa da geometria visível da prancha deve ser resolvida pela LLM conforme esta skill antes da geração do JSON.

## 2. Regras invioláveis

- Toda dimensão, quantidade, cota e relação geométrica deve ter evidência de prancha, revisão e página.
- Ausência, conflito ou revisão indefinida gera `PENDENTE_RFI`; nunca usar fallback.
- Quantidades são físicas, líquidas e nominais: sem perdas, empolamento comercial ou coeficientes de consumo.
- Aço vem do quadro/resumo de armaduras; não estimar kg/m³.
- Folgas de escavação, taludes, escoramento, espessura de lastro e critérios de impermeabilização só entram quando comprovados no projeto/memorial.
- A LLM não envia quantidade final calculada nem expressão matemática.

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
- entregar ao JSON o `comprimento_liquido_m` já resultante desse critério, com evidência da região usada na leitura.

### 5.2 Baldrame × baldrame

Em encontros em T, cruzamentos ou nós:

- cada volume físico deve existir apenas uma vez;
- a viga secundária deve terminar na face da viga principal quando este for o critério geométrico do projeto;
- em cruzamentos onde ambas são contínuas, a LLM deve interpretar a região comum e produzir comprimentos/áreas líquidos sem duplicidade;
- se a prancha não permitir decidir o critério com segurança, gerar `PENDENTE_RFI`.

### 5.3 Cava de sapata × vala de baldrame

Para escavação, apiloamento, lastro, reaterro e bota-fora:

- nunca somar simplesmente todas as cavas + todas as valas quando elas se interceptam;
- a região comum entre cava e vala deve ser contabilizada uma única vez;
- a planta de locação/geometria é obrigatória para comprovar essas relações;
- a LLM deve entregar a `area_base_liquida_m2` ou `area_liquida_m2` já sem sobreposição, conforme a regra utilizada.

### 5.4 Vala de baldrame × vala de baldrame

- interseções de valas em T, L ou cruzamento não podem ser contadas duas vezes;
- a área/volume comum pertence ao conjunto escavado uma única vez;
- a LLM consolida visualmente a geometria e fornece o input líquido; o Python não reconstrói a planta.

## 6. Critérios por serviço

### Escavação
A LLM determina a área de base líquida do conjunto válido, sem sobreposição. O Python calcula `V_escavacao = area_base_liquida_m2 × profundidade_m`. Se houver profundidades diferentes, separar em medições distintas.

### Apiloamento / compactação de fundo
Usar `area_liquida_m2`: área efetivamente preparada, com interseções contadas uma vez.

### Lastro / concreto magro
Usar `area_base_liquida_m2 × espessura_m`. Não duplicar regiões compartilhadas entre cava e vala.

### Fôrmas
Somente faces com contato real de fôrma. Fundo apoiado no solo não recebe fôrma. Faces encostadas em outro elemento já executado não são duplicadas.

### Concreto estrutural
Para baldrames, usar `comprimento_liquido_m` conforme os encontros visíveis no projeto. Para elementos isolados, usar as dimensões nominais comprovadas.

### Impermeabilização
Usar `area_liquida_m2`: somente superfícies especificadas, sem faces de encosto ou áreas duplicadas.

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
        "comprimento_liquido_m": 3.80
      },
      "evidencias": {
        "largura_m": {"raw_text": "20", "region": "DET. VB"},
        "altura_m": {"raw_text": "40", "region": "DET. VB"},
        "comprimento_liquido_m": {"raw_text": "3,80 face a face", "region": "PLANTA ENTRE S01 E S02"}
      }
    }
  ]
}
```

## 8. Campos proibidos na saída da LLM

Nunca incluir:
- `quantidade_liquida`;
- `resultado`;
- `expressao_matematica`;
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

> Importante: quando existir interseção/nó, a LLM deve aplicar o critério visual da skill e entregar o input líquido. O Python não interpreta nem consolida geometria de PDF.

## 10. Pendências

Se a informação necessária para eliminar duplicidade não estiver disponível:

```text
PENDENTE_RFI — geometria insuficiente para definir o input líquido sem dupla contagem.
```

Não aceitar soma bruta nem pedir ao Python que descubra a geometria do PDF.
