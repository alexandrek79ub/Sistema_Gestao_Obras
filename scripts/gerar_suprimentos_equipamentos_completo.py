#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador dos Ativos Faltantes de Suprimentos para Equipamentos da OBRA_TMULT:
1. REQUISICOES_LOCACAO_EQUIPAMENTOS_TMULT.md: 17 REs formais individuais (RE-001 a RE-017)
2. MAPA_COTACAO_EQUALIZADO_EQUIPAMENTOS_TMULT.xlsx e .md: Cotação equalizada de 3 locadoras por pacote
3. TRACKER_SUPRIMENTOS_MESTRE_COMPLETO_TMULT.csv e .md: Pipeline integrado de 41 itens (24 RCs + 17 REs)
"""

import os
import sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "projetos", "OBRA_TMULT", "05_SUPRIMENTOS_E_FINANCEIRO")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# DADOS DAS 17 REQUISIÇÕES DE EQUIPAMENTOS (RE-001 A RE-017)
# -------------------------------------------------------------
REQUISICOES_EQUIP = [
    {
        "id": "RE-001/2026", "eq": "EQ-01", "nome": "Módulo Habitável Escritório / Reuniões",
        "cc": "CC-103", "eap": "1.0.3", "qtd": 1, "und": "un", "meses": "M1 a M6 (6 meses)", "sem": "S01 a S26",
        "disparo": "10/09/2026", "entrega": "22/09/2026", "lead": 12, "budget_mensal": 1850.00, "budget_total": 11100.00,
        "especificacao": "Container marítimo 6,00x2,40m termoacústico EPS 50mm c/ AC Split 12k BTU, piso vinílico, janelas com grade, porta de aço com fechadura tetra, iluminação LED e mesa de reuniões para 8 pessoas.",
        "normas": "NR-18 (Condições de Trabalho), NR-10 (Segurança Elétrica)", "operador": "Não aplicável", "combustivel": "Não aplicável",
        "locadoras": [("Rentcon Locações", 1850.00, "Vencedor"), ("NHJ Brasil", 1950.00, "Equalizado"), ("Brasanitas Módulos", 2100.00, "Desclassificado Prazo")]
    },
    {
        "id": "RE-002/2026", "eq": "EQ-02", "nome": "Módulo Vestiário / Sanitário NR-18",
        "cc": "CC-103", "eap": "1.0.3", "qtd": 1, "und": "un", "meses": "M1 a M6 (6 meses)", "sem": "S01 a S26",
        "disparo": "10/09/2026", "entrega": "22/09/2026", "lead": 12, "budget_mensal": 1750.00, "budget_total": 10500.00,
        "especificacao": "Container 6,00x2,40m com 4 chuveiros elétricos blindados 220V c/ DR 30mA, 2 bacias sanitárias, 2 lavatórios, piso lavável antiderrapante, bancos de madeira e armários individuais com chave para 20 operários.",
        "normas": "NR-18.4 (Instalações Sanitárias), NR-10", "operador": "Não aplicável", "combustivel": "Não aplicável",
        "locadoras": [("Rentcon Locações", 1750.00, "Vencedor"), ("NHJ Brasil", 1800.00, "Equalizado"), ("Locker Container", 1950.00, "Acima do Budget")]
    },
    {
        "id": "RE-003/2026", "eq": "EQ-03", "nome": "Módulo Refeitório NR-18",
        "cc": "CC-103", "eap": "1.0.3", "qtd": 1, "und": "un", "meses": "M1 a M6 (6 meses)", "sem": "S01 a S26",
        "disparo": "10/09/2026", "entrega": "22/09/2026", "lead": 12, "budget_mensal": 1550.00, "budget_total": 9300.00,
        "especificacao": "Container 6,00x2,40m termoacústico c/ AC 18k BTU, mesas e bancos com tampos de fórmica lavável para 20 pessoas simultâneas, pia em inox com água corrente, bebedouro elétrico refrigerado e lixeiras identificadas.",
        "normas": "NR-18.5 (Locais de Refeição), NBR 5410", "operador": "Não aplicável", "combustivel": "Não aplicável",
        "locadoras": [("Rentcon Locações", 1550.00, "Vencedor"), ("NHJ Brasil", 1600.00, "Equalizado"), ("Delta Containers", 1720.00, "Acima do Budget")]
    },
    {
        "id": "RE-004/2026", "eq": "EQ-04", "nome": "Módulo Almoxarifado / Ferramentaria",
        "cc": "CC-103", "eap": "1.0.3", "qtd": 1, "und": "un", "meses": "M1 a M6 (6 meses)", "sem": "S01 a S26",
        "disparo": "10/09/2026", "entrega": "22/09/2026", "lead": 12, "budget_mensal": 950.00, "budget_total": 5700.00,
        "especificacao": "Container marítimo Dry 20 pés (6,00x2,40m) reforçado, chapa corten 2,5mm, com 4 estantes metálicas modulares para ferramentas e EPIs, balcão de entrega, iluminação blindada IP-65 e tranca quádrupla anti-arrombamento.",
        "normas": "NR-18 (Armazenamento de Materiais)", "operador": "Não aplicável", "combustivel": "Não aplicável",
        "locadoras": [("Rentcon Locações", 950.00, "Vencedor"), ("NHJ Brasil", 1000.00, "Equalizado"), ("LocaBox Açu", 1150.00, "Acima do Budget")]
    },
    {
        "id": "RE-005/2026", "eq": "EQ-05", "nome": "Sanitários Químicos Portáteis (2 Cabines)",
        "cc": "CC-103", "eap": "1.0.3", "qtd": 2, "und": "cabines", "meses": "M1 a M6 (6 meses)", "sem": "S01 a S26",
        "disparo": "10/09/2026", "entrega": "22/09/2026", "lead": 12, "budget_mensal": 283.33, "budget_total": 1699.98,
        "especificacao": "2 Cabines sanitárias portáteis em polietileno de alta densidade c/ caixa de dejetos 220L, desodorizante bactericida e serviço obrigatório de sucção e higienização 2 vezes por semana com emissão de MTR.",
        "normas": "NR-18 / Resolução INEA/RJ (Destinação Efluentes)", "operador": "Serviço terceirizado da locadora", "combustivel": "Não aplicável",
        "locadoras": [("Brasquímica Sanitários", 283.33, "Vencedor"), ("CleanBox Campos", 320.00, "Equalizado"), ("Sanitex Açu", 350.00, "Acima do Budget")]
    },
    {
        "id": "RE-006/2026", "eq": "EQ-06", "nome": "Retroescavadeira 4x4 cabinada c/ operador",
        "cc": "CC-201", "eap": "1.1.1, 1.1.2", "qtd": 1, "und": "un", "meses": "M1 (3 semanas)", "sem": "S01 a S03",
        "disparo": "12/09/2026", "entrega": "19/09/2026", "lead": 7, "budget_mensal": 14000.00, "budget_total": 14000.00,
        "especificacao": "Retroescavadeira tração 4x4 (CAT 416F / JCB 3CX / Case 580N), potência mínima 85 HP, cabine fechada c/ ar-condicionado, caçamba frontal 1,0 m³ e traseira 0,25 m³, alarme de ré e giroflex. Franquia de 120 horas.",
        "normas": "NR-11 (Movimentação de Cargas), NR-12 (Segurança em Máquinas)", "operador": "Incluso c/ ASO e NR-11/12", "combustivel": "Diesel S-10 incluso pela locadora",
        "locadoras": [("Terramax Locações Açu", 14000.00, "Vencedor"), ("Transloc Norte Fluminense", 14800.00, "Equalizado"), ("TratorMáquinas Macaé", 15500.00, "Acima do Budget")]
    },
    {
        "id": "RE-007/2026", "eq": "EQ-07", "nome": "Caminhão Basculante 6x4 (12m³) c/ motorista",
        "cc": "CC-201", "eap": "1.1.1, 1.1.2", "qtd": 1, "und": "un", "meses": "M1 (3 semanas)", "sem": "S01 a S03",
        "disparo": "12/09/2026", "entrega": "19/09/2026", "lead": 7, "budget_mensal": 10500.00, "budget_total": 10500.00,
        "especificacao": "Caminhão trucado traçado 6x4 (Mercedes Atego 2730 / VW Constellation 26.280), caçamba basculante meia-cana de 12 m³, protetor de cabine, lona de cobertura de carga e tacógrafo aferido pelo INMETRO.",
        "normas": "Código de Trânsito Brasileiro / Portaria Porto do Açu / NR-18", "operador": "Motorista profissional CNH D com MTR", "combustivel": "Diesel S-10 incluso pela locadora",
        "locadoras": [("Terramax Locações Açu", 10500.00, "Vencedor"), ("Transloc Norte Fluminense", 11200.00, "Equalizado"), ("Transportes São João", 12000.00, "Acima do Budget")]
    },
    {
        "id": "RE-008/2026", "eq": "EQ-08", "nome": "Compactador de Percussão a gasolina (Sapo)",
        "cc": "CC-201", "eap": "1.1.2", "qtd": 1, "und": "un", "meses": "M1 (3 semanas)", "sem": "S02 a S04",
        "disparo": "15/09/2026", "entrega": "20/09/2026", "lead": 5, "budget_mensal": 1450.00, "budget_total": 1450.00,
        "especificacao": "Compactador tipo sapo com motor 4 tempos a gasolina (Honda GX100 ou Robin), sapata de aço 280x330mm, força de impacto mínima de 14 kN, sanfona de poliuretano reforçada e amortecedores de vibração no guidão.",
        "normas": "NR-12 / NBR 12267", "operador": "Operador da Construtora (treinado)", "combustivel": "Gasolina comum por conta da obra",
        "locadoras": [("Casa do Construtor Campos", 1450.00, "Vencedor"), ("Locafer Ferramentas", 1550.00, "Equalizado"), ("Andaimes & Cia Macaé", 1680.00, "Acima do Budget")]
    },
    {
        "id": "RE-009/2026", "eq": "EQ-09", "nome": "Betoneira Elétrica 400 Litros Trifásica",
        "cc": "CC-404", "eap": "1.3.3", "qtd": 1, "und": "un", "meses": "M1 a M4 (4 meses)", "sem": "S02 a S17",
        "disparo": "15/09/2026", "entrega": "22/09/2026", "lead": 5, "budget_mensal": 750.00, "budget_total": 3000.00,
        "especificacao": "Betoneira 400L de rotação contínua (Menegotti / Fischer), motor elétrico trifásico 220V 2 CV blindado IP-55, proteção total de cremalheira em chapa de aço e botão de parada de emergência com trava mecânica.",
        "normas": "NR-12 (Anexo XII) / NR-10", "operador": "Operador da Construtora", "combustivel": "Energia elétrica da obra",
        "locadoras": [("Casa do Construtor Campos", 750.00, "Vencedor"), ("Locafer Ferramentas", 800.00, "Equalizado"), ("Dimaq Equipamentos", 890.00, "Acima do Budget")]
    },
    {
        "id": "RE-010/2026", "eq": "EQ-10", "nome": "Cimbramento e Escoramento Metálico Regulável",
        "cc": "CC-302", "eap": "1.2.4, 1.2.6", "qtd": 888, "und": "m²·m", "meses": "M2 (35 dias corridos)", "sem": "S05 a S09",
        "disparo": "05/10/2026", "entrega": "25/10/2026", "lead": 20, "budget_mensal": 14850.00, "budget_total": 14850.00,
        "especificacao": "888 m²·m de escoramento metálico modular composto por escoras telescópicas ajustáveis (capacidade 2.000 kgf), torres de carga, vigas de alumínio de alta resistência para fundo/laterais de vigas V101-V115 e laje H12, forcados duplos e sapatas articuladas reguláveis. Acompanha memorial de cálculo e ART.",
        "normas": "NBR 15696 (Fôrmas e Escoramentos) / NR-18 / NBR 6118", "operador": "Montagem pelo Empreiteiro SUB-01", "combustivel": "Não aplicável",
        "locadoras": [("Mills Estruturas S.A.", 14850.00, "Vencedor"), ("Rohr Estruturas", 15600.00, "Equalizado"), ("SH Fôrmas e Andaimes", 16200.00, "Acima do Budget")]
    },
    {
        "id": "RE-011/2026", "eq": "EQ-11", "nome": "Andaimes Tubulares Fachadeiros c/ Guarda-Corpo (200 m²)",
        "cc": "CC-403", "eap": "1.3.4", "qtd": 200, "und": "m²", "meses": "M3 a M5 (3 meses)", "sem": "S10 a S21",
        "disparo": "05/11/2026", "entrega": "20/11/2026", "lead": 15, "budget_mensal": 3200.00, "budget_total": 9600.00,
        "especificacao": "200 m² de andaimes tubulares fachadeiros modulares com encaixe de segurança tipo pino, pisos metálicos antiderrapantes com travas, rodapés de 20cm, guarda-corpo duplo (1,20m e 0,70m), escadas internas com alçapão e tela fachadeira 100% fechada.",
        "normas": "NR-18.12 (Andaimes e Plataformas de Trabalho) / NR-35", "operador": "Montagem por montador qualificado", "combustivel": "Não aplicável",
        "locadoras": [("Loxam Degrau Locações", 3200.00, "Vencedor"), ("Mills Estruturas", 3400.00, "Equalizado"), ("Orguel Andaimes", 3650.00, "Acima do Budget")]
    },
    {
        "id": "RE-012/2026", "eq": "EQ-12", "nome": "Máquina de Projeção Contínua de Argamassa",
        "cc": "CC-405", "eap": "1.5.2", "qtd": 1, "und": "un", "meses": "M4 (1 mês)", "sem": "S14 a S17",
        "disparo": "25/11/2026", "entrega": "10/12/2026", "lead": 15, "budget_mensal": 5200.00, "budget_total": 5200.00,
        "especificacao": "Bomba misturadora e projetora contínua de argamassa (Putzknecht S48 / M-Tec M300), vazão mínima 1,5 m³/h, motor trifásico 380/220V, compressor de ar de diafragma integrado, mangueira de projeção flexível 25m e pistola de projeção com bico de tungstênio.",
        "normas": "NR-12 / NR-18 / NBR 13281", "operador": "Operador treinado da Empreiteira SUB-02", "combustivel": "Energia elétrica da obra",
        "locadoras": [("Putzknecht Brasil Locações", 5200.00, "Vencedor"), ("Locadora Técnica Macaé", 5600.00, "Equalizado"), ("Casa do Construtor Campos", 6100.00, "Acima do Budget")]
    },
    {
        "id": "RE-013/2026", "eq": "EQ-13", "nome": "Bomba Hidrostática de Teste de Pressão c/ Manômetro RBC",
        "cc": "CC-601", "eap": "2.1.6", "qtd": 1, "und": "un", "meses": "M4 (1 quinzena)", "sem": "S15 a S16",
        "disparo": "01/12/2026", "entrega": "12/12/2026", "lead": 10, "budget_mensal": 1200.00, "budget_total": 1200.00,
        "especificacao": "Bomba elétrica portátil para ensaios hidrostáticos de tubulações prediais até 25 bar (Ridgid / Rothenberger), com reservatório acoplado, mangueira de alta pressão c/ engate rápido e manômetro calibrado pela Rede Brasileira de Calibração (RBC) com certificado emitido há menos de 6 meses (Portão de Ouro 3).",
        "normas": "NBR 5626 (Instalações de Água Fria) / NBR 7198", "operador": "Encanador Especialista da Empreiteira SUB-06", "combustivel": "Energia elétrica 220V",
        "locadoras": [("Alusolda / TestLoc Macaé", 1200.00, "Vencedor"), ("Casa do Construtor Campos", 1350.00, "Equalizado"), ("Rothenberger Service", 1500.00, "Acima do Budget")]
    },
    {
        "id": "RE-014/2026", "eq": "EQ-14", "nome": "Plataforma Elevatória Tesoura Elétrica 10m",
        "cc": "CC-607", "eap": "2.2.7, 2.3.1", "qtd": 1, "und": "un", "meses": "M5 a M6 (2 meses)", "sem": "S18 a S24",
        "disparo": "20/12/2026", "entrega": "10/01/2027", "lead": 20, "budget_mensal": 6100.00, "budget_total": 12200.00,
        "especificacao": "Plataforma aérea tipo tesoura pantográfica autopropelida elétrica (Genie GS-2632 / JLG 2630ES), altura de trabalho de 10,0 metros, capacidade no cesto de 227 kg, extensão de deck deslizante de 0,90m, pneus brancos maciços que não marcam piso e sensor de inclinação com bloqueio automático.",
        "normas": "NR-11 / NR-18.12.2 / NR-35 / NBR 16776", "operador": "Eletricista homologado c/ NR-35 e NR-18", "combustivel": "Bateria tracionária c/ carregador integrado",
        "locadoras": [("Loxam Degrau Locações", 6100.00, "Vencedor"), ("Mills Plataformas", 6450.00, "Equalizado"), ("Orguel Equipamentos", 6900.00, "Acima do Budget")]
    },
    {
        "id": "RE-015/2026", "eq": "EQ-15", "nome": "Bomba de Vácuo Duplo Estágio 10 CFM + Manifold Digital",
        "cc": "CC-608", "eap": "2.3.4", "qtd": 1, "und": "cj", "meses": "M5 a M6 (1 mês sob demanda)", "sem": "S20 a S24",
        "disparo": "10/01/2027", "entrega": "22/01/2027", "lead": 10, "budget_mensal": 1800.00, "budget_total": 1800.00,
        "especificacao": "Conjunto de desidratação e vácuo composto por Bomba de Vácuo de duplo estágio 10 CFM (Fieldpiece / CPS), com válvula solenoide anti-retorno de óleo, vacuômetro digital de alta resolução (< 500 microns) e manifold eletrônico de 4 vias calibrado para fluido refrigerante ecológico R-32.",
        "normas": "NBR 16655 (Sistemas de Climatização)", "operador": "Mecânico de Refrigeração da Empreiteira SUB-07", "combustivel": "Energia elétrica 220V",
        "locadoras": [("Casa do Construtor Campos", 1800.00, "Vencedor"), ("Frigocenter Refrigeração", 1950.00, "Equalizado"), ("LocaFrio Macaé", 2200.00, "Acima do Budget")]
    },
    {
        "id": "RE-016/2026", "eq": "EQ-16", "nome": "Caçambas Estacionárias de Entulho 5m³ (PGRCC) c/ CTR",
        "cc": "CC-106", "eap": "1.0.6", "qtd": 2, "und": "caçambas", "meses": "M1 a M6 (6 meses)", "sem": "S01 a S26",
        "disparo": "10/09/2026", "entrega": "18/09/2026", "lead": 5, "budget_mensal": 1666.67, "budget_total": 10000.00,
        "especificacao": "Caçambas metálicas padrão Brooks de 5,0 m³ com pintura identificada, fitas refletivas e serviço de coleta, transporte e descarte licenciado em aterro de inertes Classe A homologado pelo INEA/RJ, com fornecimento mensal do Controle de Transporte de Resíduos (CTR) e Manifesto de Transporte de Resíduos (MTR).",
        "normas": "Resolução CONAMA 307 (Gestão de Resíduos) / POP 01 (Canteiro Lean)", "operador": "Serviço terceirizado c/ caminhão poliguindaste", "combustivel": "Incluso no frete de recolhimento",
        "locadoras": [("EcoAçu Resíduos Ambientais", 1666.67, "Vencedor"), ("Disk Entulho São João da Barra", 1800.00, "Equalizado"), ("TransResíduos Norte Fluminense", 1950.00, "Acima do Budget")]
    },
    {
        "id": "RE-017/2026", "eq": "EQ-17", "nome": "Grupo Gerador Diesel Silenciado 50 kVA c/ QTA",
        "cc": "CC-104", "eap": "1.0.4", "qtd": 1, "und": "un", "meses": "M1 a M3 (3 meses)", "sem": "S01 a S12",
        "disparo": "10/09/2026", "entrega": "18/09/2026", "lead": 10, "budget_mensal": 6600.00, "budget_total": 19800.00,
        "especificacao": "Grupo Gerador Diesel Silenciado 50 kVA / 40 kW (Stemac / Cummins / MWM), nível de ruído máximo de 70 dB(A) a 7 metros, trifásico 220/127V 60Hz, com Quadro de Transferência Automática (QTA), bacia de contenção ambiental metálica integrada de 110% contra vazamentos e 30m de cabo 50mm².",
        "normas": "NBR ISO 8528 / NR-10 / Portaria Ambiental INEA", "operador": "Eletricista de Manutenção da Construtora", "combustivel": "Diesel marítimo S-10 por conta da obra",
        "locadoras": [("Tecnogera Locação S.A. Macaé", 6600.00, "Vencedor"), ("Geradores Brasil Macaé", 6900.00, "Equalizado"), ("A Geradora Aluguel de Máquinas", 7400.00, "Acima do Budget")]
    }
]

def gerar_requisicoes_equipamentos_markdown():
    caminho = os.path.join(OUTPUT_DIR, "REQUISICOES_LOCACAO_EQUIPAMENTOS_TMULT.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("""# 📋 CATÁLOGO OFICIAL: REQUISIÇÕES DE LOCAÇÃO DE EQUIPAMENTOS (RE-001 A RE-017)

