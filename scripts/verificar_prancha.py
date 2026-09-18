"""Gate determinístico para saber se pranchas já foram levantadas.

Uso simples:
    python scripts/verificar_prancha.py --obra 3 --prancha "F-01 rev.A.pdf"

Uso em lote:
    python scripts/verificar_prancha.py --obra 3 \
        --prancha "ARQ-01.pdf" --prancha "ARQ-02.pdf"

Saída simples, compatível com o fluxo anterior:
    JA_LEVANTADA|<quantidade_de_itens>
    NAO_LEVANTADA|0

Saída em lote, uma linha por prancha:
    <prancha>|JA_LEVANTADA|<quantidade_de_itens>
    <prancha>|NAO_LEVANTADA|0

Erros operacionais usam exit code 2 e são enviados para stderr.
"""

import argparse
import sqlite3
import sys
import unicodedata
from collections import Counter
from pathlib import Path


def normalizar_prancha(valor: str) -> str:
    """Normaliza somente o nome-base, preservando revisão e pontuação."""
    nome = Path(str(valor).strip()).stem
    return unicodedata.normalize("NFKC", nome).casefold().strip()


def mapa_quantidades(conn: sqlite3.Connection, obra_id: int) -> Counter:
    obra = conn.execute("SELECT 1 FROM obras WHERE id=?", (obra_id,)).fetchone()
    if not obra:
        raise ValueError(f"obra_id {obra_id} não existe no SQLite")

    rows = conn.execute(
        "SELECT prancha_referencia FROM itens_quantitativo WHERE obra_id=?",
        (obra_id,),
    ).fetchall()
    return Counter(normalizar_prancha(row[0]) for row in rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verifica se uma ou mais pranchas já possuem quantitativo no SQLite."
    )
    parser.add_argument("--obra", type=int, required=True, help="ID da obra no SQLite")
    parser.add_argument(
        "--prancha",
        action="append",
        required=True,
        help="Nome/caminho da prancha. Pode ser repetido para verificar várias de uma vez.",
    )
    parser.add_argument("--db", default="data/pmo_virtual.sqlite", help="Caminho do SQLite")
    args = parser.parse_args()

    try:
        db_path = Path(args.db)
        if not db_path.exists():
            raise ValueError(f"SQLite não encontrado: {db_path}")

        conn = sqlite3.connect(db_path)
        try:
            quantidades = mapa_quantidades(conn, args.obra)
        finally:
            conn.close()

        resultados = []
        for prancha in args.prancha:
            alvo = normalizar_prancha(prancha)
            if not alvo:
                raise ValueError("prancha inválida")
            quantidade = quantidades.get(alvo, 0)
            estado = "JA_LEVANTADA" if quantidade else "NAO_LEVANTADA"
            resultados.append((prancha, estado, quantidade))

        if len(resultados) == 1:
            _, estado, quantidade = resultados[0]
            print(f"{estado}|{quantidade}")
        else:
            for prancha, estado, quantidade in resultados:
                print(f"{prancha}|{estado}|{quantidade}")

    except (ValueError, sqlite3.Error, OSError) as exc:
        print(f"ERRO|{exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
