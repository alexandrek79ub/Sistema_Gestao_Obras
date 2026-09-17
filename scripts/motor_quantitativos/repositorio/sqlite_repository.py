import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from motor_quantitativos.domain.modelos import STATUS_QUANTITATIVO
from motor_quantitativos.auditoria.trilha_revisoes import registrar_revisao


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
        cia TEXT NOT NULL DEFAULT '',
        element_type TEXT NOT NULL DEFAULT '',
        element_id TEXT NOT NULL DEFAULT '',
        rule_id TEXT NOT NULL DEFAULT '',
        rule_version INTEGER NOT NULL DEFAULT 0,
        evidence_json TEXT NOT NULL DEFAULT '[]',
        source_revision TEXT NOT NULL DEFAULT '',
        versao INTEGER NOT NULL DEFAULT 1,
        updated_at TEXT NOT NULL,
        UNIQUE(obra_id, cod_eap, prancha_referencia, element_id, rule_id)
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
    novas_colunas = {
        "cia": "TEXT NOT NULL DEFAULT ''",
        "element_type": "TEXT NOT NULL DEFAULT ''",
        "element_id": "TEXT NOT NULL DEFAULT ''",
        "rule_id": "TEXT NOT NULL DEFAULT ''",
        "rule_version": "INTEGER NOT NULL DEFAULT 0",
        "evidence_json": "TEXT NOT NULL DEFAULT '[]'",
        "source_revision": "TEXT NOT NULL DEFAULT ''",
    }
    for coluna, definicao in novas_colunas.items():
        if not _tem_coluna(db, "itens_quantitativo", coluna):
            db.execute(f"ALTER TABLE itens_quantitativo ADD COLUMN {coluna} {definicao}")
    db.execute("INSERT OR IGNORE INTO schema_migrations(versao,aplicada_em) VALUES(?,?)", (2, agora()))
    if not db.execute("SELECT 1 FROM schema_migrations WHERE versao=3").fetchone():
        _migrar_chave_quantitativo_por_elemento(db)
        db.execute("INSERT INTO schema_migrations(versao,aplicada_em) VALUES(?,?)", (3, agora()))


def _migrar_chave_quantitativo_por_elemento(db: sqlite3.Connection) -> None:
    """Preserva os itens existentes e passa a identificar cada linha pelo elemento e regra."""
    db.execute("PRAGMA foreign_keys=OFF")
    try:
        db.executescript("""
        ALTER TABLE itens_orcamento RENAME TO itens_orcamento_v2;
        ALTER TABLE itens_quantitativo RENAME TO itens_quantitativo_v2;
        CREATE TABLE itens_quantitativo (
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
            rfi TEXT NOT NULL DEFAULT '', observacao TEXT NOT NULL DEFAULT '', cia TEXT NOT NULL DEFAULT '',
            element_type TEXT NOT NULL DEFAULT '', element_id TEXT NOT NULL DEFAULT '',
            rule_id TEXT NOT NULL DEFAULT '', rule_version INTEGER NOT NULL DEFAULT 0,
            evidence_json TEXT NOT NULL DEFAULT '[]', source_revision TEXT NOT NULL DEFAULT '',
            versao INTEGER NOT NULL DEFAULT 1, updated_at TEXT NOT NULL,
            UNIQUE(obra_id, cod_eap, prancha_referencia, element_id, rule_id)
        );
        INSERT INTO itens_quantitativo SELECT * FROM itens_quantitativo_v2;
        CREATE TABLE itens_orcamento (
            id INTEGER PRIMARY KEY,
            obra_id INTEGER NOT NULL REFERENCES obras(id),
            quantitativo_id INTEGER NOT NULL REFERENCES itens_quantitativo(id),
            revisao_id INTEGER REFERENCES revisoes(id),
            codigo_sinapi TEXT NOT NULL DEFAULT '', centro_custo TEXT NOT NULL DEFAULT '', fonte_preco TEXT NOT NULL DEFAULT '',
            custo_material REAL NOT NULL DEFAULT 0, custo_mao_obra REAL NOT NULL DEFAULT 0,
            custo_equipamento REAL NOT NULL DEFAULT 0, bdi_pct REAL NOT NULL DEFAULT 0,
            preco_unitario REAL NOT NULL DEFAULT 0, custo_total REAL NOT NULL DEFAULT 0, updated_at TEXT NOT NULL,
            UNIQUE(obra_id, quantitativo_id)
        );
        INSERT INTO itens_orcamento SELECT * FROM itens_orcamento_v2;
        DROP TABLE itens_orcamento_v2;
        DROP TABLE itens_quantitativo_v2;
        CREATE INDEX IF NOT EXISTS idx_quant_obra_eap ON itens_quantitativo(obra_id, cod_eap);
        CREATE INDEX IF NOT EXISTS idx_orc_obra ON itens_orcamento(obra_id);
        """)
    finally:
        db.execute("PRAGMA foreign_keys=ON")


