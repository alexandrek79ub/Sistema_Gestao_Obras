"""
Script Único e Oficial: processar_prancha.py
Substitui todo o labirinto de scripts antigos por um pipeline único, autossuficiente e direto.
Uso:
  python scripts/processar_prancha.py --obra 3 --prancha "EGS-051" --dados itens.json [--orcamento] [--sobrescrever]
"""

import argparse
import ast
import csv
import hashlib
import json
import re
import sqlite3
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

COLUNAS_QUANT = ["COD_EAP", "DESCRICAO_DO_SERVICO", "DISCIPLINA", "UNIDADE", "QUANTIDADE_TOTAL", "PRANCHA_REFERENCIA", "STATUS"]
COLUNAS_ORC = [
    "COD_EAP", "DESCRICAO_DO_SERVICO", "DISCIPLINA", "UNIDADE", "QUANTIDADE_TOTAL",
    "CUSTO_UNITARIO_BDI", "CUSTO_TOTAL", "EMPREITEIRO_VINCULADO", "PRANCHA_REFERENCIA",
    "FONTE_PRECO", "STATUS", "CODIGO_SINAPI", "CENTRO_CUSTO"
]

def calcular_expressao(expr: str) -> float:
    """Calcula determinística e seguramente uma expressão matemática em string."""
    if not expr:
        return 0.0
    try:
        expr_clean = expr.replace(",", ".")
        tree = ast.parse(expr_clean, mode="eval")
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
                                      ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd)):
                raise ValueError(f"Operação não permitida: {expr}")
        return float(eval(compile(tree, "<string>", "eval")))
    except Exception:
        return 0.0

def sanitizar_nome(texto: str) -> str:
    sem_acento = "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c))
    return re.sub(r"[^A-Z0-9]+", "_", sem_acento.upper()).strip("_") or "GERAL"

def escrever_csv(destino: Path, colunas: list[str], linhas: list[tuple]):
    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(colunas)
        writer.writerows(linhas)

