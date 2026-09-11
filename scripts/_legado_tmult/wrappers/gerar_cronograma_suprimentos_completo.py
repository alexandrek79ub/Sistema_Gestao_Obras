#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wrapper de compatibilidade retroativa para a OBRA_TMULT.
Delega para scripts/gerar_cronograma_suprimentos.py --obra OBRA_TMULT
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.gerar_cronograma_suprimentos import gerar_cronograma_suprimentos

if __name__ == "__main__":
    gerar_cronograma_suprimentos(obra_nome="OBRA_TMULT")
