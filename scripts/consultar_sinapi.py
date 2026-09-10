import os
import csv
import sys
import argparse
import unicodedata

def normalizar(texto):
    if not texto:
        return ""
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').upper()

def buscar(termo, tipo="composicao", limite=10):
    base_dir = os.path.abspath("apoio/sinapi_sp")
    if tipo == "insumo":
        csv_file = os.path.join(base_dir, "SINAPI_SP_INSUMOS_2026_07.csv")
        cod_col = "CODIGO_INSUMO"
        preco_col = "PRECO_UNIT_SP_RS"
    else:
        csv_file = os.path.join(base_dir, "SINAPI_SP_COMPOSICOES_2026_07.csv")
        cod_col = "CODIGO_COMPOSICAO"
        preco_col = "CUSTO_TOTAL_SP_RS"
        
    if not os.path.exists(csv_file):
        print(f"[ERRO] Arquivo {csv_file} não encontrado. Execute primeiro scripts/extrair_sinapi_sp.py!")
        return

    palavras = normalizar(termo).split()
    termo_cod = termo.strip().upper()
    resultados = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            desc_norm = normalizar(row["DESCRICAO"])
            cod = row[cod_col].strip().upper()
            grupo = row.get("GRUPO", "")
            
            # Match se todas as palavras estiverem na descrição ou se o código for exato
            if all(p in desc_norm for p in palavras) or termo_cod == cod:
                preco = row.get(preco_col, "")
                try:
                    preco_float = float(preco) if preco else 0.0
                    preco_fmt = f"R$ {preco_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                except:
                    preco_fmt = preco
                    
                resultados.append({
                    "codigo": cod,
                    "grupo": grupo,
                    "descricao": row["DESCRICAO"],
                    "unidade": row["UNIDADE"],
                    "preco": preco_fmt
                })
                if len(resultados) >= limite:
                    break
                    
    print(f"\n[BUSCA SINAPI SP 07/2026] [{tipo.upper()}]: '{termo}' (Encontrados: {len(resultados)})\n" + "="*80)
    for r in resultados:
        print(f"[{r['codigo']}] ({r['unidade']}) - {r['preco']}")
        print(f"  Grupo: {r['grupo']}")
        print(f"  {r['descricao']}")
        print("-" * 80)

if __name__ == "__main__":
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    parser = argparse.ArgumentParser(description="Consulta rápida à base SINAPI SP 07/2026")
    parser.add_argument("termo", help="Palavra-chave ou código para pesquisar")
    parser.add_argument("--insumo", action="store_true", help="Buscar na tabela de insumos (padrão é composições)")
    parser.add_argument("--limite", type=int, default=10, help="Limite de resultados (padrão: 10)")
    
    args = parser.parse_args()
    tipo_busca = "insumo" if args.insumo else "composicao"
    buscar(args.termo, tipo=tipo_busca, limite=args.limite)
