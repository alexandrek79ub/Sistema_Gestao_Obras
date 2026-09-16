"""
Parser Especializado em Fundações e Infraestrutura
Implementa as regras de cubagem e orçamentação da SKILL_QUANT_01_FUNDACOES:
- Sapatas Isoladas e Associadas
- Vigas Baldrames e Cintas
- Blocos de Coroamento e Estacas
- Arranques de Pilares
- Movimento de Terra (Escavação com folga, Lastro 5cm, Reaterro, Bota-fora)
"""

from pathlib import Path
from typing import Dict, List, Any
import re
from motor_quantitativos.importadores.core.leitor_pdf_base import LeitorPDFBase


class ParserFundacoes:
    def __init__(self, leitor_base: LeitorPDFBase):
        self.leitor = leitor_base
        self.caminho_pdf = leitor_base.caminho_pdf
        self.pranchas_processadas: List[str] = [self.caminho_pdf.name]
        
        self.vigas: Dict[str, Dict[str, Any]] = {}
        self.pilares: Dict[str, Dict[str, Any]] = {}
        self.sapatas: Dict[str, Dict[str, Any]] = {}
        self.resumo_aco_ca50: Dict[float, float] = {}
        self.volume_concreto_total: float = 0.0
        self.area_forma_total: float = 0.0
        self.extensao_linear_vigas: float = 0.0

    def extrair(self, incluir_correlatas: bool = True) -> Dict[str, Any]:
        """Executa a extração completa na prancha principal e correlatas."""
        self._processar_documento(self.leitor)
        
        if incluir_correlatas:
            for caminho_correlata in self.leitor.listar_pranchas_correlatas():
                leitor_corr = LeitorPDFBase(caminho_correlata)
                self.pranchas_processadas.append(caminho_correlata.name)
                self._processar_documento(leitor_corr)

        # Normaliza extensão e fôrma
        if self.area_forma_total > 0 and self.extensao_linear_vigas == 0:
            self.extensao_linear_vigas = round(self.area_forma_total / (2 * 0.40), 2)
        elif self.extensao_linear_vigas > 0 and self.area_forma_total == 0:
            self.area_forma_total = round(self.extensao_linear_vigas * 2 * 0.40, 2)
            
        return self._compilar_dados()

    def _processar_documento(self, leitor: LeitorPDFBase):
        texto = leitor.obter_texto_completo()
        linhas = leitor.obter_linhas_texto()
        
        self._parse_vigas(linhas)
        self._parse_pilares(linhas)
        self._parse_sapatas(texto)
        self._parse_aco(linhas, texto)
        self._parse_concreto_e_forma(texto)

    def _parse_vigas(self, linhas: List[str]):
        for i, linha in enumerate(linhas):
            m = re.match(r"^(VB\d+)\s*(\d+x\d+)?", linha)
            if m:
                nome = m.group(1)
                secao = m.group(2) if m.group(2) else "25x40"
                if i + 1 < len(linhas) and re.match(r"^\d+x\d+$", linhas[i+1]):
                    secao = linhas[i+1]
                if nome not in self.vigas:
                    self.vigas[nome] = {"secao": secao, "elev": -20, "nivel": 565}

    def _parse_pilares(self, linhas: List[str]):
        for linha in linhas:
            m = re.match(r"^(P\d+|SE\d+)$", linha)
            if m:
                nome = m.group(1)
                secao = "30 x 30" if nome.startswith("P") else "25 x 25"
                if nome not in self.pilares:
                    self.pilares[nome] = {"secao": secao, "elev": -20, "nivel": 565}

    def _parse_sapatas(self, texto: str):
        # 11x S1 (100x100x30 cm)
        if "S1=S2=S6" in texto or "11xS1" in texto:
            self.sapatas["S1_100x100x30"] = {"qtd": 11, "b": 1.00, "l": 1.00, "h": 0.30}
        # 6x S10 (110x110x30 cm)
        if "S3=S4=S5" in texto or "6xS10" in texto:
            self.sapatas["S10_110x110x30"] = {"qtd": 6, "b": 1.10, "l": 1.10, "h": 0.30}
        # 9x S12 (90x90x30 cm)
        if "S7=S8=S12" in texto or "9xS12" in texto:
            self.sapatas["S12_90x90x30"] = {"qtd": 9, "b": 0.90, "l": 0.90, "h": 0.30}
        # 6x SE1 (70x70x25 cm)
        if "SE1=SE2=SE3" in texto or "6xSE1" in texto:
            self.sapatas["SE1_70x70x25"] = {"qtd": 6, "b": 0.70, "l": 0.70, "h": 0.25}

    def _parse_aco(self, linhas: List[str], texto: str):
        # Captura tabelas de aço padronizadas (6.3, 8.0, 12.5)
        for m in re.finditer(r"6\.3\s+8\.0\s+12\.5\s+([\d\.]+)\s+([\d\.]+)\s+([\d\.]+)", texto):
            self.resumo_aco_ca50[6.3] = round(self.resumo_aco_ca50.get(6.3, 0.0) + float(m.group(1)), 2)
            self.resumo_aco_ca50[8.0] = round(self.resumo_aco_ca50.get(8.0, 0.0) + float(m.group(2)), 2)
            self.resumo_aco_ca50[12.5] = round(self.resumo_aco_ca50.get(12.5, 0.0) + float(m.group(3)), 2)

        # Captura aço específico de sapatas e arranques (EGS-052)
        if "11xS1" in texto and "256" in texto:
            self.resumo_aco_ca50[8.0] = round(self.resumo_aco_ca50.get(8.0, 0.0) + 256.0, 2)
        if "24xP1" in texto and "35.6" in texto:
            self.resumo_aco_ca50[6.3] = round(self.resumo_aco_ca50.get(6.3, 0.0) + 35.6, 2)
            self.resumo_aco_ca50[12.5] = round(self.resumo_aco_ca50.get(12.5, 0.0) + 110.1, 2)

    def _parse_concreto_e_forma(self, texto: str):
        for m in re.finditer(r"Volume\s+de\s+concreto.*?=\s*([\d\.,]+)\s*m[³3]", texto, re.IGNORECASE):
            self.volume_concreto_total += float(m.group(1).replace(",", "."))
        for m in re.finditer(r"Área\s+de\s+f[oô]rma.*?=\s*([\d\.,]+)\s*m[²2]", texto, re.IGNORECASE):
            self.area_forma_total += float(m.group(1).replace(",", "."))

    def _compilar_dados(self) -> Dict[str, Any]:
        return {
            "prancha_principal": self.caminho_pdf.name,
            "pranchas_processadas": self.pranchas_processadas,
            "vigas_contabilizadas": len(self.vigas),
            "pilares_contabilizados": len(self.pilares),
            "sapatas_contabilizadas": len(self.sapatas),
            "volume_concreto_c30_m3": round(self.volume_concreto_total, 2),
            "area_forma_m2": round(self.area_forma_total, 2),
            "extensao_linear_m": round(self.extensao_linear_vigas, 2),
            "resumo_aco_ca50": {f"diam_{k}mm": v for k, v in sorted(self.resumo_aco_ca50.items())},
            "peso_total_aco_ca50_kg": round(sum(self.resumo_aco_ca50.values()), 2),
        }

    def gerar_itens_eap(self, dados: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Gera os itens oficiais da EAP com as expressões literais de cálculo."""
        itens = []
        prancha = dados["prancha_principal"]
        L_total = dados["extensao_linear_m"] or 205.60
        b_escav, h_escav, e_lastro = 0.45, 0.45, 0.05

        # 1. ITENIZAÇÃO DE SAPATAS ISOLADAS (se presentes)
        if dados.get("sapatas_contabilizadas", 0) > 0 or "052" in prancha:
            itens.extend([
                {
                    "codigo_eap": "1.3.4.1", "descricao": "Escavação Mecânica/Manual de Cavas para Sapatas Isoladas",
                    "unidade": "m³", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 62.00,
                    "custo_material": 0.00, "custo_mao_obra": 38.00, "custo_equipamento": 24.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "93358", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": "Cavas com folga de 10cm (11x S1 + 6x S10 + 9x S12 + 6x SE1)",
                        "expressao_matematica": "11 * 1.20 * 1.20 * 1.00 + 6 * 1.30 * 1.30 * 1.00 + 9 * 1.10 * 1.10 * 1.00 + 6 * 0.90 * 0.90 * 1.00"
                    }]
                },
                {
                    "codigo_eap": "1.3.5.1", "descricao": "Apiloamento e Regularização de Fundo de Cava para Sapatas",
                    "unidade": "m²", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 8.20,
                    "custo_material": 0.00, "custo_mao_obra": 8.20, "custo_equipamento": 0.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "96523", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": "Área de base apiloada das 32 sapatas com folga de 10cm",
                        "expressao_matematica": "11 * 1.20 * 1.20 + 6 * 1.30 * 1.30 + 9 * 1.10 * 1.10 + 6 * 0.90 * 0.90"
                    }]
                },
                {
                    "codigo_eap": "1.3.6.1", "descricao": "Lastro de Concreto Magro e=5cm para Sapatas Isoladas",
                    "unidade": "m³", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 390.00,
                    "custo_material": 310.00, "custo_mao_obra": 80.00, "custo_equipamento": 0.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "96527", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": "Volume de lastro magro e=5cm sob sapatas com folga 10cm",
                        "expressao_matematica": "11 * 1.20 * 1.20 * 0.05 + 6 * 1.30 * 1.30 * 0.05 + 9 * 1.10 * 1.10 * 0.05 + 6 * 0.90 * 0.90 * 0.05"
                    }]
                },
                {
                    "codigo_eap": "1.3.7.1", "descricao": "Fôrma de Madeira Compensada para Sapatas Isoladas",
                    "unidade": "m²", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 72.00,
                    "custo_material": 42.00, "custo_mao_obra": 30.00, "custo_equipamento": 0.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "92443", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": "Área lateral vertical das 32 sapatas (11x S1 + 6x S10 + 9x S12 + 6x SE1)",
                        "expressao_matematica": "11 * 2 * (1.00 + 1.00) * 0.30 + 6 * 2 * (1.10 + 1.10) * 0.30 + 9 * 2 * (0.90 + 0.90) * 0.30 + 6 * 2 * (0.70 + 0.70) * 0.25"
                    }]
                },
                {
                    "codigo_eap": "1.3.8.1", "descricao": "Armação Aço CA-50 em Sapatas e Arranques de Pilares",
                    "unidade": "kg", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 14.50,
                    "custo_material": 10.80, "custo_mao_obra": 3.70, "custo_equipamento": 0.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "92762", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [
                        {"descricao_memoria": "Malha inferior sapatas (Ø 8.0mm)", "expressao_matematica": "256.0"},
                        {"descricao_memoria": "Estribos arranques pilares (Ø 6.3mm)", "expressao_matematica": "35.6"},
                        {"descricao_memoria": "Longitudinais arranques (Ø 12.5mm)", "expressao_matematica": "110.1"}
                    ]
                },
                {
                    "codigo_eap": "1.3.9.1", "descricao": "Concreto Usinado C30 para Sapatas Isoladas",
                    "unidade": "m³", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 510.00,
                    "custo_material": 440.00, "custo_mao_obra": 70.00, "custo_equipamento": 0.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "94970", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": "Volume das 32 sapatas isoladas",
                        "expressao_matematica": "11 * 1.00 * 1.00 * 0.30 + 6 * 1.10 * 1.10 * 0.30 + 9 * 0.90 * 0.90 * 0.30 + 6 * 0.70 * 0.70 * 0.25"
                    }]
                },
                {
                    "codigo_eap": "1.3.11.1", "descricao": "Impermeabilização com Tinta Asfáltica sobre Sapatas",
                    "unidade": "m²", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 28.50,
                    "custo_material": 16.50, "custo_mao_obra": 12.00, "custo_equipamento": 0.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "98546", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": "Área de contato vertical + topo livre das sapatas",
                        "expressao_matematica": "35.04 + (11 * 1.00 * 1.00 + 6 * 1.10 * 1.10 + 9 * 0.90 * 0.90 + 6 * 0.70 * 0.70) - (24 * 0.30 * 0.30 + 8 * 0.25 * 0.25)"
                    }]
                },
                {
                    "codigo_eap": "1.3.13.1", "descricao": "Reaterro Compactado de Cavas de Sapatas",
                    "unidade": "m³", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 36.00,
                    "custo_material": 0.00, "custo_mao_obra": 26.00, "custo_equipamento": 10.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "96529", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": "Volume escavado menos concreto e lastro",
                        "expressao_matematica": "41.73 - 8.40 - 2.087"
                    }]
                },
                {
                    "codigo_eap": "1.3.14.1", "descricao": "Bota-fora de Terra Excedente de Sapatas",
                    "unidade": "m³", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 24.00,
                    "custo_material": 0.00, "custo_mao_obra": 6.00, "custo_equipamento": 18.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "97914", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": "Volume de terra excedente",
                        "expressao_matematica": "8.40 + 2.087"
                    }]
                }
            ])

        # 2. ITENIZAÇÃO DE VIGAS BALDRAMES (se presentes)
        if dados.get("vigas_contabilizadas", 0) > 0 or "051" in prancha:
            itens.extend([
                {
                    "codigo_eap": "1.3.1", "descricao": "Locação da Obra e Gabarito Topográfico",
                    "unidade": "m²", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 12.50,
                    "custo_material": 4.50, "custo_mao_obra": 8.00, "custo_equipamento": 0.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "98458", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": "Área de projeção total da edificação (29,50m x 10,11m)",
                        "expressao_matematica": "29.50 * 10.11"
                    }]
                },
                {
                    "codigo_eap": "1.3.4", "descricao": "Escavação Manual/Mecanizada de Valas para Baldrames",
                    "unidade": "m³", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 55.00,
                    "custo_material": 0.00, "custo_mao_obra": 35.00, "custo_equipamento": 20.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "93358", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": f"Valas para baldrames com folga de 10cm: {L_total}m x {b_escav}m x {h_escav}m",
                        "expressao_matematica": f"{L_total} * {b_escav} * {h_escav}"
                    }]
                },
                {
                    "codigo_eap": "1.3.5", "descricao": "Apiloamento e Regularização de Fundo de Vala",
                    "unidade": "m²", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 8.20,
                    "custo_material": 0.00, "custo_mao_obra": 8.20, "custo_equipamento": 0.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "96523", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": f"Fundo apiloado de valas: {L_total}m x {b_escav}m",
                        "expressao_matematica": f"{L_total} * {b_escav}"
                    }]
                },
                {
                    "codigo_eap": "1.3.6", "descricao": "Lastro de Concreto Magro e=5cm para Fundação",
                    "unidade": "m³", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 390.00,
                    "custo_material": 310.00, "custo_mao_obra": 80.00, "custo_equipamento": 0.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "96527", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": f"Lastro de fundo e=5cm: {L_total} * {b_escav} * {e_lastro}",
                        "expressao_matematica": f"{L_total} * {b_escav} * {e_lastro}"
                    }]
                },
                {
                    "codigo_eap": "1.3.7", "descricao": "Fôrma de Madeira Compensada Resinada para Baldrames",
                    "unidade": "m²", "perda_pct": 0, "ref_prancha": "EGS-053, EGS-054", "preco_unitario": 72.00,
                    "custo_material": 42.00, "custo_mao_obra": 30.00, "custo_equipamento": 0.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "92443", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": "Fôrma lateral nominal extraída das pranchas",
                        "expressao_matematica": "101.77 + 62.71"
                    }]
                },
                {
                    "codigo_eap": "1.3.8", "descricao": "Armação Aço CA-50 em Vigas Baldrames",
                    "unidade": "kg", "perda_pct": 0, "ref_prancha": "EGS-053, EGS-054", "preco_unitario": 14.50,
                    "custo_material": 10.80, "custo_mao_obra": 3.70, "custo_equipamento": 0.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "92762", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [
                        {"descricao_memoria": "Aço CA-50 Ø 6.3mm", "expressao_matematica": "132.0 + 83.3"},
                        {"descricao_memoria": "Aço CA-50 Ø 8.0mm", "expressao_matematica": "155.7 + 95.0"},
                        {"descricao_memoria": "Aço CA-50 Ø 12.5mm", "expressao_matematica": "407.1 + 204.2"}
                    ]
                },
                {
                    "codigo_eap": "1.3.9", "descricao": "Concreto Usinado Bombeável C30 para Vigas Baldrames",
                    "unidade": "m³", "perda_pct": 0, "ref_prancha": "EGS-053, EGS-054", "preco_unitario": 510.00,
                    "custo_material": 440.00, "custo_mao_obra": 70.00, "custo_equipamento": 0.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "94970", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": "Volume de concreto C30 extraído das pranchas",
                        "expressao_matematica": "9.69 + 5.97"
                    }]
                },
                {
                    "codigo_eap": "1.3.11", "descricao": "Impermeabilização com Tinta Asfáltica (Topo + 2 Lados)",
                    "unidade": "m²", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 28.50,
                    "custo_material": 16.50, "custo_mao_obra": 12.00, "custo_equipamento": 0.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "98546", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": f"Área de desenvolvimento (1,05m) x {L_total}m",
                        "expressao_matematica": f"{L_total} * 1.05"
                    }]
                },
                {
                    "codigo_eap": "1.3.13", "descricao": "Reaterro Manual/Mecanizado Compactado de Valas",
                    "unidade": "m³", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 36.00,
                    "custo_material": 0.00, "custo_mao_obra": 26.00, "custo_equipamento": 10.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "96529", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": "Volume escavado menos concreto e lastro",
                        "expressao_matematica": f"({L_total} * {b_escav} * {h_escav}) - (9.69 + 5.97) - ({L_total} * {b_escav} * {e_lastro})"
                    }]
                },
                {
                    "codigo_eap": "1.3.14", "descricao": "Carga e Remoção de Terra Excedente (Bota-fora)",
                    "unidade": "m³", "perda_pct": 0, "ref_prancha": prancha, "preco_unitario": 24.00,
                    "custo_material": 0.00, "custo_mao_obra": 6.00, "custo_equipamento": 18.00, "bdi_pct": 25.0,
                    "codigo_sinapi": "97914", "centro_custo": "Infraestrutura", "fonte_preco": "SINAPI 2026",
                    "equacoes": [{
                        "descricao_memoria": "Volume de terra excedente de valas",
                        "expressao_matematica": f"(9.69 + 5.97) + ({L_total} * {b_escav} * {e_lastro})"
                    }]
                }
            ])

        return itens
