"""Prepara um levantamento quantitativo sem exploração pela LLM.

Este é o único roteador de entrada do Fast Path quantitativo:
LISTA_DE_DESENHOS.csv -> filtra disciplina/serviço -> devolve PDFs a abrir.

Não lê PDFs, carimbos, testes, catálogos ou outras pastas.
"""

import argparse
import csv
import sys
import unicodedata
from pathlib import Path

from gerar_lista_desenhos import exportar_lista


ROTAS = {
    "ALVENARIA": {
        "disciplina": "ARQUITETURA",
        "tipos": ("PLANTA_BAIXA", "CORTE", "ELEVACAO_FACHADA", "PLANTA"),
        "termos_levantados": ("ALVENARIA", "VEDAC"),
    },
    "ARQUITETURA": {
        "disciplina": "ARQUITETURA",
        "tipos": (),
        "termos_levantados": (),
    },
    "FUNDACOES": {
        "disciplina": "FUNDACOES",
        "tipos": ("PLANTA", "IMPLANTACAO_LOCACAO", "FORMA", "ARMADURA", "DETALHAMENTO"),
        "termos_levantados": ("FUND", "SAPATA", "BLOCO", "ESTACA", "BALDRAME"),
    },
    "ESTRUTURA": {
        "disciplina": "ESTRUTURA",
        "tipos": ("FORMA", "ARMADURA", "PLANTA", "DETALHAMENTO"),
        "termos_levantados": ("ESTRUT", "PILAR", "VIGA", "LAJE", "CONCRETO", "FORMA", "ARMADURA"),
    },
    "ELETRICA": {
        "disciplina": "ELETRICA",
        "tipos": ("PLANTA_BAIXA", "PLANTA", "DIAGRAMA_UNIFILAR", "DETALHAMENTO"),
        "termos_levantados": ("ELETR", "ILUMIN", "TOMAD", "SPDA", "ATERR"),
    },
    "HIDRAULICA": {
        "disciplina": "HIDRAULICA",
        "tipos": ("PLANTA_BAIXA", "PLANTA", "ISOMETRICO", "DETALHAMENTO"),
        "termos_levantados": ("HIDRAUL", "ESGOTO", "AGUA", "PLUVIAL", "DREN"),
    },
    "SERVICOS_ESPECIAIS": {
        "disciplina": "SERVICOS_ESPECIAIS",
        "tipos": (),
        "termos_levantados": (),
    },
}

COLUNAS_OBRIGATORIAS = {
    "disciplina_desenho",
    "tipo_desenho",
    "disciplinas_levantadas",
    "servicos_levantados",
    "qtd_itens_quantitativo",
    "arquivo_pdf",
    "status",
}


def norm(valor: str) -> str:
    texto = unicodedata.normalize("NFKD", str(valor or ""))
    return texto.encode("ascii", "ignore").decode("ascii").upper().strip()


def ler_lista(path: Path) -> tuple[list[dict[str, str]], set[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as arq:
        reader = csv.DictReader(arq, delimiter=";")
        campos = set(reader.fieldnames or [])
        return list(reader), campos


def atualizar_se_necessario(obra: str, lista: Path, db: Path) -> list[dict[str, str]]:
    if lista.exists():
        linhas, campos = ler_lista(lista)
        if COLUNAS_OBRIGATORIAS.issubset(campos):
            return linhas

    lista.parent.mkdir(parents=True, exist_ok=True)
    exportar_lista(obra, db, lista.parent)
    linhas, campos = ler_lista(lista)
    faltantes = sorted(COLUNAS_OBRIGATORIAS - campos)
    if faltantes:
        raise ValueError("lista sem colunas obrigatórias: " + ", ".join(faltantes))
    return linhas


def ja_levantado(linha: dict[str, str], rota: dict) -> bool:
    if int(str(linha.get("qtd_itens_quantitativo") or "0").strip() or 0) <= 0:
        return False
    termos = rota["termos_levantados"]
    if not termos:
        return False
    servicos = norm(linha.get("servicos_levantados", ""))
    return any(termo in servicos for termo in termos)


def selecionar(linhas: list[dict[str, str]], rota: dict) -> list[dict[str, str]]:
    candidatos = []
    for linha in linhas:
        if norm(linha.get("status")) != "VIGENTE":
            continue
        if norm(linha.get("disciplina_desenho")) != rota["disciplina"]:
            continue
        if ja_levantado(linha, rota):
            continue
        candidatos.append(linha)

    tipos = rota["tipos"]
    if not tipos:
        return candidatos

    preferidos = [l for l in candidatos if norm(l.get("tipo_desenho")) in tipos]
    return preferidos or candidatos


def main() -> int:
    parser = argparse.ArgumentParser(description="Seleciona pranchas do Fast Path quantitativo.")
    parser.add_argument("--obra", required=True, help="Código/pasta da obra, ex.: OBRA_PORTO")
    parser.add_argument("--servico", required=True, help="ALVENARIA, FUNDACOES, ESTRUTURA, ELETRICA, HIDRAULICA...")
    parser.add_argument("--db", type=Path, default=Path("data/pmo_virtual.sqlite"))
    parser.add_argument("--lista", type=Path)
    args = parser.parse_args()

    servico = norm(args.servico).replace(" ", "_")
    rota = ROTAS.get(servico)
    if not rota:
        print(f"ERRO|SERVICO_NAO_MAPEADO|{servico}", file=sys.stderr)
        return 2

    lista = args.lista or Path("projetos") / args.obra / "01_ENGENHARIA_E_PROJETOS" / "LISTA_DE_DESENHOS.csv"

    try:
        linhas = atualizar_se_necessario(args.obra, lista, args.db)
        selecionadas = selecionar(linhas, rota)
    except Exception as exc:
        print(f"ERRO|{exc}", file=sys.stderr)
        return 2

    if not selecionadas:
        print("NENHUMA_PRANCHA_PENDENTE")
        return 0

    for linha in selecionadas:
        print(
            "ABRIR|"
            + str(linha.get("tipo_desenho", ""))
            + "|"
            + str(linha.get("arquivo_pdf", ""))
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
