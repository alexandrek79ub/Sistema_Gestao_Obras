#!/usr/bin/env python3
"""
Calcula caminho crítico (CPM): forward pass, backward pass, e folga de cada atividade.
Algoritmo clássico e determinístico — não deve ser estimado pela LLM.

Uso:
    python calcular_cpm.py dados.json

Formato de dados.json:
{
  "atividades": [
    {"id": "A", "duracao_dias": 5, "predecessoras": []},
    {"id": "B", "duracao_dias": 3, "predecessoras": ["A"]},
    {"id": "C", "duracao_dias": 7, "predecessoras": ["A"]},
    {"id": "D", "duracao_dias": 2, "predecessoras": ["B", "C"]}
  ]
}
"""
import argparse
import json


def calcular_cpm(dados):
    atividades = {a["id"]: a for a in dados["atividades"]}

    # Detecta dependência circular ou predecessora inexistente antes de qualquer cálculo
    for aid, a in atividades.items():
        for pred in a.get("predecessoras", []):
            if pred not in atividades:
                return {
                    "status": "erro",
                    "motivo": f"Atividade '{aid}' referencia predecessora inexistente '{pred}'.",
                }

    # Ordenação topológica simples (Kahn) para detectar ciclo e definir ordem de cálculo
    grau_entrada = {aid: len(a.get("predecessoras", [])) for aid, a in atividades.items()}
    fila = [aid for aid, g in grau_entrada.items() if g == 0]
    ordem = []
    sucessores = {aid: [] for aid in atividades}
    for aid, a in atividades.items():
        for pred in a.get("predecessoras", []):
            sucessores[pred].append(aid)

    fila_local = list(fila)
    while fila_local:
        atual = fila_local.pop(0)
        ordem.append(atual)
        for suc in sucessores[atual]:
            grau_entrada[suc] -= 1
            if grau_entrada[suc] == 0:
                fila_local.append(suc)

    if len(ordem) != len(atividades):
        return {
            "status": "erro",
            "motivo": "Dependência circular detectada — não é possível calcular caminho crítico.",
        }

    # Forward pass: Early Start / Early Finish
    es, ef = {}, {}
    for aid in ordem:
        preds = atividades[aid].get("predecessoras", [])
        es[aid] = max((ef[p] for p in preds), default=0)
        ef[aid] = es[aid] + atividades[aid]["duracao_dias"]

    duracao_total = max(ef.values()) if ef else 0

    # Backward pass: Late Start / Late Finish
    ls, lf = {}, {}
    for aid in reversed(ordem):
        sucs = sucessores[aid]
        lf[aid] = min((ls[s] for s in sucs), default=duracao_total)
        ls[aid] = lf[aid] - atividades[aid]["duracao_dias"]

    resultado_atividades = []
    for aid in ordem:
        folga = round(ls[aid] - es[aid], 4)
        resultado_atividades.append({
            "id": aid,
            "duracao_dias": atividades[aid]["duracao_dias"],
            "es_inicio_mais_cedo": es[aid],
            "ef_fim_mais_cedo": ef[aid],
            "ls_inicio_mais_tarde": ls[aid],
            "lf_fim_mais_tarde": lf[aid],
            "folga_dias": folga,
            "critica": folga == 0,
        })

    caminho_critico = [a["id"] for a in resultado_atividades if a["critica"]]

    return {
        "status": "ok",
        "duracao_total_dias": duracao_total,
        "caminho_critico": caminho_critico,
        "atividades": resultado_atividades,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dados_json")
    args = ap.parse_args()

    with open(args.dados_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    print(json.dumps(calcular_cpm(dados), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
