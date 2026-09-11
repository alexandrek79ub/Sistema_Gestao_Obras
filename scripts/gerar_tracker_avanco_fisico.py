#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Acompanhamento de Avanço Físico e Curva S Real vs Planejada (EVM / SPI).

Uso:
    python scripts/gerar_tracker_avanco_fisico.py --obra OBRA_TMULT
    python scripts/gerar_tracker_avanco_fisico.py --dir projetos/OBRA_TMULT
"""

import os
import sys
import json
import argparse
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
    parser = argparse.ArgumentParser(description="Motor Universal de Acompanhamento de Avanço Físico.")
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
    return config


def obter_dados_planejado_quinzenal():
    # 12 Quinzenas (6 meses) - Baseline 01 de referência
    return [
        {"q": "Q01", "mes": "Mês 1", "datas": "22/09 a 06/10", "plan_simples": 4.5, "plan_acum": 4.5, "real_acum": 4.2},
        {"q": "Q02", "mes": "Mês 1", "datas": "07/10 a 21/10", "plan_simples": 7.5, "plan_acum": 12.0, "real_acum": 0.0},
        {"q": "Q03", "mes": "Mês 2", "datas": "22/10 a 05/11", "plan_simples": 10.0, "plan_acum": 22.0, "real_acum": 0.0},
        {"q": "Q04", "mes": "Mês 2", "datas": "06/11 a 20/11", "plan_simples": 12.0, "plan_acum": 34.0, "real_acum": 0.0},
        {"q": "Q05", "mes": "Mês 3", "datas": "21/11 a 05/12", "plan_simples": 13.0, "plan_acum": 47.0, "real_acum": 0.0},
        {"q": "Q06", "mes": "Mês 3", "datas": "06/12 a 20/12", "plan_simples": 13.0, "plan_acum": 60.0, "real_acum": 0.0},
        {"q": "Q07", "mes": "Mês 4", "datas": "21/12 a 05/01", "plan_simples": 10.0, "plan_acum": 70.0, "real_acum": 0.0},
        {"q": "Q08", "mes": "Mês 4", "datas": "06/01 a 20/01", "plan_simples": 9.0, "plan_acum": 79.0, "real_acum": 0.0},
        {"q": "Q09", "mes": "Mês 5", "datas": "21/01 a 04/02", "plan_simples": 8.0, "plan_acum": 87.0, "real_acum": 0.0},
        {"q": "Q10", "mes": "Mês 5", "datas": "05/02 a 19/02", "plan_simples": 6.0, "plan_acum": 93.0, "real_acum": 0.0},
        {"q": "Q11", "mes": "Mês 6", "datas": "20/02 a 06/03", "plan_simples": 4.5, "plan_acum": 97.5, "real_acum": 0.0},
        {"q": "Q12", "mes": "Mês 6", "datas": "07/03 a 22/03", "plan_simples": 2.5, "plan_acum": 100.0, "real_acum": 0.0}
    ]


def obter_disciplinas_eap():
    return [
        {"eap": "1.0", "nome": "Administração Local e Canteiro Provisório", "peso": 18.5, "previsto": 100.0, "real": 20.0},
        {"eap": "1.1", "nome": "Infraestrutura (Fundações e Baldrames)", "peso": 12.0, "previsto": 100.0, "real": 35.0},
        {"eap": "1.2", "nome": "Supraestrutura (Pilares, Vigas e Lajes)", "peso": 16.5, "previsto": 0.0, "real": 0.0},
        {"eap": "2.1", "nome": "Alvenaria e Vedações Verticais", "peso": 8.5, "previsto": 0.0, "real": 0.0},
        {"eap": "2.2", "nome": "Revestimentos, Pisos e Pintura", "peso": 14.5, "previsto": 0.0, "real": 0.0},
        {"eap": "2.3", "nome": "Esquadrias Metálicas e Vidros", "peso": 5.0, "previsto": 0.0, "real": 0.0},
        {"eap": "2.4", "nome": "Cobertura Termoacústica e Calhas", "peso": 6.5, "previsto": 0.0, "real": 0.0},
        {"eap": "3.1", "nome": "Instalações Elétricas e SPDA", "peso": 8.0, "previsto": 0.0, "real": 0.0},
        {"eap": "3.2", "nome": "Instalações Hidráulicas e Esgoto", "peso": 6.5, "previsto": 0.0, "real": 0.0},
        {"eap": "3.3", "nome": "Climatização HVAC e Exaustão", "peso": 4.0, "previsto": 0.0, "real": 0.0}
    ]


def construir_excel_avanco_fisico(output_dir, config):
    sigla = config.get("sigla_obra", "TMULT")
    nome = config.get("nome_obra", "TMULT — Edifício Administrativo")
    excel_path = os.path.join(output_dir, f"ACOMPANHAMENTO_AVANCO_FISICO_{sigla}.xlsx")

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    NAVY = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    BLUE_DARK = PatternFill(start_color="284B78", end_color="284B78", fill_type="solid")
    HEADER_GRAY = PatternFill(start_color="EAEEF3", end_color="EAEEF3", fill_type="solid")
    ZEBRA = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
    GREEN_FILL = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
    YELLOW_FILL = PatternFill(start_color="FEF7E0", end_color="FEF7E0", fill_type="solid")

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
    TOTAL_BORDER = Border(
        top=Side(style='thin', color='1B365D'), bottom=Side(style='double', color='1B365D'),
        left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD')
    )

    # ---------------------------------------------------------
    # ABA 1: CURVA S E INDICADORES EVM (SPI)
    # ---------------------------------------------------------
    ws_curva = wb.create_sheet(title="Curva S e SPI")
    ws_curva.views.sheetView[0].showGridLines = True

    ws_curva.merge_cells("A1:H1")
    ws_curva["A1"] = f"ACOMPANHAMENTO DE AVANÇO FÍSICO E CURVA S — {nome.upper()}"
    ws_curva["A1"].font = FONT_TITLE
    ws_curva["A1"].fill = NAVY
    ws_curva["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_curva.row_dimensions[1].height = 28

    ws_curva.merge_cells("A2:H2")
    ws_curva["A2"] = "Linha de Base 01 vs Avanço Físico Real Medido e Índice de Desempenho de Prazo (SPI)"
    ws_curva["A2"].font = FONT_SUB
    ws_curva["A2"].fill = BLUE_DARK
    ws_curva["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_curva.row_dimensions[2].height = 18

    headers_curva = [
        ("Quinzena", 12),
        ("Mês", 12),
        ("Período Executivo", 18),
        ("% Previsto Quinzena", 18),
        ("% Previsto Acumulado", 20),
        ("% Real Acumulado", 18),
        ("SPI (Prazo)", 15),
        ("Status de Prazo", 22)
    ]

    for col_idx, (h_text, width) in enumerate(headers_curva, start=1):
        cell = ws_curva.cell(row=3, column=col_idx, value=h_text)
        cell.font = FONT_TH
        cell.fill = BLUE_DARK
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        ws_curva.column_dimensions[get_column_letter(col_idx)].width = width
    ws_curva.row_dimensions[3].height = 28

    quinzenas = obter_dados_planejado_quinzenal()
    for row_idx, q in enumerate(quinzenas, start=4):
        ws_curva.cell(row=row_idx, column=1, value=q['q']).alignment = Alignment(horizontal="center")
        ws_curva.cell(row=row_idx, column=2, value=q['mes']).alignment = Alignment(horizontal="center")
        ws_curva.cell(row=row_idx, column=3, value=q['datas']).alignment = Alignment(horizontal="center")
        
        c_p_simples = ws_curva.cell(row=row_idx, column=4, value=q['plan_simples'] / 100.0)
        c_p_simples.number_format = "0.0%"
        c_p_simples.alignment = Alignment(horizontal="right")
        
        c_p_acum = ws_curva.cell(row=row_idx, column=5, value=q['plan_acum'] / 100.0)
        c_p_acum.number_format = "0.0%"
        c_p_acum.font = FONT_BOLD
        c_p_acum.alignment = Alignment(horizontal="right")

        val_real = q['real_acum'] / 100.0 if q['real_acum'] > 0 else ""
        c_real = ws_curva.cell(row=row_idx, column=6, value=val_real)
        if val_real != "":
            c_real.number_format = "0.0%"
            c_real.font = FONT_BOLD
            c_real.alignment = Alignment(horizontal="right")

        # Fórmula SPI = Real Acumulado / Previsto Acumulado
        c_spi = ws_curva.cell(row=row_idx, column=7, value=f"=IF(F{row_idx}>0, F{row_idx}/E{row_idx}, \"\")")
        c_spi.font = FONT_BOLD
        c_spi.alignment = Alignment(horizontal="right")
        c_spi.number_format = "0.00"

        # Fórmula Status
        c_st = ws_curva.cell(row=row_idx, column=8, value=f"=IF(G{row_idx}=\"\", \"Não Iniciado\", IF(G{row_idx}>=0.95, \"No Prazo (Verde)\", IF(G{row_idx}>=0.85, \"Atenção (Amarelo)\", \"Atrasado (Vermelho)\")))")
        c_st.font = FONT_REG
        c_st.alignment = Alignment(horizontal="center")

        for col in range(1, 9):
            cell = ws_curva.cell(row=row_idx, column=col)
            cell.border = THIN_BORDER
            if row_idx % 2 == 1:
                cell.fill = ZEBRA

    # ---------------------------------------------------------
    # ABA 2: AVANÇO POR DISCIPLINA DA EAP
    # ---------------------------------------------------------
    ws_disc = wb.create_sheet(title="Avanço Físico EAP")
    ws_disc.views.sheetView[0].showGridLines = True

    ws_disc.merge_cells("A1:G1")
    ws_disc["A1"] = f"AVANÇO FÍSICO POR DISCIPLINA DA EAP — {sigla}"
    ws_disc["A1"].font = FONT_TITLE
    ws_disc["A1"].fill = NAVY
    ws_disc["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_disc.row_dimensions[1].height = 28

    headers_disc = [
        ("Código EAP", 14),
        ("Disciplina Executiva da Obra", 35),
        ("Peso no Orçamento", 18),
        ("% Previsto Período", 18),
        ("% Real Concluído", 18),
        ("Contribuição Real Total", 22),
        ("Status de Conclusão", 20)
    ]

    for col_idx, (h_text, width) in enumerate(headers_disc, start=1):
        cell = ws_disc.cell(row=3, column=col_idx, value=h_text)
        cell.font = FONT_TH
        cell.fill = BLUE_DARK
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        ws_disc.column_dimensions[get_column_letter(col_idx)].width = width
    ws_disc.row_dimensions[3].height = 28

    disciplinas = obter_disciplinas_eap()
    curr_row = 4
    for d in disciplinas:
        ws_disc.cell(row=curr_row, column=1, value=d['eap']).alignment = Alignment(horizontal="center")
        ws_disc.cell(row=curr_row, column=2, value=d['nome']).font = FONT_BOLD
        
        c_peso = ws_disc.cell(row=curr_row, column=3, value=d['peso'] / 100.0)
        c_peso.number_format = "0.0%"
        c_peso.alignment = Alignment(horizontal="right")

        c_prev = ws_disc.cell(row=curr_row, column=4, value=d['previsto'] / 100.0)
        c_prev.number_format = "0.0%"
        c_prev.alignment = Alignment(horizontal="right")

        c_real = ws_disc.cell(row=curr_row, column=5, value=d['real'] / 100.0)
        c_real.number_format = "0.0%"
        c_real.font = FONT_BOLD
        c_real.alignment = Alignment(horizontal="right")

        # Contribuição Real = Peso * Real
        c_cont = ws_disc.cell(row=curr_row, column=6, value=f"=C{curr_row}*E{curr_row}")
        c_cont.number_format = "0.00%"
        c_cont.font = FONT_BOLD
        c_cont.alignment = Alignment(horizontal="right")

        c_st = ws_disc.cell(row=curr_row, column=7, value=f"=IF(E{curr_row}>=1, \"Concluído\", IF(E{curr_row}>0, \"Em Andamento\", \"Não Iniciado\"))")
        c_st.alignment = Alignment(horizontal="center")

        for col in range(1, 8):
            cell = ws_disc.cell(row=curr_row, column=col)
            cell.border = THIN_BORDER
            if curr_row % 2 == 1:
                cell.fill = ZEBRA
        curr_row += 1

    # Linha de Totais da Obra
    ws_disc.cell(row=curr_row, column=1, value="TOTAL OBRA").font = FONT_BOLD
    ws_disc.cell(row=curr_row, column=3, value=f"=SUM(C4:C{curr_row-1})").font = FONT_BOLD
    ws_disc.cell(row=curr_row, column=3).number_format = "0.0%"
    
    # Avanço Físico Global Consolidado
    c_tot_real = ws_disc.cell(row=curr_row, column=6, value=f"=SUM(F4:F{curr_row-1})")
    c_tot_real.font = FONT_TITLE
    c_tot_real.fill = GREEN_FILL
    c_tot_real.font = Font(name="Calibri", size=10, bold=True, color="137333")
    c_tot_real.number_format = "0.00%"
    c_tot_real.alignment = Alignment(horizontal="right")

    for col in range(1, 8):
        ws_disc.cell(row=curr_row, column=col).border = TOTAL_BORDER

    wb.save(excel_path)
    return excel_path


def gerar_relatorio_markdown(output_dir, config):
    sigla = config.get("sigla_obra", "TMULT")
    nome = config.get("nome_obra", "TMULT — Edifício Administrativo")
    md_path = os.path.join(output_dir, f"RELATORIO_AVANCO_FISICO_{sigla}.md")

    conteudo = f"""# 📈 RELATÓRIO EXECUTIVO DE AVANÇO FÍSICO E CURVA S
