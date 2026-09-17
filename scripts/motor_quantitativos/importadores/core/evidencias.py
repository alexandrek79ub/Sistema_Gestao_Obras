"""Tipos de evidência produzidos pela leitura de documentos técnicos."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    source_file: str
    source_revision: str
    page: int
    region: str
    raw_text: str
    evidence_type: str
    confidence: str
    review_note: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
