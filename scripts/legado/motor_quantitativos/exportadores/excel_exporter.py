"""Módulo de exportação Excel do PMO Virtual.

Re-exporta funções do pacote modular `motor_quantitativos.exportadores.excel`.
"""
from motor_quantitativos.exportadores.excel import (
    escrever_boletim_medicao_avulso,
    escrever_orcamento_excel,
)

__all__ = ["escrever_orcamento_excel", "escrever_boletim_medicao_avulso"]
