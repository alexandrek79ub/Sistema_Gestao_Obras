import csv
import json
import os
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
obra = "OBRA_TMULT"
obra_dir = os.path.join(ROOT_DIR, "projetos", obra)
plan_dir = os.path.join(obra_dir, "03_PLANEJAMENTO_E_CRONOGRAMA")

curto_prazo_csv = os.path.join(plan_dir, "PROGRAMACAO_CURTO_PRAZO_TMULT.csv")
lob_csv = os.path.join(plan_dir, "LINHA_DE_BALANCO.csv")
config_json_path = os.path.join(obra_dir, "config_obra.json")

with open(config_json_path, "r", encoding="utf-8") as f:
    config_obra = json.load(f)

# Ler curto prazo CSV
rows_cp = []
with open(curto_prazo_csv, mode="r", encoding="utf-8-sig") as f:
    reader = csv.reader(f, delimiter=";")
    header = [c.strip().strip('"') for c in next(reader)]
    for r in reader:
        if not r:
            continue
        item = {header[i]: r[i].strip().strip('"') for i in range(min(len(header), len(r)))}
        rows_cp.append(item)

def extrair_qtd_unidade(meta_fisica, rup_str):
    rup_val = 0.0
    unid_rup = "unid"
    if "HH/" in rup_str or "Hh/" in rup_str:
        parts = re.split(r'HH/|Hh/', rup_str)
        try:
            rup_val = float(parts[0].strip().replace(",", "."))
            unid_rup = parts[1].strip()
        except Exception:
            pass
            
    m = re.search(r'([0-9]+[.,]?[0-9]*)\s*(m²|m³|m|unid|unidades|peças|kg|horas|pontos|circuitos|quadros|bacias)', meta_fisica, re.IGNORECASE)
    qtd = None
    if m:
        try:
            qtd = float(m.group(1).replace(",", "."))
        except Exception:
            pass
            
    if qtd is None:
        qtd = 10.0

    return qtd, unid_rup, rup_val

lotes = []
for idx, r in enumerate(rows_cp):
    cod = r["COD_LOTE"]
    vagao = r["VAGAO_ESTEIRA"]
    num_vagao = vagao.split(":")[0].replace("Vagão", "").strip() if ":" in vagao else "01"
    nome_vagao = vagao.split(":")[1].strip() if ":" in vagao else vagao
    
    hc = int(r["HEADCOUNT_PREVISTO"]) if r["HEADCOUNT_PREVISTO"].isdigit() else 8
    dur = int(r["DURACAO_DIAS"]) if r["DURACAO_DIAS"].isdigit() else 1
    
    qtd, unid, rup = extrair_qtd_unidade(r["META_FISICA"], r["RUP_META_HH_UNID"])
    
    preds = [rows_cp[idx - 1]["COD_LOTE"]] if idx > 0 else []
    
    status = r["STATUS_EXECUCAO"]
    avanco = 100.0 if status == "CONCLUIDO" else 0.0
    
    lote = {
        "id": cod,
        "vagao_id": num_vagao,
        "vagao_nome": nome_vagao,
        "etapa_zona": r["ETAPA_ZONA"],
        "servico": r["SERVICO_LOTE"],
        "meta_fisica": r["META_FISICA"],
        "quantidade": qtd,
        "unidade": unid,
        "rup_hh_unid": rup,
        "headcount": hc,
        "duracao_dias": dur,
        "predecessoras": preds,
        "equipe_prevista": r["EQUIPE_PREVISTA"],
        "equipamentos": r["EQUIPAMENTOS_PREVISTOS"],
        "materiais_ucc": r["MATERIAIS_UCC"],
        "status": status,
        "avanco_pct": avanco,
        "rdo_vinculado": r["RDO_VINCULADO"],
        "data_inicio_base": r["DATA_INICIO"],
        "data_fim_base": r["DATA_FIM"]
    }
    lotes.append(lote)

mestre = {
    "obra": obra,
    "nome_obra": config_obra.get("nome_obra", "TMULT"),
    "sigla_obra": config_obra.get("sigla_obra", "TMULT"),
    "data_inicio_obra": "01/10/2026",
    "regime_trabalho": "6d",
    "jornada_diaria_horas": 8.8,
    "takt_time_alvo_dias": 3,
    "parametros_dimensionamento": {
        "produtividade_calibrada": True,
        "tolerancia_arredondamento": "teto"
    },
    "lotes": lotes
}

saida_json = os.path.join(plan_dir, "planejamento_mestre.json")
with open(saida_json, "w", encoding="utf-8") as f:
    json.dump(mestre, f, indent=2, ensure_ascii=False)

print(f"Sucesso! Gerado {saida_json} com {len(lotes)} lotes unificados.")
