"""Valida a saída de parsers de disciplina antes do motor."""

from collections.abc import Iterable
from typing import Any

from motor_quantitativos.domain.elementos import ElementRecord


def validar_elementos(elements: Iterable[ElementRecord]) -> list[ElementRecord]:
    validos: list[ElementRecord] = []
    for element in elements:
        if element.status not in {"LEVANTADO", "PENDENTE_RFI", "NAO_LEVANTADO"}:
            raise ValueError(f"STATUS inválido no elemento {element.element_id}")
        if not element.cia or not element.element_id or not element.disciplina:
            raise ValueError(f"Identidade incompleta no elemento {element.element_id!r}")
        if element.status == "LEVANTADO" and not element.evidence_ids:
            raise ValueError(f"Elemento levantado sem evidência: {element.element_id}")
        if element.status == "LEVANTADO":
            missing_evidence = [field for field in element.attributes if not element.attribute_evidence.get(field)]
            if missing_evidence:
                raise ValueError(f"Atributos sem evidência no elemento {element.element_id}: {', '.join(missing_evidence)}")
        if element.occurrence < 0:
            raise ValueError(f"Ocorrência negativa: {element.element_id}")
        validos.append(element)
    return validos