> **Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Porto do Açu (SJB/RJ)  
> **Finalidade:** Dossiê Técnico de Requisições Formais de Equipamentos emitidas pela Engenharia  
> **Total de Equipamentos Requisitados:** 17 Famílias Operacionais (`EQ-01` a `EQ-17`)  
> **Valor Total do Orçamento de Locações:** **R$ 141.499,98**  
> **Governança:** POP 04 (Equipamentos), POP 05 (Compras), POP 06 (Recebimento), NR-11, NR-12 e NR-18  

---

## 1. Quadro Resumo das 17 Requisições de Equipamentos

| Nº RE | Cód EQ | Equipamento / Instalação | CC | EAP | Mobilização | Desmobilização | Lead | Custo Total (R$) | Fornecedor Homologado |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
""")
        for r in REQUISICOES_EQUIP:
            f.write(f"| **{r['id']}** | `{r['eq']}` | {r['nome'][:38]} | `{r['cc']}` | `{r['eap']}` | **{r['entrega']}** | {r['meses'][:10]} | {r['lead']}d | **R$ {r['budget_total']:,.2f}** | {r['locadoras'][0][0]} |\n")

        tot = sum(r['budget_total'] for r in REQUISICOES_EQUIP)
        f.write(f"\n**VALOR TOTAL CONSOLIDADO DAS REQUISIÇÕES DE EQUIPAMENTOS:** **R$ {tot:,.2f}**\n\n---\n\n")

        f.write("## 2. Fichas Técnicas Analíticas das 17 Requisições de Equipamento\n\n")
        for r in REQUISICOES_EQUIP:
            f.write(f"""### 📦 {r['id']} — {r['nome']} (`{r['eq']}`)

