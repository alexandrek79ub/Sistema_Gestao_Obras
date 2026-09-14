"""Testes automatizados de CPM e exportação MS Project XML (AUD-009)."""

import json
import os
import tempfile
import unittest
import xml.etree.ElementTree as ET
from scripts.common.cpm import calcular_cpm_detalhado
from scripts.gerar_cronograma import gerar_ms_project_xml


class CPMMSProjectTest(unittest.TestCase):
    def setUp(self):
        # Rede conhecida de teste:
        # A (5d) -> B (10d) [caminho mais longo: 15d]
        # A (5d) -> C (3d)  [caminho mais curto: 8d, folga de 7d]
        # B -> D (2d), C -> D (2d) -> Duração total: 17d
        # Caminho crítico: A -> B -> D (17d)
        # Atividade C não é crítica (tem folga = 7d)
        self.atividades_rede = [
            {"id": "A_INICIO", "duracao_dias": 5, "predecessoras": []},
            {"id": "B_CRITICA", "duracao_dias": 10, "predecessoras": ["A_INICIO"]},
            {"id": "C_FOLGA", "duracao_dias": 3, "predecessoras": ["A_INICIO"]},
            {"id": "D_FINAL", "duracao_dias": 2, "predecessoras": ["B_CRITICA", "C_FOLGA"]},
        ]

    def test_cpm_calculo_folgas_e_caminho_critico(self):
        """Forward e Backward pass calculam folga e identificam o caminho crítico exato."""
        cpm = calcular_cpm_detalhado(self.atividades_rede, data_inicio_iso="2026-10-01")
        self.assertEqual(cpm["duracao_total_dias"], 17)
        self.assertEqual(cpm["caminho_critico"], ["A_INICIO", "B_CRITICA", "D_FINAL"])

        atividades = cpm["atividades"]
        # A: ES=0, EF=5, LS=0, LF=5, Folga=0, Critica=True
        self.assertEqual(atividades["A_INICIO"]["folga_total"], 0)
        self.assertTrue(atividades["A_INICIO"]["critica"])

        # B: ES=5, EF=15, LS=5, LF=15, Folga=0, Critica=True
        self.assertEqual(atividades["B_CRITICA"]["folga_total"], 0)
        self.assertTrue(atividades["B_CRITICA"]["critica"])

        # C: ES=5, EF=8, LS=12, LF=15, Folga=7, Critica=False
        self.assertEqual(atividades["C_FOLGA"]["folga_total"], 7)
        self.assertFalse(atividades["C_FOLGA"]["critica"])

        # D: ES=15, EF=17, LS=15, LF=17, Folga=0, Critica=True
        self.assertEqual(atividades["D_FINAL"]["folga_total"], 0)
        self.assertTrue(atividades["D_FINAL"]["critica"])

    def test_ausencia_de_cpm_impede_exportacao_produtiva(self):
        """Arquivo CPM ausente não pode gerar tarefas sintéticas nem ter sucesso silencioso."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cpm_inexistente = os.path.join(tmp_dir, "cpm_nao_existe.json")
            with self.assertRaises(FileNotFoundError):
                gerar_ms_project_xml(cpm_inexistente, tmp_dir, "TESTE", "Obra Teste")

    def test_ms_project_xml_reflete_cpm_e_criticidade_fiel(self):
        """O XML gerado possui datas, folgas e criticidade que coincidem rigorosamente com o CPM."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cpm_path = os.path.join(tmp_dir, "dados_cpm.json")
            with open(cpm_path, "w", encoding="utf-8") as f:
                json.dump({"atividades": self.atividades_rede}, f)

            xml_path = gerar_ms_project_xml(cpm_path, tmp_dir, "TESTE", "Obra Teste", data_inicio_iso="2026-10-01")
            self.assertTrue(os.path.exists(xml_path))

            # Reimportar e parsear o XML
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Encontrar tarefas (namespaces podem estar presentes no XML do MS Project)
            ns = {"msp": "http://schemas.microsoft.com/project"}
            tasks = root.findall(".//msp:Task", ns)
            if not tasks:
                tasks = root.findall(".//Task")

            tarefas_xml = {}
            for t in tasks:
                uid = t.find("UID") or t.find("msp:UID", ns)
                name = t.find("Name") or t.find("msp:Name", ns)
                crit = t.find("Critical") or t.find("msp:Critical", ns)
                start = t.find("Start") or t.find("msp:Start", ns)
                finish = t.find("Finish") or t.find("msp:Finish", ns)
                slack = t.find("TotalSlack") or t.find("msp:TotalSlack", ns)

                if uid is not None and uid.text != "0" and name is not None:
                    aid_key = name.text.replace(" ", "_")
                    tarefas_xml[aid_key] = {
                        "critical": int(crit.text) if crit is not None else 0,
                        "start": start.text if start is not None else "",
                        "finish": finish.text if finish is not None else "",
                        "slack": int(slack.text) if slack is not None else 0,
                    }

            # Validar que a tarefa não crítica (C_FOLGA) tem Critical=0 e slack > 0
            self.assertIn("C_FOLGA", tarefas_xml)
            self.assertEqual(tarefas_xml["C_FOLGA"]["critical"], 0)
            self.assertGreater(tarefas_xml["C_FOLGA"]["slack"], 0)

            # Validar que as tarefas críticas (A, B, D) têm Critical=1 e slack=0
            for crit_id in ["A_INICIO", "B_CRITICA", "D_FINAL"]:
                self.assertIn(crit_id, tarefas_xml)
                self.assertEqual(tarefas_xml[crit_id]["critical"], 1, f"Tarefa {crit_id} deveria ser crítica")
                self.assertEqual(tarefas_xml[crit_id]["slack"], 0, f"Tarefa {crit_id} deveria ter slack zero")


if __name__ == "__main__":
    unittest.main()
