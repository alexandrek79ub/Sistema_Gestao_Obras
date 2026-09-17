import csv
import json
import tempfile
import unittest
from pathlib import Path

from gerar_lista_desenhos import exportar_lista, importar_desenhos, limpar_titulo, normalizar_revisao
from motor_quantitativos.repositorio.sqlite_repository import connect


class ListaDesenhosTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name) / "01_ENGENHARIA_E_PROJETOS"
        self.pasta = self.raiz / "EDIFICIO_ADMINISTRATIVO"
        self.carimbos = self.pasta / "_carimbos_extraidos"
        self.carimbos.mkdir(parents=True)
        self.db_path = Path(self.tmp.name) / "pmo.sqlite"

    def tearDown(self):
        self.tmp.cleanup()

    def _gravar_metadados(self, itens):
        for item in itens:
            (self.pasta / item["pdf"]).write_bytes(b"pdf de teste")
            (self.carimbos / f"{Path(item['pdf']).stem}_carimbo.png").write_bytes(b"png")
        (self.carimbos / "carimbos_metadados.json").write_text(
            json.dumps(itens, ensure_ascii=False), encoding="utf-8"
        )

    def test_revisao_superior_se_torna_vigente_e_exportacao_prioriza_ultima(self):
        self._gravar_metadados([{
            "pdf": "EGS-051 rev.A.pdf", "texto": "Título: Fundação principal",
            "carimbo_img": str(self.carimbos / "EGS-051 rev.A_carimbo.png"),
        }])
        importar_desenhos("OBRA_TESTE", self.pasta, self.db_path)
        self._gravar_metadados([{
            "pdf": "EGS-051 rev.A.pdf", "texto": "Título: Fundação principal",
            "carimbo_img": str(self.carimbos / "EGS-051 rev.A_carimbo.png"),
        }, {
            "pdf": "EGS-051 rev.B.pdf", "texto": "Título: Fundação revisada",
            "carimbo_img": str(self.carimbos / "EGS-051 rev.B_carimbo.png"),
        }])
        importar_desenhos("OBRA_TESTE", self.pasta, self.db_path)
        exportar_lista("OBRA_TESTE", self.db_path, self.raiz)
        exportar_lista("OBRA_TESTE", self.db_path, self.raiz / "auditoria", incluir_superadas=True)

        db = connect(self.db_path)
        try:
            linhas = db.execute("SELECT revisao,status FROM lista_desenhos ORDER BY revisao").fetchall()
            self.assertEqual([(linha["revisao"], linha["status"]) for linha in linhas], [("A", "SUPERADA"), ("B", "VIGENTE")])
            self.assertEqual(db.execute("SELECT COUNT(*) FROM lista_desenhos").fetchone()[0], 2)
        finally:
            db.close()
        with (self.raiz / "LISTA_DE_DESENHOS.csv").open(encoding="utf-8-sig", newline="") as arquivo:
            linhas_csv = list(csv.DictReader(arquivo, delimiter=";"))
        self.assertEqual([(linha["revisao"], linha["status"]) for linha in linhas_csv], [("B", "VIGENTE")])
        self.assertIn("Priorizar para execução", linhas_csv[0]["orientacao"])

    def test_revisao_ambigua_exige_confirmacao(self):
        self._gravar_metadados([{
            "pdf": "EGS-052 rev.R1.pdf", "texto": "Título: Desenho sem revisão comparável",
        }])
        importar_desenhos("OBRA_TESTE", self.pasta, self.db_path)
        db = connect(self.db_path)
        try:
            linha = db.execute("SELECT titulo_status,status FROM lista_desenhos").fetchone()
            self.assertEqual((linha["titulo_status"], linha["status"]), ("EXTRAIDO", "PENDENTE_REVISAO"))
        finally:
            db.close()

    def test_normalizacao_nao_compara_familias_distintas(self):
        self.assertEqual(normalizar_revisao("Rev. 02"), ("2", 2, "NUMERICA"))
        self.assertEqual(normalizar_revisao("b"), ("B", 2, "ALFABETICA"))
        self.assertIsNone(normalizar_revisao("R1"))

    def test_texto_com_caractere_de_controle_fica_pendente(self):
        self.assertEqual(limpar_titulo("5HODomR\x03GR\x03DoR"), ("Título não identificado", "PENDENTE_REVISAO"))

    def test_titulo_repetido_em_pranchas_distintas_requer_revisao(self):
        self._gravar_metadados([
            {"pdf": "EGS-060 rev.A.pdf", "texto": "CANAL DE ACESSO"},
            {"pdf": "EGS-061 rev.A.pdf", "texto": "CANAL DE ACESSO"},
        ])
        importar_desenhos("OBRA_TESTE", self.pasta, self.db_path)
        db = connect(self.db_path)
        try:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM lista_desenhos WHERE titulo_status='PENDENTE_REVISAO'").fetchone()[0], 2)
        finally:
            db.close()


if __name__ == "__main__":
    unittest.main()
