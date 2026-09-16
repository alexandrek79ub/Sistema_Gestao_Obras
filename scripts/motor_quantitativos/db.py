from __future__ import annotations

import csv
import hashlib
import json
import re
import sqlite3
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


STATUS_QUANTITATIVO = {"LEVANTADO", "PENDENTE_RFI", "NAO_LEVANTADO"}
COLUNAS_QUANTITATIVO = (
    "COD_EAP", "DESCRICAO_DO_SERVICO", "DISCIPLINA", "UNIDADE",
    "QUANTIDADE_TOTAL", "PRANCHA_REFERENCIA", "STATUS",
)
COLUNAS_ORCAMENTO = (
    "COD_EAP", "DESCRICAO_DO_SERVICO", "DISCIPLINA", "UNIDADE",
    "QUANTIDADE_TOTAL", "CUSTO_UNITARIO_BDI", "CUSTO_TOTAL",
    "EMPREITEIRO_VINCULADO", "PRANCHA_REFERENCIA", "FONTE_PRECO", "STATUS",
    "CODIGO_SINAPI", "CENTRO_CUSTO",
)


def agora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _tem_coluna(db: sqlite3.Connection, tabela: str, coluna: str) -> bool:
    return any(row[1] == coluna for row in db.execute(f"PRAGMA table_info({tabela})"))


def aplicar_migracoes(db: sqlite3.Connection) -> None:
    """Aplica alterações idempotentes e registra a versão do schema no próprio banco."""
    db.execute("CREATE TABLE IF NOT EXISTS schema_migrations (versao INTEGER PRIMARY KEY, aplicada_em TEXT NOT NULL)")
    db.executescript("""
    CREATE TABLE IF NOT EXISTS obras (
        id INTEGER PRIMARY KEY,
        codigo TEXT NOT NULL UNIQUE,
        nome TEXT NOT NULL,
        diretorio_base TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS revisoes (
        id INTEGER PRIMARY KEY,
        obra_id INTEGER NOT NULL REFERENCES obras(id),
        tipo TEXT NOT NULL CHECK(tipo IN ('QUANTITATIVO','ORCAMENTO')),
        usuario TEXT NOT NULL,
        justificativa TEXT NOT NULL,
        origem TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS itens_quantitativo (
        id INTEGER PRIMARY KEY,
        obra_id INTEGER NOT NULL REFERENCES obras(id),
        revisao_id INTEGER REFERENCES revisoes(id),
        cod_eap TEXT NOT NULL,
        descricao TEXT NOT NULL,
        disciplina TEXT NOT NULL,
        unidade TEXT NOT NULL,
        quantidade_liquida REAL NOT NULL CHECK(quantidade_liquida >= 0),
        expressao_matematica TEXT NOT NULL,
        prancha_referencia TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('LEVANTADO','PENDENTE_RFI','NAO_LEVANTADO')),
        rfi TEXT NOT NULL DEFAULT '',
        observacao TEXT NOT NULL DEFAULT '',
        versao INTEGER NOT NULL DEFAULT 1,
        updated_at TEXT NOT NULL,
        UNIQUE(obra_id, cod_eap, prancha_referencia)
    );
    CREATE TABLE IF NOT EXISTS itens_orcamento (
        id INTEGER PRIMARY KEY,
        obra_id INTEGER NOT NULL REFERENCES obras(id),
        quantitativo_id INTEGER NOT NULL REFERENCES itens_quantitativo(id),
        revisao_id INTEGER REFERENCES revisoes(id),
        codigo_sinapi TEXT NOT NULL DEFAULT '',
        centro_custo TEXT NOT NULL DEFAULT '',
        fonte_preco TEXT NOT NULL DEFAULT '',
        custo_material REAL NOT NULL DEFAULT 0,
        custo_mao_obra REAL NOT NULL DEFAULT 0,
        custo_equipamento REAL NOT NULL DEFAULT 0,
        bdi_pct REAL NOT NULL DEFAULT 0,
        preco_unitario REAL NOT NULL DEFAULT 0,
        custo_total REAL NOT NULL DEFAULT 0,
        updated_at TEXT NOT NULL,
        UNIQUE(obra_id, quantitativo_id)
    );
    CREATE TABLE IF NOT EXISTS auditoria_eventos (
        id INTEGER PRIMARY KEY,
        obra_id INTEGER NOT NULL REFERENCES obras(id),
        entidade TEXT NOT NULL,
        entidade_id INTEGER NOT NULL,
        acao TEXT NOT NULL,
        antes_json TEXT NOT NULL DEFAULT '',
        depois_json TEXT NOT NULL DEFAULT '',
        usuario TEXT NOT NULL,
        justificativa TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_quant_obra_eap ON itens_quantitativo(obra_id, cod_eap);
    CREATE INDEX IF NOT EXISTS idx_orc_obra ON itens_orcamento(obra_id);
    """)
    if not _tem_coluna(db, "obras", "diretorio_base"):
        db.execute("ALTER TABLE obras ADD COLUMN diretorio_base TEXT NOT NULL DEFAULT ''")
    db.execute("INSERT OR IGNORE INTO schema_migrations(versao,aplicada_em) VALUES(?,?)", (1, agora()))


