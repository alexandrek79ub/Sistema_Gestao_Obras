"""Importa o registro mestre de desenhos e gera suas exportações derivadas.

O SQLite é a fonte de verdade. JSON de carimbos é somente a entrada de extração e
CSV/Markdown são produzidos por consulta ao banco após a importação.
"""

import argparse
import csv
import hashlib
import json
import re
import sqlite3
import sys
import unicodedata

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def agora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect(path: str | Path) -> sqlite3.Connection:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(path))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("PRAGMA journal_mode = WAL")
    return db


def garantir_obra(db: sqlite3.Connection, codigo: str, nome: str, diretorio_base: str = "") -> int:
    instante = agora()
    db.execute(
        "INSERT INTO obras(codigo,nome,diretorio_base,created_at,updated_at) VALUES(?,?,?,?,?) "
        "ON CONFLICT(codigo) DO UPDATE SET nome=excluded.nome, "
        "diretorio_base=CASE WHEN excluded.diretorio_base <> '' THEN excluded.diretorio_base ELSE obras.diretorio_base END, "
        "updated_at=excluded.updated_at",
        (codigo, nome, diretorio_base, instante, instante),
    )
    return int(db.execute("SELECT id FROM obras WHERE codigo=?", (codigo,)).fetchone()[0])



def caminho_relativo(path: str | Path, raiz: Path) -> str:
    """Mantém caminhos portáveis, relativos à pasta de engenharia quando possível."""
    candidato = Path(path)
    try:
        return candidato.resolve().relative_to(raiz.resolve()).as_posix()
    except ValueError:
        return candidato.as_posix()


