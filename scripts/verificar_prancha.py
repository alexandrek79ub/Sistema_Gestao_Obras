"""Gate Zero determinístico para levantamento quantitativo.

Uso:
    python scripts/verificar_prancha.py --obra 3 --prancha "F-01 rev.A.pdf"

Saída válida (sempre exit code 0):
    JA_LEVANTADA|<quantidade_de_itens>
    NAO_LEVANTADA|0

Erros operacionais usam exit code 2 e são enviados para stderr.
"""

import argparse
import sqlite3
import sys
import unicodedata
from pathlib import Path


def normalizar_prancha(valor: str) -> str:
    """Normaliza somente o nome-base, preservando revisão e pontuação."""
    nome = Path(str(valor).strip()).stem
    return unicodedata.normalize("NFKC", nome).casefold().strip()


def contar_itens(conn: sqlite3.Connection, obra_id: int, prancha: str) -> int:
    obra = conn.execute("SELECT 1 FROM obras WHERE id=?", (obra_id,)).fetchone()
    if not obra:
        raise ValueError(f"obra_id {obra_id} não existe no SQLite")

    alvo = normalizar_prancha(prancha)
    if not alvo:
        raise ValueError("prancha inválida")

    rows = conn.execute(
        "SELECT prancha_referencia FROM itens_quantitativo WHERE obra_id=?",
        (obra_id,),
    ).fetchall()

    return sum(
        1
        for row in rows
        if normalizar_prancha(row[0]) == alvo
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verifica se uma prancha já possui levantamento quantitativo no SQLite."
    )
    parser.add_argument("--obra", type=int, required=True, help="ID da obra no SQLite")
    parser.add_argument("--prancha", required=True, help="Nome/caminho da prancha")
    parser.add_argument("--db", default="data/pmo_virtual.sqlite", help="Caminho do SQLite")
    args = parser.parse_args()

    try:
        db_path = Path(args.db)
        if not db_path.exists():
            raise ValueError(f"SQLite não encontrado: {db_path}")

        conn = sqlite3.connect(db_path)
        try:
            quantidade = contar_itens(conn, args.obra, args.prancha)
        finally:
            conn.close()

        if quantidade:
            print(f"JA_LEVANTADA|{quantidade}")
        else:
            print("NAO_LEVANTADA|0")

    except (ValueError, sqlite3.Error, OSError) as exc:
        print(f"ERRO|{exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
