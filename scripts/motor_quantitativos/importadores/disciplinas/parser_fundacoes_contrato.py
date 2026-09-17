"""Parser de Fundação orientado ao contrato de dados.

Reconhece somente dimensões que estejam explicitamente no texto da evidência.
Não possui dimensões padrão, preços, EAP calculada por fallback ou resultados.
"""

import re
from typing import Iterable

from motor_quantitativos.domain.elementos import ElementRecord
from motor_quantitativos.importadores.core.evidencias import EvidenceRecord


_SAPATA = re.compile(
    r"(?P<occurrence>\d+)\s*[xX×]\s*(?P<element_id>S[A-Za-z0-9_-]+)"
    r"\s*\(?\s*(?P<b>[\d.,]+)\s*[xX×]\s*(?P<l>[\d.,]+)\s*[xX×]\s*(?P<h>[\d.,]+)\s*cm\s*\)?",
    re.IGNORECASE,
)


def _number(value: str) -> float:
    return float(value.replace(",", ".")) / 100


class ParserFundacoesContrato:
    def __init__(self, obra_codigo: str, evidence: Iterable[EvidenceRecord]):
        self.obra_codigo = obra_codigo
        self.evidence = tuple(evidence)

    def extrair_sapatas(self) -> list[ElementRecord]:
        elementos: list[ElementRecord] = []
        for item in self.evidence:
            for match in _SAPATA.finditer(item.raw_text):
                elementos.append(ElementRecord(
                    obra_codigo=self.obra_codigo,
                    pavimento="FUNDAÇÃO",
                    unidade_setor="GERAL",
                    ambiente="FUNDAÇÃO GERAL",
                    cia=f"FUN-GER-{match.group('element_id').upper()}",
                    disciplina="FUNDACOES",
                    element_type="SAPATA",
                    element_id=match.group("element_id").upper(),
                    occurrence=int(match.group("occurrence")),
                    attributes={
                        "largura_m": _number(match.group("b")),
                        "comprimento_m": _number(match.group("l")),
                        "altura_m": _number(match.group("h")),
                    },
                    evidence_ids=(item.evidence_id,),
                ))
        return elementos