def exportar_arquivos_obra(conn: sqlite3.Connection, obra_id: int) -> list[str]:
    """Gera automaticamente todos os artefatos (CSVs e Memórias Compactas) direto do SQLite."""
    obra = conn.execute("SELECT nome, diretorio_base FROM obras WHERE id = ?", (obra_id,)).fetchone()
    if not obra or not obra["diretorio_base"]:
        return []

    base = Path(obra["diretorio_base"])
    base.mkdir(parents=True, exist_ok=True)

    itens_raw = conn.execute("""
        SELECT q.*, o.codigo_sinapi, o.centro_custo, o.fonte_preco, o.preco_unitario, o.bdi_pct, o.custo_total
        FROM itens_quantitativo q
        LEFT JOIN itens_orcamento o ON o.quantitativo_id = q.id AND o.obra_id = q.obra_id
        WHERE q.obra_id = ?
        ORDER BY q.disciplina, q.cod_eap, q.prancha_referencia
    """, (obra_id,)).fetchall()

    if not itens_raw:
        return []

    itens = [dict(r) for r in itens_raw]


    saidas = []

    # 1. QUANTITATIVO_MESTRE.csv
    linhas_q = [(r["cod_eap"], r["descricao"], r["disciplina"], r["unidade"], r["quantidade_liquida"], r["prancha_referencia"], r["status"]) for r in itens]
    arq_qmestre = base / "QUANTITATIVO_MESTRE.csv"
    escrever_csv(arq_qmestre, COLUNAS_QUANT, linhas_q)
    saidas.append(str(arq_qmestre))

    # 2. ORCAMENTO_BASE_CONSOLIDADO.csv
    linhas_o = []
    for r in itens:
        pu = float(r["preco_unitario"] or 0)
        bdi = float(r["bdi_pct"] or 0)
        pu_bdi = round(pu * (1 + bdi / 100.0), 2) if bdi else pu
        linhas_o.append((
            r["cod_eap"], r["descricao"], r["disciplina"], r["unidade"],
            r["quantidade_liquida"], pu_bdi, r["custo_total"] or 0,
            "Engenharia", r["prancha_referencia"], r["fonte_preco"] or "",
            r["status"], r["codigo_sinapi"] or "", r["centro_custo"] or ""
        ))
    arq_orc = base / "ORCAMENTO_BASE_CONSOLIDADO.csv"
    escrever_csv(arq_orc, COLUNAS_ORC, linhas_o)
    saidas.append(str(arq_orc))

    # Checksum do quantitativo
    chk_str = json.dumps([dict(r) for r in itens], ensure_ascii=False, sort_keys=True)
    checksum = hashlib.sha256(chk_str.encode()).hexdigest()

    # 3. Exportações por disciplina (CSV + Memória Compacta)
    disciplinas = sorted({r["disciplina"] for r in itens})
    for disc in disciplinas:
        grupo = [r for r in itens if r["disciplina"] == disc]
        sufixo = sanitizar_nome(disc)

        # 3.1 CSV da disciplina
        arq_disc_csv = base / f"QUANTITATIVO_{sufixo}.csv"
        escrever_csv(arq_disc_csv, COLUNAS_QUANT, [
            (r["cod_eap"], r["descricao"], r["disciplina"], r["unidade"], r["quantidade_liquida"], r["prancha_referencia"], r["status"]) for r in grupo
        ])
        saidas.append(str(arq_disc_csv))

        # 3.2 Memória de Cálculo Compactada em Tabela Executiva
        pranchas_disc = sorted({Path(r["prancha_referencia"]).stem for r in grupo if r.get("prancha_referencia")})
        cabecalho_pranchas = ", ".join(pranchas_disc) or "Geral"

        linhas_md = [
            f"# Memória de Cálculo Auditável: {disc}",
            "",
            f"**Obra:** {obra['nome']}  ",
            f"**Pranchas de Referência:** {cabecalho_pranchas}  ",
            f"**Checksum do Quantitativo:** `{checksum}`",
            "",
            "---",
            "",
            "## 1. Demonstração Matemática Detalhada",
            "",
            "| EAP | Elemento / Serviço | Qtd Líquida | Unid | Expressão Matemática | Prancha |",
            "| :---: | :--- | :---: | :---: | :--- | :--- |"
        ]

        for r in grupo:
            desc = r["descricao"]
            prancha_nome = Path(r["prancha_referencia"]).stem if r.get("prancha_referencia") else ""
            linhas_md.append(f"| {r['cod_eap']} | {desc} | {r['quantidade_liquida']} | {r['unidade']} | `{r['expressao_matematica']}` | {prancha_nome} |")

        linhas_md.extend([
            "",
            "---",
            "",
            "## 2. Tabela Consolidada de Serviços (EAP)",
            "",
            "| EAP | Pacote de Serviço | Total Líquido | Unid | Status |",
            "| :---: | :--- | :---: | :---: | :---: |"
        ])

        totais_eap = {}
        for r in grupo:
            cod = r["cod_eap"]
            if cod not in totais_eap:
                totais_eap[cod] = {"nome": r["descricao"].split(" — ")[0], "unid": r["unidade"], "tot": 0.0, "st": r["status"]}
            totais_eap[cod]["tot"] += float(r["quantidade_liquida"] or 0.0)

        for cod in sorted(totais_eap.keys()):
            d = totais_eap[cod]
            linhas_md.append(f"| **{cod}** | {d['nome']} | **{d['tot']:.2f}** | {d['unid']} | {d['st']} |")

        arq_md = base / f"MEMORIA_CALCULO_{sufixo}.md"
        arq_md.write_text("\n".join(linhas_md), encoding="utf-8")
        saidas.append(str(arq_md))

    return saidas

