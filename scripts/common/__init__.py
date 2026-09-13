# scripts/common/__init__.py
# -*- coding: utf-8 -*-
"""
Pacote de Infraestrutura Compartilhada dos Motores Universais.

Módulos disponíveis:
  - excel_theme  : Paleta corporativa, fontes, bordas e funções utilitárias OpenPyXL.
  - obra_io      : Parsing de CLI, leitura de config_obra.json e I/O de CSVs.
  - calendario   : Cálculo de dias úteis e janelas mensais de obra.

Uso nos motores:
  from common.excel_theme import NAVY, FONT_HEADER, aplicar_cabecalho_tabela
  from common.obra_io import parse_obra_args, carregar_config_obra, salvar_csv_utf8_sig
  from common.calendario import adicionar_dias_uteis, janelas_mensais_obra
"""
