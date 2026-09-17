"""Pipeline mínimo de quantitativos de fundações.

Contrato:
PDF -> LLM extrai dados/evidências -> JSON -> este script valida/calcula -> SQLite -> CSV/Markdown.

A LLM NÃO envia quantidade calculada nem expressão matemática. Ela só escolhe uma regra
permitida e transcreve os inputs comprovados na prancha.
"""

import argparse
import csv
import json
import math
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


DISCIPLINA = "Infraestrutura e Fundações"
STATUS_OK = "LEVANTADO"
STATUS_RFI = "PENDENTE_RFI"


@dataclass(frozen=True)
class Regra:
    cod_eap: str
    descricao: str
    unidade: str
    obrigatorios: tuple[str, ...]
    calcular: Callable[[dict[str, float]], float]
    expressao: Callable[[dict[str, float]], str]


def _q(d: dict[str, float]) -> float:
    return d.get("quantidade", 1.0)


REGRAS: dict[str, Regra] = {
    "FUN.SAPATA.CONCRETO.V1": Regra(
        "1.3.9", "Concreto estrutural — sapata", "m³",
        ("largura_m", "comprimento_m", "altura_m"),
        lambda d: d["largura_m"] * d["comprimento_m"] * d["altura_m"] * _q(d),
        lambda d: f'{d["largura_m"]} * {d["comprimento_m"]} * {d["altura_m"]} * {_q(d)}',
    ),
    "FUN.SAPATA.FORMA.V1": Regra(
        "1.3.7", "Fôrmas — sapata", "m²",
        ("largura_m", "comprimento_m", "altura_m"),
        lambda d: 2 * (d["largura_m"] + d["comprimento_m"]) * d["altura_m"] * _q(d),
        lambda d: f'2 * ({d["largura_m"]} + {d["comprimento_m"]}) * {d["altura_m"]} * {_q(d)}',
    ),
    "FUN.PEDESTAL.CONCRETO.V1": Regra(
        "1.3.9", "Concreto estrutural — pedestal", "m³",
        ("largura_m", "comprimento_m", "altura_m"),
        lambda d: d["largura_m"] * d["comprimento_m"] * d["altura_m"] * _q(d),
        lambda d: f'{d["largura_m"]} * {d["comprimento_m"]} * {d["altura_m"]} * {_q(d)}',
    ),
    "FUN.PEDESTAL.FORMA.V1": Regra(
        "1.3.7", "Fôrmas — pedestal", "m²",
        ("largura_m", "comprimento_m", "altura_m"),
        lambda d: 2 * (d["largura_m"] + d["comprimento_m"]) * d["altura_m"] * _q(d),
        lambda d: f'2 * ({d["largura_m"]} + {d["comprimento_m"]}) * {d["altura_m"]} * {_q(d)}',
    ),
    "FUN.BLOCO.CONCRETO.V1": Regra(
        "1.3.9", "Concreto estrutural — bloco", "m³",
        ("largura_m", "comprimento_m", "altura_m"),
        lambda d: d["largura_m"] * d["comprimento_m"] * d["altura_m"] * _q(d),
        lambda d: f'{d["largura_m"]} * {d["comprimento_m"]} * {d["altura_m"]} * {_q(d)}',
    ),
    "FUN.BLOCO.FORMA.V1": Regra(
        "1.3.7", "Fôrmas — bloco", "m²",
        ("largura_m", "comprimento_m", "altura_m"),
        lambda d: 2 * (d["largura_m"] + d["comprimento_m"]) * d["altura_m"] * _q(d),
        lambda d: f'2 * ({d["largura_m"]} + {d["comprimento_m"]}) * {d["altura_m"]} * {_q(d)}',
    ),
    "FUN.BALDRAME.CONCRETO.V1": Regra(
        "1.3.9", "Concreto estrutural — viga baldrame", "m³",
        ("largura_m", "altura_m", "comprimento_m"),
        lambda d: d["largura_m"] * d["altura_m"] * d["comprimento_m"] * _q(d),
        lambda d: f'{d["largura_m"]} * {d["altura_m"]} * {d["comprimento_m"]} * {_q(d)}',
    ),
    "FUN.BALDRAME.FORMA_2_FACES.V1": Regra(
        "1.3.7", "Fôrmas — viga baldrame, duas faces", "m²",
        ("altura_m", "comprimento_m"),
        lambda d: 2 * d["altura_m"] * d["comprimento_m"] * _q(d),
        lambda d: f'2 * {d["altura_m"]} * {d["comprimento_m"]} * {_q(d)}',
    ),
    "FUN.ESTACA.CONCRETO.V1": Regra(
        "1.3.9", "Concreto estrutural — estaca", "m³",
        ("diametro_m", "comprimento_m"),
        lambda d: math.pi * (d["diametro_m"] / 2) ** 2 * d["comprimento_m"] * _q(d),
        lambda d: f'pi * ({d["diametro_m"]} / 2)^2 * {d["comprimento_m"]} * {_q(d)}',
    ),
    "FUN.ESTACA.PERFURACAO.V1": Regra(
        "1.3.2", "Perfuração / cravação de estacas", "m",
        ("comprimento_m",),
        lambda d: d["comprimento_m"] * _q(d),
        lambda d: f'{d["comprimento_m"]} * {_q(d)}',
    ),
    "FUN.RADIER.CONCRETO.V1": Regra(
        "1.3.9", "Concreto estrutural — radier", "m³",
        ("area_m2", "espessura_m"),
        lambda d: d["area_m2"] * d["espessura_m"] * _q(d),
        lambda d: f'{d["area_m2"]} * {d["espessura_m"]} * {_q(d)}',
    ),
    "FUN.RADIER.FORMA.V1": Regra(
        "1.3.7", "Fôrmas — borda de radier", "m²",
        ("perimetro_m", "espessura_m"),
        lambda d: d["perimetro_m"] * d["espessura_m"] * _q(d),
        lambda d: f'{d["perimetro_m"]} * {d["espessura_m"]} * {_q(d)}',
    ),
    "FUN.ARMADURA.PESO.V1": Regra(
        "1.3.8", "Armaduras CA-50 / CA-60", "kg",
        ("peso_kg",),
        lambda d: d["peso_kg"] * _q(d),
        lambda d: f'{d["peso_kg"]} * {_q(d)}',
    ),
    "FUN.LASTRO.VOLUME.V1": Regra(
        "1.3.6", "Lastro / regularização", "m³",
        ("area_base_m2", "espessura_m"),
        lambda d: d["area_base_m2"] * d["espessura_m"] * _q(d),
        lambda d: f'{d["area_base_m2"]} * {d["espessura_m"]} * {_q(d)}',
    ),
    "FUN.ESCAVACAO.RETANGULAR.V1": Regra(
        "1.3.4", "Escavação de vala / cava", "m³",
        ("largura_m", "comprimento_m", "profundidade_m"),
        lambda d: d["largura_m"] * d["comprimento_m"] * d["profundidade_m"] * _q(d),
        lambda d: f'{d["largura_m"]} * {d["comprimento_m"]} * {d["profundidade_m"]} * {_q(d)}',
    ),
    "FUN.APILOAMENTO.AREA.V1": Regra(
        "1.3.5", "Apiloamento / preparo de fundo", "m²",
        ("area_m2",),
        lambda d: d["area_m2"] * _q(d),
        lambda d: f'{d["area_m2"]} * {_q(d)}',
    ),
    "FUN.IMPERMEABILIZACAO.AREA.V1": Regra(
        "1.3.11", "Impermeabilização de fundações", "m²",
        ("area_m2",),
        lambda d: d["area_m2"] * _q(d),
        lambda d: f'{d["area_m2"]} * {_q(d)}',
    ),
    "FUN.DRENAGEM.COMPRIMENTO.V1": Regra(
        "1.3.12", "Drenagem perimetral", "m",
        ("comprimento_m",),
        lambda d: d["comprimento_m"] * _q(d),
        lambda d: f'{d["comprimento_m"]} * {_q(d)}',
    ),
}


