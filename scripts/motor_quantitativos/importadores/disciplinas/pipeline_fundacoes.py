"""Pipeline do piloto de Fundação: evidência → elemento → regra → resultado."""

from collections.abc import Iterable

from motor_quantitativos.calculo.motor_regras import calcular_regra
from motor_quantitativos.domain.elementos import ElementRecord, QuantifiedItem


def quantificar_sapatas(elements: Iterable[ElementRecord]) -> list[QuantifiedItem]:
    saida: list[QuantifiedItem] = []
    for element in elements:
        if element.status != "LEVANTADO":
            continue
        result = calcular_regra("FUN.SAPATA_CONCRETO", {
            **element.attributes,
            "occurrence": element.occurrence,
        })
        saida.append(QuantifiedItem(
            cod_eap="1.3.9",
            description=f"Concretagem estrutural da sapata {element.element_id}",
            unit=result.unit,
            quantity_net=result.quantity_net,
            expression=result.expression,
            rule_id=result.rule_id,
            rule_version=result.rule_version,
            element_ids=(element.element_id,),
            evidence_ids=element.evidence_ids,
        ))
    return saida
