"""
Roteador de Extração e Ingestão Automatizada de Pranchas
Identifica a disciplina da prancha (Fundações, Estrutura, Arquitetura, etc.)
e delega para o parser especializado correspondente.
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Garante acesso ao pacote motor_quantitativos
diretorio_scripts = Path(__file__).resolve().parent.parent.parent
if str(diretorio_scripts) not in sys.path:
    sys.path.insert(0, str(diretorio_scripts))

from motor_quantitativos.importadores.core.leitor_pdf_base import LeitorPDFBase
from motor_quantitativos.importadores.disciplinas import (
    ParserFundacoes, ParserEstrutura, ParserArquitetura, ParserInstalacoes
)
from motor_quantitativos.importadores.pdf_json_importer import importar_json_inicial


def processar_prancha(caminho_pdf: str | Path,
                      disciplina_forcada: Optional[str] = None,
                      db_path: str = "data/pmo_virtual.sqlite",
                      substituir: bool = True) -> Dict[str, Any]:
    """Processa uma prancha de engenharia e alimenta o motor de quantitativos em segundos."""
    t0 = time.time()
    caminho = Path(caminho_pdf).resolve()
    
    # 1. Leitura base
    leitor = LeitorPDFBase(caminho)
    disciplina = disciplina_forcada or leitor.detectar_disciplina()
    
    # 2. Seleção do parser especializado por disciplina
    if disciplina in {"FUNDACOES", "INFRAESTRUTURA"}:
        parser = ParserFundacoes(leitor)
        dados = parser.extrair(incluir_correlatas=True)
        itens_eap = parser.gerar_itens_eap(dados)
        titulo_disciplina = "Infraestrutura e Fundações"
    elif disciplina == "ESTRUTURA":
        parser = ParserEstrutura(leitor)
        dados = parser.extrair(incluir_correlatas=True)
        itens_eap = parser.gerar_itens_eap(dados)
        titulo_disciplina = "Estrutura"
    elif disciplina == "ARQUITETURA":
        parser = ParserArquitetura(leitor)
        dados = parser.extrair(incluir_correlatas=True)
        itens_eap = parser.gerar_itens_eap(dados)
        titulo_disciplina = "Arquitetura e Acabamentos"
    elif disciplina == "INSTALACOES":
        parser = ParserInstalacoes(leitor)
        dados = parser.extrair(incluir_correlatas=True)
        itens_eap = parser.gerar_itens_eap(dados)
        titulo_disciplina = "Instalações Prediais"
    else:
        raise ValueError(
            f"Disciplina não reconhecida para {caminho.name}; "
            "informe --disciplina explicitamente ou corrija o selo da prancha."
        )

    # 3. Montagem do payload padronizado
    dados_json = {
        "projeto": "PORTO DO AÇU - TMULT FASE I",
        "base_dir": str(caminho.parent),
        "data_auditoria": time.strftime("%d/%m/%Y"),
        "disciplinas": {
            disciplina.lower(): {
                "titulo": titulo_disciplina,
                "pranchas_ref": ", ".join(dados["pranchas_processadas"]),
                "itens_orcamento": itens_eap
            }
        }
    }

    # 4. Gravação intermediária limpa para rastreabilidade
    caminho_json = Path("data") / f"levantamento_{disciplina.lower()}_auto.json"
    caminho_json.parent.mkdir(parents=True, exist_ok=True)
    caminho_json.write_text(json.dumps(dados_json, indent=2, ensure_ascii=False), encoding="utf-8")

    # 5. Ingestão oficial no SQLite e geração dos artefatos
    arquivos_gerados = importar_json_inicial(str(caminho_json), db_path, substituir=substituir)
    tempo_total = time.time() - t0

    return {
        "disciplina": disciplina,
        "tempo_total_s": round(tempo_total, 2),
        "dados_extracao": dados,
        "total_itens_eap": len(itens_eap),
        "arquivos_gerados": [str(a) for a in arquivos_gerados]
    }


def main():
    if len(sys.argv) < 2:
        print("Uso: python roteador.py <caminho_prancha.pdf> [--db <caminho_db>] [--disciplina <NOME>]")
        sys.exit(1)
        
    pdf_alvo = sys.argv[1]
    db_alvo = "data/pmo_virtual.sqlite"
    disc = None
    
    if "--db" in sys.argv:
        idx = sys.argv.index("--db")
        if idx + 1 < len(sys.argv):
            db_alvo = sys.argv[idx + 1]
            
    if "--disciplina" in sys.argv:
        idx = sys.argv.index("--disciplina")
        if idx + 1 < len(sys.argv):
            disc = sys.argv[idx + 1].upper()

    res = processar_prancha(pdf_alvo, disciplina_forcada=disc, db_path=db_alvo, substituir=True)
    
    print("\n" + "="*70)
    print("[SUCESSO] ROTEADOR DE EXTRACAO EXECUTADO COM SUCESSO!")
    print(f"Disciplina detectada: {res['disciplina']}")
    print(f"Tempo total de execucao: {res['tempo_total_s']} segundos")
    print(f"Total de itens EAP gerados: {res['total_itens_eap']}")
    print("="*70)
    print("Arquivos gerados:")
    for a in res["arquivos_gerados"]:
        print(f"  -> {a}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