CAMPOS_PROIBIDOS = {
    "quantidade_liquida", "quantity_net", "resultado", "expressao_matematica",
    "expression", "preco_unitario", "bdi_pct", "custo_total",
}


def _numero_positivo(valor, campo: str) -> float:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"{campo}: deve ser número")
    valor = float(valor)
    if not math.isfinite(valor) or valor <= 0:
        raise ValueError(f"{campo}: deve ser maior que zero")
    return valor


def _validar_evidencia(evidencias: dict, campo: str) -> dict:
    ev = evidencias.get(campo)
    if not isinstance(ev, dict):
        raise ValueError(f"evidência ausente para '{campo}'")
    if not str(ev.get("raw_text", "")).strip():
        raise ValueError(f"evidência '{campo}' sem raw_text")
    if not str(ev.get("region", "")).strip():
        raise ValueError(f"evidência '{campo}' sem region")
    return ev


def validar_e_calcular(documento: dict) -> list[dict]:
    if not isinstance(documento, dict):
        raise ValueError("JSON raiz deve ser um objeto")
    if documento.get("schema_version") != 1:
        raise ValueError("schema_version deve ser 1")
    if str(documento.get("disciplina", "")).upper() != "FUNDACOES":
        raise ValueError("disciplina deve ser FUNDACOES")

    fonte = documento.get("fonte")
    if not isinstance(fonte, dict):
        raise ValueError("fonte é obrigatória")
    for campo in ("arquivo", "revisao", "pagina"):
        if fonte.get(campo) in (None, ""):
            raise ValueError(f"fonte.{campo} é obrigatório")
    if not isinstance(fonte["pagina"], int) or fonte["pagina"] < 1:
        raise ValueError("fonte.pagina deve ser inteiro >= 1")

    medicoes = documento.get("medicoes")
    if not isinstance(medicoes, list) or not medicoes:
        raise ValueError("medicoes deve ser uma lista não vazia")

    saida = []
    for indice, medicao in enumerate(medicoes, start=1):
        if not isinstance(medicao, dict):
            raise ValueError(f"medição {indice}: deve ser objeto")
        proibidos = CAMPOS_PROIBIDOS.intersection(medicao)
        if proibidos:
            raise ValueError(
                f"medição {indice}: campos calculados/proibidos enviados pela LLM: {sorted(proibidos)}"
            )

        elemento = str(medicao.get("elemento", "")).strip()
        rule_id = str(medicao.get("regra_id", "")).strip()
        if not elemento:
            raise ValueError(f"medição {indice}: elemento é obrigatório")
        regra = REGRAS.get(rule_id)
        if not regra:
            raise ValueError(f"medição {indice}: regra_id desconhecida: {rule_id}")

        inputs_raw = medicao.get("inputs")
        evidencias = medicao.get("evidencias")
        if not isinstance(inputs_raw, dict):
            raise ValueError(f"medição {indice}: inputs deve ser objeto")
        if not isinstance(evidencias, dict):
            raise ValueError(f"medição {indice}: evidencias deve ser objeto")

        proibidos_inputs = CAMPOS_PROIBIDOS.intersection(inputs_raw)
        if proibidos_inputs:
            raise ValueError(
                f"medição {indice}: inputs contém campos calculados/proibidos: {sorted(proibidos_inputs)}"
            )

        inputs: dict[str, float] = {}
        for campo in regra.obrigatorios:
            if campo not in inputs_raw:
                raise ValueError(f"medição {indice}: input obrigatório ausente: {campo}")
            inputs[campo] = _numero_positivo(inputs_raw[campo], campo)
            _validar_evidencia(evidencias, campo)

        if "quantidade" in inputs_raw:
            inputs["quantidade"] = _numero_positivo(inputs_raw["quantidade"], "quantidade")
            _validar_evidencia(evidencias, "quantidade")
        else:
            inputs["quantidade"] = 1.0

        resultado = float(regra.calcular(inputs))
        if not math.isfinite(resultado) or resultado < 0:
            raise ValueError(f"medição {indice}: cálculo inválido para {rule_id}")

        pagina = medicao.get("pagina", fonte["pagina"])
        revisao = str(medicao.get("revisao", fonte["revisao"])).strip()
        if not isinstance(pagina, int) or pagina < 1:
            raise ValueError(f"medição {indice}: pagina deve ser inteiro >= 1")
        if not revisao:
            raise ValueError(f"medição {indice}: revisao é obrigatória")

        saida.append({
            "cod_eap": regra.cod_eap,
            "descricao": regra.descricao,
            "disciplina": DISCIPLINA,
            "unidade": regra.unidade,
            "quantidade_liquida": round(resultado, 6),
            "expressao_matematica": regra.expressao(inputs),
            "prancha_referencia": str(fonte["arquivo"]),
            "status": STATUS_OK,
            "observacao": f"página {pagina}",
            "cia": str(medicao.get("cia", "")).strip(),
            "element_type": str(medicao.get("tipo_elemento", "")).strip(),
            "element_id": elemento,
            "rule_id": rule_id,
            "rule_version": 1,
            "evidence_json": json.dumps(evidencias, ensure_ascii=False, sort_keys=True),
            "source_revision": revisao,
        })
    return saida


