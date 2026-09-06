#!/usr/bin/env python3
"""
Calcula o índice de perda real de um material e compara contra o índice de referência
(SKILL_GESTAO_08, Seção 3.1) — só sinaliza anomalia quando a perda EXCEDE a referência,
nunca trata perda técnica esperada como problema.

Uso:
    python calcular_indice_perda.py dados.json

Formato de dados.json:
{
  "itens": [
    {
      "material": "Bloco cerâmico 14x19x29",
      "quantidade_orcada": 5000,
      "quantidade_comprada": 5400,
      "quantidade_aplicada_medida": 4950,
      "indice_perda_referencia_pct": 8
    }
  ]
}
"""
import argparse
import json


def calcular_item(item):
    orcado = item["quantidade_orcada"]
    comprado = item["quantidade_comprada"]
    aplicado = item["quantidade_aplicada_medida"]
    ref_pct = item.get("indice_perda_referencia_pct")

    if orcado <= 0:
        return {
            "material": item.get("material"),
            "status": "erro",
            "motivo": "Quantidade orçada é zero ou negativa — não é possível calcular índice de perda.",
        }

    perda_absoluta = comprado - aplicado
    indice_perda_real_pct = round(100 * perda_absoluta / orcado, 2)

    resultado = {
        "material": item.get("material"),
        "quantidade_orcada": orcado,
        "quantidade_comprada": comprado,
        "quantidade_aplicada_medida": aplicado,
        "perda_absoluta": round(perda_absoluta, 2),
        "indice_perda_real_pct": indice_perda_real_pct,
        "indice_perda_referencia_pct": ref_pct,
    }

    if ref_pct is not None:
        excesso_pct = round(indice_perda_real_pct - ref_pct, 2)
        resultado["excesso_sobre_referencia_pct"] = excesso_pct
        resultado["anomalia"] = excesso_pct > 0
        if excesso_pct > 0:
            resultado["nivel_confianca"] = "🟡" if excesso_pct <= 5 else "🔴"
            resultado["alerta"] = (
                f"Perda real ({indice_perda_real_pct}%) excede a referência "
                f"({ref_pct}%) em {excesso_pct} pontos percentuais — investigar causa "
                f"(furto, quebra excessiva, erro de medição de aplicação, retrabalho "
                f"não separado — ver SKILL_GESTAO_11)."
            )
        else:
            resultado["nivel_confianca"] = "🟢"
            resultado["alerta"] = None
    else:
        resultado["aviso"] = (
            "Sem índice de referência informado — perda calculada mas não classificada "
            "como anômala ou não. Fornecer referência (TCPO ou histórico próprio) para "
            "análise completa."
        )

    return resultado


def calcular(dados):
    resultados = [calcular_item(item) for item in dados["itens"]]
    anomalias = [r for r in resultados if r.get("anomalia")]
    return {
        "itens": resultados,
        "total_itens": len(resultados),
        "total_anomalias": len(anomalias),
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
