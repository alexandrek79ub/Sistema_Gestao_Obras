"""Entrada segura: PDF → evidência confirmada → elemento → regra → SQLite."""

import argparse
from pathlib import Path
from typing import Callable

from motor_quantitativos.auditoria.trilha_revisoes import registrar_revisao
from motor_quantitativos.exportadores import exportar_artefatos
from motor_quantitativos.importadores.core.leitor_pdf_base import LeitorPDFBase
from motor_quantitativos.importadores.disciplinas.parser_contrato import validar_elementos
from motor_quantitativos.importadores.disciplinas.parser_fundacoes_contrato import ParserFundacoesContrato
from motor_quantitativos.importadores.disciplinas.parsers_contrato import (
    extrair_arquitetura, extrair_estrutura, extrair_instalacoes, extrair_servicos_especiais,
)
from motor_quantitativos.importadores.disciplinas.pipeline_fundacoes import quantificar_sapatas
from motor_quantitativos.importadores.disciplinas.quantificador_contrato import quantificar_elementos
from motor_quantitativos.repositorio.sqlite_repository import connect, garantir_obra, persistir_itens_quantificados


def _extrair(disciplina: str, obra_codigo: str, evidencias):
    if disciplina == "FUNDACOES":
        elementos = ParserFundacoesContrato(obra_codigo, evidencias).extrair_sapatas()
        return elementos, quantificar_sapatas
    extractors: dict[str, Callable] = {
        "ESTRUTURA": extrair_estrutura,
        "ARQUITETURA": extrair_arquitetura,
        "INSTALACOES": extrair_instalacoes,
        "SERVICOS_ESPECIAIS": extrair_servicos_especiais,
    }
    try:
        return extractors[disciplina](obra_codigo, evidencias), quantificar_elementos
    except KeyError as exc:
        raise ValueError(f"Disciplina não suportada pelo fluxo contratual: {disciplina}") from exc


def processar_prancha(caminho_pdf: str | Path, *, obra_codigo: str, obra_nome: str,
                      source_revision: str, disciplina: str, db_path: str | Path,
                      diretorio_obra: str | Path, evidencias_confirmadas: bool = False) -> dict:
    """Persiste apenas quantitativos líquidos com evidência confirmada explicitamente."""
    if not evidencias_confirmadas:
        raise ValueError("Extração concluída sem gravação: revise as evidências e confirme explicitamente antes de calcular")

    leitor = LeitorPDFBase(caminho_pdf)
    try:
        evidencias = leitor.extrair_evidencias(source_revision, confidence="USER_CONFIRMED")
    finally:
        leitor.doc.close()
    elementos, quantificador = _extrair(disciplina.upper(), obra_codigo, evidencias)
    if not elementos:
        raise ValueError("Nenhum elemento com cotas explícitas foi encontrado; registrar RFI, sem criar quantitativo")
    elementos = validar_elementos(elementos)
    itens = quantificador(elementos)
    if not itens:
        raise ValueError("Nenhum item quantificável foi produzido; registrar RFI, sem criar quantitativo")

    db = connect(db_path)
    try:
        obra_id = garantir_obra(db, obra_codigo, obra_nome, str(Path(diretorio_obra).resolve()))
        revisao_id = registrar_revisao(
            db, obra_id, "QUANTITATIVO", f"pdf-contratual:{Path(caminho_pdf).name}",
            "motor-python", f"Importação contratual da revisão {source_revision}",
        )
        item_ids = persistir_itens_quantificados(db, obra_id, itens, revisao_id)
        arquivos = exportar_artefatos(db, obra_id)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    return {"obra_id": obra_id, "elementos": len(elementos), "itens": len(item_ids), "arquivos": [str(a) for a in arquivos]}


def main() -> None:
    parser = argparse.ArgumentParser(description="Importação contratual e multiobra de quantitativos")
    parser.add_argument("pdf_path")
    parser.add_argument("--obra", required=True, help="Código estável da obra")
    parser.add_argument("--nome-obra", required=True)
    parser.add_argument("--revisao", required=True, help="Revisão da prancha")
    parser.add_argument("--disciplina", required=True, choices=("FUNDACOES", "ESTRUTURA", "ARQUITETURA", "INSTALACOES", "SERVICOS_ESPECIAIS"))
    parser.add_argument("--db", default="data/pmo_virtual.sqlite")
    parser.add_argument("--diretorio-obra", required=True)
    parser.add_argument("--confirmar-evidencias", action="store_true", help="Declara que as evidências extraídas foram revisadas")
    args = parser.parse_args()
    resultado = processar_prancha(
        args.pdf_path, obra_codigo=args.obra, obra_nome=args.nome_obra, source_revision=args.revisao,
        disciplina=args.disciplina, db_path=args.db, diretorio_obra=args.diretorio_obra,
        evidencias_confirmadas=args.confirmar_evidencias,
    )
    print(resultado)


if __name__ == "__main__":
    main()
