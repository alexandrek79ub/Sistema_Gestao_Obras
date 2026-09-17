import argparse
import os
import sqlite3
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def consultar_prancha_sqlite(db_path: str, prancha_query: str, obra_query: str = None):
    if not os.path.exists(db_path):
        print(f"[ERRO] Banco SQLite não encontrado em: {db_path}")
        return []

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Identifica obras correspondentes
    if obra_query:
        obras = c.execute(
            "SELECT id, codigo, nome FROM obras WHERE id = ? OR codigo LIKE ? OR nome LIKE ?",
            (obra_query if obra_query.isdigit() else -1, f"%{obra_query}%", f"%{obra_query}%"),
        ).fetchall()
    else:
        obras = c.execute("SELECT id, codigo, nome FROM obras").fetchall()

    if not obras:
        print(f"[AVISO] Nenhuma obra encontrada com o termo: '{obra_query}'")
        conn.close()
        return []

    resultados = []
    # Limpa termo da prancha para busca mais ampla (ex: extrai EGS-052 ou 052)
    termo = prancha_query.strip()
    termo_base = os.path.splitext(os.path.basename(termo))[0]

    for obra_id, obra_cod, obra_nome in obras:
        # Busca itens de quantitativo
        query = """
            SELECT id, cod_eap, descricao, quantidade_liquida, unidade, prancha_referencia, status, updated_at
            FROM itens_quantitativo
            WHERE obra_id = ? AND (
                prancha_referencia LIKE ? OR prancha_referencia LIKE ? OR observacao LIKE ?
            )
            ORDER BY cod_eap
        """
        itens = c.execute(
            query,
            (obra_id, f"%{termo}%", f"%{termo_base}%", f"%{termo_base}%"),
        ).fetchall()

        if itens:
            resultados.append({
                "obra_id": obra_id,
                "obra_codigo": obra_cod,
                "obra_nome": obra_nome,
                "itens": itens,
            })

    conn.close()
    return resultados


def main():
    parser = argparse.ArgumentParser(description="Verifica se uma prancha já possui quantitativos levantados no SQLite.")
    parser.add_argument("prancha", help="Código, nome do arquivo ou trecho do nome da prancha (ex: EGS-052, 052)")
    parser.add_argument("--obra", default=None, help="Código ou nome da obra (opcional)")
    parser.add_argument("--db", default="data/pmo_virtual.sqlite", help="Caminho do SQLite oficial")

    args = parser.parse_args()
    resultados = consultar_prancha_sqlite(args.db, args.prancha, args.obra)

    if not resultados:
        print(f"[INFO] Nenhum quantitativo encontrado para a prancha '{args.prancha}' no banco de dados.")
        sys.exit(0)

    print(f"\n🚨 [ALERTA DE DUPLICIDADE] Prancha '{args.prancha}' JÁ POSSUI quantitativos registrados no SQLite!\n")
    for res in resultados:
        print(f"🏗️  Obra: {res['obra_nome']} (Código: {res['obra_codigo']} | ID: {res['obra_id']})")
        print(f"📊 Total de Itens Levantados: {len(res['itens'])}")
        print("-" * 90)
        print(f"{'EAP':<10} | {'Descrição':<42} | {'Qtd Líquida':>12} | {'Unid':<5} | {'Prancha Registrada'}")
        print("-" * 90)
        for item in res["itens"]:
            id_item, eap, desc, qtd, unid, prancha_ref, st, upd = item
            desc_curta = (desc[:39] + "...") if len(desc) > 42 else desc
            print(f"{eap:<10} | {desc_curta:<42} | {qtd:>12.3f} | {unid:<5} | {prancha_ref}")
        print("-" * 90)
        print("Ação recomendada: Não realizar levantamento duplicado. Confirmar com o usuário se deseja revisar os itens acima.\n")


if __name__ == "__main__":
    main()
