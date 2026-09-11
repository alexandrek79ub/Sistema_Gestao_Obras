#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Geração do Caderno de FVS (Fichas de Verificação de Serviço) Bloqueantes.

Uso:
    python scripts/gerar_fvs_bloqueantes.py --obra OBRA_TMULT
    python scripts/gerar_fvs_bloqueantes.py --dir projetos/OBRA_TMULT
"""

import os
import sys
import json
import argparse
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
    parser = argparse.ArgumentParser(description="Motor Universal de FVSs Bloqueantes de Campo.")
    parser.add_argument("--obra", type=str, default="OBRA_TMULT", help="Nome da pasta da obra em projetos/")
    parser.add_argument("--dir", type=str, default=None, help="Caminho direto para a pasta da obra")
    return parser.parse_args()


def carregar_dados_obra(obra_dir):
    config_path = os.path.join(obra_dir, "config_obra.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {
            "nome_obra": os.path.basename(obra_dir),
            "sigla_obra": os.path.basename(obra_dir)[:6].upper()
        }
    return config


def obter_definicoes_fvs(sigla, nome):
    return [
        {
            "codigo": "FVS-01",
            "titulo": "Topografia, Locação de Eixos e Terraplenagem",
            "pop": "POP 21 (Topografia a Laser) e POP 01 (Canteiro Lean)",
            "nbr": "ABNT NBR 13133 (Execução de Levantamento Topográfico)",
            "etapa_obra": "Infraestrutura / Locação de Canteiro",
            "contrato_bloqueado": "SUB-01 (Estrutura e Fundações)",
            "tolerancia": "Erro angular máximo de ± 10\"; Desvio linear máximo em eixos principais de ± 3mm; Nível de cota de fundo de valas com tolerância de ± 10mm.",
            "itens_verificacao": [
                "Locação do gabarito perimetral de tábua corrida fixado com pontaletes travados e pintados",
                "Conferência de esquadro geral da edificação via triangulação 3-4-5 com trena de precisão ou estação total",
                "Cotas de nível e amarração ao marco georreferenciado (RN oficial do empreendimento)",
                "Alinhamento dos eixos de sapatas e arranques de pilares c/ linhas de nylon de alta tenacidade",
                "Compactação e nivelamento da praça de trabalho e valas de circulação de canteiro"
            ],
            "servico_sucessor_bloqueado": "Escavação mecanizada profunda e concretagem de lastro de fundação"
        },
        {
            "codigo": "FVS-02",
            "titulo": "Fundações Isoladas, Estacas e Vigas Baldrames",
            "pop": "POP 10 (Fundações) e POP 14 (Impermeabilização)",
            "nbr": "ABNT NBR 6122 (Projeto e Execução de Fundações) e NBR 9575",
            "etapa_obra": "Infraestrutura / Cavas e Fundações",
            "contrato_bloqueado": "SUB-01 (Medição 01 e 02)",
            "tolerancia": "Espessura mínima de lastro de concreto magro: 50mm; Cobrimento mínimo de armadura em contato c/ solo: 50mm (ou 40mm com lastro brita/concreto magro); Desaprumo em arranques máx. 5mm.",
            "itens_verificacao": [
                "Limpeza e remoção total de terra solta do fundo de cava antes do lastro",
                "Aplicação de concreto magro e=5cm em 100% da área de contato das sapatas",
                "Montagem e estroncamento de fôrmas compensadas de sapatas e baldrames",
                "Posicionamento das armaduras com espaçadores plásticos tipo pastilha de concreto (proibido toco de madeira)",
                "Amarração de arranques de pilares (P1 a P24) com conferência de bitola e transpasse normativo",
                "Impermeabilização de baldrames com 2 demãos cruzadas de emulsão asfáltica elastomérica"
            ],
            "servico_sucessor_bloqueado": "Lançamento de concreto estrutural usinado e reaterro de valas"
        },
        {
            "codigo": "FVS-03",
            "titulo": "Estrutura de Concreto Armado (Pilares, Vigas e Lajes)",
            "pop": "POP 11 (Concretagem), POP 19 (Fôrmas) e POP 22 (Controle de Concreto)",
            "nbr": "ABNT NBR 6118 (Projeto de Estruturas de Concreto) e NBR 14931",
            "etapa_obra": "Supraestrutura",
            "contrato_bloqueado": "SUB-01 (Medição 03 e 04)",
            "tolerancia": "Desaprumo em pilares máximo de 1/500 da altura (máx. 6mm para h=3m); Nivelamento de fundo de vigas máx. L/500; Flecha residual em laje menor que L/350 após desforma.",
            "itens_verificacao": [
                "Estanqueidade das fôrmas, aplicação uniforme de desmoldante biodegradável",
                "Aprumo e travamento vertical dos pilares com escoras metálicas reguláveis push-pull",
                "Limpeza prévia do pé do pilar (janela de inspeção) para remoção de serragem e impurezas",
                "Conferência de armaduras (bitola, quantidade, estribos e cobrimento normativo de 30mm a 40mm)",
                "Teste de abatimento do concreto (Slump test 12 ± 2 cm) no ato do descarregamento",
                "Moldagem obrigatória de 6 corpos de prova por caminhão betoneira (ruptura aos 7, 14 e 28 dias)",
                "Vibração uniforme por camadas sem tocar na armadura e início da cura úmida contínua por 7 dias"
            ],
            "servico_sucessor_bloqueado": "Desforma de fundo de vigas/lajes e início do levantamento de alvenaria"
        },
        {
            "codigo": "FVS-04",
            "titulo": "Alvenaria Estrutural e Alvenaria de Vedação",
            "pop": "POP 12 (Alvenaria e Vedações)",
            "nbr": "ABNT NBR 8545 (Execução de Alvenaria sem Função Estrutural)",
            "etapa_obra": "Vedações e Fechamentos Verticais",
            "contrato_bloqueado": "SUB-02 (Alvenaria e Vedações)",
            "tolerancia": "Desaprumo máximo de 3mm por pavimento; Nivelamento das fiadas com desvio máx. de 3mm em 3 metros; Espessura de junta de argamassa entre 10mm e 15mm.",
            "itens_verificacao": [
                "Locação e marcação da primeira fiada com esquadro e prumo de face perfeitos",
                "Fixação de telas metálicas de amarração alvenaria/pilar galvanizadas a cada 2 fiadas",
                "Execução de vergas e contravergas pré-moldadas em todos os vãos de portas e janelas (transpasse mín. 20cm)",
                "Encunhamento flexível (aperto) com argamassa expansiva ou espuma PU após 14 dias de cura",
                "Amarração em amarração tradicional com traspasse de 1/2 bloco (mínimo 1/3 bloco)",
                "Alinhamento dos shafts e passagens de tubulações sem quebra estrutural indiscriminada"
            ],
            "servico_sucessor_bloqueado": "Aplicação de chapisco, emboço e reboco nas paredes"
        },
        {
            "codigo": "FVS-05",
            "titulo": "Impermeabilização e Teste de Estanqueidade (72 Horas)",
            "pop": "POP 14 (Impermeabilização de Alta Performance)",
            "nbr": "ABNT NBR 9575 (Seleção e Projeto) e NBR 9574 (Execução de Impermeabilização)",
            "etapa_obra": "Áreas Molhadas, Cobertura e Reservatórios",
            "contrato_bloqueado": "SUB-07 (Impermeabilização)",
            "tolerancia": "Caimento mínimo de 1% em direção aos ralos; Meia-cana em cantos vivos raio mín. 5cm; Teste de lâmina d'água de 72 horas com ZERO infiltração ou rebaixamento além da evaporação normal.",
            "itens_verificacao": [
                "Regularização da superfície com argamassa cimento e areia 1:3 e cantos arredondados (meia-cana)",
                "Execução de rebaixo de 1cm em torno de ralos e passagens de tubulações com primer epóxi",
                "Aplicação da membrana/manta conforme especificação técnica e número de demãos cruzadas",
                "Subida da impermeabilização nos rodapés em no mínimo 20cm acima do piso acabado",
                "Enchimento com lâmina d'água de 5cm a 10cm por exatas 72 horas com registro fotográfico e cota de nível",
                "Vistoria na laje inferior/ambiente adjacente comprovando 100% de ausência de umidade ou gotejamento",
                "Aplicação de camada separadora e argamassa de proteção mecânica antes do tráfego"
            ],
            "servico_sucessor_bloqueado": "Instalação de revestimentos cerâmicos, pisos vinílicos e reaterro de baldrames"
        },
        {
            "codigo": "FVS-06",
            "titulo": "Instalações Hidráulicas e Teste Hidrostático sob Pressão",
            "pop": "POP 15 (Instalações Hidrossanitárias)",
            "nbr": "ABNT NBR 5626 (Instalação Predial de Água Fria) e NBR 8160 (Esgoto)",
            "etapa_obra": "Instalações Hidrossanitárias e Incêndio",
            "contrato_bloqueado": "SUB-05 (Instalações Hidráulicas)",
            "tolerancia": "Queda de pressão no teste hidrostático menor que 2% após 1 hora de pressurização contínua a 1,5x a pressão de trabalho (mínimo 60 mca / 6 bar); Declividade mínima em esgoto de 2% para tubos <= 75mm e 1% para 100mm.",
            "itens_verificacao": [
                "Alinhamento, fixação e envelopamento de prumadas e ramais em shafts e alvenarias",
                "Instalação de plugs roscáveis em todos os pontos de utilização antes do teste",
                "Enchimento da rede c/ água eliminando 100% do ar pelas extremidades mais altas",
                "Pressurização com bomba de teste hidrostático e manômetro calibrado (mín. 6 kgf/cm²)",
                "Manutenção da pressão por no mínimo 1 hora sem vazamento em conexões ou soldas",
                "Teste de fumaça / estanqueidade por gravidade na rede de esgoto e ventilação sanitária",
                "Proteção mecânica dos tubos antes do fechamento com reboco"
            ],
            "servico_sucessor_bloqueado": "Chapisco e emboço de alvenarias que contêm tubulações e fechamento de shafts"
        },
        {
            "codigo": "FVS-07",
            "titulo": "Instalações Elétricas, Cabeamento e Malha de Aterramento SPDA",
            "pop": "POP 16 (Instalações Elétricas) e POP 23 (SESMT)",
            "nbr": "ABNT NBR 5410 (Instalações de Baixa Tensão) e NBR 5419 (Proteção SPDA)",
            "etapa_obra": "Instalações Elétricas, Telefonia e SPDA",
            "contrato_bloqueado": "SUB-06 (Instalações Elétricas e SPDA)",
            "tolerancia": "Resistência de isolamento mínima de 1,0 MΩ para circuitos de 220V/380V; Resistência de aterramento máxima de 10 Ω (ou conforme projeto SPDA); Queda de tensão máxima de 4% no ponto terminal.",
            "itens_verificacao": [
                "Eletrodutos rígidos e corrugados fixados e desobstruídos com arame-guia",
                "Caixas de passagem 4x2 e 4x4 chumbadas no prumo e niveladas",
                "Cabeamento passado com identificação por cores normativas (Azul claro=Neutro, Verde=Terra, Preto/Vermelho=Fases)",
                "Instalação dos barramentos do Quadro de Distribuição Geral (QDG) com DR geral e DPS classe II",
                "Medição da malha de aterramento com terrômetro calibrado (eletrodos cravados no solo)",
                "Teste de continuidade elétrica e ensaio de isolamento com Megômetro",
                "Identificação e anilhamento de todos os condutores nos quadros terminais"
            ],
            "servico_sucessor_bloqueado": "Fechamento de forro de gesso, colocação de espelhos e energização final da obra"
        },
        {
            "codigo": "FVS-08",
            "titulo": "Cobertura Termoacústica, Calhas e Esquadrias de Alumínio",
            "pop": "POP 24 (Coberturas) e POP 25 (Esquadrias e Fachadas)",
            "nbr": "ABNT NBR 10821 (Esquadrias Externas) e NBR 14514 (Telhas Metálicas)",
            "etapa_obra": "Cobertura, Fachada e Fechamentos Externos",
            "contrato_bloqueado": "SUB-03 (Cobertura) e SUB-04 (Esquadrias)",
            "tolerancia": "Declividade mínima de calhas de 0,5%; Sobreposição longitudinal de telhas de no mín. 200mm c/ parafusos autobrocantes c/ arruela EPDM; Estanqueidade 100% sob jato d'água contínuo por 15 min.",
            "itens_verificacao": [
                "Estrutura metálica de apoio pintada, alinhada e ancorada nas vigas de concreto",
                "Instalação de telhas termoacústicas tipo sanduíche PIR com fixação e vedação de cumeeiras",
                "Caimento e teste de estanqueidade de calhas e condutores verticais de águas pluviais",
                "Chumbamento de contramarcos de alumínio com conferência de esquadro, prumo e nível",
                "Aplicação de silicone estrutural neutro de vedação perimetral externa entre marco e alvenaria",
                "Teste de permeabilidade à água com mangueira pressurizada direcionada às frestas das esquadrias",
                "Funcionamento perfeito de roldanas, fechos cremona e fechaduras com proteção plástica mantida"
            ],
            "servico_sucessor_bloqueado": "Execução de forros internos de gesso e pintura fina de acabamento"
        }
    ]


def gerar_fichas_individuais_fvs(output_dir, fvs_list, sigla, nome):
    fvs_dir = os.path.join(output_dir, "FVS")
    os.makedirs(fvs_dir, exist_ok=True)

    for f in fvs_list:
        itens_md = "\n".join([f"- [ ] **Item {i+1:02d}:** {it}  \n  *Status:* [ ] C (Conforme) | [ ] NC (Não Conforme) | [ ] NA (Não Aplica) — *Obs:* ________________" for i, it in enumerate(f['itens_verificacao'])])
        
        md_content = f"""# 📋 FICHA DE VERIFICAÇÃO DE SERVIÇO — {f['codigo']}
