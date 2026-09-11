#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Geração de RDO (Relatório Diário de Obra) e Painel de Produção.

Uso:
    python scripts/gerar_rdo.py --obra OBRA_TMULT
    python scripts/gerar_rdo.py --dir projetos/OBRA_TMULT
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def parse_args():
    parser = argparse.ArgumentParser(description="Motor Universal de RDO e Painel de Produção.")
    parser.add_argument("--obra", type=str, default="OBRA_TMULT", help="Nome da pasta da obra em projetos/")
    parser.add_argument("--dir", type=str, default=None, help="Caminho direto para a pasta da obra")
    return parser.parse_args()


def carregar_dados_obra(obra_dir):
    config_path = os.path.join(obra_dir, "config_obra.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {
            "nome_obra": os.path.basename(obra_dir),
            "sigla_obra": os.path.basename(obra_dir)[:6].upper(),
            "prazo_meses": 6.0
        }
    
    # Tentar carregar contratos de empreiteiros
    contratos_path = os.path.join(obra_dir, "02_ORCAMENTO_BASE_E_CONTRATOS", "contratos_empreiteiros.json")
    contratos = []
    if os.path.exists(contratos_path):
        with open(contratos_path, "r", encoding="utf-8") as f:
            contratos = json.load(f)
            
    # Tentar carregar contratos de locação
    locacoes_path = os.path.join(obra_dir, "02_ORCAMENTO_BASE_E_CONTRATOS", "contratos_locacao.json")
    locacoes = []
    if os.path.exists(locacoes_path):
        with open(locacoes_path, "r", encoding="utf-8") as f:
            locacoes = json.load(f)

    return config, contratos, locacoes


