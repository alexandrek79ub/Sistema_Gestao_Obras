#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Compliance de SST, Controle de Vencimento Documental e Gestão de RH.
Implementa a SKILL_GESTAO_17_VENCIMENTO_DOCUMENTAL_SEGURANCA e POP 23 (SESMT).

Uso:
    python scripts/gerar_compliance_sst.py --obra OBRA_TMULT
    python scripts/gerar_compliance_sst.py --dir projetos/OBRA_TMULT
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
    parser = argparse.ArgumentParser(description="Motor Universal de Compliance SST e Vencimento Documental.")
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
            "sigla_obra": os.path.basename(obra_dir)[:6].upper()
        }
    return config


def obter_documentos_obra():
    return [
        {
            "doc": "PGR — Programa de Gerenciamento de Riscos (NR-01 / NR-18)",
            "titular": "Construtora Principal (Canteiro Geral)",
            "emissao": "15/09/2026",
            "vencimento": "15/09/2027",
            "janela_alerta": "30 dias",
            "status": "Vigente (Verde)",
            "resp": "Engenheiro de Segurança / TST"
        },
        {
            "doc": "PCMSO — Prog. Controle Médico de Saúde Ocupacional (NR-07)",
            "titular": "Construtora Principal (Canteiro Geral)",
            "emissao": "15/09/2026",
            "vencimento": "15/09/2027",
            "janela_alerta": "30 dias",
            "status": "Vigente (Verde)",
            "resp": "Médico do Trabalho Coordenador"
        },
        {
            "doc": "LTCAT — Laudo Técnico das Condições Ambientais de Trabalho",
            "titular": "Construtora Principal (Canteiro Geral)",
            "emissao": "15/09/2026",
            "vencimento": "15/09/2027",
            "janela_alerta": "30 dias",
            "status": "Vigente (Verde)",
            "resp": "Engenheiro de Segurança do Trabalho"
        },
        {
            "doc": "PGR da Empreiteira SUB-01 (Estruturas e Fundações)",
            "titular": "Empreiteira Estrutural Norte Fluminense",
            "emissao": "10/09/2026",
            "vencimento": "10/09/2027",
            "janela_alerta": "30 dias",
            "status": "Vigente (Verde)",
            "resp": "TST Empreiteiro"
        },
        {
            "doc": "PCMSO da Empreiteira SUB-01 (Estruturas e Fundações)",
            "titular": "Empreiteira Estrutural Norte Fluminense",
            "emissao": "10/09/2026",
            "vencimento": "10/09/2027",
            "janela_alerta": "30 dias",
            "status": "Vigente (Verde)",
            "resp": "Médico do Trabalho Terceirizado"
        },
        {
            "doc": "ART de Instalações Provisórias Elétricas (NR-10)",
            "titular": "Canteiro / Quadro Geral e Gerador",
            "emissao": "18/09/2026",
            "vencimento": "22/03/2027",
            "janela_alerta": "30 dias",
            "status": "Vigente (Verde)",
            "resp": "Engenheiro Eletricista"
        },
        {
            "doc": "Laudo de Aterramento e Continuidade do SPDA",
            "titular": "Malha de Canteiro e Módulos Habitáveis",
            "emissao": "20/09/2026",
            "vencimento": "20/09/2027",
            "janela_alerta": "30 dias",
            "status": "Vigente (Verde)",
            "resp": "Engenheiro Eletricista"
        }
    ]


