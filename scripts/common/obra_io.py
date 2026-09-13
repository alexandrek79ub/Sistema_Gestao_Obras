#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários de I/O e CLI — Motores Universais.

Centraliza parsing de argumentos, resolução de caminhos, leitura de config_obra.json
e escrita de CSVs no padrão mandatório do ecossistema (utf-8-sig, delimitador ';').

Regras aplicadas (Manual de Boas Práticas §2.1, §2.2, §3.1):
  - CLI com argparse: --obra e --dir obrigatórios.
  - Caminhos resolvidos a partir da raiz do repositório (sem hardcoding).
  - CSVs sempre escritos com utf-8-sig e delimitador ';'.
  - Fallback seguro se config_obra.json não existir.
"""

import os
import sys
import csv
import json
import argparse

# Raiz do repositório: dois níveis acima de scripts/common/
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Blindagem de encoding UTF-8 no Windows (Manual §2.3)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


# =============================================================================
# CLI — PARSING DE ARGUMENTOS
# =============================================================================

def parse_obra_args(descricao="Motor Universal de Gestão de Obras."):
    """
    Cria e retorna um parser argparse padronizado com --obra e --dir.

    Uso nos motores:
        from common.obra_io import parse_obra_args, resolver_obra_dir
        args = parse_obra_args("Descrição do Motor")
        obra_dir = resolver_obra_dir(args)

    Args:
        descricao : Texto de descrição para --help do script.

    Returns:
        argparse.Namespace com atributos .obra e .dir
    """
    parser = argparse.ArgumentParser(description=descricao)
    parser.add_argument(
        "--obra",
        type=str,
        default="OBRA_TMULT",
        help="Nome da pasta da obra em projetos/ (ex: OBRA_TMULT, RESIDENCIAL_ALPHA)"
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=None,
        help="Caminho direto absoluto ou relativo para a pasta da obra (sobrescreve --obra)"
    )
    return parser.parse_args()


def resolver_obra_dir(args):
    """
    Resolve o caminho absoluto da pasta da obra a partir dos argumentos de CLI.

    Prioridade: --dir > --obra
    Nunca utiliza caminhos hardcoded (Manual §2.2).

    Args:
        args : Namespace retornado por parse_obra_args() ou argparse.

    Returns:
        str : Caminho absoluto da pasta da obra.

    Raises:
        SystemExit : Se a pasta resolvida não existir.
    """
    if args.dir:
        obra_dir = os.path.abspath(args.dir)
    else:
        obra_dir = os.path.join(ROOT_DIR, "projetos", args.obra)

    if not os.path.isdir(obra_dir):
        print(f"[ERRO] Pasta da obra não encontrada: {obra_dir}")
        sys.exit(1)

    return obra_dir


# =============================================================================
# CONFIGURAÇÃO DA OBRA
# =============================================================================

_CONFIG_FALLBACK_FIELDS = {
    "nome_obra": None,           # preenchido dinamicamente pelo nome da pasta
    "sigla_obra": None,          # primeiros 6 caracteres do nome da pasta
    "prazo_meses": 6,
    "data_inicio": "01/10/2026",
    "bdi_servicos": 0.2717,
    "bdi_equipamentos": 0.15,
    "valor_contrato": 0.0,
    "cliente": "A definir",
    "endereco_obra": "A definir",
}


def carregar_config_obra(obra_dir):
    """
    Carrega o arquivo config_obra.json da obra com fallback seguro.

    Se config_obra.json não existir, retorna um dicionário com valores padrão
    derivados do nome da pasta, sem lançar exceção (Manual §2.5).

    Args:
        obra_dir : Caminho absoluto da pasta da obra.

    Returns:
        dict : Configuração da obra.
    """
    config_path = os.path.join(obra_dir, "config_obra.json")
    nome_pasta = os.path.basename(obra_dir)

    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        # Garante que campos obrigatórios existam (retrocompatibilidade)
        config.setdefault("nome_obra", nome_pasta)
        config.setdefault("sigla_obra", nome_pasta[:6].upper())
        for k, v in _CONFIG_FALLBACK_FIELDS.items():
            config.setdefault(k, v)
        return config
    else:
        print(f"[AVISO] config_obra.json não encontrado em {obra_dir}. Usando valores padrão.")
        fallback = dict(_CONFIG_FALLBACK_FIELDS)
        fallback["nome_obra"] = nome_pasta
        fallback["sigla_obra"] = nome_pasta[:6].upper()
        return fallback


# =============================================================================
# LEITURA DE ARQUIVOS PADRÃO DA OBRA
# =============================================================================

def carregar_cpm_json(obra_dir):
    """
    Lê dados_cpm.json da pasta 03_PLANEJAMENTO_E_CRONOGRAMA.

    Returns:
        dict ou None se não encontrado.
    """
    cpm_path = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA", "dados_cpm.json")
    if not os.path.exists(cpm_path):
        print(f"[AVISO] dados_cpm.json não encontrado: {cpm_path}")
        return None
    with open(cpm_path, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_orcamento_csv(obra_dir):
    """
    Lê o CSV de orçamento base consolidado da pasta 02_ORCAMENTO_BASE_E_CONTRATOS.

    Returns:
        list[dict] : Linhas do CSV como dicionários, ou lista vazia se não encontrado.
    """
    candidatos = [
        os.path.join(obra_dir, "02_ORCAMENTO_BASE_E_CONTRATOS", "ORCAMENTO_BASE_CONSOLIDADO.csv"),
    ]
    for path in candidatos:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8-sig") as f:
                return list(csv.DictReader(f, delimiter=";"))
    print(f"[AVISO] Arquivo de orçamento base não encontrado em {obra_dir}/02_ORCAMENTO_BASE_E_CONTRATOS/")
    return []


def carregar_programacao_curto_prazo(obra_dir, obra_nome=None):
    """
    Localiza e lê o CSV de programação de curto prazo (esteira Takt/WWP).

    Tenta múltiplos padrões de nome de arquivo para retrocompatibilidade.

    Returns:
        list[dict] : Linhas do CSV como dicionários, ou lista vazia se não encontrado.
    """
    sigla = os.path.basename(obra_dir).replace("OBRA_", "")
    candidatos = [
        f"PROGRAMACAO_CURTO_PRAZO_{os.path.basename(obra_dir)}.csv",
        f"PROGRAMACAO_CURTO_PRAZO_{sigla}.csv",
        "PROGRAMACAO_CURTO_PRAZO_OBRA_TMULT.csv",
        "PROGRAMACAO_CURTO_PRAZO_TMULT.csv",
    ]
    dir_plan = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA")
    for nome in candidatos:
        path = os.path.join(dir_plan, nome)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8-sig") as f:
                return list(csv.DictReader(f, delimiter=";"))
    print(f"[AVISO] CSV de programação de curto prazo não encontrado em {dir_plan}")
    return []


# =============================================================================
# ESCRITA DE CSVs
# =============================================================================

def salvar_csv_utf8_sig(caminho, cabecalho, linhas):
    """
    Grava um arquivo CSV com encoding utf-8-sig e delimitador ';'.
    Padrão mandatório do ecossistema (Manual §3.1).

    Args:
        caminho   : Caminho absoluto do arquivo de saída.
        cabecalho : Lista de strings com os títulos das colunas.
        linhas    : Lista de listas/tuplas com os dados de cada linha.

    Example:
        salvar_csv_utf8_sig(
            "projetos/OBRA_TMULT/06_SST_E_RH/HISTOGRAMA.csv",
            ["Função", "Mês 1", "Mês 2"],
            [["Pedreiro", 2, 3], ["Servente", 4, 5]]
        )
    """
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(cabecalho)
        writer.writerows(linhas)
    print(f"[OK] CSV salvo: {os.path.relpath(caminho, ROOT_DIR)}")


def salvar_json(caminho, dados, indent=2):
    """
    Grava um arquivo JSON com encoding utf-8 e indentação legível.

    Args:
        caminho : Caminho absoluto do arquivo de saída.
        dados   : Objeto Python serializável (dict, list, etc.).
        indent  : Indentação JSON (padrão: 2).
    """
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=indent)
    print(f"[OK] JSON salvo: {os.path.relpath(caminho, ROOT_DIR)}")


def salvar_markdown(caminho, conteudo):
    """
    Grava um arquivo Markdown com encoding utf-8 (padrão do ecossistema).

    Args:
        caminho  : Caminho absoluto do arquivo de saída.
        conteudo : String com o conteúdo Markdown.
    """
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"[OK] MD salvo:  {os.path.relpath(caminho, ROOT_DIR)}")
