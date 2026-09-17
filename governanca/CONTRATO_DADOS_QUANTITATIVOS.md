# Contrato mínimo de dados — Quantitativos de fundações

## Objetivo

Manter uma única fronteira entre LLM e código:

```text
PDF -> LLM -> evidencias.json -> processar_prancha.py -> SQLite -> CSV/Markdown
```

A LLM extrai. O Python valida e calcula.

## JSON aceito

```json
{
  "schema_version": 1,
  "disciplina": "FUNDACOES",
  "fonte": {
    "arquivo": "F-01.pdf",
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
        "quantidade": {"raw_text": "4x S01", "region": "PLANTA"}
      }
    }
  ]
}
```

## Regras

1. Cada input obrigatório deve possuir evidência.
2. `raw_text` preserva o que foi lido; `region` indica onde foi lido.
3. A LLM não pode enviar:
   - `quantidade_liquida`
   - `quantity_net`
   - `resultado`
   - `expressao_matematica`
   - `expression`
   - preço, BDI ou custo.
4. A LLM só pode usar `regra_id` cadastrada no motor.
5. Campo ausente ou ambíguo não recebe fallback. O processamento deve ser bloqueado e a pendência deve virar RFI.
6. O Python produz:
   - expressão auditável;
   - quantidade líquida;
   - EAP;
   - unidade;
   - status;
   - persistência no SQLite.
7. Erro nunca vira quantidade zero silenciosamente.
8. SQLite é a fonte de verdade. CSV e Markdown são somente exportações.

## Responsabilidade das camadas

| Camada | Responsabilidade |
|---|---|
| Skill | dizer à LLM o que procurar e quais `regra_id` existem |
| LLM | transcrever inputs e evidências |
| `processar_prancha.py` | validar, calcular e persistir |
| SQLite | armazenar resultado oficial |
| CSV/Markdown | apresentar resultados |

Não criar novas camadas sem necessidade comprovada.
