#!/usr/bin/env python3
"""
Aplica o Portão de Qualidade de Dado (SKILL_GESTAO_07, Seção 1) em código — checagens
de completude, outlier estatístico (IQR) e duplicidade, que não deveriam depender do
"olho" da LLM revisando linha por linha.

Uso:
    python portao_qualidade_dado.py dados.json

Formato de dados.json:
{
  "serie": [
    {"data": "2026-08-01", "valor": 1200, "chave_duplicidade": "2026-08-01|CIA-01"},
    {"data": "2026-08-02", "valor": 1150, "chave_duplicidade": "2026-08-02|CIA-01"},
    ...
  ],
  "dias_uteis_esperados": 20
}
"""
import argparse
import json


def detectar_outliers_iqr(valores):
    """Retorna índices considerados outlier pelo método IQR (1,5x), padrão para
    amostras pequenas — evita métodos que exigem grande volume de dado (SKILL_GESTAO_07)."""
    if len(valores) < 4:
        return []
    ordenados = sorted(valores)
    n = len(ordenados)
    q1 = ordenados[n // 4]
    q3 = ordenados[(3 * n) // 4]
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    return [
        i for i, v in enumerate(valores)
        if v < limite_inferior or v > limite_superior
    ]


def checar(dados):
    serie = dados.get("serie", [])
    dias_uteis_esperados = dados.get("dias_uteis_esperados")

    problemas = []

    # 1. Completude
    if dias_uteis_esperados is not None:
        completude_pct = round(100 * len(serie) / dias_uteis_esperados, 1) if dias_uteis_esperados else None
        if completude_pct is not None and completude_pct < 80:
            problemas.append({
                "tipo": "completude",
                "severidade": "🔴",
                "detalhe": f"Apenas {len(serie)} de {dias_uteis_esperados} dias úteis esperados "
                           f"({completude_pct}%) — abaixo de 80%, análise não confiável.",
            })
        elif completude_pct is not None and completude_pct < 100:
            problemas.append({
                "tipo": "completude",
                "severidade": "🟡",
                "detalhe": f"{completude_pct}% de completude — utilizável, mas mencionar a lacuna "
                           f"no relatório.",
            })

    # 2. Duplicidade
    chaves = [item.get("chave_duplicidade") for item in serie if item.get("chave_duplicidade")]
    duplicadas = set(c for c in chaves if chaves.count(c) > 1)
    if duplicadas:
        problemas.append({
            "tipo": "duplicidade",
            "severidade": "🔴",
            "detalhe": f"{len(duplicadas)} chave(s) duplicada(s) encontrada(s): {sorted(duplicadas)}",
        })

    # 3. Outlier bruto (possível erro de digitação)
    valores = [item["valor"] for item in serie if "valor" in item]
    indices_outlier = detectar_outliers_iqr(valores)
    if indices_outlier:
        detalhes_outlier = [
            {"posicao": i, "data": serie[i].get("data"), "valor": serie[i]["valor"]}
            for i in indices_outlier
        ]
        problemas.append({
            "tipo": "outlier_estatistico",
            "severidade": "🟡",
            "detalhe": "Valor(es) fora do padrão pelo método IQR — pode ser erro de digitação "
                       "ou evento real, exige checagem manual antes de usar na análise.",
            "itens": detalhes_outlier,
        })

    # 4. N mínimo para qualquer projeção (referência da SKILL_GESTAO_07, Seção 4)
    if len(serie) < 5:
        problemas.append({
            "tipo": "amostra_pequena",
            "severidade": "🔴",
            "detalhe": f"Apenas {len(serie)} ponto(s) de dado — insuficiente para qualquer "
                       f"projeção de tendência (mínimo 5, conforme SKILL_GESTAO_07).",
        })

    severidade_maxima = "🟢"
    if any(p["severidade"] == "🔴" for p in problemas):
        severidade_maxima = "🔴"
    elif any(p["severidade"] == "🟡" for p in problemas):
        severidade_maxima = "🟡"

    return {
        "n_registros": len(serie),
        "status_geral": severidade_maxima,
        "aprovado_para_analise": severidade_maxima != "🔴",
        "problemas_encontrados": problemas,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dados_json")
    args = ap.parse_args()

    with open(args.dados_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    print(json.dumps(checar(dados), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