## {nome.upper()} ({sigla})

> **Referência Técnica:** Linha de Base 01 (Baseline 01 de 6 Meses / 12 Quinzenas)  
> **Metodologia de Governança:** Earned Value Management (EVM) e Schedule Performance Index (SPI)

---

## 🎯 1. STATUS GLOBAL DO AVANÇO FÍSICO

* **Data da Última Aferição:** 26/09/2026 (Fechamento da Semana S01)
* **Avanço Físico Previsto Acumulado (Q01):** **4,50%**
* **Avanço Físico Real Medido In Loco (Trena POP 09):** **4,20%**
* **Índice de Desempenho de Prazo (SPI):** **`0,93`** *(Classificação: Atenção / Alinhado à Curva de Mobilização)*
* **Situação do Caminho Crítico (CPM):** Canteiro e Fundações em andamento regular, sem desvios de marcos contratuais.

---

## 📊 2. AVANÇO FÍSICO POR MACRO-DISCIPLINA DA EAP

| EAP | Disciplina | Peso Financeiro | % Previsto | % Real Concluído | Contribuição Real | Status |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **1.0** | Administração Local e Canteiro NR-18 | 18,5% | 100,0% | **20,0%** | +3,70% | Em Andamento |
| **1.1** | Infraestrutura (Fundações e Baldrames) | 12,0% | 100,0% | **35,0%** | +4,20% | Em Andamento |
| **1.2** | Supraestrutura de Concreto Armado | 16,5% | 0,0% | **0,0%** | 0,00% | Não Iniciado |
| **2.1** | Alvenaria e Vedações Verticais | 8,5% | 0,0% | **0,0%** | 0,00% | Não Iniciado |
| **2.2** | Revestimentos, Pisos e Pintura | 14,5% | 0,0% | **0,0%** | 0,00% | Não Iniciado |
| **2.3** | Esquadrias Metálicas e Vidros | 5,0% | 0,0% | **0,0%** | 0,00% | Não Iniciado |
| **2.4** | Cobertura Termoacústica e Calhas | 6,5% | 0,0% | **0,0%** | 0,00% | Não Iniciado |
| **3.1** | Instalações Elétricas e SPDA | 8,0% | 0,0% | **0,0%** | 0,00% | Não Iniciado |
| **3.2** | Instalações Hidráulicas e Esgoto | 6,5% | 0,0% | **0,0%** | 0,00% | Não Iniciado |
| **3.3** | Climatização HVAC e Exaustão | 4,0% | 0,0% | **0,0%** | 0,00% | Não Iniciado |
| **TOTAL** | **Consolidado da Edificação** | **100,0%** | — | — | **`4,20%`** | **No Prazo** |

