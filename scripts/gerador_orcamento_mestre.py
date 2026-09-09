import os
import csv
import json
import argparse
import ast
import math
import re
import shutil

def calcular_expressao(expressao):
    """
    Avalia uma expressão matemática de forma segura e determinística.
    Permite números, constantes de engenharia (pi, e), funções matemáticas básicas (sqrt, abs, round)
    e operadores aritméticos (+, -, *, /, **, //, %).
    """
    try:
        # Substitui vírgulas por pontos caso a IA tenha enviado padrão brasileiro
        expressao_limpa = str(expressao).replace(',', '.')
        
        # Cria uma AST (Abstract Syntax Tree) e avalia apenas nós seguros
        node = ast.parse(expressao_limpa, mode='eval')
        valid_nodes = (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, 
            ast.operator, ast.unaryop, ast.Name, ast.Call, 
            ast.Load, ast.expr_context
        )
        
        allowed_names = {'pi', 'e', 'sqrt', 'abs', 'round'}
        
        for n in ast.walk(node):
            if not isinstance(n, valid_nodes):
                raise ValueError(f"Operação não permitida na expressão: {expressao}")
            if isinstance(n, ast.Name):
                if n.id.lower() not in allowed_names:
                    raise ValueError(f"Identificador não permitido: '{n.id}'")
            if isinstance(n, ast.Call):
                if not (isinstance(n.func, ast.Name) and n.func.id.lower() in {'sqrt', 'abs', 'round'}):
                    raise ValueError(f"Função não permitida na expressão: '{ast.dump(n.func)}'")
                
        # Contexto matemático seguro (zero builtins)
        math_context = {
            "pi": math.pi,
            "PI": math.pi,
            "Pi": math.pi,
            "e": math.e,
            "sqrt": math.sqrt,
            "abs": abs,
            "round": round
        }
        
        resultado = eval(compile(node, '<string>', 'eval'), {"__builtins__": None}, math_context)
        return round(float(resultado), 4)
    except Exception as e:
        print(f"[AVISO] Não foi possível calcular a expressão '{expressao}': {e}")
        return 0.0

