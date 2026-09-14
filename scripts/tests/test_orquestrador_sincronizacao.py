"""Testes automatizados do orquestrador e sincronização bidirecional (AUD-007 e AUD-008)."""

import os
import subprocess
import sys
import unittest
from unittest.mock import patch

from scripts.orquestrar_cronogramas import pipeline_sincronizar, pipeline_gerar_tudo


class OrquestradorSincronizacaoTest(unittest.TestCase):
    def test_aud007_obra_inexistente_encerra_com_codigo_nao_zero(self):
        """Orquestrador deve terminar com código 1 (não zero) ao receber obra inexistente."""
        cmd = [sys.executable, os.path.join("scripts", "orquestrar_cronogramas.py"), "--obra", "__OBRA_INEXISTENTE_TEST__", "--gerar-tudo"]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(res.returncode, 0, "Deveria falhar com código de saída não-zero.")
        self.assertIn("Pasta da obra '__OBRA_INEXISTENTE_TEST__'", res.stdout + res.stderr)

    def test_aud007_falha_etapa_obrigatoria_aborta_pipeline(self):
        """Se o Passo 1 falhar, o pipeline de geração deve parar imediatamente e retornar False."""
        with patch("scripts.orquestrar_cronogramas.run_script") as mock_run:
            # Passo 1 falha
            mock_run.return_value = (False, "Falha simulada no Passo 1")
            sucesso = pipeline_gerar_tudo("OBRA_TMULT")
            self.assertFalse(sucesso)
            # Apenas 1 chamada deve ter ocorrido antes de abortar
            self.assertEqual(mock_run.call_count, 1)

    def test_aud008_sincronizacao_executa_modos_distintos_por_origem(self):
        """Origem 'lob' deve chamar 'lob_para_esteira' e origem 'curto-prazo' deve chamar 'esteira_para_lob'."""
        chamadas_lob = []
        with patch("scripts.orquestrar_cronogramas.run_script") as mock_run:
            mock_run.return_value = (True, "")
            sucesso = pipeline_sincronizar("OBRA_TMULT", origem="lob")
            self.assertTrue(sucesso)
            chamadas_lob = [args for args, _ in mock_run.call_args_list]

        # Verificar se sincronizar_esteira_e_lob.py foi chamado com --modo lob_para_esteira
        chamada_sinc = [c for c in chamadas_lob if c[0] == "sincronizar_esteira_e_lob.py"][0]
        args_passados = chamada_sinc[1]
        self.assertIn("--modo", args_passados)
        idx_modo = args_passados.index("--modo")
        self.assertEqual(args_passados[idx_modo + 1], "lob_para_esteira")

        chamadas_cp = []
        with patch("scripts.orquestrar_cronogramas.run_script") as mock_run:
            mock_run.return_value = (True, "")
            sucesso = pipeline_sincronizar("OBRA_TMULT", origem="curto-prazo")
            self.assertTrue(sucesso)
            chamadas_cp = [args for args, _ in mock_run.call_args_list]

        chamada_sinc_cp = [c for c in chamadas_cp if c[0] == "sincronizar_esteira_e_lob.py"][0]
        args_passados_cp = chamada_sinc_cp[1]
        self.assertIn("--modo", args_passados_cp)
        idx_modo_cp = args_passados_cp.index("--modo")
        self.assertEqual(args_passados_cp[idx_modo_cp + 1], "esteira_para_lob")

        # Garantir que os dois modos foram semântica e comprovadamente distintos
        self.assertNotEqual(args_passados[idx_modo + 1], args_passados_cp[idx_modo_cp + 1])


if __name__ == "__main__":
    unittest.main()
