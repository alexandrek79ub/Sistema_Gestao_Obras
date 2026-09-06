#!/usr/bin/env python3
"""
Checa vencimento de documentos de segurança (PGR, PCMSO, LTCAT, ASO, CA de EPI) contra
a janela de alerta definida na SKILL_GESTAO_17 — cálculo de data determinístico, não
deixado para o agente "lembrar" de checar.

Uso:
    python checar_vencimento_documental.py dados.json

Formato de dados.json:
{
  "data_referencia": "2026-08-31",
  "documentos": [
    {"tipo": "PGR", "titular": "Obra Principal", "data_vencimento": "2026-09-10"},
    {"tipo": "ASO", "titular": "Joao Silva", "data_vencimento": "2026-09-05"},
    {"tipo": "CA_EPI", "titular": "Maria Souza - Capacete", "data_vencimento": "2026-07-01"}
  ]
}
"""
import argparse
import json
from datetime import datetime

JANELA_ALERTA_DIAS = {
    "PGR": 30,
    "PCMSO": 30,
    "LTCAT": 30,
    "ASO": 15,
    "CA_EPI": 15,
}


def checar(dados):
    data_ref = datetime.strptime(dados["data_referencia"], "%Y-%m-%d")
    documentos = dados["documentos"]

    vencidos, vencendo, vigentes = [], [], []

    for doc in documentos:
        tipo = doc["tipo"]
        vencimento = datetime.strptime(doc["data_vencimento"], "%Y-%m-%d")
        dias_restantes = (vencimento - data_ref).days
        janela = JANELA_ALERTA_DIAS.get(tipo, 15)  # padrão conservador se tipo não mapeado

        item = {
            "tipo": tipo,
            "titular": doc.get("titular"),
            "data_vencimento": doc["data_vencimento"],
            "dias_restantes": dias_restantes,
        }

        if dias_restantes < 0:
            item["dias_vencido"] = abs(dias_restantes)
            vencidos.append(item)
        elif dias_restantes <= janela:
            vencendo.append(item)
        else:
            vigentes.append(item)

    # Ordena vencidos e vencendo por urgência (mais crítico primeiro)
    vencidos.sort(key=lambda d: -d["dias_vencido"])
    vencendo.sort(key=lambda d: d["dias_restantes"])

    return {
        "data_referencia": dados["data_referencia"],
        "total_documentos": len(documentos),
        "vencidos": vencidos,
        "vencendo": vencendo,
        "total_vigentes": len(vigentes),
        "alerta_geral": (
            f"🔴 {len(vencidos)} documento(s) VENCIDO(S) — ação imediata necessária."
            if vencidos else
            f"🟡 {len(vencendo)} documento(s) vencendo em breve — agendar renovação."
            if vencendo else
            "🟢 Nenhum documento vencido ou vencendo dentro da janela de alerta."
        ),
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