def formatar_moeda(valor):
    """Formata valor float para moeda brasileira R$ XX.XXX,XX"""
    if valor <= 0:
        return "-"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

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

    header_csv = [
        "Código EAP", "Item / Descricao", "Disciplina", 
        "Qtd Projeto", "Unidade Proj", "Perda (%)", 
        "Qtd Comercial UCC", "Unidade UCC", "Prancha Referencia",
        "Preço Unitário (R$)", "Custo Total (R$)"
    ]
    consolidated_rows = [header_csv]

    print(f"\n[INFO] Iniciando Geração Mestra (Motor Híbrido Cérebro/CPU v2.0)")
    print(f"[INFO] Projeto: {projeto}")
    print(f"[INFO] Destino: {base_dir}\n")

    unidades_discretas = (
        'barra', 'barras', 'saco', 'sacos', 'lata', 'latas', 
        'caixa', 'caixas', 'unid', 'unidade', 'unidades', 
        'peca', 'peça', 'peças', 'rolo', 'rolos', 'tubo', 'tubos', 
        'chapa', 'chapas', 'betoneira', 'betoneiras', 'caminhão', 
        'caminhoes', 'caminhões', 'galão', 'galões', 'galao'
    )

    total_geral_financeiro = 0.0

    for key, disc in disciplinas.items():
        titulo_disc = disc.get("titulo", key.upper())
        pranchas_ref = disc.get("pranchas_ref", "N/A")
        
        csv_filename = disc.get("csv_filename", f"QUANTITATIVO_{key.upper()}.csv")
        md_filename = disc.get("md_filename", f"MEMORIA_CALCULO_{key.upper()}.md")
        
        csv_path = os.path.join(base_dir, csv_filename)
        md_path = os.path.join(base_dir, md_filename)

        memoria_calculo_dinamica = []
        rows_com_disciplina = []
        subtotal_disc_financeiro = 0.0
        
        itens = disc.get("itens_orcamento", [])
        
        # Suporte a itens de equações dinâmicas (Motor AST Cérebro/CPU)
        for item in itens:
            # Dados do Item
            cod_eap = item.get("codigo_eap", "")
            descricao = item.get("descricao", "")
            unidade = item.get("unidade", "")
            perda_pct = float(item.get("perda_pct", 0))
            unidade_ucc = item.get("unidade_ucc", unidade)
            ref_prancha = item.get("ref_prancha", pranchas_ref)
            fator_ucc = float(item.get("fator_conversao_ucc", 1.0))
            preco_unit = float(item.get("preco_unitario", item.get("custo_unitario", 0.0)))
            
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
            
            # Aplicação de Perdas e Unidade Comercial (UCC) com Regra da Trena / POP 05
            unid_ucc_clean = unidade_ucc.lower().strip()
            eh_discreto = any(u in unid_ucc_clean for u in unidades_discretas) or item.get("arredondar_cima", False)
            
            qtd_com_perda = total_qtd_projeto * (1 + (perda_pct / 100))
            
            if eh_discreto:
                # Arredondamento para CIMA (teto) para insumos inteiros de compra
                qtd_ucc = math.ceil(round(qtd_com_perda * fator_ucc, 6))
            else:
                qtd_ucc = round(qtd_com_perda * fator_ucc, 2)
                
            total_qtd_projeto = round(total_qtd_projeto, 4)
            
            # Cálculo Financeiro Opcional
            custo_total_item = round(qtd_ucc * preco_unit, 2) if preco_unit > 0 else 0.0
            subtotal_disc_financeiro += custo_total_item
            total_geral_financeiro += custo_total_item

            preco_str = formatar_moeda(preco_unit)
            total_str = formatar_moeda(custo_total_item)
            
            nota_financeira = f" | **Custo Total:** `{total_str}`" if custo_total_item > 0 else ""
            memoria_calculo_dinamica.append(f"\n> **Total Projeto:** `{total_qtd_projeto} {unidade}` | **Com Perda ({perda_pct}%):** `{round(qtd_com_perda, 4)} {unidade}` | **Pedido (UCC):** `{qtd_ucc} {unidade_ucc}`{nota_financeira}\n")
            
            # Montagem da Linha do CSV
            r_novo = [
                cod_eap, descricao, titulo_disc, total_qtd_projeto, unidade, 
                perda_pct, qtd_ucc, unidade_ucc, ref_prancha, preco_str, total_str
            ]
            rows_com_disciplina.append(r_novo)
            consolidated_rows.append(r_novo)

        # Suporte a datasets existentes com linhas pré-compiladas ("rows")
        if not itens and "rows" in disc:
            for r in disc["rows"]:
                r_exp = list(r)
                while len(r_exp) < len(header_csv):
                    r_exp.append("-")
                rows_com_disciplina.append(r_exp)
                consolidated_rows.append(r_exp)

        # Write CSV da Disciplina
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(header_csv)
            writer.writerows(rows_com_disciplina)
        print(f"  [OK] Células Calculadas e CSV Gerado: {csv_filename}")

        # Write Markdown de Memória de Cálculo
        # Preservação integral da memória técnica existente (se não estiver gerando via equações dinâmicas)
        secao_memoria_preservada = ""
        secao_3_preservada = ""
        caution_block_preservado = ""
        if os.path.exists(md_path):
            try:
                with open(md_path, 'r', encoding='utf-8') as f_existente:
                    conteudo_anterior = f_existente.read()
                    
                    if not memoria_calculo_dinamica:
                        # 1. Preservar bloco de alerta inicial (CAUTION / WARNING / NOTE) se existir
                        m_alert = re.search(r'(>\s*\[![A-Z]+\][\s\S]*?)(?=\n##|\Z)', conteudo_anterior)
                        if m_alert:
                            caution_block_preservado = m_alert.group(1).strip()
                        
                        # 2. Preservar toda a memória técnica que antecede a Tabela Consolidada Oficial
                        marcador_tabela = ""
                        if "## 📊 2. Tabela Consolidada" in conteudo_anterior:
                            marcador_tabela = "## 📊 2. Tabela Consolidada"
                        elif "## 📊 Tabela Consolidada" in conteudo_anterior:
                            marcador_tabela = "## 📊 Tabela Consolidada"
                        elif "## 📊 2." in conteudo_anterior:
                            marcador_tabela = "## 📊 2."

                        if marcador_tabela:
                            partes = conteudo_anterior.split(marcador_tabela, 1)
                            cabecalho_e_memoria = partes[0]
                            resto_tabela = marcador_tabela + partes[1]
                            
                            # Extrai a memória após o cabeçalho inicial (após a primeira linha '---')
                            if "\n---\n" in cabecalho_e_memoria:
                                partes_cab = cabecalho_e_memoria.split("\n---\n", 1)
                                memoria_bruta = partes_cab[1].strip()
                            else:
                                memoria_bruta = cabecalho_e_memoria.strip()
                            
                            # Remove o bloco de alerta da memória bruta se já foi capturado
                            if caution_block_preservado and caution_block_preservado in memoria_bruta:
                                memoria_bruta = memoria_bruta.replace(caution_block_preservado, "").strip()
                                
                            secao_memoria_preservada = memoria_bruta.rstrip("-").strip()
                    
                    # 3. Preservar seções de fechamento (Certificado / Checklists / Seção 3) para todas as disciplinas
                    if "## 📋 3." in conteudo_anterior:
                        s3_raw = "## 📋 3." + conteudo_anterior.split("## 📋 3.", 1)[1]
                        s3_clean = re.split(r'\n---\s*\n\s*\*Data da última atualização', s3_raw, flags=re.IGNORECASE)[0].strip()
                        secao_3_preservada = s3_clean.rstrip("-").strip()
                    elif "CERTIFICADO DE AUDITORIA" in conteudo_anterior:
                        m_cert = re.search(r'(\={20,}[\s\S]*?STATUS:[\s\S]*?\={20,})', conteudo_anterior)
                        if m_cert:
                            secao_3_preservada = m_cert.group(1).strip()
            except Exception as e:
                print(f"  [AVISO] Não foi possível ler seções existentes de {md_path}: {e}")

        # Trava de Segurança: se o arquivo existente tem mais de 40 linhas e a memória técnica não pôde ser lida nem gerada
        if os.path.exists(md_path) and not memoria_calculo_dinamica and not secao_memoria_preservada:
            with open(md_path, 'r', encoding='utf-8') as f_existente:
                linhas_existente = len(f_existente.readlines())
            if linhas_existente > 40:
                print(f"  [TRAVA DE SEGURANÇA] Arquivo {md_filename} possui {linhas_existente} linhas detalhadas e a memória técnica não foi parseada com segurança. Sobrescrita abortada para evitar perda de dados!")
                continue

        # Backup de segurança antes de sobrescrever
        if os.path.exists(md_path):
            try:
                shutil.copy2(md_path, md_path + ".bak")
            except Exception:
                pass

        md_content = f"# 🏛️ Memória de Cálculo Auditável: {titulo_disc}\n\n"
        md_content += f"**Projeto:** {projeto}  \n"
        md_content += f"**Disciplina:** {titulo_disc}  \n"
        md_content += f"**Documentos de Referência:** Pranchas `{pranchas_ref}`  \n"
        md_content += f"**Data da Auditoria:** {data_auditoria}  \n\n"
        md_content += "---\n\n"
        
        if caution_block_preservado:
            md_content += f"{caution_block_preservado}\n\n"

        if memoria_calculo_dinamica:
            md_content += "## 🧮 1. Demonstração Matemática Detalhada (Calculada via CPU)\n\n"
            md_content += "\n".join(memoria_calculo_dinamica)
            md_content += "\n\n---\n\n"
        elif secao_memoria_preservada:
            md_content += f"{secao_memoria_preservada}\n\n---\n\n"
        
        md_content += "## 📊 2. Tabela Consolidada de Quantitativos e Pedido de Compras (UCC)\n\n"
        md_content += "| Código EAP | Descrição do Insumo / Serviço | Qtd Projeto | Perda (%) | Qtd Comercial UCC | Unidade UCC | Prancha Ref | Preço Unit. | Custo Total |\n"
        md_content += "| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: |\n"
        
        for r in rows_com_disciplina:
            md_content += f"| **{r[0]}** | {r[1]} | {r[3]} {r[4]} | {r[5]}% | **{r[6]}** | `{r[7]}` | `{r[8]}` | {r[9]} | **{r[10]}** |\n"

        if subtotal_disc_financeiro > 0:
            md_content += f"\n> 💰 **Subtotal Financeiro da Disciplina:** `{formatar_moeda(subtotal_disc_financeiro)}`\n"

        if secao_3_preservada:
            if not secao_3_preservada.startswith("## 📋 3.") and not secao_3_preservada.startswith("="):
                md_content += f"\n---\n\n## 📋 3. {secao_3_preservada}\n"
            else:
                md_content += f"\n---\n\n{secao_3_preservada}\n"

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
    print(f"\n[SUCESSO] Matemática Avaliada. Orçamento Consolidado Gerado: {consolidated_csv_path} ({len(consolidated_rows)-1} itens)")
    if total_geral_financeiro > 0:
        print(f"[FINANCEIRO] Total Orçamento Base Consolidado: {formatar_moeda(total_geral_financeiro)}\n")
    else:
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motor de cálculo matemático e formatação de CSV/MD a partir do JSON extraído pela IA.")
    parser.add_argument("json_path", help="Caminho para o JSON com as equações literais.")
    args = parser.parse_args()
    gerar_orcamento(args.json_path)
