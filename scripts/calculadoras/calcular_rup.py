#!/usr/bin/env python3
"""
Calcula RUP (Razão Unitária de Produção) cíclica e cumulativa, com as regras de
confiabilidade da SKILL_GESTAO_08 e SKILL_GESTAO_07 aplicadas em código, não deixadas
para o julgamento do agente de IA.

Por que isso é script e não "conta feita pela LLM":
- Divisão e média são determinísticas — não deveriam variar entre duas execuções.
- A regra "3+ períodos consecutivos fora da meta = alerta real" é lógica de contagem,
  não interpretação — fica mais confiável em código do que em texto de prompt.

Uso:
    python calcular_rup.py dados.json

Formato de dados.json esperado:
{
  "meta_rup": 0.85,
  "periodos": [
    {"data": "2026-08-01", "homens_hora": 64, "quantidade_executada": 80},
    {"data": "2026-08-02", "homens_hora": 64, "quantidade_executada": 75},
    ...
  ]
}

Saída: JSON com RUP cíclico por período, RUP cumulativo, e alerta se aplicável.
"""
import argparse
import json
import sys


def calcular(dados):
    meta = dados.get("meta_rup")
    periodos = dados["periodos"]

    if len(periodos) < 5:
        return {
            "status": "dado_insuficiente",
            "motivo": f"Apenas {len(periodos)} período(s) informado(s). "
                      f"SKILL_GESTAO_08 exige no mínimo 5 dias para calcular RUP com confiança.",
            "n_periodos": len(periodos),
        }

    resultados = []
    hh_acumulado = 0.0
    qtd_acumulada = 0.0
    periodos_fora_da_meta_seguidos = 0
    max_sequencia_fora_da_meta = 0

    for p in periodos:
        hh = p["homens_hora"]
        qtd = p["quantidade_executada"]

        if qtd <= 0:
            # Não dá para calcular RUP sem quantidade executada medida (Regra da Trena)
            resultados.append({
                "data": p.get("data"),
                "rup_ciclico": None,
                "motivo": "Quantidade executada é zero ou não informada — RUP não calculado "
                          "(não usar avanço estimado, ver Regra da Trena).",
            })
            continue

        rup_ciclico = round(hh / qtd, 4)
        hh_acumulado += hh
        qtd_acumulada += qtd
        rup_cumulativo = round(hh_acumulado / qtd_acumulada, 4) if qtd_acumulada > 0 else None

        fora_da_meta = meta is not None and rup_ciclico > meta
        if fora_da_meta:
            periodos_fora_da_meta_seguidos += 1
            max_sequencia_fora_da_meta = max(max_sequencia_fora_da_meta, periodos_fora_da_meta_seguidos)
        else:
            periodos_fora_da_meta_seguidos = 0

        resultados.append({
            "data": p.get("data"),
            "rup_ciclico": rup_ciclico,
            "rup_cumulativo": rup_cumulativo,
            "fora_da_meta": fora_da_meta,
        })

    alerta_real = max_sequencia_fora_da_meta >= 3
    rup_cumulativo_final = round(hh_acumulado / qtd_acumulada, 4) if qtd_acumulada > 0 else None

    return {
        "status": "ok",
        "n_periodos": len(periodos),
        "meta_rup": meta,
        "rup_cumulativo_final": rup_cumulativo_final,
        "maior_sequencia_fora_da_meta": max_sequencia_fora_da_meta,
        "alerta_real": alerta_real,
        "interpretacao": (
            "3+ períodos consecutivos fora da meta — problema real, investigar causa "
            "(ver protocolo de correlação x causa da SKILL_GESTAO_07)."
            if alerta_real else
            "Nenhuma sequência de 3+ períodos fora da meta — variação pontual, não "
            "necessariamente um problema estrutural."
        ),
        "detalhe_por_periodo": resultados,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dados_json")
    args = ap.parse_args()

    with open(args.dados_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    resultado = calcular(dados)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