def gerar_templates_rdo(output_dir, config):
    sigla = config.get("sigla_obra", "OBRA")
    nome = config.get("nome_obra", "Obra")
    
    template_md = f"""# 📋 TEMPLATE EXECUTIVO: Relatório Diário de Obra (RDO)
**Obra:** {nome} ({sigla})  
**Documento Padronizado segundo POP 02 (Rotina Lean) e SKILL_GESTAO_02 (Produção)**

---

## 📌 CABEÇALHO GERAL
* **Número do RDO:** RDO-[NÚMERO]
* **Data:** [DD/MM/AAAA] — [Dia da Semana]
* **Prazo Contratual:** Dia [D] de [TOTAL_DIAS] dias corridos
* **Engenheiro Residente:** [Nome / CREA]
* **Mestre de Obras:** [Nome]

---

## ☀️ CONDIÇÕES METEOROLÓGICAS E IMPACTOS
| Período | Condição | Temperatura | Condição de Trabalho | Horas Paralisação |
|---|---|---|---|:---:|
| **Manhã (07h às 12h)** | [ ] Sol [ ] Nublado [ ] Chuva Fraca [ ] Chuva Forte | [ ] °C | [ ] Praticável [ ] Parcial [ ] Impraticável | [0.0] h |
| **Tarde (13h às 17h)** | [ ] Sol [ ] Nublado [ ] Chuva Fraca [ ] Chuva Forte | [ ] °C | [ ] Praticável [ ] Parcial [ ] Impraticável | [0.0] h |

*Impacto no Caminho Crítico:* [ ] Nenhum [ ] Paralisação Parcial [ ] Paralisação Total  
*Frentes Remanejadas para Área Coberta:* [Listar ou indicar "N/A"]

---

## 👷 EFETIVO DE CANTEIRO (HEADCOUNT & HORAS HOMEM)
### 1. Equipe Própria / Gestão
* Engenheiro Residente: [N]
* Mestre de Obras: [N]
* Técnico de Segurança (TST): [N]
* Almoxarife / Apontador: [N]
* Vigia / Portaria: [N]

### 2. Mão de Obra de Empreiteiros Terceirizados
| Pacote / Contrato | Empresa / Encarregado | Oficiais | Serventes | Total Efetivo | Horas Trabalhadas |
|---|---|:---:|:---:|:---:|:---:|
| **SUB-01:** Estrutura e Fundações | [Nome Empreiteiro] | [ ] | [ ] | [ ] | [ ] h |
| **SUB-02:** Alvenaria e Vedações | [Nome Empreiteiro] | [ ] | [ ] | [ ] | [ ] h |
| **SUB-03:** Cobertura e Calhas | [Nome Empreiteiro] | [ ] | [ ] | [ ] | [ ] h |
| **SUB-04:** Esquadrias Metálicas | [Nome Empreiteiro] | [ ] | [ ] | [ ] | [ ] h |
| **SUB-05:** Instalações Hidráulicas | [Nome Empreiteiro] | [ ] | [ ] | [ ] | [ ] h |
| **SUB-06:** Instalações Elétricas / SPDA | [Nome Empreiteiro] | [ ] | [ ] | [ ] | [ ] h |
| **SUB-07:** Impermeabilização | [Nome Empreiteiro] | [ ] | [ ] | [ ] | [ ] h |
| **SUB-08:** Pintura e Acabamentos | [Nome Empreiteiro] | [ ] | [ ] | [ ] | [ ] h |
| **TOTAL GERAL DE EFETIVO NO DIA:** | — | **[ ]** | **[ ]** | **[ ]** | **[ ] HH** |

---

## 🚜 EQUIPAMENTOS EM OPERAÇÃO NO CANTEIRO
| Código / Equipamento | Regime | Status no Dia | Horas de Operação | Ocorrência / Manutenção |
|---|---|---|:---:|---|
| **LOC-01:** Mini Retroescavadeira | Diária / Mensal | [ ] Operando [ ] Parado [ ] Manutenção | [ ] h | [Obs] |
| **LOC-02:** Betoneira 400L Elétrica | Mensal | [ ] Operando [ ] Parado [ ] Manutenção | [ ] h | [Obs] |
| **LOC-03:** Compactador Tipo Sapo | Mensal | [ ] Operando [ ] Parado [ ] Manutenção | [ ] h | [Obs] |
| **LOC-04:** Andaimes Fachadeiros | Mensal | [ ] Operando [ ] Ocioso | [ ] h | [Obs] |
| **LOC-05:** Gerador de Energia 15 kVA | Mensal | [ ] Operando [ ] Standby | [ ] h | [Obs] |
| **LOC-06:** Caçambas Estacionárias | Por Troca | [ ] Em uso [ ] Cheia aguardando coleta | — | [Obs] |

---

## 🔨 FRENTES DE SERVIÇO EXECUTADAS NO DIA (AMARRAÇÃO COM A EAP)
| Item EAP | Descrição da Atividade Executada | Local / Ambiente / Eixo | Quantidade Medida no Dia | Unidade |
|---|---|---|:---:|:---:|
| **1.1.[X]** | [Descrição detalhada da atividade] | [Ex: Sapatas S1-S8] | [0.00] | [m³/m²/kg] |
| **1.2.[X]** | [Descrição detalhada da atividade] | [Ex: Fôrma Viga V101] | [0.00] | [m²] |
| **2.1.[X]** | [Descrição detalhada da atividade] | [Ex: Alvenaria Eixo A-B] | [0.00] | [m²] |

---

## ✅ QUALIDADE E FVS (FICHAS DE VERIFICAÇÃO DE SERVIÇO)
* **FVSs Inspecionadas no Dia:**
  - [ ] FVS-[CÓDIGO]: [Descrição] — Resultado: [ ] Aprovado [ ] Reprovado com RNC
* **Corpos de Prova Moldados (Concreto):**
  - [ ] Concretagem realizada: [Volume m³] | Nota Fiscal Concreto: [Nº] | Lacre: [Nº]
  - [ ] Corpos de Prova: [Nº CPs] moldados para ruptura aos 7, 14 e 28 dias.

---

## ⚠️ OCORRÊNCIAS, IMPEDIMENTOS E INTERFERÊNCIAS
* **Paralisações:** [Indicar motivos e duração ou registrar "Sem paralisações relevantes"]
* **Acidentes / Quase-Acidentes:** [ ] Nenhum registro no dia [ ] Registrado (Descrever e acionar SESMT)
* **Visitas Técnicas / Fiscalização:** [Registrar fiscais, projetistas ou clientes que visitaram o canteiro]
* **Entregas de Materiais Recebidos:** [NF nº, Fornecedor, Material conferido segundo POP 06]

---

## 🎯 METAS E ALERTAS PARA O DIA SEGUINTE (D+1)
1. **Frente Prioritária:** [Atividade foco do dia seguinte]
2. **Suprimentos / Logística:** [Material a posicionar ou confirmar entrega]
3. **Equipamento:** [Revisão preventiva ou remanejamento programado]

---

## ✍️ VALIDAÇÃO E ASSINATURAS
* **Elaborado por (Mestre de Obras):** _______________________________________ Data: ____/____/________
* **Aprovado por (Engenheiro Residente):** ___________________________________ Data: ____/____/________
"""

    md_path = os.path.join(output_dir, "TEMPLATE_RDO_EXECUTIVO.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(template_md)

    # Template CSV de Lançamento Diário
    csv_header = (
        "NUM_RDO;DATA;DIA_SEMANA;CLIMA_MANHA;CLIMA_TARDE;CONDICAO_TRABALHO;HORAS_PARALISACAO;"
        "EFETIVO_PROPRIO;EFETIVO_TERCEIRO;TOTAL_EFETIVO;TOTAL_HH;"
        "EQUIPAMENTOS_ATIVOS;ITENS_EAP_EXECUTADOS;FVS_INSPECIONADA;STATUS_FVS;OCORRENCIAS;ENGENHEIRO_APROVADOR\n"
    )
    csv_path = os.path.join(output_dir, "TEMPLATE_RDO_EXECUTIVO.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(csv_header)


def gerar_rdos_piloto_semana1(output_dir, config):
    rdos_dir = os.path.join(output_dir, "RDOS")
    os.makedirs(rdos_dir, exist_ok=True)
    
    sigla = config.get("sigla_obra", "TMULT")
    nome = config.get("nome_obra", "TMULT — Edifício Administrativo")

    semana1_dados = [
        {
            "num": "001",
            "data": "22/09/2026",
            "dia": "Terça-feira",
            "clima_m": "Sol",
            "clima_t": "Sol",
            "temp": "24°C a 29°C",
            "cond": "Praticável",
            "h_paral": 0.0,
            "ef_prop": 5,
            "ef_terc": 8,
            "hh": 104,
            "eap": "1.0.1 (Mobilização Canteiro NR-18) e 1.1.1 (Locação Topográfica da Obra)",
            "equip": "LOC-01 (Mini Retro - 6h), LOC-05 (Gerador - 8h), LOC-03 (Sapo - 4h)",
            "fvs": "FVS-01-TOPOGRAFIA_E_LOCACAO",
            "fvs_status": "Aprovado",
            "obs": "Início oficial de mobilização. Entrega e montagem dos 4 containers NR-18 e ligação provisória de água pipa e gerador. Execução do gabarito de tábua corrida perimetral com estação total (POP 21). DDS de integração NR-18 aplicado a todos os 13 trabalhadores."
        },
        {
            "num": "002",
            "data": "23/09/2026",
            "dia": "Quarta-feira",
            "clima_m": "Sol",
            "clima_t": "Nublado",
            "temp": "23°C a 27°C",
            "cond": "Praticável",
            "h_paral": 0.0,
            "ef_prop": 5,
            "ef_terc": 10,
            "hh": 120,
            "eap": "1.1.1 (Escavação Mecânica e Manual de Sapatas S1 a S16)",
            "equip": "LOC-01 (Mini Retro - 8h), LOC-06 (Caçamba Estacionária)",
            "fvs": "FVS-01-TOPOGRAFIA_E_LOCACAO e FVS-02-FUNDACOES",
            "fvs_status": "Aprovado Parcial (Liberação de eixos 1 a 4)",
            "obs": "Escavação mecânica com mini retroescavadeira das primeiras 16 sapatas isoladas. Equipe de serventes fazendo o acerto manual de fundo de cava e descarte em caçamba. Sem interferências subterrâneas encontradas."
        },
        {
            "num": "003",
            "data": "24/09/2026",
            "dia": "Quinta-feira",
            "clima_m": "Nublado",
            "clima_t": "Chuva Fraca",
            "temp": "21°C a 25°C",
            "cond": "Praticável c/ Restrição",
            "h_paral": 1.0,
            "ef_prop": 5,
            "ef_terc": 11,
            "hh": 120,
            "eap": "1.1.1 (Escavação S17 a S32) e 1.1.2 (Apiloamento e Lastro de Concreto Magro S1 a S12)",
            "equip": "LOC-01 (Mini Retro - 6h), LOC-02 (Betoneira 400L - 5h), LOC-03 (Compactador - 4h)",
            "fvs": "FVS-02-FUNDACOES (Lastro Magro e Nivelamento)",
            "fvs_status": "Aprovado",
            "obs": "Chuva leve às 15h paralisou escavação externa por 1 hora. Equipe remanejada para montagem e corte de armaduras na bancada coberta do canteiro. Lançamento de concreto magro espessura 5cm nas sapatas S1 a S12."
        },
        {
            "num": "004",
            "data": "25/09/2026",
            "dia": "Sexta-feira",
            "clima_m": "Sol",
            "clima_t": "Sol",
            "temp": "22°C a 28°C",
            "cond": "Praticável",
            "h_paral": 0.0,
            "ef_prop": 5,
            "ef_terc": 12,
            "hh": 136,
            "eap": "1.1.5 (Montagem de Fôrmas Sapatas S1-S16) e 1.1.10 (Posicionamento Armaduras S1-S16)",
            "equip": "LOC-02 (Betoneira - 4h), LOC-05 (Gerador - 8h)",
            "fvs": "FVS-02-FUNDACOES (Armação e Fôrmas de Sapatas)",
            "fvs_status": "Aprovado c/ Ressalva (Ajustar espaçadores pastilha em S4 e S7)",
            "obs": "Carpinteiros posicionando fôrmas compensadas 17mm e armadores fixando as malhas de ferro CA-50 com espaçadores tipo pastilha para garantir cobrimento normativo de 40mm. Inspeção do Engenheiro liberou fôrmas após ajuste de pastilhas nas sapatas S4 e S7."
        },
        {
            "num": "005",
            "data": "26/09/2026",
            "dia": "Sábado (Meio Período)",
            "clima_m": "Sol",
            "clima_t": "Ensolarado",
            "temp": "23°C a 30°C",
            "cond": "Praticável",
            "h_paral": 0.0,
            "ef_prop": 3,
            "ef_terc": 8,
            "hh": 44,
            "eap": "1.1.3 (Concretagem 1ª Etapa Sapatas S1-S16 fck 30 MPa)",
            "equip": "Caminhão Betoneira Usinado + Bomba Lança, Vibrador de Imersão",
            "fvs": "FVS-03-ESTRUTURA_CONCRETO (Concretagem Fundação)",
            "fvs_status": "Aprovado (6 CPs moldados)",
            "obs": "Concretagem usinada de 18,5 m³ de concreto fck 30 MPa (NF 4821 - Usina Norte Fluminense). Slump test medido em 12 ± 2 cm. Moldados 6 corpos de prova para ensaios aos 7, 14 e 28 dias. Início imediato da cura úmida com aspersão de água e lona plástica."
        }
    ]

    for d in semana1_dados:
        conteudo = f"""# 📋 Relatório Diário de Obra — RDO-{d['num']}
**Obra:** {nome} ({sigla})  
**Data:** {d['data']} ({d['dia']})  
**Engenheiro Responsável:** Alexandre (CREA-RJ 2026-A) | **Mestre de Obras:** João da Silva

---

## ☀️ Condições Meteorológicas
* **Período Manhã:** {d['clima_m']} | **Período Tarde:** {d['clima_t']}
* **Temperatura:** {d['temp']} | **Condição:** {d['cond']}
* **Horas de Paralisação por Chuva/Clima:** {d['h_paral']} horas

---

## 👷 Efetivo Presente (Headcount)
* **Equipe de Gestão e Apoio Própria:** {d['ef_prop']} pessoas (Engenheiro, Mestre, TST, Almoxarife, Vigia)
* **Mão de Obra Terceirizada (SUB-01):** {d['ef_terc']} profissionais (Carpinteiros, Armadores e Serventes)
* **Total de Mão de Obra no Canteiro:** {d['ef_prop'] + d['ef_terc']} pessoas
* **Total de Horas-Homem (HH) Trabalhadas:** {d['hh']} HH

---

## 🚜 Equipamentos Operando
* {d['equip']}

---

## 🔨 Frentes de Serviço e Avanço EAP
* **Pacotes EAP Executados:** {d['eap']}
* **FVS Inspecionada:** {d['fvs']} — **Resultado:** {d['fvs_status']}

---

## 📝 Ocorrências e Diário de Bordo
{d['obs']}

---
*Assinado digitalmente via Ecossistema Antigravity PMO Virtual.*
"""
        caminho_rdo = os.path.join(rdos_dir, f"RDO_{d['num']}_{d['data'].replace('/', '-')}.md")
        with open(caminho_rdo, "w", encoding="utf-8") as f:
            f.write(conteudo)

    return semana1_dados


def construir_painel_excel_rdos(output_dir, config, semana1_dados):
    sigla = config.get("sigla_obra", "TMULT")
    nome = config.get("nome_obra", "TMULT — Edifício Administrativo")
    excel_path = os.path.join(output_dir, "PAINEL_RDOS_OBRA.xlsx")

    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # remove aba default

    # Paleta Corporativa
    NAVY = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    BLUE_DARK = PatternFill(start_color="284B78", end_color="284B78", fill_type="solid")
    HEADER_GRAY = PatternFill(start_color="EAEEF3", end_color="EAEEF3", fill_type="solid")
    ZEBRA_LIGHT = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
    GREEN_FILL = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
    YELLOW_FILL = PatternFill(start_color="FEF7E0", end_color="FEF7E0", fill_type="solid")
    
    FONT_TITLE = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
    FONT_SUBTITLE = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    FONT_TH = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    FONT_BOLD = Font(name="Calibri", size=9, bold=True, color="1B365D")
    FONT_REG = Font(name="Calibri", size=9, color="333333")
    FONT_GREEN = Font(name="Calibri", size=9, bold=True, color="137333")
    FONT_AMBER = Font(name="Calibri", size=9, bold=True, color="B06000")

    THIN_BORDER = Border(
        left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'), bottom=Side(style='thin', color='DDDDDD')
    )
    TOTAL_BORDER = Border(
        top=Side(style='thin', color='1B365D'), bottom=Side(style='double', color='1B365D'),
        left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD')
    )

    # -------------------------------------------------------------
    # ABA 1: PAINEL GERAL (DASHBOARD DIÁRIO)
    # -------------------------------------------------------------
    ws_dash = wb.create_sheet(title="Painel Geral de Produção")
    ws_dash.views.sheetView[0].showGridLines = True

    ws_dash.merge_cells("A1:H1")
    ws_dash["A1"] = f"PAINEL CONSOLIDADO DE PRODUÇÃO E RDOS — {nome.upper()}"
    ws_dash["A1"].font = FONT_TITLE
    ws_dash["A1"].fill = NAVY
    ws_dash["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.row_dimensions[1].height = 28

    ws_dash.merge_cells("A2:H2")
    ws_dash["A2"] = "Controle Contínuo de Diários de Obra, Mão de Obra, Clima, Equipamentos e FVS Bloqueantes"
    ws_dash["A2"].font = FONT_SUBTITLE
    ws_dash["A2"].fill = BLUE_DARK
    ws_dash["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.row_dimensions[2].height = 18

    # Cards KPI (Linha 4 e 5)
    cards = [
        ("B4", "C5", "TOTAL DIAS REGISTRADOS", "=COUNTA('Registro Diário RDO'!A6:A100)", "dias"),
        ("D4", "E5", "TOTAL HORAS-HOMEM (HH)", "=SUM('Registro Diário RDO'!I6:I100)", "HH"),
        ("F4", "G5", "HORAS DE PARALISAÇÃO", "=SUM('Registro Diário RDO'!F6:F100)", "horas")
    ]
    for c_top, c_bot, titulo, formula, unid in cards:
        ws_dash.merge_cells(f"{c_top}:{c_bot}")
        cell = ws_dash[c_top]
        cell.value = f"{titulo}\n"
        cell.font = FONT_BOLD
        cell.fill = HEADER_GRAY
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # Linha com fórmula abaixo do KPI
    ws_dash["B6"] = "Dias com RDO Emitido:"
    ws_dash["B6"].font = FONT_REG
    ws_dash["C6"] = "=COUNTA('Registro Diário RDO'!A6:A100)"
    ws_dash["C6"].font = FONT_BOLD

    ws_dash["D6"] = "Média de Efetivo / Dia:"
    ws_dash["D6"].font = FONT_REG
    ws_dash["E6"] = "=AVERAGE('Registro Diário RDO'!H6:H100)"
    ws_dash["E6"].font = FONT_BOLD
    ws_dash["E6"].number_format = "#,##0.0"

    ws_dash["F6"] = "Total Horas Paralisação:"
    ws_dash["F6"].font = FONT_REG
    ws_dash["G6"] = "=SUM('Registro Diário RDO'!F6:F100)"
    ws_dash["G6"].font = FONT_BOLD
    ws_dash["G6"].number_format = "#,##0.0"

    # Tabela Resumo das Semanas
    ws_dash.cell(row=9, column=2, value="SEMANA OPERACIONAL").fill = NAVY
    ws_dash.cell(row=9, column=2).font = FONT_TH
    ws_dash.cell(row=9, column=3, value="PERÍODO").fill = NAVY
    ws_dash.cell(row=9, column=3).font = FONT_TH
    ws_dash.cell(row=9, column=4, value="DIAS TRABALHADOS").fill = NAVY
    ws_dash.cell(row=9, column=4).font = FONT_TH
    ws_dash.cell(row=9, column=5, value="TOTAL HH").fill = NAVY
    ws_dash.cell(row=9, column=5).font = FONT_TH
    ws_dash.cell(row=9, column=6, value="STATUS CAMINHO CRÍTICO").fill = NAVY
    ws_dash.cell(row=9, column=6).font = FONT_TH
    ws_dash.cell(row=9, column=7, value="FVS LIBERADAS").fill = NAVY
    ws_dash.cell(row=9, column=7).font = FONT_TH

    semanas_resumo = [
        ("Semana S01 (Mobilização)", "22/09/2026 a 26/09/2026", 5, "=SUM('Registro Diário RDO'!I6:I10)", "No Prazo (Fundações Iniciadas)", "FVS-01 e FVS-02 Aprovadas"),
        ("Semana S02 (Fundações)", "29/09/2026 a 03/10/2026", "-", "-", "Aguardando Início", "Pendente"),
        ("Semana S03 (Baldrames)", "06/10/2026 a 10/10/2026", "-", "-", "Aguardando Início", "Pendente"),
        ("Semana S04 (Pilares P1-P24)", "13/10/2026 a 17/10/2026", "-", "-", "Aguardando Início", "Pendente"),
        ("Semana S05 (Laje H12 e Vigas)", "20/10/2026 a 24/10/2026", "-", "-", "Aguardando Início", "Pendente"),
        ("Semana S06 (Desforma e Cura)", "27/10/2026 a 31/10/2026", "-", "-", "Aguardando Início", "Pendente"),
    ]

    r_idx = 10
    for sem, per, dias, hh_f, status, fvs in semanas_resumo:
        ws_dash.cell(row=r_idx, column=2, value=sem).font = FONT_BOLD
        ws_dash.cell(row=r_idx, column=3, value=per).font = FONT_REG
        ws_dash.cell(row=r_idx, column=4, value=dias).font = FONT_REG
        ws_dash.cell(row=r_idx, column=4).alignment = Alignment(horizontal="center")
        c_hh = ws_dash.cell(row=r_idx, column=5, value=hh_f)
        c_hh.font = FONT_BOLD
        c_hh.alignment = Alignment(horizontal="right")
        if str(hh_f).startswith("="):
            c_hh.number_format = "#,##0"
            
        c_st = ws_dash.cell(row=r_idx, column=6, value=status)
        c_st.font = FONT_GREEN if "No Prazo" in status else FONT_REG
        
        ws_dash.cell(row=r_idx, column=7, value=fvs).font = FONT_REG
        
        for c in range(2, 8):
            ws_dash.cell(row=r_idx, column=c).border = THIN_BORDER
        r_idx += 1

    # -------------------------------------------------------------
    # ABA 2: REGISTRO DIÁRIO RDO
    # -------------------------------------------------------------
    ws_log = wb.create_sheet(title="Registro Diário RDO")
    ws_log.views.sheetView[0].showGridLines = True

    headers_log = [
        ("Nº RDO", 10),
        ("Data", 12),
        ("Dia Semana", 14),
        ("Clima Manhã", 14),
        ("Clima Tarde", 14),
        ("Horas Paralisadas", 16),
        ("Efetivo Próprio", 14),
        ("Efetivo Terceiro", 14),
        ("Total Efetivo", 14),
        ("Total HH", 12),
        ("Pacotes EAP Executados", 35),
        ("FVS Inspecionada", 25),
        ("Status FVS", 16),
        ("Ocorrências e Observações de Canteiro", 50)
    ]

    ws_log.merge_cells("A1:N1")
    ws_log["A1"] = f"DIÁRIO DE BORDO E REGISTRO DIÁRIO DE PRODUÇÃO (RDOS) — {sigla}"
    ws_log["A1"].font = FONT_TITLE
    ws_log["A1"].fill = NAVY
    ws_log["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_log.row_dimensions[1].height = 25

    for c_idx, (h_name, width) in enumerate(headers_log, start=1):
        cell = ws_log.cell(row=3, column=c_idx, value=h_name)
        cell.font = FONT_TH
        cell.fill = BLUE_DARK
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        ws_log.column_dimensions[get_column_letter(c_idx)].width = width
    ws_log.row_dimensions[3].height = 28

    # Preencher com os dados da Semana 1 piloto
    curr_row = 4
    for d in semana1_dados:
        ws_log.cell(row=curr_row, column=1, value=f"RDO-{d['num']}").alignment = Alignment(horizontal="center")
        ws_log.cell(row=curr_row, column=2, value=d['data']).alignment = Alignment(horizontal="center")
        ws_log.cell(row=curr_row, column=3, value=d['dia'])
        ws_log.cell(row=curr_row, column=4, value=d['clima_m'])
        ws_log.cell(row=curr_row, column=5, value=d['clima_t'])
        
        c_hparal = ws_log.cell(row=curr_row, column=6, value=d['h_paral'])
        c_hparal.alignment = Alignment(horizontal="right")
        c_hparal.number_format = "#,##0.0"
        
        c_efp = ws_log.cell(row=curr_row, column=7, value=d['ef_prop'])
        c_efp.alignment = Alignment(horizontal="right")
        
        c_eft = ws_log.cell(row=curr_row, column=8, value=d['ef_terc'])
        c_eft.alignment = Alignment(horizontal="right")
        
        # Fórmula: Total Efetivo = Efetivo Próprio + Terceiro
        c_tot = ws_log.cell(row=curr_row, column=9, value=f"=G{curr_row}+H{curr_row}")
        c_tot.font = FONT_BOLD
        c_tot.alignment = Alignment(horizontal="right")
        
        c_hh = ws_log.cell(row=curr_row, column=10, value=d['hh'])
        c_hh.font = FONT_BOLD
        c_hh.alignment = Alignment(horizontal="right")
        c_hh.number_format = "#,##0"
        
        ws_log.cell(row=curr_row, column=11, value=d['eap'])
        ws_log.cell(row=curr_row, column=12, value=d['fvs'])
        
        c_st = ws_log.cell(row=curr_row, column=13, value=d['fvs_status'])
        c_st.font = FONT_GREEN if "Aprovado" in d['fvs_status'] else FONT_AMBER
        c_st.fill = GREEN_FILL if "Aprovado" in d['fvs_status'] else YELLOW_FILL
        c_st.alignment = Alignment(horizontal="center")
        
        ws_log.cell(row=curr_row, column=14, value=d['obs'])

        for col in range(1, 15):
            cell = ws_log.cell(row=curr_row, column=col)
            cell.border = THIN_BORDER
            if curr_row % 2 == 1 and col != 13:
                cell.fill = ZEBRA_LIGHT
        curr_row += 1

    # Linha de Totais da Semana 1
    ws_log.cell(row=curr_row, column=1, value="TOTAL SEMANA 1").font = FONT_BOLD
    ws_log.cell(row=curr_row, column=6, value=f"=SUM(F4:F{curr_row-1})").font = FONT_BOLD
    ws_log.cell(row=curr_row, column=6).number_format = "#,##0.0"
    ws_log.cell(row=curr_row, column=7, value=f"=AVERAGE(G4:G{curr_row-1})").font = FONT_BOLD
    ws_log.cell(row=curr_row, column=7).number_format = "#,##0.0"
    ws_log.cell(row=curr_row, column=8, value=f"=AVERAGE(H4:H{curr_row-1})").font = FONT_BOLD
    ws_log.cell(row=curr_row, column=8).number_format = "#,##0.0"
    ws_log.cell(row=curr_row, column=9, value=f"=AVERAGE(I4:I{curr_row-1})").font = FONT_BOLD
    ws_log.cell(row=curr_row, column=9).number_format = "#,##0.0"
    ws_log.cell(row=curr_row, column=10, value=f"=SUM(J4:J{curr_row-1})").font = FONT_BOLD
    ws_log.cell(row=curr_row, column=10).number_format = "#,##0"
    for col in range(1, 15):
        ws_log.cell(row=curr_row, column=col).border = TOTAL_BORDER

    # Autoajuste de colunas na aba Dashboard
    for col in ws_dash.columns:
        col_letter = get_column_letter(col[0].column)
        ws_dash.column_dimensions[col_letter].width = 18

    wb.save(excel_path)
    return excel_path


def main():
    args = parse_args()
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    if args.dir:
        obra_dir = os.path.abspath(args.dir)
    else:
        obra_dir = os.path.join(workspace_root, "projetos", args.obra)

    if not os.path.exists(obra_dir):
        print(f"[ERRO] Pasta da obra não encontrada: {obra_dir}")
        sys.exit(1)

    print(f"\n=======================================================")
    print(f"🚀 MOTOR UNIVERSAL DE RDO E PRODUÇÃO DE CAMPO")
    print(f"=======================================================")
    print(f"📂 Diretório da Obra: {obra_dir}")

    config, contratos, locacoes = carregar_dados_obra(obra_dir)
    sigla = config.get("sigla_obra", "OBRA")
    print(f"🏗️  Obra Ativa: {config.get('nome_obra', sigla)} ({sigla})")

    output_dir = os.path.join(obra_dir, "04_PRODUCAO_E_AVANCO")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[1/3] Gerando Templates Executivos de RDO (Markdown e CSV)...")
    gerar_templates_rdo(output_dir, config)
    print(f"      ✅ TEMPLATE_RDO_EXECUTIVO.md gerado")
    print(f"      ✅ TEMPLATE_RDO_EXECUTIVO.csv gerado")

    print(f"\n[2/3] Gerando Lote Piloto da Semana 1 de Mobilização (RDO-001 a RDO-005)...")
    semana1 = gerar_rdos_piloto_semana1(output_dir, config)
    print(f"      ✅ 5 Diários de Obra gerados em 04_PRODUCAO_E_AVANCO/RDOS/")

    print(f"\n[3/3] Construindo Planilha Executiva PAINEL_RDOS_OBRA.xlsx...")
    excel_path = construir_painel_excel_rdos(output_dir, config, semana1)
    print(f"      ✅ Planilha Excel gerada com sucesso: {excel_path}")

    print(f"\n✨ Motor de RDO concluído com 100% de sucesso!")


if __name__ == "__main__":
    main()