## {f['titulo'].upper()}

**Obra:** {nome} ({sigla})  
**Documento do Sistema de Gestão da Qualidade (PBQP-H / ISO 9001)**  
**Procedimentos de Referência:** {f['pop']}  
**Normas Regulamentadoras:** {f['nbr']}  

---

### 1. DADOS DE IDENTIFICAÇÃO DA INSPEÇÃO
* **Data da Inspeção:** ____/____/2026
* **Local / Eixos Inspecionados:** __________________________________________________
* **Empreiteiro / Fornecedor:** {f['contrato_bloqueado']}
* **Encarregado da Execução:** _____________________________________________________
* **Engenheiro Residente:** Alexandre (CREA-RJ 2026-A)
* **Auditor / TST:** _______________________________________________________________

---

### 2. CRITÉRIOS DE TOLERÂNCIA NORMATIVA E ACEITAÇÃO
> **Tolerâncias Inegociáveis:**  
> {f['tolerancia']}

---

### 3. ITENS OBRIGATÓRIOS DE VERIFICAÇÃO EM CAMPO
{itens_md}

---

### 4. GATILHO DE BLOQUEIO INTERDISCIPLINAR (PORTÃO DA EAP)
* 🛑 **Serviço Sucessor Bloqueado:** {f['servico_sucessor_bloqueado']}.
* 🚫 **Contrato Financeiramente Bloqueado:** {f['contrato_bloqueado']} — Nenhuma medição quinzenal será liberada para este contrato sem a assinatura desta FVS aprovada.