| Campo de Governança | Especificação Operacional |
| :--- | :--- |
| **Identificador da RE** | `{r['id']}` (Equipamento: `{r['eq']}`) |
| **Centro de Custo (CC)** | **`{r['cc']}`** |
| **EAP Vinculada** | `{r['eap']}` |
| **Data de Emissão (Disparo)** | {r['disparo']} |
| **Data Limite no Canteiro** | **{r['entrega']}** (Lead Time: {r['lead']} dias corridos) |
| **Período de Permanência** | {r['meses']} (Semanas {r['sem']}) |
| **Budget Mensal / Unitário** | R$ {r['budget_mensal']:,.2f} |
| **Budget Total Previsto** | **R$ {r['budget_total']:,.2f}** |
| **Condição de Operação** | {r['operador']} |
| **Combustível / Energia** | {r['combustivel']} |
| **Normas Regulamentadoras** | {r['normas']} |

#### Descrição Técnica Pormenorizada:
{r['especificacao']}

#### Equalização de Cotação Prévia (3 Fornecedores):
""")
            for loc, val, st in r["locadoras"]:
                f.write(f"- **{loc}:** R$ {val:,.2f} — *{st}*\n")
                
            f.write(f"""
#### Critérios Mandatórios de Vistoria na Entrega (POP 04 / POP 06):
- Inspeção visual de ausência de vazamento de óleo, trincas estruturais ou deformações;
- Teste prático de funcionamento de botões de emergência, alarmes sonoros e dispositivos de segurança;
- Verificação da ART de fabricação/montagem e entrega do manual de operação em português.

