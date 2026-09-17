# Contrato de Dados de Engenharia — Quantitativos

## 1. Finalidade

Este contrato define a fronteira entre extração de pranchas, parsers de disciplina, catálogo de regras, motor de cálculo e SQLite. Ele representa somente quantitativo físico líquido de projeto. Preços, BDI, perdas, UCC, embalagens e insumos derivados ficam fora deste contrato.

## 2. Fluxo obrigatório

```text
PDF/CAD/BIM → EvidenceRecord → ElementRecord → CalculationRequest
           → CalculationResult → SQLite/artefatos derivados
```

O parser nunca grava preço, não escolhe regra por aproximação e não calcula resultado final.

## 3. EvidenceRecord

Cada valor usado em cálculo precisa de uma evidência:

| Campo | Obrigatório | Regra |
|---|---:|---|
| `source_file` | sim | Caminho relativo ou identificador do documento |
| `source_revision` | sim | Revisão da prancha/documento |
| `page` | sim | Página 1-based |
| `region` | sim | Coordenadas ou identificador de bloco/tabela |
| `raw_text` | sim | Transcrição original, sem normalização destrutiva |
| `evidence_type` | sim | `TEXT`, `TABLE`, `DIMENSION`, `CALLOUT`, `OCR`, `USER_CONFIRMED` |
| `confidence` | sim | `CONFIRMED`, `REVIEW_REQUIRED` ou `USER_CONFIRMED` |
| `review_note` | não | Justificativa de revisão/ambiguidade |

Sem evidência, o campo não pode alimentar uma expressão.

## 4. ElementRecord

Objeto normalizado produzido por um parser de disciplina:

```json
{
  "obra_codigo": "OBRA_EXEMPLO",
  "pavimento": "FUNDAÇÃO",
  "unidade_setor": "GERAL",
  "ambiente": "FUNDAÇÃO GERAL",
  "cia": "FUN-GER-S01",
  "disciplina": "FUNDACOES",
  "element_type": "SAPATA",
  "element_id": "S1",
  "occurrence": 11,
  "attributes": {
    "largura_m": 1.0,
    "comprimento_m": 1.0,
    "altura_m": 0.3
  },
  "attribute_evidence": {
    "occurrence": ["evidence-id-1"],
    "largura_m": ["evidence-id-2"],
    "comprimento_m": ["evidence-id-2"],
    "altura_m": ["evidence-id-2"]
  },
  "status": "LEVANTADO"
}
```

Regras:

- `occurrence` é contagem comprovada, não multiplicador arbitrário.
- `attributes` só contém dados extraídos/confirmados; não contém resultado derivado.
- Unidade original deve ser preservada em metadado quando houver conversão.
- `element_id` não substitui `cia` nem `cod_eap`.
- Campo obrigatório ausente gera `PENDENTE_RFI`, nunca valor padrão.

## 5. CalculationRequest

Gerado pelo catálogo de regras a partir de um ou mais `ElementRecord`:

| Campo | Obrigatório | Regra |
|---|---:|---|
| `rule_id` | sim | Identificador versionado da regra |
| `rule_version` | sim | Versão imutável usada no cálculo |
| `cod_eap` | sim | Serviço oficial da EAP |
| `service_description` | sim | Serviço executivo, não insumo |
| `unit` | sim | Unidade de saída (`m`, `m²`, `m³`, `kg`, `un`) |
| `expression_template` | sim | Fórmula auditável sem resultado embutido |
| `expression` | sim | Expressão literal com valores comprovados |
| `source_element_ids` | sim | Elementos que alimentaram a expressão |
| `evidence_ids` | sim | Evidências transitivas do cálculo |
| `status` | sim | `LEVANTADO` ou `PENDENTE_RFI` |

`expression` não pode conter preço, perda, empolamento, arredondamento comercial ou constante de obra não evidenciada.

## 6. CalculationResult

```json
{
  "quantity_net": 3.3,
  "unit": "m³",
  "precision": 4,
  "status": "CALCULADO",
  "calculated_at": "2026-09-17T00:00:00Z"
}
```

O resultado é produzido exclusivamente pelo avaliador determinístico. Se a expressão for inválida, houver unidade incompatível ou evidência insuficiente, o resultado deve ser `BLOCKED` e gerar RFI/erro auditável; nunca retornar zero silenciosamente.

## 7. RFIRecord

Campos mínimos: `rfi_id`, `obra_codigo`, `source_file`, `page`, `element_id`, `missing_fields`, `question`, `status`, `created_at`, `response_reference`.

Um item `PENDENTE_RFI` não pode alimentar orçamento aprovado, medição ou compra.

## 8. Persistência mínima no SQLite

O schema futuro deve preservar no item quantitativo: `obra_id`, `cia`, `element_type`, `element_id`, `cod_eap`, `rule_id`, `rule_version`, `quantity_net`, `unit`, `expression`, `status`, `rfi_id`, `evidence_json`, `source_revision` e `updated_at`.

Os artefatos CSV, Excel e Markdown são derivados desse registro e nunca são fonte editável.

## 9. Critérios de aceitação

- Um parser consegue produzir `ElementRecord` sem conhecer SQLite ou exportadores.
- Uma regra consegue consumir elementos de PDF, CAD, BIM ou entrada manual no mesmo formato.
- Todo resultado possui expressão, regra, unidade, elemento e evidência.
- Nenhuma camada aceita valor padrão silencioso.
- Quantitativo físico não contém preço, BDI, perda, UCC ou insumo derivado.
