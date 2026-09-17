"""Geração e avaliação determinística das regras de quantitativo."""

import re
from dataclasses import dataclass
from numbers import Real
from typing import Any, Mapping

from motor_quantitativos.calculo.avaliador_expressoes import calcular_expressao
from motor_quantitativos.regras.catalogo import RuleDefinition, get_rule


class CalculationBlockedError(ValueError):
    """Indica que o item precisa de RFI ou correção antes do cálculo."""


@dataclass(frozen=True)
class CalculationResult:
    rule_id: str
    rule_version: int
    expression: str
    quantity_net: float
    unit: str


_FIELD_PATTERN = re.compile(r"\b[a-zA-Z_]\w*\b")
_SAFE_CONSTANTS = {"pi"}


def _numeric_fields(rule: RuleDefinition) -> tuple[str, ...]:
    names = tuple(dict.fromkeys(_FIELD_PATTERN.findall(rule.expression_template)))
    return tuple(name for name in names if name not in _SAFE_CONSTANTS)


def gerar_expressao(rule: RuleDefinition, attributes: Mapping[str, Any]) -> str:
    missing = [field for field in rule.required_fields if field not in attributes or attributes[field] in (None, "")]
    if missing:
        raise CalculationBlockedError(f"Dados obrigatórios ausentes para {rule.rule_id}: {', '.join(missing)}")

    invalid = [field for field in _numeric_fields(rule) if field not in attributes]
    if invalid:
        raise CalculationBlockedError(f"Campos da fórmula não fornecidos para {rule.rule_id}: {', '.join(invalid)}")

    values: dict[str, str] = {}
    for field in _numeric_fields(rule):
        value = attributes[field]
        if not isinstance(value, Real) or isinstance(value, bool):
            raise CalculationBlockedError(f"Campo não numérico em {rule.rule_id}: {field}")
        if float(value) < 0:
            raise CalculationBlockedError(f"Campo negativo em {rule.rule_id}: {field}")
        values[field] = format(float(value), ".12g")

    expression = rule.expression_template
    for field in sorted(values, key=len, reverse=True):
        expression = re.sub(rf"\b{re.escape(field)}\b", values[field], expression)
    return expression


def calcular_regra(rule_id: str, attributes: Mapping[str, Any]) -> CalculationResult:
    rule = get_rule(rule_id)
    expression = gerar_expressao(rule, attributes)
    quantity = calcular_expressao(expression)
    if quantity < 0:
        raise CalculationBlockedError(f"Resultado negativo para {rule_id}")
    return CalculationResult(rule.rule_id, rule.version, expression, quantity, rule.unit)
