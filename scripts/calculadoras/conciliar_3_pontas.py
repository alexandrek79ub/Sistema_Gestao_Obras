#!/usr/bin/env python3
"""
Faz o match numérico entre Pedido de Compra (PO) e Nota Fiscal (NF) dentro de
tolerância — SKILL_QUANTIFICACAO_CONCILIACAO_3_PONTAS. Resolve a parte determinística
(a conta bate ou não bate); casos ambíguos (item substituído, múltiplos PO do mesmo
fornecedor) continuam exigindo julgamento humano/agente, não são decididos aqui.

Uso:
    python conciliar_3_pontas.py dados.json

Formato de dados.json:
{
  "tolerancia_preco_pct": 2,
  "pedidos": [
    {"po_id": "PO-001", "fornecedor": "Fornecedor A", "item": "Cimento CP-II 50kg",
     "quantidade": 100, "preco_unitario": 32.50}
  ],
  "notas_fiscais": [
    {"nf_id": "NF-4521", "fornecedor": "Fornecedor A", "item": "Cimento CP-II 50kg",
     "quantidade": 100, "preco_unitario": 32.50, "recebimento_fisico_confirmado": true}
  ]
}
"""
import argparse
import json


def normalizar(texto):
    return (texto or "").strip().lower()


def conciliar_par(po, nf, tolerancia_preco_pct):
    qtd_po = po["quantidade"]
    qtd_nf = nf["quantidade"]
    preco_po = po["preco_unitario"]
    preco_nf = nf["preco_unitario"]

    entrega_parcial = qtd_nf < qtd_po
    saldo_po_restante = round(qtd_po - qtd_nf, 4) if entrega_parcial else 0
    excesso_entrega = qtd_nf > qtd_po

    divergencia_preco_pct = round(100 * abs(preco_nf - preco_po) / preco_po, 2) if preco_po else None
    preco_diverge = divergencia_preco_pct is not None and divergencia_preco_pct > tolerancia_preco_pct

    recebimento_confirmado = nf.get("recebimento_fisico_confirmado", False)

    if not recebimento_confirmado:
        status = "pendente_recebimento_fisico"
        nivel_confianca = "🟡"
    elif preco_diverge:
        status = "divergencia_preco"
        nivel_confianca = "🔴"
    elif entrega_parcial:
        status = "entrega_parcial"
        nivel_confianca = "🟡"
    elif excesso_entrega:
        status = "excesso_entrega"
        nivel_confianca = "🟡"
    else:
        status = "conciliado_total"
        nivel_confianca = "🟢"

    return {
        "po_id": po["po_id"],
        "nf_id": nf["nf_id"],
        "fornecedor": po["fornecedor"],
        "item": po["item"],
        "quantidade_po": qtd_po,
        "quantidade_nf": qtd_nf,
        "saldo_po_restante": saldo_po_restante,
        "preco_po": preco_po,
        "preco_nf": preco_nf,
        "divergencia_preco_pct": divergencia_preco_pct,
        "recebimento_fisico_confirmado": recebimento_confirmado,
        "status": status,
        "nivel_confianca": nivel_confianca,
    }


def conciliar(dados):
    tolerancia = dados.get("tolerancia_preco_pct", 2)
    pedidos = dados.get("pedidos", [])
    notas = dados.get("notas_fiscais", [])

    resultados = []
    nfs_sem_match = []
    pos_usados = set()

    for nf in notas:
        # Candidatos: mesmo fornecedor + mesmo item, PO ainda não totalmente usado
        candidatos = [
            po for po in pedidos
            if normalizar(po["fornecedor"]) == normalizar(nf["fornecedor"])
            and normalizar(po["item"]) == normalizar(nf["item"])
        ]

        if not candidatos:
            nfs_sem_match.append({
                "nf_id": nf["nf_id"],
                "motivo": "Nenhum PO encontrado com mesmo fornecedor+item — cai no fluxo "
                          "de classificação do zero (SKILL_QUANTIFICACAO_PEDIDO_DE_COMPRA).",
            })
            continue

        if len(candidatos) > 1:
            # Múltiplos PO do mesmo fornecedor/item — escolhe o de quantidade mais
            # próxima da NF como melhor candidato, mas sinaliza ambiguidade.
            candidatos.sort(key=lambda po: abs(po["quantidade"] - nf["quantidade"]))
            po_escolhido = candidatos[0]
            ambiguidade = True
        else:
            po_escolhido = candidatos[0]
            ambiguidade = False

        resultado = conciliar_par(po_escolhido, nf, tolerancia)
        if ambiguidade:
            resultado["ambiguidade_multiplos_po"] = True
            resultado["nivel_confianca"] = "🟡" if resultado["nivel_confianca"] == "🟢" else resultado["nivel_confianca"]
            resultado["alerta_ambiguidade"] = (
                f"Havia {len(candidatos)} PO(s) em aberto para o mesmo fornecedor/item — "
                f"escolhido o de quantidade mais próxima. Confirmar manualmente."
            )
        resultados.append(resultado)
        pos_usados.add(po_escolhido["po_id"])

    pos_nunca_atendidos = [
        po for po in pedidos if po["po_id"] not in pos_usados
    ]

    return {
        "conciliacoes": resultados,
        "notas_sem_po_correspondente": nfs_sem_match,
        "pedidos_ainda_sem_nenhuma_entrega": [
            {"po_id": po["po_id"], "item": po["item"], "quantidade": po["quantidade"]}
            for po in pos_nunca_atendidos
        ],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dados_json")
    args = ap.parse_args()

    with open(args.dados_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    print(json.dumps(conciliar(dados), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
