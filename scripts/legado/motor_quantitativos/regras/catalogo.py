"""Registro único das regras executáveis do quantitativo.

Este módulo descreve regras; não extrai PDF, não acessa SQLite e não avalia
expressões. A avaliação pertence ao motor de cálculo da fase seguinte.
"""

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class RuleDefinition:
    rule_id: str
    version: int
    discipline: str
    cod_eap: str
    description: str
    unit: str
    required_fields: tuple[str, ...]
    expression_template: str
    source_skill: str


_RULES: Mapping[str, RuleDefinition] = {
    "FUN.ESCAVACAO_CAVA": RuleDefinition(
        "FUN.ESCAVACAO_CAVA", 1, "FUNDACOES", "1.3.4", "Escavação de cavas e valas", "m³",
        ("occurrence", "largura_m", "comprimento_m", "folga_lateral_m", "profundidade_escavacao_m"),
        "occurrence * (largura_m + 2 * folga_lateral_m) * (comprimento_m + 2 * folga_lateral_m) * profundidade_escavacao_m",
        "SKILL_QUANT_01_FUNDACOES §1 e §4.1",
    ),
    "FUN.APILOAMENTO_CAVA": RuleDefinition(
        "FUN.APILOAMENTO_CAVA", 1, "FUNDACOES", "1.3.5", "Apiloamento de fundo de cava", "m²",
        ("occurrence", "largura_m", "comprimento_m", "folga_lateral_m"),
        "occurrence * (largura_m + 2 * folga_lateral_m) * (comprimento_m + 2 * folga_lateral_m)",
        "SKILL_QUANT_01_FUNDACOES §1 e §4.1",
    ),
    "FUN.LASTRO": RuleDefinition(
        "FUN.LASTRO", 1, "FUNDACOES", "1.3.6", "Lastro de concreto magro ou regularização", "m³",
        ("occurrence", "largura_m", "comprimento_m", "folga_lateral_m", "espessura_lastro_m"),
        "occurrence * (largura_m + 2 * folga_lateral_m) * (comprimento_m + 2 * folga_lateral_m) * espessura_lastro_m",
        "SKILL_QUANT_01_FUNDACOES §1 e §4.2",
    ),
    "FUN.SAPATA_CONCRETO": RuleDefinition(
        "FUN.SAPATA_CONCRETO", 1, "FUNDACOES", "1.3.9", "Concretagem estrutural de sapatas", "m³",
        ("occurrence", "largura_m", "comprimento_m", "altura_m"),
        "occurrence * largura_m * comprimento_m * altura_m",
        "SKILL_QUANT_01_FUNDACOES §2.1",
    ),
    "FUN.SAPATA_FORMA": RuleDefinition(
        "FUN.SAPATA_FORMA", 1, "FUNDACOES", "1.3.7", "Fôrma lateral de sapatas", "m²",
        ("occurrence", "largura_m", "comprimento_m", "altura_m"),
        "occurrence * 2 * (largura_m + comprimento_m) * altura_m",
        "SKILL_QUANT_01_FUNDACOES §2.1",
    ),
    "FUN.ESTACA_CONCRETO": RuleDefinition(
        "FUN.ESTACA_CONCRETO", 1, "FUNDACOES", "1.3.9", "Concreto do fuste de estacas", "m³",
        ("occurrence", "diametro_m", "comprimento_util_m"),
        "occurrence * pi * (diametro_m / 2) ** 2 * comprimento_util_m",
        "SKILL_QUANT_01_FUNDACOES §2.4",
    ),
    "FUN.RADIER_CONCRETO": RuleDefinition(
        "FUN.RADIER_CONCRETO", 1, "FUNDACOES", "1.3.9", "Concretagem de radier", "m³",
        ("occurrence", "area_projetada_m2", "espessura_radier_m"),
        "occurrence * area_projetada_m2 * espessura_radier_m",
        "SKILL_QUANT_01_FUNDACOES §2.5",
    ),
    "EST.PILAR_CONCRETO": RuleDefinition(
        "EST.PILAR_CONCRETO", 1, "ESTRUTURA", "1.4.3", "Concretagem de pilares", "m³",
        ("occurrence", "largura_m", "profundidade_m", "altura_m"),
        "occurrence * largura_m * profundidade_m * altura_m",
        "SKILL_QUANT_02_ESTRUTURA §1.1",
    ),
    "EST.VIGA_CONCRETO": RuleDefinition(
        "EST.VIGA_CONCRETO", 1, "ESTRUTURA", "1.4.8", "Concretagem de vigas", "m³",
        ("occurrence", "largura_m", "altura_m", "comprimento_livre_m"),
        "occurrence * largura_m * altura_m * comprimento_livre_m",
        "SKILL_QUANT_02_ESTRUTURA §1.2",
    ),
    "ARQ.PAREDE_AREA_LIQUIDA": RuleDefinition(
        "ARQ.PAREDE_AREA_LIQUIDA", 1, "ARQUITETURA", "2.1.2", "Área líquida de parede", "m²",
        ("perimetro_liquido_m", "altura_m", "desconto_vaos_m2"),
        "perimetro_liquido_m * altura_m - desconto_vaos_m2",
        "SKILL_QUANT_03A_ALVENARIA_E_VEDACAO §1.1",
    ),
    "ARQ.PISO_AREA_LIQUIDA": RuleDefinition(
        "ARQ.PISO_AREA_LIQUIDA", 1, "ARQUITETURA", "2.2.1", "Área líquida de piso", "m²",
        ("area_bruta_m2", "descontos_m2"),
        "area_bruta_m2 - descontos_m2",
        "SKILL_QUANT_03A_ALVENARIA_E_VEDACAO §2",
    ),
    "ELEC.ELETRODUTO_COMPRIMENTO": RuleDefinition(
        "ELEC.ELETRODUTO_COMPRIMENTO", 1, "ELETRICA", "3.1.2", "Eletroduto de projeto", "m",
        ("comprimento_trecho_m",),
        "comprimento_trecho_m",
        "SKILL_QUANT_04_ELETRICA §1",
    ),
    "HID.TUBULACAO_COMPRIMENTO": RuleDefinition(
        "HID.TUBULACAO_COMPRIMENTO", 1, "HIDRAULICA", "3.2.5", "Tubulação hidráulica de projeto", "m",
        ("comprimento_trecho_m",),
        "comprimento_trecho_m",
        "SKILL_QUANT_05_HIDRAULICA §2",
    ),
    "ESP.SERVICO_AREA": RuleDefinition(
        "ESP.SERVICO_AREA", 1, "SERVICOS_ESPECIAIS", "4.2", "Serviço especial por área de projeto", "m²",
        ("area_projetada_m2",),
        "area_projetada_m2",
        "SKILL_QUANT_06_SERVICOS_ESPECIAIS §1",
    ),
}


def get_rule(rule_id: str) -> RuleDefinition:
    try:
        return _RULES[rule_id]
    except KeyError as exc:
        raise KeyError(f"Regra de quantitativo não cadastrada: {rule_id}") from exc


def list_rules(discipline: str | None = None) -> tuple[RuleDefinition, ...]:
    rules = tuple(_RULES.values())
    if discipline is None:
        return rules
    return tuple(rule for rule in rules if rule.discipline == discipline.upper())