def escrever_csv(destino: Path, colunas: list[str], linhas: list[tuple]) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(colunas)
        writer.writerows(linhas)


def exportar_arquivos_obra(conn: sqlite3.Connection, obra_id: int) -> list[str]:
    obra = conn.execute("SELECT nome, diretorio_base FROM obras WHERE id=?", (obra_id,)).fetchone()
    if not obra or not obra["diretorio_base"]:
        return []

    base = Path(obra["diretorio_base"])
    itens = conn.execute("""
        SELECT cod_eap,descricao,disciplina,unidade,quantidade_liquida,
               expressao_matematica,prancha_referencia,status,element_id,
               rule_id,source_revision
        FROM itens_quantitativo
        WHERE obra_id=?
        ORDER BY disciplina,cod_eap,prancha_referencia,element_id,rule_id
    """, (obra_id,)).fetchall()
    if not itens:
        return []

    colunas = [
        "COD_EAP", "DESCRICAO_DO_SERVICO", "DISCIPLINA", "UNIDADE",
        "QUANTIDADE_TOTAL", "PRANCHA_REFERENCIA", "STATUS",
    ]
    linhas = [
        (r["cod_eap"], r["descricao"], r["disciplina"], r["unidade"],
         r["quantidade_liquida"], r["prancha_referencia"], r["status"])
        for r in itens
    ]

    csv_path = base / "QUANTITATIVO_MESTRE.csv"
    escrever_csv(csv_path, colunas, linhas)

    md = [
        "# Memória de Cálculo — Quantitativos",
        "",
        f"**Obra:** {obra['nome']}",
        "",
        "| EAP | Elemento | Serviço | Resultado | Unid. | Regra | Expressão | Prancha | Revisão |",
        "|---|---|---|---:|:---:|---|---|---|---|",
    ]
    for r in itens:
        md.append(
            f"| {r['cod_eap']} | {r['element_id']} | {r['descricao']} | "
            f"{r['quantidade_liquida']:.6f} | {r['unidade']} | {r['rule_id']} | "
            f"`{r['expressao_matematica']}` | {Path(r['prancha_referencia']).name} | {r['source_revision']} |"
        )

    md_path = base / "MEMORIA_CALCULO_QUANTITATIVOS.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(md), encoding="utf-8")
    return [str(csv_path), str(md_path)]


