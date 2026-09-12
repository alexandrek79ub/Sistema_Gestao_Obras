# -*- coding: utf-8 -*-
"""
Script: gerar_programacao_curto_prazo_takt.py
Motor Universal de Programação de Curto Prazo (Weekly Work Plan - WWP)
estruturada rigorosamente como uma ESTEIRA DE PRODUÇÃO LEAN (Takt Planning),
harmonizada integralmente com o Caminho Crítico (dados_cpm.json)
e a Linha de Balanço Canônica de 15 Vagões.

Uso:
    python scripts/gerar_programacao_curto_prazo_takt.py --obra OBRA_TMULT
    python scripts/gerar_programacao_curto_prazo_takt.py --obra RESIDENCIAL_ALPHA
"""

import os
import sys
import csv
import json
import argparse


MAPA_LOTE_CPM_ATIVIDADES = {
    "LOTE-001": ("A01_MOB_CANTEIRO", 1.0, 10),
    "LOTE-002": ("A02_ESCAV_INFRA", 2/6, 2),
    "LOTE-003": ("A03_SAPATAS_CONC", 2/7, 2),
    "LOTE-004": ("A02_ESCAV_INFRA", 2/6, 2),
    "LOTE-005": ("A03_SAPATAS_CONC", 2/7, 2),
    "LOTE-006": ("A02_ESCAV_INFRA", 2/6, 2),
    "LOTE-007": ("A03_SAPATAS_CONC", 3/7, 3),
    "LOTE-008": ("A04_BALDRAMES_CONC", 4/7, 4),
    "LOTE-009": ("A04_BALDRAMES_CONC", 3/7, 3),
    "LOTE-010": ("A05_IMPERM_BALDRAME", 1.0, 4),
    "LOTE-011": ("A06_REATERRO_INFRA", 1.0, 3),
    "LOTE-012": ("A07_PILARES_SUPRA", 3/9, 3),
    "LOTE-013": ("A07_PILARES_SUPRA", 3/9, 3),
    "LOTE-014": ("A07_PILARES_SUPRA", 3/9, 3),
    "LOTE-015": ("A08_VIGAS_LAJE_FORMA", 1.0, 5),
    "LOTE-016": ("A09_CONCRET_LAJE_H12", 1.0, 16),
    "LOTE-017": ("A12_ALVENARIA_VEDACAO", 7/20, 7),
    "LOTE-018": ("A12_ALVENARIA_VEDACAO", 7/20, 7),
    "LOTE-019": ("A12_ALVENARIA_VEDACAO", 6/20, 6),
    "LOTE-020": ("A11_ESTRUT_TERCAS_COB", 1.0, 10),
    "LOTE-021": ("A13_TELHAS_SANDWICH_PLAT", 1.0, 10),
    "LOTE-022": ("A14_ELET_EMBUTIDA", 1.0, 10),
    "LOTE-023": ("A16_TESTE_HIDROSTATICO_72H", 1.0, 3),
    "LOTE-024": ("A17_EMBOCO_REBOCO", 2/14, 2),
    "LOTE-025": ("A17_EMBOCO_REBOCO", 6/14, 6),
    "LOTE-026": ("A17_EMBOCO_REBOCO", 6/14, 6),
    "LOTE-027": ("A18_IMPERM_WCS", 1.0, 3),
    "LOTE-028": ("A19_CONTRAPISO", 1.0, 6),
    "LOTE-029": ("A22_PISO_PORCELANATO", 5/14, 5),
    "LOTE-030": ("A22_PISO_PORCELANATO", 5/14, 5),
    "LOTE-031": ("A22_PISO_PORCELANATO", 4/14, 4),
    "LOTE-032": ("A24_RODAPES_ACAB", 1.0, 4),
    "LOTE-033": ("A21_ESQUADRIAS_FIX", 4/8, 4),
    "LOTE-034": ("A21_ESQUADRIAS_FIX", 4/8, 4),
    "LOTE-035": ("A20_INFRA_DUTOS_HVAC", 7/10, 7),
    "LOTE-036": ("A20_INFRA_DUTOS_HVAC", 3/10, 3),
    "LOTE-037": ("A23_FIACAO_TELECOM", 6/10, 6),
    "LOTE-038": ("A23_FIACAO_TELECOM", 4/10, 4),
    "LOTE-039": ("A25_PINTURA_1A_DEMAO", 3/5, 3),
    "LOTE-040": ("A25_PINTURA_1A_DEMAO", 2/5, 2),
    "LOTE-041": ("A27_LOUCAS_METAIS", 1.0, 6),
    "LOTE-042": ("A28_LUMINARIAS_ESPELHOS", 1.0, 5),
    "LOTE-043": ("A29_PINTURA_FINAL", 1.0, 7),
    "LOTE-044": ("A26_APARELHOS_HVAC", 1.0, 6),
    "LOTE-045": ("A30_COMISSIONAMENTO", 2/6, 2),
    "LOTE-046": ("A31_LIMPEZA_ENTREGA", 2/6, 2),
    "LOTE-047": ("A30_COMISSIONAMENTO", 2/6, 2),
    "LOTE-048": ("A30_COMISSIONAMENTO", 1/6, 1),
    "LOTE-049": ("A30_COMISSIONAMENTO", 1/6, 1),
    "LOTE-050": ("A31_LIMPEZA_ENTREGA", 1/6, 1),
    "LOTE-051": ("A31_LIMPEZA_ENTREGA", 1/6, 1),
    "LOTE-052": ("A31_LIMPEZA_ENTREGA", 2/6, 2),
}

def derivar_duracoes_do_cpm(cpm_path):
    """Lê dados_cpm.json e deriva dinamicamente as durações de cada lote."""
    if not os.path.exists(cpm_path):
        print(f"[-] Aviso: {cpm_path} não encontrado. Mantendo durações canônicas.")
        return {}
    with open(cpm_path, "r", encoding="utf-8") as f:
        cpm_data = json.load(f)
    atividades = {a['id']: a['duracao_dias'] for a in cpm_data.get('atividades', [])}
    
    duracoes_derivadas = {}
    for cod_lote, (aid, frac, fallback_dur) in MAPA_LOTE_CPM_ATIVIDADES.items():
        if aid in atividades:
            if cod_lote == "LOTE-016":
                a09_dur = atividades.get("A09_CONCRET_LAJE_H12", 1)
                a10_dur = atividades.get("A10_CURA_DESFORMA", 12)
                duracoes_derivadas[cod_lote] = a09_dur + a10_dur + 3
            elif frac == 1.0:
                duracoes_derivadas[cod_lote] = atividades[aid]
            else:
                dur_calc = int(round(atividades[aid] * frac))
                duracoes_derivadas[cod_lote] = dur_calc if dur_calc > 0 else fallback_dur
        else:
            duracoes_derivadas[cod_lote] = fallback_dur
    return duracoes_derivadas