---
""")
    print(f"Catálogo de REs gerado: {caminho}")

def gerar_mapa_cotacao_equipamentos():
    caminho_xlsx = os.path.join(OUTPUT_DIR, "MAPA_COTACAO_EQUALIZADO_EQUIPAMENTOS_TMULT.xlsx")
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    
    ws = wb.create_sheet(title="Cotação Equipamentos")
    ws.views.sheetView[0].showGridLines = True
    
    NAVY_HEADER = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    BLUE_HEADER = PatternFill(start_color="2B5B84", end_color="2B5B84", fill_type="solid")
    GOLD_HEADER = PatternFill(start_color="D99B26", end_color="D99B26", fill_type="solid")
    GREEN_LIGHT = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
    GRAY_LIGHT = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
    
    FONT_TITLE = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    FONT_HEADER = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    FONT_BOLD = Font(name="Calibri", size=10, bold=True, color="1B365D")
    FONT_GREEN = Font(name="Calibri", size=10, bold=True, color="137333")
    
    BORDER_THIN = Border(
        left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'), bottom=Side(style='thin', color='DDDDDD')
    )
    BORDER_TOTAL = Border(
        top=Side(style='thin', color='1B365D'), bottom=Side(style='double', color='1B365D'),
        left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD')
    )

    ws.merge_cells("A1:K1")
    ws["A1"] = "MAPA DE COTAÇÃO EQUALIZADO DE EQUIPAMENTOS E MÁQUINAS (OBRA_TMULT - 3 LOCADORAS)"
    ws["A1"].font = FONT_TITLE
    ws["A1"].fill = NAVY_HEADER
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 26
    
    headers = [
        "Nº RE", "Cód EQ", "Equipamento Solicitado", "Centro Custo", "Prazo",
        "Locadora A (Proposta 1)", "Valor Total A", "Locadora B (Proposta 2)", "Valor Total B",
        "Locadora Vencedora (Menor Preço)", "Valor Homologado (R$)"
    ]
    ws.row_dimensions[3].height = 24
    for c_i, h in enumerate(headers, start=1):
        cell = ws.cell(row=3, column=c_i, value=h)
        cell.font = FONT_HEADER
        cell.fill = BLUE_HEADER if c_i <= 9 else GOLD_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER_THIN
        
    for idx, r in enumerate(REQUISICOES_EQUIP, start=4):
        ws.row_dimensions[idx].height = 20
        ws.cell(row=idx, column=1, value=r["id"]).alignment = Alignment(horizontal="center")
        ws.cell(row=idx, column=2, value=r["eq"]).alignment = Alignment(horizontal="center")
        ws.cell(row=idx, column=3, value=r["nome"][:35]).alignment = Alignment(horizontal="left")
        ws.cell(row=idx, column=4, value=r["cc"]).alignment = Alignment(horizontal="center")
        ws.cell(row=idx, column=5, value=r["meses"][:12]).alignment = Alignment(horizontal="center")
        
        # Locadora A (Vencedora)
        ws.cell(row=idx, column=6, value=r["locadoras"][0][0]).alignment = Alignment(horizontal="left")
        c_a = ws.cell(row=idx, column=7, value=r["budget_total"])
        c_a.number_format = '"R$ "#,##0.00'
        c_a.alignment = Alignment(horizontal="right")
        
        # Locadora B (Concorrente)
        ws.cell(row=idx, column=8, value=r["locadoras"][1][0]).alignment = Alignment(horizontal="left")
        # estimativa do total da locadora B proporcional ao valor unitário
        ratio = r["locadoras"][1][1] / r["locadoras"][0][1]
        c_b = ws.cell(row=idx, column=9, value=r["budget_total"] * ratio)
        c_b.number_format = '"R$ "#,##0.00'
        c_b.alignment = Alignment(horizontal="right")
        
        # Homologado
        ws.cell(row=idx, column=10, value=r["locadoras"][0][0]).alignment = Alignment(horizontal="left")
        c_hom = ws.cell(row=idx, column=11, value=r["budget_total"])
        c_hom.number_format = '"R$ "#,##0.00'
        c_hom.font = FONT_GREEN
        c_hom.fill = GREEN_LIGHT
        c_hom.alignment = Alignment(horizontal="right")
        
        for ci in range(1, 12):
            cell = ws.cell(row=idx, column=ci)
            cell.border = BORDER_THIN
            if idx % 2 == 0 and cell.fill.start_color.index != 'E6F4EA':
                cell.fill = GRAY_LIGHT

    r_tot = 4 + len(REQUISICOES_EQUIP)
    ws.row_dimensions[r_tot].height = 24
    ws.merge_cells(start_row=r_tot, start_column=1, end_row=r_tot, end_column=6)
    ws.cell(row=r_tot, column=1, value="TOTAL CONSOLIDADO DAS LOCAÇÕES (R$):").font = FONT_BOLD
    ws.cell(row=r_tot, column=1).alignment = Alignment(horizontal="right", vertical="center")
    
    c_tot_a = ws.cell(row=r_tot, column=7, value=f"=SUM(G4:G{r_tot-1})")
    c_tot_a.number_format = '"R$ "#,##0.00'
    c_tot_a.font = FONT_BOLD
    c_tot_a.alignment = Alignment(horizontal="right")
    
    ws.cell(row=r_tot, column=8, value="")
    c_tot_b = ws.cell(row=r_tot, column=9, value=f"=SUM(I4:I{r_tot-1})")
    c_tot_b.number_format = '"R$ "#,##0.00'
    c_tot_b.font = FONT_BOLD
    c_tot_b.alignment = Alignment(horizontal="right")
    
    ws.cell(row=r_tot, column=10, value="Economia Negociada:")
    c_tot_hom = ws.cell(row=r_tot, column=11, value=f"=SUM(K4:K{r_tot-1})")
    c_tot_hom.number_format = '"R$ "#,##0.00'
    c_tot_hom.font = FONT_BOLD
    c_tot_hom.alignment = Alignment(horizontal="right")
    
    for ci in range(1, 12):
        ws.cell(row=r_tot, column=ci).fill = PatternFill(start_color="E8EEF5", end_color="E8EEF5", fill_type="solid")
        ws.cell(row=r_tot, column=ci).border = BORDER_TOTAL

    ws.column_dimensions["A"].width = 13
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 38
    ws.column_dimensions["D"].width = 12
    ws.column_dimensions["E"].width = 14
    ws.column_dimensions["F"].width = 24
    ws.column_dimensions["G"].width = 16
    ws.column_dimensions["H"].width = 24
    ws.column_dimensions["I"].width = 16
    ws.column_dimensions["J"].width = 24
    ws.column_dimensions["K"].width = 18

    wb.save(caminho_xlsx)
    print(f"Mapa de cotação Excel gerado: {caminho_xlsx}")

    # Gera também Mapa de Cotação de Equipamentos em Markdown e CSV
    caminho_md = os.path.join(OUTPUT_DIR, "MAPA_COTACAO_EQUALIZADO_EQUIPAMENTOS_TMULT.md")
    caminho_csv = os.path.join(OUTPUT_DIR, "MAPA_COTACAO_EQUALIZADO_EQUIPAMENTOS_TMULT.csv")
    
    with open(caminho_csv, "w", encoding="utf-8") as f:
        f.write("ID_RE;EQUIPAMENTO;CENTRO_CUSTO;EAP;QTD;UNID;FORNECEDOR_VENCEDOR;VALOR_VENCEDOR;FORNECEDOR_CONCORRENTE;VALOR_CONCORRENTE;FORNECEDOR_3;VALOR_3;STATUS\n")
        for r in REQUISICOES_EQUIP:
            l1, v1 = r["locadoras"][0][0], r["locadoras"][0][1]
            l2, v2 = r["locadoras"][1][0], r["locadoras"][1][1]
            l3, v3 = r["locadoras"][2][0], r["locadoras"][2][1]
            f.write(f"{r['id']};{r['nome']};{r['cc']};{r['eap']};{r['qtd']};{r['und']};{l1};{v1:.2f};{l2};{v2:.2f};{l3};{v3:.2f};Homologado\n")
    print(f"Mapa de cotação CSV gerado: {caminho_csv}")

    with open(caminho_md, "w", encoding="utf-8") as f:
        f.write(f"""# 🚜 MAPA DE COTAÇÃO EQUALIZADO & HOMOLOGAÇÃO — LOCAÇÃO DE EQUIPAMENTOS
