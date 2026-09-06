#!/usr/bin/env python3
"""
Converte quantidade necessária de aço (kg) em número de barras comerciais fechadas a
comprar, aplicando a regra de UCC da SKILL_QUANTIFICACAO_MASTER (nunca comprar
"quebrado" — sempre arredondar para cima até a unidade comercial fechada).

Por que script e não LLM: peso linear por bitola é tabela fixa (norma), e "arredondar
sempre pra cima" é regra determinística — não deveria variar por interpretação.

Uso:
    python calcular_ucc_aco.py dados.json

Formato de dados.json:
{
  "itens": [
    {"bitola_mm": 10.0, "kg_necessario": 340, "comprimento_barra_m": 12}
  ]
}

Tabela de peso linear (kg/m) por bitola é a padrão comercial brasileira (CA-50/CA-60).
"""
import argparse
import json
import math

# Peso linear padrão (kg/m) por bitola nominal (mm) — CA-50, referência de mercado.
# Se o fornecedor usar norma/tabela diferente, isso deve ser sobrescrito via
# "peso_linear_kg_m" explícito no item de entrada, nunca assumido silenciosamente.
PESO_LINEAR_PADRAO = {
    5.0: 0.154,
    6.3: 0.245,
    8.0: 0.395,
    10.0: 0.617,
    12.5: 0.963,
    16.0: 1.578,
    20.0: 2.466,
    25.0: 3.853,
    32.0: 6.313,
}


def calcular_item(item):
    bitola = item["bitola_mm"]
    kg_necessario = item["kg_necessario"]
    comprimento_barra = item.get("comprimento_barra_m", 12)

    peso_linear = item.get("peso_linear_kg_m") or PESO_LINEAR_PADRAO.get(bitola)
    if peso_linear is None:
        return {
            "bitola_mm": bitola,
            "status": "erro",
            "motivo": f"Bitola {bitola}mm não está na tabela padrão e nenhum "
                      f"'peso_linear_kg_m' foi informado explicitamente. Não é seguro "
                      f"assumir um valor — confirmar com humano.",
        }

    peso_por_barra = round(peso_linear * comprimento_barra, 4)
    barras_exatas = kg_necessario / peso_por_barra
    barras_a_comprar = math.ceil(barras_exatas)  # Regra UCC: sempre arredonda para cima
    kg_efetivamente_comprado = round(barras_a_comprar * peso_por_barra, 2)
    sobra_kg = round(kg_efetivamente_comprado - kg_necessario, 2)
    sobra_pct = round(100 * sobra_kg / kg_necessario, 2) if kg_necessario else None

    return {
        "bitola_mm": bitola,
        "peso_linear_kg_m": peso_linear,
        "comprimento_barra_m": comprimento_barra,
        "peso_por_barra_kg": peso_por_barra,
        "kg_necessario": kg_necessario,
        "barras_a_comprar": barras_a_comprar,
        "kg_efetivamente_comprado": kg_efetivamente_comprado,
        "sobra_kg": sobra_kg,
        "sobra_pct": sobra_pct,
        "alerta_sobra_alta": sobra_pct is not None and sobra_pct > 15,
    }


def calcular(dados):
    resultados = [calcular_item(item) for item in dados["itens"]]
    total_kg_comprado = sum(
        r["kg_efetivamente_comprado"] for r in resultados if r.get("status") != "erro"
    )
    return {
        "itens": resultados,
        "total_kg_efetivamente_comprado": round(total_kg_comprado, 2),
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
