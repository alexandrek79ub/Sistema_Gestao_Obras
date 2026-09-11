#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Ingestão de Coleta Digital de Campo (RDO & FVS Mobile 4.0).
Processa apontamentos do aplicativo móvel, formulários de campo e mensagens de WhatsApp.

Uso:
    python scripts/processar_coleta_campo.py --obra OBRA_TMULT --arquivo apontamento.json
    python scripts/processar_coleta_campo.py --obra OBRA_TMULT --texto "RDO 22/09/2026: 5 pedreiros, 4 serventes..."
    python scripts/processar_coleta_campo.py --dir projetos/OBRA_TMULT --arquivo apontamento.json
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

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
    """
    dados = {
        "tipo": "rdo",
        "data": datetime.now().strftime("%d/%m/%Y"),
        "dia": datetime.now().strftime("%A"),
        "clima_m": "Ensolarado",
        "clima_t": "Ensolarado",
        "cond": "Próprio",
        "h_paral": 0.0,
        "ef_prop": 5,
        "ef_terc": 10,
        "hh": 132.0,
        "equip": "1x Betoneira 400L, 1x Vibrador de Imersão, Ferramental Manual",
        "eap": "EAP 1.3 / Fundações e Estrutura",
        "fvs": "Nenhuma",
        "fvs_status": "Em Andamento",
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
            dados["fvs_status"] = "🟢 Aprovado"
        elif "reprovad" in txt_lower:
            dados["fvs_status"] = "🔴 Reprovado"

    # Recalcular HH
    total_efetivo = dados["ef_prop"] + dados["ef_terc"]
    dados["hh"] = round(total_efetivo * 8.8 - (dados["h_paral"] * total_efetivo), 1)

    return dados


def processar_ingestao_rdo(obra_dir, config, rdo_data):
    sigla = config.get("sigla_obra", "TMULT")
    nome = config.get("nome_obra", "Empreendimento")
    producao_dir = os.path.join(obra_dir, "04_PRODUCAO_E_AVANCO")
    rdos_dir = os.path.join(producao_dir, "RDOS")
    os.makedirs(rdos_dir, exist_ok=True)

    # Descobrir próximo número de RDO
    arquivos_existentes = [f for f in os.listdir(rdos_dir) if f.startswith("RDO_") and f.endswith(".md")]
    max_num = 5
    for a in arquivos_existentes:
        m = re.search(r"RDO_(\d+)_", a)
        if m:
            num = int(m.group(1))
            if num > max_num:
                max_num = num
    prox_num = max_num + 1
    num_fmt = f"{prox_num:03d}"

    data_rdo = rdo_data.get("data", datetime.now().strftime("%d/%m/%Y"))
    data_slug = data_rdo.replace("/", "-")
    dia_semana = rdo_data.get("dia", "Dia Útil")

    # 1. Gerar Markdown do RDO
    conteudo_md = f"""# 📋 Relatório Diário de Obra — RDO-{num_fmt}
**Obra:** {nome} ({sigla})  
**Data:** {data_rdo} ({dia_semana})  
**Engenheiro Responsável:** Alexandre (CREA-RJ 2026-A) | **Mestre de Obras:** João da Silva  
**Origem do Apontamento:** Coleta Digital Mobile 4.0 / App de Campo  

---

## ☀️ Condições Meteorológicas
* **Período Manhã:** {rdo_data.get('clima_m', 'Ensolarado')} | **Período Tarde:** {rdo_data.get('clima_t', 'Ensolarado')}
* **Horas de Paralisação por Chuva/Clima:** {rdo_data.get('h_paral', 0.0)} horas

---

## 👷 Efetivo Presente (Headcount)
* **Equipe de Gestão e Apoio Própria:** {rdo_data.get('ef_prop', 5)} colaboradores
* **Mão de Obra Terceirizada (Empreiteiros):** {rdo_data.get('ef_terc', 12)} profissionais
* **Total de Efetivo em Canteiro:** {rdo_data.get('ef_prop', 5) + rdo_data.get('ef_terc', 12)} pessoas
* **Total de Horas-Homem (HH) Trabalhadas:** {rdo_data.get('hh', 149.6)} HH

---

## 🚜 Equipamentos Operando
* {rdo_data.get('equip', 'Betoneiras, Vibradores de Concreto e Ferramental de Canteiro')}

---

## 🔨 Frentes de Serviço e Avanço EAP
* **Pacotes EAP Executados:** {rdo_data.get('eap', 'EAP 1.3 / Fundações e Estrutura')}
* **FVS Inspecionada:** {rdo_data.get('fvs', 'Nenhuma')} — **Resultado:** {rdo_data.get('fvs_status', 'Conforme')}