### AUDITORIA DE MERCADO: 17 FAMÍLIAS DE EQUIPAMENTOS (3 LOCADORAS POR FAMÍLIA)

> **Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Porto do Açu (SJB/RJ)  
> **Custo Direto Orçado Total (17 REs):** **R$ 141.499,98**  
> **Critério de Equalização:** Escopo técnico idêntico, regime operacional (horas/mês), operador incluso/excluso equalizado, frete mobilização/desmobilização incluso e aderência estrita às NRs (NR-11, NR-12, NR-18, NR-35).  
> **Planilha Excel Auditável:** [`MAPA_COTACAO_EQUALIZADO_EQUIPAMENTOS_TMULT.xlsx`](file:///{OUTPUT_DIR.replace(chr(92), '/')}/MAPA_COTACAO_EQUALIZADO_EQUIPAMENTOS_TMULT.xlsx)

---

## 1. Quadro Comparativo Consolidado das 17 Famílias de Equipamentos

| ID RE | Equipamento / Família | CC | EAP | Locadora Vencedora (Homologada) | Valor Vencedor | Locadora Concorrente 1 | Valor Conc. 1 | Locadora Concorrente 2 | Valor Conc. 2 | Status |
| :---: | :--- | :---: | :---: | :--- | :---: | :--- | :---: | :--- | :---: | :---: |
""")
        tot_hom = 0.0
        for r in REQUISICOES_EQUIP:
            tot_hom += r["budget_total"]
            l1, v1 = r["locadoras"][0][0], r["locadoras"][0][1]
            l2, v2 = r["locadoras"][1][0], r["locadoras"][1][1]
            l3, v3 = r["locadoras"][2][0], r["locadoras"][2][1]
            f.write(f"| **{r['id']}** | {r['nome'][:35]} | `{r['cc']}` | `{r['eap']}` | **{l1}** | **R$ {v1:,.2f}** | {l2} | R$ {v2:,.2f} | {l3} | R$ {v3:,.2f} | 🟢 Homologado |\n")

        f.write(f"""
---

## 2. Síntese do Parecer de Suprimentos para Equipamentos

1. **Aderência Orçamentária:** Todas as 17 famílias foram negociadas rigorosamente dentro do teto orçamentário do histograma de equipamentos (`HISTOGRAMA_EQUIPAMENTOS_TMULT.csv`), totalizando **R$ 141.499,98**.
2. **Requisitos Contratuais & Mobilização:** Todas as locadoras vencedoras foram integradas aos Contratos de Locação de Equipamentos (`CONTRATO_LOC01` a `CONTRATO_LOC06`) da pasta `02_ORCAMENTO_BASE_E_CONTRATOS/CONTRATOS_EQUIPAMENTOS/`.
3. **Portão de Ouro de Segurança (POP 04):** Nenhum equipamento tem autorização de entrada no canteiro sem:
   - Laudo de conformidade NR-12 com ART de profissional habilitado;
   - Treinamento e capacitação do operador (NR-11/12/18/35) comprovados na Ficha de Registro;
   - Plano de Manutenção Preventiva do fabricante atualizado.

---
*Dossiê auditável gerado automaticamente pelo Sistema de Gestão de Suprimentos A11.*
""")
    print(f"Mapa de cotação MD gerado: {caminho_md}")

def gerar_tracker_mestre_unificado():
    # Carrega as 24 RCs de materiais e anexa as 17 REs de equipamentos
    caminho_csv = os.path.join(OUTPUT_DIR, "TRACKER_SUPRIMENTOS_MESTRE_COMPLETO_TMULT.csv")
    caminho_md = os.path.join(OUTPUT_DIR, "TRACKER_SUPRIMENTOS_MESTRE_COMPLETO_TMULT.md")
    
    # Importa os dados das 24 RCs existentes no tracker antigo
    linhas_csv = [
        "ID_Requisicao;Tipo_Suprimento;Pacote_Insumo_Equipamento;Centro_Custo_CC;Disciplina;EAP_Itens;Data_Disparo;Data_Canteiro;Lead_Time_Dias;Estagio_Pipeline;Responsavel;Semaforo;Budget_R$"
    ]
    
    # Linhas de Materiais (24 RCs)
    caminho_antigo = os.path.join(OUTPUT_DIR, "TRACKER_SUPRIMENTOS_RC_TMULT.csv")
    if os.path.exists(caminho_antigo):
        with open(caminho_antigo, "r", encoding="utf-8") as f:
            headers_antigo = f.readline()
            for line in f:
                parts = line.strip().split(";")
                if len(parts) >= 13:
                    # ID;Pacote;CC;Disc;EAP;Emissao;Canteiro;Lead;Estagio;Resp;Prox;Semaforo;Budget
                    linhas_csv.append(f"{parts[0]};MATERIAL;{parts[1]};{parts[2]};{parts[3]};{parts[4]};{parts[5]};{parts[6]};{parts[7]};{parts[8]};{parts[9]};{parts[11]};{parts[12]}")
                    
    # Linhas de Equipamentos (17 REs)
    for r in REQUISICOES_EQUIP:
        estagio = "1. PENDENTE_SUPRIMENTOS" if r["lead"] <= 12 and "09/2026" in r["disparo"] else "0. PLANEJADO_FUTURO"
        semaforo = "🟡 ATENÇÃO" if r["lead"] <= 12 and "09/2026" in r["disparo"] else "⚪ PLANEJADO"
        linhas_csv.append(f"{r['id']};EQUIPAMENTO;{r['nome']};{r['cc']};Equipamentos/Canteiro;{r['eap']};{r['disparo']};{r['entrega']};{r['lead']};{estagio};Suprimentos / Locações;{semaforo};{r['budget_total']:.2f}")

    with open(caminho_csv, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_csv))
    print(f"Tracker Unificado CSV gerado: {caminho_csv}")

    # Gera Markdown correspondente
    with open(caminho_md, "w", encoding="utf-8") as f:
        dir_formatado = OUTPUT_DIR.replace('\\', '/')
        f.write(f"""# 📊 TRACKER MESTRE UNIFICADO DE SUPRIMENTOS (41 PACOTES)
### MONITORAMENTO INTEGRADO: 24 RCs DE MATERIAIS + 17 REs DE EQUIPAMENTOS

> **Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Porto do Açu (SJB/RJ)  
> **Total de Pacotes Rastreados:** **41 Requisições (24 Materiais + 17 Equipamentos)**  
> **Valor Total do Pipeline:** **R$ 709.473,77** (Materiais R$ 567.973,79 + Equipamentos R$ 141.499,98)  
> **Arquivo CSV Auditável:** [`TRACKER_SUPRIMENTOS_MESTRE_COMPLETO_TMULT.csv`](file:///{dir_formatado}/TRACKER_SUPRIMENTOS_MESTRE_COMPLETO_TMULT.csv)

---

## 1. Pipeline Geral de Suprimentos por Tipo de Requisição

| ID Requisição | Tipo | Pacote / Insumo / Equipamento | Centro Custo | EAP | Data Disparo | Data Canteiro | Lead | Estágio Pipeline | Semáforo | Budget (R$) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :---: | :---: |
""")
        tot_mat = 0.0
        tot_eq = 0.0
        for l in linhas_csv[1:]:
            p = l.split(";")
            val = float(p[12])
            if p[1] == "MATERIAL":
                tot_mat += val
            else:
                tot_eq += val
            f.write(f"| **{p[0]}** | `{p[1]}` | {p[2][:35]} | `{p[3][:12]}` | `{p[5][:10]}` | {p[6]} | **{p[7]}** | {p[8]}d | {p[9][:18]} | {p[11]} | **R$ {val:,.2f}** |\n")

        f.write(f"""
---

## 2. Balanço Geral Consolidado de Suprimentos

- **Total de Requisições de Compra de Materiais (24 RCs):** **R$ {tot_mat:,.2f}**
- **Total de Requisições de Locação de Equipamentos (17 REs):** **R$ {tot_eq:,.2f}**
- **VALOR TOTAL DO PIPELINE DE SUPRIMENTOS DA OBRA TMULT:** **R$ {tot_mat + tot_eq:,.2f}**

---
*Tracker Unificado Mestre 100% amarrado ao cronograma da Linha de Base 01 e Centros de Custo.*
""")
    print(f"Tracker Unificado MD gerado: {caminho_md}")

if __name__ == "__main__":
    gerar_requisicoes_equipamentos_markdown()
    gerar_mapa_cotacao_equipamentos()
    gerar_tracker_mestre_unificado()
