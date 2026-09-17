import re
from pathlib import Path
from typing import Any, Iterable

def extrair_rotulo_desenho(ref: str) -> str:
    if not ref:
        return ""
    nome = Path(ref).name
    m_num = re.search(r"EGS-(\d+)", nome, re.IGNORECASE)
    num_curto = f"Desenho {m_num.group(1)}" if m_num else ""
    m_cod = re.search(r"^(.*?)(?:\s+rev\.?([A-Za-z0-9]+))?(?:\.pdf)?$", nome, re.IGNORECASE)
    cod = m_cod.group(1).strip() if m_cod else nome
    rev = f" — Rev. {m_cod.group(2).upper()}" if m_cod and m_cod.group(2) else ""
    if num_curto and cod != num_curto:
        return f"{cod}{rev} ({num_curto})"
    return f"{cod}{rev}"

def escrever_memoria_calculo(destino: Path, obra_nome: str, checksum: str, disciplina: str, grupo: Iterable[dict[str, Any]]) -> None:
    itens_lista = list(grupo)
    desenhos_unicos = sorted({extrair_rotulo_desenho(r.get("prancha_referencia", "")) for r in itens_lista if r.get("prancha_referencia")})
    desenho_header = ", ".join(desenhos_unicos) if desenhos_unicos else "Não especificado"

    linhas = [
        f"# Memória de Cálculo Auditável: {disciplina}", 
        "", 
        f"**Obra:** {obra_nome}  ", 
        f"**Número do Desenho:** {desenho_header}  ",
        f"**Checksum do quantitativo:** `{checksum}`", 
        "", 
        "---", 
        "", 
        "## 1. Demonstração Matemática Detalhada", 
        ""
    ]
    
    for r in itens_lista:
        rotulo_desenho = extrair_rotulo_desenho(r.get("prancha_referencia", ""))
        linhas.extend([
            f"### {r['cod_eap']} — {r['descricao']}", 
            f"- **Número do Desenho:** {rotulo_desenho}",
            f"- **Expressão:** `{r['expressao_matematica']}`", 
            f"- **Resultado líquido:** `{r['quantidade_liquida']} {r['unidade']}`", 
            f"- **Prancha / Arquivo:** `{r['prancha_referencia']}`",
        ])
        if r.get("observacao"):
            linhas.append(f"- **Observação / Auditoria:** {r['observacao']}")
        if r.get("cia"):
            linhas.append(f"- **CIA/Ambiente:** `{r['cia']}`")
        if r.get("element_id"):
            linhas.append(f"- **Elemento:** `{r['element_id']}`")
        linhas.append("")
        
    linhas.extend([
        "## 2. Tabela Consolidada de Quantitativos Físicos de Projeto", 
        "", 
        "| EAP | Serviço | Quantidade líquida | Unidade | Número do Desenho | Status |", 
        "|---|---|---:|---|---|---|"
    ])
    
    linhas.extend(
        f"| {r['cod_eap']} | {r['descricao']} | {r['quantidade_liquida']} | {r['unidade']} | {extrair_rotulo_desenho(r.get('prancha_referencia', ''))} | {r['status']} |" 
        for r in itens_lista
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
        for r in itens_lista
    )
    linhas.append("")
    
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(linhas), encoding="utf-8")
