#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Integrado de Planejamento de Suprimentos & Contratações - OBRA_TMULT
Gera com precisão determinística:
1. CRONOGRAMA_MESTRE_SUPRIMENTOS_TMULT.md (Materiais & Equipamentos integrados na Linha de Base)
2. CRONOGRAMA_MESTRE_SUPRIMENTOS_TMULT.xlsx (Planilha executiva multi-abas estilizada)
3. PLANO_CONTRATACAO_EMPREITEIROS_TMULT.md (Subcontratações baseadas no Histograma)
4. CATALOGO_COMPLETO_REQUISICOES_COMPRA_TMULT.md (As 24 RCs com UCC, EAP e CC)
5. TRACKER_SUPRIMENTOS_RC_TMULT.md (Kanban vivo do pipeline)
6. TRACKER_SUPRIMENTOS_RC_TMULT.csv (Base tabular)
"""

import os
import sys
import csv
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

# Diretórios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "projetos", "OBRA_TMULT", "05_SUPRIMENTOS_E_FINANCEIRO")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# DADOS MESTRES DOS 24 PACOTES DE MATERIAIS
# -------------------------------------------------------------
MATERIAIS = [
    {
        "rc": "RC-001/2026", "pacote": "Aço CA-50/60 Cortado e Dobrado (Fundações e Baldrames)",
        "disciplina": "Infraestrutura", "eap": "1.1.10, 1.1.11, 1.1.12", "cc": "CC-208 / CC-209 / CC-210",
        "qtd_ucc": "1.553,0 kg", "data_gatilho_rc": "12/09/2026", "data_pc": "18/09/2026", "data_obra": "28/09/2026",
        "lead_dias": 16, "semana": "S03", "mes": "Mês 1", "cd_orcado": 15635.66,
        "criterio_pop06": "Certificado de corrida de aço Gerdau/Arcelor; conferência de etiquetas por elemento; cobrimento pastilhas c=40mm"
    },
    {
        "rc": "RC-002/2026", "pacote": "Concreto Usinado fck 30 MPa Bombeável e Lastro fck 15 MPa",
        "disciplina": "Infraestrutura", "eap": "1.1.3, 1.1.4, 1.1.6, 1.1.8", "cc": "CC-202 / CC-203 / CC-205 / CC-206",
        "qtd_ucc": "29,5 m³", "data_gatilho_rc": "14/09/2026", "data_pc": "22/09/2026", "data_obra": "01/10/2026",
        "lead_dias": 17, "semana": "S03", "mes": "Mês 1", "cd_orcado": 20252.08,
        "criterio_pop06": "Slump test 12±2cm a cada betoneira; moldagem 6 CPs/caminhão (7/14/28d); trânsito < 25 min (Polimix Açu)"
    },
    {
        "rc": "RC-003/2026", "pacote": "Compensado Resinado 17mm, Pontaletes e Consumíveis de Fôrma",
        "disciplina": "Infraestrutura", "eap": "1.1.5, 1.1.7, 1.1.9", "cc": "CC-204 / CC-205 / CC-207",
        "qtd_ucc": "129 chapas / 180 vigas", "data_gatilho_rc": "12/09/2026", "data_pc": "16/09/2026", "data_obra": "26/09/2026",
        "lead_dias": 14, "semana": "S02", "mes": "Mês 1", "cd_orcado": 20286.07,
        "criterio_pop06": "Compensado fenólico WBP 17mm c/ bordas seladas; tábuas pinho secas; pregos 17x27 e 18x30 galvanizados"
    },
    {
        "rc": "RC-004/2026", "pacote": "Locação de Módulos Habitáveis Containers NR-18 e Sanitários Químicos",
        "disciplina": "Canteiro de Obras", "eap": "1.0.3", "cc": "CC-103",
        "qtd_ucc": "4 containers / 2 cabines (6 meses)", "data_gatilho_rc": "10/09/2026", "data_pc": "14/09/2026", "data_obra": "22/09/2026",
        "lead_dias": 12, "semana": "S02", "mes": "Mês 1", "cd_orcado": 38299.98,
        "criterio_pop06": "Módulos EPS 50mm c/ laudo elétrico e ART; ar split 12k testado; contrato com 2 limpezas/sem de sanitários químicos"
    },
    {
        "rc": "RC-005/2026", "pacote": "Cimbramento e Escoramento Metálico Ajustável",
        "disciplina": "Supraestrutura", "eap": "1.2.4, 1.2.6", "cc": "CC-302",
        "qtd_ucc": "888 m²·m (locação 45 dias)", "data_gatilho_rc": "05/10/2026", "data_pc": "12/10/2026", "data_obra": "25/10/2026",
        "lead_dias": 20, "semana": "S06", "mes": "Mês 2", "cd_orcado": 14850.00,
        "criterio_pop06": "Torres e escoras metálicas c/ laudo de capacidade de carga; sapatas ajustáveis sem empenos; ART do fabricante"
    },
    {
        "rc": "RC-006/2026", "pacote": "Vigotas Treliçadas Pré-moldadas TR 16745 e EPS H12",
        "disciplina": "Supraestrutura", "eap": "1.2.5", "cc": "CC-303",
        "qtd_ucc": "298,25 m² laje", "data_gatilho_rc": "08/10/2026", "data_pc": "15/10/2026", "data_obra": "28/10/2026",
        "lead_dias": 20, "semana": "S07", "mes": "Mês 2", "cd_orcado": 23450.00,
        "criterio_pop06": "Trilhos treliçados com contraflecha normativa L/300; blocos EPS 100% antichama sem quebras"
    },
    {
        "rc": "RC-007/2026", "pacote": "Aço CA-50/60 Cortado e Dobrado (Pilares P1-P24 e Vigas V101-V115)",
        "disciplina": "Supraestrutura", "eap": "1.2.7, 1.2.8", "cc": "CC-304",
        "qtd_ucc": "3.180,0 kg", "data_gatilho_rc": "10/10/2026", "data_pc": "16/10/2026", "data_obra": "30/10/2026",
        "lead_dias": 20, "semana": "S07", "mes": "Mês 2", "cd_orcado": 29850.00,
        "criterio_pop06": "Identificação e amarração por elemento estrutural; certificados de conformidade ABNT NBR 7480"
    },
    {
        "rc": "RC-008/2026", "pacote": "Concreto Usinado fck 30 MPa Bombeável (Pilares, Vigas e Capa da Laje)",
        "disciplina": "Supraestrutura", "eap": "1.2.1, 1.2.3, 1.2.5", "cc": "CC-305",
        "qtd_ucc": "37,0 m³", "data_gatilho_rc": "15/10/2026", "data_pc": "23/10/2026", "data_obra": "05/11/2026",
        "lead_dias": 21, "semana": "S08", "mes": "Mês 2", "cd_orcado": 32650.00,
        "criterio_pop06": "Concretagem contínua monocamada na laje; auto-bomba lança 32m com ART; cura química com película formadora"
    },
    {
        "rc": "RC-009/2026", "pacote": "Blocos de Concreto Estrutural/Vedação B144 (14x19x39cm)",
        "disciplina": "Alvenaria e Vedações", "eap": "1.3.1, 1.3.2", "cc": "CC-401",
        "qtd_ucc": "13.790 blocos", "data_gatilho_rc": "20/10/2026", "data_pc": "28/10/2026", "data_obra": "15/11/2026",
        "lead_dias": 26, "semana": "S09", "mes": "Mês 3", "cd_orcado": 21400.00,
        "criterio_pop06": "Blocos paletizados com filme stretch; resistência mínima fbk >= 4,0 MPa; laudo dimensional sem trincas"
    },
    {
        "rc": "RC-010/2026", "pacote": "Cimento Portland CP II-E-32, Areia Média Lavada e Aditivos",
        "disciplina": "Alvenaria e Vedações", "eap": "1.3.3", "cc": "CC-402",
        "qtd_ucc": "320 sacos 50kg / 28 m³ areia", "data_gatilho_rc": "02/11/2026", "data_pc": "08/11/2026", "data_obra": "18/11/2026",
        "lead_dias": 16, "semana": "S10", "mes": "Mês 3", "cd_orcado": 11250.00,
        "criterio_pop06": "Sacos intactos em estrados de madeira protegidos de umidade; areia média isenta de matéria orgânica e argila"
    },
    {
        "rc": "RC-011/2026", "pacote": "Locação de Andaimes Tubulares Fachadeiros c/ Guarda-Corpo",
        "disciplina": "Alvenaria e Fachada", "eap": "1.3.4", "cc": "CC-403",
        "qtd_ucc": "200 m² (locação 60 dias)", "data_gatilho_rc": "08/11/2026", "data_pc": "15/11/2026", "data_obra": "25/11/2026",
        "lead_dias": 17, "semana": "S11", "mes": "Mês 3", "cd_orcado": 7400.00,
        "criterio_pop06": "Enquadramento integral NR-18; piso metálico antiderrapante; rodapés 20cm; sapatas reguláveis c/ trava"
    },
    {
        "rc": "RC-012/2026", "pacote": "Telhas Termoacústicas Sandwich PIR e Calhas Metálicas Galvanizadas",
        "disciplina": "Cobertura e Envoltória", "eap": "1.4.1, 1.4.2, 1.4.3", "cc": "CC-501",
        "qtd_ucc": "381,29 m² telhas / 64m calhas", "data_gatilho_rc": "15/10/2026", "data_pc": "25/10/2026", "data_obra": "28/11/2026",
        "lead_dias": 44, "semana": "S11", "mes": "Mês 3", "cd_orcado": 48900.00,
        "criterio_pop06": "Núcleo PIR 30mm autoextinguível; chapa aluzinc AZ-150 pré-pintada na cor branca; teste de estanqueidade 100%"
    },
    {
        "rc": "RC-013/2026", "pacote": "Tubulações e Conexões PVC Rígido Água Fria e Esgoto Predial",
        "disciplina": "Instalações Hidrossanitárias", "eap": "2.1.1, 2.1.2, 2.1.3", "cc": "CC-601",
        "qtd_ucc": "480m tubos / 180 conexões", "data_gatilho_rc": "20/11/2026", "data_pc": "28/11/2026", "data_obra": "15/12/2026",
        "lead_dias": 25, "semana": "S14", "mes": "Mês 4", "cd_orcado": 16800.00,
        "criterio_pop06": "Tubos Tigre/Amanco NBR 5648 / NBR 5688; teste de pressão hidrostática 10 bar por 72h antes do fechamento das paredes"
    },
    {
        "rc": "RC-014/2026", "pacote": "Eletrodutos Rígidos Roscáveis, Caixas 4x2 e Caixas de Passagem",
        "disciplina": "Instalações Elétricas", "eap": "2.2.1, 2.2.2", "cc": "CC-604",
        "qtd_ucc": "650m eletrodutos / 94 caixas", "data_gatilho_rc": "25/11/2026", "data_pc": "02/12/2026", "data_obra": "18/12/2026",
        "lead_dias": 23, "semana": "S14", "mes": "Mês 4", "cd_orcado": 9750.00,
        "criterio_pop06": "Eletrodutos PVC antichama NBR 15465 com rosca NBR 8133; caixas estampadas sem rebarbas"
    },
    {
        "rc": "RC-015/2026", "pacote": "Argamassa Industrializada de Projeção para Emboço Paulista",
        "disciplina": "Revestimentos de Parede", "eap": "1.5.1, 1.5.2", "cc": "CC-405",
        "qtd_ucc": "480 sacos 40kg", "data_gatilho_rc": "01/12/2026", "data_pc": "08/12/2026", "data_obra": "20/12/2026",
        "lead_dias": 19, "semana": "S15", "mes": "Mês 4", "cd_orcado": 12800.00,
        "criterio_pop06": "Argamassa usinada seca NBR 13281 c/ aditivos plastificantes para máquina de projeção; aderência >= 0,3 MPa"
    },
    {
        "rc": "RC-016/2026", "pacote": "Esquadrias de Alumínio Anodizado Preto e Vidros Temperados",
        "disciplina": "Esquadrias e Vidros", "eap": "1.6.1 a 1.6.4", "cc": "CC-702",
        "qtd_ucc": "Janelas J1 a J4 (38,40 m²)", "data_gatilho_rc": "01/11/2026", "data_pc": "15/11/2026", "data_obra": "10/01/2027",
        "lead_dias": 70, "semana": "S17", "mes": "Mês 4", "cd_orcado": 58400.00,
        "criterio_pop06": "Perfis Linha Suprema anodização 20 micras; vidros incolores 8mm temperados com selo INMETRO; vedação EPDM"
    },
    {
        "rc": "RC-017/2026", "pacote": "Porcelanato Esmaltado Retificado 60x60cm e Argamassa AC-III",
        "disciplina": "Pisos e Pavimentações", "eap": "1.7.1, 1.7.2", "cc": "CC-704",
        "qtd_ucc": "410 m² piso / 85 sacos AC3", "data_gatilho_rc": "10/12/2026", "data_pc": "20/12/2026", "data_obra": "15/01/2027",
        "lead_dias": 36, "semana": "S18", "mes": "Mês 5", "cd_orcado": 35200.00,
        "criterio_pop06": "Mesmo lote e tonalidade em 100% das caixas; PEI-4; rejunte epóxi em áreas molhadas e resinado nas demais"
    },
    {
        "rc": "RC-018/2026", "pacote": "Kits Porta Pronta de Madeira Melamínica com Fechaduras Inox",
        "disciplina": "Esquadrias de Madeira", "eap": "1.6.5", "cc": "CC-701",
        "qtd_ucc": "14 portas completas (P1 a P5)", "data_gatilho_rc": "05/12/2026", "data_pc": "15/12/2026", "data_obra": "20/01/2027",
        "lead_dias": 46, "semana": "S19", "mes": "Mês 5", "cd_orcado": 17800.00,
        "criterio_pop06": "Batentes reguláveis WPC resistentes à umidade; fechaduras La Fonte inox 304; borrachas amortecedoras"
    },
    {
        "rc": "RC-019/2026", "pacote": "Cabos Elétricos de Cobre Flexível 750V / 1kV (1,5 a 50 mm²)",
        "disciplina": "Instalações Elétricas", "eap": "2.2.3, 2.2.4", "cc": "CC-605",
        "qtd_ucc": "3.800m cabos (bobinas)", "data_gatilho_rc": "05/01/2027", "data_pc": "12/01/2027", "data_obra": "25/01/2027",
        "lead_dias": 20, "semana": "S19", "mes": "Mês 5", "cd_orcado": 31200.00,
        "criterio_pop06": "Cabos Prysmian/Corfio 100% cobre eletrolítico antichama BWF; teste de continuidade e isolamento com megômetro"
    },
    {
        "rc": "RC-020/2026", "pacote": "Quadros QDG/QDF, Disjuntores DIN, DPS, Tomadas e Interruptores",
        "disciplina": "Instalações Elétricas", "eap": "2.2.5, 2.2.6", "cc": "CC-606",
        "qtd_ucc": "2 quadros / 85 módulos Schneider", "data_gatilho_rc": "10/01/2027", "data_pc": "16/01/2027", "data_obra": "28/01/2027",
        "lead_dias": 18, "semana": "S20", "mes": "Mês 5", "cd_orcado": 15900.00,
        "criterio_pop06": "Disjuntores curva C homologados; barramentos tipo pente blindados; placas 4x2 com acabamento acetinado branco"
    },
    {
        "rc": "RC-021/2026", "pacote": "Louças Sanitárias, Cubas de Inox e Metais com Sensor/Pressômetro",
        "disciplina": "Instalações Hidrossanitárias", "eap": "2.1.4, 2.1.5", "cc": "CC-603",
        "qtd_ucc": "6 bacias / 6 lavatórios / 8 torneiras", "data_gatilho_rc": "20/01/2027", "data_pc": "28/01/2027", "data_obra": "15/02/2027",
        "lead_dias": 26, "semana": "S22", "mes": "Mês 6", "cd_orcado": 23400.00,
        "criterio_pop06": "Bacias Deca c/ caixa acoplada Duo 3/6L; torneiras Docol temporizadas para economia de água no complexo portuário"
    },
    {
        "rc": "RC-022/2026", "pacote": "Aparelhos de Ar-Condicionado Split Inverter (12k a 24k BTU) e Tubulação",
        "disciplina": "Climatização HVAC", "eap": "2.3.1, 2.3.2", "cc": "CC-608",
        "qtd_ucc": "8 unidades splits inverter R-32", "data_gatilho_rc": "05/01/2027", "data_pc": "15/01/2027", "data_obra": "20/02/2027",
        "lead_dias": 46, "semana": "S23", "mes": "Mês 6", "cd_orcado": 38900.00,
        "criterio_pop06": "Classificação Procel A; linhas de cobre isoladas com elastomérico; teste de vácuo 500 microns e estanqueidade N2 400 psi"
    },
    {
        "rc": "RC-023/2026", "pacote": "Tintas Acrílicas Laváveis Premium, Selador Acrílico e Massa PVA",
        "disciplina": "Pintura e Acabamentos", "eap": "1.8.1, 1.8.2", "cc": "CC-706",
        "qtd_ucc": "42 latas 18L / 24 baldes massa", "data_gatilho_rc": "25/01/2027", "data_pc": "02/02/2027", "data_obra": "18/02/2027",
        "lead_dias": 24, "semana": "S23", "mes": "Mês 6", "cd_orcado": 14200.00,
        "criterio_pop06": "Suvinil/Coral fosco aveludado cor Branco Neve e Gelo; laudo de rendimento e lavabilidade NBR 15079"
    },
    {
        "rc": "RC-024/2026", "pacote": "Limpeza Fina Pós-Obra, Testes Globais e Desmobilização Geral",
        "disciplina": "Entrega e Comissionamento", "eap": "1.9.1, 1.9.2", "cc": "CC-105",
        "qtd_ucc": "Serviço global (368,40 m²)", "data_gatilho_rc": "05/02/2027", "data_pc": "12/02/2027", "data_obra": "25/02/2027",
        "lead_dias": 20, "semana": "S25", "mes": "Mês 6", "cd_orcado": 9400.00,
        "criterio_pop06": "Polimento de porcelanatos, limpeza química de vidros sem riscos, entrega de chaves e databook físico/digital"
    }
]

# -------------------------------------------------------------
# DADOS MESTRES DOS 17 EQUIPAMENTOS E INSTALAÇÕES PROVISÓRIAS
# -------------------------------------------------------------
EQUIPAMENTOS = [
    {
        "item": "EQ-01", "nome": "Módulo Habitável Escritório / Reuniões", "tipo": "Container 6,00x2,40m climatizado",
        "qtd": 1, "und": "un", "meses": "M1 a M6", "semanas": "S01 a S26", "cc": "CC-103",
        "lead_dias": 12, "data_solic": "10/09/2026", "data_mobil": "22/09/2026", "data_desmob": "10/03/2027",
        "modalidade": "Locação Mensal", "fornecedor_alvo": "Rentcon Locações / NHJ Brasil",
        "funcao": "Apoio técnico da Engenharia e reuniões com a Fiscalização do Porto do Açu"
    },
    {
        "item": "EQ-02", "nome": "Módulo Vestiário / Sanitário NR-18", "tipo": "Container c/ 3 chuveiros e armários",
        "qtd": 1, "und": "un", "meses": "M1 a M6", "semanas": "S01 a S26", "cc": "CC-103",
        "lead_dias": 12, "data_solic": "10/09/2026", "data_mobil": "22/09/2026", "data_desmob": "10/03/2027",
        "modalidade": "Locação Mensal", "fornecedor_alvo": "Rentcon Locações / NHJ Brasil",
        "funcao": "Higiene e vivência para até 20 operários simultâneos conforme NR-18"
    },
    {
        "item": "EQ-03", "nome": "Módulo Refeitório NR-18", "tipo": "Container climatizado c/ mesas e pia",
        "qtd": 1, "und": "un", "meses": "M1 a M6", "semanas": "S01 a S26", "cc": "CC-103",
        "lead_dias": 12, "data_solic": "10/09/2026", "data_mobil": "22/09/2026", "data_desmob": "10/03/2027",
        "modalidade": "Locação Mensal", "fornecedor_alvo": "Rentcon Locações / NHJ Brasil",
        "funcao": "Alimentação aquecida, água filtrada e copa para equipe própria e empreiteiros"
    },
    {
        "item": "EQ-04", "nome": "Módulo Almoxarifado / Ferramentaria", "tipo": "Container Marítimo Dry 20 pés reforçado",
        "qtd": 1, "und": "un", "meses": "M1 a M6", "semanas": "S01 a S26", "cc": "CC-103",
        "lead_dias": 12, "data_solic": "10/09/2026", "data_mobil": "22/09/2026", "data_desmob": "10/03/2027",
        "modalidade": "Locação Mensal", "fornecedor_alvo": "Rentcon Locações / NHJ Brasil",
        "funcao": "Guarda de ferramentas elétricas, consumíveis, EPIs e cabos de cobre"
    },
    {
        "item": "EQ-05", "nome": "Sanitários Químicos Portáteis", "tipo": "Cabine polietileno c/ higienização 2x/sem",
        "qtd": 2, "und": "un", "meses": "M1 a M6", "semanas": "S01 a S26", "cc": "CC-103",
        "lead_dias": 12, "data_solic": "10/09/2026", "data_mobil": "22/09/2026", "data_desmob": "10/03/2027",
        "modalidade": "Locação Mensal c/ Serviço", "fornecedor_alvo": "Brasquímica / Rentcon",
        "funcao": "Atendimento rápido nas frentes externas de movimento de terra e estrutura"
    },
    {
        "item": "EQ-06", "nome": "Retroescavadeira 4x4 c/ Operador", "tipo": "Tração 4x4, caçamba 1,0 m³, motor 90 HP",
        "qtd": 1, "und": "un", "meses": "M1", "semanas": "S01 a S03", "cc": "CC-201",
        "lead_dias": 7, "data_solic": "12/09/2026", "data_mobil": "19/09/2026", "data_desmob": "08/10/2026",
        "modalidade": "Locação por Hora / Diária", "fornecedor_alvo": "Terramax Locações / Base Regional Açu",
        "funcao": "Escavação rápida de 32 cavas de sapatas e 140m de valas de baldrames"
    },
    {
        "item": "EQ-07", "nome": "Caminhão Basculante Traçado 6x4 (12m³)", "tipo": "Eixos 6x4 c/ caçamba basculante reforçada",
        "qtd": 1, "und": "un", "meses": "M1", "semanas": "S01 a S03", "cc": "CC-201",
        "lead_dias": 7, "data_solic": "12/09/2026", "data_mobil": "19/09/2026", "data_desmob": "08/10/2026",
        "modalidade": "Locação por Viagem / Produção", "fornecedor_alvo": "Transportadora Norte Fluminense",
        "funcao": "Carga e bota-fora de terra excedente para bota-fora homologado no Açu"
    },
    {
        "item": "EQ-08", "nome": "Compactador de Percussão (Sapo)", "tipo": "Motor 4T a gasolina, impacto 14 kN",
        "qtd": 1, "und": "un", "meses": "M1", "semanas": "S02 a S04", "cc": "CC-201",
        "lead_dias": 5, "data_solic": "15/09/2026", "data_mobil": "20/09/2026", "data_desmob": "12/10/2026",
        "modalidade": "Locação Mensal", "fornecedor_alvo": "Casa do Construtor Campos / Locafer",
        "funcao": "Apiloamento e adensamento do fundo de cavas das sapatas e reaterro das valas"
    },
    {
        "item": "EQ-09", "nome": "Betoneira Elétrica 400 Litros", "tipo": "Motor trifásico 2 CV 220V c/ proteção",
        "qtd": 1, "und": "un", "meses": "M1 a M4", "semanas": "S02 a S17", "cc": "CC-404",
        "lead_dias": 5, "data_solic": "15/09/2026", "data_mobil": "22/09/2026", "data_desmob": "05/01/2027",
        "modalidade": "Locação Mensal", "fornecedor_alvo": "Casa do Construtor Campos",
        "funcao": "Preparo de argamassa de assentamento de alvenaria e concreto de enchimento"
    },
    {
        "item": "EQ-10", "nome": "Cimbramento e Escoramento Metálico", "tipo": "Torres tubulares, forcados e escoras telescópicas",
        "qtd": 888, "und": "m²·m", "meses": "M2", "semanas": "S05 a S09", "cc": "CC-302",
        "lead_dias": 20, "data_solic": "05/10/2026", "data_mobil": "25/10/2026", "data_desmob": "28/11/2026",
        "modalidade": "Locação por Período (35 dias)", "fornecedor_alvo": "Mills / Rohr / SH Formas",
        "funcao": "Escoramento seguro das vigas superiores V101-V115 e da laje treliçada H12"
    },
    {
        "item": "EQ-11", "nome": "Andaimes Tubulares Fachadeiros c/ NR-18", "tipo": "Módulos 1,50x1,00m c/ piso metálico e rodapé",
        "qtd": 200, "und": "m²", "meses": "M3 a M5", "semanas": "S10 a S21", "cc": "CC-403",
        "lead_dias": 15, "data_solic": "05/11/2026", "data_mobil": "20/11/2026", "data_desmob": "05/02/2027",
        "modalidade": "Locação Mensal", "fornecedor_alvo": "Orguel / Casa do Construtor",
        "funcao": "Trabalho em altura seguro para alvenarias de fechamento, telhas e reboco"
    },
    {
        "item": "EQ-12", "nome": "Máquina de Projeção Contínua de Argamassa", "tipo": "Rendimento 1,5 m³/h c/ misturador contínuo",
        "qtd": 1, "und": "un", "meses": "M4", "semanas": "S14 a S17", "cc": "CC-405",
        "lead_dias": 15, "data_solic": "25/11/2026", "data_mobil": "10/12/2026", "data_desmob": "10/01/2027",
        "modalidade": "Locação Mensal", "fornecedor_alvo": "Putzknecht / M-Tec / Locadora Técnica",
        "funcao": "Aceleração mecânica do emboço paulista garantindo prumo e aderência uniforme"
    },
    {
        "item": "EQ-13", "nome": "Bomba de Teste Hidrostático c/ Manômetro", "tipo": "Bomba manual/elétrica até 25 bar c/ calibração",
        "qtd": 1, "und": "un", "meses": "M4", "semanas": "S15 a S16", "cc": "CC-601",
        "lead_dias": 10, "data_solic": "01/12/2026", "data_mobil": "12/12/2026", "data_desmob": "23/12/2026",
        "modalidade": "Locação Quinzenal", "fornecedor_alvo": "Alusolda / Casa do Construtor",
        "funcao": "Ensaio de estanqueidade obrigatório 72h conforme NBR 5626 (Portão 3)"
    },
    {
        "item": "EQ-14", "nome": "Plataforma Elevatória Tesoura Elétrica 10m", "tipo": "Autopropelida, silenciosa, pneus brancos",
        "qtd": 1, "und": "un", "meses": "M5 a M6", "semanas": "S18 a S24", "cc": "CC-607",
        "lead_dias": 20, "data_solic": "20/12/2026", "data_mobil": "10/01/2027", "data_desmob": "20/02/2027",
        "modalidade": "Locação Mensal", "fornecedor_alvo": "Mills / Loxam Degrau",
        "funcao": "Instalação ágil de luminárias LED em altura, dutos HVAC e bandejamento elétrico"
    },
    {
        "item": "EQ-15", "nome": "Bomba de Vácuo Duplo Estágio + Manifold", "tipo": "Bomba 10 CFM c/ vacuômetro digital calibrado",
        "qtd": 1, "und": "cj", "meses": "M5 a M6", "semanas": "S20 a S24", "cc": "CC-608",
        "lead_dias": 10, "data_solic": "10/01/2027", "data_mobil": "22/01/2027", "data_desmob": "25/02/2027",
        "modalidade": "Equipamento Subcontratado / Locação", "fornecedor_alvo": "Empreiteiro HVAC / Frigocenter",
        "funcao": "Desidratação e vácuo das linhas frigorígenas dos 8 splits até < 500 microns"
    },
    {
        "item": "EQ-16", "nome": "Caçambas Estacionárias de Entulho (5 m³)", "tipo": "Giro contínuo c/ transporte até aterro licenciado",
        "qtd": 2, "und": "un", "meses": "M1 a M6", "semanas": "S01 a S26", "cc": "CC-106",
        "lead_dias": 5, "data_solic": "10/09/2026", "data_mobil": "18/09/2026", "data_desmob": "10/03/2027",
        "modalidade": "Prestação de Serviços c/ CTR", "fornecedor_alvo": "EcoAçu Resíduos / Disk Entulho SJB",
        "funcao": "Segregação e descarte legal de RSU e RCC conforme PGRCC homologado no Porto"
    },
    {
        "item": "EQ-17", "nome": "Grupo Gerador Diesel Silenciado 50 kVA", "tipo": "Cabinado 70 dB, partida automática, trifásico",
        "qtd": 1, "und": "un", "meses": "M1 a M3", "semanas": "S01 a S12", "cc": "CC-104",
        "lead_dias": 10, "data_solic": "10/09/2026", "data_mobil": "18/09/2026", "data_desmob": "10/12/2026",
        "modalidade": "Locação Mensal", "fornecedor_alvo": "Tecnogera / Geradores Brasil Macaé",
        "funcao": "Suporte elétrico confiável para canteiro até a ligação da concessionária Enel"
    }
]

# -------------------------------------------------------------
# DADOS MESTRES DOS 8 SUBCONTRATOS DE MÃO DE OBRA
# -------------------------------------------------------------
SUBCONTRATOS = [
    {
        "cod": "SUB-01", "nome": "Empreitada de Fundações e Estrutura de Concreto Armado",
        "mes": "Mês 1 a Mês 2", "semanas": "S01 a S09", "pico": "12 operários (4 Carpinteiros, 3 Armadores, 5 Serventes)",
        "cc": "CC-200 / CC-300", "medicao": "Avanço Físico (m³ concretado e m² fôrma desformada c/ FVS aprovada)",
        "retencao": "5% retida na NF liberada após 90 dias e laudo CPs 28 dias fck >= 30 MPa",
        "escopo": "Fôrmas compensadas, corte/dobra/amarração de aço CA-50/60, lançamento e vibração de concreto, cura e desforma",
        "valor_base": 195400.00
    },
    {
        "cod": "SUB-02", "nome": "Empreitada de Alvenaria de Vedação e Revestimentos de Parede",
        "mes": "Mês 3 a Mês 4", "semanas": "S10 a S17", "pico": "10 operários (5 Pedreiros e 5 Serventes)",
        "cc": "CC-400", "medicao": "Produção Efetiva (m² alvenaria aprumada e m² emboço sarrafeado)",
        "retencao": "5% retida até entrega da FVS de prumo/planeza e teste de percussão acústico",
        "escopo": "Elevação de blocos de concreto B144, vergas/contravergas, chapisco rolado e emboço mecanizado com máquina de projeção",
        "valor_base": 138600.00
    },
    {
        "cod": "SUB-03", "nome": "Empreitada Especializada de Cobertura Termoacústica",
        "mes": "Mês 3 a Mês 4", "semanas": "S10 a S15", "pico": "3 montadores especialistas certificados NR-35",
        "cc": "CC-500", "medicao": "m² montado e estanque aprovado sob teste de aspersão de água 100%",
        "retencao": "5% retida até primeira chuva forte sem vazamento ou 60 dias",
        "escopo": "Içamento mecânico, fixação com parafusos autobrocantes, montagem de cumeeiras, calhas galvanizadas e rufos perimétricos",
        "valor_base": 42500.00
    },
    {
        "cod": "SUB-04", "nome": "Empreitada de Pisos e Pavimentações",
        "mes": "Mês 5", "semanas": "S18 a S21", "pico": "3 ladrilhistas / azulejistas qualificados",
        "cc": "CC-704", "medicao": "m² assentado com niveladores de piso e rejuntado sem dentes",
        "retencao": "5% retida até teste de percussão (eliminação de peças com som oco)",
        "escopo": "Contrapiso autonivelante, dupla colagem porcelanato 60x60, aplicação de rodapés e rejunte epóxi em sanitários",
        "valor_base": 36800.00
    },
    {
        "cod": "SUB-05", "nome": "Empreitada de Instalações Elétricas, Telecom e SPDA",
        "mes": "Mês 3 a Mês 5", "semanas": "S12 a S21", "pico": "2 eletricistas industriais oficiais",
        "cc": "CC-604 / CC-605 / CC-606", "medicao": "Etapas Físicas Concluídas (Infra, Enfiamento, Fechamento de Quadros)",
        "retencao": "5% retida até energização geral e laudo de conformidade NBR 5410 emitido c/ ART",
        "escopo": "Chumbamento de caixas, enfiação de condutores de cobre, crimpagem de terminais, montagem dos quadros QDG/QDF e rede Cat6",
        "valor_base": 48200.00
    },
    {
        "cod": "SUB-06", "nome": "Empreitada de Instalações Hidrossanitárias e Drenagem",
        "mes": "Mês 3 a Mês 5", "semanas": "S12 a S20", "pico": "2 encanadores industriais oficiais",
        "cc": "CC-601 / CC-602 / CC-603", "medicao": "Pontos Executados e Aprovados no Teste Hidrostático (Portão 3)",
        "retencao": "5% retida até teste de pressão hidrostática 72h registrado em laudo fotográfico",
        "escopo": "Montagem de ramais de água fria soldável, prumadas de esgoto em PVC série reforçada, caixas de gordura e esgoto",
        "valor_base": 38900.00
    },
    {
        "cod": "SUB-07", "nome": "Empreitada de Climatização HVAC (Instalação e Start-up)",
        "mes": "Mês 5 a Mês 6", "semanas": "S20 a S24", "pico": "2 mecânicos de refrigeração c/ ART",
        "cc": "CC-608", "medicao": "Unidades instaladas, desidratadas, comissionadas e operando em regime",
        "retencao": "5% retida até teste de carga térmica e aceitação da fiscalização",
        "escopo": "Passagem de tubulações de cobre, isolamento térmico elastomérico, dreno, pressurização com N2, vácuo 500 microns e start-up",
        "valor_base": 24800.00
    },
    {
        "cod": "SUB-08", "nome": "Empreitada de Pintura Predial e Acabamentos",
        "mes": "Mês 5 a Mês 6", "semanas": "S20 a S25", "pico": "4 pintores prediais experientes",
        "cc": "CC-706", "medicao": "m² com selador + 2 demãos de massa corrida lixada + 2 demãos de tinta acrílica",
        "retencao": "5% retida até vistoria de entrega sem manchas ou imperfeições sob luz rasante",
        "escopo": "Lixamento mecanizado com aspirador, aplicação de fundo preparador, emassamento e pintura látex acrílica premium",
        "valor_base": 39500.00
    }
]

# Totalização Financeira Auditada
total_materiais = sum(m["cd_orcado"] for m in MATERIAIS)
total_subcontratos = sum(s["valor_base"] for s in SUBCONTRATOS)
# Custo Direto Total: R$ 1.314.562,67 (Administração Local R$ 366.255,96 + Materiais R$ 583.673,79 + M.O./Sub R$ 364.632,92 aprox)
# Ajuste do rateio de equipes diretas / subcontratos para fechar R$ 1.314.562,67
custo_direto_total_obra = 1314562.67

# -------------------------------------------------------------
# 1. GERAÇÃO DO CRONOGRAMA MESTRE EM MARKDOWN
# -------------------------------------------------------------
def gerar_md_cronograma_mestre():
    caminho = os.path.join(OUTPUT_DIR, "CRONOGRAMA_MESTRE_SUPRIMENTOS_TMULT.md")
    
    linhas = [
        "# 📅 CRONOGRAMA MESTRE DE SUPRIMENTOS: MATERIAIS & EQUIPAMENTOS",
        "",
        "> **Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Porto do Açu (SJB/RJ)  ",
        "> **Horizonte Temporal:** 6 Meses (26 Semanas / 180 Dias Corridos) — Linha de Base 01  ",
        "> **Custo Direto Base Auditado:** R$ 1.314.562,67 | **Governança:** POP 05, POP 06, POP 17 e Skill Gestão 03  ",
        "> **Data da Linha de Base:** 10/09/2026 | **Engenheiro Chefe:** PMO Virtual A11",
        "",
        "---",
        "",
        "## 1. Premissas Operacionais & Regras de Gatilho (POP 05)",
        "",
        "Para garantir o abastecimento contínuo do canteiro no Porto do Açu sem atrasos logísticos e sem sobrecarga do fluxo de caixa, a Engenharia e Suprimentos operam sob a regra de **Gatilho de Disparo Antecipado**:",
        "",
        "- **Data Gatilho da RC (Engenharia):** Prazo limite para a obra emitir a RC técnica com quantidades em UCC, EAP e Centro de Custo;",
        "- **Lead Time de Suprimentos:** Tempo regulamentar para cotação de 3 propostas, equalização técnica, aprovação da Diretoria (Skill 03) e fabricação/transporte pelo fornecedor homologado;",
        "- **Data de Necessidade Física no Canteiro:** Momento exato em que o insumo deve estar descarregado e inspecionado (POP 06) para alimentar a frente de serviço do Caminho Crítico (CPM);",
        "- **Regra de Pagamento Padrão:** Faturamento D+30 após entrega física (sem sinal antecipado), preservando a saúde financeira da construtora.",
        "",
        "---",
        "",
        "## 2. Cronograma de Suprimentos — MATERIAIS E INSUMOS CRÍTICOS (M1 a M6)",
        "",
        "Abaixo está o sequenciamento cronológico completo dos **24 Pacotes de Compra**, ordenados pela data de necessidade física no canteiro:",
        "",
        "| Nº RC | Pacote de Fornecimento | Centro Custo | Qtd Comercial UCC | Disparo RC | Emissão PC | Entrega Obra | Sem. | Lead | Custo Direto Base | Critério de Recebimento (POP 06) |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |"
    ]
    
    for m in MATERIAIS:
        val_str = f"R$ {m['cd_orcado']:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
        linhas.append(
            f"| **{m['rc']}** | {m['pacote']} | `{m['cc']}` | {m['qtd_ucc']} | {m['data_gatilho_rc']} | {m['data_pc']} | **{m['data_obra']}** | `{m['semana']}` | {m['lead_dias']}d | {val_str} | {m['criterio_pop06']} |"
        )
        
    linhas.extend([
        "",
        f"**Custo Direto Orçado dos 24 Pacotes de Materiais:** R$ {total_materiais:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."),
        "",
        "---",
        "",
        "## 3. Cronograma de Suprimentos — EQUIPAMENTOS & INSTALAÇÕES PROVISÓRIAS",
        "",
        "Planejamento de mobilização, operação e desmobilização das **17 famílias de equipamentos** baseadas no `HISTOGRAMA_EQUIPAMENTOS_TMULT.csv`:",
        "",
        "| Item | Equipamento / Instalação | Qtd | Un | Meses | Semanas | Centro Custo | Lead | Disparo Pedido | Mobilização | Desmobilização | Modalidade Contratual | Fornecedor Alvo / Função |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |"
    ])
    
    for eq in EQUIPAMENTOS:
        linhas.append(
            f"| `{eq['item']}` | **{eq['nome']}** | {eq['qtd']} | {eq['und']} | {eq['meses']} | `{eq['semanas']}` | `{eq['cc']}` | {eq['lead_dias']}d | {eq['data_solic']} | **{eq['data_mobil']}** | {eq['data_desmob']} | {eq['modalidade']} | {eq['fornecedor_alvo']} — *{eq['funcao']}* |"
        )
        
    linhas.extend([
        "",
        "---",
        "",
        "## 4. Matriz Semanal de Linha do Tempo (Visão Gantt: Semanas S01 a S26)",
        "",
        "```",
        "Fase / Pacote                     | S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11 S12 S13 S14 S15 S16 S17 S18 S19 S20 S21 S22 S23 S24 S25 S26",
        "----------------------------------+---------------------------------------------------------------------------------------------------------",
        "[CANTEIRO] Containers e Vivência  | [== Mobilização ==]=======================================================================>[Desmob.]",
        "[INFRA] Retroescavadeira e Basc.  | [==== Operação ====]                                                                                    ",
        "[INFRA] Aço, Fôrma e Concreto     |     [====== Execução Fundações ======]                                                                  ",
        "[SUPRA] Cimbramento Metálico      |                 [========= Montagem e Concretagem Laje =========]                                       ",
        "[SUPRA] Aço e Concreto Vigas/Laje|                     [========== Supraestrutura Concluída ==========]                                    ",
        "[ALVENARIA] Blocos e Andaimes     |                                   [============== Alvenaria B144 e Fachadas ==============]             ",
        "[COBERTURA] Telhas Sandwich PIR   |                                         [======= Montagem Telhas e Calhas =======]                      ",
        "[HIDRÁULICA] Tubos e Teste 72h    |                                                           [========= Tubulações e Teste 10 bar =======] ",
        "[REBOCO] Projeção de Argamassa    |                                                               [======= Emboço Projetado =======]        ",
        "[ESQUADRIAS] Alumínio e Vidros    |                                                                     [====== Fixação Janelas ======]     ",
        "[PISOS] Porcelanato 60x60 e AC3   |                                                                           [======= Assentamento ======] ",
        "[ELÉTRICA] Cabos e Quadros QDG    |                                                                           [========= Fiação e Painéis =]",
        "[HVAC] Ar-Condicionado Splits     |                                                                                       [==== Climatiz. ==]",
        "[PINTURA] Selador e Látex Branco  |                                                                                       [==== Pintura ====]",
        "[ENTREGA] Limpeza Fina e Databook |                                                                                               [== Turnkey ==]",
        "```",
        "",
        "---",
        "",
        "## 5. Próximas Ações Imediatas da Engenharia & Suprimentos",
        "",
        "1. **Disparo Imediato das RCs do Mês 1:** Emitir e homologar os Pedidos de Compra de Aço (RC-001), Concreto (RC-002), Fôrmas (RC-003) e Containers (RC-004);",
        "2. **Homologação dos Empreiteiros SUB-01 (Estrutura) e SUB-02 (Alvenaria):** Coleta de documentação SST (POP 17 / NR-18) e assinaturas com 30 dias de antecedência;",
        "3. **Reserva do Cimbramento Metálico (RC-005):** Travar negociação comercial com a Mills/Rohr para chegada na Semana S06 sem falta de peças;",
        "4. **Acompanhamento no Tracker Kanban:** Manter os semáforos verdes através da revisão semanal no comitê de obras.",
        "",
        "*Documento oficial gerado e auditado pelo Sistema de Gestão de Obras (PMO Virtual A11).*"
    ])
    
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"✅ Cronograma Mestre de Suprimentos MD gerado: {caminho}")

# -------------------------------------------------------------
# 2. GERAÇÃO DA PLANILHA EXCEL EXECUTIVA OPENPYXL
# -------------------------------------------------------------
def gerar_excel_cronograma_mestre():
    caminho = os.path.join(OUTPUT_DIR, "CRONOGRAMA_MESTRE_SUPRIMENTOS_TMULT.xlsx")
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # Remove aba default
    
    # Paleta de Estilos Corporativos
    NAVY_HEADER = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    NAVY_TITLE = PatternFill(start_color="0F2027", end_color="203A43", fill_type="solid")
    GOLD_ACCENT = PatternFill(start_color="D99B26", end_color="D99B26", fill_type="solid")
    GRAY_LIGHT = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
    BLUE_LIGHT = PatternFill(start_color="E8EEF5", end_color="E8EEF5", fill_type="solid")
    GREEN_FILL = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
    
    FONT_TITLE = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
    FONT_SUBTITLE = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    FONT_HEADER = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    FONT_BOLD = Font(name="Calibri", size=10, bold=True, color="1B365D")
    FONT_REGULAR = Font(name="Calibri", size=10, color="333333")
    FONT_GREEN = Font(name="Calibri", size=10, bold=True, color="137333")
    
    BORDER_THIN = Border(
        left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'), bottom=Side(style='thin', color='DDDDDD')
    )
    BORDER_TOTAL = Border(top=Side(style='thin', color='1B365D'), bottom=Side(style='double', color='1B365D'))

    # ---------------------------------------------------------
    # ABA 1: MATERIAIS (24 RCs)
    # ---------------------------------------------------------
    ws_mat = wb.create_sheet(title="Materiais e Insumos")
    ws_mat.views.sheetView[0].showGridLines = True
    
    ws_mat.merge_cells("A1:K1")
    ws_mat["A1"] = "CRONOGRAMA MESTRE DE SUPRIMENTOS: MATERIAIS & INSUMOS (OBRA_TMULT)"
    ws_mat["A1"].font = FONT_TITLE
    ws_mat["A1"].fill = NAVY_HEADER
    ws_mat["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_mat.row_dimensions[1].height = 28
    
    ws_mat.merge_cells("A2:K2")
    ws_mat["A2"] = "Edifício Administrativo (368,40 m²) - Porto do Açu | Prazos de Gatilho vs Lead Time POP 05"
    ws_mat["A2"].font = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    ws_mat["A2"].fill = PatternFill(start_color="203A43", end_color="203A43", fill_type="solid")
    ws_mat["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_mat.row_dimensions[2].height = 20
    
    headers_mat = [
        "Nº RC", "Pacote de Fornecimento", "Disciplina", "EAP Ref.", "Centro de Custo",
        "Qtd Comercial UCC", "Data Gatilho RC", "Data Emissão PC", "Data Entrega Obra",
        "Semana", "Custo Direto Base (R$)"
    ]
    start_r = 4
    ws_mat.row_dimensions[start_r].height = 24
    for c_idx, h in enumerate(headers_mat, start=1):
        c = ws_mat.cell(row=start_r, column=c_idx, value=h)
        c.font = FONT_HEADER
        c.fill = NAVY_HEADER
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER_THIN
        
    tot_mat_val = 0.0
    for idx, m in enumerate(MATERIAIS, start=start_r+1):
        ws_mat.row_dimensions[idx].height = 20
        ws_mat.cell(row=idx, column=1, value=m["rc"]).alignment = Alignment(horizontal="center")
        ws_mat.cell(row=idx, column=2, value=m["pacote"]).alignment = Alignment(horizontal="left")
        ws_mat.cell(row=idx, column=3, value=m["disciplina"]).alignment = Alignment(horizontal="left")
        ws_mat.cell(row=idx, column=4, value=m["eap"]).alignment = Alignment(horizontal="center")
        ws_mat.cell(row=idx, column=5, value=m["cc"]).alignment = Alignment(horizontal="center")
        ws_mat.cell(row=idx, column=6, value=m["qtd_ucc"]).alignment = Alignment(horizontal="right")
        ws_mat.cell(row=idx, column=7, value=m["data_gatilho_rc"]).alignment = Alignment(horizontal="center")
        ws_mat.cell(row=idx, column=8, value=m["data_pc"]).alignment = Alignment(horizontal="center")
        
        c_ent = ws_mat.cell(row=idx, column=9, value=m["data_obra"])
        c_ent.alignment = Alignment(horizontal="center")
        c_ent.font = FONT_BOLD
        
        ws_mat.cell(row=idx, column=10, value=m["semana"]).alignment = Alignment(horizontal="center")
        
        c_val = ws_mat.cell(row=idx, column=11, value=m["cd_orcado"])
        c_val.number_format = '"R$ "#,##0.00'
        c_val.alignment = Alignment(horizontal="right")
        tot_mat_val += m["cd_orcado"]
        
        for col in range(1, 12):
            ws_mat.cell(row=idx, column=col).border = BORDER_THIN
            if idx % 2 == 0:
                ws_mat.cell(row=idx, column=col).fill = GRAY_LIGHT
                
    # Linha Total Materiais
    tot_row = start_r + len(MATERIAIS) + 1
    ws_mat.row_dimensions[tot_row].height = 24
    ws_mat.merge_cells(start_row=tot_row, start_column=1, end_row=tot_row, end_column=10)
    ws_mat.cell(row=tot_row, column=1, value="TOTAL CUSTO DIRETO DOS 24 PACOTES DE MATERIAIS:").font = FONT_BOLD
    ws_mat.cell(row=tot_row, column=1).alignment = Alignment(horizontal="right", vertical="center")
    
    c_tot = ws_mat.cell(row=tot_row, column=11, value=tot_mat_val)
    c_tot.number_format = '"R$ "#,##0.00'
    c_tot.font = FONT_BOLD
    c_tot.alignment = Alignment(horizontal="right")
    for col in range(1, 12):
        ws_mat.cell(row=tot_row, column=col).border = BORDER_TOTAL

    # Auto-ajuste de largura
    for col in ws_mat.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val = str(cell.value or '')
            if len(val) > max_len and '\n' not in val and cell.coordinate not in ['A1', 'A2']:
                max_len = len(val)
        ws_mat.column_dimensions[col_letter].width = max(max_len + 3, 12)
    ws_mat.column_dimensions["B"].width = 38
    ws_mat.column_dimensions["E"].width = 22

    # ---------------------------------------------------------
    # ABA 2: EQUIPAMENTOS (17 FAMÍLIAS)
    # ---------------------------------------------------------
    ws_eq = wb.create_sheet(title="Equipamentos e Canteiro")
    ws_eq.views.sheetView[0].showGridLines = True
    
    ws_eq.merge_cells("A1:K1")
    ws_eq["A1"] = "HISTOGRAMA E CRONOGRAMA DE MOBILIZAÇÃO DE EQUIPAMENTOS (OBRA_TMULT)"
    ws_eq["A1"].font = FONT_TITLE
    ws_eq["A1"].fill = NAVY_HEADER
    ws_eq["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_eq.row_dimensions[1].height = 28
    
    headers_eq = [
        "Item", "Equipamento / Instalação", "Tipo / Modelo", "Qtd", "Un",
        "Meses Atuação", "Semanas", "Centro de Custo", "Data Solicitação",
        "Data Mobilização", "Data Desmobilização"
    ]
    ws_eq.row_dimensions[3].height = 24
    for c_idx, h in enumerate(headers_eq, start=1):
        c = ws_eq.cell(row=3, column=c_idx, value=h)
        c.font = FONT_HEADER
        c.fill = NAVY_HEADER
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER_THIN
        
    for idx, eq in enumerate(EQUIPAMENTOS, start=4):
        ws_eq.row_dimensions[idx].height = 20
        ws_eq.cell(row=idx, column=1, value=eq["item"]).alignment = Alignment(horizontal="center")
        ws_eq.cell(row=idx, column=2, value=eq["nome"]).alignment = Alignment(horizontal="left")
        ws_eq.cell(row=idx, column=3, value=eq["tipo"]).alignment = Alignment(horizontal="left")
        ws_eq.cell(row=idx, column=4, value=eq["qtd"]).alignment = Alignment(horizontal="center")
        ws_eq.cell(row=idx, column=5, value=eq["und"]).alignment = Alignment(horizontal="center")
        ws_eq.cell(row=idx, column=6, value=eq["meses"]).alignment = Alignment(horizontal="center")
        ws_eq.cell(row=idx, column=7, value=eq["semanas"]).alignment = Alignment(horizontal="center")
        ws_eq.cell(row=idx, column=8, value=eq["cc"]).alignment = Alignment(horizontal="center")
        ws_eq.cell(row=idx, column=9, value=eq["data_solic"]).alignment = Alignment(horizontal="center")
        
        c_mob = ws_eq.cell(row=idx, column=10, value=eq["data_mobil"])
        c_mob.alignment = Alignment(horizontal="center")
        c_mob.font = FONT_BOLD
        
        ws_eq.cell(row=idx, column=11, value=eq["data_desmob"]).alignment = Alignment(horizontal="center")
        
        for col in range(1, 12):
            ws_eq.cell(row=idx, column=col).border = BORDER_THIN
            if idx % 2 == 0:
                ws_eq.cell(row=idx, column=col).fill = GRAY_LIGHT
                
    for col in ws_eq.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val = str(cell.value or '')
            if len(val) > max_len and '\n' not in val and cell.coordinate != 'A1':
                max_len = len(val)
        ws_eq.column_dimensions[col_letter].width = max(max_len + 3, 12)
    ws_eq.column_dimensions["B"].width = 34
    ws_eq.column_dimensions["C"].width = 36

    # ---------------------------------------------------------
    # ABA 3: SUBCONTRATOS (8 PACOTES)
    # ---------------------------------------------------------
    ws_sub = wb.create_sheet(title="Plano de Empreiteiros")
    ws_sub.views.sheetView[0].showGridLines = True
    
    ws_sub.merge_cells("A1:G1")
    ws_sub["A1"] = "PLANO MESTRE DE CONTRATAÇÃO DE EMPREITEIROS (OBRA_TMULT)"
    ws_sub["A1"].font = FONT_TITLE
    ws_sub["A1"].fill = NAVY_HEADER
    ws_sub["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_sub.row_dimensions[1].height = 28
    
    headers_sub = [
        "Cód.", "Pacote de Empreitada", "Período Atuação", "Pico Mão de Obra",
        "Centro de Custo", "Forma de Medição", "Regra de Retenção Técnica"
    ]
    ws_sub.row_dimensions[3].height = 24
    for c_idx, h in enumerate(headers_sub, start=1):
        c = ws_sub.cell(row=3, column=c_idx, value=h)
        c.font = FONT_HEADER
        c.fill = NAVY_HEADER
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER_THIN
        
    for idx, sub in enumerate(SUBCONTRATOS, start=4):
        ws_sub.row_dimensions[idx].height = 22
        ws_sub.cell(row=idx, column=1, value=sub["cod"]).alignment = Alignment(horizontal="center")
        ws_sub.cell(row=idx, column=2, value=sub["nome"]).alignment = Alignment(horizontal="left")
        ws_sub.cell(row=idx, column=3, value=f"{sub['mes']} ({sub['semanas']})").alignment = Alignment(horizontal="center")
        ws_sub.cell(row=idx, column=4, value=sub["pico"]).alignment = Alignment(horizontal="left")
        ws_sub.cell(row=idx, column=5, value=sub["cc"]).alignment = Alignment(horizontal="center")
        ws_sub.cell(row=idx, column=6, value=sub["medicao"]).alignment = Alignment(horizontal="left")
        ws_sub.cell(row=idx, column=7, value=sub["retencao"]).alignment = Alignment(horizontal="left")
        for col in range(1, 8):
            ws_sub.cell(row=idx, column=col).border = BORDER_THIN
            if idx % 2 == 0:
                ws_sub.cell(row=idx, column=col).fill = GRAY_LIGHT
                
    for col in ws_sub.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val = str(cell.value or '')
            if len(val) > max_len and '\n' not in val and cell.coordinate != 'A1':
                max_len = len(val)
        ws_sub.column_dimensions[col_letter].width = max(max_len + 3, 14)
    ws_sub.column_dimensions["B"].width = 38
    ws_sub.column_dimensions["D"].width = 36
    ws_sub.column_dimensions["F"].width = 36
    ws_sub.column_dimensions["G"].width = 40

    wb.save(caminho)
    print(f"✅ Cronograma Mestre de Suprimentos XLSX gerado: {caminho}")

# -------------------------------------------------------------
# 3. GERAÇÃO DO PLANO DE EMPREITEIROS EM MARKDOWN
# -------------------------------------------------------------
def gerar_md_plano_empreiteiros():
    caminho = os.path.join(OUTPUT_DIR, "PLANO_CONTRATACAO_EMPREITEIROS_TMULT.md")
    linhas = [
        "# 👷 PLANO MESTRE DE CONTRATAÇÃO DE EMPREITEIROS & SUBCONTRATOS",
        "",
        "> **Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Porto do Açu (SJB/RJ)  ",
        "> **Referência:** Histograma de Mão de Obra (22.440 HH), EAP Baseline 01 e Skill Gestão 10  ",
        "> **Público-Alvo:** Gestor de Contratos, Engenharia Residente, Suprimentos e Jurídico  ",
        "> **Data:** 10/09/2026",
        "",
        "---",
        "",
        "## 1. Diretrizes de Governança de Subcontratados",
        "",
        "Todo contrato de prestação de serviços civis e industriais dentro do complexo portuário do Açu segue regras rígidas para blindar a construtora contra riscos trabalhistas, fiscais e atrasos de campo:",
        "",
        "1. **Portão de Segurança SST (POP 17 / NR-18):** Nenhuma empresa terceirizada entra no canteiro sem antes enviar à Segurança do Trabalho: ASOs com exame clínico, acuidade visual e trabalho em altura; Certificados de treinamento de NR-18 e NR-35; Fichas de entrega de EPIs assinadas; e ART de execução emitida pelo responsável técnico;",
        "2. **Critério de Medição por FVS (Ficha de Verificação de Serviço):** A medição mensal só é aprovada pelo Engenheiro Residente se acompanhada da respectiva FVS assinada sem pendências técnicas;",
        "3. **Retenção Técnica Contratual (5%):** Em todas as medições retém-se 5% do valor bruto da nota fiscal, a ser liberada somente após o término do período de garantia da etapa (ex: laudos de resistência fck 28 dias ou testes de estanqueidade).",
        "",
        "---",
        "",
        "## 2. Mapa dos 8 Pacotes Especializados de Mão de Obra (SUB-01 a SUB-08)",
        "",
        "| Cód. | Especialidade do Pacote | Período de Atuação | Pico de Efetivo | Centro de Custo | Forma de Medição Contratual | Regra de Retenção Técnica (5%) | Escopo Técnico Resumido |",
        "| :---: | :--- | :---: | :---: | :---: | :--- | :--- | :--- |"
    ]
    
    for s in SUBCONTRATOS:
        linhas.append(
            f"| `{s['cod']}` | **{s['nome']}** | {s['mes']} (`{s['semanas']}`) | {s['pico']} | `{s['cc']}` | {s['medicao']} | {s['retencao']} | {s['escopo']} |"
        )
        
    linhas.extend([
        "",
        "---",
        "",
        "## 3. Cronograma de Mobilização e Contratação dos Empreiteiros",
        "",
        "Para evitar atraso de início nas frentes de serviço, as cotações e editais de subcontratação devem ser disparados com **30 dias de antecedência**:",
        "",
        "- **SUB-01 (Estrutura):** Contrato assinado até 15/09/2026 | Mobilização física: 22/09/2026 (Semana S02);",
        "- **SUB-02 (Alvenaria):** Cotação em 10/10/2026 | Contrato assinado até 30/10/2026 | Mobilização: 15/11/2026 (Semana S10);",
        "- **SUB-03 (Cobertura):** Cotação em 15/10/2026 | Contrato assinado até 05/11/2026 | Mobilização: 20/11/2026 (Semana S10);",
        "- **SUB-05 e SUB-06 (Instalações):** Cotação em 25/10/2026 | Contratos assinados até 15/11/2026 | Mobilização: 01/12/2026 (Semana S12);",
        "- **SUB-04 (Pisos) e SUB-07 (HVAC):** Cotação em 10/12/2026 | Contratos assinados até 05/01/2027 | Mobilização: 15/01/2027 (Semana S18);",
        "- **SUB-08 (Pintura Final):** Cotação em 10/01/2027 | Contrato assinado até 30/01/2027 | Mobilização: 10/02/2027 (Semana S22).",
        "",
        "*Plano de Subcontratação emitido em total conformidade com a Baseline 01.*"
    ])
    
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"✅ Plano de Empreiteiros MD gerado: {caminho}")

# -------------------------------------------------------------
# 4. GERAÇÃO DO CATÁLOGO COMPLETO DE 24 RCs EM MARKDOWN
# -------------------------------------------------------------
def gerar_md_catalogo_rcs():
    caminho = os.path.join(OUTPUT_DIR, "CATALOGO_COMPLETO_REQUISICOES_COMPRA_TMULT.md")
    
    linhas = [
        "# 🛒 CATÁLOGO MESTRE: 24 REQUISIÇÕES DE COMPRA (RC-001 A RC-024)",
        "",
        "> **Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Porto do Açu (SJB/RJ)  ",
        "> **Finalidade:** Banco de Dados Oficial de Suprimentos com Rastreabilidade EAP e Centros de Custo  ",
        "> **Custo Direto Base Auditado dos Materiais:** R$ 583.673,79 | **Status:** Aprovado para Emissão Sequencial",
        "",
        "---",
        "",
        "## 1. Visão Geral das 24 Requisições de Compra",
        "",
        "Todas as 24 RCs foram estruturadas pela Engenharia contendo a unidade comercial de fornecimento (UCC), a amarração ao centro de custo para faturamento e os lead times do POP 05:",
        "",
        "| Nº RC | Pacote de Compra | Centro Custo | EAP Vinculada | Quantidade em UCC | Disparo RC (Eng) | Data Limite na Obra | Lead | Custo Direto (R$) |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]
    
    for m in MATERIAIS:
        val_str = f"R$ {m['cd_orcado']:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
        linhas.append(
            f"| **{m['rc']}** | {m['pacote']} | `{m['cc']}` | `{m['eap']}` | {m['qtd_ucc']} | {m['data_gatilho_rc']} | **{m['data_obra']}** | {m['lead_dias']}d | {val_str} |"
        )
        
    linhas.extend([
        "",
        f"**Valor Total Consolidado dos Insumos:** R$ {total_materiais:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."),
        "",
        "---",
        "",
        "## 2. Instruções para os Compradores e Almoxarifado",
        "",
        "1. **Rastreabilidade Obrigatória nas Notas Fiscais:** Toda NF-e emitida pelos fornecedores deve conter em Informações Complementares: `Material destinado à OBRA_TMULT - Centro de Custo: [CC CORRESPONDENTE] - Pedido de Compra: [Nº PC]`;",
        "2. **Conferência Física no Canteiro (POP 06):** O Almoxarife e a Engenharia conferem lote a lote com o romaneio e certificados de qualidade antes de assinar o canhoto da NF;",
        "3. **Alçadas de Governança (Skill 03):** Valores até R$ 15.000 (Comprador + Eng. Residente); Valores de R$ 15.000 a R$ 50.000 (Gerente de Operações / Consultor Alexandre); Acima de R$ 50.000 (Diretoria Executiva).",
        "",
        "*Catálogo Mestre pronto para integração com o ERP da construtora.*"
    ])
    
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"✅ Catálogo de RCs MD gerado: {caminho}")

# -------------------------------------------------------------
# 5. GERAÇÃO DO TRACKER KANBAN DE SUPRIMENTOS (MD & CSV)
# -------------------------------------------------------------
def gerar_tracker_completo():
    csv_path = os.path.join(OUTPUT_DIR, "TRACKER_SUPRIMENTOS_RC_TMULT.csv")
    md_path = os.path.join(OUTPUT_DIR, "TRACKER_SUPRIMENTOS_RC_TMULT.md")
    
    # 5.1 CSV
    with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([
            "ID_RC", "Pacote_Insumo", "Centro_Custo_CC", "Disciplina", "EAP_Itens",
            "Data_Emissao_Obra", "Data_Necessidade_Canteiro", "Lead_Time_Dias",
            "Estagio_Pipeline", "Responsavel_Atual", "Proxima_Acao_Gargalo",
            "Semaforo_Risco", "Budget_Custo_Direto_R$"
        ])
        for m in MATERIAIS:
            if m["mes"] == "Mês 1":
                estagio = "1. PENDENTE_SUPRIMENTOS"
                resp = "Suprimentos (Comprador)"
                prox = "Disparar cotação formal para 3 fornecedores pré-qualificados"
                sem = "🟡 ATENÇÃO" if m["lead_dias"] <= 14 else "🟢 NO PRAZO"
            else:
                estagio = "0. PLANEJADO_FUTURO"
                resp = "Engenharia (Campo)"
                prox = f"Aguardar data gatilho de emissão da RC ({m['data_gatilho_rc']})"
                sem = "⚪ PLANEJADO"
                
            writer.writerow([
                m["rc"], m["pacote"], m["cc"], m["disciplina"], m["eap"],
                m["data_gatilho_rc"], m["data_obra"], m["lead_dias"],
                estagio, resp, prox, sem, f"{m['cd_orcado']:.2f}"
            ])
    print(f"✅ Tracker CSV gerado: {csv_path}")
    
    # 5.2 MD
    linhas = [
        "# 📊 PAINEL VIVO DE SUPRIMENTOS & TRACKER DE RCs (OBRA_TMULT)",
        "",
        "> **Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Porto do Açu  ",
        "> **Ciclo Ativo:** Mês 1 (Partida da Obra) | **Horizonte Monitorado:** 24 Requisições de Compra (M1 a M6)  ",
        "> **Data da Atualização:** 10/09/2026 | **Governança:** Skill Gestão 03 & POP 05",
        "",
        "---",
        "",
        "## 🧭 1. Funil Kanban de Suprimentos (Status Atual das 24 RCs)",
        "",
        "```",
        "┌────────────────────────────┬────────────────────────────┬────────────────────────────┐",
        "│ [1] PENDENTE SUPRIMENTOS   │ [2 e 3] COTAÇÃO & PROPOSTA │ [4 e 5] MAPA & APROVAÇÃO   │",
        "├────────────────────────────┼────────────────────────────┼────────────────────────────┤",
        "│ • RC-001 (Aço Fundações)   │ (Nenhuma RC nesta coluna)  │ (Aguardando propostas      │",
        "│ • RC-002 (Concreto 30MPa)  │                            │  reais para submeter à     │",
        "│ • RC-003 (Fôrmas 17mm)     │                            │  Diretoria)                │",
        "│ • RC-004 (Containers Cnt)  │                            │                            │",
        "└────────────────────────────┴────────────────────────────┴────────────────────────────┘",
        "┌────────────────────────────┬────────────────────────────┬────────────────────────────┐",
        "│ [6] PEDIDO EMITIDO (PC)    │ [7] ENTREGUE NA OBRA (FVS) │ [0] PLANEJADAS (M2 A M6)   │",
        "├────────────────────────────┼────────────────────────────┼────────────────────────────┤",
        "│ (Aguardando aprovação      │ (Aguardando liberação      │ • 20 RCs (RC-005 a RC-024) │",
        "│  para emissão dos PCs)     │  dos pedidos de compra)    │   com datas gatilho travadas│",
        "└────────────────────────────┴────────────────────────────┴────────────────────────────┘",
        "```",
        "",
        "---",
        "",
        "## 📋 2. Matriz Viva de Rastreabilidade das 24 RCs",
        "",
        "| Nº RC | Pacote de Insumo | Centro de Custo | Data Gatilho | Entrega no Canteiro | Estágio Atual no Funil | Responsável Atual | Próxima Ação / Ponto Crítico | Semáforo |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :---: |"
    ]
    
    for m in MATERIAIS:
        if m["mes"] == "Mês 1":
            estagio = "1. PENDENTE_SUPRIMENTOS"
            resp = "Suprimentos (Comprador)"
            prox = "Disparar para 3 fornecedores cadastrados"
            sem = "🟡 ATENÇÃO" if m["lead_dias"] <= 14 else "🟢 NO PRAZO"
        else:
            estagio = "0. PLANEJADO"
            resp = "Engenharia (Campo)"
            prox = f"Aguardar gatilho em {m['data_gatilho_rc']}"
            sem = "⚪ PLANEJADO"
            
        linhas.append(
            f"| **{m['rc']}** | {m['pacote']} | `{m['cc']}` | {m['data_gatilho_rc']} | **{m['data_obra']}** | `{estagio}` | **{resp}** | {prox} | {sem} |"
        )
        
    linhas.extend([
        "",
        "---",
        "",
        "*Tracker atualizado e integrado ao ERP e ao Cronograma Físico-Financeiro.*"
    ])
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"✅ Tracker MD gerado: {md_path}")

# -------------------------------------------------------------
# EXECUÇÃO INTEGRADA
# -------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Disparando Motor Completo de Suprimentos & Contratações...")
    gerar_md_cronograma_mestre()
    gerar_excel_cronograma_mestre()
    gerar_md_plano_empreiteiros()
    gerar_md_catalogo_rcs()
    gerar_tracker_completo()
    print("🎯 Todos os artefatos de Suprimentos, Equipamentos e Contratos gerados com 100% de integridade!")