---

### 5. PARECER DA FISCALIZAÇÃO / ENGENHARIA
* [ ] **APROVADO:** Serviço liberado para execução do sucessor e medição contratual.
* [ ] **APROVADO COM RESSALVA:** Ajustes menores exigidos em até 24 horas (não bloqueia).
* [ ] **REPROVADO COM RNC:** Não conformidade detectada. Frente de serviço embargada até retificação e nova inspeção.

*Descrição de Pendências / RNC (se aplicável):*
____________________________________________________________________________________
____________________________________________________________________________________

---

### 6. ASSINATURAS E RESPONSABILIDADES
* **Encarregado do Empreiteiro:** ________________________________ Data: ____/____/________
* **Engenheiro Residente (Fiscal):** _____________________________ Data: ____/____/________
"""
        caminho_fvs = os.path.join(fvs_dir, f"{f['codigo']}_{f['titulo'].split(',')[0].replace(' ', '_').upper()}.md")
        with open(caminho_fvs, "w", encoding="utf-8") as file:
            file.write(md_content)


def gerar_caderno_mestre_fvs(output_dir, fvs_list, sigla, nome):
    caderno_path = os.path.join(output_dir, f"CADERNO_FVS_BLOQUEANTES_{sigla}.md")

    tabela_resumo = []
    for f in fvs_list:
        tabela_resumo.append(
            f"| **{f['codigo']}** | {f['titulo']} | {f['nbr'].split('(')[0].strip()} | **{f['contrato_bloqueado']}** | {f['servico_sucessor_bloqueado']} |"
        )
    tabela_md = "\n".join(tabela_resumo)

    detalhamento = []
    for f in fvs_list:
        itens_txt = "\n".join([f"  {idx+1}. {it}" for idx, it in enumerate(f['itens_verificacao'])])
        detalhamento.append(f"""### 📌 {f['codigo']} — {f['titulo']}
