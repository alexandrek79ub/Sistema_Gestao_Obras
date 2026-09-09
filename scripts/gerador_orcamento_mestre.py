import os
import csv
import json
import argparse
import ast

def calcular_expressao(expressao):
    """
    Avalia uma expressão matemática de forma segura.
    Permite apenas números e operadores matemáticos básicos.
    """
    try:
        # Substitui vírgulas por pontos caso a IA tenha enviado padrão brasileiro
        expressao_limpa = expressao.replace(',', '.')
        
        # Cria uma AST (Abstract Syntax Tree) e avalia apenas nós seguros
        node = ast.parse(expressao_limpa, mode='eval')
        valid_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, 
                       ast.operator, ast.unaryop)
                       
        for n in ast.walk(node):
            if not isinstance(n, valid_nodes):
                raise ValueError(f"Operação não permitida na expressão: {expressao}")
                
        # Compila e executa com contexto vazio (segurança máxima)
        resultado = eval(compile(node, '<string>', 'eval'), {"__builtins__": None}, {})
        return round(resultado, 4)
    except Exception as e:
        print(f"[AVISO] Não foi possível calcular a expressão '{expressao}': {e}")
        return 0.0

def gerar_orcamento(json_path):
    if not os.path.exists(json_path):
        print(f"[ERRO] Arquivo {json_path} não encontrado!")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    projeto = data.get("projeto", "PROJETO_NAO_NOMEADO")
    base_dir = data.get("base_dir", ".")
    data_auditoria = data.get("data_auditoria", "DATA_NAO_INFORMADA")
    disciplinas = data.get("disciplinas", {})

    os.makedirs(base_dir, exist_ok=True)

    header_csv = ["Código EAP", "Item / Descricao", "Disciplina", "Qtd Projeto", "Unidade Proj", "Perda (%)", "Qtd Comercial UCC", "Unidade UCC", "Prancha Referencia"]
    consolidated_rows = [header_csv]

    print(f"\n[INFO] Iniciando Geração Mestra (Motor Híbrido Cérebro/CPU)")
    print(f"[INFO] Projeto: {projeto}")
    print(f"[INFO] Destino: {base_dir}\n")

    for key, disc in disciplinas.items():
        titulo_disc = disc.get("titulo", key.upper())
        pranchas_ref = disc.get("pranchas_ref", "N/A")
        
        csv_filename = disc.get("csv_filename", f"QUANTITATIVO_{key.upper()}.csv")
        md_filename = disc.get("md_filename", f"MEMORIA_CALCULO_{key.upper()}.md")
        
        csv_path = os.path.join(base_dir, csv_filename)
        md_path = os.path.join(base_dir, md_filename)

        memoria_calculo_dinamica = []
        rows_com_disciplina = []
        
        itens = disc.get("itens_orcamento", [])
        
        for item in itens:
            # Dados do Item
            cod_eap = item.get("codigo_eap", "")
            descricao = item.get("descricao", "")
            unidade = item.get("unidade", "")
            perda_pct = float(item.get("perda_pct", 0))
            unidade_ucc = item.get("unidade_ucc", unidade)
            ref_prancha = item.get("ref_prancha", pranchas_ref)
            fator_ucc = float(item.get("fator_conversao_ucc", 1.0)) # Ex: 1m3 para 1m3 = 1. Kg para barra = 1/12
            
            # Processamento Matemático Físico
            memoria_calculo_dinamica.append(f"### {cod_eap} - {descricao}")
            total_qtd_projeto = 0.0
            
            for eq in item.get("equacoes", []):
                desc_eq = eq.get("descricao_memoria", "Subitem")
                expressao = eq.get("expressao_matematica", "0")
                
                # CPU resolve a matemática rigorosamente
                resultado = calcular_expressao(expressao)
                total_qtd_projeto += resultado
                
                # Escreve a memória granular
                memoria_calculo_dinamica.append(f"- **{desc_eq}:** `{expressao}` = **{resultado} {unidade}**")
            
            # Aplicação de Perdas e Unidade Comercial (UCC)
            qtd_com_perda = total_qtd_projeto * (1 + (perda_pct / 100))
            qtd_ucc = round(qtd_com_perda * fator_ucc, 2)
            total_qtd_projeto = round(total_qtd_projeto, 4)
            
            memoria_calculo_dinamica.append(f"\n> **Total Projeto:** `{total_qtd_projeto} {unidade}` | **Com Perda ({perda_pct}%):** `{round(qtd_com_perda, 4)} {unidade}` | **Pedido (UCC):** `{qtd_ucc} {unidade_ucc}`\n")
            
            # Montagem da Linha do CSV
            r_novo = [cod_eap, descricao, titulo_disc, total_qtd_projeto, unidade, perda_pct, qtd_ucc, unidade_ucc, ref_prancha]
            rows_com_disciplina.append(r_novo)
            consolidated_rows.append(r_novo)

        # Write CSV
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(header_csv)
            writer.writerows(rows_com_disciplina)
        print(f"  [OK] Células Calculadas e CSV Gerado: {csv_filename}")

        # Write Markdown de Memória de Cálculo
        md_content = f"# 🏛️ Memória de Cálculo Auditável: {titulo_disc}\n\n"
        md_content += f"**Projeto:** {projeto}  \n"
        md_content += f"**Disciplina:** {titulo_disc}  \n"
        md_content += f"**Documentos de Referência:** Pranchas `{pranchas_ref}`  \n"
        md_content += f"**Data da Auditoria:** {data_auditoria}  \n\n"
        md_content += "---\n\n"
        
        md_content += "## 🧮 1. Demonstração Matemática Detalhada (Calculada via CPU)\n\n"
        md_content += "\n".join(memoria_calculo_dinamica)
        
        md_content += "\n\n---\n\n"
        md_content += "## 📊 2. Tabela Consolidada de Quantitativos e Pedido de Compras (UCC)\n\n"
        md_content += "| Código EAP | Descrição do Insumo / Serviço | Qtd Projeto | Perda (%) | Qtd Comercial UCC | Unidade UCC | Prancha Ref |\n"
        md_content += "| :---: | :--- | :---: | :---: | :---: | :---: | :--- |\n"
        
        for r in rows_com_disciplina:
            md_content += f"| **{r[0]}** | {r[1]} | {r[3]} {r[4]} | {r[5]}% | **{r[6]}** | `{r[7]}` | `{r[8]}` |\n"

        md_content += "\n---\n\n"
        md_content += f"*Data da última atualização:* {data_auditoria}\n"

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"  [OK] Markdown Gerado com Equações Avaliadas: {md_filename}")

    # Gerar Orçamento Consolidado Mestre em CSV
    consolidated_csv_path = os.path.join(base_dir, "ORCAMENTO_BASE_CONSOLIDADO.csv")
    with open(consolidated_csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(consolidated_rows)
    print(f"\n[SUCESSO] Matemática Avaliada. Orçamento Consolidado Gerado: {consolidated_csv_path} ({len(consolidated_rows)-1} itens)\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motor de cálculo matemático e formatação de CSV/MD a partir do JSON extraído pela IA.")
    parser.add_argument("json_path", help="Caminho para o JSON com as equações literais.")
    args = parser.parse_args()
    gerar_orcamento(args.json_path)
