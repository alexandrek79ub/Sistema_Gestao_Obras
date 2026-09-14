#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Catálogo Canônico e Governança da EAP de Serviços da Plataforma de Gestão de Obras.

Fonte da Verdade:
- governanca/INDICE_MESTRE_SKILLS.md (Seção 1.1 - Cadeia Global Integrada Níveis 1.1 a 5.1 e 4 Portões)
- Tabelas Disciplinares Oficiais de Serviços:
  * SKILL_QUANT_06 (§1.5 - Níveis 1.1, 1.2, 4.1, 4.2 e 5.1)
  * SKILL_QUANT_01 (§1.2 - Nível 1.3 Infraestrutura e Fundações)
  * SKILL_QUANT_02 (§4.1 - Nível 1.4 Superestrutura)
  * SKILL_QUANT_03 / 03A / 03B / 03C (§2 - Níveis 2.1 Alvenaria/Acabamentos Internos e 2.2 Cobertura/Fachadas)
  * SKILL_QUANT_04 (§3 - Nível 3.1 Instalações Elétricas e SPDA)
  * SKILL_QUANT_05 (§3 - Nível 3.2 Instalações Hidrossanitárias e Gás)

Diretrizes Vinculantes da Decisão de Governança:
1. Preservar a regra funcional de engenharia do portão de acabamento (1ª demão de pintura libera dispositivos de acabamento).
2. Utilizar a taxonomia das tabelas disciplinares atuais como referência para a EAP de serviço (2.1.8 = Pintura Interna).
3. Segregar rigorosamente CODIGO_EAP_SERVICO de códigos legados de insumo/BOM e contratuais/históricos.
4. Não renumerar automaticamente dados existentes; preservar códigos legados para rastreabilidade.
5. Código desconhecido gera diagnóstico explícito, nunca caindo silenciosamente em distribuição genérica.
"""

import re
from typing import Dict, List, Optional, Tuple, Any

# =============================================================================
# MACROETAPAS CANÔNICAS DA EAP DE SERVIÇOS (NÍVEIS 1.1 A 5.1 + 1.0 ADM)
# =============================================================================

MACROETAPAS_EAP: Dict[str, Dict[str, str]] = {
    "1.0": {
        "disciplina": "Administração Local e Canteiro",
        "skill_origem": "AGENTS.md / SKILL_ADM",
        "unidade_avanco": "mês",
        "descricao": "Equipe de gestão, vivência, instalações provisórias e mobilização contínua"
    },
    "1.1": {
        "disciplina": "Serviços Preliminares, Legalização e Mobilização",
        "skill_origem": "SKILL_QUANT_06",
        "unidade_avanco": "un / m",
        "descricao": "Marco Zero, projetos, licenças, tapumes e locação inicial"
    },
    "1.2": {
        "disciplina": "Terraplenagem e Obras de Contenção",
        "skill_origem": "SKILL_QUANT_06",
        "unidade_avanco": "m² / m³",
        "descricao": "Cortes, aterros, bota-fora e conformação de platôs"
    },
    "1.3": {
        "disciplina": "Infraestrutura e Fundações",
        "skill_origem": "SKILL_QUANT_01",
        "unidade_avanco": "m / m³ / kg",
        "descricao": "Estacas, tubulões, blocos de coroamento, vigas baldrame e impermeabilização"
    },
    "1.4": {
        "disciplina": "Superestrutura",
        "skill_origem": "SKILL_QUANT_02",
        "unidade_avanco": "m² / m³ / kg",
        "descricao": "Pilares, vigas, lajes, formas, armaduras, concreto e desforma"
    },
    "2.1": {
        "disciplina": "Alvenaria, Vedações Verticais e Acabamentos Internos",
        "skill_origem": "SKILL_QUANT_03",
        "unidade_avanco": "m² / m / conj",
        "descricao": "Alvenaria de vedação, chapisco, emboço, contrapiso, pisos cerâmicos, impermeabilização molhada, esquadrias e pintura interna"
    },
    "2.2": {
        "disciplina": "Cobertura, Fachadas e Fechamento Externo",
        "skill_origem": "SKILL_QUANT_03C",
        "unidade_avanco": "m² / m / kg",
        "descricao": "Estrutura e telhas de cobertura, calhas, rufos, platibanda, revestimento de fachada e pavimentação externa"
    },
    "3.1": {
        "disciplina": "Instalações Elétricas, Telecomunicações e SPDA",
        "skill_origem": "SKILL_QUANT_04",
        "unidade_avanco": "m / un / pt",
        "descricao": "Eletrodutos embutidos, caixas, cabeamento, alimentadores, quadros, dispositivos finais e testes"
    },
    "3.2": {
        "disciplina": "Instalações Hidrossanitárias, Gás e Drenagem",
        "skill_origem": "SKILL_QUANT_05",
        "unidade_avanco": "m / un / pt",
        "descricao": "Redes enterradas, caixas, ramais de água e esgoto, teste hidrostático, prumadas e metais/louças"
    },
    "4.1": {
        "disciplina": "Sistemas Especiais",
        "skill_origem": "SKILL_QUANT_06",
        "unidade_avanco": "un / m",
        "descricao": "HVAC, elevadores, pressurização, bombas de recalque e SDAI"
    },
    "4.2": {
        "disciplina": "Urbanização Externa e Lazer",
        "skill_origem": "SKILL_QUANT_06",
        "unidade_avanco": "m² / un",
        "descricao": "Paisagismo, piscinas, vias, acessibilidade e muros de divisa"
    },
    "5.1": {
        "disciplina": "Encerramento, Comissionamento e Databook",
        "skill_origem": "SKILL_QUANT_06",
        "unidade_avanco": "un / m²",
        "descricao": "Limpeza pós-obra, testes finais integrados, as-built, vistoria e entrega técnica"
    }
}

# =============================================================================
# OS 4 PORTÕES INTERDISCIPLINARES BLOQUEANTES DA ENGENHARIA
# =============================================================================

PORTAO_1_FUNDACAO = {
    "id": "PORTAO_01_FUNDACAO",
    "nome": "Portão Geotécnico e Fundação (Impermeabilização -> Reaterro)",
    "bloqueadora": "1.3.11",  # Impermeabilização de baldrames/blocos
    "bloqueada": "1.3.13",    # Reaterro de valas
    "descricao": "É proibido aterrar valas e blocos antes da impermeabilização hidrófuga inspecionada e liberada."
}

PORTAO_2_ESTRUTURA = {
    "id": "PORTAO_02_ESTRUTURA_PRUMADAS",
    "nome": "Portão Estrutura -> Prumadas Verticais (Desforma de Laje -> Shafts)",
    "bloqueadora": "1.4.12",  # Desforma total de lajes
    "bloqueadas": ["3.1.7", "3.2.8"],  # Prumadas elétricas e prumadas de esgoto/água em shafts
    "descricao": "Prumadas em shafts verticais exigem desforma total do pavimento superior para eliminar riscos de queda."
}

PORTAO_3_HIDRAULICA = {
    "id": "PORTAO_03_TESTE_HIDROSTATICO",
    "nome": "Portão Hidráulico -> Fechamento Civil [REGRA DE OURO]",
    "bloqueadora": "3.2.7",   # Teste Hidrostático sob pressão 72h
    "bloqueadas": ["2.1.2", "2.1.3"],  # Chapisco e Emboço/Reboco
    "descricao": "Nunca chapiscar ou emboçar paredes sobre tubulações sem aprovação do Teste Hidrostático 72h."
}

PORTAO_4_ACABAMENTO = {
    "id": "PORTAO_04_ACABAMENTO_PROTEGIDO",
    "nome": "Portão Civil -> Dispositivos de Acabamento",
    "bloqueadora": "2.1.8",   # 1ª Demão de Pintura Interna (com proteção de pisos)
    "bloqueadas": ["3.1.9", "3.1.11", "3.2.10", "3.2.11"],  # Tomadas/espelhos, luminárias, louças e metais nobres
    "descricao": "Dispositivos de acabamento fino só podem ser instalados após a 1ª demão de pintura e proteção de piso."
}

PORTÕES_OFICIAIS = [
    PORTAO_1_FUNDACAO,
    PORTAO_2_ESTRUTURA,
    PORTAO_3_HIDRAULICA,
    PORTAO_4_ACABAMENTO
]

# =============================================================================
# FUNÇÕES DE CLASSIFICAÇÃO E DIAGNÓSTICO
# =============================================================================

def normalizar_codigo_eap(codigo: Any) -> str:
    """Normaliza o código EAP removendo espaços e caracteres espúrios."""
    if codigo is None:
        return ""
    cod = str(codigo).strip()
    return cod


def obter_macroetapa(codigo: str) -> Optional[str]:
    """Extrai o prefixo de macroetapa (ex: '1.3' a partir de '1.3.11' ou '1.3')."""
    cod = normalizar_codigo_eap(codigo)
    partes = cod.split('.')
    if len(partes) >= 2:
        prefixo = f"{partes[0]}.{partes[1]}"
        if prefixo in MACROETAPAS_EAP:
            return prefixo
    elif len(partes) == 1 and partes[0]:
        # Suporte a 1.0 se passado como 1
        for macro in MACROETAPAS_EAP:
            if macro.startswith(f"{partes[0]}."):
                return macro
    return None


def classificar_codigo_eap(codigo: str) -> Dict[str, Any]:
    """
    Classifica um código EAP de serviço conforme a governança canônica.
    Retorna diagnóstico explícito caso o código seja desconhecido.
    """
    cod = normalizar_codigo_eap(codigo)
    if not cod:
        return {
            "codigo": cod,
            "valido": False,
            "macroetapa": None,
            "disciplina": None,
            "tipo": "INVALIDO_VAZIO",
            "diagnostico": "Código EAP ausente ou em branco."
        }

    macro = obter_macroetapa(cod)
    if not macro:
        return {
            "codigo": cod,
            "valido": False,
            "macroetapa": None,
            "disciplina": None,
            "tipo": "DESCONHECIDO",
            "diagnostico": f"Código '{cod}' não pertence a nenhuma macroetapa oficial da EAP (1.0 a 5.1)."
        }

    info_macro = MACROETAPAS_EAP[macro]
    return {
        "codigo": cod,
        "valido": True,
        "macroetapa": macro,
        "disciplina": info_macro["disciplina"],
        "skill_origem": info_macro["skill_origem"],
        "unidade_avanco": info_macro["unidade_avanco"],
        "tipo": "CODIGO_EAP_SERVICO",
        "diagnostico": None
    }


def verificar_violacao_portoes(atividades_com_predecessoras: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    """
    Verifica se uma rede de atividades respeita os 4 portões de bloqueio interdisciplinares.
    Retorna a lista de violações encontradas.
    """
    violacoes = []

    # Mapear predecessoras acumuladas / diretas
    for aid, preds in atividades_com_predecessoras.items():
        aid_norm = normalizar_codigo_eap(aid)
        preds_norm = [normalizar_codigo_eap(p) for p in preds]

        # Portão 1: 1.3.13 requer 1.3.11
        if aid_norm == PORTAO_1_FUNDACAO["bloqueada"]:
            if PORTAO_1_FUNDACAO["bloqueadora"] not in preds_norm:
                violacoes.append({
                    "portao": PORTAO_1_FUNDACAO["id"],
                    "tarefa": aid_norm,
                    "bloqueadora_faltante": PORTAO_1_FUNDACAO["bloqueadora"],
                    "motivo": PORTAO_1_FUNDACAO["descricao"]
                })

        # Portão 2: 3.1.7 ou 3.2.8 requerem 1.4.12
        if aid_norm in PORTAO_2_ESTRUTURA["bloqueadas"]:
            if PORTAO_2_ESTRUTURA["bloqueadora"] not in preds_norm:
                violacoes.append({
                    "portao": PORTAO_2_ESTRUTURA["id"],
                    "tarefa": aid_norm,
                    "bloqueadora_faltante": PORTAO_2_ESTRUTURA["bloqueadora"],
                    "motivo": PORTAO_2_ESTRUTURA["descricao"]
                })

        # Portão 3: 2.1.2 ou 2.1.3 requerem 3.2.7
        if aid_norm in PORTAO_3_HIDRAULICA["bloqueadas"]:
            if PORTAO_3_HIDRAULICA["bloqueadora"] not in preds_norm:
                violacoes.append({
                    "portao": PORTAO_3_HIDRAULICA["id"],
                    "tarefa": aid_norm,
                    "bloqueadora_faltante": PORTAO_3_HIDRAULICA["bloqueadora"],
                    "motivo": PORTAO_3_HIDRAULICA["descricao"]
                })

        # Portão 4: 3.1.9, 3.1.11, 3.2.10, 3.2.11 requerem 2.1.8
        if aid_norm in PORTAO_4_ACABAMENTO["bloqueadas"]:
            if PORTAO_4_ACABAMENTO["bloqueadora"] not in preds_norm:
                violacoes.append({
                    "portao": PORTAO_4_ACABAMENTO["id"],
                    "tarefa": aid_norm,
                    "bloqueadora_faltante": PORTAO_4_ACABAMENTO["bloqueadora"],
                    "motivo": PORTAO_4_ACABAMENTO["descricao"]
                })

    return violacoes


def determinar_distribuicao_canonica(
    eap: str,
    prazo_meses: int = 6,
    descricao: str = ""
) -> Tuple[Dict[str, float], Optional[str]]:
    """
    Determina a distribuição mensal (P_M1..P_MN) no cronograma com base no catálogo canônico.
    Substitui regras obsoletas que confundiam infraestrutura (1.1) e superestrutura (1.2).
    Retorna (pesos_meses, aviso_diagnostico).
    """
    eap_norm = normalizar_codigo_eap(eap)
    classificacao = classificar_codigo_eap(eap_norm)
    
    pesos = {f"P_M{m}": 0.0 for m in range(1, prazo_meses + 1)}
    aviso = None

    if not classificacao["valido"]:
        # Não pertencer ao catálogo oficial gera aviso explícito
        aviso = f"Código '{eap_norm}' não catalogado na EAP oficial; alocado com diagnóstico de advertência."
        mid = max(1, prazo_meses // 2)
        pesos[f"P_M{mid}"] = 1.0
        return pesos, aviso

    macro = classificacao["macroetapa"]
    desc_upper = (descricao or "").upper()

    # 1.0 Administração Local e Canteiro: linear em todo o prazo da obra
    if macro == "1.0":
        fator = 1.0 / float(prazo_meses)
        for m in range(1, prazo_meses + 1):
            pesos[f"P_M{m}"] = fator

    # 1.1 Preliminares e Mobilização: Mês 1 (ou M1 e M2 para prazos longos)
    elif macro == "1.1":
        pesos["P_M1"] = 1.0

    # 1.2 Terraplenagem: Início da obra (Mês 1 se prazo curto, ou M1/M2)
    elif macro == "1.2":
        if prazo_meses >= 6:
            pesos["P_M1"] = 0.7
            pesos["P_M2"] = 0.3
        else:
            pesos["P_M1"] = 1.0

    # 1.3 Infraestrutura e Fundações: Mês 1 a Mês 2
    elif macro == "1.3":
        if prazo_meses >= 6:
            pesos["P_M1"] = 0.6
            pesos["P_M2"] = 0.4
        else:
            pesos["P_M1"] = 1.0

    # 1.4 Superestrutura: Mês 2 e Mês 3 (ciclo de estrutura)
    elif macro == "1.4":
        if prazo_meses >= 6:
            pesos["P_M2"] = 0.5
            pesos["P_M3"] = 0.5
        elif prazo_meses >= 3:
            pesos["P_M2"] = 1.0
        else:
            pesos["P_M1"] = 1.0

    # 2.1 Alvenaria e Acabamentos Internos
    elif macro == "2.1":
        if eap_norm.startswith("2.1.1.") or eap_norm == "2.1.1":  # Alvenaria bruta
            pesos["P_M3"] = 1.0
        elif eap_norm.startswith("2.1.2"):  # Chapisco
            pesos["P_M3"] = 0.5
            pesos["P_M4"] = 0.5
        elif eap_norm.startswith("2.1.3"):  # Emboço / Reboco
            pesos["P_M4"] = 1.0
        elif eap_norm.startswith("2.1.4"):  # Contrapiso
            pesos["P_M4"] = 0.5
            pesos["P_M5"] = 0.5
        elif eap_norm.startswith("2.1.11"):  # Impermeabilização molhada
            pesos["P_M4"] = 1.0
        elif eap_norm.startswith("2.1.5") or eap_norm.startswith("2.1.6") or eap_norm.startswith("2.1.7"):  # Pisos e revestimentos
            pesos["P_M5"] = 1.0
        elif eap_norm.startswith("2.1.8"):  # Pintura Interna (2.1.8 conforme tabela disciplinar)
            if "SELADOR" in desc_upper or "LIXA" in desc_upper:
                pesos["P_M5"] = 0.5
                pesos["P_M6"] = 0.5
            else:
                mes_fim = min(6, prazo_meses)
                pesos[f"P_M{mes_fim}"] = 1.0
        elif eap_norm.startswith("2.1.9") or eap_norm.startswith("2.1.10"):  # Esquadrias (portas/janelas)
            pesos["P_M5"] = 1.0
        else:
            mes_alvo = min(5, prazo_meses)
            pesos[f"P_M{mes_alvo}"] = 1.0

    # 2.2 Cobertura e Fachadas Externas
    elif macro == "2.2":
        if eap_norm.startswith("2.2.1") or eap_norm.startswith("2.2.2") or eap_norm.startswith("2.2.5"):  # Cobertura, calhas
            pesos["P_M3"] = 1.0
        elif eap_norm.startswith("2.2.7") or eap_norm.startswith("2.2.8"):  # Revestimento fachada e platibanda
            pesos["P_M4"] = 0.5
            pesos["P_M5"] = 0.5
        elif eap_norm.startswith("2.2.9") or eap_norm.startswith("2.2.10"):  # Muros, portões, pavimentação externa
            pesos["P_M5"] = 0.5
            pesos["P_M6"] = 0.5
        else:
            pesos["P_M4"] = 1.0

    # 3.1 Elétrica, Dados e SPDA
    elif macro == "3.1":
        if any(term in desc_upper for term in ["ELETRODUTO", "CAIXA", "ATERRAMENTO", "RASGO"]):
            pesos["P_M4"] = 1.0
        elif any(term in desc_upper for term in ["CABO", "CONDUTOR", "ENFIACAO", "ALIMENTADOR"]):
            pesos["P_M5"] = 1.0
        elif any(term in desc_upper for term in ["QUADRO", "QDC", "TOMADA", "INTERRUPTOR", "LUMINARIA", "SPDA"]):
            mes_fim = min(6, prazo_meses)
            pesos[f"P_M{mes_fim}"] = 1.0
        else:
            pesos["P_M5"] = 1.0

    # 3.2 Hidráulica, Gás e Drenagem
    elif macro == "3.2":
        if any(term in desc_upper for term in ["TUBO", "ESGOTO", "AGUA", "CONEXAO", "RAMAL", "CAIXA DE GORDURA", "CAIXA DE PASSAGEM"]):
            pesos["P_M4"] = 1.0
        elif any(term in desc_upper for term in ["TESTE", "HIDROSTATICO"]):
            pesos["P_M4"] = 1.0
        elif any(term in desc_upper for term in ["LOUCA", "BACIA", "CUBA", "METAL", "TORNEIRA", "CHUVEIRO", "REGISTRO"]):
            mes_fim = min(6, prazo_meses)
            pesos[f"P_M{mes_fim}"] = 1.0
        else:
            pesos["P_M5"] = 1.0

    # 4.1 e 4.2 Sistemas Especiais e Urbanização
    elif macro in ("4.1", "4.2"):
        mes_target = min(5, prazo_meses)
        pesos[f"P_M{mes_target}"] = 1.0

    # 5.1 Encerramento e Databook: último mês
    elif macro == "5.1":
        pesos[f"P_M{prazo_meses}"] = 1.0

    return pesos, aviso
