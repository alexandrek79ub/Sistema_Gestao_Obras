#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Organograma Executivo & Estrutura Funcional de Campo Multi-Obra
Ecossistema de Gestão de Obras & PMO Virtual

Gera o Organograma em PNG de alta resolução e em SVG vetorial nativo
diretamente na pasta 06_SST_E_RH da obra selecionada.

Uso:
    python scripts/gerar_organograma_visual.py --obra OBRA_TMULT
    python scripts/gerar_organograma_visual.py --obra RESIDENCIAL_ALPHA
    python scripts/gerar_organograma_visual.py --dir /caminho/personalizado/da/obra
"""

import os
import sys
import json
import argparse
import html
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def obter_dados_obra(proj_dir, obra_id):
    config_path = os.path.join(proj_dir, "config_obra.json")
    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            print(f"[AVISO] Não foi possível ler config_obra.json: {e}")

    nome_obra = config.get("nome_obra", obra_id)
    sigla_obra = config.get("sigla_obra", obra_id)

    # Dedicação do Engenheiro Residente
    dedicacao_eng = "Dedicação 60% (EAP 1.0.1) • Gestão Técnica, Qualidade & Fiscalização"
    for item in config.get("administracao_local", []):
        desc = item.get("descricao", "")
        if "engenheiro" in desc.lower():
            if "50%" in desc:
                dedicacao_eng = "Dedicação 50% (EAP 1.0.1) • Gestão Técnica, Qualidade & Fiscalização"
            elif "100%" in desc:
                dedicacao_eng = "Dedicação 100% (EAP 1.0.1) • Gestão Técnica, Qualidade & Fiscalização"
            elif "dedicação" in desc.lower():
                dedicacao_eng = desc
            break

    if sigla_obra == "TMULT":
        subtitulo = "EDIFÍCIO ADMINISTRATIVO TMULT (PORTO DO AÇU) — BASELINE 01"
    else:
        subtitulo = f"{nome_obra.upper()} — BASELINE 01"

    return {
        "nome_obra": nome_obra,
        "sigla_obra": sigla_obra,
        "subtitulo": subtitulo,
        "dedicacao_eng": dedicacao_eng
    }

# ==============================================================================
# 1. GERAÇÃO EM SVG VETORIAL (NATIVO, ULTRA NÍTIDO)
# ==============================================================================
def gerar_svg(svg_path, info):
    subtitulo_xml = html.escape(info["subtitulo"])
    dedicacao_eng_xml = html.escape(info["dedicacao_eng"])

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 950" width="100%" height="100%" style="background-color: #FFFFFF; font-family: 'Segoe UI', Arial, sans-serif;">
  <defs>
    <!-- Gradientes e Sombras -->
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000000" flood-opacity="0.10" />
    </filter>
    <linearGradient id="gradNavy" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1B365D" />
      <stop offset="100%" stop-color="#122540" />
    </linearGradient>
    <linearGradient id="gradBlue" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#284B78" />
      <stop offset="100%" stop-color="#1C3555" />
    </linearGradient>
    <linearGradient id="gradGold" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#E5A632" />
      <stop offset="100%" stop-color="#C28414" />
    </linearGradient>
    <linearGradient id="gradEnc" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#4A6B82" />
      <stop offset="100%" stop-color="#375163" />
    </linearGradient>
    <linearGradient id="gradLight" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#F8FAFC" />
      <stop offset="100%" stop-color="#EDF2F7" />
    </linearGradient>
  </defs>

  <!-- Cabeçalho do Diagrama -->
  <rect x="0" y="0" width="1200" height="70" fill="url(#gradNavy)" />
  <text x="600" y="32" font-size="20" font-weight="bold" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">ORGANOGRAMA EXECUTIVO &amp; ESTRUTURA FUNCIONAL DE CAMPO</text>
  <text x="600" y="55" font-size="13" fill="#D99B26" text-anchor="middle">{subtitulo_xml}</text>

  <!-- LINHAS DE CONEXÃO -->
  <!-- Linha Central Sede -> Residente -->
  <path d="M 600 150 L 600 230" stroke="#1B365D" stroke-width="3" fill="none" />
  <!-- Linhas Laterais Staff -> Residente -->
  <path d="M 270 145 L 270 180 L 600 180" stroke="#718096" stroke-width="2" stroke-dasharray="5,5" fill="none" />
  <path d="M 930 145 L 930 180 L 600 180" stroke="#718096" stroke-width="2" stroke-dasharray="5,5" fill="none" />
  
  <!-- Linha Residente -> Nível Supervisão (TST, Mestre, Almoxarife) -->
  <path d="M 600 310 L 600 370" stroke="#1B365D" stroke-width="3" fill="none" />
  <path d="M 270 370 L 930 370" stroke="#1B365D" stroke-width="3" fill="none" />
  <path d="M 270 370 L 270 410" stroke="#1B365D" stroke-width="3" fill="none" />
  <path d="M 600 370 L 600 410" stroke="#1B365D" stroke-width="3" fill="none" />
  <path d="M 930 370 L 930 410" stroke="#1B365D" stroke-width="3" fill="none" />

  <!-- Linha Mestre -> 3 Encarregados de Frente -->
  <path d="M 600 490 L 600 550" stroke="#1B365D" stroke-width="3" fill="none" />
  <path d="M 220 550 L 980 550" stroke="#1B365D" stroke-width="3" fill="none" />
  <path d="M 220 550 L 220 590" stroke="#1B365D" stroke-width="3" fill="none" />
  <path d="M 600 550 L 600 590" stroke="#1B365D" stroke-width="3" fill="none" />
  <path d="M 980 550 L 980 590" stroke="#1B365D" stroke-width="3" fill="none" />

  <!-- Linhas Encarregados -> Equipes de Produção -->
  <path d="M 220 665 L 220 710" stroke="#4A6B82" stroke-width="2" fill="none" />
  <path d="M 600 665 L 600 710" stroke="#4A6B82" stroke-width="2" fill="none" />
  <path d="M 980 665 L 980 710" stroke="#4A6B82" stroke-width="2" fill="none" />
  <path d="M 930 490 L 930 515 L 1100 515 L 1100 750" stroke="#718096" stroke-width="2" stroke-dasharray="4,4" fill="none" />

  <!-- ==================== NÍVEL 1: DIRETORIA & STAFF ==================== -->
  <!-- Diretoria (Centro) -->
  <g filter="url(#shadow)">
    <rect x="440" y="90" width="320" height="60" rx="8" fill="url(#gradNavy)" />
    <text x="600" y="115" font-size="14" font-weight="bold" fill="#FFFFFF" text-anchor="middle">DIRETORIA DE OPERAÇÕES</text>
    <text x="600" y="135" font-size="11" fill="#E2E8F0" text-anchor="middle">Sponsor Executivo &amp; Gestão Contratual</text>
  </g>

  <!-- PMO Virtual (Esquerda) -->
  <g filter="url(#shadow)">
    <rect x="120" y="95" width="300" height="50" rx="6" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1.5" />
    <text x="270" y="117" font-size="12" font-weight="bold" fill="#1E293B" text-anchor="middle">PMO VIRTUAL &amp; CONTROLADORIA</text>
    <text x="270" y="133" font-size="10" fill="#64748B" text-anchor="middle">Planejamento, Custos &amp; Curva S (Backoffice)</text>
  </g>

  <!-- Suprimentos (Direita) -->
  <g filter="url(#shadow)">
    <rect x="780" y="95" width="300" height="50" rx="6" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1.5" />
    <text x="930" y="117" font-size="12" font-weight="bold" fill="#1E293B" text-anchor="middle">COORDENAÇÃO DE SUPRIMENTOS</text>
    <text x="930" y="133" font-size="10" fill="#64748B" text-anchor="middle">Compras &amp; Logística Portuária (Sede)</text>
  </g>

  <!-- ==================== NÍVEL 2: GESTÃO DE CAMPO (ENGENHEIRO RESIDENTE) ==================== -->
  <g filter="url(#shadow)">
    <rect x="380" y="230" width="440" height="80" rx="8" fill="url(#gradBlue)" stroke="#1B365D" stroke-width="2" />
    <rect x="380" y="230" width="440" height="26" rx="8" fill="#1B365D" />
    <text x="600" y="248" font-size="13" font-weight="bold" fill="#D99B26" text-anchor="middle">RESPONSÁVEL TÉCNICO LEGAL — CREA/CAU</text>
    <text x="600" y="278" font-size="16" font-weight="bold" fill="#FFFFFF" text-anchor="middle">ENGENHEIRO RESIDENTE DE OBRA</text>
    <text x="600" y="298" font-size="11" fill="#E2E8F0" text-anchor="middle">{dedicacao_eng_xml}</text>
  </g>

  <!-- ==================== NÍVEL 3: SUPERVISÃO OPERACIONAL ==================== -->
  <!-- TST (Esquerda) -->
  <g filter="url(#shadow)">
    <rect x="120" y="410" width="300" height="80" rx="6" fill="url(#gradGold)" />
    <text x="270" y="435" font-size="14" font-weight="bold" fill="#FFFFFF" text-anchor="middle">SEGURANÇA &amp; MEIO AMB. (TST)</text>
    <text x="270" y="455" font-size="11" fill="#FFFFFF" text-anchor="middle">Técnico de Segurança do Trabalho (100%)</text>
    <text x="270" y="475" font-size="10" font-weight="bold" fill="#1B365D" text-anchor="middle">NR-18 • NR-35 • Stop Work Authority</text>
  </g>

  <!-- Mestre de Obras (Centro) -->
  <g filter="url(#shadow)">
    <rect x="440" y="410" width="320" height="80" rx="6" fill="url(#gradBlue)" stroke="#1B365D" stroke-width="2" />
    <text x="600" y="435" font-size="15" font-weight="bold" fill="#FFFFFF" text-anchor="middle">MESTRE DE OBRAS GERAL</text>
    <text x="600" y="455" font-size="11" fill="#D99B26" text-anchor="middle">Dedicação 100% Presencial (EAP 1.0.1)</text>
    <text x="600" y="475" font-size="10" fill="#E2E8F0" text-anchor="middle">Coordenação de Produção, Frentes e Prazos</text>
  </g>

  <!-- Almoxarife & Apontador (Direita) -->
  <g filter="url(#shadow)">
    <rect x="780" y="410" width="300" height="80" rx="6" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1.5" />
    <text x="930" y="435" font-size="13" font-weight="bold" fill="#1E293B" text-anchor="middle">ALMOXARIFADO &amp; APONTAMENTO</text>
    <text x="930" y="455" font-size="11" fill="#475569" text-anchor="middle">Almoxarife / Apontador de Campo (100%)</text>
    <text x="930" y="475" font-size="10" fill="#64748B" text-anchor="middle">Recebimento NFs, Estoques e FVS de Insumos</text>
  </g>

  <!-- ==================== NÍVEL 4: LÍDERES DE FRENTE ==================== -->
  <!-- Líder Civil -->
  <g filter="url(#shadow)">
    <rect x="70" y="590" width="300" height="75" rx="6" fill="url(#gradEnc)" />
    <text x="220" y="615" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">ENCARREGADO DE OBRAS CIVIS</text>
    <text x="220" y="635" font-size="10" fill="#E2E8F0" text-anchor="middle">Fundações, Estrutura, Alvenaria e Reboco</text>
    <text x="220" y="653" font-size="10" fill="#D99B26" text-anchor="middle">Portões 1, 2 e 3 (Fechamento)</text>
  </g>

  <!-- Líder Instalações -->
  <g filter="url(#shadow)">
    <rect x="450" y="590" width="300" height="75" rx="6" fill="url(#gradEnc)" />
    <text x="600" y="615" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">ENCARREGADO DE INSTALAÇÕES</text>
    <text x="600" y="635" font-size="10" fill="#E2E8F0" text-anchor="middle">Elétrica, SPDA, Hidráulica, Telecom &amp; HVAC</text>
    <text x="600" y="653" font-size="10" fill="#D99B26" text-anchor="middle">Teste Hidrostático 72h e Comissionamento</text>
  </g>

  <!-- Líder Acabamentos -->
  <g filter="url(#shadow)">
    <rect x="830" y="590" width="300" height="75" rx="6" fill="url(#gradEnc)" />
    <text x="980" y="615" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">ENCARREGADO DE ACABAMENTOS</text>
    <text x="980" y="635" font-size="10" fill="#E2E8F0" text-anchor="middle">Porcelanato, Esquadrias, Vidros e Pintura</text>
    <text x="980" y="653" font-size="10" fill="#D99B26" text-anchor="middle">Portão 4 e Proteção de Pisos</text>
  </g>

  <!-- ==================== NÍVEL 5: EQUIPES DE PRODUÇÃO DIRETA ==================== -->
  <!-- Equipe Civil -->
  <g filter="url(#shadow)">
    <rect x="70" y="710" width="300" height="210" rx="6" fill="url(#gradLight)" stroke="#CBD5E1" stroke-width="1.5" />
    <rect x="70" y="710" width="300" height="26" rx="6" fill="#4A6B82" />
    <text x="220" y="728" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">EQUIPE CIVIL (Pico: 14 operários)</text>
    <text x="85" y="755" font-size="11" fill="#1E293B">• Pedreiros Oficiais (2 a 5 profissionais)</text>
    <text x="85" y="775" font-size="11" fill="#1E293B">• Carpinteiros de Fôrmas (4 profissionais)</text>
    <text x="85" y="795" font-size="11" fill="#1E293B">• Armadores de Aço CA-50 (2 a 3 profissionais)</text>
    <text x="85" y="815" font-size="11" fill="#1E293B">• Montadores Cobertura Sandwich (3 prof.)</text>
    <text x="85" y="835" font-size="11" fill="#1E293B">• Serventes de Apoio Civil (2 a 5 prof.)</text>
    <text x="85" y="855" font-size="11" fill="#1E293B">• Operador de Retroescavadeira (M1)</text>
    <rect x="85" y="875" width="270" height="30" rx="4" fill="#E2E8F0" />
    <text x="220" y="895" font-size="10" font-weight="bold" fill="#284B78" text-anchor="middle">Média: 9 operários diretos</text>
  </g>

  <!-- Equipe Instalações -->
  <g filter="url(#shadow)">
    <rect x="450" y="710" width="300" height="210" rx="6" fill="url(#gradLight)" stroke="#CBD5E1" stroke-width="1.5" />
    <rect x="450" y="710" width="300" height="26" rx="6" fill="#4A6B82" />
    <text x="600" y="728" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">EQUIPE INSTALAÇÕES (Pico: 6 operários)</text>
    <text x="465" y="755" font-size="11" fill="#1E293B">• Eletricistas Instaladores (2 profissionais)</text>
    <text x="465" y="775" font-size="11" fill="#1E293B">• Encanadores Hidráulicos (1 a 2 prof.)</text>
    <text x="465" y="795" font-size="11" fill="#1E293B">• Mecânicos de Refrigeração HVAC (2 prof.)</text>
    <text x="465" y="815" font-size="11" fill="#1E293B">• Técnicos de Cabeamento UTP Cat6</text>
    <text x="465" y="835" font-size="11" fill="#1E293B">• Instrumentistas de Testes e Vácuo</text>
    <rect x="465" y="875" width="270" height="30" rx="4" fill="#E2E8F0" />
    <text x="600" y="895" font-size="10" font-weight="bold" fill="#284B78" text-anchor="middle">Atuação concentrada: M4 a M6</text>
  </g>

  <!-- Equipe Acabamentos & Apoio -->
  <g filter="url(#shadow)">
    <rect x="830" y="710" width="300" height="210" rx="6" fill="url(#gradLight)" stroke="#CBD5E1" stroke-width="1.5" />
    <rect x="830" y="710" width="300" height="26" rx="6" fill="#4A6B82" />
    <text x="980" y="728" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">EQUIPE ACABAMENTOS &amp; APOIO</text>
    <text x="845" y="755" font-size="11" fill="#1E293B">• Ladrilhistas Porcelanato 60x60 (3 prof.)</text>
    <text x="845" y="775" font-size="11" fill="#1E293B">• Pintores Acrílicos e Massistas (1 a 4 prof.)</text>
    <text x="845" y="795" font-size="11" fill="#1E293B">• Marceneiros de Portas/Esquadrias (2 prof.)</text>
    <text x="845" y="815" font-size="11" fill="#1E293B">• Auxiliares de Limpeza Fina Pós-Obra (2 prof.)</text>
    <text x="845" y="835" font-size="11" fill="#1E293B">• Vigia Noturno Patrimonial (1 prof. fixo)</text>
    <rect x="845" y="875" width="270" height="30" rx="4" fill="#E2E8F0" />
    <text x="980" y="895" font-size="10" font-weight="bold" fill="#284B78" text-anchor="middle">Atuação concentrada: M5 e M6</text>
  </g>
</svg>
"""
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"-> SVG vetorial gerado: {svg_path}")

