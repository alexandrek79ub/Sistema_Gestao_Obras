# SKILL QUANT 01 — FUNDAÇÕES (EXTRAÇÃO)

> Dependência: `SKILL_QUANTIFICACAO_MASTER.md`
> Papel desta skill: orientar a LLM a **ler a prancha e transcrever evidências**.
> O cálculo é responsabilidade exclusiva de `scripts/processar_prancha.py`.

## 1. Princípio

A LLM não calcula quantitativos. Ela apenas identifica:

- tipo do elemento;
- código/identificador do elemento;
- valores dimensionais explicitamente visíveis;
- quantidade/ocorrência explicitamente comprovada;
- revisão, página e região da evidência;
- regra de cálculo permitida que corresponde ao dado observado.

Se um campo obrigatório não estiver claramente comprovado, não invente, não estime e não use fallback. O item deve ficar fora do JSON de cálculo e ser reportado como pendência/RFI.

## 2. Formato de saída obrigatório

A saída para fundações deve seguir este formato:

```json
{
  "schema_version": 1,
  "disciplina": "FUNDACOES",
  "fonte": {
    "arquivo": "EGS-051.pdf",
    "revisao": "A",
    "pagina": 1
  },
  "medicoes": [
    {
      "elemento": "S01",
      "tipo_elemento": "SAPATA",
      "cia": "FUN-GER-S01",
      "regra_id": "FUN.SAPATA.CONCRETO.V1",
      "inputs": {
        "largura_m": 1.5,
        "comprimento_m": 1.8,
        "altura_m": 0.5,
        "quantidade": 4
      },
      "evidencias": {
        "largura_m": {"raw_text": "1,50", "region": "DETALHE S01"},
        "comprimento_m": {"raw_text": "1,80", "region": "DETALHE S01"},
        "altura_m": {"raw_text": "0,50", "region": "CORTE S01"},
        "quantidade": {"raw_text": "4x S01", "region": "PLANTA DE LOCAÇÃO"}
      }
    }
  ]
}
```

## 3. Campos proibidos na saída da LLM

Nunca incluir:

- `quantidade_liquida`
- `quantity_net`
- `resultado`
- `expressao_matematica`
- `expression`
- preço, BDI ou custo

O motor Python cria a expressão auditável e o resultado.

## 4. Regras disponíveis

Use somente uma das regras abaixo quando todos os inputs obrigatórios estiverem comprovados.

| regra_id | Elemento/serviço | Inputs obrigatórios |
|---|---|---|
| `FUN.SAPATA.CONCRETO.V1` | Concreto de sapata | `largura_m`, `comprimento_m`, `altura_m` |
| `FUN.SAPATA.FORMA.V1` | Fôrma lateral de sapata | `largura_m`, `comprimento_m`, `altura_m` |
| `FUN.PEDESTAL.CONCRETO.V1` | Concreto de pedestal | `largura_m`, `comprimento_m`, `altura_m` |
| `FUN.PEDESTAL.FORMA.V1` | Fôrma lateral de pedestal | `largura_m`, `comprimento_m`, `altura_m` |
| `FUN.BLOCO.CONCRETO.V1` | Concreto de bloco prismático | `largura_m`, `comprimento_m`, `altura_m` |
| `FUN.BLOCO.FORMA.V1` | Fôrma lateral de bloco prismático | `largura_m`, `comprimento_m`, `altura_m` |
| `FUN.BALDRAME.CONCRETO.V1` | Concreto de baldrame | `largura_m`, `altura_m`, `comprimento_m` |
| `FUN.BALDRAME.FORMA_2_FACES.V1` | Fôrma de baldrame apoiado no solo | `altura_m`, `comprimento_m` |
| `FUN.ESTACA.CONCRETO.V1` | Concreto de estaca circular | `diametro_m`, `comprimento_m` |
| `FUN.ESTACA.PERFURACAO.V1` | Perfuração/cravação | `comprimento_m` |
| `FUN.RADIER.CONCRETO.V1` | Concreto de radier | `area_m2`, `espessura_m` |
| `FUN.RADIER.FORMA.V1` | Fôrma de borda de radier | `perimetro_m`, `espessura_m` |
| `FUN.ARMADURA.PESO.V1` | Armadura | `peso_kg` |
| `FUN.LASTRO.VOLUME.V1` | Lastro/regularização | `area_base_m2`, `espessura_m` |
| `FUN.ESCAVACAO.RETANGULAR.V1` | Escavação retangular | `largura_m`, `comprimento_m`, `profundidade_m` |
| `FUN.APILOAMENTO.AREA.V1` | Apiloamento/preparo de fundo | `area_m2` |
| `FUN.IMPERMEABILIZACAO.AREA.V1` | Impermeabilização | `area_m2` |
| `FUN.DRENAGEM.COMPRIMENTO.V1` | Drenagem perimetral | `comprimento_m` |

`quantidade` é opcional e, quando omitida, o motor assume 1 ocorrência. Se informada, também exige evidência.

## 5. Regras de leitura

- Preserve a unidade observada e converta para SI apenas quando a conversão for inequívoca.
- Cada input usado deve possuir `raw_text` e `region`.
- Armadura só pode usar `FUN.ARMADURA.PESO.V1` quando o peso estiver explicitamente indicado em quadro/resumo ou documento equivalente.
- Não estimar aço por kg/m³.
- Não inventar folga de escavação, espessura de lastro, talude ou empolamento.
- Movimentação de terra exige planta/geometry de locação suficiente para evitar sobreposição entre cavas e valas.
- Uma prancha de detalhe isolado não deve originar escavação, reaterro ou bota-fora sem a geometria de implantação correspondente.
- Baldrames devem usar comprimentos comprovados; não atravesse apoios por suposição.
- Para geometrias não suportadas pelas regras acima, interrompa e solicite nova regra Python. Não improvise fórmula.

## 6. Pendências

Quando faltar informação necessária, responda de forma explícita, por exemplo:

```text
PENDENTE_RFI — S01: altura da sapata não está legível na prancha.
```

Não produza medição parcial calculável para esse serviço.

## 7. Responsabilidades

```text
LLM:
PDF -> elementos -> inputs -> evidências -> regra_id

Python:
validação -> expressão -> cálculo -> SQLite -> CSV/Markdown
```

Esta separação é obrigatória.
