#!/usr/bin/env python3
"""
Valida a calibração de escala de um PDF vetorial: compara o fator calculado a partir
de uma cota real conhecida contra a escala nominal do carimbo, e sinaliza divergência
acima de 5% — regra que já estava escrita em texto em deteccao_escala.md, mas que
precisa ser aplicada sempre igual, não "lembrada" pelo agente a cada vez.

Uso:
    python validar_escala_pdf.py dados.json

Formato de dados.json:
{
  "escala_nominal": "1:50",
  "cotas_de_referencia": [
    {"descricao": "Parede sala", "valor_real_m": 3.5, "distancia_medida_pdf_pt": 201.6},
    {"descricao": "Parede cozinha", "valor_real_m": 2.8, "distancia_medida_pdf_pt": 161.3}
  ]
}
"""
import argparse
import json


def parse_escala_nominal(texto):
    """Extrai a razão numérica de uma string tipo '1:50' ou '1/50'."""
    texto = texto.replace(" ", "").replace("ESC", "").replace("ESCALA", "").strip(":=")
    for separador in [":", "/"]:
        if separador in texto:
            partes = texto.split(separador)
            try:
                return float(partes[0]) / float(partes[1])
            except (ValueError, ZeroDivisionError, IndexError):
                return None
    return None


def calcular(dados):
    escala_nominal_str = dados.get("escala_nominal")
    razao_nominal = parse_escala_nominal(escala_nominal_str) if escala_nominal_str else None

    cotas = dados.get("cotas_de_referencia", [])
    if not cotas:
        return {
            "status": "sem_cotas",
            "motivo": "Nenhuma cota de referência informada — não é possível calibrar "
                      "com confiança. Escala nominal isolada não é confiável o suficiente "
                      "(deteccao_escala.md, Seção 'Em PDF vetorial').",
        }

    fatores_calculados = []
    for cota in cotas:
        valor_real = cota["valor_real_m"]
        distancia_pdf = cota["distancia_medida_pdf_pt"]
        if distancia_pdf == 0:
            continue
        # fator = metros reais por ponto PDF
        fator = valor_real / distancia_pdf
        fatores_calculados.append({
            "descricao": cota.get("descricao"),
            "fator_m_por_pt": round(fator, 6),
        })

    if not fatores_calculados:
        return {"status": "erro", "motivo": "Nenhuma cota válida (distância zero)."}

    fatores = [f["fator_m_por_pt"] for f in fatores_calculados]
    fator_medio = sum(fatores) / len(fatores)
    variacao_entre_cotas_pct = round(
        100 * (max(fatores) - min(fatores)) / fator_medio, 2
    ) if fator_medio else None

    resultado = {
        "status": "ok",
        "escala_nominal": escala_nominal_str,
        "razao_nominal": razao_nominal,
        "fator_calculado_por_cota": fatores_calculados,
        "fator_medio_m_por_pt": round(fator_medio, 6),
        "variacao_entre_cotas_pct": variacao_entre_cotas_pct,
    }

    if variacao_entre_cotas_pct is not None and variacao_entre_cotas_pct > 5:
        resultado["alerta_inconsistencia_entre_cotas"] = (
            f"As cotas usadas para calibração divergem {variacao_entre_cotas_pct}% entre "
            f"si — pode indicar distorção de escala entre eixos X/Y, ou erro de medição "
            f"em uma das cotas. Calibrar X e Y separadamente (deteccao_escala.md, item 2)."
        )

    # Compara fator médio contra o que a escala nominal implicaria, se a escala nominal
    # tiver uma referência de conversão (aqui assumimos que 1 pt PDF a 72 dpi = 1/72 in,
    # e a escala nominal informa quantos metros reais por unidade de desenho — como o
    # PDF não carrega essa referência de desenho original, este comparativo só é feito
    # quando o chamador fornecer explicitamente o fator nominal esperado).
    fator_nominal_esperado = dados.get("fator_nominal_m_por_pt")
    if fator_nominal_esperado:
        divergencia_pct = round(
            100 * abs(fator_medio - fator_nominal_esperado) / fator_nominal_esperado, 2
        )
        resultado["divergencia_vs_escala_nominal_pct"] = divergencia_pct
        if divergencia_pct > 5:
            resultado["alerta_divergencia_escala"] = (
                f"Fator calculado por cota diverge {divergencia_pct}% da escala nominal "
                f"do carimbo. Prancha provavelmente foi plotada/exportada fora de escala "
                f"— usar o fator calculado por cota, não a escala nominal "
                f"(deteccao_escala.md, item 3: cotas têm prioridade)."
            )

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