def connect(path: str | Path) -> sqlite3.Connection:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(path))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("PRAGMA journal_mode = WAL")
    aplicar_migracoes(db)
    return db


def criar_backup(db_path: str | Path, diretorio_backup: str | Path | None = None) -> Path:
    """Cria um snapshot consistente via API SQLite, inclusive quando WAL está ativo."""
    origem = Path(db_path)
    destino_dir = Path(diretorio_backup) if diretorio_backup else origem.parent / "backups"
    destino_dir.mkdir(parents=True, exist_ok=True)
    destino = destino_dir / f"{origem.stem}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.sqlite"
    fonte = sqlite3.connect(str(origem))
    alvo = sqlite3.connect(str(destino))
    try:
        fonte.backup(alvo)
    finally:
        alvo.close()
        fonte.close()
    return destino


def garantir_obra(db: sqlite3.Connection, codigo: str, nome: str, diretorio_base: str = "") -> int:
    instante = agora()
    db.execute(
        "INSERT INTO obras(codigo,nome,diretorio_base,created_at,updated_at) VALUES(?,?,?,?,?) "
        "ON CONFLICT(codigo) DO UPDATE SET nome=excluded.nome, "
        "diretorio_base=CASE WHEN excluded.diretorio_base <> '' THEN excluded.diretorio_base ELSE obras.diretorio_base END, "
        "updated_at=excluded.updated_at",
        (codigo, nome, diretorio_base, instante, instante),
    )
    return int(db.execute("SELECT id FROM obras WHERE codigo=?", (codigo,)).fetchone()[0])


def registrar_revisao(db: sqlite3.Connection, obra_id: int, tipo: str, origem: str,
                      usuario: str = "motor-python", justificativa: str = "") -> int:
    if tipo not in {"QUANTITATIVO", "ORCAMENTO"}:
        raise ValueError("Tipo de revisão inválido")
    cur = db.execute(
        "INSERT INTO revisoes(obra_id,tipo,usuario,justificativa,origem,created_at) VALUES(?,?,?,?,?,?)",
        (obra_id, tipo, usuario.strip() or "motor-python", justificativa.strip() or "Atualização automatizada", origem, agora()),
    )
    return int(cur.lastrowid)


def substituir_quantitativos(db: sqlite3.Connection, obra_id: int, itens: Iterable[dict[str, Any]],
                             revisao_id: int) -> list[int]:
    """Uso exclusivo da importação inicial ou da reimportação explicitamente autorizada."""
    ids: list[int] = []
    for item in itens:
        valores = (
            obra_id, revisao_id, item["cod_eap"], item["descricao"], item["disciplina"], item["unidade"],
            float(item["quantidade_liquida"]), item["expressao_matematica"], item["prancha_referencia"],
            item.get("status", "LEVANTADO"), item.get("rfi", ""), item.get("observacao", ""), agora(),
        )
        db.execute(
            "INSERT INTO itens_quantitativo(obra_id,revisao_id,cod_eap,descricao,disciplina,unidade,quantidade_liquida,"
            "expressao_matematica,prancha_referencia,status,rfi,observacao,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(obra_id,cod_eap,prancha_referencia) DO UPDATE SET revisao_id=excluded.revisao_id,"
            "descricao=excluded.descricao,disciplina=excluded.disciplina,unidade=excluded.unidade,"
            "quantidade_liquida=excluded.quantidade_liquida,expressao_matematica=excluded.expressao_matematica,"
            "status=excluded.status,rfi=excluded.rfi,observacao=excluded.observacao,"
            "versao=itens_quantitativo.versao+1,updated_at=excluded.updated_at",
            valores,
        )
        ids.append(int(db.execute(
            "SELECT id FROM itens_quantitativo WHERE obra_id=? AND cod_eap=? AND prancha_referencia=?",
            (obra_id, item["cod_eap"], item["prancha_referencia"]),
        ).fetchone()[0]))
    return ids


