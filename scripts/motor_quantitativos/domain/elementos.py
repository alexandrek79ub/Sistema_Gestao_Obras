"""Modelos normalizados entre parser, catálogo e motor."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ElementRecord:
    obra_codigo: str
    pavimento: str
    unidade_setor: str
    ambiente: str
    cia: str
    disciplina: str
    element_type: str
    element_id: str
    occurrence: int
    attributes: dict[str, Any]
    evidence_ids: tuple[str, ...]
    status: str = "LEVANTADO"
    attribute_evidence: dict[str, tuple[str, ...]] = field(default_factory=dict)
    source_file: str = ""
    source_revision: str = ""


@dataclass(frozen=True)
class QuantifiedItem:
    cod_eap: str
    description: str
    unit: str
    quantity_net: float
    expression: str
    rule_id: str
    rule_version: int
    element_ids: tuple[str, ...] = field(default_factory=tuple)
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    status: str = "LEVANTADO"
    cia: str = ""
    element_type: str = ""
    source_file: str = ""
    source_revision: str = ""