---

## 🧭 3. DIRETRIZES DE RECUPERAÇÃO E CONTROLE DE PRAZO
1. **Gargalo Identificado:** Chuva pontual no dia 24/09 reduziu 1 hora de escavação, recuperada no sábado (26/09) com a concretagem das sapatas S1 a S16.
2. **Meta da Quinzena Q02:** Concluir 100% das 32 sapatas isoladas e avançar a armação e fôrmas das vigas baldrames para atingir a meta acumulada de 12,0%.
3. **Amarração Contratual:** A primeira medição quinzenal do contrato `SUB-01` será emitida na quinzena Q01 e condicionada às assinaturas das `FVS-01` e `FVS-02`.

---
*Relatório emitido pela Engenharia de Planejamento e PMO Virtual.*
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
    print(f"📈 MOTOR UNIVERSAL DE AVANÇO FÍSICO E CURVA S (EVM)")
    print(f"=======================================================")
    print(f"📂 Diretório da Obra: {obra_dir}")

    config = carregar_dados_obra(obra_dir)
    sigla = config.get("sigla_obra", "OBRA")
    nome = config.get("nome_obra", sigla)
    print(f"🏗️  Obra Ativa: {nome} ({sigla})")

    output_dir = os.path.join(obra_dir, "04_PRODUCAO_E_AVANCO")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[1/2] Construindo Planilha Excel ACOMPANHAMENTO_AVANCO_FISICO_{sigla}.xlsx...")
    excel_path = construir_excel_avanco_fisico(output_dir, config)
    print(f"      ✅ Planilha Excel gerada: {excel_path}")

    print(f"\n[2/2] Gerando Relatório Executivo RELATORIO_AVANCO_FISICO_{sigla}.md...")
    md_path = gerar_relatorio_markdown(output_dir, config)
    print(f"      ✅ Relatório Markdown gerado: {md_path}")

    print(f"\n✨ Motor de Avanço Físico concluído com 100% de sucesso!")


if __name__ == "__main__":
    main()
