import http.client
import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path

from api_pmo import Handler
from migrar_quantitativo_sqlite import importar_json_inicial
from motor_quantitativos.db import (atualizar_quantitativo, connect, exportar_artefatos, garantir_obra,
                                    gravar_orcamento, recalcular_orcamento, registrar_revisao,
                                    substituir_quantitativos)


class MotorQuantitativosTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name) / "obra"
        self.db = connect(Path(self.tmp.name) / "teste.sqlite")
        self.obra = garantir_obra(self.db, "TESTE", "Obra Teste", str(self.base))
        revisao = registrar_revisao(self.db, self.obra, "QUANTITATIVO", "teste")
        self.item = substituir_quantitativos(self.db, self.obra, [{
            "cod_eap": "1.3.11", "descricao": "Impermeabilização", "disciplina": "Fundação",
            "unidade": "m²", "quantidade_liquida": 12.5, "expressao_matematica": "5 * 2.5",
            "prancha_referencia": "F-01", "status": "LEVANTADO",
        }], revisao)[0]
        revisao_orc = registrar_revisao(self.db, self.obra, "ORCAMENTO", "teste")
        gravar_orcamento(self.db, self.obra, [{
            "cod_eap": "1.3.11", "prancha_referencia": "F-01", "preco_unitario": 20,
            "bdi_pct": 10, "codigo_sinapi": "123", "centro_custo": "CC-01", "fonte_preco": "SINAPI",
        }], revisao_orc)
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_schema_mantem_quantidade_liquida_sem_perdas(self):
        row = self.db.execute("SELECT quantidade_liquida,status FROM itens_quantitativo WHERE id=?", (self.item,)).fetchone()
        self.assertEqual((row[0], row[1]), (12.5, "LEVANTADO"))
        self.assertFalse(self.db.execute("SELECT 1 FROM pragma_table_info('itens_quantitativo') WHERE name='taxa_perda'").fetchone())
        self.assertEqual(self.db.execute("SELECT versao FROM schema_migrations").fetchone()[0], 1)

    def test_edicao_auditavel_recalcula_orcamento_e_exporta(self):
        revisao = atualizar_quantitativo(self.db, self.obra, self.item, {"quantidade_liquida": 14.0}, "teste-web", "Correção da prancha", 1)
        recalcular_orcamento(self.db, self.obra, revisao)
        arquivos = exportar_artefatos(self.db, self.obra)
        self.db.commit()
        linha_atualizada = self.db.execute("SELECT quantidade_liquida,versao FROM itens_quantitativo WHERE id=?", (self.item,)).fetchone()
        self.assertEqual((linha_atualizada["quantidade_liquida"], linha_atualizada["versao"]), (14.0, 2))
        self.assertEqual(self.db.execute("SELECT custo_total FROM itens_orcamento WHERE quantitativo_id=?", (self.item,)).fetchone()[0], 308.0)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM auditoria_eventos").fetchone()[0], 1)
        self.assertTrue((self.base / "QUANTITATIVO_MESTRE.csv").exists())
        self.assertTrue((self.base / "ORCAMENTO_BASE_CONSOLIDADO.csv").exists())
        self.assertTrue(any(path.name.startswith("MEMORIA_CALCULO_") for path in arquivos))
        self.assertIn("14.0", (self.base / "ORCAMENTO_BASE_CONSOLIDADO.csv").read_text(encoding="utf-8-sig"))

    def test_rejeita_conflito_sem_justificativa_ou_versao_atual(self):
        with self.assertRaises(ValueError):
            atualizar_quantitativo(self.db, self.obra, self.item, {"quantidade_liquida": 14.0}, "teste", "", 1)
        atualizar_quantitativo(self.db, self.obra, self.item, {"quantidade_liquida": 14.0}, "teste", "Ajuste confirmado", 1)
        with self.assertRaises(RuntimeError):
            atualizar_quantitativo(self.db, self.obra, self.item, {"quantidade_liquida": 15.0}, "teste", "Tentativa antiga", 1)

    def test_importacao_inicial_nao_sobrescreve_banco_sem_flag_explicita(self):
        arquivo_json = Path(self.tmp.name) / "entrada.json"
        destino = Path(self.tmp.name) / "exportacoes"
        arquivo_json.write_text(json.dumps({"projeto": "Importação Teste", "base_dir": str(destino), "disciplinas": {
            "fundacao": {"titulo": "Fundação", "pranchas_ref": "F-01", "itens_orcamento": [{
                "codigo_eap": "1.3.11", "descricao": "Impermeabilização", "unidade": "m²",
                "preco_unitario": 20, "equacoes": [{"expressao_matematica": "5 * 2.5"}],
            }]}}}, ensure_ascii=False), encoding="utf-8")
        banco = Path(self.tmp.name) / "importacao.sqlite"
        saidas = importar_json_inicial(str(arquivo_json), str(banco))
        self.assertTrue(any(arquivo.name == "ORCAMENTO_BASE_CONSOLIDADO.csv" for arquivo in saidas))
        with self.assertRaises(ValueError):
            importar_json_inicial(str(arquivo_json), str(banco))

    def test_api_exige_chave_versao_e_regenera_exportacoes(self):
        anteriores = Handler.db_path, Handler.api_key, Handler.usuario, Handler.backup_dir
        Handler.db_path, Handler.api_key, Handler.usuario, Handler.backup_dir = str(Path(self.tmp.name) / "teste.sqlite"), "segredo", "engenheiro-web", str(Path(self.tmp.name) / "backups")
        servidor = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=servidor.serve_forever, daemon=True)
        thread.start()
        try:
            porta = servidor.server_address[1]
            conexao = http.client.HTTPConnection("127.0.0.1", porta, timeout=3)
            conexao.request("GET", f"/api/quantitativos?obra_id={self.obra}")
            self.assertEqual(conexao.getresponse().status, 401)
            payload = json.dumps({"alteracoes": {"quantidade_liquida": 14}, "justificativa": "Revisão conferida", "versao_esperada": 1})
            conexao.request("PATCH", f"/api/quantitativo/{self.obra}/{self.item}", body=payload,
                             headers={"Content-Type": "application/json", "X-PMO-API-Key": "segredo"})
            self.assertEqual(conexao.getresponse().status, 200)
            self.assertTrue((self.base / "ORCAMENTO_BASE_CONSOLIDADO.csv").exists())
            self.assertEqual(len(list((Path(self.tmp.name) / "backups").glob("*.sqlite"))), 1)
        finally:
            servidor.shutdown()
            servidor.server_close()
            thread.join(timeout=3)
            Handler.db_path, Handler.api_key, Handler.usuario, Handler.backup_dir = anteriores


if __name__ == "__main__":
    unittest.main()