def obter_lotes_padrao(nome_obra):
    """Retorna os lotes de produção calculados em ritmo de esteira Takt (52 lotes / 26 semanas / 15 vagões)."""
    lotes = [
        {
            "COD_LOTE": "LOTE-001",
            "SEMANA": "Semana 01",
            "DIAS_SEMANA": "Dias 01 a 03 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 1 (Zona 1 - Geral)",
            "VAGAO_ESTEIRA": "Vagão 01: Topografia & Canteiro",
            "SERVICO_LOTE": "Mobilização de Canteiro NR-18 e Locação Gabarito Geral",
            "META_FISICA": "100% canteiro montado + 368 m² gabarito tábua corrida",
            "DURACAO_DIAS": "10",
            "EQUIPE_PREVISTA": "1 Topógrafo + 2 Ajudantes + 4 Serventes",
            "HEADCOUNT_PREVISTO": "7",
            "EQUIPAMENTOS_PREVISTOS": "LOC-02 Caminhão Munck + Estação Total",
            "MATERIAIS_UCC": "Containers NR-18, pontaletes e tábuas 30cm",
            "RUP_META_HH_UNID": "0,38 HH/m²",
            "STATUS_EXECUCAO": "CONCLUIDO",
            "RDO_VINCULADO": "RDO-001"
        },
        {
            "COD_LOTE": "LOTE-002",
            "SEMANA": "Semana 01",
            "DIAS_SEMANA": "Dias 04 a 06 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 1 (Zona 1 - S1 a S12)",
            "VAGAO_ESTEIRA": "Vagão 02: Fundações Sapatas",
            "SERVICO_LOTE": "Escavação Mecanizada e Lastro S1 a S12 + Corte e Dobra de Armaduras na Bancada",
            "META_FISICA": "12 cavas de sapatas (19,2 m³ escav. + 1,14 m³ lastro) + 96 kg aço CA-50 cortado e dobrado na central",
            "DURACAO_DIAS": "2",
            "EQUIPE_PREVISTA": "1 Operador + 2 Armadores (Central de Aço) + 4 Serventes",
            "HEADCOUNT_PREVISTO": "7",
            "EQUIPAMENTOS_PREVISTOS": "LOC-01 Mini Retroescavadeira + LOC-05 Gerador + Dobradeira elétrica",
            "MATERIAIS_UCC": "Piquetes de locação + Concreto magro fck 15 MPa + Aço CA-50 Ø8mm (96 kg)",
            "RUP_META_HH_UNID": "0,95 HH/m³",
            "STATUS_EXECUCAO": "CONCLUIDO",
            "RDO_VINCULADO": "RDO-002"
        },
        {
            "COD_LOTE": "LOTE-003",
            "SEMANA": "Semana 02",
            "DIAS_SEMANA": "Dias 07 a 09 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 1 (Zona 1 - S1 a S12)",
            "VAGAO_ESTEIRA": "Vagão 02: Fundações Sapatas",
            "SERVICO_LOTE": "Armação e Fôrmas das Sapatas S1 a S12 (Etapa 1)",
            "META_FISICA": "12 sapatas (96 kg aço CA-50 + 13,45 m² fôrmas compensado)",
            "DURACAO_DIAS": "2",
            "EQUIPE_PREVISTA": "2 Carpinteiros + 2 Armadores + 4 Serventes",
            "HEADCOUNT_PREVISTO": "8",
            "EQUIPAMENTOS_PREVISTOS": "LOC-05 Gerador + Dobradeira elétrica portátil",
            "MATERIAIS_UCC": "Aço CA-50 Ø8mm cortado e dobrado + Painéis fôrma 17mm",
            "RUP_META_HH_UNID": "1,10 HH/m³",
            "STATUS_EXECUCAO": "CONCLUIDO",
            "RDO_VINCULADO": "RDO-003"
        },
        {
            "COD_LOTE": "LOTE-004",
            "SEMANA": "Semana 02",
            "DIAS_SEMANA": "Dias 10 a 12 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 2 (Zona 2 - S13 a S24)",
            "VAGAO_ESTEIRA": "Vagão 02: Fundações Sapatas",
            "SERVICO_LOTE": "Escavação/Lastro S13 a S24 + Concretagem S1 a S12 + Corte e Dobra Bancada S13 a S24",
            "META_FISICA": "12 cavas (19,2 m³) + Concretagem S1-12 (3,21 m³) + 96 kg aço CA-50 cortado e dobrado na central",
            "DURACAO_DIAS": "2",
            "EQUIPE_PREVISTA": "1 Operador + 2 Armadores (Central de Aço) + 2 Pedreiros + 4 Serventes",
            "HEADCOUNT_PREVISTO": "9",
            "EQUIPAMENTOS_PREVISTOS": "LOC-01 Retroescavadeira + Vibrador mangote 45mm + Dobradeira elétrica",
            "MATERIAIS_UCC": "Concreto usinado fck 30 MPa (1 betoneira) + Lastro 15 MPa + Aço CA-50 Ø8mm",
            "RUP_META_HH_UNID": "0,85 HH/m³",
            "STATUS_EXECUCAO": "CONCLUIDO",
            "RDO_VINCULADO": "RDO-004"
        },
        {
            "COD_LOTE": "LOTE-005",
            "SEMANA": "Semana 03",
            "DIAS_SEMANA": "Dias 13 a 15 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 2 (Zona 2 - S13 a S24)",
            "VAGAO_ESTEIRA": "Vagão 02: Fundações Sapatas",
            "SERVICO_LOTE": "Armação e Fôrmas Sapatas S13 a S24 [Etapa 1 em Cura e Desforma]",
            "META_FISICA": "12 sapatas (96 kg aço CA-50 + 13,45 m² fôrmas) + Desforma S1-S12",
            "DURACAO_DIAS": "2",
            "EQUIPE_PREVISTA": "2 Carpinteiros + 2 Armadores + 4 Serventes",
            "HEADCOUNT_PREVISTO": "8",
            "EQUIPAMENTOS_PREVISTOS": "LOC-05 Gerador + Desmoldante ecológico",
            "MATERIAIS_UCC": "Aço CA-50 Ø8mm + Painéis de fôrma reaproveitados",
            "RUP_META_HH_UNID": "1,05 HH/m³",
            "STATUS_EXECUCAO": "CONCLUIDO",
            "RDO_VINCULADO": "RDO-005"
        },
        {
            "COD_LOTE": "LOTE-006",
            "SEMANA": "Semana 03",
            "DIAS_SEMANA": "Dias 16 a 18 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 3 (Zona 3 - S25 a S32)",
            "VAGAO_ESTEIRA": "Vagão 02: Fundações Sapatas",
            "SERVICO_LOTE": "Escavação S25 a S32 + Concretagem S13 a S24 + Corte e Dobra Bancada S25 a S32 e Baldrames",
            "META_FISICA": "8 cavas (12,8 m³ escavação) + 3,21 m³ concreto fck 30 MPa + 64 kg aço sapatas cortado",
            "DURACAO_DIAS": "2",
            "EQUIPE_PREVISTA": "1 Operador + 2 Armadores (Central de Aço) + 2 Pedreiros + 4 Serventes",
            "HEADCOUNT_PREVISTO": "9",
            "EQUIPAMENTOS_PREVISTOS": "LOC-01 Retroescavadeira + Vibrador 45mm + Dobradeira elétrica + Jericas",
            "MATERIAIS_UCC": "Concreto usinado fck 30 MPa + Lastro magro fck 15 MPa + Aço CA-50",
            "RUP_META_HH_UNID": "0,85 HH/m³",
            "STATUS_EXECUCAO": "CONCLUIDO",
            "RDO_VINCULADO": "RDO-006"
        },
        {
            "COD_LOTE": "LOTE-007",
            "SEMANA": "Semana 04",
            "DIAS_SEMANA": "Dias 19 a 21 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 3 (Zona 3 - S25 a S32)",
            "VAGAO_ESTEIRA": "Vagão 02: Fundações Sapatas",
            "SERVICO_LOTE": "Armação, Fôrmas e Concretagem Sapatas S25 a S32 (Etapa 3)",
            "META_FISICA": "8 sapatas finais (64 kg aço + 8,98 m² fôrmas + 2,13 m³ conc)",
            "DURACAO_DIAS": "3",
            "EQUIPE_PREVISTA": "2 Carpinteiros + 2 Armadores + 1 Pedreiro + 4 Serventes",
            "HEADCOUNT_PREVISTO": "9",
            "EQUIPAMENTOS_PREVISTOS": "LOC-05 Gerador + Vibrador 45mm",
            "MATERIAIS_UCC": "Aço CA-50 + Fôrmas 17mm + Concreto fck 30 (Total 32 sapatas)",
            "RUP_META_HH_UNID": "0,90 HH/m³",
            "STATUS_EXECUCAO": "CONCLUIDO",
            "RDO_VINCULADO": "RDO-007"
        },
        {
            "COD_LOTE": "LOTE-008",
            "SEMANA": "Semana 04",
            "DIAS_SEMANA": "Dias 22 a 24 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 1 (Zona 1 - Baldrames VB1 a VB6)",
            "VAGAO_ESTEIRA": "Vagão 03: Vigas Baldrames",
            "SERVICO_LOTE": "Montagem Fôrmas e Armação Baldrames VB1 a VB6 [Esteira Entra em Vigas]",
            "META_FISICA": "48 m vigas baldrames 25x40cm + 368 kg aço CA-50 cortado",
            "DURACAO_DIAS": "4",
            "EQUIPE_PREVISTA": "3 Carpinteiros + 2 Armadores + 4 Serventes",
            "HEADCOUNT_PREVISTO": "9",
            "EQUIPAMENTOS_PREVISTOS": "LOC-05 Gerador + Dobradeira elétrica + Espaçadores",
            "MATERIAIS_UCC": "Compensado resinado 17mm + Aço CA-50 Ø10/12.5mm",
            "RUP_META_HH_UNID": "1,20 HH/m³",
            "STATUS_EXECUCAO": "CONCLUIDO",
            "RDO_VINCULADO": "RDO-008"
        },
        {
            "COD_LOTE": "LOTE-009",
            "SEMANA": "Semana 05",
            "DIAS_SEMANA": "Dias 25 a 27 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 1 e 2 (Zona 1 e 2 - Baldrames)",
            "VAGAO_ESTEIRA": "Vagão 03: Vigas Baldrames",
            "SERVICO_LOTE": "Concretagem VB1 a VB6 (Etapa 1) + Fôrmas/Armação VB7 a VB12 (Etapa 2)",
            "META_FISICA": "4,8 m³ concreto VB1-6 + 46 m fôrmas/armação VB7-12 (350 kg aço)",
            "DURACAO_DIAS": "3",
            "EQUIPE_PREVISTA": "4 Carpinteiros + 3 Armadores + 2 Pedreiros + 5 Serventes",
            "HEADCOUNT_PREVISTO": "14",
            "EQUIPAMENTOS_PREVISTOS": "LOC-05 Gerador + Vibrador 45mm + Jericas",
            "MATERIAIS_UCC": "Concreto fck 30 MPa usinado + Compensado 17mm + Aço CA-50",
            "RUP_META_HH_UNID": "1,10 HH/m³",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-010",
            "SEMANA": "Semana 05",
            "DIAS_SEMANA": "Dias 28 a 30 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 2 e 3 (Zona 2 e 3 - Baldrames)",
            "VAGAO_ESTEIRA": "Vagão 03: Vigas Baldrames",
            "SERVICO_LOTE": "Concretagem VB7 a VB12 (Etapa 2) + Fôrmas/Armação VB13 a VB19 (Etapa 3)",
            "META_FISICA": "4,6 m³ concreto VB7-12 + 46 m fôrmas VB13-19 (359 kg aço)",
            "DURACAO_DIAS": "4",
            "EQUIPE_PREVISTA": "4 Carpinteiros + 3 Armadores + 2 Pedreiros + 5 Serventes",
            "HEADCOUNT_PREVISTO": "14",
            "EQUIPAMENTOS_PREVISTOS": "LOC-05 Gerador + Vibrador 45mm + Calhas",
            "MATERIAIS_UCC": "Concreto fck 30 MPa + Compensado resinado 17mm",
            "RUP_META_HH_UNID": "1,10 HH/m³",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-011",
            "SEMANA": "Semana 06",
            "DIAS_SEMANA": "Dias 31 a 33 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 3 e 1 (Baldrames e Pilares P1 a P8)",
            "VAGAO_ESTEIRA": "Vagão 03: Vigas Baldrames",
            "SERVICO_LOTE": "Concretagem VB13 a VB19 + Fôrmas e Armação Pilares P1 a P8 (Etapa 1)",
            "META_FISICA": "4,64 m³ conc baldrames + 8 pilares (28,6 m² fôrmas + 131 kg aço)",
            "DURACAO_DIAS": "3",
            "EQUIPE_PREVISTA": "4 Carpinteiros + 3 Armadores + 2 Pedreiros + 5 Serventes",
            "HEADCOUNT_PREVISTO": "14",
            "EQUIPAMENTOS_PREVISTOS": "Prumos metálicos + Vibrador 45mm + Andaimes tubulares",
            "MATERIAIS_UCC": "Concreto fck 30 MPa + Gravatas metálicas + Aço CA-50",
            "RUP_META_HH_UNID": "1,25 HH/m³",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-012",
            "SEMANA": "Semana 06",
            "DIAS_SEMANA": "Dias 34 a 36 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 1 e 2 (Pilares P1-8 Concreto & P9-16 Fôrmas)",
            "VAGAO_ESTEIRA": "Vagão 04: Pilares Supraestrutura",
            "SERVICO_LOTE": "Concretagem Pilares P1 a P8 (Etapa 1) + Fôrmas Pilares P9 a P16 (Etapa 2)",
            "META_FISICA": "2,15 m³ concreto P1-8 + 8 pilares fôrmas P9-16 (28,6 m² + 131 kg)",
            "DURACAO_DIAS": "3",
            "EQUIPE_PREVISTA": "4 Carpinteiros + 3 Armadores + 2 Pedreiros + 5 Serventes",
            "HEADCOUNT_PREVISTO": "14",
            "EQUIPAMENTOS_PREVISTOS": "Vibrador mangote 45mm + Prumos + Andaimes tubulares",
            "MATERIAIS_UCC": "Concreto bombeável fck 30 MPa + Gravatas e sarrafos",
            "RUP_META_HH_UNID": "1,25 HH/m³",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-013",
            "SEMANA": "Semana 07",
            "DIAS_SEMANA": "Dias 37 a 39 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 2 e 3 (Pilares P9-16 Concreto & P17-24 Fôrmas)",
            "VAGAO_ESTEIRA": "Vagão 04: Pilares Supraestrutura",
            "SERVICO_LOTE": "Concretagem Pilares P9 a P16 + Fôrmas Pilares P17 a P24 (Etapa 3)",
            "META_FISICA": "2,15 m³ conc P9-16 + 8 pilares fôrmas P17-24 (28,6 m² + 131 kg)",
            "DURACAO_DIAS": "3",
            "EQUIPE_PREVISTA": "4 Carpinteiros + 3 Armadores + 2 Pedreiros + 5 Serventes",
            "HEADCOUNT_PREVISTO": "14",
            "EQUIPAMENTOS_PREVISTOS": "Vibrador mangote 45mm + Andaimes + LOC-05 Gerador",
            "MATERIAIS_UCC": "Concreto bombeável fck 30 MPa + Compensado 17mm",
            "RUP_META_HH_UNID": "1,20 HH/m³",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-014",
            "SEMANA": "Semana 07",
            "DIAS_SEMANA": "Dias 40 a 42 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 3 e 1 (Pilares P17-24 & Vigas Laje V101-108)",
            "VAGAO_ESTEIRA": "Vagão 04: Pilares Supraestrutura",
            "SERVICO_LOTE": "Concretagem Pilares P17 a P24 + Cimbramento Vigas V101 a V108 (Etapa 1)",
            "META_FISICA": "2,14 m³ conc pilares (Total 24 P = 6,44 m³) + 104 m² fôrmas vigas",
            "DURACAO_DIAS": "3",
            "EQUIPE_PREVISTA": "4 Carpinteiros + 3 Armadores + 2 Pedreiros + 5 Serventes",
            "HEADCOUNT_PREVISTO": "14",
            "EQUIPAMENTOS_PREVISTOS": "Cimbramento metálico modulado (LOC-08) + Vibrador 45mm",
            "MATERIAIS_UCC": "Concreto fck 30 MPa + Escoramento metálico + Aço CA-50",
            "RUP_META_HH_UNID": "1,30 HH/m³",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-015",
            "SEMANA": "Semana 08",
            "DIAS_SEMANA": "Dias 43 a 45 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 2 e 3 (Vigas Laje V109 a V115)",
            "VAGAO_ESTEIRA": "Vagão 05: Vigas & Laje H12",
            "SERVICO_LOTE": "Montagem Cimbramento e Armação Vigas V109 a V115 (Etapas 2 e 3)",
            "META_FISICA": "7 vigas superiores (104 m² fôrmas + 940 kg aço CA-50 cortado)",
            "DURACAO_DIAS": "5",
            "EQUIPE_PREVISTA": "4 Carpinteiros + 3 Armadores + 2 Pedreiros + 5 Serventes",
            "HEADCOUNT_PREVISTO": "14",
            "EQUIPAMENTOS_PREVISTOS": "Cimbramento metálico modulado (LOC-08) + Dobradeira",
            "MATERIAIS_UCC": "Compensado resinado 17mm + Aço CA-50 + Espaçadores",
            "RUP_META_HH_UNID": "1,25 HH/m³",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-016",
            "SEMANA": "Semana 08",
            "DIAS_SEMANA": "Dias 46 a 48 (Qui-Sáb)",
            "ETAPA_ZONA": "Térreo Geral (Laje Superior H12)",
            "VAGAO_ESTEIRA": "Vagão 05: Vigas & Laje H12",
            "SERVICO_LOTE": "Vigotas Treliçadas, Blocos EPS, Malha Q-138 e Concretagem Laje H12",
            "META_FISICA": "968,8 m vigotas + 1.148 EPS + 999 kg malha + 13,17 m³ conc fck 30",
            "DURACAO_DIAS": "4",
            "EQUIPE_PREVISTA": "1 Mestre + 4 Carpinteiros + 3 Pedreiros + 6 Serventes",
            "HEADCOUNT_PREVISTO": "14",
            "EQUIPAMENTOS_PREVISTOS": "Bomba de concreto sobre caminhão + Vibradores mangote",
            "MATERIAIS_UCC": "Concreto bombeável fck 30 MPa (2 betoneiras) + Malha Q-138",
            "RUP_META_HH_UNID": "0,75 HH/m³",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-017",
            "SEMANA": "Semana 09",
            "DIAS_SEMANA": "Dias 49 a 51 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 1 (Zona 1 - Recepção/Diretoria)",
            "VAGAO_ESTEIRA": "Vagão 06: Alvenaria de Vedação",
            "SERVICO_LOTE": "Alvenaria de Vedação Blocos Concreto 14x19x39 - Etapa 1",
            "META_FISICA": "85 m² alvenaria de blocos com vergas, contravergas e telas",
            "DURACAO_DIAS": "7",
            "EQUIPE_PREVISTA": "5 Pedreiros + 5 Serventes (SUB-02)",
            "HEADCOUNT_PREVISTO": "10",
            "EQUIPAMENTOS_PREVISTOS": "LOC-06 Betoneira 400L + Masseiras + Andaimes",
            "MATERIAIS_UCC": "Blocos de concreto 14x19x39 + Argamassa pronta + Telas",
            "RUP_META_HH_UNID": "0,80 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-018",
            "SEMANA": "Semana 09",
            "DIAS_SEMANA": "Dias 52 a 54 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 2 (Zona 2 - Salas Técnicas/CPD)",
            "VAGAO_ESTEIRA": "Vagão 06: Alvenaria de Vedação",
            "SERVICO_LOTE": "Alvenaria de Vedação Blocos Concreto 14x19x39 - Etapa 2 [Esteira Move]",
            "META_FISICA": "85 m² alvenaria de blocos com vergas e eletrodutos embutidos",
            "DURACAO_DIAS": "7",
            "EQUIPE_PREVISTA": "5 Pedreiros + 5 Serventes (SUB-02)",
            "HEADCOUNT_PREVISTO": "10",
            "EQUIPAMENTOS_PREVISTOS": "LOC-06 Betoneira 400L + Andaimes tubulares",
            "MATERIAIS_UCC": "Blocos de concreto + Argamassa pronta de assentamento",
            "RUP_META_HH_UNID": "0,80 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-019",
            "SEMANA": "Semana 10",
            "DIAS_SEMANA": "Dias 55 a 57 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 3 (Zona 3 - Sanitários e Apoio)",
            "VAGAO_ESTEIRA": "Vagão 06: Alvenaria de Vedação",
            "SERVICO_LOTE": "Alvenaria de Vedação Blocos Concreto - Etapa 3 [Conclusão Paredes]",
            "META_FISICA": "80 m² alvenaria divisórias WCs e copa com encunhamento",
            "DURACAO_DIAS": "6",
            "EQUIPE_PREVISTA": "5 Pedreiros + 5 Serventes (SUB-02)",
            "HEADCOUNT_PREVISTO": "10",
            "EQUIPAMENTOS_PREVISTOS": "LOC-06 Betoneira 400L + Andaimes tubulares",
            "MATERIAIS_UCC": "Blocos de concreto + Argamassa expansiva de encunhamento",
            "RUP_META_HH_UNID": "0,80 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-020",
            "SEMANA": "Semana 10",
            "DIAS_SEMANA": "Dias 58 a 60 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 1 a 3 (Cobertura e Platibanda)",
            "VAGAO_ESTEIRA": "Vagão 07: Cobertura Metálica",
            "SERVICO_LOTE": "Montagem das Terças Metálicas da Cobertura e Rufos",
            "META_FISICA": "381 m² projeção de terças galvanizadas perfil U + linha de vida",
            "DURACAO_DIAS": "10",
            "EQUIPE_PREVISTA": "3 Montadores Especialistas + 2 Ajudantes + 4 Serventes Apoio",
            "HEADCOUNT_PREVISTO": "9",
            "EQUIPAMENTOS_PREVISTOS": "Guincho elétrico de coluna + Linha de vida + Cinto duplo",
            "MATERIAIS_UCC": "Perfis metálicos U enrijecidos galvanizados + Chumbadores",
            "RUP_META_HH_UNID": "0,35 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-021",
            "SEMANA": "Semana 11",
            "DIAS_SEMANA": "Dias 61 a 63 (Seg-Qua)",
            "ETAPA_ZONA": "Cobertura Superior",
            "VAGAO_ESTEIRA": "Vagão 07: Cobertura Metálica",
            "SERVICO_LOTE": "Instalação de Telhas Termoacústicas Sandwich PIR 30mm",
            "META_FISICA": "381 m² telhas sandwich PIR + calhas de beiral e rufos",
            "DURACAO_DIAS": "10",
            "EQUIPE_PREVISTA": "3 Montadores Especialistas + 2 Ajudantes + 4 Serventes Apoio",
            "HEADCOUNT_PREVISTO": "9",
            "EQUIPAMENTOS_PREVISTOS": "Parafusadeiras a bateria + EPIs específicos NR-35",
            "MATERIAIS_UCC": "Telhas sandwich trapezoidais PIR + Parafusos autobrocantes",
            "RUP_META_HH_UNID": "0,28 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-022",
            "SEMANA": "Semana 11",
            "DIAS_SEMANA": "Dias 64 a 66 (Qui-Sáb)",
            "ETAPA_ZONA": "Todos os Setores (Embutidos)",
            "VAGAO_ESTEIRA": "Vagão 08: Instalações Embutidas",
            "SERVICO_LOTE": "Ranhuras, Eletrodutos, Caixas de Tomada e Tubulações Embutidas",
            "META_FISICA": "180 m eletrodutos flexíveis + 140 m tubos PVC esgoto e água",
            "DURACAO_DIAS": "10",
            "EQUIPE_PREVISTA": "2 Eletricistas + 2 Encanadores + 4 Serventes (SUB-03/04)",
            "HEADCOUNT_PREVISTO": "8",
            "EQUIPAMENTOS_PREVISTOS": "Ranhuradora mecânica com aspirador + Termofusora 220V",
            "MATERIAIS_UCC": "Tubos PVC esgoto tigre + Eletrodutos corrugados antichama",
            "RUP_META_HH_UNID": "0,55 HH/m",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-023",
            "SEMANA": "Semana 12",
            "DIAS_SEMANA": "Dias 67 a 69 (Seg-Qua)",
            "ETAPA_ZONA": "Redes Hidráulicas (Portão de Qualidade 3)",
            "VAGAO_ESTEIRA": "Vagão 08: Instalações Embutidas",
            "SERVICO_LOTE": "Teste Hidrostático Pressurizado 72h em Redes de Água e Esgoto",
            "META_FISICA": "Pressão de 6 kgf/cm² por 72h em 16 pontos de consumo (Portão 3)",
            "DURACAO_DIAS": "3",
            "EQUIPE_PREVISTA": "1 Encanador Oficial + 1 TST + 2 Serventes",
            "HEADCOUNT_PREVISTO": "4",
            "EQUIPAMENTOS_PREVISTOS": "Bomba manual de teste hidrostático + Manômetro aferido",
            "MATERIAIS_UCC": "Água tratada + Plugs e registros de retenção",
            "RUP_META_HH_UNID": "0,15 HH/ponto",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-024",
            "SEMANA": "Semana 12",
            "DIAS_SEMANA": "Dias 70 a 72 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 1 e 2 (Paredes Internas)",
            "VAGAO_ESTEIRA": "Vagão 09: Reboco Paulista",
            "SERVICO_LOTE": "Chapisco Rolado com Resina Acrílica Fixadora nas Paredes",
            "META_FISICA": "440 m² chapisco rolado traço 1:3 com Bianco",
            "DURACAO_DIAS": "2",
            "EQUIPE_PREVISTA": "4 Pedreiros + 4 Serventes (SUB-02)",
            "HEADCOUNT_PREVISTO": "8",
            "EQUIPAMENTOS_PREVISTOS": "LOC-06 Betoneira 400L + Rolos para textura",
            "MATERIAIS_UCC": "Cimento CP II + Areia grossa + Aditivo adesivo Bianco",
            "RUP_META_HH_UNID": "0,25 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-025",
            "SEMANA": "Semana 13",
            "DIAS_SEMANA": "Dias 73 a 75 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 1 (Zona 1 - Recepção/Diretoria)",
            "VAGAO_ESTEIRA": "Vagão 09: Reboco Paulista",
            "SERVICO_LOTE": "Emboço/Reboco Paulista Projetado Mecanicamente - Etapa 1",
            "META_FISICA": "220 m² reboco espessura 2,0 cm com mestras metálicas",
            "DURACAO_DIAS": "6",
            "EQUIPE_PREVISTA": "4 Pedreiros + 4 Serventes (SUB-02)",
            "HEADCOUNT_PREVISTO": "8",
            "EQUIPAMENTOS_PREVISTOS": "LOC-09 Projetor Mecânico de Argamassa + Réguas alumínio",
            "MATERIAIS_UCC": "Argamassa pronta de emboço projetado + Cantoneiras PVC",
            "RUP_META_HH_UNID": "0,60 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-026",
            "SEMANA": "Semana 13",
            "DIAS_SEMANA": "Dias 76 a 78 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 2 e 3 (Salas Técnicas e Sanitários)",
            "VAGAO_ESTEIRA": "Vagão 09: Reboco Paulista",
            "SERVICO_LOTE": "Emboço/Reboco Paulista Projetado - Etapa 2 e 3 [Esteira Move]",
            "META_FISICA": "220 m² reboco desempenado (Total paredes = 440 m²)",
            "DURACAO_DIAS": "6",
            "EQUIPE_PREVISTA": "4 Pedreiros + 4 Serventes (SUB-02)",
            "HEADCOUNT_PREVISTO": "8",
            "EQUIPAMENTOS_PREVISTOS": "LOC-09 Projetor Mecânico de Argamassa + Desempenadeiras",
            "MATERIAIS_UCC": "Argamassa pronta de emboço projetado + Aditivo plastificante",
            "RUP_META_HH_UNID": "0,60 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-027",
            "SEMANA": "Semana 14",
            "DIAS_SEMANA": "Dias 79 a 81 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 3 (Sanitários e Copa - Áreas Molhadas)",
            "VAGAO_ESTEIRA": "Vagão 10: Pisos & Porcelanato",
            "SERVICO_LOTE": "Impermeabilização com Membrana Polimérica em Sanitários e Copa",
            "META_FISICA": "65 m² membrana com tela de poliéster em ralos e cantos",
            "DURACAO_DIAS": "3",
            "EQUIPE_PREVISTA": "2 Impermeabilizadores + 3 Serventes (SUB-01)",
            "HEADCOUNT_PREVISTO": "5",
            "EQUIPAMENTOS_PREVISTOS": "Misturador mecânico de argamassa + Trinchas especiais",
            "MATERIAIS_UCC": "Argamassa polimérica flexível Viapol + Tela estruturante",
            "RUP_META_HH_UNID": "0,40 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-028",
            "SEMANA": "Semana 14",
            "DIAS_SEMANA": "Dias 82 a 84 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 1 e 2 (Áreas Secas)",
            "VAGAO_ESTEIRA": "Vagão 10: Pisos & Porcelanato",
            "SERVICO_LOTE": "Execução de Contrapiso Sarrafeado e Nivelado e=3cm",
            "META_FISICA": "180 m² contrapiso sarrafeado com nível a laser rotativo",
            "DURACAO_DIAS": "6",
            "EQUIPE_PREVISTA": "3 Pedreiros + 4 Serventes (SUB-02)",
            "HEADCOUNT_PREVISTO": "7",
            "EQUIPAMENTOS_PREVISTOS": "LOC-06 Betoneira 400L + Nível laser rotativo + Réguas",
            "MATERIAIS_UCC": "Argamassa semisseca de regularização traço 1:4",
            "RUP_META_HH_UNID": "0,50 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-029",
            "SEMANA": "Semana 15",
            "DIAS_SEMANA": "Dias 85 a 87 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 1 (Zona 1 - Recepção/Diretoria)",
            "VAGAO_ESTEIRA": "Vagão 10: Pisos & Porcelanato",
            "SERVICO_LOTE": "Assentamento de Porcelanato Retificado 60x60cm - Etapa 1",
            "META_FISICA": "90 m² porcelanato 60x60 com dupla colagem e niveladores",
            "DURACAO_DIAS": "5",
            "EQUIPE_PREVISTA": "3 Ladrilhistas + 3 Ajudantes (SUB-05)",
            "HEADCOUNT_PREVISTO": "6",
            "EQUIPAMENTOS_PREVISTOS": "Cortadora elétrica de bancada refrigerada + Ventosas",
            "MATERIAIS_UCC": "Porcelanato retificado 60x60cm + Argamassa AC-III branca",
            "RUP_META_HH_UNID": "0,70 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-030",
            "SEMANA": "Semana 15",
            "DIAS_SEMANA": "Dias 88 a 90 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 2 (Zona 2 - Salas Técnicas/CPD)",
            "VAGAO_ESTEIRA": "Vagão 10: Pisos & Porcelanato",
            "SERVICO_LOTE": "Assentamento de Porcelanato Retificado 60x60cm - Etapa 2",
            "META_FISICA": "90 m² porcelanato 60x60 com dupla colagem (Total = 180 m²)",
            "DURACAO_DIAS": "5",
            "EQUIPE_PREVISTA": "3 Ladrilhistas + 3 Ajudantes (SUB-05)",
            "HEADCOUNT_PREVISTO": "6",
            "EQUIPAMENTOS_PREVISTOS": "Cortadora elétrica de bancada + Espaçadores niveladores",
            "MATERIAIS_UCC": "Porcelanato retificado 60x60cm + Argamassa AC-III",
            "RUP_META_HH_UNID": "0,70 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-031",
            "SEMANA": "Semana 16",
            "DIAS_SEMANA": "Dias 91 a 93 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 3 (Sanitários e Copa - Paredes)",
            "VAGAO_ESTEIRA": "Vagão 10: Pisos & Porcelanato",
            "SERVICO_LOTE": "Assentamento de Cerâmica Esmaltada nas Paredes dos Sanitários",
            "META_FISICA": "110 m² cerâmica esmaltada até o teto com rejunte resinado",
            "DURACAO_DIAS": "4",
            "EQUIPE_PREVISTA": "3 Ladrilhistas + 3 Ajudantes (SUB-05)",
            "HEADCOUNT_PREVISTO": "6",
            "EQUIPAMENTOS_PREVISTOS": "Cortadora manual + Nível a laser + Desempenadeira denteada",
            "MATERIAIS_UCC": "Revestimento cerâmico esmaltado + Argamassa AC-II + Rejunte",
            "RUP_META_HH_UNID": "0,75 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-032",
            "SEMANA": "Semana 16",
            "DIAS_SEMANA": "Dias 94 a 96 (Qui-Sáb)",
            "ETAPA_ZONA": "Todos os Setores (Rejunte e Rodapés)",
            "VAGAO_ESTEIRA": "Vagão 10: Pisos & Porcelanato",
            "SERVICO_LOTE": "Rejuntamento Resinado Geral e Fixação de Rodapés em Porcelanato",
            "META_FISICA": "290 m² rejunte epóxi/resinado + 120 m rodapés de 10cm",
            "DURACAO_DIAS": "4",
            "EQUIPE_PREVISTA": "3 Ladrilhistas + 3 Ajudantes (SUB-05)",
            "HEADCOUNT_PREVISTO": "6",
            "EQUIPAMENTOS_PREVISTOS": "Espátulas emborrachadas + Esponjas de limpeza especial",
            "MATERIAIS_UCC": "Rejunte resinado impermeável + Rodapés cortados e polidos",
            "RUP_META_HH_UNID": "0,20 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-033",
            "SEMANA": "Semana 17",
            "DIAS_SEMANA": "Dias 97 a 99 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 1 e 2 (Caixilharia Externa)",
            "VAGAO_ESTEIRA": "Vagão 11: Esquadrias de Alumínio",
            "SERVICO_LOTE": "Instalação de Janelas de Alumínio Linha Suprema e Vidros Temperados",
            "META_FISICA": "22 m² janelas de correr com vidros acústicos 8mm e contra-marcos",
            "DURACAO_DIAS": "4",
            "EQUIPE_PREVISTA": "2 Montadores de Esquadrias + 2 Ajudantes",
            "HEADCOUNT_PREVISTO": "4",
            "EQUIPAMENTOS_PREVISTOS": "Ventosas duplas de sucção + Parafusadeiras a bateria",
            "MATERIAIS_UCC": "Esquadrias linha Suprema anodizada preta + Selante PU-40",
            "RUP_META_HH_UNID": "0,80 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-034",
            "SEMANA": "Semana 17",
            "DIAS_SEMANA": "Dias 100 a 102 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 3 e Fachadas (Portas e Vidros)",
            "VAGAO_ESTEIRA": "Vagão 11: Esquadrias de Alumínio",
            "SERVICO_LOTE": "Fixação de Portas de Alumínio, Vidros Fixos e Vedações PU",
            "META_FISICA": "20 m² portas de alumínio + vedações perimetrais com selante",
            "DURACAO_DIAS": "4",
            "EQUIPE_PREVISTA": "2 Montadores de Esquadrias + 2 Ajudantes",
            "HEADCOUNT_PREVISTO": "4",
            "EQUIPAMENTOS_PREVISTOS": "Pistolas aplicadoras de selante PU + Nível a laser",
            "MATERIAIS_UCC": "Portas completas com fechaduras lafon + Selante PU-40",
            "RUP_META_HH_UNID": "0,80 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-035",
            "SEMANA": "Semana 18",
            "DIAS_SEMANA": "Dias 103 a 105 (Seg-Qua)",
            "ETAPA_ZONA": "Todos os Setores (Tubulações HVAC)",
            "VAGAO_ESTEIRA": "Vagão 12: Climatização HVAC",
            "SERVICO_LOTE": "Instalação de Redes Frigorígenas de Cobre Isoladas e Drenos",
            "META_FISICA": "120 m tubulação de cobre com isolamento elastomérico + drenos PVC",
            "DURACAO_DIAS": "7",
            "EQUIPE_PREVISTA": "2 Técnicos de Refrigeração HVAC + 2 Ajudantes (SUB-08)",
            "HEADCOUNT_PREVISTO": "4",
            "EQUIPAMENTOS_PREVISTOS": "Conjunto de solda oxiacetilênica + Curvador de tubos",
            "MATERIAIS_UCC": "Tubos de cobre classe A + Isolamento Armaflex + Solda prata",
            "RUP_META_HH_UNID": "0,65 HH/m",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-036",
            "SEMANA": "Semana 18",
            "DIAS_SEMANA": "Dias 106 a 108 (Qui-Sáb)",
            "ETAPA_ZONA": "Todos os Setores (Pressurização e Vácuo HVAC)",
            "VAGAO_ESTEIRA": "Vagão 12: Climatização HVAC",
            "SERVICO_LOTE": "Pressurização com Nitrogênio e Teste de Vácuo em Linhas VRF",
            "META_FISICA": "Vácuo em 8 circuitos frigorígenos atingindo 500 microns",
            "DURACAO_DIAS": "3",
            "EQUIPE_PREVISTA": "2 Técnicos de Refrigeração HVAC + 2 Ajudantes (SUB-08)",
            "HEADCOUNT_PREVISTO": "4",
            "EQUIPAMENTOS_PREVISTOS": "Bomba de vácuo 12 CFM + Vacuômetro digital + Manifold",
            "MATERIAIS_UCC": "Gás Nitrogênio seco (N2) + Válvulas de serviço",
            "RUP_META_HH_UNID": "1,50 HH/circuito",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-037",
            "SEMANA": "Semana 19",
            "DIAS_SEMANA": "Dias 109 a 111 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 1 e 2 (Cabeamento Elétrico)",
            "VAGAO_ESTEIRA": "Vagão 13: Acabamentos Elétr./Hidr.",
            "SERVICO_LOTE": "Enfiamento de Cabos de Força, Iluminação e Cabling Cat.6",
            "META_FISICA": "1.200 m cabos elétricos antichama 2,5/4/6mm² + cabos Cat.6",
            "DURACAO_DIAS": "6",
            "EQUIPE_PREVISTA": "2 Eletricistas Instaladores + 2 Ajudantes (SUB-03)",
            "HEADCOUNT_PREVISTO": "4",
            "EQUIPAMENTOS_PREVISTOS": "Passa-fios de aço + Decapadores automáticos e multímetro",
            "MATERIAIS_UCC": "Cabos flexíveis antichama 750V + Cabo UTP Cat.6 Furukawa",
            "RUP_META_HH_UNID": "0,08 HH/m",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-038",
            "SEMANA": "Semana 19",
            "DIAS_SEMANA": "Dias 112 a 114 (Qui-Sáb)",
            "ETAPA_ZONA": "Todos os Setores (Quadros de Distribuição)",
            "VAGAO_ESTEIRA": "Vagão 13: Acabamentos Elétr./Hidr.",
            "SERVICO_LOTE": "Montagem, Barramentos e Identificação de Circuitos nos Quadros",
            "META_FISICA": "1 QGBT geral + 3 Quadros de Distribuição de Circuitos com DR",
            "DURACAO_DIAS": "4",
            "EQUIPE_PREVISTA": "2 Eletricistas Instaladores + 2 Ajudantes (SUB-03)",
            "HEADCOUNT_PREVISTO": "4",
            "EQUIPAMENTOS_PREVISTOS": "Alicate prensa-terminais hidráulico + Rotulador eletrônico",
            "MATERIAIS_UCC": "Disjuntores termomagnéticos Schneider + DPS classe II + DR",
            "RUP_META_HH_UNID": "4,50 HH/quadro",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-039",
            "SEMANA": "Semana 20",
            "DIAS_SEMANA": "Dias 115 a 117 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 1 e 2 (Paredes Internas)",
            "VAGAO_ESTEIRA": "Vagão 14: Pintura Acrílica Final",
            "SERVICO_LOTE": "Emassamento com Massa Corrida Acrílica e Lixamento Mecanizado",
            "META_FISICA": "270 m² aplicação de duas demãos de massa acrílica lixada",
            "DURACAO_DIAS": "3",
            "EQUIPE_PREVISTA": "4 Pintores Oficiais + 2 Ajudantes (SUB-06)",
            "HEADCOUNT_PREVISTO": "6",
            "EQUIPAMENTOS_PREVISTOS": "Lixadeiras orbitais elétricas acopladas a aspirador industrial",
            "MATERIAIS_UCC": "Massa corrida acrílica Suvinil + Selador acrílico primer",
            "RUP_META_HH_UNID": "0,25 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-040",
            "SEMANA": "Semana 20",
            "DIAS_SEMANA": "Dias 118 a 120 (Qui-Sáb)",
            "ETAPA_ZONA": "Etapa 3 e Fachadas Externas",
            "VAGAO_ESTEIRA": "Vagão 14: Pintura Acrílica Final",
            "SERVICO_LOTE": "Emassamento e Selador em Fachadas e Setor 3 [Esteira Move]",
            "META_FISICA": "270 m² aplicação de primer selador e massa acrílica",
            "DURACAO_DIAS": "2",
            "EQUIPE_PREVISTA": "4 Pintores Oficiais + 2 Ajudantes (SUB-06)",
            "HEADCOUNT_PREVISTO": "6",
            "EQUIPAMENTOS_PREVISTOS": "Andaime fachadeiro NR-18 + Lixadeiras de haste girafa",
            "MATERIAIS_UCC": "Selador acrílico pigmentado + Fitas crepe especiais",
            "RUP_META_HH_UNID": "0,25 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-041",
            "SEMANA": "Semana 21",
            "DIAS_SEMANA": "Dias 121 a 123 (Seg-Qua)",
            "ETAPA_ZONA": "Etapa 3 (Sanitários e Copa)",
            "VAGAO_ESTEIRA": "Vagão 13: Acabamentos Elétr./Hidr.",
            "SERVICO_LOTE": "Instalação de Bacias Acopladas, Cubas e Torneiras Temporizadas",
            "META_FISICA": "14 bacias sanitárias Deca + 8 lavatórios de bancada + 12 torneiras",
            "DURACAO_DIAS": "6",
            "EQUIPE_PREVISTA": "2 Encanadores Oficiais + 2 Ajudantes (SUB-04)",
            "HEADCOUNT_PREVISTO": "4",
            "EQUIPAMENTOS_PREVISTOS": "Chaves de lavatório + Nível bolha de precisão",
            "MATERIAIS_UCC": "Bacias Deca Vogue + Vedações de cera + Torneiras Docol antivandalismo",
            "RUP_META_HH_UNID": "1,20 HH/unid",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-042",
            "SEMANA": "Semana 21",
            "DIAS_SEMANA": "Dias 124 a 126 (Qui-Sáb)",
            "ETAPA_ZONA": "Todos os Setores (Luminárias LED)",
            "VAGAO_ESTEIRA": "Vagão 13: Acabamentos Elétr./Hidr.",
            "SERVICO_LOTE": "Instalação de Luminárias Painel LED 40W, Interruptores e Tomadas",
            "META_FISICA": "32 painéis LED embutir + 60 tomadas 2P+T 10A/20A com placas",
            "DURACAO_DIAS": "5",
            "EQUIPE_PREVISTA": "2 Eletricistas Instaladores + 2 Ajudantes (SUB-03)",
            "HEADCOUNT_PREVISTO": "4",
            "EQUIPAMENTOS_PREVISTOS": "Escadas de fibra de vidro isoladas + Chaves isoladas 1000V",
            "MATERIAIS_UCC": "Painéis LED 40W 6500K + Módulos Pial Legrand brancos",
            "RUP_META_HH_UNID": "0,65 HH/unid",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-043",
            "SEMANA": "Semana 22",
            "DIAS_SEMANA": "Dias 127 a 129 (Seg-Qua)",
            "ETAPA_ZONA": "Toda a Edificação (Demãos Finais Pintura)",
            "VAGAO_ESTEIRA": "Vagão 14: Pintura Acrílica Final",
            "SERVICO_LOTE": "Pintura Látex Acrílica Fosca Lavável em Duas Demãos de Acabamento",
            "META_FISICA": "540 m² duas demãos de tinta látex acrílica fosca acetinada",
            "DURACAO_DIAS": "7",
            "EQUIPE_PREVISTA": "4 Pintores Oficiais + 2 Ajudantes (SUB-06)",
            "HEADCOUNT_PREVISTO": "6",
            "EQUIPAMENTOS_PREVISTOS": "Máquina de pintura Airless de alta pressão + Rolos microfibra",
            "MATERIAIS_UCC": "Tinta acrílica Suvinil Toque de Seda + Plásticos para isolamento",
            "RUP_META_HH_UNID": "0,20 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-044",
            "SEMANA": "Semana 22",
            "DIAS_SEMANA": "Dias 130 a 132 (Qui-Sáb)",
            "ETAPA_ZONA": "Todos os Setores (Climatização Startup)",
            "VAGAO_ESTEIRA": "Vagão 12: Climatização HVAC",
            "SERVICO_LOTE": "Instalação de Evaporadoras Cassete, Carga de Gás R-410A e Startup",
            "META_FISICA": "8 evaporadoras Cassete conectadas e 2 condensadoras ligadas",
            "DURACAO_DIAS": "6",
            "EQUIPE_PREVISTA": "2 Técnicos de Refrigeração HVAC + 2 Ajudantes (SUB-08)",
            "HEADCOUNT_PREVISTO": "4",
            "EQUIPAMENTOS_PREVISTOS": "Balança digital de carga de fluido + Termômetro de contato",
            "MATERIAIS_UCC": "Aparelhos Splits Inverter 36.000 BTU + Gás refrigerante R-410A",
            "RUP_META_HH_UNID": "3,00 HH/unid",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-045",
            "SEMANA": "Semana 23",
            "DIAS_SEMANA": "Dias 133 a 135 (Seg-Qua)",
            "ETAPA_ZONA": "Edifício Administrativo Turnkey",
            "VAGAO_ESTEIRA": "Vagão 15: Comissionamento & Entrega",
            "SERVICO_LOTE": "Comissionamento Elétrico sob Carga, Termografia e Equilíbrio HVAC",
            "META_FISICA": "Laudo termográfico de quadros + Laudo de vazão e temperatura HVAC",
            "DURACAO_DIAS": "2",
            "EQUIPE_PREVISTA": "1 Engenheiro Residente + 2 Eletricistas + 1 Técnico HVAC",
            "HEADCOUNT_PREVISTO": "4",
            "EQUIPAMENTOS_PREVISTOS": "Câmera termográfica Fluke + Anemômetro de hélice digital",
            "MATERIAIS_UCC": "Etiquetas de calibração + Formulários técnicos DataBook",
            "RUP_META_HH_UNID": "2,00 HH/sistema",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-046",
            "SEMANA": "Semana 23",
            "DIAS_SEMANA": "Dias 136 a 138 (Qui-Sáb)",
            "ETAPA_ZONA": "Edifício Administrativo Turnkey",
            "VAGAO_ESTEIRA": "Vagão 15: Comissionamento & Entrega",
            "SERVICO_LOTE": "Limpeza Química Pós-Obra Especializada e Desmobilização de Canteiro",
            "META_FISICA": "381 m² área interna com pisos encerados, vidros limpos e canteiro NR-18 desmobilizado",
            "DURACAO_DIAS": "2",
            "EQUIPE_PREVISTA": "1 Mestre de Obras + 4 Auxiliares de Limpeza Especializada",
            "HEADCOUNT_PREVISTO": "5",
            "EQUIPAMENTOS_PREVISTOS": "Enceradeira industrial + Lavadora de alta pressão + Caminhão Munck",
            "MATERIAIS_UCC": "Removedores pós-obra de resíduos + Cera impermeabilizante",
            "RUP_META_HH_UNID": "0,12 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-047",
            "SEMANA": "Semana 24",
            "DIAS_SEMANA": "Dias 139 a 141 (Seg-Qua)",
            "ETAPA_ZONA": "Edifício Administrativo Turnkey",
            "VAGAO_ESTEIRA": "Vagão 15: Comissionamento & Entrega",
            "SERVICO_LOTE": "Vistoria e Testes de Carga Elétrica, Automação e Pressão Hidráulica Final",
            "META_FISICA": "100% circuitos testados sob carga nominal + 16 pontos de água/esgoto aferidos",
            "DURACAO_DIAS": "2",
            "EQUIPE_PREVISTA": "1 Engenheiro Residente + 2 Eletricistas + 1 Encanador + 2 Serventes",
            "HEADCOUNT_PREVISTO": "6",
            "EQUIPAMENTOS_PREVISTOS": "Câmera termográfica Fluke + Multímetro digital + Manômetros calibrados",
            "MATERIAIS_UCC": "Relatórios técnicos de comissionamento + Plugs e fusíveis de reserva",
            "RUP_META_HH_UNID": "1,00 HH/teste",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-048",
            "SEMANA": "Semana 24",
            "DIAS_SEMANA": "Dias 142 a 144 (Qui-Sáb)",
            "ETAPA_ZONA": "Edifício Administrativo Turnkey",
            "VAGAO_ESTEIRA": "Vagão 15: Comissionamento & Entrega",
            "SERVICO_LOTE": "Consolidação de Desenhos As-Built, Manuais de Operação e Termos de Garantia",
            "META_FISICA": "DataBook completo (3 pastas físicas + pen-drive digital) com pranchas as-built",
            "DURACAO_DIAS": "1",
            "EQUIPE_PREVISTA": "1 Engenheiro Residente + 1 Técnico de Edificações + 2 Apoio Administrativo",
            "HEADCOUNT_PREVISTO": "4",
            "EQUIPAMENTOS_PREVISTOS": "Plotter + Scanner profissional + Estação CAD",
            "MATERIAIS_UCC": "Pastas técnicas de arquivo + Mídias digitais criptografadas",
            "RUP_META_HH_UNID": "0,50 HH/documento",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-049",
            "SEMANA": "Semana 25",
            "DIAS_SEMANA": "Dias 145 a 147 (Seg-Qua)",
            "ETAPA_ZONA": "Edifício Administrativo Turnkey",
            "VAGAO_ESTEIRA": "Vagão 15: Comissionamento & Entrega",
            "SERVICO_LOTE": "Treinamento Técnico Operacional da Equipe de Facilties e Manutenção do Terminal",
            "META_FISICA": "16 horas de capacitação presencial com entrega de certificados operacionais",
            "DURACAO_DIAS": "1",
            "EQUIPE_PREVISTA": "1 Engenheiro Residente + 1 Técnico HVAC + 1 Eletricista Instalador",
            "HEADCOUNT_PREVISTO": "3",
            "EQUIPAMENTOS_PREVISTOS": "Projetor multimídia + Painel simulador didático",
            "MATERIAIS_UCC": "Apostilas operacionais plastificadas + Fichas de inspeção preventiva",
            "RUP_META_HH_UNID": "1,50 HH/módulo",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-050",
            "SEMANA": "Semana 25",
            "DIAS_SEMANA": "Dias 148 a 150 (Qui-Sáb)",
            "ETAPA_ZONA": "Edifício Administrativo Turnkey",
            "VAGAO_ESTEIRA": "Vagão 15: Comissionamento & Entrega",
            "SERVICO_LOTE": "Auditoria Final de Qualidade, SST e Desmobilização Total do Canteiro NR-18",
            "META_FISICA": "100% canteiro desmobilizado com terreno limpo e regularizado (368 m²)",
            "DURACAO_DIAS": "1",
            "EQUIPE_PREVISTA": "1 Mestre de Obras + 4 Serventes Apoio",
            "HEADCOUNT_PREVISTO": "5",
            "EQUIPAMENTOS_PREVISTOS": "Caminhão Munck 12t + Caçambas estacionárias",
            "MATERIAIS_UCC": "Cargas de descarte ambiental homologadas + Termo PGRCC",
            "RUP_META_HH_UNID": "0,20 HH/m²",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-051",
            "SEMANA": "Semana 26",
            "DIAS_SEMANA": "Dias 151 a 153 (Seg-Qua)",
            "ETAPA_ZONA": "Edifício Administrativo Turnkey",
            "VAGAO_ESTEIRA": "Vagão 15: Comissionamento & Entrega",
            "SERVICO_LOTE": "Vistoria Conjunta de Recebimento Provisório (Fiscalização do Porto x Construtora)",
            "META_FISICA": "Laudo de vistoria sem pendências impeditivas e assinatura do Termo Provisório",
            "DURACAO_DIAS": "1",
            "EQUIPE_PREVISTA": "1 Engenheiro Residente + 1 Mestre de Obras + Fiscalização Portuária",
            "HEADCOUNT_PREVISTO": "3",
            "EQUIPAMENTOS_PREVISTOS": "Nível a laser + Trena eletrônica + Formulário digital de vistoria",
            "MATERIAIS_UCC": "Fichas FVS assinadas de todos os portões de qualidade",
            "RUP_META_HH_UNID": "1,00 HH/vistoria",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        },
        {
            "COD_LOTE": "LOTE-052",
            "SEMANA": "Semana 26",
            "DIAS_SEMANA": "Dias 154 a 156 (Qui-Sáb)",
            "ETAPA_ZONA": "Edifício Administrativo Turnkey",
            "VAGAO_ESTEIRA": "Vagão 15: Comissionamento & Entrega",
            "SERVICO_LOTE": "Assinatura do Termo de Recebimento Definitivo e Entrega das Chaves Turnkey",
            "META_FISICA": "Entrega oficial das chaves do Edifício Administrativo TMULT 100% operacional",
            "DURACAO_DIAS": "2",
            "EQUIPE_PREVISTA": "Diretoria Técnica + Engenheiro Residente + Gestores TMULT",
            "HEADCOUNT_PREVISTO": "3",
            "EQUIPAMENTOS_PREVISTOS": "Kit oficial de chaves codificadas + Controle de acesso RFID",
            "MATERIAIS_UCC": "Termo de Entrega Definitiva + Garantias legais da construção",
            "RUP_META_HH_UNID": "1,00 HH/entrega",
            "STATUS_EXECUCAO": "PROGRAMADO",
            "RDO_VINCULADO": ""
        }
    ]
    return lotes

