# -*- coding: utf-8 -*-
"""Módulo Canônico de Governança de Qualidade, FVS e Liberação de Medições.

Centraliza regras para validação técnica de inspeções, ciclo de vida de FVS
(RASCUNHO, SUBMETIDA, REPROVADA, APROVADA), conferência de checklists,
tolerâncias normativas e desbloqueio estrito de medições contratuais (AUD-001).
"""

import hashlib
import json
import os
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

try:
    from scripts.common.persistencia import bloquear_recurso, salvar_texto_atomico, salvar_workbook_atomico, salvar_json_atomico
except ImportError:
    from common.persistencia import bloquear_recurso, salvar_texto_atomico, salvar_workbook_atomico, salvar_json_atomico

STATUS_VALIDOS = {"RASCUNHO", "SUBMETIDA", "REPROVADA", "APROVADA"}


def resolver_caminho_catalogo():
    """Localiza o arquivo apoio/catalogo_fvs.json a partir da raiz do repositório."""
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(raiz, "apoio", "catalogo_fvs.json")


def carregar_catalogo_fvs():
    """Carrega o catálogo auditável de definições oficiais de FVS."""
    caminho = resolver_caminho_catalogo()
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Catálogo de FVS não encontrado: {caminho}")
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def obter_definicao_fvs(codigo_fvs, catalogo=None):
    """Retorna a definição da FVS pelo código oficial (FVS-01 a FVS-08)."""
    if not codigo_fvs:
        raise ValueError("Código da FVS não fornecido.")
    codigo_limpo = str(codigo_fvs).strip().upper()
    if catalogo is None:
        catalogo = carregar_catalogo_fvs()
    for item in catalogo:
        if item.get("codigo", "").upper() == codigo_limpo:
            return item
    raise ValueError(f"Código de FVS não reconhecido no catálogo oficial: '{codigo_fvs}'. Permitidos: FVS-01 a FVS-08.")


def gerar_hash_assinatura(evidencia):
    """Gera hash auditável a partir da evidência de assinatura informada."""
    if not evidencia or not str(evidencia).strip():
        return None
    conteudo = str(evidencia).strip().encode("utf-8")
    return hashlib.sha256(conteudo).hexdigest()[:24]


def avaliar_aprovacao_fvs(dados, catalogo=None):
    """Realiza a avaliação técnica governada de uma submissão de FVS.

    Retorna um dicionário estruturado com o parecer técnico, pendências e
    se a medição pode ser desbloqueada.
    """
    if not dados or not isinstance(dados, dict):
        return {
            "aprovado": False,
            "status": "REPROVADA",
            "liberacao_medicao": False,
            "motivos": ["Payload de FVS inválido ou vazio."],
            "codigo_fvs": None,
        }

    codigo_fvs = str(dados.get("codigo", "")).strip().upper()
    motivos = []

    # 1. Validar existência do código no catálogo oficial
    try:
        definicao = obter_definicao_fvs(codigo_fvs, catalogo=catalogo)
    except ValueError as err:
        return {
            "aprovado": False,
            "status": "REPROVADA",
            "liberacao_medicao": False,
            "motivos": [str(err)],
            "codigo_fvs": codigo_fvs,
        }

    # 2. Responsável Técnico explicitamente identificado
    responsavel = str(dados.get("responsavel", "")).strip()
    if not responsavel or responsavel.lower() in {"mestre de obras / eng. residente", "default", "undefined", "null"}:
        motivos.append("Responsável técnico pela inspeção não identificado explicitamente.")

    # 3. Medição e Tolerância em campo
    tolerancia_medida = str(dados.get("medicao_tolerancia", "")).strip()
    if not tolerancia_medida or tolerancia_medida.lower() in {"conforme especificação", "ok", "conforme", "padrao", "default"}:
        motivos.append("Medição quantitativa de tolerância em campo (trena, nível, slump ou ensaio) não informada.")

    # 4. Evidência de assinatura digital
    assinatura = dados.get("assinatura")
    assinatura_str = str(assinatura).strip() if assinatura else ""
    if not assinatura_str or assinatura_str.lower() in {"pendente", "aguardando", "none", "null"}:
        motivos.append("Evidência de assinatura digital ausente ou pendente.")

    # 5. Checklist de itens normativos
    itens_obrigatorios = definicao.get("itens_verificacao", [])
    itens_conferidos = dados.get("itens_conferidos")

    if not itens_conferidos:
        motivos.append(f"Nenhum item do checklist normativo ({len(itens_obrigatorios)} obrigatórios) foi conferido.")
    elif isinstance(itens_conferidos, list):
        conferidos_set = {str(it).strip().lower() for it in itens_conferidos}
        nao_atendidos = []
        for obrigatorio in itens_obrigatorios:
            obrig_lower = obrigatorio.strip().lower()
            # Verifica correspondência exata ou por prefixo significativo
            encontrado = any(obrig_lower in c or c in obrig_lower for c in conferidos_set)
            if not encontrado:
                nao_atendidos.append(obrigatorio)
        if nao_atendidos:
            motivos.append(f"Checklist incompleto: {len(nao_atendidos)} de {len(itens_obrigatorios)} itens obrigatórios não foram atendidos.")
    elif isinstance(itens_conferidos, dict):
        nao_marcados = [k for k, v in itens_conferidos.items() if not v]
        if nao_marcados or len(itens_conferidos) < len(itens_obrigatorios):
            motivos.append("Checklist possui itens não conformes ou não assinalados.")

    # 6. Parecer declarado no apontamento
    status_declarado = str(dados.get("status", "")).strip().upper()
    if "NAO_CONFORME" in status_declarado or "REPROVAD" in status_declarado:
        motivos.append("Parecer declarado pelo inspetor é de Não Conformidade.")

    # Conclusão estrita
    aprovado = len(motivos) == 0
    status_final = "APROVADA" if aprovado else "REPROVADA"
    liberacao_medicao = aprovado  # Medição NUNCA é desbloqueada sem aprovação comprovada

    hash_ass = gerar_hash_assinatura(assinatura_str) if assinatura_str else None

    return {
        "aprovado": aprovado,
        "status": status_final,
        "liberacao_medicao": liberacao_medicao,
        "codigo_fvs": codigo_fvs,
        "titulo_fvs": definicao.get("titulo"),
        "contrato_bloqueado": definicao.get("contrato_bloqueado"),
        "responsavel": responsavel,
        "tolerancia_medida": tolerancia_medida,
        "hash_assinatura": hash_ass,
        "motivos": motivos,
    }


