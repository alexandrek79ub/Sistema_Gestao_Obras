"""Testes de mesa para a persistência atômica compartilhada."""

import json
import os
import tempfile
import unittest

from scripts.common.persistencia import bloquear_recurso, salvar_json_atomico, salvar_texto_atomico


class PersistenciaAtomicaTest(unittest.TestCase):
    def test_promocao_atomica_preserva_conteudo_integral(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = os.path.join(diretorio, "artefato.json")
            with bloquear_recurso(diretorio, "artefato"):
                salvar_json_atomico(caminho, {"versao": 1, "itens": ["A", "B"]})
            with open(caminho, encoding="utf-8") as arquivo:
                self.assertEqual(json.load(arquivo)["itens"], ["A", "B"])
            self.assertFalse(any(nome.endswith(".tmp") for nome in os.listdir(diretorio)))

    def test_lock_e_escrita_temporaria_nao_promovem_arquivo_parcial(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = os.path.join(diretorio, "registro.md")
            with bloquear_recurso(diretorio, "registro"):
                salvar_texto_atomico(caminho, "versao completa")
                self.assertTrue(os.path.exists(os.path.join(diretorio, ".registro.lock")))
            self.assertFalse(os.path.exists(os.path.join(diretorio, ".registro.lock")))
            with open(caminho, encoding="utf-8") as arquivo:
                self.assertEqual(arquivo.read(), "versao completa")


if __name__ == "__main__":
    unittest.main()
