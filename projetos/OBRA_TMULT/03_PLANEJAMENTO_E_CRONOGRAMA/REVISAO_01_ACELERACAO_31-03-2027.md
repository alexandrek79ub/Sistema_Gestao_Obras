# Revisão 01 — Aceleração para 31/03/2027

Data de emissão: 14/09/2026

Esta revisão preserva a Baseline 01 documental, cujo término é 26/04/2027 e
cuja duração é 178 dias úteis. O `dados_cpm.json` passa a representar o plano
operacional revisado, com término em 31/03/2027 e 156 dias úteis.

## Alterações no caminho crítico

| Atividade CPM | Baseline 01 | Revisão 01 |
|---|---:|---:|
| A12_ALVENARIA_VEDACAO | 20 d | 16 d |
| A17_EMBOCO_REBOCO | 14 d | 10 d |
| A22_PISO_PORCELANATO | 14 d | 8 d |
| A25_PINTURA_1A_DEMAO | 5 d | 3 d |
| A26_APARELHOS_HVAC | 6 d | 4 d |
| A27_LOUCAS_METAIS | 6 d | 4 d |
| A28_LUMINARIAS_ESPELHOS | 5 d | 3 d |
| A29_PINTURA_FINAL | 7 d | 4 d |
| A31_LIMPEZA_ENTREGA | 6 d | 5 d |

Os efetivos de cada lote são recalculados pelo motor Takt pela relação
`efetivo revisado = teto(efetivo base × duração base / duração revisada)`.
O histograma oficial é sempre regenerado após a programação de curto prazo.

## Portão de aceite

Esta revisão só é válida após a auditoria dos seis eixos aprovar CPM, Takt,
Linha de Balanço, sincronização CPM x LOB, físico-financeiro e histograma.