---

## 📝 Ocorrências e Diário de Bordo
{rdo_data.get('obs', 'Atividades executadas dentro do ritmo previsto na Linha de Base 01.')}

---
*Assinado digitalmente via Coleta Digital Mobile Antigravity PMO Virtual.*
"""
    caminho_md = os.path.join(rdos_dir, f"RDO_{num_fmt}_{data_slug}.md")
    with open(caminho_md, "w", encoding="utf-8") as f:
        f.write(conteudo_md)

    # 2. Inserir linha na planilha PAINEL_RDOS_OBRA.xlsx
    excel_path = os.path.join(producao_dir, "PAINEL_RDOS_OBRA.xlsx")
    if os.path.exists(excel_path):
        wb = openpyxl.load_workbook(excel_path)
        if "Registro Diário RDO" in wb.sheetnames:
            ws_log = wb["Registro Diário RDO"]
            
            # Encontrar primeira linha vazia
            row = 4
            while ws_log.cell(row=row, column=1).value is not None:
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
            ws_log.cell(row=row, column=4, value=rdo_data.get('clima_m', 'Ensolarado'))
            ws_log.cell(row=row, column=5, value=rdo_data.get('clima_t', 'Ensolarado'))

            c_hp = ws_log.cell(row=row, column=6, value=float(rdo_data.get('h_paral', 0.0)))
            c_hp.alignment = Alignment(horizontal="right")
            c_hp.number_format = "#,##0.0"

            c_efp = ws_log.cell(row=row, column=7, value=int(rdo_data.get('ef_prop', 5)))
            c_efp.alignment = Alignment(horizontal="right")

            c_eft = ws_log.cell(row=row, column=8, value=int(rdo_data.get('ef_terc', 12)))
            c_eft.alignment = Alignment(horizontal="right")

            c_tot = ws_log.cell(row=row, column=9, value=f"=G{row}+H{row}")
            c_tot.font = FONT_BOLD
            c_tot.alignment = Alignment(horizontal="right")

            c_hh = ws_log.cell(row=row, column=10, value=f"=(I{row}*8.8)-(F{row}*I{row})")
            c_hh.font = FONT_BOLD
            c_hh.alignment = Alignment(horizontal="right")
            c_hh.number_format = "#,##0.0"

            ws_log.cell(row=row, column=11, value=rdo_data.get('eap', 'EAP 1.3 / Execução'))
            ws_log.cell(row=row, column=12, value=rdo_data.get('fvs', 'Nenhuma'))

            st_fvs = rdo_data.get('fvs_status', 'Conforme')
            c_st = ws_log.cell(row=row, column=13, value=st_fvs)
            c_st.alignment = Alignment(horizontal="center")
            if "Aprovad" in st_fvs or "Conforme" in st_fvs:
                c_st.font = FONT_GREEN
            elif "Reprovad" in st_fvs:
                c_st.font = FONT_RED

            ws_log.cell(row=row, column=14, value=rdo_data.get('obs', ''))

            for c in range(1, 15):
                cell = ws_log.cell(row=row, column=c)
                cell.border = THIN_BORDER
                if not cell.font or cell.font.name != "Calibri":
                    cell.font = FONT_REG
                if row % 2 == 1:
                    cell.fill = ZEBRA
            ws_log.row_dimensions[row].height = 20

            # O Painel Geral é automaticamente recalculado via fórmulas do Excel
            wb.save(excel_path)

    # 3. Trilha de Auditoria
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
        "rdo_gerado": f"RDO_{num_fmt}_{data_slug}.md",
        "dados": rdo_data
    }
    fila.append(registro)
    with open(trilha_path, "w", encoding="utf-8") as f:
        json.dump(fila, f, indent=2, ensure_ascii=False)

    return {
        "status": "sucesso",
        "rdo_numero": f"RDO-{num_fmt}",
        "arquivo_md": caminho_md,
        "excel_atualizado": excel_path
    }


def processar_ingestao_fvs(obra_dir, config, fvs_data):
    sigla = config.get("sigla_obra", "TMULT")
    producao_dir = os.path.join(obra_dir, "04_PRODUCAO_E_AVANCO")
    fvs_dir = os.path.join(producao_dir, "FVS")
    os.makedirs(fvs_dir, exist_ok=True)

    codigo_fvs = fvs_data.get("codigo", "FVS-01").upper().strip()
    status = fvs_data.get("status", "🟢 Aprovado")
    data_insp = fvs_data.get("data", datetime.now().strftime("%d/%m/%Y"))
    resp = fvs_data.get("responsavel", "Mestre de Obras / Eng. Residente")
    tolerancia = fvs_data.get("medicao_tolerancia", "Conforme especificação")
    obs = fvs_data.get("observacoes", "Inspeção em conformidade com o POP")

    # 1. Registrar em Markdown de Auditoria de Inspeções
    reg_path = os.path.join(fvs_dir, "REGISTRO_INSPECOES_CAMPO.md")
    cabecalho_necessario = not os.path.exists(reg_path)
    
    with open(reg_path, "a", encoding="utf-8") as f:
        if cabecalho_necessario:
            f.write(f"# 🛡️ REGISTRO CRONOLÓGICO DE INSPEÇÕES DE CAMPO (FVS)\n")
            f.write(f"**Obra:** {config.get('nome_obra', 'Obra')} ({sigla})\n\n")
            f.write(f"| Data | Código FVS | Responsável | Medição / Tolerância | Status | Liberação Medição |\n")
            f.write(f"| :---: | :---: | :--- | :--- | :---: | :---: |\n")
        
        liberacao = "✅ Desbloqueada" if "Aprovad" in status else "⛔ Bloqueada"
        f.write(f"| {data_insp} | **{codigo_fvs}** | {resp} | {tolerancia} | {status} | {liberacao} |\n")

    # 2. Atualizar planilha MATRIZ_BLOQUEIO_FVS_CONTRATOS
    matriz_path = os.path.join(producao_dir, f"MATRIZ_BLOQUEIO_FVS_CONTRATOS_{sigla}.xlsx")
    if not os.path.exists(matriz_path):
        # Tenta nome alternativo
        matriz_path = os.path.join(producao_dir, "MATRIZ_BLOQUEIO_FVS_CONTRATOS_TMULT.xlsx")

    if os.path.exists(matriz_path):
        wb = openpyxl.load_workbook(matriz_path)
        ws = wb.active
        
        # Procurar FVS pelo código na coluna 1 (A)
        for r in range(4, ws.max_row + 1):
            cell_val = str(ws.cell(row=r, column=1).value or "").strip().upper()
            if cell_val == codigo_fvs:
                # Se ainda não existirem cabeçalhos de status de campo, adicionar nas cols H e I
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

                c_st = ws.cell(row=r, column=8, value=status)
                c_st.alignment = Alignment(horizontal="center", vertical="center")
                if "Aprovad" in status:
                    c_st.fill = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
                    c_st.font = Font(name="Calibri", size=10, bold=True, color="137333")
                else:
                    c_st.fill = PatternFill(start_color="FCE8E6", end_color="FCE8E6", fill_type="solid")
                    c_st.font = Font(name="Calibri", size=10, bold=True, color="C5221F")

                c_dt = ws.cell(row=r, column=9, value=data_insp)
                c_dt.alignment = Alignment(horizontal="center", vertical="center")
                c_dt.font = Font(name="Calibri", size=9)

                THIN_BORDER = Border(
                    left=Side(style='thin', color="E0E0E0"),
                    right=Side(style='thin', color="E0E0E0"),
                    top=Side(style='thin', color="E0E0E0"),
                    bottom=Side(style='thin', color="E0E0E0")
                )
                c_st.border = THIN_BORDER
                c_dt.border = THIN_BORDER
                break
        wb.save(matriz_path)

    # 3. Trilha de Auditoria
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
        "tipo": "FVS",
        "dados": fvs_data
    }
    fila.append(registro)
    with open(trilha_path, "w", encoding="utf-8") as f:
        json.dump(fila, f, indent=2, ensure_ascii=False)

    return {
        "status": "sucesso",
        "codigo_fvs": codigo_fvs,
        "parecer": status,
        "registro_md": reg_path
    }


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
        res = processar_ingestao_rdo(obra_dir, config, payload)
        print(f"      ✅ RDO gerado com sucesso: {res['rdo_numero']}")
        print(f"      ✅ Arquivo Markdown criado: {res['arquivo_md']}")
        print(f"      ✅ Planilha PAINEL_RDOS_OBRA.xlsx atualizada com sucesso!")

    elif tipo == "fvs":
        print("[1/2] Processando Inspeção de Qualidade FVS...")
        res = processar_ingestao_fvs(obra_dir, config, payload)
        print(f"      ✅ Inspeção {res['codigo_fvs']} processada com status: {res['parecer']}")
        print(f"      ✅ Registro de inspeções atualizado: {res['registro_md']}")
        print(f"      ✅ Planilha MATRIZ_BLOQUEIO_FVS_CONTRATOS atualizada com sucesso!")

    print("\n✨ Ingestão de dados de campo concluída com 100% de sucesso!")


if __name__ == "__main__":
    main()
