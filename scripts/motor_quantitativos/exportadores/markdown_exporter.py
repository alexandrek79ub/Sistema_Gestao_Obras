from pathlib import Path
from typing import Any, Iterable

def escrever_memoria_calculo(destino: Path, obra_nome: str, checksum: str, disciplina: str, grupo: Iterable[dict[str, Any]]) -> None:
    linhas = [
        f"# Memória de Cálculo Auditável: {disciplina}", 
        "", 
        f"**Obra:** {obra_nome}  ", 
        f"**Checksum do quantitativo:** `{checksum}`", 
        "", 
        "---", 
        "", 
        "## 1. Demonstração Matemática Detalhada", 
        ""
    ]
    
    for r in grupo:
        linhas.extend([
            f"### {r['cod_eap']} — {r['descricao']}", 
            f"- **Expressão:** `{r['expressao_matematica']}`", 
            f"- **Resultado líquido:** `{r['quantidade_liquida']} {r['unidade']}`", 
            f"- **Prancha:** `{r['prancha_referencia']}`", 
            f"- **Regra:** `{r.get('rule_id', '')}` v{r.get('rule_version', 0)}",
            f"- **CIA/Elemento:** `{r.get('cia', '')}` / `{r.get('element_id', '')}`",
            f"- **Evidências:** `{r.get('evidence_json', '[]')}`",
            ""
        ])
        
    linhas.extend([
        "## 2. Tabela Consolidada de Quantitativos Físicos de Projeto", 
        "", 
        "| EAP | Serviço | Quantidade líquida | Unidade | Prancha | Status |", 
        "|---|---|---:|---|---|---|"
    ])
    
    linhas.extend(
        f"| {r['cod_eap']} | {r['descricao']} | {r['quantidade_liquida']} | {r['unidade']} | {r['prancha_referencia']} | {r['status']} |" 
        for r in grupo
    )
    
    linhas.extend([
        "", 
        "## 3. Tabela Oficial de Serviços para EAP e Cronograma", 
        "", 
        "| EAP | Serviço | Status |", 
        "|---|---|---|"
    ])
    
    linhas.extend(
        f"| {r['cod_eap']} | {r['descricao']} | {r['status']} |" 
        for r in grupo
    )
    linhas.append("")
    
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(linhas), encoding="utf-8")