def salvar_programacao_obra(nome_obra, takt_dias=3):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    pasta_obra = os.path.join(root_dir, 'projetos', nome_obra)
    pasta_plan = os.path.join(pasta_obra, '03_PLANEJAMENTO_E_CRONOGRAMA')
    
    if not os.path.exists(pasta_plan):
        os.makedirs(pasta_plan, exist_ok=True)
        
    sigla = nome_obra.replace('OBRA_', '')
    dest_paths = [
        os.path.join(pasta_plan, f'PROGRAMACAO_CURTO_PRAZO_{sigla}.csv'),
        os.path.join(pasta_plan, f'PROGRAMACAO_CURTO_PRAZO_{nome_obra}.csv'),
    ]
    if nome_obra == 'OBRA_TMULT':
        dest_paths.append(os.path.join(pasta_plan, 'PROGRAMACAO_CURTO_PRAZO_TMULT.csv'))
        
    dest_template = os.path.join(root_dir, 'projetos', '_TEMPLATE_OBRA_NOVA', '03_PLANEJAMENTO_E_CRONOGRAMA', 'TEMPLATE_PROGRAMACAO_CURTO_PRAZO.csv')
    if os.path.exists(os.path.dirname(dest_template)):
        dest_paths.append(dest_template)
        
    lotes = obter_lotes_padrao(nome_obra)
    
    # Derivação dinâmica do CPM se dados_cpm.json existir na obra
    cpm_path = os.path.join(pasta_plan, 'dados_cpm.json')
    duracoes_cpm = derivar_duracoes_do_cpm(cpm_path)
    if duracoes_cpm:
        print(f'[*] Sincronizando {len(lotes)} lotes com as durações reais do CPM ({cpm_path})...')
        for lote in lotes:
            cod = lote['COD_LOTE']
            if cod in duracoes_cpm:
                lote['DURACAO_DIAS'] = str(duracoes_cpm[cod])

    # Mapeamento do Calendário Operacional Heijunka (178 dias úteis CPM - Início 01/10/2026)
    import datetime
    base_dt = datetime.date(2026, 10, 1)
    def day_to_date(day_idx):
        cur = base_dt
        added = 0
        while added < (day_idx - 1):
            cur += datetime.timedelta(days=1)
            if cur.weekday() != 6:
                added += 1
        return cur

    weekday_br = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    LOTE_CALENDARIO_CPM = {
        "LOTE-001": (1, 10),
        "LOTE-002": (11, 12),
        "LOTE-003": (13, 14),
        "LOTE-004": (15, 16),
        "LOTE-005": (17, 18),
        "LOTE-006": (19, 20),
        "LOTE-007": (21, 23),
        "LOTE-008": (24, 27),
        "LOTE-009": (28, 31),
        "LOTE-010": (32, 34),
        "LOTE-011": (35, 37),
        "LOTE-012": (38, 40),
        "LOTE-013": (41, 43),
        "LOTE-014": (44, 46),
        "LOTE-015": (47, 54),
        "LOTE-016": (55, 67),
        "LOTE-017": (68, 74),
        "LOTE-018": (75, 81),
        "LOTE-019": (82, 87),
        "LOTE-020": (68, 77),
        "LOTE-021": (88, 97),
        "LOTE-022": (98, 107),
        "LOTE-023": (108, 110),
        "LOTE-024": (111, 112),
        "LOTE-025": (113, 118),
        "LOTE-026": (119, 124),
        "LOTE-027": (125, 127), # Impermeabilização WCs (Zona 03) -> 23/02/2027 a 25/02/2027
        "LOTE-028": (125, 130), # Contrapiso (Zonas 01 e 02) -> 23/02/2027 a 01/03/2027
        "LOTE-029": (131, 135), # Porcelanato Z1 -> 02/03/2027 a 06/03/2027
        "LOTE-030": (136, 140), # Porcelanato Z2 -> 08/03/2027 a 12/03/2027
        "LOTE-031": (141, 144), # Cerâmica Z3 -> 13/03/2027 a 17/03/2027
        "LOTE-032": (145, 148), # Rodapés -> 18/03/2027 a 22/03/2027
        "LOTE-033": (140, 143), # Esquadrias Janelas
        "LOTE-034": (145, 148), # Esquadrias Fachada e Portas
        "LOTE-035": (134, 139), # HVAC Dutos
        "LOTE-036": (140, 142), # HVAC Vácuo e Condensadoras
        "LOTE-037": (128, 133), # Fiação e Telecom
        "LOTE-038": (141, 144), # Quadros CPD
        "LOTE-039": (149, 151), # Pintura 1a Demão Z1-Z2
        "LOTE-040": (152, 153), # Pintura 1a Demão Z3
        "LOTE-041": (154, 159), # Louças e Metais
        "LOTE-042": (154, 158), # Luminárias LED
        "LOTE-043": (163, 166), # Pintura Final Demãos
        "LOTE-044": (159, 162), # Aparelhos HVAC
        "LOTE-045": (167, 168), # Comissionamento Elétrico
        "LOTE-046": (173, 174), # Limpeza Pós-Obra
        "LOTE-047": (169, 170), # Vistoria Carga
        "LOTE-048": (171, 171), # As-Built DataBook
        "LOTE-049": (172, 172), # Treinamento Operacional
        "LOTE-050": (175, 175), # Auditoria SST e Desmobilização
        "LOTE-051": (176, 176), # Vistoria Provisória
        "LOTE-052": (177, 178), # Termo Definitivo e Handover Turnkey (Dia 178: 26/04/2027)
    }

    for lote in lotes:
        cod = lote['COD_LOTE']
        if cod in LOTE_CALENDARIO_CPM:
            d_ini, d_fim = LOTE_CALENDARIO_CPM[cod]
            dt_i = day_to_date(d_ini)
            dt_f = day_to_date(d_fim)
            lote['DATA_INICIO'] = dt_i.strftime("%d/%m/%Y")
            lote['DATA_FIM'] = dt_f.strftime("%d/%m/%Y")
            lote['DURACAO_DIAS'] = str(d_fim - d_ini + 1)
            w_i = weekday_br[dt_i.weekday()]
            w_f = weekday_br[dt_f.weekday()]
            if d_ini == d_fim:
                lote['DIAS_SEMANA'] = f"Dia {d_ini:03d} ({w_i})"
            else:
                lote['DIAS_SEMANA'] = f"Dias {d_ini:03d} a {d_fim:03d} ({w_i}-{w_f})"
                
    fieldnames = [
        'COD_LOTE', 'SEMANA', 'DIAS_SEMANA', 'DATA_INICIO', 'DATA_FIM',
        'ETAPA_ZONA', 'VAGAO_ESTEIRA', 'SERVICO_LOTE', 'META_FISICA',
        'DURACAO_DIAS', 'EQUIPE_PREVISTA', 'HEADCOUNT_PREVISTO',
        'EQUIPAMENTOS_PREVISTOS', 'MATERIAIS_UCC', 'RUP_META_HH_UNID',
        'STATUS_EXECUCAO', 'RDO_VINCULADO'
    ]
    
    # Grava em todos os destinos relevantes
    unique_paths = list(dict.fromkeys(dest_paths))
    for p in unique_paths:
        with open(p, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';', quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for lote in lotes:
                writer.writerow(lote)
        print(f'[LEAN TAKT] Sucesso: {len(lotes)} lotes gravados em {p}')
        
    # Sincronização Automática com a Linha de Balanço (LOB)
    try:
        import subprocess
        script_sync = os.path.join(root_dir, 'scripts', 'sincronizar_esteira_e_lob.py')
        if os.path.exists(script_sync):
            print('[SINCRONIZADOR LEAN] Disparando sincronização com a Linha de Balanço (LOB)...')
            subprocess.run([sys.executable, script_sync, '--obra', nome_obra, '--modo', 'esteira_para_lob'], check=True)
    except Exception as err:
        print(f'[!] Aviso: Sincronização com LOB via subprocesso falhou: {err}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gerador Universal de Programação de Curto Prazo em Esteira Lean (Takt Time)')
    parser.add_argument('--obra', type=str, default='OBRA_TMULT', help='Nome da pasta da obra em projetos/')
    parser.add_argument('--takt-dias', type=int, default=3, help='Duração do Takt Time em dias úteis (1 a 6 dias, padrão 3)')
    args = parser.parse_args()
    salvar_programacao_obra(args.obra, takt_dias=args.takt_dias)
