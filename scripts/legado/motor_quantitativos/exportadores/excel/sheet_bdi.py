from openpyxl.styles import Alignment, Font, PatternFill
from motor_quantitativos.exportadores.excel.estilos import (
    COR_CABECALHO, COR_TOPO, COR_TOTAL,
    ajustar_larguras, borda_padrao, borda_total
)


def adicionar_aba_bdi(wb) -> None:
    ws = wb.create_sheet(title="02_BDI_Analítico")
    ws.freeze_panes = "A5"

    ws.merge_cells("A1:F1")
    ws["A1"].value = "MEMORIAL DE CÁLCULO ANALÍTICO DO BDI (ACÓRDÃO 2622/2013 - TCU / IBEC)"
    ws["A1"].font = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    ws["A1"].fill = PatternFill(start_color=COR_TOPO, end_color=COR_TOPO, fill_type="solid")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 26

    ws.merge_cells("A2:F2")
    ws["A2"].value = "Fórmula Oficial: BDI = [ ((1 + AC + S + R) * (1 + DF) * (1 + L)) / (1 - I) ] - 1"
    ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="64748B")
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 18

    cabecalhos = [
        ("Item", "center"), ("Componente do BDI", "left"), ("Sigla", "center"),
        ("Faixa Referencial TCU", "center"), ("Valor Adotado (%)", "right"),
        ("Justificativa Técnica / Base Normativa", "left"),
    ]

    for col_idx, (nome_col, alin) in enumerate(cabecalhos, start=1):
        cell = ws.cell(row=4, column=col_idx, value=nome_col)
        cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color=COR_CABECALHO, end_color=COR_CABECALHO, fill_type="solid")
        cell.alignment = Alignment(horizontal=alin, vertical="center")
        cell.border = borda_padrao()
    ws.row_dimensions[4].height = 24

    bdi_itens = [
        ("1", "Administração Central", "AC", "3,00% a 5,50%", 0.0400, "Rateio corporativo da sede e governança"),
        ("2", "Seguros e Garantias", "S", "0,80% a 1,50%", 0.0100, "Seguro de riscos de engenharia e apólices"),
        ("3", "Riscos e Imprevistos", "R", "0,97% a 2,00%", 0.0150, "Flutuações pontuais e intempéries leves"),
        ("4", "Despesas Financeiras", "DF", "0,59% a 1,39%", 0.0100, "Custo do capital de giro (defasagem medição)"),
        ("5", "Lucro Operacional Bruto", "L", "6,16% a 9,96%", 0.0800, "Remuneração justa pela capacidade e risco"),
        ("6", "Tributos Faturamento (PIS/COFINS/ISS)", "I", "5,65% a 13,15%", 0.0865, "PIS (0,65%) + COFINS (3%) + ISS médio (5%)"),
    ]

    for idx, (num, comp, sigla, faixa, val, just) in enumerate(bdi_itens):
        r_num = 5 + idx
        ws.row_dimensions[r_num].height = 20
        ws.cell(row=r_num, column=1, value=num).alignment = Alignment(horizontal="center", vertical="center")
        ws.cell(row=r_num, column=2, value=comp)
        ws.cell(row=r_num, column=3, value=sigla).alignment = Alignment(horizontal="center", vertical="center")
        ws.cell(row=r_num, column=4, value=faixa).alignment = Alignment(horizontal="center", vertical="center")
        
        c_val = ws.cell(row=r_num, column=5, value=val)
        c_val.number_format = "0.00%"
        c_val.alignment = Alignment(horizontal="right", vertical="center")
        
        ws.cell(row=r_num, column=6, value=just)
        for col in range(1, 7):
            ws.cell(row=r_num, column=col).border = borda_padrao()
            ws.cell(row=r_num, column=col).font = Font(name="Calibri", size=10)

    # Linha BDI Resultante
    r_res = 11
    ws.row_dimensions[r_res].height = 26
    ws.merge_cells(f"A{r_res}:D{r_res}")
    ws[f"A{r_res}"].value = "TAXA DE BDI ANALÍTICA RESULTANTE:"
    ws[f"A{r_res}"].font = Font(name="Calibri", size=10, bold=True, color="0F172A")
    ws[f"A{r_res}"].alignment = Alignment(horizontal="right", vertical="center")
    ws[f"A{r_res}"].fill = PatternFill(start_color=COR_TOTAL, end_color=COR_TOTAL, fill_type="solid")

    for col in range(1, 5):
        ws.cell(row=r_res, column=col).border = borda_total()

    cell_bdi_res = ws[f"E{r_res}"]
    cell_bdi_res.value = "=ROUND((( (1 + E5 + E6 + E7) * (1 + E8) * (1 + E9) ) / (1 - E10)) - 1, 4)"
    cell_bdi_res.font = Font(name="Calibri", size=11, bold=True, color="0F172A")
    cell_bdi_res.number_format = "0.00%"
    cell_bdi_res.alignment = Alignment(horizontal="right", vertical="center")
    cell_bdi_res.fill = PatternFill(start_color=COR_TOTAL, end_color=COR_TOTAL, fill_type="solid")
    cell_bdi_res.border = borda_total()

    ws.cell(row=r_res, column=6, value="Fórmula paramétrica viva (recalcula com os parâmetros)").fill = PatternFill(start_color=COR_TOTAL, end_color=COR_TOTAL, fill_type="solid")
    ws.cell(row=r_res, column=6).border = borda_total()
    ws.cell(row=r_res, column=6).font = Font(name="Calibri", size=9, italic=True)

    ajustar_larguras(ws)
