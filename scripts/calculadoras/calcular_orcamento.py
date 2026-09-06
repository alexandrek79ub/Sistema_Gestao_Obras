#!/usr/bin/env python3
"""
Calcula o orçamento a partir do quantitativo (SKILL_QUANTIFICACAO_MASTER) + tabela de
custo unitário (CCU), fazendo o link pelo código CIA — nunca a LLM "lembrando" de qual
custo vai com qual quantidade. Item sem match de CIA na tabela de custo é sinalizado,
nunca estimado.

Uso:
    python calcular_orcamento.py dados.json

Formato de dados.json:
{
  "bdi_pct": 25,
  "quantitativo": [
    {"cia": "02.01.03", "descricao": "Alvenaria de vedação", "quantidade": 145, "unidade": "m2"}
  ],
  "tabela_custo_unitario": [
    {"cia": "02.01.03", "custo_unitario_direto": 68.40, "fonte": "SINAPI 08/2026"}
  ]
}
"""
import argparse
import json


def calcular(dados):
    bdi_pct = dados.get("bdi_pct", 0)
    quantitativo = dados["quantitativo"]
    tabela_custo = {c["cia"]: c for c in dados["tabela_custo_unitario"]}

    itens_orcados = []
    itens_pendentes = []
    total_direto = 0.0

    for q in quantitativo:
        cia = q["cia"]
        custo_info = tabela_custo.get(cia)

        if custo_info is None:
            itens_pendentes.append({
                "cia": cia,
                "descricao": q.get("descricao"),
                "quantidade": q["quantidade"],
                "unidade": q.get("unidade"),
                "motivo": "Nenhum custo unitário cadastrado para este CIA — não pode ser "
                          "orçado automaticamente (SKILL_QUANTIFICACAO_ORCAMENTACAO, Seção 1).",
            })
            continue

        custo_unitario = custo_info["custo_unitario_direto"]
        quantidade = q["quantidade"]
        custo_direto_item = round(quantidade * custo_unitario, 2)
        valor_final_item = round(custo_direto_item * (1 + bdi_pct / 100), 2)

        total_direto += custo_direto_item

        itens_orcados.append({
            "cia": cia,
            "descricao": q.get("descricao"),
            "quantidade": quantidade,
            "unidade": q.get("unidade"),
            "custo_unitario_direto": custo_unitario,
            "fonte_custo": custo_info.get("fonte"),
            "custo_direto_total": custo_direto_item,
            "bdi_pct_aplicado": bdi_pct,
            "valor_final_item": valor_final_item,
        })

    total_final = round(total_direto * (1 + bdi_pct / 100), 2)

    return {
        "bdi_pct": bdi_pct,
        "total_custo_direto": round(total_direto, 2),
        "total_final_com_bdi": total_final,
        "n_itens_orcados": len(itens_orcados),
        "n_itens_pendentes": len(itens_pendentes),
        "itens_orcados": itens_orcados,
        "itens_pendentes_sem_custo": itens_pendentes,
        "alerta": (
            f"⚠️ {len(itens_pendentes)} item(ns) do quantitativo não tem custo unitário "
            f"cadastrado e ficou de fora do total — orçamento está incompleto."
            if itens_pendentes else None
        ),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dados_json")
    args = ap.parse_args()

    with open(args.dados_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    print(json.dumps(calcular(dados), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
