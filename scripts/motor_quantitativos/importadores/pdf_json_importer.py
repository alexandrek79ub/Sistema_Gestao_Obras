import json
from pathlib import Path

from motor_quantitativos.calculo.avaliador_expressoes import calcular_expressao
from motor_quantitativos.repositorio.sqlite_repository import (
    connect, garantir_obra, gravar_orcamento, substituir_quantitativos
)
from motor_quantitativos.auditoria.trilha_revisoes import registrar_revisao
from motor_quantitativos.exportadores import exportar_artefatos


def importar_json_inicial(json_path: str, db_path: str, substituir: bool = False) -> list[Path]:
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    projeto = data.get("projeto", "OBRA_NAO_NOMEADA")
    obra_codigo = projeto.upper().replace(" ", "_")
    base_dir = str(Path(data.get("base_dir", Path(json_path).parent)).resolve())
    itens, itens_orcamento = [], []
    
    for disciplina, bloco in data.get("disciplinas", {}).items():
        for item in bloco.get("itens_orcamento", []):
            expressoes = item.get("equacoes", [])
            prancha = item.get("ref_prancha", bloco.get("pranchas_ref", ""))
            itens.append({
                "cod_eap": item["codigo_eap"], "descricao": item["descricao"],
                "disciplina": bloco.get("titulo", disciplina), "unidade": item["unidade"],
                "quantidade_liquida": sum(calcular_expressao(e["expressao_matematica"]) for e in expressoes),
                "expressao_matematica": " + ".join(e["expressao_matematica"] for e in expressoes) or "0",
                "prancha_referencia": prancha, "status": item.get("status", "LEVANTADO"),
                "observacao": "Importação inicial do JSON; a partir desta revisão, SQLite é a fonte oficial.",
            })
            itens_orcamento.append({
                "cod_eap": item["codigo_eap"], "prancha_referencia": prancha,
                "preco_unitario": item.get("preco_unitario", 0), "bdi_pct": item.get("bdi_pct", 0),
                "centro_custo": item.get("centro_custo", ""), "codigo_sinapi": item.get("codigo_sinapi", ""),
                "fonte_preco": item.get("fonte_preco", ""),
            })
            
    db = connect(db_path)
    try:
        obra_id = garantir_obra(db, obra_codigo, projeto, base_dir)
        existentes = db.execute("SELECT COUNT(*) FROM itens_quantitativo WHERE obra_id=?", (obra_id,)).fetchone()[0]
        if existentes and not substituir:
            raise ValueError("A obra já possui dados no SQLite. Use --substituir somente para uma reimportação aprovada.")
        if existentes and substituir:
            db.execute("DELETE FROM itens_orcamento WHERE obra_id=?", (obra_id,))
            db.execute("DELETE FROM itens_quantitativo WHERE obra_id=?", (obra_id,))
        
        revisao_quant = registrar_revisao(db, obra_id, "QUANTITATIVO", f"importacao-inicial:{json_path}", "motor-python", "Importação inicial autorizada")
        substituir_quantitativos(db, obra_id, itens, revisao_quant)
        
        revisao_orc = registrar_revisao(db, obra_id, "ORCAMENTO", f"importacao-inicial:{json_path}", "motor-python", "Orçamento importado junto ao levantamento inicial")
        gravar_orcamento(db, obra_id, itens_orcamento, revisao_orc)
        
        saidas = exportar_artefatos(db, obra_id)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
        
    return saidas
