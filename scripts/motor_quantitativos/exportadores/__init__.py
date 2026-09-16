import hashlib
import json
import re
import sqlite3
import unicodedata
from pathlib import Path
from typing import Any

from motor_quantitativos.domain.modelos import COLUNAS_ORCAMENTO, COLUNAS_QUANTITATIVO
from motor_quantitativos.exportadores.csv_exporter import escrever_csv
from motor_quantitativos.exportadores.markdown_exporter import escrever_memoria_calculo


def exportar_checksum(db: sqlite3.Connection, obra_id: int) -> str:
    rows = [dict(row) for row in db.execute(
        "SELECT cod_eap,descricao,disciplina,unidade,quantidade_liquida,expressao_matematica,prancha_referencia,status,versao FROM itens_quantitativo WHERE obra_id=? ORDER BY id", 
        (obra_id,)
    )]
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def _nome_disciplina(disciplina: str) -> str:
    sem_acento = "".join(c for c in unicodedata.normalize("NFKD", disciplina) if not unicodedata.combining(c))
    nome = re.sub(r"[^A-Z0-9]+", "_", sem_acento.upper()).strip("_")
    return nome or "SEM_DISCIPLINA"


def exportar_artefatos(db: sqlite3.Connection, obra_id: int, diretorio_base: str | Path | None = None) -> list[Path]:
    obra = db.execute("SELECT nome,diretorio_base FROM obras WHERE id=?", (obra_id,)).fetchone()
    if obra is None:
        raise ValueError("Obra não encontrada")
    
    base = Path(diretorio_base or obra["diretorio_base"])
    if not str(base):
        raise ValueError("Diretório de exportação da obra não definido")
        
    itens = db.execute("""
        SELECT q.*, o.codigo_sinapi,o.centro_custo,o.fonte_preco,o.preco_unitario,o.bdi_pct,o.custo_total
        FROM itens_quantitativo q LEFT JOIN itens_orcamento o ON o.quantitativo_id=q.id AND o.obra_id=q.obra_id
        WHERE q.obra_id=? ORDER BY q.disciplina,q.cod_eap,q.prancha_referencia
    """, (obra_id,)).fetchall()
    
    saidas: list[Path] = []
    
    # 1. QUANTITATIVO_MESTRE.csv
    linhas_quant = [(r["cod_eap"], r["descricao"], r["disciplina"], r["unidade"], r["quantidade_liquida"], r["prancha_referencia"], r["status"]) for r in itens]
    mestre = base / "QUANTITATIVO_MESTRE.csv"
    escrever_csv(mestre, COLUNAS_QUANTITATIVO, linhas_quant)
    saidas.append(mestre)
    
    # 2. ORCAMENTO_BASE_CONSOLIDADO.csv
    linhas_orc = []
    for r in itens:
        pu = float(r["preco_unitario"] or 0)
        bdi = float(r["bdi_pct"] or 0)
        pu_bdi = round(pu * (1 + bdi / 100.0), 2) if bdi else pu
        linhas_orc.append((
            r["cod_eap"], r["descricao"], r["disciplina"], r["unidade"],
            r["quantidade_liquida"], pu_bdi, r["custo_total"] or 0,
            "Engenharia", r["prancha_referencia"], r["fonte_preco"] or "",
            r["status"], r["codigo_sinapi"] or "", r["centro_custo"] or ""
        ))
    orcamento = base / "ORCAMENTO_BASE_CONSOLIDADO.csv"
    escrever_csv(orcamento, COLUNAS_ORCAMENTO, linhas_orc)
    saidas.append(orcamento)
    
    checksum = exportar_checksum(db, obra_id)
    
    # 3. Exportações por disciplina
    for disciplina in sorted({r["disciplina"] for r in itens}):
        grupo = [dict(r) for r in itens if r["disciplina"] == disciplina]
        sufixo = _nome_disciplina(disciplina)
        
        # 3.1. CSV da Disciplina
        quant_disc = base / f"QUANTITATIVO_{sufixo}.csv"
        escrever_csv(quant_disc, COLUNAS_QUANTITATIVO, [(r["cod_eap"], r["descricao"], r["disciplina"], r["unidade"], r["quantidade_liquida"], r["prancha_referencia"], r["status"]) for r in grupo])
        saidas.append(quant_disc)
        
        # 3.2. Markdown da Disciplina
        memoria = base / f"MEMORIA_CALCULO_{sufixo}.md"
        escrever_memoria_calculo(memoria, obra["nome"], checksum, disciplina, grupo)
        saidas.append(memoria)
        
    return saidas
