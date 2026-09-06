#!/usr/bin/env python3
"""
Projeta saldo de caixa por período (desembolsos na data de vencimento, não na data do
serviço — SKILL_GESTAO_09), sempre em 3 cenários, nunca em número único, seguindo a
regra da SKILL_GESTAO_07 de nunca entregar projeção pontual.

Uso:
    python calcular_fluxo_caixa.py dados.json

Formato de dados.json:
{
  "saldo_inicial": 50000,
  "periodos": [
    {
      "periodo": "2026-09",
      "recebimentos_previstos": 200000,
      "probabilidade_atraso_recebimento_pct": 15,
      "desembolsos_previstos": 180000
    }
  ]
}

Cenários:
- Otimista: todos os recebimentos previstos chegam no prazo, desembolsos como previstos.
- Realista: recebimentos ajustados pela probabilidade de atraso informada.
- Pessimista: recebimento do período mais provável de atrasar é adiado 1 período inteiro.
"""
import argparse
import json


def calcular(dados):
    saldo_inicial = dados["saldo_inicial"]
    periodos = dados["periodos"]

    saldo_otimista = saldo_inicial
    saldo_realista = saldo_inicial
    linha_otimista = []
    linha_realista = []

    recebimento_pessimista_adiado = 0.0

    for p in periodos:
        recebimento = p["recebimentos_previstos"]
        desembolso = p["desembolsos_previstos"]
        prob_atraso_pct = p.get("probabilidade_atraso_recebimento_pct", 0)

        # Otimista: tudo entra no prazo
        saldo_otimista += recebimento - desembolso
        linha_otimista.append({"periodo": p["periodo"], "saldo_acumulado": round(saldo_otimista, 2)})

        # Realista: desconta a fração com probabilidade de atraso (fica pro próximo período)
        recebimento_efetivo_realista = recebimento * (1 - prob_atraso_pct / 100)
        saldo_realista += recebimento_efetivo_realista - desembolso
        linha_realista.append({"periodo": p["periodo"], "saldo_acumulado": round(saldo_realista, 2)})

    # Pessimista: combina o desconto de probabilidade do cenário realista COM o atraso
    # de 1 período do recebimento de maior risco — precisa ser sempre igual ou pior que
    # o realista em cada período, nunca melhor (corrigido após teste revelar inconsistência).
    saldo_pessimista = saldo_inicial
    linha_pessimista = []
    atraso_pendente = 0.0
    maior_prob_periodo = max(periodos, key=lambda p: p.get("probabilidade_atraso_recebimento_pct", 0))
    for p in periodos:
        recebimento = p["recebimentos_previstos"]
        desembolso = p["desembolsos_previstos"]
        prob_atraso_pct = p.get("probabilidade_atraso_recebimento_pct", 0)

        # Mesmo desconto permanente do cenário realista (fração que nunca chega)
        recebimento_efetivo = recebimento * (1 - prob_atraso_pct / 100) + atraso_pendente
        atraso_pendente = 0.0

        # Adicionalmente, no período de maior risco, atrasa a parte que "chegaria" 1 período
        if p is maior_prob_periodo and prob_atraso_pct > 0:
            parcela_recebida_no_periodo = recebimento * (1 - prob_atraso_pct / 100)
            atraso_pendente = parcela_recebida_no_periodo
            recebimento_efetivo = 0.0

        saldo_pessimista += recebimento_efetivo - desembolso
        linha_pessimista.append({"periodo": p["periodo"], "saldo_acumulado": round(saldo_pessimista, 2)})

    # Detecta primeiro período com saldo negativo em cada cenário
    def primeiro_negativo(linha):
        for item in linha:
            if item["saldo_acumulado"] < 0:
                return item["periodo"]
        return None

    resultado = {
        "saldo_inicial": saldo_inicial,
        "cenario_otimista": {
            "saldo_final": linha_otimista[-1]["saldo_acumulado"] if linha_otimista else saldo_inicial,
            "primeiro_periodo_negativo": primeiro_negativo(linha_otimista),
            "detalhe": linha_otimista,
        },
        "cenario_realista": {
            "saldo_final": linha_realista[-1]["saldo_acumulado"] if linha_realista else saldo_inicial,
            "primeiro_periodo_negativo": primeiro_negativo(linha_realista),
            "detalhe": linha_realista,
        },
        "cenario_pessimista": {
            "saldo_final": linha_pessimista[-1]["saldo_acumulado"] if linha_pessimista else saldo_inicial,
            "primeiro_periodo_negativo": primeiro_negativo(linha_pessimista),
            "detalhe": linha_pessimista,
        },
    }

    if resultado["cenario_realista"]["primeiro_periodo_negativo"]:
        resultado["alerta"] = (
            f"🔴 No cenário realista, o saldo fica negativo a partir de "
            f"{resultado['cenario_realista']['primeiro_periodo_negativo']} — ação "
            f"corretiva necessária com antecedência (SKILL_GESTAO_09, Seção 3)."
        )
    elif resultado["cenario_pessimista"]["primeiro_periodo_negativo"]:
        resultado["alerta"] = (
            f"🟡 O cenário realista fica positivo, mas o pessimista fica negativo a "
            f"partir de {resultado['cenario_pessimista']['primeiro_periodo_negativo']} — "
            f"risco a monitorar, não crítico ainda."
        )
    else:
        resultado["alerta"] = None

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