def atualizar_quantitativo(db: sqlite3.Connection, obra_id: int, item_id: int, alteracoes: dict[str, Any],
                           usuario: str, justificativa: str, versao_esperada: int) -> int:
    if not usuario or not usuario.strip():
        raise ValueError("Usuário responsável é obrigatório")
    if not justificativa or not justificativa.strip():
        raise ValueError("Justificativa da alteração é obrigatória")
    atual = db.execute("SELECT * FROM itens_quantitativo WHERE id=? AND obra_id=?", (item_id, obra_id)).fetchone()
    if atual is None:
        raise ValueError("Item de quantitativo não encontrado")
    if int(atual["versao"]) != int(versao_esperada):
        raise RuntimeError(f"Conflito de versão: item está na versão {atual['versao']}")
    permitidos = {"descricao", "unidade", "quantidade_liquida", "expressao_matematica", "prancha_referencia", "status", "rfi", "observacao"}
    campos = {k: v for k, v in alteracoes.items() if k in permitidos}
    if not campos:
        raise ValueError("Nenhum campo editável informado")
    if "quantidade_liquida" in campos and float(campos["quantidade_liquida"]) < 0:
        raise ValueError("Quantidade líquida não pode ser negativa")
    if "status" in campos and campos["status"] not in STATUS_QUANTITATIVO:
        raise ValueError("STATUS inválido")
    revisao = registrar_revisao(db, obra_id, "QUANTITATIVO", "api-local", usuario, justificativa)
    antes = dict(atual)
    campos.update({"revisao_id": revisao, "versao": int(atual["versao"]) + 1, "updated_at": agora()})
    assignments = ", ".join(f"{campo}=?" for campo in campos)
    cur = db.execute(f"UPDATE itens_quantitativo SET {assignments} WHERE id=? AND obra_id=? AND versao=?",
                     (*campos.values(), item_id, obra_id, versao_esperada))
    if cur.rowcount != 1:
        raise RuntimeError("Conflito de versão durante a atualização")
    depois = dict(db.execute("SELECT * FROM itens_quantitativo WHERE id=?", (item_id,)).fetchone())
    db.execute("INSERT INTO auditoria_eventos(obra_id,entidade,entidade_id,acao,antes_json,depois_json,usuario,justificativa,created_at) "
               "VALUES(?,?,?,?,?,?,?,?,?)", (obra_id, "itens_quantitativo", item_id, "ATUALIZAR", json.dumps(antes, default=str),
               json.dumps(depois, default=str), usuario, justificativa, agora()))
    return revisao


def recalcular_orcamento(db: sqlite3.Connection, obra_id: int, revisao_id: int | None = None) -> None:
    db.execute(
        "UPDATE itens_orcamento SET custo_total=ROUND((SELECT quantidade_liquida FROM itens_quantitativo q WHERE q.id=quantitativo_id) "
        "* preco_unitario * (1 + bdi_pct / 100.0), 2), revisao_id=COALESCE(?, revisao_id), updated_at=? WHERE obra_id=?",
        (revisao_id, agora(), obra_id),
    )


def gravar_orcamento(db: sqlite3.Connection, obra_id: int, itens: Iterable[dict[str, Any]], revisao_id: int) -> None:
    for item in itens:
        quant = db.execute("SELECT id,quantidade_liquida FROM itens_quantitativo WHERE obra_id=? AND cod_eap=? AND prancha_referencia=?",
                           (obra_id, item["cod_eap"], item["prancha_referencia"])).fetchone()
        if quant is None:
            raise ValueError(f"Item de orçamento sem quantitativo: {item['cod_eap']}")
        preco, bdi = float(item.get("preco_unitario", 0) or 0), float(item.get("bdi_pct", 0) or 0)
        total = round(float(quant["quantidade_liquida"]) * preco * (1 + bdi / 100), 2)
        db.execute(
            "INSERT INTO itens_orcamento(obra_id,quantitativo_id,revisao_id,codigo_sinapi,centro_custo,fonte_preco,"
            "custo_material,custo_mao_obra,custo_equipamento,preco_unitario,bdi_pct,custo_total,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(obra_id,quantitativo_id) DO UPDATE SET revisao_id=excluded.revisao_id,codigo_sinapi=excluded.codigo_sinapi,"
            "centro_custo=excluded.centro_custo,fonte_preco=excluded.fonte_preco,custo_material=excluded.custo_material,"
            "custo_mao_obra=excluded.custo_mao_obra,custo_equipamento=excluded.custo_equipamento,preco_unitario=excluded.preco_unitario,"
            "bdi_pct=excluded.bdi_pct,custo_total=excluded.custo_total,updated_at=excluded.updated_at",
            (obra_id, quant["id"], revisao_id, item.get("codigo_sinapi", ""), item.get("centro_custo", ""), item.get("fonte_preco", ""),
             float(item.get("custo_material", 0) or 0), float(item.get("custo_mao_obra", 0) or 0), float(item.get("custo_equipamento", 0) or 0),
             preco, bdi, total, agora()),
        )