def hash_arquivo(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            digest.update(bloco)
    return digest.hexdigest()


def normalizar_referencia_prancha(valor: str) -> str:
    """Normaliza o nome-base para cruzar lista de desenhos e quantitativos."""
    nome = Path(str(valor).strip()).stem
    return unicodedata.normalize("NFKC", nome).casefold().strip()


def normalizar_revisao(valor: str) -> tuple[str, int, str] | None:
    """Normaliza revisões numéricas ou alfabéticas sem comparar famílias distintas."""
    revisao = re.sub(r"^\s*(?:rev(?:is[aã]o)?\.?\s*)", "", valor, flags=re.IGNORECASE).strip().upper()
    if re.fullmatch(r"\d+", revisao):
        return (str(int(revisao)), int(revisao), "NUMERICA")
    if re.fullmatch(r"[A-Z]+", revisao):
        ordem = 0
        for letra in revisao:
            ordem = ordem * 26 + (ord(letra) - ord("A") + 1)
        return (revisao, ordem, "ALFABETICA")
    return None


def extrair_codigo_revisao(nome_pdf: str, texto_carimbo: str) -> tuple[str, str]:
    nome = Path(nome_pdf).stem
    correspondencia = re.search(r"^(?P<codigo>.+?)\s+rev\.?\s*(?P<revisao>[A-Za-z0-9]+)$", nome, re.IGNORECASE)
    if correspondencia:
        return correspondencia.group("codigo").strip(), correspondencia.group("revisao").upper()
    correspondencia = re.search(r"^(?P<codigo>.+?)_(?P<revisao>\d+)$", nome)
    if correspondencia:
        return correspondencia.group("codigo").strip(), correspondencia.group("revisao")
    revisao_texto = re.search(r"\brev(?:is[aã]o)?\.?\s*[:\-]?\s*([A-Za-z0-9]+)\b", texto_carimbo, re.IGNORECASE)
    return nome, revisao_texto.group(1).upper() if revisao_texto else "DESCONHECIDA"


def classificar_desenho(titulo: str, texto_carimbo: str, arquivo_pdf: str) -> tuple[str, str]:
    """Classifica disciplina e tipo uma única vez na geração da lista.

    A classificação é conservadora: quando os metadados não sustentam uma decisão,
    retorna INDEFINIDA em vez de inventar.
    """
    bruto = " ".join([str(titulo or ""), str(texto_carimbo or ""), str(arquivo_pdf or "")])
    texto = unicodedata.normalize("NFKD", bruto).encode("ascii", "ignore").decode("ascii").upper()

    regras_disciplina = [
        ("ELETRICA", r"\b(ELETRIC|ILUMINAC|TOMAD|QDC|QUADRO DE DISTRIB|SPDA|ATERRAMENTO|UNIFILAR|DIAGRAMA ELETR)"),
        ("HIDRAULICA", r"\b(HIDRAUL|SANITAR|ESGOTO|AGUA FRIA|AGUA QUENTE|PLUVIAL|DRENAGEM|ISOMETR|PRUMADA|INCENDIO|GAS)"),
        ("FUNDACOES", r"\b(FUNDAC|SAPATA|BLOCO DE COROAMENTO|ESTACA|BROCA|BALDRAME|LOCACAO DE FUND)"),
        ("ESTRUTURA", r"\b(ESTRUT|FORMA|ARMADURA|PILAR|VIGA|LAJE|CONCRETO ARMADO|DETALHE DE ACO)"),
        ("ARQUITETURA", r"\b(ARQUITET|PLANTA BAIXA|PAVIMENTO|ALVENARIA|VEDAC|FACHADA|CORTE|COBERTURA|ESQUADRIA|LAYOUT)"),
        ("SERVICOS_ESPECIAIS", r"\b(HVAC|AR CONDICIONADO|CLIMATIZ|ELEVADOR|PAISAGIS|PAVIMENTACAO|URBANIZACAO|CANTEIRO)"),
    ]
    disciplina = "INDEFINIDA"
    for nome, padrao in regras_disciplina:
        if re.search(padrao, texto):
            disciplina = nome
            break

    regras_tipo = [
        ("PLANTA_BAIXA", r"\bPLANTA BAIXA\b"),
        ("CORTE", r"\bCORTE[S]?\b"),
        ("ELEVACAO_FACHADA", r"\b(ELEVACAO|FACHADA)\b"),
        ("IMPLANTACAO_LOCACAO", r"\b(IMPLANTACAO|LOCACAO)\b"),
        ("COBERTURA", r"\bCOBERTURA\b"),
        ("FORMA", r"\bFORMA[S]?\b"),
        ("ARMADURA", r"\b(ARMADURA|FERRAGEM|ACO)\b"),
        ("ISOMETRICO", r"\bISOMETR"),
        ("DIAGRAMA_UNIFILAR", r"\b(UNIFILAR|DIAGRAMA)\b"),
        ("DETALHAMENTO", r"\b(DETALHE|DETALHAMENTO)\b"),
        ("PLANTA", r"\bPLANTA\b"),
    ]
    tipo = "INDEFINIDO"
    for nome, padrao in regras_tipo:
        if re.search(padrao, texto):
            tipo = nome
            break
    return disciplina, tipo


def limpar_titulo(texto_carimbo: str) -> tuple[str, str]:
    """Extrai um título candidato; ausência de sinal claro permanece pendente."""
    if any(ord(caractere) < 32 and caractere not in "\n\r\t" for caractere in texto_carimbo):
        return "Título não identificado", "PENDENTE_REVISAO"
    texto = re.sub(r"[\x00-\x1f]+", " ", texto_carimbo)
    linhas = [re.sub(r"\s+", " ", linha).strip(" -:|") for linha in texto.splitlines()]
    linhas = [linha for linha in linhas if linha]
    rotulo = re.compile(r"(?:t[ií]tulo|title|nome do desenho)\s*[:\-]?\s*(.+)", re.IGNORECASE)
    for linha in linhas:
        achado = rotulo.search(linha)
        if achado and len(achado.group(1).strip()) >= 4:
            return achado.group(1).strip(), "EXTRAIDO"

    candidatas = [
        linha for linha in linhas
        if 8 <= len(linha) <= 180
        and not re.search(r"\brev(?:is[aã]o)?\b|escala|data|folha|sheet|projeto|cliente", linha, re.IGNORECASE)
        and not (re.fullmatch(r"[A-Z0-9._\-/ ]+", linha) and re.search(r"\d|[-_./]", linha))
    ]
    if candidatas:
        return max(candidatas, key=len), "EXTRAIDO"
    return "Título não identificado", "PENDENTE_REVISAO"


def registrar_auditoria(db: Any, obra_id: int, desenho_id: int, acao: str, antes: dict[str, Any] | None,
                       depois: dict[str, Any], justificativa: str) -> None:
    db.execute(
        "INSERT INTO auditoria_eventos(obra_id,entidade,entidade_id,acao,antes_json,depois_json,usuario,justificativa,created_at) "
        "VALUES(?,?,?,?,?,?,?,?,?)",
        (obra_id, "lista_desenhos", desenho_id, acao, json.dumps(antes or {}, ensure_ascii=False),
         json.dumps(depois, ensure_ascii=False), "importador-lista-desenhos", justificativa, agora()),
    )


def definir_status_revisao(db: Any, obra_id: int, codigo: str, revisao: str,
                           tipo: str, ordem: int | None) -> str:
    """Define vigência sem assumir equivalência entre padrões de revisão distintos."""
    existentes = db.execute(
        "SELECT id,revisao,revisao_tipo,revisao_ordem,status FROM lista_desenhos "
        "WHERE obra_id=? AND codigo=? AND revisao<>?", (obra_id, codigo, revisao)
    ).fetchall()
    if ordem is None:
        return "PENDENTE_REVISAO"
    comparaveis = [linha for linha in existentes if linha["revisao_tipo"] == tipo and linha["revisao_ordem"] is not None]
    incomparaveis = [linha for linha in existentes if linha["revisao_tipo"] not in ("", tipo)]
    if incomparaveis or any(int(linha["revisao_ordem"]) == ordem for linha in comparaveis):
        return "PENDENTE_REVISAO"
    if not comparaveis:
        return "VIGENTE"
    maior = max(int(linha["revisao_ordem"]) for linha in comparaveis)
    return "VIGENTE" if ordem > maior else "SUPERADA"


def importar_desenhos(obra: str, pasta: Path, db_path: Path) -> dict[str, int]:
    pasta = pasta.resolve()
    raiz_engenharia = pasta.parent
    metadados_path = pasta / "_carimbos_extraidos" / "carimbos_metadados.json"
    if not metadados_path.exists():
        raise FileNotFoundError(f"Metadados não encontrados: {metadados_path}. Execute extrair_carimbos.py primeiro.")
    metadados = json.loads(metadados_path.read_text(encoding="utf-8"))
    if not isinstance(metadados, list):
        raise ValueError("carimbos_metadados.json deve conter uma lista de registros")

    db = connect(db_path)
    try:
        obra_id = garantir_obra(db, obra, obra, str(raiz_engenharia))
        resumo = {"importados": 0}
        for metadado in metadados:
            nome_pdf = str(metadado.get("pdf", "")).strip()
            if not nome_pdf:
                continue
            pdf = pasta / nome_pdf
            if not pdf.exists():
                raise FileNotFoundError(f"PDF informado nos metadados não encontrado: {pdf}")
            texto = str(metadado.get("texto", ""))
            codigo, revisao = extrair_codigo_revisao(nome_pdf, texto)
            titulo, titulo_status = limpar_titulo(texto)
            revisao_normalizada = normalizar_revisao(revisao)
            tipo = revisao_normalizada[2] if revisao_normalizada else ""
            ordem = revisao_normalizada[1] if revisao_normalizada else None
            status_calculado = definir_status_revisao(db, obra_id, codigo, revisao, tipo, ordem)
            carimbo = metadado.get("carimbo_img") or pasta / "_carimbos_extraidos" / f"{pdf.stem}_carimbo.png"
            valores = {
                "titulo": titulo, "titulo_status": titulo_status, "revisao_tipo": tipo,
                "revisao_ordem": ordem, "status": status_calculado,
                "arquivo_pdf": caminho_relativo(pdf, raiz_engenharia),
                "carimbo_img": caminho_relativo(carimbo, raiz_engenharia), "texto_carimbo": texto,
                "hash_arquivo": hash_arquivo(pdf), "updated_at": agora(),
            }
            anterior = db.execute(
                "SELECT * FROM lista_desenhos WHERE obra_id=? AND codigo=? AND revisao=?",
                (obra_id, codigo, revisao),
            ).fetchone()
            if anterior is not None:
                # Não rebaixa uma decisão humana pendente/confirmada em reexecuções idempotentes.
                if anterior["status"] == "PENDENTE_REVISAO":
                    valores["status"] = "PENDENTE_REVISAO"
                db.execute(
                    "UPDATE lista_desenhos SET titulo=?,titulo_status=?,revisao_tipo=?,revisao_ordem=?,status=?,"
                    "arquivo_pdf=?,carimbo_img=?,texto_carimbo=?,hash_arquivo=?,updated_at=? WHERE id=?",
                    (*valores.values(), anterior["id"]),
                )
                desenho_id = int(anterior["id"])
                registrar_auditoria(db, obra_id, desenho_id, "ATUALIZAR", dict(anterior),
                                   dict(db.execute("SELECT * FROM lista_desenhos WHERE id=?", (desenho_id,)).fetchone()),
                                   "Releitura automatizada de carimbo")
            else:
                instante = agora()
                cur = db.execute(
                    "INSERT INTO lista_desenhos(obra_id,codigo,titulo,titulo_status,revisao,revisao_tipo,revisao_ordem,status,"
                    "arquivo_pdf,carimbo_img,texto_carimbo,hash_arquivo,data_registro,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (obra_id, codigo, titulo, titulo_status, revisao, tipo, ordem, status_calculado,
                     valores["arquivo_pdf"], valores["carimbo_img"], texto, valores["hash_arquivo"], instante, instante),
                )
                desenho_id = int(cur.lastrowid)
                registrar_auditoria(db, obra_id, desenho_id, "INSERIR", None,
                                   dict(db.execute("SELECT * FROM lista_desenhos WHERE id=?", (desenho_id,)).fetchone()),
                                   "Extração automatizada de carimbo")

            status_final = db.execute("SELECT status FROM lista_desenhos WHERE id=?", (desenho_id,)).fetchone()[0]
            if status_final == "VIGENTE":
                anteriores_vigentes = db.execute(
                    "SELECT * FROM lista_desenhos WHERE obra_id=? AND codigo=? AND id<>? AND status='VIGENTE'",
                    (obra_id, codigo, desenho_id),
                ).fetchall()
                for anterior_vigente in anteriores_vigentes:
                    db.execute("UPDATE lista_desenhos SET status='SUPERADA',updated_at=? WHERE id=?", (agora(), anterior_vigente["id"]))
                    registrar_auditoria(db, obra_id, int(anterior_vigente["id"]), "SUPERAR", dict(anterior_vigente),
                                       dict(db.execute("SELECT * FROM lista_desenhos WHERE id=?", (anterior_vigente["id"],)).fetchone()),
                                       f"Substituída pela revisão {revisao} do desenho {codigo}")
            resumo["importados"] += 1
        # Um mesmo título candidato repetido em pranchas diferentes pode ser o nome
        # do empreendimento, não o título do desenho. Mantemos o valor para revisão,
        # mas não o apresentamos como extração confiável.
        repetidos = db.execute(
            "SELECT titulo FROM lista_desenhos WHERE obra_id=? AND titulo_status='EXTRAIDO' "
            "GROUP BY titulo HAVING COUNT(*) > 1", (obra_id,)
        ).fetchall()
        for repetido in repetidos:
            candidatos = db.execute(
                "SELECT * FROM lista_desenhos WHERE obra_id=? AND titulo=? AND titulo_status='EXTRAIDO'",
                (obra_id, repetido["titulo"]),
            ).fetchall()
            for candidato in candidatos:
                db.execute("UPDATE lista_desenhos SET titulo_status='PENDENTE_REVISAO',updated_at=? WHERE id=?", (agora(), candidato["id"]))
                registrar_auditoria(db, obra_id, int(candidato["id"]), "SINALIZAR_TITULO", dict(candidato),
                                   dict(db.execute("SELECT * FROM lista_desenhos WHERE id=?", (candidato["id"],)).fetchone()),
                                   "Título candidato repetido em pranchas distintas; requer revisão humana")
        totais = db.execute(
            "SELECT SUM(status='VIGENTE'),SUM(status='PENDENTE_REVISAO'),SUM(titulo_status='PENDENTE_REVISAO') "
            "FROM lista_desenhos WHERE obra_id=?", (obra_id,)
        ).fetchone()
        resumo.update({"vigentes": int(totais[0] or 0), "revisoes_pendentes": int(totais[1] or 0),
                       "titulos_pendentes": int(totais[2] or 0)})
        db.commit()
        return resumo
    finally:
        db.close()


