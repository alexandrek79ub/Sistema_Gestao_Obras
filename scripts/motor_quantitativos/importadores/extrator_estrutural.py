"""
Adaptador de compatibilidade para o novo sistema modular de extração.
Delega a execução para o roteador modular em scripts/motor_quantitativos/importadores/roteador.py.
"""

import sys
from pathlib import Path

diretorio_scripts = Path(__file__).resolve().parent.parent.parent
if str(diretorio_scripts) not in sys.path:
    sys.path.insert(0, str(diretorio_scripts))

from motor_quantitativos.importadores.roteador import main

if __name__ == "__main__":
    main()
