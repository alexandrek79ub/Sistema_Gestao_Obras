from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import openpyxl

from motor_quantitativos.exportadores.excel.sheet_orcamento import adicionar_aba_orcamento
from motor_quantitativos.exportadores.excel.sheet_bdi import adicionar_aba_bdi
from motor_quantitativos.exportadores.excel.sheet_composicoes import adicionar_aba_composicoes
from motor_quantitativos.exportadores.excel.sheet_curva_abc import adicionar_aba_curva_abc
from motor_quantitativos.exportadores.excel.sheet_memoria import adicionar_aba_memoria
from motor_quantitativos.exportadores.excel.sheet_medicao import adicionar_aba_medicao


def escrever_orcamento_excel(caminho: Path, nome_obra: str, checksum: str, itens: list[dict[str, Any]]) -> Path:
    """Orquestrador do Caderno Executivo Master da Obra (6 abas com formulas vivas)."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    data_emissao = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")

    wb = openpyxl.Workbook()

    # 1. Planilha Orçamentária Executiva
    linha_total_orcamento = adicionar_aba_orcamento(wb, nome_obra, checksum, data_emissao, itens)

    # 2. Memorial Analítico de BDI (TCU 2622 / IBEC)
    adicionar_aba_bdi(wb)

    # 3. Composições Analíticas de Custos (CCU)
    adicionar_aba_composicoes(wb, nome_obra, itens)

    # 4. Curva ABC de Serviços (Matriz Pareto 80/20)
    adicionar_aba_curva_abc(wb, nome_obra, itens, linha_total_orcamento)

    # 5. Memória de Cálculo e Levantamento Geométrico
    adicionar_aba_memoria(wb, nome_obra, itens)

    # 6. Boletim de Medição e Avanço Físico-Financeiro
    adicionar_aba_medicao(wb, nome_obra, itens)

    wb.save(str(caminho))
    return caminho


def escrever_boletim_medicao_avulso(caminho: Path, nome_obra: str, itens: list[dict[str, Any]]) -> Path:
    """Gera um arquivo avulso leve focado exclusivamente na rotina de medicao de campo."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.Workbook()
    adicionar_aba_medicao(wb, nome_obra, itens)
    wb.save(str(caminho))
    return caminho
