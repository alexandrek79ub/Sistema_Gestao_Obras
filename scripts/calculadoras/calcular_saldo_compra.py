#!/usr/bin/env python3
"""
Calcula o saldo a comprar de um item (SKILL_QUANTIFICACAO_PEDIDO_DE_COMPRA, Seção 1) e
sinaliza automaticamente quando um novo pedido excede esse saldo — em vez de deixar o
agente "decidir de cabeça" se um pedido é razoável.

Uso:
    python calcular_saldo_compra.py dados.json

Formato de dados.json:
{
  "item": "Cimento CP-II 50kg",
  "quantidade_orcada": 500,
  "unidade": "saco",
  "pedidos_anteriores": [120, 150, 100],
  "estoque_em_canteiro": 20,
  "novo_pedido_proposto": 150
}
"""
import argparse
import json


def calcular(dados):
    orcado = dados["quantidade_orcada"]
    comprado = sum(dados.get("pedidos_anteriores", []))
    estoque = dados.get("estoque_em_canteiro", 0)
    novo_pedido = dados.get("novo_pedido_proposto")

    saldo_a_comprar = orcado - comprado - estoque

    resultado = {
        "item": dados.get("item"),
        "unidade": dados.get("unidade"),
        "quantidade_orcada": orcado,
        "quantidade_ja_comprada": comprado,
        "estoque_em_canteiro": estoque,
        "saldo_a_comprar": round(saldo_a_comprar, 4),
    }

    if novo_pedido is not None:
        excede = novo_pedido > saldo_a_comprar
        resultado["novo_pedido_proposto"] = novo_pedido
        resultado["excede_saldo"] = excede
        if excede:
            resultado["nivel_confianca"] = "🟡"
            resultado["alerta"] = (
                f"Pedido de {novo_pedido} {dados.get('unidade', '')} excede o saldo "
                f"a comprar de {round(saldo_a_comprar, 4)}. Pode ser compra antecipada "
                f"legítima (preço, prazo de entrega) ou erro — confirmar com humano "
                f"antes de processar (SKILL_QUANTIFICACAO_PEDIDO_DE_COMPRA, Seção 1)."
            )
        elif saldo_a_comprar <= 0:
            resultado["nivel_confianca"] = "🔴"
            resultado["alerta"] = (
                "Saldo a comprar já é zero ou negativo — este item já foi totalmente "
                "coberto por pedidos anteriores. Novo pedido não tem lastro no "
                "quantitativo orçado."
            )
        else:
            resultado["nivel_confianca"] = "🟢"
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