def gravar(conn: sqlite3.Connection, obra_id: int, itens: list[dict], prancha: str, sobrescrever: bool) -> int:
    obra = conn.execute("SELECT id FROM obras WHERE id=?", (obra_id,)).fetchone()
    if not obra:
        raise ValueError(f"obra_id {obra_id} não existe no SQLite")

    termo = f"%{Path(prancha).stem}%"
    existente = conn.execute(
        "SELECT COUNT(*) AS n FROM itens_quantitativo WHERE obra_id=? AND prancha_referencia LIKE ?",
        (obra_id, termo),
    ).fetchone()["n"]

    if existente and not sobrescrever:
        raise ValueError(
            f"prancha '{prancha}' já possui {existente} itens; use --sobrescrever para substituir"
        )
    if existente:
        conn.execute(
            "DELETE FROM itens_quantitativo WHERE obra_id=? AND prancha_referencia LIKE ?",
            (obra_id, termo),
        )

    agora = datetime.now(timezone.utc).isoformat()
    cur = conn.execute("""
        INSERT INTO revisoes (obra_id,tipo,usuario,justificativa,origem,created_at)
        VALUES (?, 'QUANTITATIVO', 'pipeline-fundacoes', ?, ?, ?)
    """, (obra_id, f"Processamento validado da prancha {prancha}", f"processar_prancha:{prancha}", agora))
    revisao_id = cur.lastrowid

    for item in itens:
        conn.execute("""
            INSERT INTO itens_quantitativo (
                obra_id,revisao_id,cod_eap,descricao,disciplina,unidade,
                quantidade_liquida,expressao_matematica,prancha_referencia,status,
                observacao,cia,element_type,element_id,rule_id,rule_version,
                evidence_json,source_revision,updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            obra_id, revisao_id, item["cod_eap"], item["descricao"], item["disciplina"],
            item["unidade"], item["quantidade_liquida"], item["expressao_matematica"],
            item["prancha_referencia"], item["status"], item["observacao"], item["cia"],
            item["element_type"], item["element_id"], item["rule_id"], item["rule_version"],
            item["evidence_json"], item["source_revision"], agora,
        ))
    conn.commit()
    return revisao_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida extração da LLM e calcula quantitativos de fundações.")
    parser.add_argument("--obra", type=int, required=True, help="ID da obra no SQLite")
    parser.add_argument("--prancha", required=True, help="Arquivo/código da prancha")
    parser.add_argument("--dados", required=True, help="JSON de evidências produzido pela LLM")
    parser.add_argument("--sobrescrever", action="store_true")
    parser.add_argument("--db", default="data/pmo_virtual.sqlite")
    args = parser.parse_args()

    try:
        documento = json.loads(Path(args.dados).read_text(encoding="utf-8"))
        itens = validar_e_calcular(documento)

        db_path = Path(args.db)
        if not db_path.exists():
            raise ValueError(f"SQLite não encontrado: {db_path}")

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        try:
            revisao_id = gravar(conn, args.obra, itens, args.prancha, args.sobrescrever)
            saidas = exportar_arquivos_obra(conn, args.obra)
        finally:
            conn.close()

        print(f"[OK] {len(itens)} medições validadas e calculadas. Revisão {revisao_id}.")
        for arquivo in saidas:
            print(f"[ARTEFATO] {arquivo}")
    except (OSError, json.JSONDecodeError, ValueError, sqlite3.Error) as exc:
        print(f"[BLOQUEADO] {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
