#!/usr/bin/env python3
"""
Detecta se uma frente de serviço mais rápida "alcança" (colide com) a frente
predecessora numa Linha de Balanço — geometria de retas posição×tempo, cálculo
determinístico que o Gantt não revela (SKILL_GESTAO_16, Seção 2 e 6).

Modelo: cada atividade progride pelos pavimentos numa taxa constante (dias por
pavimento). Se a atividade sucessora tem ritmo mais rápido (menos dias/pavimento) que
a predecessora, ela eventualmente alcança e colide — a menos que termine antes.

Uso:
    python detectar_colisao_linha_balanco.py dados.json

Formato de dados.json:
{
  "total_pavimentos": 10,
  "atividades": [
    {
      "id": "Alvenaria",
      "inicio_pavimento_1_dia": 0,
      "ritmo_dias_por_pavimento": 4,
      "predecessora": null
    },
    {
      "id": "Reboco",
      "inicio_pavimento_1_dia": 8,
      "ritmo_dias_por_pavimento": 2.5,
      "predecessora": "Alvenaria",
      "intervalo_minimo_dias": 3
    }
  ]
}
"""
import argparse
import json


def posicao_no_pavimento(atividade, pavimento):
    """Dia em que a atividade conclui o pavimento informado (reta linear)."""
    return atividade["inicio_pavimento_1_dia"] + atividade["ritmo_dias_por_pavimento"] * (pavimento - 1)


def checar_colisao(predecessora, sucessora, total_pavimentos, intervalo_minimo):
    """
    Verifica se em algum pavimento a distância entre sucessora e predecessora fica
    menor que o intervalo mínimo de segurança — indicando colisão de frente.
    """
    pontos_de_risco = []
    for pav in range(1, total_pavimentos + 1):
        dia_pred = posicao_no_pavimento(predecessora, pav)
        dia_suc = posicao_no_pavimento(sucessora, pav)
        # intervalo_real = quantos dias a sucessora está atrás da predecessora naquele
        # pavimento. Positivo e >= intervalo_minimo = seguro. Negativo ou pequeno demais
        # = a sucessora alcançou/ultrapassou a predecessora = colisão.
        intervalo_real = dia_suc - dia_pred
        if intervalo_real < intervalo_minimo:
            pontos_de_risco.append({
                "pavimento": pav,
                "dia_predecessora": round(dia_pred, 2),
                "dia_sucessora": round(dia_suc, 2),
                "intervalo_real_dias": round(intervalo_real, 2),
            })
    return pontos_de_risco


def analisar(dados):
    total_pavimentos = dados["total_pavimentos"]
    atividades = {a["id"]: a for a in dados["atividades"]}

    resultados = []
    for aid, a in atividades.items():
        pred_id = a.get("predecessora")
        if not pred_id:
            continue
        if pred_id not in atividades:
            resultados.append({
                "atividade": aid,
                "status": "erro",
                "motivo": f"Predecessora '{pred_id}' não encontrada.",
            })
            continue

        predecessora = atividades[pred_id]
        intervalo_minimo = a.get("intervalo_minimo_dias", 0)
        pontos_de_risco = checar_colisao(predecessora, a, total_pavimentos, intervalo_minimo)

        resultado = {
            "atividade": aid,
            "predecessora": pred_id,
            "ritmo_atividade_dias_por_pav": a["ritmo_dias_por_pavimento"],
            "ritmo_predecessora_dias_por_pav": predecessora["ritmo_dias_por_pavimento"],
            "mais_rapida_que_predecessora": a["ritmo_dias_por_pavimento"] < predecessora["ritmo_dias_por_pavimento"],
            "colisao_detectada": len(pontos_de_risco) > 0,
        }

        if pontos_de_risco:
            resultado["primeiro_pavimento_com_colisao"] = pontos_de_risco[0]["pavimento"]
            resultado["nivel_confianca"] = "🔴"
            resultado["alerta"] = (
                f"'{aid}' alcança '{pred_id}' a partir do pavimento "
                f"{pontos_de_risco[0]['pavimento']} — intervalo de segurança de "
                f"{intervalo_minimo} dias será violado. Ajustar ritmo, data de início, "
                f"ou intervalo antes de liberar o cronograma."
            )
            resultado["detalhe_pontos_de_risco"] = pontos_de_risco
        else:
            resultado["nivel_confianca"] = "🟢"
            resultado["alerta"] = None

        resultados.append(resultado)

    return {"total_pavimentos": total_pavimentos, "analise_por_atividade": resultados}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dados_json")
    args = ap.parse_args()

    with open(args.dados_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    print(json.dumps(analisar(dados), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