* **Normas ABNT:** {f['nbr']}
* **Procedimentos POP:** {f['pop']}
* **Contrato Bloqueado em Caso de Reprovação:** `{f['contrato_bloqueado']}`
* **Serviço Sucessor Condicionado:** `{f['servico_sucessor_bloqueado']}`
* **Tolerâncias Rígidas:** {f['tolerancia']}
* **Checklist Mínimo:**
{itens_txt}
""")

    conteudo_caderno = f"""# 🛡️ CADERNO MESTRE DE FVS BLOQUEANTES E QUALIDADE
## {nome.upper()} ({sigla})

> **Documento Oficial de Governança de Campo**  
> **Homologado segundo:** PBQP-H Nível A, ISO 9001, POP 08 (Sistema de Qualidade) e `agents.md`.

---

## 🎯 1. PRINCÍPIO DA LIBERAÇÃO EM CASCATA E BLOQUEIO CONTRATUAL

Nenhum serviço de engenharia nesta obra pode ser executado de forma aleatória ou presumida. O ecossistema opera sob a **Regra dos Portões de Qualidade**:

1. **Predecessor Inspecionado:** Um serviço sucessor NUNCA pode começar sem a FVS do serviço predecessor estar formalmente assinada pelo Engenheiro Residente.
2. **Amarração Contratual:** Nenhuma medição quinzenal de empreiteiro (`SUB-01` a `SUB-08`) pode ser liberada pelo setor Financeiro sem que a FVS correspondente esteja anexada e com status **APROVADO**.
3. **Ciclo RNC (Relatório de Não Conformidade):** Serviços com reprovação na FVS geram abertura compulsória de RNC (POP 08), paralisação da frente envolvida e refazimento com custo integral por conta do empreiteiro causador.

