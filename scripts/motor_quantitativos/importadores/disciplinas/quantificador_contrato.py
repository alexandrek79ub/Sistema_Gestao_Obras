"""Liga elementos normalizados às regras por disciplina."""

from collections.abc import Iterable

from motor_quantitativos.calculo.motor_regras import calcular_regra
from motor_quantitativos.domain.elementos import ElementRecord, QuantifiedItem
from motor_quantitativos.regras import get_rule


_RULE_BY_TYPE = {
    ("ESTRUTURA", "PILAR"): "EST.PILAR_CONCRETO",
    ("ESTRUTURA", "VIGA"): "EST.VIGA_CONCRETO",
    ("ARQUITETURA", "PAREDE"): "ARQ.PAREDE_AREA_LIQUIDA",
    ("ELETRICA", "ELETRODUTO"): "ELEC.ELETRODUTO_COMPRIMENTO",
    ("HIDRAULICA", "TUBULACAO"): "HID.TUBULACAO_COMPRIMENTO",
    ("SERVICOS_ESPECIAIS", "SERVICO_AREA"): "ESP.SERVICO_AREA",
}


def quantificar_elementos(elements: Iterable[ElementRecord]) -> list[QuantifiedItem]:
    itens: list[QuantifiedItem] = []
    for element in elements:
        rule_id = _RULE_BY_TYPE.get((element.disciplina, element.element_type))
        if element.status != "LEVANTADO":
            raise ValueError(f"Elemento bloqueado para cálculo: {element.element_id} ({element.status})")
        if rule_id is None:
            raise ValueError(f"Sem regra contratual para {element.disciplina}/{element.element_type}: {element.element_id}")
        result = calcular_regra(rule_id, {**element.attributes, "occurrence": element.occurrence})
        rule = get_rule(rule_id)
        itens.append(QuantifiedItem(
            cod_eap=rule.cod_eap,
            description=rule.description,
            unit=result.unit, quantity_net=result.quantity_net, expression=result.expression,
            rule_id=result.rule_id, rule_version=result.rule_version,
            element_ids=(element.element_id,), evidence_ids=element.evidence_ids,
            cia=element.cia, element_type=element.element_type,
            source_file=element.source_file, source_revision=element.source_revision,
        ))
    return itens