def connect(path: str | Path) -> sqlite3.Connection:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(path))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("PRAGMA journal_mode = WAL")
    aplicar_migracoes(db)
    return db


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


def substituir_quantitativos(db: sqlite3.Connection, obra_id: int, itens: Iterable[dict[str, Any]],
                             revisao_id: int) -> list[int]:
    """Uso exclusivo da importação inicial ou da reimportação explicitamente autorizada."""
    ids: list[int] = []
    for item in itens:
        valores = (
            obra_id, revisao_id, item["cod_eap"], item["descricao"], item["disciplina"], item["unidade"],
            float(item["quantidade_liquida"]), item["expressao_matematica"], item["prancha_referencia"],
            item.get("status", "LEVANTADO"), item.get("rfi", ""), item.get("observacao", ""),
            item.get("cia", ""), item.get("element_type", ""), item.get("element_id", ""),
            item.get("rule_id", ""), int(item.get("rule_version", 0) or 0), item.get("evidence_json", "[]"),
            item.get("source_revision", ""), agora(),
        )
        db.execute(
            "INSERT INTO itens_quantitativo(obra_id,revisao_id,cod_eap,descricao,disciplina,unidade,quantidade_liquida,"
            "expressao_matematica,prancha_referencia,status,rfi,observacao,cia,element_type,element_id,rule_id,rule_version,evidence_json,source_revision,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(obra_id,cod_eap,prancha_referencia,element_id,rule_id) DO UPDATE SET revisao_id=excluded.revisao_id,"
            "descricao=excluded.descricao,disciplina=excluded.disciplina,unidade=excluded.unidade,"
            "quantidade_liquida=excluded.quantidade_liquida,expressao_matematica=excluded.expressao_matematica,"
            "status=excluded.status,rfi=excluded.rfi,observacao=excluded.observacao,cia=excluded.cia,"
            "element_type=excluded.element_type,element_id=excluded.element_id,rule_id=excluded.rule_id,"
            "rule_version=excluded.rule_version,evidence_json=excluded.evidence_json,source_revision=excluded.source_revision,"
            "versao=itens_quantitativo.versao+1,updated_at=excluded.updated_at",
            valores,
        )
        ids.append(int(db.execute(
            "SELECT id FROM itens_quantitativo WHERE obra_id=? AND cod_eap=? AND prancha_referencia=? AND element_id=? AND rule_id=?",
            (obra_id, item["cod_eap"], item["prancha_referencia"], item.get("element_id", ""), item.get("rule_id", "")),
        ).fetchone()[0]))
    return ids


def persistir_itens_quantificados(db: sqlite3.Connection, obra_id: int, itens: Iterable[Any],
                                 revisao_id: int, prancha_referencia: str = "",
                                 disciplina: str = "") -> list[int]:
    """Persiste saídas de ``QuantifiedItem`` sem introduzir preço ou perda."""
    payload = []
    for item in itens:
        payload.append({
            "cod_eap": item.cod_eap,
            "descricao": item.description,
            "disciplina": disciplina or item.rule_id.split(".", 1)[0],
            "unidade": item.unit,
            "quantidade_liquida": item.quantity_net,
            "expressao_matematica": item.expression,
            "prancha_referencia": prancha_referencia or item.source_file,
            "status": item.status,
            "cia": item.cia,
            "element_type": item.element_type,
            "element_id": item.element_ids[0] if item.element_ids else "",
            "rule_id": item.rule_id,
            "rule_version": item.rule_version,
            "evidence_json": json.dumps(item.evidence_ids, ensure_ascii=False),
            "source_revision": item.source_revision,
        })
    return substituir_quantitativos(db, obra_id, payload, revisao_id)


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
