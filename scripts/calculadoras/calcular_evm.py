#!/usr/bin/env python3
"""
Calcula SPI, CPI e EAC (3 cenários) usando as fórmulas padrão do PMI — determinístico,
nunca "estimado" pela LLM. Aplica a regra da SKILL_GESTAO_07 de nunca entregar projeção
em número único, sempre em faixa otimista/realista/pessimista, com R² quando houver
série histórica suficiente para regressão.

Uso:
    python calcular_evm.py dados.json

Formato de dados.json:
{
  "bac": 1500000,
  "pv": 600000,
  "ev": 550000,
  "ac": 580000,
  "serie_historica_custo_acumulado": [
    {"periodo": 1, "custo_acumulado": 100000},
    {"periodo": 2, "custo_acumulado": 220000},
    ...
  ]
}
BAC = Orçamento total (Budget At Completion)
PV  = Valor planejado até a data (Planned Value)
EV  = Valor agregado até a data (Earned Value)
AC  = Custo real até a data (Actual Cost)
"""
import argparse
import json


def regressao_linear_simples(pontos):
    """Regressão linear simples (mínimos quadrados) sobre (x, y). Retorna slope, intercept, r2."""
    n = len(pontos)
    if n < 2:
        return None
    xs = [p[0] for p in pontos]
    ys = [p[1] for p in pontos]
    x_media = sum(xs) / n
    y_media = sum(ys) / n

    num = sum((xs[i] - x_media) * (ys[i] - y_media) for i in range(n))
    den = sum((xs[i] - x_media) ** 2 for i in range(n))
    if den == 0:
        return None
    slope = num / den
    intercept = y_media - slope * x_media

    # R²
    ss_tot = sum((y - y_media) ** 2 for y in ys)
    ss_res = sum((ys[i] - (slope * xs[i] + intercept)) ** 2 for i in range(n))
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else None

    return {"slope": slope, "intercept": intercept, "r2": round(r2, 4) if r2 is not None else None}


def calcular(dados):
    bac = dados["bac"]
    pv = dados["pv"]
    ev = dados["ev"]
    ac = dados["ac"]

    spi = round(ev / pv, 4) if pv else None
    cpi = round(ev / ac, 4) if ac else None

    resultado = {
        "bac": bac, "pv": pv, "ev": ev, "ac": ac,
        "spi": spi,
        "cpi": cpi,
        "interpretacao_spi": (
            "Adiantado em relação ao planejado" if spi and spi > 1 else
            "Atrasado em relação ao planejado" if spi and spi < 1 else
            "Exatamente conforme planejado" if spi == 1 else "Não calculável"
        ),
        "interpretacao_cpi": (
            "Gastando menos que o previsto por unidade de trabalho" if cpi and cpi > 1 else
            "Gastando mais que o previsto por unidade de trabalho" if cpi and cpi < 1 else
            "Exatamente conforme orçado" if cpi == 1 else "Não calculável"
        ),
    }

    # EAC método 1: CPI constante (padrão PMI)
    eac_cpi_constante = round(ac + (bac - ev) / cpi, 2) if cpi else None

    # EAC método 2: regressão linear sobre série histórica de custo, se houver dado suficiente
    serie = dados.get("serie_historica_custo_acumulado", [])
    eac_regressao = None
    r2_regressao = None
    if len(serie) >= 4:
        pontos = [(p["periodo"], p["custo_acumulado"]) for p in serie]
        reg = regressao_linear_simples(pontos)
        if reg:
            r2_regressao = reg["r2"]
            # Projeta até o ponto em que custo acumulado atingiria o BAC, de forma simplificada:
            # usa a taxa de gasto por período (slope) para estimar quanto falta gastar.
            taxa_por_periodo = reg["slope"]
            if taxa_por_periodo > 0:
                periodos_restantes_estimados = (bac - ac) / taxa_por_periodo
                eac_regressao = round(ac + taxa_por_periodo * max(periodos_restantes_estimados, 0), 2)

    resultado["eac"] = {
        "metodo_cpi_constante": eac_cpi_constante,
        "metodo_regressao_linear": eac_regressao,
        "r2_regressao": r2_regressao,
        "aviso_r2_baixo": (
            "R² abaixo de 0,5 — tendência pouco confiável, poucos dados ou alta variabilidade."
            if r2_regressao is not None and r2_regressao < 0.5 else None
        ),
        "n_periodos_usados_na_regressao": len(serie),
    }

    # Faixa otimista/realista/pessimista — nunca um número único (SKILL_GESTAO_07, Seção 5)
    candidatos_eac = [v for v in [eac_cpi_constante, eac_regressao] if v is not None]
    if candidatos_eac:
        resultado["faixa_projecao"] = {
            "otimista": min(candidatos_eac),
            "realista": round(sum(candidatos_eac) / len(candidatos_eac), 2),
            "pessimista": max(candidatos_eac),
        }
    else:
        resultado["faixa_projecao"] = None

    return resultado


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dados_json")
    args = ap.parse_args()

    with open(args.dados_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    print(json.dumps(calcular(dados), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