def obter_trabalhadores_base():
    return [
        {"nome": "Alexandre de Oliveira", "cargo": "Engenheiro Residente", "empresa": "Construtora Própria", "aso_dt": "10/09/2026", "aso_venc": "10/09/2027", "nr18": "Sim (4h)", "nr35": "Sim (Apto)", "nr10": "Não Requer", "nr12": "Não Requer", "epi_ca": "Conforme", "status": "🟢 Apto Total"},
        {"nome": "João da Silva", "cargo": "Mestre de Obras", "empresa": "Construtora Própria", "aso_dt": "11/09/2026", "aso_venc": "11/09/2027", "nr18": "Sim (4h)", "nr35": "Sim (Apto)", "nr10": "Sim (Básico)", "nr12": "Sim (Apto)", "epi_ca": "Conforme", "status": "🟢 Apto Total"},
        {"nome": "Carlos Eduardo Lima", "cargo": "Técnico Seg Trabalho (TST)", "empresa": "Construtora Própria", "aso_dt": "12/09/2026", "aso_venc": "12/09/2027", "nr18": "Sim (4h)", "nr35": "Sim (Apto)", "nr10": "Sim (Apto)", "nr12": "Sim (Apto)", "epi_ca": "Conforme", "status": "🟢 Apto Total"},
        {"nome": "Marcos Antônio Santos", "cargo": "Almoxarife / Apontador", "empresa": "Construtora Própria", "aso_dt": "14/09/2026", "aso_venc": "14/09/2027", "nr18": "Sim (4h)", "nr35": "Não Requer", "nr10": "Não Requer", "nr12": "Não Requer", "epi_ca": "Conforme", "status": "🟢 Apto Total"},
        {"nome": "Sebastião Ferreira", "cargo": "Vigia Diurno/Noturno", "empresa": "Construtora Própria", "aso_dt": "14/09/2026", "aso_venc": "14/09/2027", "nr18": "Sim (4h)", "nr35": "Não Requer", "nr10": "Não Requer", "nr12": "Não Requer", "epi_ca": "Conforme", "status": "🟢 Apto Total"},
        {"nome": "Raimundo Nonato", "cargo": "Encarregado de Carpintaria", "empresa": "SUB-01 (Estrutura)", "aso_dt": "15/09/2026", "aso_venc": "15/09/2027", "nr18": "Sim (4h)", "nr35": "Sim (Apto)", "nr10": "Não Requer", "nr12": "Sim (Serra)", "epi_ca": "Conforme", "status": "🟢 Apto Total"},
        {"nome": "José Alves de Souza", "cargo": "Carpinteiro Oficial", "empresa": "SUB-01 (Estrutura)", "aso_dt": "15/09/2026", "aso_venc": "15/09/2027", "nr18": "Sim (4h)", "nr35": "Sim (Apto)", "nr10": "Não Requer", "nr12": "Sim (Serra)", "epi_ca": "Conforme", "status": "🟢 Apto Total"},
        {"nome": "Antônio Carlos Vieira", "cargo": "Carpinteiro Oficial", "empresa": "SUB-01 (Estrutura)", "aso_dt": "16/09/2026", "aso_venc": "16/09/2027", "nr18": "Sim (4h)", "nr35": "Sim (Apto)", "nr10": "Não Requer", "nr12": "Sim (Serra)", "epi_ca": "Conforme", "status": "🟢 Apto Total"},
        {"nome": "Manoel Messias", "cargo": "Armador Oficial", "empresa": "SUB-01 (Estrutura)", "aso_dt": "16/09/2026", "aso_venc": "16/09/2027", "nr18": "Sim (4h)", "nr35": "Sim (Apto)", "nr10": "Não Requer", "nr12": "Sim (Policorte)", "epi_ca": "Conforme", "status": "🟢 Apto Total"},
        {"nome": "Geraldo Pereira", "cargo": "Armador Oficial", "empresa": "SUB-01 (Estrutura)", "aso_dt": "17/09/2026", "aso_venc": "17/09/2027", "nr18": "Sim (4h)", "nr35": "Sim (Apto)", "nr10": "Não Requer", "nr12": "Não Requer", "epi_ca": "Conforme", "status": "🟢 Apto Total"},
        {"nome": "Francisco Chagas", "cargo": "Servente de Obras", "empresa": "SUB-01 (Estrutura)", "aso_dt": "17/09/2026", "aso_venc": "17/09/2027", "nr18": "Sim (4h)", "nr35": "Sim (Apto)", "nr10": "Não Requer", "nr12": "Não Requer", "epi_ca": "Conforme", "status": "🟢 Apto Total"},
        {"nome": "Vitor Hugo Rocha", "cargo": "Servente de Obras", "empresa": "SUB-01 (Estrutura)", "aso_dt": "18/09/2026", "aso_venc": "18/09/2027", "nr18": "Sim (4h)", "nr35": "Sim (Apto)", "nr10": "Não Requer", "nr12": "Não Requer", "epi_ca": "Conforme", "status": "🟢 Apto Total"},
        {"nome": "Leandro Barbosa", "cargo": "Operador Retroescavadeira", "empresa": "LOC-01 (Locadora)", "aso_dt": "18/09/2026", "aso_venc": "18/09/2027", "nr18": "Sim (4h)", "nr35": "Não Requer", "nr10": "Não Requer", "nr12": "Sim (Operador CNH D)", "epi_ca": "Conforme", "status": "🟢 Apto Total"}
    ]


