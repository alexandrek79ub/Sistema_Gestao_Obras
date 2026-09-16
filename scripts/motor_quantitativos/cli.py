import argparse
import sys
from pathlib import Path

# Adiciona o diretorio scripts ao sys.path para importacoes absolutas
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from motor_quantitativos.importadores.pdf_json_importer import importar_json_inicial


def main():
    parser = argparse.ArgumentParser(description="Motor de Quantitativos e Orçamento PMO Virtual")
    parser.add_argument("json_path", help="Caminho para o JSON com as equações literais")
    parser.add_argument("--db", default="data/pmo_virtual.sqlite", help="Caminho do SQLite oficial")
    parser.add_argument("--substituir", action="store_true", help="Permite reimportação explícita para uma obra já existente")
    
    args = parser.parse_args()
    
    arquivos = importar_json_inicial(args.json_path, args.db, args.substituir)
    print("Importação concluída. Exportações derivadas atualizadas:")
    for arquivo in arquivos:
        print(f"- {arquivo}")

if __name__ == "__main__":
    main()
