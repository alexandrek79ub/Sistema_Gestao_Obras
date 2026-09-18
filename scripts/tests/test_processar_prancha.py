import unittest

from processar_prancha import validar_e_calcular


def documento_base():
    return {
        "schema_version": 1,
        "disciplina": "FUNDACOES",
        "fonte": {
            "arquivo": "F-01.pdf",
            "revisao": "A",
            "pagina": 1,
        },
        "medicoes": [
            {
                "elemento": "S01",
                "tipo_elemento": "SAPATA",
                "regra_id": "FUN.SAPATA.CONCRETO.V1",
                "inputs": {
                    "largura_m": 1.5,
                    "comprimento_m": 1.8,
                    "altura_m": 0.5,
                    "quantidade": 4,
                },
                "evidencias": {
                    "largura_m": {"raw_text": "1,50", "region": "DETALHE S01"},
                    "comprimento_m": {"raw_text": "1,80", "region": "DETALHE S01"},
                    "altura_m": {"raw_text": "0,50", "region": "CORTE S01"},
                    "quantidade": {"raw_text": "4x S01", "region": "PLANTA"},
                },
            }
        ],
    }


class ProcessarPranchaTest(unittest.TestCase):
    def test_calculo_e_expressao_sao_produzidos_pelo_python(self):
        itens = validar_e_calcular(documento_base())
        self.assertEqual(len(itens), 1)
        self.assertEqual(itens[0]["rule_id"], "FUN.SAPATA.CONCRETO.V1")
        self.assertAlmostEqual(itens[0]["quantidade_liquida"], 5.4)
        self.assertEqual(itens[0]["expressao_matematica"], "1.5 * 1.8 * 0.5 * 4.0")

    def test_rejeita_quantidade_calculada_enviada_pela_llm(self):
        doc = documento_base()
        doc["medicoes"][0]["quantidade_liquida"] = 999
        with self.assertRaisesRegex(ValueError, "campos calculados/proibidos"):
            validar_e_calcular(doc)

    def test_rejeita_expressao_enviada_pela_llm(self):
        doc = documento_base()
        doc["medicoes"][0]["expressao_matematica"] = "1.5 * 1.8 * 0.5"
        with self.assertRaisesRegex(ValueError, "campos calculados/proibidos"):
            validar_e_calcular(doc)

    def test_rejeita_input_sem_evidencia(self):
        doc = documento_base()
        del doc["medicoes"][0]["evidencias"]["altura_m"]
        with self.assertRaisesRegex(ValueError, "evidência ausente"):
            validar_e_calcular(doc)

    def test_rejeita_regra_desconhecida(self):
        doc = documento_base()
        doc["medicoes"][0]["regra_id"] = "FUN.INVENTADA.V1"
        with self.assertRaisesRegex(ValueError, "regra_id desconhecida"):
            validar_e_calcular(doc)

    def test_rejeita_zero_ou_valor_negativo(self):
        doc = documento_base()
        doc["medicoes"][0]["inputs"]["altura_m"] = 0
        with self.assertRaisesRegex(ValueError, "maior que zero"):
            validar_e_calcular(doc)

    def test_quantidade_default_um_nao_exige_evidencia(self):
        doc = documento_base()
        del doc["medicoes"][0]["inputs"]["quantidade"]
        del doc["medicoes"][0]["evidencias"]["quantidade"]
        item = validar_e_calcular(doc)[0]
        self.assertAlmostEqual(item["quantidade_liquida"], 1.35)


    def test_baldrame_exige_comprimento_liquido(self):
        doc = documento_base()
        med = doc["medicoes"][0]
        med["elemento"] = "VB01"
        med["tipo_elemento"] = "BALDRAME"
        med["regra_id"] = "FUN.BALDRAME.CONCRETO.V1"
        med["inputs"] = {
            "largura_m": 0.20,
            "altura_m": 0.40,
            "comprimento_liquido_m": 3.80,
        }
        med["evidencias"] = {
            "largura_m": {"raw_text": "20", "region": "DET. VB01"},
            "altura_m": {"raw_text": "40", "region": "DET. VB01"},
            "comprimento_liquido_m": {
                "raw_text": "3,80 face a face",
                "region": "PLANTA DE LOCACAO",
            },
        }
        item = validar_e_calcular(doc)[0]
        self.assertAlmostEqual(item["quantidade_liquida"], 0.304)



if __name__ == "__main__":
    unittest.main()