def promover_fvs_governado(obra_dir, config, dados_fvs):
    """Executa a promoção oficial de uma FVS sob controle de lock e escrita atômica.

    Atualiza REGISTRO_INSPECOES_CAMPO.md e a planilha MATRIZ_BLOQUEIO_FVS_CONTRATOS.
    Garante que medição só é liberada se todos os critérios técnicos forem satisfeitos.
    """
    producao_dir = os.path.join(obra_dir, "04_PRODUCAO_E_AVANCO")
    fvs_dir = os.path.join(producao_dir, "FVS")
    os.makedirs(fvs_dir, exist_ok=True)

    sigla = config.get("sigla_obra", "OBRA")
    nome_obra = config.get("nome_obra", os.path.basename(obra_dir))

    with bloquear_recurso(producao_dir, "governanca_fvs"):
        avaliacao = avaliar_aprovacao_fvs(dados_fvs)
        codigo_fvs = avaliacao.get("codigo_fvs")
        data_insp = dados_fvs.get("data", datetime.now().strftime("%d/%m/%Y"))
        resp = avaliacao.get("responsavel") or "NÃO IDENTIFICADO"
        tol = avaliacao.get("tolerancia_medida") or "NÃO MEDIDO"
        aprovado = avaliacao["aprovado"]

        status_texto = "🟢 Aprovado" if aprovado else "🔴 Reprovado"
        liberacao_texto = "✅ Desbloqueada" if aprovado else "⛔ Bloqueada"
        hash_ass = avaliacao.get("hash_assinatura") or "SEM_EVIDENCIA"

        # 1. Atualizar REGISTRO_INSPECOES_CAMPO.md
        reg_path = os.path.join(fvs_dir, "REGISTRO_INSPECOES_CAMPO.md")
        cabecalho_necessario = not os.path.exists(reg_path)
        linhas_existentes = ""
        if not cabecalho_necessario:
            with open(reg_path, "r", encoding="utf-8") as f:
                linhas_existentes = f.read()

        nova_linha = f"| {data_insp} | **{codigo_fvs}** | {resp} | {tol} | {status_texto} | {liberacao_texto} | `{hash_ass}` |\n"

        if cabecalho_necessario:
            conteudo_md = (
                f"# 🛡️ REGISTRO CRONOLÓGICO DE INSPEÇÕES DE CAMPO (FVS)\n"
                f"**Obra:** {nome_obra} ({sigla})  \n"
                f"**Governança:** Motor Universal de Qualidade AUD-001  \n\n"
                f"| Data | Código FVS | Responsável | Medição / Tolerância | Status | Liberação Medição | Hash Assinatura |\n"
                f"| :---: | :---: | :--- | :--- | :---: | :---: | :---: |\n"
                f"{nova_linha}"
            )
        else:
            conteudo_md = linhas_existentes.rstrip() + "\n" + nova_linha

        salvar_texto_atomico(reg_path, conteudo_md)

        # 2. Atualizar planilha de matriz de bloqueio se existir
        matriz_path = os.path.join(producao_dir, f"MATRIZ_BLOQUEIO_FVS_CONTRATOS_{sigla}.xlsx")
        if not os.path.exists(matriz_path):
            matriz_path = os.path.join(producao_dir, "MATRIZ_BLOQUEIO_FVS_CONTRATOS_TMULT.xlsx")
        if not os.path.exists(matriz_path):
            matriz_path = os.path.join(producao_dir, "MATRIZ_BLOQUEIO_FVS_CONTRATOS_OBRA_NOVA.xlsx")

        if os.path.exists(matriz_path):
            wb = openpyxl.load_workbook(matriz_path)
            ws = wb.active
            for r in range(4, ws.max_row + 1):
                cell_val = str(ws.cell(row=r, column=1).value or "").strip().upper()
                if cell_val == codigo_fvs:
                    # Garantir cabeçalhos colunas 8 e 9
                    if ws.cell(row=3, column=8).value != "Status Atual de Campo":
                        ws.cell(row=3, column=8, value="Status Atual de Campo")
                        ws.cell(row=3, column=8).font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
                        ws.cell(row=3, column=8).fill = PatternFill(start_color="284B78", end_color="284B78", fill_type="solid")
                        ws.cell(row=3, column=8).alignment = Alignment(horizontal="center", vertical="center")
                        ws.column_dimensions["H"].width = 22

                        ws.cell(row=3, column=9, value="Última Inspeção")
                        ws.cell(row=3, column=9).font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
                        ws.cell(row=3, column=9).fill = PatternFill(start_color="284B78", end_color="284B78", fill_type="solid")
                        ws.cell(row=3, column=9).alignment = Alignment(horizontal="center", vertical="center")
                        ws.column_dimensions["I"].width = 16

                    c_st = ws.cell(row=r, column=8, value=status_texto)
                    c_st.alignment = Alignment(horizontal="center", vertical="center")
                    if aprovado:
                        c_st.fill = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
                        c_st.font = Font(name="Calibri", size=10, bold=True, color="137333")
                    else:
                        c_st.fill = PatternFill(start_color="FCE8E6", end_color="FCE8E6", fill_type="solid")
                        c_st.font = Font(name="Calibri", size=10, bold=True, color="C5221F")

                    c_dt = ws.cell(row=r, column=9, value=data_insp)
                    c_dt.alignment = Alignment(horizontal="center", vertical="center")
                    c_dt.font = Font(name="Calibri", size=9)

                    thin_border = Border(
                        left=Side(style='thin', color="E0E0E0"),
                        right=Side(style='thin', color="E0E0E0"),
                        top=Side(style='thin', color="E0E0E0"),
                        bottom=Side(style='thin', color="E0E0E0")
                    )
                    c_st.border = thin_border
                    c_dt.border = thin_border
                    break
            salvar_workbook_atomico(matriz_path, wb)

        # 3. Trilha de Auditoria
        trilha_path = os.path.join(producao_dir, "fila_apontamentos_campo.json")
        fila = []
        if os.path.exists(trilha_path):
            try:
                with open(trilha_path, "r", encoding="utf-8") as f:
                    fila = json.load(f)
            except Exception:
                fila = []

        registro_auditoria = {
            "id": f"GOV-FVS-{codigo_fvs}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "tipo": "FVS_PROMOCAO_GOVERNADA",
            "resultado": avaliacao,
            "dados_entrada": dados_fvs,
        }
        fila.append(registro_auditoria)
        salvar_json_atomico(trilha_path, fila)

        return {
            "status": avaliacao["status"],
            "aprovado": avaliacao["aprovado"],
            "codigo_fvs": codigo_fvs,
            "liberacao_medicao": avaliacao["liberacao_medicao"],
            "responsavel": resp,
            "hash_assinatura": hash_ass,
            "registro_md": reg_path,
            "motivos": avaliacao.get("motivos", []),
        }