def main():
    parser = argparse.ArgumentParser(description="Pipeline oficial simplificado de levantamento de pranchas.")
    parser.add_argument("--obra", type=int, default=3, help="ID da obra no SQLite (padrão: 3 - OBRA_PORTO)")
    parser.add_argument("--prancha", required=True, help="Nome do arquivo ou código do desenho")
    parser.add_argument("--dados", required=True, help="Caminho do arquivo JSON com dados nominais")
    parser.add_argument("--titulo", default=None, help="Título do desenho")
    parser.add_argument("--orcamento", action="store_true", help="Se definido, inclui itens no orçamento base")
    parser.add_argument("--sobrescrever", action="store_true", help="Substitui itens anteriores da prancha")
    parser.add_argument("--db", default="data/pmo_virtual.sqlite", help="Caminho do SQLite")

    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"[ERRO] Banco SQLite não encontrado em {db_path}")
        sys.exit(1)

    dados_path = Path(args.dados)
    if not dados_path.exists():
        print(f"[ERRO] Arquivo de dados não encontrado: {dados_path}")
        sys.exit(1)

    with open(dados_path, "r", encoding="utf-8") as f:
        itens = json.load(f)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    prancha_termo = f"%{Path(args.prancha).stem}%"
    total_existente = cursor.execute(
        "SELECT COUNT(*) as tot FROM itens_quantitativo WHERE obra_id = ? AND prancha_referencia LIKE ?",
        (args.obra, prancha_termo)
    ).fetchone()["tot"]

    if total_existente > 0:
        if not args.sobrescrever:
            print(f"[ALERTA] A prancha '{args.prancha}' já possui {total_existente} itens registrados na obra {args.obra}.")
            print("Passe --sobrescrever para atualizar.")
            conn.close()
            sys.exit(0)
        else:
            cursor.execute("DELETE FROM itens_quantitativo WHERE obra_id = ? AND prancha_referencia LIKE ?", (args.obra, prancha_termo))

    agora = datetime.now(timezone.utc).isoformat()
    tipo_rev = "ORCAMENTO" if args.orcamento else "QUANTITATIVO"
    cursor.execute("""
        INSERT INTO revisoes (obra_id, tipo, usuario, justificativa, origem, created_at)
        VALUES (?, ?, 'auditor-engenharia', ?, ?, ?)
    """, (args.obra, tipo_rev, f"Levantamento nominal da prancha {args.prancha}", f"pipeline-oficial:{args.prancha}", agora))
    revisao_id = cursor.lastrowid

    cont = 0
    for it in itens:
        cod_eap = it.get("cod_eap", "")
        desc = it.get("descricao", "")
        disc = it.get("disciplina", "Infraestrutura e Fundações")
        unid = it.get("unidade", "un")
        expr = it.get("expressao_matematica", "")
        qtd = it.get("quantidade_liquida")
        if qtd is None:
            qtd = calcular_expressao(expr)
        else:
            qtd = float(qtd)

        cursor.execute("""
            INSERT INTO itens_quantitativo (
                obra_id, revisao_id, cod_eap, descricao, disciplina, unidade,
                quantidade_liquida, expressao_matematica, prancha_referencia,
                status, observacao, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (args.obra, revisao_id, cod_eap, desc, disc, unid, qtd, expr, args.prancha, it.get("status", "LEVANTADO"), it.get("observacao", ""), agora))
        quant_id = cursor.lastrowid
        cont += 1

        if args.orcamento and "preco_unitario" in it:
            pu = float(it.get("preco_unitario", 0.0))
            bdi = float(it.get("bdi_pct", 0.0))
            custo_tot = round(qtd * pu * (1 + bdi / 100), 2)
            cursor.execute("""
                INSERT INTO itens_orcamento (
                    obra_id, quantitativo_id, revisao_id, codigo_sinapi, centro_custo,
                    fonte_preco, preco_unitario, bdi_pct, custo_total, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (args.obra, quant_id, revisao_id, it.get("sinapi", ""), it.get("centro_custo", "GERAL"), it.get("fonte", "SINAPI"), pu, bdi, custo_tot, agora))

    if args.titulo:
        cursor.execute("""
            UPDATE lista_desenhos SET status = 'VIGENTE', titulo = ?, updated_at = ?
            WHERE obra_id = ? AND codigo LIKE ?
        """, (args.titulo, agora, args.obra, prancha_termo))

    conn.commit()
    print(f"\n[SUCESSO] {cont} itens gravados no SQLite (Revisão ID {revisao_id}).")

    saidas = exportar_arquivos_obra(conn, args.obra)
    print("[ARTEFATOS] Documentos compactados atualizados com sucesso:")
    for s in saidas:
        print(f"  -> {Path(s).name}")

    conn.close()

if __name__ == "__main__":
    main()
