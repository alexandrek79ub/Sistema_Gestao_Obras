#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Catalogação e Lista Mestra de Desenhos Multi-Obra
Ecossistema de Gestão de Obras & PMO Virtual

Varre o diretório 01_ENGENHARIA_E_PROJETOS da obra informada, identifica pranchas PDF,
cruza com o dicionário titulos_desenhos.json (se presente) e gera a LISTA_DE_DESENHOS.csv
e LISTA_DE_DESENHOS.md estruturada com links diretos e carimbos auditáveis.

Uso:
    python scripts/gerar_lista_desenhos.py --obra OBRA_TMULT
    python scripts/gerar_lista_desenhos.py --obra OBRA_PETROBRAS_PORTARIA
    python scripts/gerar_lista_desenhos.py --all
    python scripts/gerar_lista_desenhos.py --dir /caminho/personalizado/da/obra
"""

import os
import sys
import csv
import json
import glob
import re
import argparse

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def extrair_codigo_revisao(fname):
    """Extrai código da prancha e número/letra de revisão a partir do nome do arquivo."""
    base_name = os.path.splitext(fname)[0]

    # Padrão 1: "CODIGO rev.X" ou "CODIGO revX"
    match = re.search(r'(.+?)\s+rev\.?([A-Za-z0-9]+)', fname, re.IGNORECASE)
    if match:
        return match.group(1).strip(), match.group(2).strip()

    # Padrão 2: "CODIGO_REV.pdf" (ex: P70069-406-DW-1430-002_1.pdf -> rev 1)
    match2 = re.search(r'(.+?)_([0-9]+)$', base_name)
    if match2:
        return match2.group(1).strip(), match2.group(2).strip()

    # Padrão 3: Sem indicador claro de revisão -> rev 0
    return base_name.strip(), "0"

def processar_desenhos_obra(proj_dir, obra_id):
    eng_dir = os.path.join(proj_dir, "01_ENGENHARIA_E_PROJETOS")
    if not os.path.exists(eng_dir):
        print(f"[AVISO] Pasta 01_ENGENHARIA_E_PROJETOS não encontrada em {proj_dir}")
        return None

    # 1. Carregar configuração e metadados
    config_path = os.path.join(proj_dir, "config_obra.json")
    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            pass

    nome_obra = config.get("nome_obra", obra_id)

    # 2. Carregar títulos dos desenhos (se existir)
    titulos_path = os.path.join(eng_dir, "titulos_desenhos.json")
    titulos_map = {}
    if os.path.exists(titulos_path):
        try:
            with open(titulos_path, "r", encoding="utf-8") as f:
                titulos_map = json.load(f)
        except Exception as e:
            print(f"[AVISO] Não foi possível ler {titulos_path}: {e}")

    # 3. Detectar PDFs em subpastas ou diretamente em 01_ENGENHARIA_E_PROJETOS
    subdirs = [d for d in os.listdir(eng_dir) if os.path.isdir(os.path.join(eng_dir, d)) and not d.startswith("_")]
    
    pastas_para_varrer = []
    if subdirs:
        for sd in subdirs:
            pastas_para_varrer.append((sd, os.path.join(eng_dir, sd)))
    else:
        pastas_para_varrer.append(("", eng_dir))

    todos_desenhos = []
    item_idx = 1

    for subdir_rel, abs_path in pastas_para_varrer:
        pdfs = sorted(glob.glob(os.path.join(abs_path, "*.pdf")))
        if not pdfs:
            continue

        carimbo_dir = os.path.join(abs_path, "_carimbos_extraidos")
        os.makedirs(carimbo_dir, exist_ok=True)

        for p in pdfs:
            fname = os.path.basename(p)
            codigo, rev = extrair_codigo_revisao(fname)

            titulo = titulos_map.get(fname, f"Prancha {codigo}")
            img_name = os.path.splitext(fname)[0] + "_carimbo.png"

            if subdir_rel:
                rel_pdf = f"{subdir_rel}/{fname}"
                rel_carimbo = f"{subdir_rel}/_carimbos_extraidos/{img_name}"
            else:
                rel_pdf = fname
                rel_carimbo = f"_carimbos_extraidos/{img_name}"

            todos_desenhos.append({
                "item": item_idx,
                "codigo": codigo,
                "titulo": titulo,
                "revisao": rev,
                "arquivo_pdf": rel_pdf,
                "carimbo_img": rel_carimbo,
                "abs_pdf": p
            })
            item_idx += 1

    if not todos_desenhos:
        print(f"[INFO] Nenhum arquivo PDF encontrado em {eng_dir}")
        return None

    # 4. Gravar LISTA_DE_DESENHOS.csv
    csv_path = os.path.join(eng_dir, "LISTA_DE_DESENHOS.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["item", "codigo", "titulo", "revisao", "arquivo_pdf", "carimbo_img"], delimiter=";")
        writer.writeheader()
        for d in todos_desenhos:
            writer.writerow({
                "item": d["item"],
                "codigo": d["codigo"],
                "titulo": d["titulo"],
                "revisao": d["revisao"],
                "arquivo_pdf": d["arquivo_pdf"],
                "carimbo_img": d["carimbo_img"]
            })

    # 5. Gravar LISTA_DE_DESENHOS.md
    md_path = os.path.join(eng_dir, "LISTA_DE_DESENHOS.md")
    subpasta_display = pastas_para_varrer[0][0] if pastas_para_varrer and pastas_para_varrer[0][0] else ""
    loc_display = f"`01_ENGENHARIA_E_PROJETOS/{subpasta_display}/`" if subpasta_display else "`01_ENGENHARIA_E_PROJETOS/`"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 📋 Lista Mestra de Desenhos - {nome_obra}\n\n")
        f.write(f"**Projeto:** {nome_obra}\n\n")
        f.write(f"**Localização dos Arquivos:** {loc_display}\n\n")
        f.write(f"**Total de Pranchas Indexadas:** {len(todos_desenhos)}\n\n")
        f.write("---\n\n")
        f.write("## 📐 Tabela Mestra de Pranchas\n\n")
        f.write("| Item | Código do Desenho | Título / Descrição da Prancha | Rev | Arquivo PDF |\n")
        f.write("| :---: | :--- | :--- | :---: | :--- |\n")
        for d in todos_desenhos:
            pdf_link_path = d["abs_pdf"].replace("\\", "/")
            pdf_filename = os.path.basename(d["arquivo_pdf"])
            f.write(f"| {d['item']} | `{d['codigo']}` | {d['titulo']} | **{d['revisao']}** | [{pdf_filename}](file:///{pdf_link_path}) |\n")
        f.write("\n---\n\n")
        f.write("## 🖼️ Imagens dos Carimbos Extraídos\n\n")
        f.write("Os carimbos foram recortados para consulta rápida e auditoria:\n\n")
        f.write(f"```text\n01_ENGENHARIA_E_PROJETOS/{subpasta_display}/_carimbos_extraidos/\n```\n\n")
        f.write(f"*Data da última atualização:* {config.get('data_auditoria', '11/09/2026')}\n")

    print(f"-> CSV gerado: {csv_path} ({len(todos_desenhos)} pranchas)")
    print(f"-> MD gerado:  {md_path}")
    return {
        "csv_path": csv_path,
        "md_path": md_path,
        "total_pranchas": len(todos_desenhos)
    }

def gerar_lista_desenhos(obra_nome=None, custom_dir=None, process_all=False):
    base_repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    projetos_dir = os.path.join(base_repo_dir, "projetos")

    if process_all:
        print(f"\n=======================================================")
        print(f"Processando Lista Mestra de Desenhos em Todas as Obras")
        print(f"=======================================================")
        for d in sorted(os.listdir(projetos_dir)):
            full_p = os.path.join(projetos_dir, d)
            if os.path.isdir(full_p) and not d.startswith("_"):
                print(f"\nObra: {d}")
                processar_desenhos_obra(full_p, d)
        return

    if custom_dir:
        proj_dir = os.path.abspath(custom_dir)
        obra_id = os.path.basename(proj_dir)
    elif obra_nome:
        proj_dir = os.path.join(projetos_dir, obra_nome)
        obra_id = obra_nome
    else:
        proj_dir = os.path.join(projetos_dir, "OBRA_TMULT")
        obra_id = "OBRA_TMULT"

    if not os.path.exists(proj_dir):
        raise FileNotFoundError(f"Diretório da obra não encontrado: {proj_dir}")

    print(f"\n=======================================================")
    print(f"Gerando Lista Mestra de Desenhos: {obra_id}")
    print(f"=======================================================")
    processar_desenhos_obra(proj_dir, obra_id)
    print("✅ Concluído com sucesso!\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motor Universal de Catalogação de Desenhos e Pranchas")
    parser.add_argument("--obra", help="Nome da pasta da obra em /projetos/ (default: OBRA_TMULT)")
    parser.add_argument("--dir", help="Caminho direto para a pasta da obra")
    parser.add_argument("--all", action="store_true", help="Processa todas as obras do repositório")
    args = parser.parse_args()

    gerar_lista_desenhos(obra_nome=args.obra, custom_dir=args.dir, process_all=args.all)
