#!/usr/bin/env python3
"""Compilador puro: lê planejamento_mestre.json e só emite artefatos derivados."""
import argparse
import csv
import json
import re
from pathlib import Path


def setores(etapa: str, servico: str = "") -> list[str]:
    texto_etapa = etapa.lower()
    texto_completo = (etapa + " " + servico).lower()
    nomes = {
        "1": "Zona 01 - Recepção/Diretoria",
        "2": "Zona 02 - Salas Técnicas/CPD",
        "3": "Zona 03 - Sanitários e Apoio",
        "4": "Zona 04 - Cobertura e Platibanda",
    }
    # 1. Cobertura e Platibanda explícita
    if any(x in texto_etapa for x in ("cobertura", "platibanda", "telha")):
        return [nomes["4"]]

    # 2. Detecção de Zonas / Etapas numéricas (ex: "Etapa 1 e 2", "Zona 2 e 3", "Etapa 3 e 1")
    zonas = []
    for trecho in re.findall(r"\b(?:etapa|zona|setor|setores)\s*([1-4](?:\s*(?:e|a|,)\s*[1-4])*)", texto_etapa):
        for numero in re.findall(r"[1-4]", trecho):
            nome = nomes[numero]
            if nome not in zonas:
                zonas.append(nome)

    if zonas:
        return zonas

    # 3. Termos setoriais descritivos
    if any(x in texto_completo for x in ("cobertura", "platibanda", "telha")):
        return [nomes["4"]]
    if any(x in texto_completo for x in ("sanitário", "sanitarios", "wc", "copa", "hidrául", "hidraul")):
        return [nomes["3"]]
    if any(x in texto_completo for x in ("cpd", "salas técnicas", "quadro", "qgbt", "qdf")):
        return [nomes["2"]]
    if any(x in texto_completo for x in ("recepção", "recepcao", "diretoria")):
        return [nomes["1"]]

    # 4. Serviços térreos ou de envoltória geral (laje, embutidos, pintura final, turnkey)
    if any(x in texto_completo for x in ("laje", "todos os setores", "toda a edificação", "edifício administrativo", "edificio administrativo", "turnkey", "geral", "térreo", "terreo", "paredes internas", "áreas secas")):
        return [nomes["1"], nomes["2"], nomes["3"]]

    return [nomes["1"]]


def escrever_csv(path: Path, campos: list[str], linhas: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=campos, delimiter=";")
        writer.writeheader()
        writer.writerows(linhas)


def compilar(obra: str) -> None:
    raiz = Path(__file__).resolve().parents[1]
    plano = raiz / "projetos" / obra / "03_PLANEJAMENTO_E_CRONOGRAMA"
    mestre_path = plano / "planejamento_mestre.json"
    mestre = json.loads(mestre_path.read_text(encoding="utf-8"))
    lotes = mestre.get("lotes", [])
    if not lotes:
        raise ValueError("planejamento_mestre.json não contém lotes.")

    curto = []
    lob = []
    cpm = []
    for sequencia, lote in enumerate(lotes, 1):
        inicio = lote.get("data_inicio_formatada", "")
        fim = lote.get("data_fim_formatada", "")
        duracao = lote.get("duracao_dias", 0)
        vagao = f"Vagão {str(lote.get('vagao_id', '')).zfill(2)}: {lote.get('vagao_nome', '')}"
        curto.append({
            "COD_LOTE": lote["id"], "DATA_INICIO": inicio, "DATA_FIM": fim,
            "ETAPA_ZONA": lote.get("etapa_zona", ""), "VAGAO_ESTEIRA": vagao,
            "SERVICO_LOTE": lote.get("servico", ""), "DURACAO_DIAS": duracao,
            "EQUIPE_PREVISTA": lote.get("equipe_prevista", ""),
            "HEADCOUNT_PREVISTO": lote.get("headcount", ""),
            "STATUS_EXECUCAO": lote.get("status", ""), "RDO_VINCULADO": lote.get("rdo_vinculado", ""),
        })

        setores_lote = setores(lote.get("etapa_zona", ""), lote.get("servico", ""))
        for setor in setores_lote:
            equipe = lote.get("equipe_prevista", "")
            if len(setores_lote) > 1:
                sigla_setor = setor.split(" - ")[0]
                equipe = f"{equipe} [{sigla_setor}]"

            lob.append({
                "LOCAL_PAVIMENTO": setor,
                "SEQUENCIA": sequencia,
                "VAGAO": vagao.replace("Vagão ", "").replace(":", ".", 1),
                "ATIVIDADE": lote.get("servico", ""),
                "EQUIPE_RESPONSAVEL": equipe,
                "RITMO_DIAS_POR_LOCAL": max(1, duracao),
                "DATA_INICIO": inicio,
                "DATA_FIM": fim
            })

        cpm.append({"id": lote["id"], "nome": lote.get("servico", lote["id"]),
                    "duracao_dias": duracao,
                    "predecessoras": lote.get("predecessoras", [])})

    if not lob:
        raise ValueError("Nenhum lote possui setor físico inequívoco para a LOB.")
    escrever_csv(plano / f"PROGRAMACAO_CURTO_PRAZO_{obra}.csv", list(curto[0]), curto)
    escrever_csv(plano / f"PROGRAMACAO_CURTO_PRAZO_{obra.replace('OBRA_', '')}.csv", list(curto[0]), curto)
    escrever_csv(plano / "LINHA_DE_BALANCO.csv", list(lob[0]), lob)
    (plano / "dados_cpm.json").write_text(json.dumps({"atividades": cpm}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {len(lotes)} lotes lidos; {len(lob)} pontos LOB emitidos. JSON não alterado.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--obra", required=True)
    compilar(parser.parse_args().obra)
