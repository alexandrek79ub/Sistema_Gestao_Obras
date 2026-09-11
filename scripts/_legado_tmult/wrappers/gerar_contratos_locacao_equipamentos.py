#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wrapper de compatibilidade retroativa para a OBRA_TMULT.
Delega a execução para o motor universal scripts/gerar_contratos_locacao.py.
"""
import sys
import subprocess
from pathlib import Path

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    engine = base_dir / "scripts" / "gerar_contratos_locacao.py"
    cmd = [sys.executable, str(engine), "--obra", "OBRA_TMULT"] + sys.argv[1:]
    sys.exit(subprocess.call(cmd))
