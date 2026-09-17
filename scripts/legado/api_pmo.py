#!/usr/bin/env python3
"""API local para edição controlada da fonte oficial SQLite do PMO."""
import argparse
import json
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from motor_quantitativos.repositorio.sqlite_repository import atualizar_quantitativo, connect, recalcular_orcamento
from motor_quantitativos.auditoria.trilha_revisoes import criar_backup
from motor_quantitativos.exportadores import exportar_artefatos


class Handler(BaseHTTPRequestHandler):
    db_path = "data/pmo_virtual.sqlite"
    api_key = ""
    usuario = "web-local"
    backup_dir = None

    def _responder(self, status: int, payload: dict | None = None) -> None:
        corpo = json.dumps(payload or {}, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "http://localhost:3000")
        self.send_header("Access-Control-Allow-Methods", "GET, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-PMO-API-Key")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        if status != 204:
            self.wfile.write(corpo)

    def _autorizado(self) -> bool:
        return bool(self.api_key) and secrets.compare_digest(self.headers.get("X-PMO-API-Key", ""), self.api_key)

    def _exigir_autorizacao(self) -> bool:
        if self._autorizado():
            return True
        self._responder(401, {"erro": "chave de API ausente ou inválida"})
        return False

    def do_OPTIONS(self) -> None:
        self._responder(204)

    def do_GET(self) -> None:
        if not self._exigir_autorizacao():
            return
        url = urlparse(self.path)
        if url.path != "/api/quantitativos":
            self._responder(404, {"erro": "rota não encontrada"})
            return
        parametros = parse_qs(url.query)
        obra = parametros.get("obra_id", [None])[0]
        if obra is None:
            self._responder(400, {"erro": "obra_id é obrigatório"})
            return
        try:
            limite = min(max(int(parametros.get("limite", [100])[0]), 1), 500)
            deslocamento = max(int(parametros.get("deslocamento", [0])[0]), 0)
            db = connect(self.db_path)
            try:
                itens = db.execute("SELECT * FROM itens_quantitativo WHERE obra_id=? ORDER BY cod_eap,prancha_referencia LIMIT ? OFFSET ?", (int(obra), limite, deslocamento)).fetchall()
            finally:
                db.close()
            self._responder(200, {"itens": [dict(item) for item in itens]})
        except ValueError:
            self._responder(400, {"erro": "obra_id inválido"})

    def do_PATCH(self) -> None:
        if not self._exigir_autorizacao():
            return
        partes = [p for p in urlparse(self.path).path.split("/") if p]
        if len(partes) != 4 or partes[:2] != ["api", "quantitativo"]:
            self._responder(404, {"erro": "rota não encontrada"})
            return
        try:
            tamanho = int(self.headers.get("Content-Length", "0"))
            if tamanho <= 0 or tamanho > 100_000:
                raise ValueError("Corpo da requisição inválido")
            payload = json.loads(self.rfile.read(tamanho))
            justificativa = payload.get("justificativa", "")
            versao = payload.get("versao_esperada")
            if versao is None:
                raise ValueError("versao_esperada é obrigatória")
            backup = criar_backup(self.db_path, self.backup_dir)
            db = connect(self.db_path)
            try:
                revisao = atualizar_quantitativo(db, int(partes[2]), int(partes[3]), payload.get("alteracoes", {}),
                                                  self.usuario, justificativa, int(versao))
                recalcular_orcamento(db, int(partes[2]), revisao)
                exportacoes = exportar_artefatos(db, int(partes[2]))
                db.commit()
            except Exception:
                db.rollback()
                raise
            finally:
                db.close()
            self._responder(200, {"status": "atualizado", "revisao_id": revisao, "backup": str(backup), "exportacoes": [str(p) for p in exportacoes]})
        except RuntimeError as erro:
            self._responder(409, {"erro": str(erro)})
        except (ValueError, json.JSONDecodeError) as erro:
            self._responder(400, {"erro": str(erro)})
        except Exception as erro:
            self._responder(500, {"erro": "falha interna", "detalhe": str(erro)})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/pmo_virtual.sqlite")
    parser.add_argument("--host", default="127.0.0.1", help="A API é local; não exponha sem autenticação corporativa.")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--api-key", required=True, help="Chave local da interface; não registre no Git.")
    parser.add_argument("--usuario", default="web-local", help="Identidade auditada desta instância local.")
    parser.add_argument("--backup-dir", help="Diretório dos snapshots SQLite; padrão: data/backups.")
    args = parser.parse_args()
    Handler.db_path, Handler.api_key, Handler.usuario, Handler.backup_dir = args.db, args.api_key, args.usuario, args.backup_dir
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()