def exportar_checksum(db: sqlite3.Connection, obra_id: int) -> str:
    rows = [dict(row) for row in db.execute("SELECT cod_eap,descricao,disciplina,unidade,quantidade_liquida,expressao_matematica,prancha_referencia,status,versao FROM itens_quantitativo WHERE obra_id=? ORDER BY id", (obra_id,))]
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def _nome_disciplina(disciplina: str) -> str:
    sem_acento = "".join(c for c in unicodedata.normalize("NFKD", disciplina) if not unicodedata.combining(c))
    nome = re.sub(r"[^A-Z0-9]+", "_", sem_acento.upper()).strip("_")
    return nome or "SEM_DISCIPLINA"


def _escrever_csv(destino: Path, cabecalho: tuple[str, ...], linhas: Iterable[Iterable[Any]]) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", newline="", encoding="utf-8-sig") as arquivo:
        writer = csv.writer(arquivo, delimiter=";")
        writer.writerow(cabecalho)
        writer.writerows(linhas)


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
    linhas_quant = [(r["cod_eap"], r["descricao"], r["disciplina"], r["unidade"], r["quantidade_liquida"], r["prancha_referencia"], r["status"]) for r in itens]
    mestre = base / "QUANTITATIVO_MESTRE.csv"
    _escrever_csv(mestre, COLUNAS_QUANTITATIVO, linhas_quant)
    saidas.append(mestre)
    linhas_orc = [(r["cod_eap"], r["descricao"], r["disciplina"], r["unidade"], r["quantidade_liquida"], r["preco_unitario"] or 0, r["custo_total"] or 0, "Engenharia", r["prancha_referencia"], r["fonte_preco"] or "", r["status"], r["codigo_sinapi"] or "", r["centro_custo"] or "") for r in itens]
    orcamento = base / "ORCAMENTO_BASE_CONSOLIDADO.csv"
    _escrever_csv(orcamento, COLUNAS_ORCAMENTO, linhas_orc)
    saidas.append(orcamento)
    for disciplina in sorted({r["disciplina"] for r in itens}):
        grupo = [r for r in itens if r["disciplina"] == disciplina]
        sufixo = _nome_disciplina(disciplina)
        quant_disc = base / f"QUANTITATIVO_{sufixo}.csv"
        _escrever_csv(quant_disc, COLUNAS_QUANTITATIVO, [(r["cod_eap"], r["descricao"], r["disciplina"], r["unidade"], r["quantidade_liquida"], r["prancha_referencia"], r["status"]) for r in grupo])
        saidas.append(quant_disc)
        memoria = base / f"MEMORIA_CALCULO_{sufixo}.md"
        linhas = [f"# Memória de Cálculo Auditável: {disciplina}", "", f"**Obra:** {obra['nome']}  ", f"**Checksum do quantitativo:** `{exportar_checksum(db, obra_id)}`", "", "---", "", "## 1. Demonstração Matemática Detalhada", ""]
        for r in grupo:
            linhas.extend([f"### {r['cod_eap']} — {r['descricao']}", f"- **Expressão:** `{r['expressao_matematica']}`", f"- **Resultado líquido:** `{r['quantidade_liquida']} {r['unidade']}`", f"- **Prancha:** `{r['prancha_referencia']}`", ""])
        linhas.extend(["## 2. Tabela Consolidada de Quantitativos Físicos de Projeto", "", "| EAP | Serviço | Quantidade líquida | Unidade | Prancha | Status |", "|---|---|---:|---|---|---|"])
        linhas.extend(f"| {r['cod_eap']} | {r['descricao']} | {r['quantidade_liquida']} | {r['unidade']} | {r['prancha_referencia']} | {r['status']} |" for r in grupo)
        linhas.extend(["", "## 3. Tabela Oficial de Serviços para EAP e Cronograma", "", "| EAP | Serviço | Status |", "|---|---|---|", *(f"| {r['cod_eap']} | {r['descricao']} | {r['status']} |" for r in grupo), ""])
        memoria.write_text("\n".join(linhas), encoding="utf-8")
        saidas.append(memoria)
    return saidas