def exportar_lista(obra: str, db_path: Path, saida: Path, incluir_superadas: bool = False) -> tuple[Path, Path]:
    """Exporta a lista já enriquecida com o que foi levantado em cada prancha."""
    db = connect(db_path)
    try:
        obra_row = db.execute("SELECT id FROM obras WHERE codigo=?", (obra,)).fetchone()
        if not obra_row:
            raise ValueError(f"obra '{obra}' não existe no SQLite")
        obra_id = int(obra_row["id"])

        filtros = "" if incluir_superadas else "AND d.status='VIGENTE'"
        linhas = db.execute(
            "SELECT d.codigo,d.titulo,d.titulo_status,d.revisao,d.status,d.arquivo_pdf,d.carimbo_img,d.texto_carimbo "
            "FROM lista_desenhos d JOIN obras o ON o.id=d.obra_id WHERE o.codigo=? " + filtros +
            " ORDER BY d.codigo,d.revisao_ordem,d.revisao", (obra,)
        ).fetchall()

        quantitativos = {}
        for item in db.execute(
            "SELECT prancha_referencia,disciplina,cod_eap,descricao "
            "FROM itens_quantitativo WHERE obra_id=?",
            (obra_id,),
        ).fetchall():
            chave = normalizar_referencia_prancha(item["prancha_referencia"])
            if not chave:
                continue
            resumo = quantitativos.setdefault(
                chave,
                {"disciplinas": set(), "servicos": set(), "qtd": 0},
            )
            disciplina = str(item["disciplina"] or "").strip()
            if disciplina:
                resumo["disciplinas"].add(disciplina)
            cod_eap = str(item["cod_eap"] or "").strip()
            descricao = str(item["descricao"] or "").strip()
            servico = " — ".join(parte for parte in (cod_eap, descricao) if parte)
            if servico:
                resumo["servicos"].add(servico)
            resumo["qtd"] += 1
    finally:
        db.close()

    saida.mkdir(parents=True, exist_ok=True)
    csv_path = saida / "LISTA_DE_DESENHOS.csv"
    md_path = saida / "LISTA_DE_DESENHOS.md"

    registros = []
    for linha in linhas:
        item = dict(linha)
        item["orientacao"] = (
            "Priorizar para execução, quantitativos e consultas" if item["status"] == "VIGENTE"
            else "Não utilizar — revisão superada" if item["status"] == "SUPERADA"
            else "Revisão pendente de confirmação humana"
        )
        disciplina_desenho, tipo_desenho = classificar_desenho(
            item["titulo"], item.get("texto_carimbo", ""), item["arquivo_pdf"]
        )
        item["disciplina_desenho"] = disciplina_desenho
        item["tipo_desenho"] = tipo_desenho
        item.pop("texto_carimbo", None)
        resumo = quantitativos.get(
            normalizar_referencia_prancha(item["arquivo_pdf"]),
            {"disciplinas": set(), "servicos": set(), "qtd": 0},
        )
        item["disciplinas_levantadas"] = " | ".join(sorted(resumo["disciplinas"]))
        item["servicos_levantados"] = " | ".join(sorted(resumo["servicos"]))
        item["qtd_itens_quantitativo"] = int(resumo["qtd"])
        registros.append(item)

    with csv_path.open("w", newline="", encoding="utf-8-sig") as arquivo:
        campos = [
            "codigo", "titulo", "titulo_status", "revisao", "status", "orientacao",
            "disciplina_desenho", "tipo_desenho",
            "disciplinas_levantadas", "servicos_levantados", "qtd_itens_quantitativo",
            "arquivo_pdf", "carimbo_img",
        ]
        writer = csv.DictWriter(arquivo, fieldnames=campos, delimiter=";")
        writer.writeheader()
        writer.writerows(registros)

    with md_path.open("w", encoding="utf-8") as arquivo:
        arquivo.write(f"# Lista Mestra de Desenhos — {obra}\n\n")
        arquivo.write(
            "Fonte oficial: `data/pmo_virtual.sqlite`. A lista inclui o estado atual dos quantitativos por prancha.\n\n"
        )
        arquivo.write(
            "| Código | Título | Disciplina | Tipo | Rev. | Status | Disciplinas levantadas | Serviços levantados | Itens | PDF |\n"
            "|---|---|---|---|---:|---|---|---|---:|---|\n"
        )
        for item in registros:
            disciplinas = item["disciplinas_levantadas"] or "—"
            servicos = item["servicos_levantados"] or "—"
            arquivo.write(
                f"| {item['codigo']} | {item['titulo']} | {item['disciplina_desenho']} | {item['tipo_desenho']} | "
                f"{item['revisao']} | {item['status']} | {disciplinas} | {servicos} | "
                f"{item['qtd_itens_quantitativo']} | "
                f"`{item['arquivo_pdf']}` |\n"
            )
    return csv_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Registra e exporta a lista mestra de desenhos.")
    parser.add_argument("--obra", required=True, help="Código da obra")
    parser.add_argument("--pasta", required=True, type=Path, help="Pasta com os PDFs e _carimbos_extraidos")
    parser.add_argument("--db", type=Path, default=Path("data/pmo_virtual.sqlite"), help="Banco SQLite oficial")
    parser.add_argument("--saida", type=Path, help="Pasta dos artefatos derivados; padrão: pai de --pasta")
    parser.add_argument("--incluir-superadas", action="store_true", help="Inclui revisões superadas na exportação")
    args = parser.parse_args()
    resumo = importar_desenhos(args.obra, args.pasta, args.db)
    csv_path, md_path = exportar_lista(args.obra, args.db, args.saida or args.pasta.parent, args.incluir_superadas)
    print(f"{resumo['importados']} desenho(s) processado(s): {resumo['vigentes']} revisão(ões) vigente(s), "
          f"{resumo['revisoes_pendentes']} revisão(ões) pendente(s), {resumo['titulos_pendentes']} título(s) pendente(s).")
    print(f"CSV derivado: {csv_path}\nMarkdown derivado: {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
