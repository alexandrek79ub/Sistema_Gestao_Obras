"""Parsers textuais mínimos das disciplinas não-fundação.

Os padrões aceitam apenas cotas explícitas; ausência de correspondência não cria
elemento sintético.
"""

import re
from collections.abc import Iterable

from motor_quantitativos.domain.elementos import ElementRecord
from motor_quantitativos.importadores.core.evidencias import EvidenceRecord


def _m(value: str) -> float:
    return float(value.replace(",", ".")) / 100


def _record(obra: str, evidence: EvidenceRecord, tipo: str, ident: str, attrs: dict, disciplina: str) -> ElementRecord:
    return ElementRecord(obra, "NÃO_INFORMADO", "NÃO_INFORMADO", "NÃO_INFORMADO",
                         f"{disciplina[:3]}-GER-{ident}", disciplina, tipo, ident, 1, attrs,
                         (evidence.evidence_id,))


def extrair_estrutura(obra: str, evidence: Iterable[EvidenceRecord]) -> list[ElementRecord]:
    saida: list[ElementRecord] = []
    vistos: set[tuple[str, str]] = set()
    for item in evidence:
        texto = re.sub(r"\s+", " ", item.raw_text)
        for m in re.finditer(r"\b(P\w+)\s+(\d+[,.]?\d*)\s*[xX×]\s*(\d+[,.]?\d*)\s*cm\s+H\s*=\s*(\d+[,.]?\d*)\s*m", texto, re.I):
            ident = m.group(1).upper()
            if ("PILAR", ident) not in vistos:
                vistos.add(("PILAR", ident))
                saida.append(_record(obra, item, "PILAR", ident, {"largura_m": _m(m.group(2)), "profundidade_m": _m(m.group(3)), "altura_m": float(m.group(4).replace(',', '.'))}, "ESTRUTURA"))
        for m in re.finditer(r"\b(P\w+)\s+(\d+[,.]?\d*)\s*[xX×]\s*(\d+[,.]?\d*)\s*(?:cm)?\s+(-?\d+[,.]?\d*)\s+(\d+[,.]?\d*)", texto, re.I):
            ident = m.group(1).upper()
            if ("PILAR", ident) not in vistos:
                vistos.add(("PILAR", ident))
                altura = abs(float(m.group(5).replace(',', '.')) - float(m.group(4).replace(',', '.'))) / 100
                saida.append(_record(obra, item, "PILAR", ident, {"largura_m": _m(m.group(2)), "profundidade_m": _m(m.group(3)), "altura_m": altura}, "ESTRUTURA"))
        for m in re.finditer(r"\b(V\w+)\s+(\d+[,.]?\d*)\s*[xX×]\s*(\d+[,.]?\d*)\s*cm\s+L\s*=\s*(\d+[,.]?\d*)\s*m", item.raw_text, re.I):
            ident = m.group(1).upper()
            if ("VIGA", ident) not in vistos:
                vistos.add(("VIGA", ident))
                saida.append(_record(obra, item, "VIGA", ident, {"largura_m": _m(m.group(2)), "altura_m": _m(m.group(3)), "comprimento_livre_m": float(m.group(4).replace(',', '.'))}, "ESTRUTURA"))
    return saida


def extrair_instalacoes(obra: str, evidence: Iterable[EvidenceRecord]) -> list[ElementRecord]:
    saida: list[ElementRecord] = []
    for item in evidence:
        for m in re.finditer(r"\bELETRODUTO\s+(\w+)\s+L\s*=\s*(\d+[,.]?\d*)\s*m", item.raw_text, re.I):
            saida.append(_record(obra, item, "ELETRODUTO", m.group(1).upper(), {"comprimento_trecho_m": float(m.group(2).replace(',', '.'))}, "ELETRICA"))
        for m in re.finditer(r"\bTUBO\s+(\w+)\s+L\s*=\s*(\d+[,.]?\d*)\s*m", item.raw_text, re.I):
            saida.append(_record(obra, item, "TUBULACAO", m.group(1).upper(), {"comprimento_trecho_m": float(m.group(2).replace(',', '.'))}, "HIDRAULICA"))
    return saida


def extrair_arquitetura(obra: str, evidence: Iterable[EvidenceRecord]) -> list[ElementRecord]:
    saida: list[ElementRecord] = []
    for item in evidence:
        for m in re.finditer(r"\bPAREDE\s+(\w+)\s+P\s*=\s*(\d+[,.]?\d*)\s*m\s+H\s*=\s*(\d+[,.]?\d*)\s*m\s+V[AÃ]OS\s*=\s*(\d+[,.]?\d*)\s*m2", item.raw_text, re.I):
            saida.append(_record(obra, item, "PAREDE", m.group(1).upper(), {"perimetro_liquido_m": float(m.group(2).replace(',', '.')), "altura_m": float(m.group(3).replace(',', '.')), "desconto_vaos_m2": float(m.group(4).replace(',', '.'))}, "ARQUITETURA"))
    return saida


def extrair_servicos_especiais(obra: str, evidence: Iterable[EvidenceRecord]) -> list[ElementRecord]:
    saida: list[ElementRecord] = []
    for item in evidence:
        for m in re.finditer(r"\bAREA\s+(\w+)\s*=\s*(\d+[,.]?\d*)\s*m2", item.raw_text, re.I):
            saida.append(_record(obra, item, "SERVICO_AREA", m.group(1).upper(), {"area_projetada_m2": float(m.group(2).replace(',', '.'))}, "SERVICOS_ESPECIAIS"))
    return saida