# ==============================================================================
# 2. GERAÇÃO EM PNG DE ALTA RESOLUÇÃO VIA PILLOW (PIL)
# ==============================================================================
def gerar_png(png_path, info):
    width, height = 1200, 960
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Cores
    c_navy = (27, 54, 93)
    c_blue = (40, 75, 120)
    c_gold = (217, 155, 38)
    c_enc = (74, 107, 130)
    c_gray_bg = (248, 250, 252)
    c_line = (27, 54, 93)
    c_line_dash = (148, 163, 184)
    c_border = (203, 213, 225)
    c_text_dark = (30, 41, 59)
    c_text_muted = (100, 116, 139)
    
    # Fontes padrão
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 20)
        font_sub = ImageFont.truetype("arial.ttf", 13)
        font_box_title = ImageFont.truetype("arialbd.ttf", 14)
        font_box_sub = ImageFont.truetype("arial.ttf", 11)
        font_box_desc = ImageFont.truetype("arial.ttf", 10)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_box_title = ImageFont.load_default()
        font_box_sub = ImageFont.load_default()
        font_box_desc = ImageFont.load_default()

    # Barra de Título
    draw.rectangle([(0, 0), (width, 70)], fill=c_navy)
    draw.text((width // 2, 22), "ORGANOGRAMA EXECUTIVO & ESTRUTURA FUNCIONAL DE CAMPO", fill=(255, 255, 255), font=font_title, anchor="mm")
    draw.text((width // 2, 50), info["subtitulo"], fill=c_gold, font=font_sub, anchor="mm")

    # Linhas de Conexão
    draw.line([(600, 150), (600, 230)], fill=c_line, width=3)
    draw.line([(270, 145), (270, 180)], fill=c_line_dash, width=2)
    draw.line([(270, 180), (600, 180)], fill=c_line_dash, width=2)
    draw.line([(930, 145), (930, 180)], fill=c_line_dash, width=2)
    draw.line([(930, 180), (600, 180)], fill=c_line_dash, width=2)

    draw.line([(600, 310), (600, 370)], fill=c_line, width=3)
    draw.line([(270, 370), (930, 370)], fill=c_line, width=3)
    draw.line([(270, 370), (270, 410)], fill=c_line, width=3)
    draw.line([(600, 370), (600, 410)], fill=c_line, width=3)
    draw.line([(930, 370), (930, 410)], fill=c_line, width=3)

    draw.line([(600, 490), (600, 550)], fill=c_line, width=3)
    draw.line([(220, 550), (980, 550)], fill=c_line, width=3)
    draw.line([(220, 550), (220, 590)], fill=c_line, width=3)
    draw.line([(600, 550), (600, 590)], fill=c_line, width=3)
    draw.line([(980, 550), (980, 590)], fill=c_line, width=3)

    draw.line([(220, 665), (220, 710)], fill=c_enc, width=2)
    draw.line([(600, 665), (600, 710)], fill=c_enc, width=2)
    draw.line([(980, 665), (980, 710)], fill=c_enc, width=2)

    # Nível 1: Diretoria
    draw.rounded_rectangle([(440, 90), (760, 150)], radius=8, fill=c_navy)
    draw.text((600, 110), "DIRETORIA DE OPERAÇÕES", fill=(255, 255, 255), font=font_box_title, anchor="mm")
    draw.text((600, 130), "Sponsor Executivo & Gestão Contratual", fill=(226, 232, 240), font=font_box_sub, anchor="mm")

    # Staff PMO
    draw.rounded_rectangle([(120, 95), (420, 145)], radius=6, fill=c_gray_bg, outline=c_border, width=2)
    draw.text((270, 112), "PMO VIRTUAL & CONTROLADORIA", fill=c_text_dark, font=font_box_title, anchor="mm")
    draw.text((270, 130), "Planejamento, Custos & Curva S (Backoffice)", fill=c_text_muted, font=font_box_desc, anchor="mm")

    # Staff Suprimentos
    draw.rounded_rectangle([(780, 95), (1080, 145)], radius=6, fill=c_gray_bg, outline=c_border, width=2)
    draw.text((930, 112), "COORDENAÇÃO DE SUPRIMENTOS", fill=c_text_dark, font=font_box_title, anchor="mm")
    draw.text((930, 130), "Compras & Logística Portuária (Sede)", fill=c_text_muted, font=font_box_desc, anchor="mm")

    # Nível 2: Engenheiro Residente
    draw.rounded_rectangle([(380, 230), (820, 310)], radius=8, fill=c_blue, outline=c_navy, width=2)
    draw.rounded_rectangle([(380, 230), (820, 256)], radius=6, fill=c_navy)
    draw.text((600, 243), "RESPONSÁVEL TÉCNICO LEGAL — CREA/CAU", fill=c_gold, font=font_box_desc, anchor="mm")
    draw.text((600, 273), "ENGENHEIRO RESIDENTE DE OBRA", fill=(255, 255, 255), font=font_box_title, anchor="mm")
    draw.text((600, 295), info["dedicacao_eng"], fill=(226, 232, 240), font=font_box_desc, anchor="mm")

    # Nível 3: Supervisores
    # TST
    draw.rounded_rectangle([(120, 410), (420, 490)], radius=6, fill=c_gold)
    draw.text((270, 430), "SEGURANÇA & MEIO AMB. (TST)", fill=(255, 255, 255), font=font_box_title, anchor="mm")
    draw.text((270, 452), "Técnico de Seg. do Trabalho (100%)", fill=(255, 255, 255), font=font_box_sub, anchor="mm")
    draw.text((270, 472), "NR-18 • NR-35 • Stop Work Authority", fill=c_navy, font=font_box_desc, anchor="mm")

    # Mestre
    draw.rounded_rectangle([(440, 410), (760, 490)], radius=6, fill=c_blue, outline=c_navy, width=2)
    draw.text((600, 430), "MESTRE DE OBRAS GERAL", fill=(255, 255, 255), font=font_box_title, anchor="mm")
    draw.text((600, 452), "Dedicação 100% Presencial (EAP 1.0.1)", fill=c_gold, font=font_box_sub, anchor="mm")
    draw.text((600, 472), "Coordenação de Produção, Frentes e Prazos", fill=(226, 232, 240), font=font_box_desc, anchor="mm")

    # Almoxarife
    draw.rounded_rectangle([(780, 410), (1080, 490)], radius=6, fill=c_gray_bg, outline=c_border, width=2)
    draw.text((930, 430), "ALMOXARIFADO & APONTAMENTO", fill=c_text_dark, font=font_box_title, anchor="mm")
    draw.text((930, 452), "Almoxarife / Apontador de Campo (100%)", fill=c_text_muted, font=font_box_sub, anchor="mm")
    draw.text((930, 472), "Recebimento NFs, Estoques e FVS de Insumos", fill=c_text_muted, font=font_box_desc, anchor="mm")

    # Nível 4: Encarregados
    enc_data = [
        (70, 220, "ENCARREGADO DE OBRAS CIVIS", "Fundações, Estrutura, Alvenaria e Reboco", "Portões 1, 2 e 3 (Fechamento)"),
        (450, 600, "ENCARREGADO DE INSTALAÇÕES", "Elétrica, SPDA, Hidráulica, Telecom & HVAC", "Teste Hidrostático 72h e Comissionamento"),
        (830, 980, "ENCARREGADO DE ACABAMENTOS", "Porcelanato, Esquadrias, Vidros e Pintura", "Portão 4 e Proteção de Pisos"),
    ]
    for x1, cx, t1, t2, t3 in enc_data:
        draw.rounded_rectangle([(x1, 590), (x1 + 300, 665)], radius=6, fill=c_enc)
        draw.text((cx, 610), t1, fill=(255, 255, 255), font=font_box_title, anchor="mm")
        draw.text((cx, 630), t2, fill=(226, 232, 240), font=font_box_desc, anchor="mm")
        draw.text((cx, 648), t3, fill=c_gold, font=font_box_desc, anchor="mm")

    # Nível 5: Blocos de Equipes
    draw.rounded_rectangle([(70, 710), (370, 920)], radius=6, fill=c_gray_bg, outline=c_border, width=2)
    draw.rounded_rectangle([(70, 710), (370, 736)], radius=6, fill=c_enc)
    draw.text((220, 723), "EQUIPE CIVIL (Pico: 14 operários)", fill=(255, 255, 255), font=font_box_sub, anchor="mm")
    textos_civil = [
        "• Pedreiros Oficiais (2 a 5 profissionais)",
        "• Carpinteiros de Fôrmas (4 profissionais)",
        "• Armadores de Aço CA-50 (2 a 3 prof.)",
        "• Montadores Cobertura Sandwich (3 prof.)",
        "• Serventes de Apoio Civil (2 a 5 prof.)",
        "• Operador de Retroescavadeira (M1)",
    ]
    y = 755
    for txt in textos_civil:
        draw.text((85, y), txt, fill=c_text_dark, font=font_box_desc)
        y += 18
    draw.rounded_rectangle([(85, 875), (355, 905)], radius=4, fill=(226, 232, 240))
    draw.text((220, 890), "Média: 9 operários diretos", fill=c_blue, font=font_box_desc, anchor="mm")

    # Equipe Instalações
    draw.rounded_rectangle([(450, 710), (750, 920)], radius=6, fill=c_gray_bg, outline=c_border, width=2)
    draw.rounded_rectangle([(450, 710), (750, 736)], radius=6, fill=c_enc)
    draw.text((600, 723), "EQUIPE INSTALAÇÕES (Pico: 6 operários)", fill=(255, 255, 255), font=font_box_sub, anchor="mm")
    textos_inst = [
        "• Eletricistas Instaladores (2 profissionais)",
        "• Encanadores Hidráulicos (1 a 2 prof.)",
        "• Mecânicos de Climatização HVAC (2 prof.)",
        "• Técnicos de Cabeamento UTP Cat6",
        "• Instrumentistas de Testes e Vácuo",
    ]
    y = 755
    for txt in textos_inst:
        draw.text((465, y), txt, fill=c_text_dark, font=font_box_desc)
        y += 18
    draw.rounded_rectangle([(465, 875), (735, 905)], radius=4, fill=(226, 232, 240))
    draw.text((600, 890), "Atuação concentrada: M4 a M6", fill=c_blue, font=font_box_desc, anchor="mm")

    # Equipe Acabamentos
    draw.rounded_rectangle([(830, 710), (1130, 920)], radius=6, fill=c_gray_bg, outline=c_border, width=2)
    draw.rounded_rectangle([(830, 710), (1130, 736)], radius=6, fill=c_enc)
    draw.text((980, 723), "EQUIPE ACABAMENTOS & APOIO", fill=(255, 255, 255), font=font_box_sub, anchor="mm")
    textos_acab = [
        "• Ladrilhistas Porcelanato 60x60 (3 prof.)",
        "• Pintores Acrílicos e Massistas (1 a 4 prof.)",
        "• Marceneiros Portas/Esquadrias (2 prof.)",
        "• Auxiliares Limpeza Pós-Obra (2 prof.)",
        "• Vigia Noturno Patrimonial (1 prof. fixo)",
    ]
    y = 755
    for txt in textos_acab:
        draw.text((845, y), txt, fill=c_text_dark, font=font_box_desc)
        y += 18
    draw.rounded_rectangle([(845, 875), (1115, 905)], radius=4, fill=(226, 232, 240))
    draw.text((980, 890), "Atuação concentrada: M5 e M6", fill=c_blue, font=font_box_desc, anchor="mm")

    img.save(png_path, "PNG", quality=95)
    print(f"-> PNG de alta resolução gerado: {png_path}")

def gerar_organograma(obra_nome="OBRA_TMULT", custom_dir=None):
    base_repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if custom_dir:
        proj_dir = os.path.abspath(custom_dir)
        obra_id = os.path.basename(proj_dir)
    elif obra_nome:
        proj_dir = os.path.join(base_repo_dir, "projetos", obra_nome)
        obra_id = obra_nome
    else:
        proj_dir = os.path.join(base_repo_dir, "projetos", "OBRA_TMULT")
        obra_id = "OBRA_TMULT"

    if not os.path.exists(proj_dir):
        raise FileNotFoundError(f"Diretório da obra não encontrado: {proj_dir}")

    output_dir = os.path.join(proj_dir, "06_SST_E_RH")
    os.makedirs(output_dir, exist_ok=True)

    info = obter_dados_obra(proj_dir, obra_id)
    sigla = info["sigla_obra"]

    png_path = os.path.join(output_dir, f"ORGANOGRAMA_{sigla}.png")
    svg_path = os.path.join(output_dir, f"ORGANOGRAMA_{sigla}.svg")

    print(f"\n=======================================================")
    print(f"Gerando Organograma Executivo: {info['nome_obra']}")
    print(f"Destino: {output_dir}")
    print(f"=======================================================")

    gerar_svg(svg_path, info)
    gerar_png(png_path, info)
    print("✅ Organograma visual gerado com sucesso!\n")

    return {
        "png_path": png_path,
        "svg_path": svg_path
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motor Universal de Organograma Executivo Multi-Obra")
    parser.add_argument("--obra", default="OBRA_TMULT", help="Nome da pasta da obra em /projetos/ (default: OBRA_TMULT)")
    parser.add_argument("--dir", help="Caminho direto para a pasta da obra")
    args = parser.parse_args()

    gerar_organograma(obra_nome=args.obra, custom_dir=args.dir)
