#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wrapper de compatibilidade retroativa para a OBRA_TMULT.
Delega a execução para o Motor Universal: scripts/precificar_obra.py --obra OBRA_TMULT
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.precificar_obra import precificar_obra

if __name__ == "__main__":
    precificar_obra(obra_nome="OBRA_TMULT")
