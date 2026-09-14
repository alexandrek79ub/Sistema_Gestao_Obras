# -*- coding: utf-8 -*-
"""Testes de Regressão da Fase 4 / AUD-004: Veracidade dos painéis e motores.

Valida a eliminação de fallbacks específicos da OBRA_TMULT em scripts/gerar_fluxo_caixa.py,
a parametrização legítima via config_obra.json e o isolamento entre múltiplas obras.
"""

import os
import sys
import unittest
import tempfile
import shutil
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scripts.gerar_fluxo_caixa import carregar_dados_cronograma, modelar_fluxo_caixa


class TestFase4Aud004FluxoCaixa(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _criar_cronograma_csv(self, vendas_por_mes):
        caminho = os.path.join(self.temp_dir, "CRONOGRAMA_TESTE.csv")
        data = {
            "Código EAP": ["1.1.1", "2.1.1"],
            "Item / Descrição": ["Serviço A", "Serviço B"],
            "Preço Total Turnkey (R$)": [100000.0, 100000.0],
        }
        for m, v in enumerate(vendas_por_mes, start=1):
            data[f"R$ Mês {m}"] = [v / 2.0, v / 2.0]
        df = pd.DataFrame(data)
        df.to_csv(caminho, sep=";", index=False, encoding="utf-8")
        return caminho

    def test_obra_sem_administracao_local_nao_herda_custos_tmult(self):
        """Obra sem itens de administração local deve resultar em c_g=0, c_v=0, etc.

        e não herdar R$ 29.300,00 ou R$ 23.009,33 da TMULT.
        """
        cronograma_csv = self._criar_cronograma_csv([50000.0, 50000.0])
        config_obra_vazia = {
            "nome_obra": "Obra Nova Teste",
            "sigla_obra": "TESTE",
            "administracao_local": [],
            "parametros_fluxo_caixa": {
                "retencao_pct": 0.05,
                "adiantamento_pct": 0.0,
                "aliquota_impostos_pct": 0.05,
            },
        }

        vendas_m, diretos_m, tot_venda, tot_cd = carregar_dados_cronograma(
            cronograma_csv, prazo_meses=2, bdi_servico=0.25, bdi_equip=0.15, config=config_obra_vazia
        )
        fluxo = modelar_fluxo_caixa(
            vendas_m, diretos_m, tot_venda, tot_cd, config_obra_vazia, prazo_meses=2
        )

        # Custo de gestão e vivência devem ser exatamente 0.0, e não os valores da TMULT
        self.assertEqual(fluxo["des_mo_gestao"][1], 0.0)
        self.assertEqual(fluxo["des_vivencia"][1], 0.0)
        self.assertEqual(fluxo["des_locacoes"][1], 0.0)
        self.assertEqual(fluxo["des_contas"][1], 0.0)

    def test_obra_com_venda_similar_nao_recebe_calibracao_tmult_sem_config(self):
        """Uma obra qualquer com valor próximo a 1.660.762,28 não pode sofrer

        calibração forçada para 1.314.562,67 se não tiver configurado em config_obra.json.
        """
        # 6 meses somando exatamente 1.660.762,28
        parcela = round(1660762.28 / 6, 2)
        vendas = [parcela] * 5 + [round(1660762.28 - (parcela * 5), 2)]
        cronograma_csv = self._criar_cronograma_csv(vendas)

        config_sem_alvo = {
            "nome_obra": "Obra Segunda",
            "sigla_obra": "SEGUNDA",
            "parametros_fluxo_caixa": {},
        }

        vendas_m, diretos_m, tot_venda, tot_cd = carregar_dados_cronograma(
            cronograma_csv, prazo_meses=6, bdi_servico=0.2717, bdi_equip=0.15, config=config_sem_alvo
        )

        # O custo direto não deve ser forçado para 1314562.67
        self.assertNotEqual(tot_cd, 1314562.67)
        self.assertEqual(tot_cd, sum(diretos_m.values()))

    def test_obra_com_parametros_legitimos_aplica_alvo_e_particao(self):
        """Quando a obra configura total_custo_direto_alvo e particao customizada em

        config_obra.json, o motor aplica os parâmetros da obra ativa.
        """
        cronograma_csv = self._criar_cronograma_csv([100000.0, 100000.0])
        config_custom = {
            "nome_obra": "Obra Parametrizada",
            "sigla_obra": "PARAM",
            "parametros_fluxo_caixa": {
                "total_custo_direto_alvo": 150000.0,
                "particao_mo_pct": 0.40,
                "particao_mat_pct": 0.60,
                "retencao_pct": 0.05,
            },
            "administracao_local": [
                {"eap": "1.0.1", "custo_unitario": 5000.0},
                {"eap": "1.0.5", "custo_unitario": 3000.0},
            ],
        }

        vendas_m, diretos_m, tot_venda, tot_cd = carregar_dados_cronograma(
            cronograma_csv, prazo_meses=2, bdi_servico=0.25, bdi_equip=0.15, config=config_custom
        )

        self.assertEqual(tot_cd, 150000.0)
        self.assertEqual(sum(diretos_m.values()), 150000.0)

        fluxo = modelar_fluxo_caixa(
            vendas_m, diretos_m, tot_venda, tot_cd, config_custom, prazo_meses=2
        )

        self.assertEqual(fluxo["des_mo_gestao"][1], 5000.0)
        self.assertEqual(fluxo["des_vivencia"][1], 3000.0)


if __name__ == "__main__":
    unittest.main()
