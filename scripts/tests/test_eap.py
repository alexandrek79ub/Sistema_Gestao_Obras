"""Testes de conformidade e governança da EAP (AUD-003)."""

import unittest
from scripts.common.eap import (
    classificar_codigo_eap,
    determinar_distribuicao_canonica,
    verificar_violacao_portoes,
    PORTAO_1_FUNDACAO,
    PORTAO_2_ESTRUTURA,
    PORTAO_3_HIDRAULICA,
    PORTAO_4_ACABAMENTO,
    MACROETAPAS_EAP,
)


class EAPGovernancaTest(unittest.TestCase):
    def test_classificacao_codigos_oficiais_indice_mestre(self):
        """Todos os níveis oficiais (1.0 a 5.1) devem ser classificados com suas disciplinas correspondentes."""
        casos = [
            ("1.0", "Administração Local e Canteiro"),
            ("1.1.1", "Serviços Preliminares, Legalização e Mobilização"),
            ("1.2.1", "Terraplenagem e Obras de Contenção"),
            ("1.3.11", "Infraestrutura e Fundações"),
            ("1.4.12", "Superestrutura"),
            ("2.1.8", "Alvenaria, Vedações Verticais e Acabamentos Internos"),
            ("2.2.8", "Cobertura, Fachadas e Fechamento Externo"),
            ("3.1.9", "Instalações Elétricas, Telecomunicações e SPDA"),
            ("3.2.7", "Instalações Hidrossanitárias, Gás e Drenagem"),
            ("4.1.2", "Sistemas Especiais"),
            ("4.2.1", "Urbanização Externa e Lazer"),
            ("5.1.3", "Encerramento, Comissionamento e Databook"),
        ]
        for cod, disciplina_esperada in casos:
            res = classificar_codigo_eap(cod)
            self.assertTrue(res["valido"], f"Código {cod} deveria ser válido")
            self.assertEqual(res["disciplina"], disciplina_esperada, f"Disciplina incorreta para {cod}")
            self.assertEqual(res["tipo"], "CODIGO_EAP_SERVICO")

    def test_codigo_desconhecido_gera_diagnostico_explicito(self):
        """Códigos inexistentes ou fora da taxonomia oficial geram diagnóstico explícito de advertência."""
        for cod_invalido in ["9.9.9", "X.Y.Z", "0.0.1", "6.1.1"]:
            res = classificar_codigo_eap(cod_invalido)
            self.assertFalse(res["valido"])
            self.assertIsNotNone(res["diagnostico"])
            self.assertIn("não pertence a nenhuma macroetapa", res["diagnostico"])

            pesos, aviso = determinar_distribuicao_canonica(cod_invalido, prazo_meses=6)
            self.assertIsNotNone(aviso)
            self.assertIn("não catalogado", aviso)

    def test_regras_obsoletas_de_prefixo_eliminadas(self):
        """Garante que 1.1 NÃO é mais tratado como infraestrutura e 1.2 NÃO é tratado como supraestrutura."""
        # Na regra obsoleta, 1.1 era 100% mês 1 como 'infra' e 1.2 era 100% mês 2 como 'supraestrutura'.
        # Na EAP canônica: 1.3 é Infraestrutura e 1.4 é Superestrutura.
        res_1_3 = classificar_codigo_eap("1.3.1")
        self.assertEqual(res_1_3["disciplina"], "Infraestrutura e Fundações")
        self.assertEqual(res_1_3["macroetapa"], "1.3")

        res_1_4 = classificar_codigo_eap("1.4.1")
        self.assertEqual(res_1_4["disciplina"], "Superestrutura")
        self.assertEqual(res_1_4["macroetapa"], "1.4")

        # 1.1 é Preliminares e 1.2 é Terraplenagem
        self.assertEqual(classificar_codigo_eap("1.1")["disciplina"], "Serviços Preliminares, Legalização e Mobilização")
        self.assertEqual(classificar_codigo_eap("1.2")["disciplina"], "Terraplenagem e Obras de Contenção")

    def test_quatro_portoes_interdisciplinares_validacao(self):
        """Verifica a detecção de conformidade e violação para os 4 portões oficiais."""
        # Cenário 1: Rede em conformidade com os 4 portões
        rede_valida = {
            "1.3.11": ["1.3.10"],
            "1.3.13": ["1.3.11"],       # Portão 1: Reaterro após impermeabilização
            "1.4.12": ["1.4.11"],
            "3.1.7": ["1.4.12"],        # Portão 2: Prumada elétrica após desforma
            "3.2.8": ["1.4.12"],        # Portão 2: Prumada hidráulica após desforma
            "3.2.7": ["3.2.5"],
            "2.1.2": ["3.2.7"],         # Portão 3: Chapisco após teste hidrostático
            "2.1.8": ["2.1.7"],         # Pintura interna 1ª demão
            "3.1.9": ["2.1.8"],         # Portão 4: Acabamento elétrico após pintura
            "3.2.11": ["2.1.8"],        # Portão 4: Metais nobres após pintura
        }
        violacoes = verificar_violacao_portoes(rede_valida)
        self.assertEqual(len(violacoes), 0, f"Rede válida gerou violações espúrias: {violacoes}")

        # Cenário 2: Violação do Portão 1 (1.3.13 sem 1.3.11)
        violacoes_p1 = verificar_violacao_portoes({"1.3.13": ["1.3.0"]})
        self.assertEqual(len(violacoes_p1), 1)
        self.assertEqual(violacoes_p1[0]["portao"], PORTAO_1_FUNDACAO["id"])

        # Cenário 3: Violação do Portão 2 (3.1.7 sem 1.4.12)
        violacoes_p2 = verificar_violacao_portoes({"3.1.7": ["2.1.1"]})
        self.assertEqual(len(violacoes_p2), 1)
        self.assertEqual(violacoes_p2[0]["portao"], PORTAO_2_ESTRUTURA["id"])

        # Cenário 4: Violação do Portão 3 (2.1.2 sem 3.2.7)
        violacoes_p3 = verificar_violacao_portoes({"2.1.2": ["2.1.1"]})
        self.assertEqual(len(violacoes_p3), 1)
        self.assertEqual(violacoes_p3[0]["portao"], PORTAO_3_HIDRAULICA["id"])

        # Cenário 5: Violação do Portão 4 (3.1.9 sem 2.1.8)
        violacoes_p4 = verificar_violacao_portoes({"3.1.9": ["3.1.8"]})
        self.assertEqual(len(violacoes_p4), 1)
        self.assertEqual(violacoes_p4[0]["portao"], PORTAO_4_ACABAMENTO["id"])


if __name__ == "__main__":
    unittest.main()
