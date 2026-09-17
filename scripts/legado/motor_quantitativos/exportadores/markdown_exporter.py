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
        f"**Desenhos de Referência:** {desenho_header}  ",
        f"**Checksum do Quantitativo:** `{checksum}`", 
        "", 
        "---", 
        "", 
        "## 1. Demonstração Matemática Detalhada", 
        "",
        "| EAP | Elemento / Serviço | Qtd Líquida | Unid | Expressão Matemática | Prancha |",
        "| :---: | :--- | :---: | :---: | :--- | :--- |"
    ]
    
    # Tabela compacta dos itens com fórmulas
    for r in itens_lista:
        rotulo_desenho = extrair_rotulo_desenho(r.get("prancha_referencia", ""))
        desc = r['descricao']
        elem = r.get('element_id')
        if elem and elem not in desc:
            desc = f"{elem} — {desc}"
        expr = r.get('expressao_matematica', '')
        linhas.append(f"| {r['cod_eap']} | {desc} | {r['quantidade_liquida']} | {r['unidade']} | `{expr}` | {rotulo_desenho} |")
        
    linhas.extend([
        "",
        "---",
        "",
        "## 2. Tabela Consolidada de Serviços (EAP)", 
        "", 
        "| EAP | Pacote de Serviço | Total Líquido | Unid | Status |", 
        "| :---: | :--- | :---: | :---: | :---: |"
    ])
    
    # Consolidação por código EAP
    totais_eap = {}
    for r in itens_lista:
        cod = r['cod_eap']
        unid = r['unidade']
        st = r.get('status', 'LEVANTADO')
        # Nome base do serviço
        nome_servico = r['descricao']
        if " — " in nome_servico:
            nome_servico = nome_servico.split(" — ")[0]
        if cod not in totais_eap:
            totais_eap[cod] = {
                "nome": nome_servico,
                "unidade": unid,
                "total": 0.0,
                "status": st
            }
        totais_eap[cod]["total"] += float(r.get('quantidade_liquida', 0.0) or 0.0)

    for cod in sorted(totais_eap.keys()):
        d = totais_eap[cod]
        linhas.append(f"| **{cod}** | {d['nome']} | **{d['total']:.2f}** | {d['unidade']} | {d['status']} |")
        
    linhas.append("")
    
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(linhas), encoding="utf-8")