---

## 📊 2. MATRIZ RESUMO DAS FVSs E BLOQUEIOS INTERDISCIPLINARES

| FVS | Disciplina Inspecionada | Norma ABNT Base | Contrato Bloqueado | Liberação do Sucessor |
|---|---|---|---|---|
{tabela_md}

---

## 🔍 3. DETALHAMENTO DAS FICHAS DE VERIFICAÇÃO DE SERVIÇO

{chr(10).join(detalhamento)}

---

## 🛑 4. PROTOCOLO DE TRATAMENTO DE NÃO CONFORMIDADES (RNC)

Quando um item de inspeção for marcado como **Não Conforme (NC)**:
1. **Ação Imediata (Disposição):** A Engenharia emite ordem de paralisação imediata da atividade na área afetada.
2. **Registro Fotográfico:** Mínimo de 3 fotos datadas e georreferenciadas anexadas ao dossiê.
3. **Prazo de Correção:** O empreiteiro dispõe de até 48 horas para apresentar a proposta técnica de correção sem ônus para a obra.
4. **Reinspeção:** A FVS só recebe assinatura após refazimento total e nova medição dimensional com trena a laser/equipamento calibrado.

---
*Aprovado pela Engenharia Chefe e PMO Virtual.*
"""
    with open(caderno_path, "w", encoding="utf-8") as f:
        f.write(conteudo_caderno)
    return caderno_path


def construir_matriz_excel_fvs(output_dir, fvs_list, sigla, nome):
    excel_path = os.path.join(output_dir, f"MATRIZ_BLOQUEIO_FVS_CONTRATOS_{sigla}.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Matriz FVS e Bloqueios"
    ws.views.sheetView[0].showGridLines = True

    # Cores
    NAVY = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    BLUE_DARK = PatternFill(start_color="284B78", end_color="284B78", fill_type="solid")
    HEADER_GRAY = PatternFill(start_color="EAEEF3", end_color="EAEEF3", fill_type="solid")
    ZEBRA = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
    GREEN_FILL = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
    RED_FILL = PatternFill(start_color="FCE8E6", end_color="FCE8E6", fill_type="solid")

    FONT_TITLE = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
    FONT_SUB = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    FONT_TH = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    FONT_BOLD = Font(name="Calibri", size=9, bold=True, color="1B365D")
    FONT_REG = Font(name="Calibri", size=9, color="333333")
    FONT_RED = Font(name="Calibri", size=9, bold=True, color="C5221F")
    FONT_GREEN = Font(name="Calibri", size=9, bold=True, color="137333")

    THIN_BORDER = Border(
        left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'), bottom=Side(style='thin', color='DDDDDD')
    )

    ws.merge_cells("A1:G1")
    ws["A1"] = f"MATRIZ DE QUALIDADE, FVS E BLOQUEIOS CONTRATUAIS — {nome.upper()}"
    ws["A1"].font = FONT_TITLE
    ws["A1"].fill = NAVY
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:G2")
    ws["A2"] = "Amarração Direta entre Inspeções em Campo, Tolerâncias NBR e Retenção de Medições de Empreiteiros"
    ws["A2"].font = FONT_SUB
    ws["A2"].fill = BLUE_DARK
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 18

    headers = [
        ("Código", 12),
        ("Disciplina Inspecionada", 30),
        ("Norma Técnica ABNT", 25),
        ("POP de Referência", 25),
        ("Tolerância Dimensional Normativa", 45),
        ("Contrato Financeiramente Bloqueado", 25),
        ("Serviço Sucessor Condicionado", 35)
    ]

    for col_idx, (h_text, width) in enumerate(headers, start=1):
        cell = ws.cell(row=3, column=col_idx, value=h_text)
        cell.font = FONT_TH
        cell.fill = BLUE_DARK
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        ws.column_dimensions[get_column_letter(col_idx)].width = width
    ws.row_dimensions[3].height = 28

    for row_idx, f in enumerate(fvs_list, start=4):
        ws.cell(row=row_idx, column=1, value=f['codigo']).font = FONT_BOLD
        ws.cell(row=row_idx, column=1).alignment = Alignment(horizontal="center", vertical="center")
        
        ws.cell(row=row_idx, column=2, value=f['titulo']).font = FONT_BOLD
        ws.cell(row=row_idx, column=3, value=f['nbr'])
        ws.cell(row=row_idx, column=4, value=f['pop'])
        
        c_tol = ws.cell(row=row_idx, column=5, value=f['tolerancia'])
        c_tol.alignment = Alignment(wrap_text=True)
        
        c_bloq = ws.cell(row=row_idx, column=6, value=f['contrato_bloqueado'])
        c_bloq.font = FONT_RED
        c_bloq.fill = RED_FILL
        c_bloq.alignment = Alignment(horizontal="center", vertical="center")
        
        c_suc = ws.cell(row=row_idx, column=7, value=f['servico_sucessor_bloqueado'])
        c_suc.alignment = Alignment(wrap_text=True)

        for col in range(1, 8):
            cell = ws.cell(row=row_idx, column=col)
            cell.border = THIN_BORDER
            if row_idx % 2 == 1 and col != 6:
                cell.fill = ZEBRA
        ws.row_dimensions[row_idx].height = 45

    wb.save(excel_path)
    return excel_path


def main():
    args = parse_args()
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    if args.dir:
        obra_dir = os.path.abspath(args.dir)
    else:
        obra_dir = os.path.join(workspace_root, "projetos", args.obra)

    if not os.path.exists(obra_dir):
        print(f"[ERRO] Pasta da obra não encontrada: {obra_dir}")
        sys.exit(1)

    print(f"\n=======================================================")
    print(f"🛡️ MOTOR UNIVERSAL DE QUALIDADE DE CAMPO E FVS")
    print(f"=======================================================")
    print(f"📂 Diretório da Obra: {obra_dir}")

    config = carregar_dados_obra(obra_dir)
    sigla = config.get("sigla_obra", "OBRA")
    nome = config.get("nome_obra", sigla)
    print(f"🏗️  Obra Ativa: {nome} ({sigla})")

    output_dir = os.path.join(obra_dir, "04_PRODUCAO_E_AVANCO")
    os.makedirs(output_dir, exist_ok=True)

    fvs_list = obter_definicoes_fvs(sigla, nome)

    print(f"\n[1/3] Gerando 8 Fichas Individuais de Verificação de Serviço em 04_PRODUCAO_E_AVANCO/FVS/...")
    gerar_fichas_individuais_fvs(output_dir, fvs_list, sigla, nome)
    print(f"      ✅ 8 FVSs estruturadas em Markdown prontas para impressão e prancheta")

    print(f"\n[2/3] Compilando Caderno Mestre CADERNO_FVS_BLOQUEANTES_{sigla}.md...")
    caderno_path = gerar_caderno_mestre_fvs(output_dir, fvs_list, sigla, nome)
    print(f"      ✅ Caderno Mestre gerado: {caderno_path}")

    print(f"\n[3/3] Construindo Matriz Visual MATRIZ_BLOQUEIO_FVS_CONTRATOS_{sigla}.xlsx...")
    excel_path = construir_matriz_excel_fvs(output_dir, fvs_list, sigla, nome)
    print(f"      ✅ Planilha Excel gerada: {excel_path}")

    print(f"\n✨ Motor de FVSs Bloqueantes concluído com 100% de sucesso!")


if __name__ == "__main__":
    main()
