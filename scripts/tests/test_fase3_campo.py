# -*- coding: utf-8 -*-
"""Testes de Regressão e Validação da Fase 3 — Governança de Campo.

Cobre AUD-001 (Aprovação de FVS e Liberação de Medição)
e AUD-010 (Emissão de RDO, Numeração inicial 001, Integridade e Assinatura).
"""

import os
import shutil
import tempfile
import unittest
import openpyxl

from scripts.common.qualidade_fvs import (
    obter_definicao_fvs,
    avaliar_aprovacao_fvs,
    promover_fvs_governado,
)
from scripts.processar_coleta_campo import (
    processar_ingestao_rdo,
    processar_ingestao_fvs,
    processar_promocao_fvs,
)


class TestFase3FvsGovernanca(unittest.TestCase):
    """Validações de regras de negócio de AUD-001 (Qualidade e FVS)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="teste_fase3_fvs_")
        self.producao_dir = os.path.join(self.temp_dir, "04_PRODUCAO_E_AVANCO")
        os.makedirs(self.producao_dir, exist_ok=True)
        self.config = {
            "sigla_obra": "TESTE",
            "nome_obra": "Obra de Teste Unitário",
        }

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_codigo_fvs_valido_e_invalido(self):
        def_01 = obter_definicao_fvs("FVS-01")
        self.assertEqual(def_01["codigo"], "FVS-01")
        self.assertIn("Topografia", def_01["titulo"])

        with self.assertRaises(ValueError):
            obter_definicao_fvs("FVS-99")

        with self.assertRaises(ValueError):
            obter_definicao_fvs("")

    def test_fvs_submetida_incompleta_rejeita_aprovacao(self):
        # Falta tolerância e responsável
        dados_incompletos = {
            "codigo": "FVS-01",
            "data": "14/09/2026",
            "status": "CONFORME_INFORMADO",
            "itens_conferidos": [
                "Locação do gabarito perimetral de tábua corrida fixado com pontaletes travados e pintados",
            ],
            "assinatura": "token_valido_123",
        }
        res = avaliar_aprovacao_fvs(dados_incompletos)
        self.assertFalse(res["aprovado"])
        self.assertEqual(res["status"], "REPROVADA")
        self.assertFalse(res["liberacao_medicao"])
        self.assertTrue(len(res["motivos"]) > 0)

    def test_fvs_checklist_incompleto_nao_libera_medicao(self):
        def_01 = obter_definicao_fvs("FVS-01")
        itens = def_01["itens_verificacao"]
        # Envia apenas o primeiro item
        dados = {
            "codigo": "FVS-01",
            "data": "14/09/2026",
            "responsavel": "Eng. Fulano de Tal (CREA-1234)",
            "medicao_tolerancia": "Desvio medido: 1.5mm",
            "itens_conferidos": [itens[0]],
            "assinatura": "hash_assinatura_valida_xyz",
            "status": "CONFORME_INFORMADO",
        }
        res = avaliar_aprovacao_fvs(dados)
        self.assertFalse(res["aprovado"])
        self.assertFalse(res["liberacao_medicao"])
        self.assertIn("Checklist incompleto", res["motivos"][0])

    def test_fvs_sem_assinatura_nao_libera_medicao(self):
        def_01 = obter_definicao_fvs("FVS-01")
        dados = {
            "codigo": "FVS-01",
            "data": "14/09/2026",
            "responsavel": "Eng. Fulano de Tal (CREA-1234)",
            "medicao_tolerancia": "Desvio medido: 1.5mm",
            "itens_conferidos": def_01["itens_verificacao"],
            "assinatura": "Pendente",
            "status": "CONFORME_INFORMADO",
        }
        res = avaliar_aprovacao_fvs(dados)
        self.assertFalse(res["aprovado"])
        self.assertFalse(res["liberacao_medicao"])

    def test_fvs_100_porcento_conforme_aprova_e_desbloqueia(self):
        def_01 = obter_definicao_fvs("FVS-01")
        dados = {
            "codigo": "FVS-01",
            "data": "14/09/2026",
            "responsavel": "Eng. Alexandre (CREA-RJ 2026-A)",
            "medicao_tolerancia": "Desvio linear medido = 1.8mm (tolerância máx 3mm)",
            "itens_conferidos": def_01["itens_verificacao"],
            "assinatura": "canvas_base64_data_url_assinado_comprovado",
            "status": "CONFORME_INFORMADO",
        }
        res = promover_fvs_governado(self.temp_dir, self.config, dados)
        self.assertTrue(res["aprovado"])
        self.assertEqual(res["status"], "APROVADA")
        self.assertTrue(res["liberacao_medicao"])

        # Verificar gravação no markdown
        reg_md = os.path.join(self.producao_dir, "FVS", "REGISTRO_INSPECOES_CAMPO.md")
        self.assertTrue(os.path.exists(reg_md))
        with open(reg_md, "r", encoding="utf-8") as f:
            conteudo = f.read()
        self.assertIn("FVS-01", conteudo)
        self.assertIn("Aprovado", conteudo)
        self.assertIn("✅ Desbloqueada", conteudo)
        self.assertIn(res["hash_assinatura"], conteudo)

    def test_fvs_reprovada_bloqueia_medicao(self):
        def_01 = obter_definicao_fvs("FVS-01")
        dados = {
            "codigo": "FVS-01",
            "data": "14/09/2026",
            "responsavel": "Eng. Alexandre (CREA-RJ 2026-A)",
            "medicao_tolerancia": "Desvio linear medido = 8mm (excede tolerância 3mm)",
            "itens_conferidos": def_01["itens_verificacao"],
            "assinatura": "canvas_base64_data_url_assinado",
            "status": "NAO_CONFORME_INFORMADO",
        }
        res = promover_fvs_governado(self.temp_dir, self.config, dados)
        self.assertFalse(res["aprovado"])
        self.assertEqual(res["status"], "REPROVADA")
        self.assertFalse(res["liberacao_medicao"])

        reg_md = os.path.join(self.producao_dir, "FVS", "REGISTRO_INSPECOES_CAMPO.md")
        with open(reg_md, "r", encoding="utf-8") as f:
            conteudo = f.read()
        self.assertIn("🔴 Reprovado", conteudo)
        self.assertIn("⛔ Bloqueada", conteudo)


class TestFase3RdoGovernanca(unittest.TestCase):
    """Validações de regras de negócio de AUD-010 (RDO e integridade de campo)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="teste_fase3_rdo_")
        self.producao_dir = os.path.join(self.temp_dir, "04_PRODUCAO_E_AVANCO")
        os.makedirs(self.producao_dir, exist_ok=True)
        self.config = {
            "sigla_obra": "TESTE",
            "nome_obra": "Obra de Teste Unitário",
            "engenheiro_responsavel": "Eng. Alexandre",
        }

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_primeiro_rdo_inicia_em_001(self):
        # Diretório RDOS vazio
        rdo_data = {
            "data": "14/09/2026",
            "dia": "Segunda-feira",
            "responsavel": "Mestre Carlos",
            "clima_m": "Ensolarado",
            "clima_t": "Ensolarado",
            "ef_prop": 2,
            "ef_terc": 4,
            "h_paral": 0.0,
            "eap": "1.1.1 Locação Inicial",
            "assinatura": "ass_hash_12345",
        }
        res = processar_ingestao_rdo(self.temp_dir, self.config, rdo_data)
        self.assertEqual(res["rdo_numero"], "RDO-001")
        self.assertTrue(os.path.basename(res["arquivo_md"]).startswith("RDO_001_"))
        self.assertEqual(res["status_documento"], "OFICIAL")

        # Segundo RDO deve ser 002
        rdo_data_2 = dict(rdo_data, data="15/09/2026")
        res2 = processar_ingestao_rdo(self.temp_dir, self.config, rdo_data_2)
        self.assertEqual(res2["rdo_numero"], "RDO-002")

    def test_rdo_campos_obrigatorios_ausentes_rejeita(self):
        # Sem data
        with self.assertRaises(ValueError):
            processar_ingestao_rdo(self.temp_dir, self.config, {
                "ef_prop": 2, "ef_terc": 4, "eap": "1.1.1", "responsavel": "Engenheiro"
            })

        # Sem efetivo próprio
        with self.assertRaises(ValueError):
            processar_ingestao_rdo(self.temp_dir, self.config, {
                "data": "14/09/2026", "ef_terc": 4, "eap": "1.1.1", "responsavel": "Engenheiro"
            })

        # Sem EAP
        with self.assertRaises(ValueError):
            processar_ingestao_rdo(self.temp_dir, self.config, {
                "data": "14/09/2026", "ef_prop": 2, "ef_terc": 4, "responsavel": "Engenheiro"
            })

        # Sem responsável
        config_sem_eng = {"sigla_obra": "TESTE"}
        with self.assertRaises(ValueError):
            processar_ingestao_rdo(self.temp_dir, config_sem_eng, {
                "data": "14/09/2026", "ef_prop": 2, "ef_terc": 4, "eap": "1.1.1"
            })

    def test_rdo_sem_assinatura_marca_rascunho(self):
        rdo_data = {
            "data": "14/09/2026",
            "dia": "Segunda-feira",
            "responsavel": "Mestre Carlos",
            "clima_m": "Ensolarado",
            "clima_t": "Ensolarado",
            "ef_prop": 2,
            "ef_terc": 4,
            "h_paral": 0.0,
            "eap": "1.1.1 Locação Inicial",
            "assinatura": "Pendente",
        }
        res = processar_ingestao_rdo(self.temp_dir, self.config, rdo_data)
        self.assertEqual(res["status_documento"], "RASCUNHO")

        with open(res["arquivo_md"], "r", encoding="utf-8") as f:
            conteudo = f.read()
        self.assertIn("RASCUNHO / PENDENTE DE ASSINATURA", conteudo)
        self.assertNotIn("Assinado digitalmente por", conteudo)

    def test_rdo_com_assinatura_registra_evidencia(self):
        rdo_data = {
            "data": "14/09/2026",
            "dia": "Segunda-feira",
            "responsavel": "Eng. Alexandre",
            "clima_m": "Ensolarado",
            "clima_t": "Ensolarado",
            "ef_prop": 3,
            "ef_terc": 5,
            "h_paral": 0.0,
            "eap": "1.1.1 Locação Inicial",
            "assinatura": "token_assinatura_digital_crea_valida",
        }
        res = processar_ingestao_rdo(self.temp_dir, self.config, rdo_data)
        self.assertEqual(res["status_documento"], "OFICIAL")

        with open(res["arquivo_md"], "r", encoding="utf-8") as f:
            conteudo = f.read()
        self.assertIn("Status do Documento:** OFICIAL", conteudo)
        self.assertIn("Assinado digitalmente por Eng. Alexandre", conteudo)
        self.assertIn("Evidência de integridade:", conteudo)


if __name__ == "__main__":
    unittest.main()
