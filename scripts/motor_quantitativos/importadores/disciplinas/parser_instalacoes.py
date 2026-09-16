"""
Parser Especializado em Instalações Prediais (MEP)
Implementa as regras de SKILL_QUANT_04_ELETRICA e SKILL_QUANT_05_HIDRAULICA:
- Eletrodutos, fiação, quadros (QDC), SPDA
- Tubulações hidráulicas (água fria, água quente, esgoto, pluvial)
- Caixas de inspeção/passagem, prumadas
"""

from typing import Dict, List, Any
from motor_quantitativos.importadores.core.leitor_pdf_base import LeitorPDFBase


class ParserInstalacoes:
    def __init__(self, leitor_base: LeitorPDFBase):
        self.leitor = leitor_base
        self.caminho_pdf = leitor_base.caminho_pdf

    def extrair(self, incluir_correlatas: bool = True) -> Dict[str, Any]:
        """Extrai redes, circuitos e pontos de instalações."""
        return {
            "prancha_principal": self.caminho_pdf.name,
            "disciplina": "INSTALACOES",
            "redes": {},
            "pontos": {},
        }

    def gerar_itens_eap(self, dados: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Gera itens de EAP para instalações elétricas e hidráulicas."""
        return []
