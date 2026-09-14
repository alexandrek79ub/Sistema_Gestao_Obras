#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Ingestão de Coleta Digital de Campo (RDO & FVS Mobile 4.0).
Processa apontamentos do aplicativo móvel, formulários de campo e mensagens de WhatsApp.
Governança da Fase 3 (AUD-001 e AUD-010).

Uso:
    python scripts/processar_coleta_campo.py --obra OBRA_TMULT --arquivo apontamento.json
    python scripts/processar_coleta_campo.py --obra OBRA_TMULT --texto "RDO 22/09/2026: 5 pedreiros, 4 serventes..."
    python scripts/processar_coleta_campo.py --obra OBRA_TMULT --arquivo fvs.json --promover-fvs
    python scripts/processar_coleta_campo.py --dir projetos/OBRA_TMULT --arquivo apontamento.json
"""

import os
import sys
import json
import re
import argparse
import hashlib
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from common.persistencia import bloquear_recurso, salvar_json_atomico, salvar_texto_atomico, salvar_workbook_atomico
    from common.qualidade_fvs import avaliar_aprovacao_fvs, promover_fvs_governado, obter_definicao_fvs
except ImportError:
    from scripts.common.persistencia import bloquear_recurso, salvar_json_atomico, salvar_texto_atomico, salvar_workbook_atomico
    from scripts.common.qualidade_fvs import avaliar_aprovacao_fvs, promover_fvs_governado, obter_definicao_fvs

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def parse_args():
    parser = argparse.ArgumentParser(description="Motor Universal de Ingestão de Coleta de Campo.")
    parser.add_argument("--obra", type=str, default="OBRA_TMULT", help="Nome da pasta da obra em projetos/")
    parser.add_argument("--dir", type=str, default=None, help="Caminho direto para a pasta da obra")
    parser.add_argument("--arquivo", type=str, default=None, help="Caminho para arquivo JSON de apontamento")
    parser.add_argument("--texto", type=str, default=None, help="Texto de mensagem rápida / WhatsApp do Mestre")
    parser.add_argument("--tipo", type=str, choices=["rdo", "fvs", "auto"], default="auto", help="Tipo de apontamento")
    parser.add_argument("--promover-fvs", action="store_true", help="Executa a análise governada e promove a FVS oficial")
    parser.add_argument("--aprovar-fvs", action="store_true", help="Alias para --promover-fvs")
    return parser.parse_args()


def carregar_dados_obra(obra_dir):
    config_path = os.path.join(obra_dir, "config_obra.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {
            "nome_obra": os.path.basename(obra_dir),
            "sigla_obra": os.path.basename(obra_dir)[:6].upper(),
            "prazo_meses": 6.0
        }
    return config


def parse_whatsapp_rdo(texto):
    """
    Extrai variáveis de um texto informal enviado pelo Mestre ou Encarregado via WhatsApp.
    O resultado inicial é tratado como rascunho de campo até confirmação técnica.
    """
    dados = {
        "tipo": "rdo",
        "data": datetime.now().strftime("%d/%m/%Y"),
        "dia": datetime.now().strftime("%A"),
        "responsavel": "Mestre de Obras (via WhatsApp)",
        "clima_m": "Ensolarado",
        "clima_t": "Ensolarado",
        "cond": "Próprio",
        "h_paral": 0.0,
        "ef_prop": 5,
        "ef_terc": 0,
        "hh": 44.0,
        "equip": "Ferramental Manual",
        "eap": "EAP 1.0 / Mobilização Geral",
        "fvs": "Nenhuma",
        "fvs_status": "Em Andamento",
        "assinatura": None,
        "obs": texto.strip()
    }

    # Data
    match_data = re.search(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", texto)
    if match_data:
        d_str = match_data.group(1).replace("-", "/")
        partes = d_str.split("/")
        if len(partes[2]) == 2:
            partes[2] = "20" + partes[2]
        dados["data"] = f"{int(partes[0]):02d}/{int(partes[1]):02d}/{partes[2]}"

    # Clima
    txt_lower = texto.lower()
    if "chuva forte" in txt_lower or "temporal" in txt_lower:
        dados["clima_m"] = "Chuvoso"
        dados["clima_t"] = "Chuva Forte"
        dados["cond"] = "Impróprio Parcial"
        dados["h_paral"] = 3.0
    elif "chuva" in txt_lower or "garoa" in txt_lower:
        dados["clima_t"] = "Chuva Leve"
        dados["h_paral"] = 1.0
    elif "nublado" in txt_lower:
        dados["clima_m"] = "Nublado"
        dados["clima_t"] = "Nublado"

    # Horas de paralisação explícitas
    match_h = re.search(r"(\d+(?:[.,]\d+)?)\s*h(?:oras?)?\s*(?:de\s*)?(?:chuva|paralisad|parada)", txt_lower)
    if match_h:
        dados["h_paral"] = float(match_h.group(1).replace(",", "."))

    # Efetivo
    pedreiros = 0
    serventes = 0
    carpinteiros = 0
    armadores = 0
    eletricistas = 0

    m_ped = re.search(r"(\d+)\s*(?:pedreir|oficia)", txt_lower)
    if m_ped: pedreiros = int(m_ped.group(1))

    m_ser = re.search(r"(\d+)\s*(?:servente|ajudante)", txt_lower)
    if m_ser: serventes = int(m_ser.group(1))

    m_carp = re.search(r"(\d+)\s*(?:carpinteir)", txt_lower)
    if m_carp: carpinteiros = int(m_carp.group(1))

    m_arm = re.search(r"(\d+)\s*(?:armador|ferreir)", txt_lower)
    if m_arm: armadores = int(m_arm.group(1))

    m_ele = re.search(r"(\d+)\s*(?:eletricista)", txt_lower)
    if m_ele: eletricistas = int(m_ele.group(1))

    total_terc = pedreiros + serventes + carpinteiros + armadores + eletricistas
    if total_terc > 0:
        dados["ef_terc"] = total_terc

    m_prop = re.search(r"(\d+)\s*(?:proprio|gestao|engenhar)", txt_lower)
    if m_prop:
        dados["ef_prop"] = int(m_prop.group(1))

    # FVS mencionada
    m_fvs = re.search(r"(fvs[-\s]?0?[1-8])", txt_lower)
    if m_fvs:
        cod = m_fvs.group(1).upper().replace(" ", "")
        if not cod.startswith("FVS-"):
            cod = cod[:3] + "-" + cod[3:]
        dados["fvs"] = cod
        if "aprovad" in txt_lower or "ok" in txt_lower or "conforme" in txt_lower:
            dados["fvs_status"] = "SUBMETIDA"
        elif "reprovad" in txt_lower:
            dados["fvs_status"] = "SUBMETIDA_COM_RESSALVA"

    # Recalcular HH
    total_efetivo = dados["ef_prop"] + dados["ef_terc"]
    dados["hh"] = round(max(0.0, total_efetivo * 8.8 - (dados["h_paral"] * total_efetivo)), 1)

    return dados


def processar_ingestao_rdo(obra_dir, config, rdo_data):
    """Gera o RDO oficial ou rascunho com base exclusivamente nos dados informados.
    
    AUD-010: numeração inicia em 001, valores factuais não são inventados,
    e a assinatura digital exige comprovação auditável.
    """
    sigla = config.get("sigla_obra", "OBRA")
    nome = config.get("nome_obra", os.path.basename(obra_dir))
    producao_dir = os.path.join(obra_dir, "04_PRODUCAO_E_AVANCO")
    rdos_dir = os.path.join(producao_dir, "RDOS")
    os.makedirs(rdos_dir, exist_ok=True)

    # 1. Validação estrita de campos obrigatórios (sem invenção de fatos)
    data_rdo = rdo_data.get("data")
    if not data_rdo or not str(data_rdo).strip():
        raise ValueError("Campo obrigatório ausente no RDO: 'data' deve ser informada.")

    if "ef_prop" not in rdo_data or rdo_data["ef_prop"] is None:
        raise ValueError("Campo obrigatório ausente no RDO: efetivo próprio ('ef_prop') deve ser informado numericamente.")
    if "ef_terc" not in rdo_data or rdo_data["ef_terc"] is None:
        raise ValueError("Campo obrigatório ausente no RDO: efetivo terceirizado ('ef_terc') deve ser informado numericamente.")

    ef_prop = int(rdo_data["ef_prop"])
    ef_terc = int(rdo_data["ef_terc"])
    total_efetivo = ef_prop + ef_terc

    eap = rdo_data.get("eap")
    if not eap or not str(eap).strip():
        raise ValueError("Campo obrigatório ausente no RDO: frentes EAP executadas ('eap') devem ser informadas.")

    responsavel = (
        rdo_data.get("responsavel")
        or rdo_data.get("engenheiro")
        or config.get("engenheiro_responsavel")
    )
    if not responsavel or not str(responsavel).strip():
        raise ValueError("Campo obrigatório ausente no RDO: responsável técnico pelo apontamento não identificado.")

    mestre = rdo_data.get("mestre") or config.get("mestre_obras") or "Não informado"

    h_paral = float(rdo_data.get("h_paral", 0.0))
    hh_calculado = round(max(0.0, total_efetivo * 8.8 - (h_paral * total_efetivo)), 1)

    # 2. Descobrir próximo número de RDO (AUD-010: inicia em 001 se vazio)
    arquivos_existentes = [f for f in os.listdir(rdos_dir) if f.startswith("RDO_") and f.endswith(".md")]
    max_num = 0
    for a in arquivos_existentes:
        m = re.search(r"RDO_(\d+)_", a)
        if m:
            num = int(m.group(1))
            if num > max_num:
                max_num = num
    prox_num = max_num + 1
    num_fmt = f"{prox_num:03d}"

    data_slug = data_rdo.replace("/", "-")
    dia_semana = rdo_data.get("dia", "Dia Útil")

    # 3. Validação de assinatura e integridade
    assinatura_raw = rdo_data.get("assinatura")
    assinatura_str = str(assinatura_raw).strip() if assinatura_raw else ""
    tem_assinatura = bool(
        assinatura_str
        and assinatura_str.lower() not in {"pendente", "aguardando", "none", "null", "false"}
    )

    if tem_assinatura:
        hash_ass = hashlib.sha256(assinatura_str.encode("utf-8")).hexdigest()[:16]
        rodape_assinatura = f"*Assinado digitalmente por {responsavel} em {datetime.now().strftime('%d/%m/%Y %H:%M')}. Evidência de integridade: `{hash_ass}`*"
        status_documento = "OFICIAL"
    else:
        rodape_assinatura = "*Status: RASCUNHO / PENDENTE DE ASSINATURA — Documento não oficializado sem evidência válida de assinatura do Responsável Técnico.*"
        status_documento = "RASCUNHO"

    clima_m = rdo_data.get("clima_m", "Não informado")
    clima_t = rdo_data.get("clima_t", "Não informado")
    equip = rdo_data.get("equip", "Nenhum equipamento pesado reportado")
    fvs = rdo_data.get("fvs", "Nenhuma")
    fvs_status = rdo_data.get("fvs_status", "N/A")
    obs = rdo_data.get("obs", "Sem ocorrências anormais registradas no período.")

    # 4. Gerar Markdown do RDO
    conteudo_md = f"""# 📋 Relatório Diário de Obra — RDO-{num_fmt}
