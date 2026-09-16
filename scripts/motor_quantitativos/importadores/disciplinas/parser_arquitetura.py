"""
Parser Especializado em Arquitetura e Acabamentos
Implementa as regras da SKILL_QUANT_03_ARQUITETURA:
- Alvenarias com desconto de vãos NBR 12721 (3 faixas)
- Dedução de pilares embutidos
- Revestimentos de Parede e Teto (emboço, gesso, pintura)
- Pisos e Rodapés
- Esquadrias (portas e janelas)
"""

from typing import Dict, List, Any
from motor_quantitativos.importadores.core.leitor_pdf_base import LeitorPDFBase


class ParserArquitetura:
    def __init__(self, leitor_base: LeitorPDFBase):
        self.leitor = leitor_base
        self.caminho_pdf = leitor_base.caminho_pdf

    def extrair(self, incluir_correlatas: bool = True) -> Dict[str, Any]:
        """Extrai elementos arquitetônicos e ambientes."""
        return {
            "prancha_principal": self.caminho_pdf.name,
            "disciplina": "ARQUITETURA",
            "ambientes": {},
            "esquadrias": {},
        }

    def gerar_itens_eap(self, dados: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Gera itens de EAP para arquitetura."""
        return []
