"""
Módulo Core: Leitor Base de Pranchas e Documentos Técnicos em PDF
Responsável pelo baixo nível de abertura, normalização de rotação,
decodificação de caracteres CAD e extração de blocos e metadados.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import re

try:
    import fitz  # PyMuPDF
except ImportError:
    raise ImportError("PyMuPDF não instalado. Instale com: pip install pymupdf")


class LeitorPDFBase:
    def __init__(self, caminho_pdf: str | Path):
        self.caminho_pdf = Path(caminho_pdf).resolve()
        if not self.caminho_pdf.exists():
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {self.caminho_pdf}")
            
        self.doc = fitz.open(str(self.caminho_pdf))
        self.total_paginas = len(self.doc)

    def obter_linhas_texto(self, pagina_idx: int = 0) -> List[str]:
        """Extrai linhas limpas de texto da página."""
        if pagina_idx >= self.total_paginas:
            return []
        texto = self.doc[pagina_idx].get_text()
        return [linha.strip() for linha in texto.split("\n") if linha.strip()]

    def obter_texto_completo(self, pagina_idx: int = 0) -> str:
        """Extrai texto contínuo consolidado."""
        if pagina_idx >= self.total_paginas:
            return ""
        return self.doc[pagina_idx].get_text()

    def obter_blocos(self, pagina_idx: int = 0) -> List[Dict[str, Any]]:
        """Extrai blocos de texto com coordenadas espaciais."""
        if pagina_idx >= self.total_paginas:
            return []
        blocos = self.doc[pagina_idx].get_text("blocks")
        resultado = []
        for b in blocos:
            resultado.append({
                "x0": b[0], "y0": b[1], "x1": b[2], "y1": b[3],
                "texto": b[4].strip(),
                "linhas": [l.strip() for l in b[4].split("\n") if l.strip()]
            })
        return resultado

    def detectar_disciplina(self, pagina_idx: int = 0) -> str:
        """Identifica a disciplina provável pelo selo/carimbo e notas da prancha."""
        texto = self.obter_texto_completo(pagina_idx).upper()
        
        # Fundações / Infraestrutura
        if any(k in texto for k in ["BALDRAME", "SAPATA", "BLOCO DE COROAMENTO", "ESTACA", "FUNDAÇÃO", "FUNDACAO"]):
            return "FUNDACOES"
            
        # Estrutura / Superestrutura
        if any(k in texto for k in ["FORMA DO TÉRREO", "FORMA DO TIPO", "PLANTA DE FORMA", "VIGAS DO TETO", "PILARES"]):
            return "ESTRUTURA"
            
        # Arquitetura
        if any(k in texto for k in ["PLANTA BAIXA", "LAYOUT", "ALVENARIA", "ACABAMENTOS", "ESQUADRIAS", "CORTE AA", "FACHADA"]):
            return "ARQUITETURA"
            
        # Instalações
        if any(k in texto for k in ["DIAGRAMA UNIFILAR", "QDC", "ILUMINAÇÃO", "TOMADAS", "SPDA", "AGUA FRIA", "ESGOTO"]):
            return "INSTALACOES"
            
        return "GENERICA"

    def listar_pranchas_correlatas(self) -> List[Path]:
        """Localiza automaticamente pranchas da mesma série no mesmo diretório."""
        nome = self.caminho_pdf.name
        pasta = self.caminho_pdf.parent
        
        match = re.match(r"(.*?EGS-05)\d", nome)
        if match:
            prefixo = match.group(1)
            return sorted([p for p in pasta.glob(f"{prefixo}*.pdf") if p != self.caminho_pdf])
            
        match = re.match(r"(.*?EGS-)\d+", nome)
        if match:
            prefixo = match.group(1)
            return sorted([p for p in pasta.glob(f"{prefixo}*.pdf") if p != self.caminho_pdf])
            
        return []