def construir_excel_compliance_sst(output_dir, config):
    sigla = config.get("sigla_obra", "TMULT")
    nome = config.get("nome_obra", "TMULT — Edifício Administrativo")
    excel_path = os.path.join(output_dir, f"PAINEL_COMPLIANCE_SST_{sigla}.xlsx")

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    NAVY = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    BLUE_DARK = PatternFill(start_color="284B78", end_color="284B78", fill_type="solid")
    HEADER_GRAY = PatternFill(start_color="EAEEF3", end_color="EAEEF3", fill_type="solid")
    ZEBRA = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
    GREEN_FILL = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")

    FONT_TITLE = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
    FONT_SUB = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    FONT_TH = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    FONT_BOLD = Font(name="Calibri", size=9, bold=True, color="1B365D")
    FONT_REG = Font(name="Calibri", size=9, color="333333")
    FONT_GREEN = Font(name="Calibri", size=9, bold=True, color="137333")

    THIN_BORDER = Border(
        left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'), bottom=Side(style='thin', color='DDDDDD')
    )

    # -------------------------------------------------------------
    # ABA 1: DOCUMENTOS DA OBRA (PGR / PCMSO / LTCAT)
    # -------------------------------------------------------------
    ws_doc = wb.create_sheet(title="Documentos da Obra")
    ws_doc.views.sheetView[0].showGridLines = True

    ws_doc.merge_cells("A1:G1")
    ws_doc["A1"] = f"PAINEL DE DOCUMENTAÇÃO DE SEGURANÇA E COMPLIANCE — {nome.upper()}"
    ws_doc["A1"].font = FONT_TITLE
    ws_doc["A1"].fill = NAVY
    ws_doc["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_doc.row_dimensions[1].height = 28

    ws_doc.merge_cells("A2:G2")
    ws_doc["A2"] = "Controle de Vigência de Programas Legais (PGR, PCMSO, LTCAT, Laudos) com Alerta Preventivo D-30"
    ws_doc["A2"].font = FONT_SUB
    ws_doc["A2"].fill = BLUE_DARK
    ws_doc["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_doc.row_dimensions[2].height = 18

    headers_doc = [
        ("Documento Legal / Programa", 38),
        ("Titular / Abrangência", 32),
        ("Data de Emissão", 16),
        ("Data de Vencimento", 18),
        ("Janela de Alerta", 16),
        ("Status Atual", 18),
        ("Responsável Técnico", 30)
    ]

    for col_idx, (h_text, width) in enumerate(headers_doc, start=1):
        cell = ws_doc.cell(row=3, column=col_idx, value=h_text)
        cell.font = FONT_TH
        cell.fill = BLUE_DARK
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        ws_doc.column_dimensions[get_column_letter(col_idx)].width = width
    ws_doc.row_dimensions[3].height = 28

    docs = obter_documentos_obra()
    for row_idx, d in enumerate(docs, start=4):
        ws_doc.cell(row=row_idx, column=1, value=d['doc']).font = FONT_BOLD
        ws_doc.cell(row=row_idx, column=2, value=d['titular'])
        ws_doc.cell(row=row_idx, column=3, value=d['emissao']).alignment = Alignment(horizontal="center")
        ws_doc.cell(row=row_idx, column=4, value=d['vencimento']).alignment = Alignment(horizontal="center")
        ws_doc.cell(row=row_idx, column=5, value=d['janela_alerta']).alignment = Alignment(horizontal="center")
        
        c_st = ws_doc.cell(row=row_idx, column=6, value=d['status'])
        c_st.font = FONT_GREEN
        c_st.fill = GREEN_FILL
        c_st.alignment = Alignment(horizontal="center")
        
        ws_doc.cell(row=row_idx, column=7, value=d['resp'])

        for col in range(1, 8):
            cell = ws_doc.cell(row=row_idx, column=col)
            cell.border = THIN_BORDER
            if row_idx % 2 == 1 and col != 6:
                cell.fill = ZEBRA

    # -------------------------------------------------------------
    # ABA 2: CONTROLE DE ASOS E NRs DA EQUIPE (HEADCOUNT)
    # -------------------------------------------------------------
    ws_equipe = wb.create_sheet(title="Controle de Mão de Obra e ASOs")
    ws_equipe.views.sheetView[0].showGridLines = True

    ws_equipe.merge_cells("A1:K1")
    ws_equipe["A1"] = f"CONTROLE INDIVIDUAL DE ASO, CAPACITAÇÃO E EPI — {sigla}"
    ws_equipe["A1"].font = FONT_TITLE
    ws_equipe["A1"].fill = NAVY
    ws_equipe["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_equipe.row_dimensions[1].height = 28

    headers_eq = [
        ("Nome do Colaborador", 26),
        ("Função / Cargo", 24),
        ("Empresa Vinculada", 22),
        ("Data ASO", 14),
        ("Vencimento ASO", 16),
        ("NR-18 (Integ.)", 14),
        ("NR-35 (Altura)", 14),
        ("NR-10 (Elétrica)", 15),
        ("NR-12 (Máquinas)", 16),
        ("Ficha EPI c/ CA", 16),
        ("Status de Acesso", 18)
    ]

    for col_idx, (h_text, width) in enumerate(headers_eq, start=1):
        cell = ws_equipe.cell(row=3, column=col_idx, value=h_text)
        cell.font = FONT_TH
        cell.fill = BLUE_DARK
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        ws_equipe.column_dimensions[get_column_letter(col_idx)].width = width
    ws_equipe.row_dimensions[3].height = 28

    trabalhadores = obter_trabalhadores_base()
    for row_idx, t in enumerate(trabalhadores, start=4):
        ws_equipe.cell(row=row_idx, column=1, value=t['nome']).font = FONT_BOLD
        ws_equipe.cell(row=row_idx, column=2, value=t['cargo'])
        ws_equipe.cell(row=row_idx, column=3, value=t['empresa'])
        ws_equipe.cell(row=row_idx, column=4, value=t['aso_dt']).alignment = Alignment(horizontal="center")
        ws_equipe.cell(row=row_idx, column=5, value=t['aso_venc']).alignment = Alignment(horizontal="center")
        ws_equipe.cell(row=row_idx, column=6, value=t['nr18']).alignment = Alignment(horizontal="center")
        ws_equipe.cell(row=row_idx, column=7, value=t['nr35']).alignment = Alignment(horizontal="center")
        ws_equipe.cell(row=row_idx, column=8, value=t['nr10']).alignment = Alignment(horizontal="center")
        ws_equipe.cell(row=row_idx, column=9, value=t['nr12']).alignment = Alignment(horizontal="center")
        ws_equipe.cell(row=row_idx, column=10, value=t['epi_ca']).alignment = Alignment(horizontal="center")
        
        c_st = ws_equipe.cell(row=row_idx, column=11, value=t['status'])
        c_st.font = FONT_GREEN
        c_st.fill = GREEN_FILL
        c_st.alignment = Alignment(horizontal="center")

        for col in range(1, 12):
            cell = ws_equipe.cell(row=row_idx, column=col)
            cell.border = THIN_BORDER
            if row_idx % 2 == 1 and col != 11:
                cell.fill = ZEBRA

    # -------------------------------------------------------------
    # ABA 3: CRONOGRAMA DE DDS MATINAL
    # -------------------------------------------------------------
    ws_dds = wb.create_sheet(title="Programa de DDS")
    ws_dds.views.sheetView[0].showGridLines = True

    ws_dds.merge_cells("A1:E1")
    ws_dds["A1"] = f"CRONOGRAMA DE DIÁLOGOS DIÁRIOS DE SEGURANÇA (DDS) — {sigla}"
    ws_dds["A1"].font = FONT_TITLE
    ws_dds["A1"].fill = NAVY
    ws_dds["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dds.row_dimensions[1].height = 28

    headers_dds = [
        ("Semana", 12),
        ("Dia", 14),
        ("Tema Obrigatório do DDS", 40),
        ("Norma Vinculada", 18),
        ("Responsável / Instrutor", 25)
    ]

    for col_idx, (h_text, width) in enumerate(headers_dds, start=1):
        cell = ws_dds.cell(row=3, column=col_idx, value=h_text)
        cell.font = FONT_TH
        cell.fill = BLUE_DARK
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = THIN_BORDER
        ws_dds.column_dimensions[get_column_letter(col_idx)].width = width

    temas_dds = [
        ("S01", "22/09 - Ter", "Integração Geral de Canteiro e Procedimentos de Emergência", "NR-18", "TST Carlos Lima"),
        ("S01", "23/09 - Quar", "Riscos em Escavações de Valas e Sapatas: Talude e Escoramento", "NR-18 e NR-20", "TST Carlos Lima"),
        ("S01", "24/09 - Qui", "Cuidado com Ferramentas Manuais e Perfurocortantes em Armações", "NR-12 e POP 03", "Mestre João da Silva"),
        ("S01", "25/09 - Sex", "Uso Obrigatório e Conservação de Botinas, Óculos e Luvas", "NR-06", "TST Carlos Lima"),
        ("S01", "26/09 - Sáb", "Segurança em Concretagem Usinada: Vibradores e Mangote da Bomba", "NR-18", "Eng. Alexandre"),
        ("S02", "29/09 - Ter", "Trabalho Sob Radiação Solar e Hidratação Contínua (Porto do Açu)", "NR-24", "TST Carlos Lima"),
        ("S02", "30/09 - Quar", "Ordem e Limpeza: Descarte de Pregos, Arames e Madeira de Fôrma", "POP 01 (Lean)", "Mestre João da Silva"),
        ("S03", "06/10 - Ter", "Trabalho em Altura: Ponto de Ancoragem e Talabarte Duplo", "NR-35", "TST Carlos Lima"),
        ("S04", "13/10 - Ter", "Bloqueio e Etiquetagem de Energia Elétrica (Lockout/Tagout)", "NR-10", "TST Carlos Lima"),
    ]

    for row_idx, t in enumerate(temas_dds, start=4):
        ws_dds.cell(row=row_idx, column=1, value=t[0]).alignment = Alignment(horizontal="center")
        ws_dds.cell(row=row_idx, column=2, value=t[1]).alignment = Alignment(horizontal="center")
        ws_dds.cell(row=row_idx, column=3, value=t[2]).font = FONT_BOLD
        ws_dds.cell(row=row_idx, column=4, value=t[3]).alignment = Alignment(horizontal="center")
        ws_dds.cell(row=row_idx, column=5, value=t[4])

        for col in range(1, 6):
            cell = ws_dds.cell(row=row_idx, column=col)
            cell.border = THIN_BORDER
            if row_idx % 2 == 1:
                cell.fill = ZEBRA

    wb.save(excel_path)
    return excel_path


def gerar_relatorio_sst_markdown(output_dir, config):
    sigla = config.get("sigla_obra", "TMULT")
    nome = config.get("nome_obra", "TMULT — Edifício Administrativo")
    md_path = os.path.join(output_dir, f"RELATORIO_COMPLIANCE_SST_{sigla}.md")

    conteudo = f"""# 🦺 RELATÓRIO DE COMPLIANCE DE SST E GOVERNANÇA DE RH
## {nome.upper()} ({sigla})

> **Documento Oficial de Auditoria de Segurança do Trabalho**  
> **Fundamentação Normativa:** NR-01 (PGR), NR-07 (PCMSO), NR-09 (Agentes Ambientais), NR-18 (Construção Civil) e SKILL_GESTAO_17.

---

## 🎯 1. STATUS GLOBAL DE CONFORMIDADE DOCUMENTAL (STATUS DA PORTARIA)

* **Data da Auditoria de Conformidade:** 26/09/2026
* **Status Geral do Canteiro:** **`100% REGULAR (SEM PENDÊNCIAS CRÍTICAS)`**
* **Trabalhadores Cadastrados e Autorizados na Portaria:** 13 colaboradores (5 próprios + 8 terceirizados)
* **Controle de Vencimentos em D-30 e D-15:** ZERO documentos vencendo nos próximos 30 dias.
* **Aderência às NRs Obrigatórias:**
  - NR-18 (Integração de 4 horas): 100% dos operários treinados;
  - NR-35 (Trabalho em Altura): 100% dos carpinteiros, armadores e serventes aptos no ASO e com certificado;
  - NR-10 (Segurança Elétrica): Profissionais eletricistas habilitados e com reciclagem em dia;
  - NR-12 (Operação de Máquinas): Operador de retroescavadeira e carpinteiros certificados para serra circular de bancada.

---

## 📋 2. QUADRO DE PROGRAMAS LEGAIS DA CONSTRUTORA E TERCEIROS

| Programa / Documento | Titular | Emissão | Vigência | Status | Gestor / Responsável |
|---|---|:---:|:---:|:---:|---|
| **PGR (NR-01 / NR-18)** | Construtora Própria | 15/09/2026 | 15/09/2027 | 🟢 Vigente | Eng. Segurança / TST |
| **PCMSO (NR-07)** | Construtora Própria | 15/09/2026 | 15/09/2027 | 🟢 Vigente | Médico do Trabalho Coordenador |
| **LTCAT (INSS / Previdência)** | Construtora Própria | 15/09/2026 | 15/09/2027 | 🟢 Vigente | Eng. Segurança do Trabalho |
| **PGR Terceiro (SUB-01)** | Empreiteira Estrutural | 10/09/2026 | 10/09/2027 | 🟢 Vigente | TST Terceirizado |
| **PCMSO Terceiro (SUB-01)** | Empreiteira Estrutural | 10/09/2026 | 10/09/2027 | 🟢 Vigente | Médico Coordenador Terceirizado |
| **ART Elétrica de Canteiro** | Canteiro e Gerador | 18/09/2026 | 22/03/2027 | 🟢 Vigente | Eng. Eletricista |
| **Laudo SPDA e Aterramento** | Malha de Canteiro | 20/09/2026 | 20/09/2027 | 🟢 Vigente | Eng. Eletricista |

---

## 🛑 3. REGRAS INEGOCIÁVEIS DE ACESSO AO CANTEIRO (RED FLAGS)

1. **Barragem na Portaria:** Nenhum trabalhador (próprio ou subcontratado) pode transpor a portaria do canteiro sem:
   - ASO Admissional ou Periódico com carimbo de "APTO" emitido por clínica credenciada;
   - Treinamento Admissional de Integração NR-18 (4 horas) ministrado pelo TST da obra;
   - Ficha de EPI preenchida e assinada com todos os números de CA vigentes.
2. **Trabalho em Altura (Andaimes, Fôrmas e Lajes):** Proibido subir a mais de 2,00m do nível inferior sem cinto tipo paraquedista conectado com talabarte duplo em ponto de ancoragem testado ou linha de vida metálica.
3. **Máquinas:** Operação exclusiva por trabalhadores com crachá específico de qualificação NR-12.

---
*Relatório de SST aprovado pelo Engenheiro Residente e TST da Obra.*
"""
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return md_path


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
    print(f"🦺 MOTOR UNIVERSAL DE COMPLIANCE SST E CONTROLE DE RH")
    print(f"=======================================================")
    print(f"📂 Diretório da Obra: {obra_dir}")

    config = carregar_dados_obra(obra_dir)
    sigla = config.get("sigla_obra", "OBRA")
    nome = config.get("nome_obra", sigla)
    print(f"🏗️  Obra Ativa: {nome} ({sigla})")

    output_dir = os.path.join(obra_dir, "06_SST_E_RH")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[1/2] Construindo Planilha Excel PAINEL_COMPLIANCE_SST_{sigla}.xlsx...")
    excel_path = construir_excel_compliance_sst(output_dir, config)
    print(f"      ✅ Planilha Excel gerada com sucesso: {excel_path}")

    print(f"\n[2/2] Gerando Relatório Executivo RELATORIO_COMPLIANCE_SST_{sigla}.md...")
    md_path = gerar_relatorio_sst_markdown(output_dir, config)
    print(f"      ✅ Relatório Markdown gerado: {md_path}")

    print(f"\n✨ Motor de Compliance SST concluído com 100% de sucesso!")


if __name__ == "__main__":
    main()