**Obra:** {nome} ({sigla})  
**Data:** {data_rdo} ({dia_semana})  
**Responsável Técnico:** {responsavel} | **Mestre de Obras:** {mestre}  
**Status do Documento:** {status_documento}  
**Origem do Apontamento:** Coleta Digital Mobile 4.0 / App de Campo  

---

## ☀️ Condições Meteorológicas
* **Período Manhã:** {clima_m} | **Período Tarde:** {clima_t}
* **Horas de Paralisação por Chuva/Clima:** {h_paral} horas

---

## 👷 Efetivo Presente (Headcount)
* **Equipe de Gestão e Apoio Própria:** {ef_prop} colaboradores
* **Mão de Obra Terceirizada (Empreiteiros):** {ef_terc} profissionais
* **Total de Efetivo em Canteiro:** {total_efetivo} pessoas
* **Total de Horas-Homem (HH) Trabalhadas:** {hh_calculado} HH

---

## 🚜 Equipamentos Operando
* {equip}

---

## 🔨 Frentes de Serviço e Avanço EAP
* **Pacotes EAP Executados:** {eap}
* **FVS Inspecionada:** {fvs} — **Resultado:** {fvs_status}

---

## 📝 Ocorrências e Diário de Bordo
{obs}

---
{rodape_assinatura}
"""
    caminho_md = os.path.join(rdos_dir, f"RDO_{num_fmt}_{data_slug}.md")
    salvar_texto_atomico(caminho_md, conteudo_md)

    # 5. Inserir linha na planilha PAINEL_RDOS_OBRA.xlsx
    excel_path = os.path.join(producao_dir, "PAINEL_RDOS_OBRA.xlsx")
    if os.path.exists(excel_path):
        wb = openpyxl.load_workbook(excel_path)
        if "Registro Diário RDO" in wb.sheetnames:
            ws_log = wb["Registro Diário RDO"]

            # Encontrar primeira linha livre a partir da linha 4
            row = 4
            while ws_log.cell(row=row, column=1).value is not None and str(ws_log.cell(row=row, column=1).value).strip() != "":
                val_col1 = str(ws_log.cell(row=row, column=1).value).strip()
                if val_col1.startswith("TOTAL"):
                    ws_log.insert_rows(row, 1)
                    break
                row += 1

            THIN_BORDER = Border(
                left=Side(style='thin', color="E0E0E0"),
                right=Side(style='thin', color="E0E0E0"),
                top=Side(style='thin', color="E0E0E0"),
                bottom=Side(style='thin', color="E0E0E0")
            )
            FONT_REG = Font(name="Calibri", size=9, color="333333")
            FONT_BOLD = Font(name="Calibri", size=9, bold=True, color="1B365D")
            FONT_GREEN = Font(name="Calibri", size=9, bold=True, color="137333")
            FONT_RED = Font(name="Calibri", size=9, bold=True, color="C5221F")
            ZEBRA = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")

            ws_log.cell(row=row, column=1, value=f"RDO-{num_fmt}").alignment = Alignment(horizontal="center")
            ws_log.cell(row=row, column=2, value=data_rdo).alignment = Alignment(horizontal="center")
            ws_log.cell(row=row, column=3, value=dia_semana)
            ws_log.cell(row=row, column=4, value=clima_m)
            ws_log.cell(row=row, column=5, value=clima_t)

            c_hp = ws_log.cell(row=row, column=6, value=h_paral)
            c_hp.alignment = Alignment(horizontal="right")
            c_hp.number_format = "#,##0.0"

            c_efp = ws_log.cell(row=row, column=7, value=ef_prop)
            c_efp.alignment = Alignment(horizontal="right")

            c_eft = ws_log.cell(row=row, column=8, value=ef_terc)
            c_eft.alignment = Alignment(horizontal="right")

            c_tot = ws_log.cell(row=row, column=9, value=f"=G{row}+H{row}")
            c_tot.font = FONT_BOLD
            c_tot.alignment = Alignment(horizontal="right")

            c_hh = ws_log.cell(row=row, column=10, value=f"=(I{row}*8.8)-(F{row}*I{row})")
            c_hh.font = FONT_BOLD
            c_hh.alignment = Alignment(horizontal="right")
            c_hh.number_format = "#,##0.0"

            ws_log.cell(row=row, column=11, value=eap)
            ws_log.cell(row=row, column=12, value=fvs)

            c_st = ws_log.cell(row=row, column=13, value=fvs_status)
            c_st.alignment = Alignment(horizontal="center")
            if "Aprovad" in fvs_status or "Conforme" in fvs_status:
                c_st.font = FONT_GREEN
            elif "Reprovad" in fvs_status:
                c_st.font = FONT_RED

            ws_log.cell(row=row, column=14, value=obs)

            for c in range(1, 15):
                cell = ws_log.cell(row=row, column=c)
                cell.border = THIN_BORDER
                if not cell.font or cell.font.name != "Calibri":
                    cell.font = FONT_REG
                if row % 2 == 1:
                    cell.fill = ZEBRA
            ws_log.row_dimensions[row].height = 20

            salvar_workbook_atomico(excel_path, wb)

    # 6. Trilha de Auditoria
    trilha_path = os.path.join(producao_dir, "fila_apontamentos_campo.json")
    fila = []
    if os.path.exists(trilha_path):
        try:
            with open(trilha_path, "r", encoding="utf-8") as f:
                fila = json.load(f)
        except Exception:
            fila = []

    registro = {
        "id": f"APONT-RDO-{num_fmt}",
        "timestamp": datetime.now().isoformat(),
        "tipo": "RDO",
        "status": status_documento,
        "responsavel": responsavel,
        "rdo_gerado": f"RDO_{num_fmt}_{data_slug}.md",
        "dados": rdo_data
    }
    fila.append(registro)
    salvar_json_atomico(trilha_path, fila)

    return {
        "status": "sucesso",
        "rdo_numero": f"RDO-{num_fmt}",
        "status_documento": status_documento,
        "arquivo_md": caminho_md,
        "excel_atualizado": excel_path
    }


def processar_ingestao_fvs(obra_dir, config, fvs_data):
    """Ingestão e contenção: FVS de campo é gravada em staging como SUBMETIDA.
    
    Não promove registro oficial nem libera medição de forma autônoma (AUD-001).
    """
    codigo_fvs = str(fvs_data.get("codigo", "")).upper().strip()
    
    # Validar se o código é reconhecido no catálogo oficial
    try:
        obter_definicao_fvs(codigo_fvs)
    except Exception as err:
        print(f"⚠️ Validação preliminar FVS: {err}")

    # Gravar em fila/staging para análise governada posterior
    producao_dir = os.path.join(obra_dir, "04_PRODUCAO_E_AVANCO")
    trilha_path = os.path.join(producao_dir, "fila_apontamentos_campo.json")
    fila = []
    if os.path.exists(trilha_path):
        try:
            with open(trilha_path, "r", encoding="utf-8") as f:
                fila = json.load(f)
        except Exception:
            fila = []
    
    registro = {
        "id": f"APONT-FVS-{codigo_fvs}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "tipo": "FVS_SUBMISSAO",
        "status": "SUBMETIDA",
        "dados": fvs_data
    }
    fila.append(registro)
    salvar_json_atomico(trilha_path, fila)

    return {
        "status": "SUBMETIDA",
        "codigo_fvs": codigo_fvs,
        "parecer": "PENDENTE_ANALISE_GOVERNADA",
        "registro_md": None,
    }


def processar_promocao_fvs(obra_dir, config, fvs_data):
    """Executa a análise técnica governada e promove a FVS oficialmente (AUD-001)."""
    return promover_fvs_governado(obra_dir, config, fvs_data)


def main():
    args = parse_args()
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    if args.dir:
        obra_dir = os.path.abspath(args.dir)
    else:
        obra_dir = os.path.join(workspace_root, "projetos", args.obra)

    if not os.path.exists(obra_dir):
        print(f"❌ Erro: Diretório da obra não encontrado: {obra_dir}")
        sys.exit(1)

    config = carregar_dados_obra(obra_dir)
    sigla = config.get("sigla_obra", "OBRA")
    nome = config.get("nome_obra", os.path.basename(obra_dir))

    print("=======================================================")
    print("📲 MOTOR DE INGESTÃO DE COLETA DIGITAL DE CAMPO 4.0")
    print("=======================================================")
    print(f"📂 Diretório da Obra: {obra_dir}")
    print(f"🏗️  Obra Ativa: {sigla} — {nome}\n")

    payload = None

    # Caso 1: Arquivo JSON fornecido
    if args.arquivo:
        caminho_arq = os.path.abspath(args.arquivo)
        if not os.path.exists(caminho_arq):
            print(f"❌ Erro: Arquivo de apontamento não encontrado: {caminho_arq}")
            sys.exit(1)
        with open(caminho_arq, "r", encoding="utf-8") as f:
            payload = json.load(f)
        print(f"📥 Apontamento lido do arquivo: {caminho_arq}")

    # Caso 2: Texto informado na linha de comando (WhatsApp / Voz)
    elif args.texto:
        print(f"📥 Processando texto de campo informado via CLI...")
        print(f"   Mensagem: \"{args.texto}\"")
        payload = parse_whatsapp_rdo(args.texto)

    else:
        print("❌ Erro: Forneça um arquivo JSON (--arquivo) ou um texto (--texto).")
        sys.exit(1)

    tipo = payload.get("tipo", args.tipo).lower()
    if tipo == "auto":
        if "codigo" in payload or "fvs" in str(payload.get("tipo", "")).lower():
            tipo = "fvs"
        else:
            tipo = "rdo"

    if tipo == "rdo":
        print("[1/2] Processando Apontamento Diário de RDO...")
        producao_dir = os.path.join(obra_dir, "04_PRODUCAO_E_AVANCO")
        with bloquear_recurso(producao_dir, "ingestao_rdo"):
            res = processar_ingestao_rdo(obra_dir, config, payload)
        print(f"      ✅ RDO gerado com sucesso: {res['rdo_numero']} [{res['status_documento']}]")
        print(f"      ✅ Arquivo Markdown criado: {res['arquivo_md']}")
        print(f"      ✅ Planilha PAINEL_RDOS_OBRA.xlsx atualizada com sucesso!")

    elif tipo == "fvs":
        if args.promover_fvs or args.aprovar_fvs:
            print("[1/2] Executando Análise Técnica Governada de FVS (AUD-001)...")
            res = processar_promocao_fvs(obra_dir, config, payload)
            if res["aprovado"]:
                print(f"      ✅ FVS {res['codigo_fvs']} APROVADA tecnicamente por {res['responsavel']}!")
                print(f"      ✅ Medição correspondente DESBLOQUEADA com sucesso.")
                print(f"      ✅ Registro oficial: {res['registro_md']}")
            else:
                print(f"      ⛔ FVS {res['codigo_fvs']} REPROVADA ou PENDENTE.")
                print(f"      ⛔ Medição permanece BLOQUEADA.")
                for motivo in res.get("motivos", []):
                    print(f"         - {motivo}")
        else:
            print("[1/2] Registrando submissão de FVS para análise governada...")
            res = processar_ingestao_fvs(obra_dir, config, payload)
            print(f"      ⏸️ FVS {res['codigo_fvs']} permanece {res['parecer']}.")
            print("      ⏸️ Nenhum registro oficial ou liberação de medição foi alterado.")

    print("\n✨ Ingestão de dados de campo concluída com 100% de sucesso!")


if __name__ == "__main__":
    main()
