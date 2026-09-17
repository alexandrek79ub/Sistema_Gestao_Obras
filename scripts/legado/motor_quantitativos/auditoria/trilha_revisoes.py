import sqlite3
from datetime import datetime, timezone
from pathlib import Path

def agora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def registrar_revisao(db: sqlite3.Connection, obra_id: int, tipo: str, origem: str,
                      usuario: str = "motor-python", justificativa: str = "") -> int:
    if tipo not in {"QUANTITATIVO", "ORCAMENTO"}:
        raise ValueError("Tipo de revisão inválido")
    cur = db.execute(
        "INSERT INTO revisoes(obra_id,tipo,usuario,justificativa,origem,created_at) VALUES(?,?,?,?,?,?)",
        (obra_id, tipo, usuario.strip() or "motor-python", justificativa.strip() or "Atualização automatizada", origem, agora()),
    )
    return int(cur.lastrowid)

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
