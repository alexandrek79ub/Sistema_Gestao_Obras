#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador dos Contratos de Locação de Equipamentos da OBRA_TMULT
Cria os 6 pacotes formais de locação de equipamentos (LOC-01 a LOC-06)
com minutas contratuais, SLAs de manutenção, requisitos NR-12/NR-18,
matriz de responsabilidades e planilha Excel de controle.
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
OUTPUT_DIR = os.path.join(BASE_DIR, "projetos", "OBRA_TMULT", "02_ORCAMENTO_BASE_E_CONTRATOS", "CONTRATOS_EQUIPAMENTOS")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# DADOS DOS 6 PACOTES DE LOCAÇÃO DE EQUIPAMENTOS
# -------------------------------------------------------------
PACOTES_LOCACAO = [
    {
        "cod": "LOC-01",
        "nome_arquivo": "CONTRATO_LOC01_MODULOS_HABITAVEIS_NR18.md",
        "titulo": "CONTRATO DE LOCAÇÃO DE MÓDULOS HABITÁVEIS CONTAINERS E SANITÁRIOS QUÍMICOS NR-18",
        "itens_equip": "EQ-01 (Escritório), EQ-02 (Vestiário), EQ-03 (Refeitório), EQ-04 (Almoxarifado) e EQ-05 (Sanitários Químicos)",
        "locador": "Rentcon Locações de Módulos Habitáveis Ltda / NHJ Brasil",
        "cnpj": "12.345.678/0001-90",
        "periodo": "22/09/2026 a 10/03/2027 (6 Meses / Semanas S01 a S26)",
        "cc": "CC-103 (Canteiro e Vivência NR-18)",
        "eap": "1.0.3",
        "valor_total": 38299.98,
        "valor_mensal": 6383.33,
        "escopo": [
            "1 Módulo Escritório 6,00x2,40m termoacústico c/ AC 12.000 BTU, janelas c/ grade, iluminação LED e mesa de reuniões",
            "1 Módulo Vestiário 6,00x2,40m com 4 chuveiros elétricos blindados, lavatórios, bancos e armários NR-18",
            "1 Módulo Refeitório 6,00x2,40m climatizado com mesas, bancos laváveis, pia de inox e bebedouro refrigerado",
            "1 Módulo Almoxarifado/Ferramentaria Dry 20 pés com prateleiras reforçadas e tranca tetra quádrupla",
            "2 Cabines de sanitários químicos portáteis em polietileno com 2 manutenções e sucções de efluentes semanais"
        ],
        "obrigacoes_locador": [
            "Transporte com caminhão munck e içamento seguro no canteiro da OBRA_TMULT no Porto do Açu em 22/09/2026",
            "ART de fabricação e laudo de habitabilidade elétrica e térmica conforme NR-18 e NR-10",
            "Manutenção e sucção sanitária semanal dos químicos com destinação licenciada pelo INEA/RJ",
            "Substituição imediata de ar-condicionado ou fiação em caso de defeito em até 24 horas úteis"
        ],
        "obrigacoes_locatario": [
            "Execução prévia dos apoios de concreto nivelados para assentamento dos containers",
            "Ponto de energia 220V trifásico e água potável no limite de 5 metros dos módulos",
            "Zelo e conservação das instalações elétricas, fechaduras e esquadrias durante o período de locação"
        ]
    },
    {
        "cod": "LOC-02",
        "nome_arquivo": "CONTRATO_LOC02_TERRAPLENAGEM_E_TRANSPORTE.md",
        "titulo": "CONTRATO DE LOCAÇÃO DE MAQUINÁRIO PESADO DE TERRAPLENAGEM COM OPERADOR E COMBUSTÍVEL",
        "itens_equip": "EQ-06 (Retroescavadeira 4x4) e EQ-07 (Caminhão Basculante 12m³ Traçado 6x4)",
        "locador": "Terramax Locações e Terraplenagem do Norte Fluminense Ltda",
        "cnpj": "23.456.789/0001-01",
        "periodo": "19/09/2026 a 08/10/2026 (3 Semanas / Semanas S01 a S03)",
        "cc": "CC-201 (Escavação e Movimento de Terra)",
        "eap": "1.1.1, 1.1.2",
        "valor_total": 24500.00,
        "valor_mensal": 24500.00,
        "escopo": [
            "1 Retroescavadeira 4x4 cabinada c/ caçamba frontal 1,0m³ e retro 0,25m³ c/ operador habilitado e qualificado",
            "1 Caminhão Basculante 6x4 traçado caçamba 12m³ com motorista habilitado e MTR para bota-fora de terra excedente",
            "Operação contínua de escavação mecânica de 32 cavas de sapatas e 140,44m de valas de baldrames",
            "Transporte de 180 m³ de material excedente para bota-fora licenciado no Complexo do Porto do Açu"
        ],
        "obrigacoes_locador": [
            "Fornecimento de operador e motorista com ASO, integração de segurança e treinamento NR-12/NR-18 válidos",
            "Máquinas com alarme sonoro de ré, cinto de segurança, extintor inspecionado e plano de manutenção preventiva",
            "Combustível diesel S-10, lubrificantes e manutenção mecânica por conta exclusiva da locadora",
            "Substituição de máquina defeituosa em no máximo 12 horas para não paralisar as fundações"
        ],
        "obrigacoes_locatario": [
            "Acompanhamento topográfico com marcação a laser e gabaritos de eixos pelo Engenheiro e Topógrafo",
            "Liberação do acesso de veículos pesados e segurança patrimonial na área portuária",
            "Emissão de CTR / MTR eletrônico para destinação de resíduos de escavação"
        ]
    },
    {
        "cod": "LOC-03",
        "nome_arquivo": "CONTRATO_LOC03_GRUPO_GERADOR_SILENCIADO.md",
        "titulo": "CONTRATO DE LOCAÇÃO DE GRUPO GERADOR DIESEL SILENCIADO 50 kVA AUTOMÁTICO",
        "itens_equip": "EQ-17 (Grupo Gerador Diesel Silenciado 50 kVA c/ Bacia de Contenção)",
        "locador": "Tecnogera Locação de Geradores e Energia Temporária S.A. / Macaé",
        "cnpj": "34.567.890/0001-12",
        "periodo": "18/09/2026 a 10/12/2026 (3 Meses / Semanas S01 a S12)",
        "cc": "CC-104 (Energia Temporária e Utilidades)",
        "eap": "1.0.4",
        "valor_total": 19800.00,
        "valor_mensal": 6600.00,
        "escopo": [
            "1 Grupo Gerador Diesel 50 kVA silenciado (nível de ruído < 70 dB a 7m), trifásico 220/127V 60Hz",
            "Quadro de Transferência Automática (QTA) com chave reversora e disjuntor de proteção geral",
            "Bacia de contenção ecológica em chapa metálica de 110% do volume do tanque contra vazamentos de óleo/diesel",
            "Cabo de força flexível 50mm² (3 fases + neutro + terra) com 30 metros de extensão"
        ],
        "obrigacoes_locador": [
            "Entrega, içamento e start-up elétrico no canteiro com teste de carga e emissão de ART",
            "Manutenção preventiva a cada 250 horas de operação (troca de filtros de óleo, ar, combustível e correias)",
            "Plantão técnico 24/7 com atendimento presencial em até 4 horas no Porto do Açu"
        ],
        "obrigacoes_locatario": [
            "Abastecimento com diesel marítimo S-10 limpo e filtrado",
            "Aterramento elétrico temporário do chassi e neutro com hastes cobreadas de 5/8\" e cabo 35mm²",
            "Operação diária conforme manual do fabricante e registro horímetro na planilha de RDO"
        ]
    },
    {
        "cod": "LOC-04",
        "nome_arquivo": "CONTRATO_LOC04_CIMBRAMENTO_E_ESCORAMENTO.md",
        "titulo": "CONTRATO DE LOCAÇÃO DE SISTEMA DE CIMBRAMENTO E ESCORAMENTO METÁLICO REGULÁVEL",
        "itens_equip": "EQ-10 (Sistema de Cimbramento Metálico e Torres para Vigas e Laje)",
        "locador": "Mills Estruturas e Serviços de Engenharia S.A.",
        "cnpj": "45.678.901/0001-23",
        "periodo": "25/10/2026 a 28/11/2026 (35 Dias Corridos / Semanas S05 a S09)",
        "cc": "CC-302 (Fôrmas e Escoramentos Estruturais)",
        "eap": "1.2.4, 1.2.6",
        "valor_total": 14850.00,
        "valor_mensal": 14850.00,
        "escopo": [
            "888 m²·m de escoras metálicas telescópicas ajustáveis (capacidade 2.000 kgf cada) com pinos de trava",
            "Vigas metálicas de alumínio de alta resistência para suporte dos painéis compensados das vigas V101-V115",
            "Forcados simples e duplos, cruzetas reguláveis e sapatas articuladas de nivelamento milimétrico",
            "Projeto de cimbramento estruturado com memorial de cálculo de cargas e ART recolhida por Engenheiro Mecânico/Civil"
        ],
        "obrigacoes_locador": [
            "Entrega de materiais 100% inspecionados, retos, sem corrosão e com roscas lubrificadas",
            "Projeto de modulação de escoras indicando espaçamentos máximos de 1,20m e contra-flechas de L/300",
            "Vistoria técnica presencial no canteiro antes da concretagem para liberação formal da montagem"
        ],
        "obrigacoes_locatario": [
            "Montagem rigorosamente conforme o projeto da Mills, respeitando prumos e travamentos diagonais",
            "Proteção das peças contra respingos diretos de concreto e proibição de soldas nas escoras",
            "Devolução com peças limpas e organizadas em pallets/feixes amarrados"
        ]
    },
    {
        "cod": "LOC-05",
        "nome_arquivo": "CONTRATO_LOC05_ANDAIMES_E_PLATAFORMA_ELEVATORIA.md",
        "titulo": "CONTRATO DE LOCAÇÃO DE ANDAIMES FACHADEIROS NR-18 E PLATAFORMA TESOURA ELÉTRICA 10M",
        "itens_equip": "EQ-11 (200m² Andaimes Fachadeiros Tubulares) e EQ-14 (Plataforma Elevatória Tesoura Elétrica)",
        "locador": "Loxam Degrau Locação de Equipamentos e Plataformas S.A.",
        "cnpj": "56.789.012/0001-34",
        "periodo": "20/11/2026 a 20/02/2027 (3 Meses / Semanas S10 a S24)",
        "cc": "CC-403 (Andaimes e Fachadas) e CC-607 (Elevação em Altura)",
        "eap": "1.3.4, 2.2.7, 2.3.1",
        "valor_total": 21800.00,
        "valor_mensal": 7266.67,
        "escopo": [
            "200 m² de andaime tubular fachadeiro com piso metálico antiderrapante, rodapés de 20cm e escadas internas c/ alçapão",
            "Guarda-corpo duplo (1,20m e 0,70m) e tela de proteção em polietileno fachadeira 100% fechada conforme NR-18",
            "1 Plataforma aérea tipo tesoura elétrica autopropelida (altura de trabalho 10 metros, capacidade 230 kg)",
            "Carregador de bateria inteligente bivolt integrado e pneus de borracha maciça que não marcam o porcelanato"
        ],
        "obrigacoes_locador": [
            "Equipamentos em conformidade integral com NR-18 e NR-35, acompanhados de laudos e ART",
            "Treinamento de operação da plataforma elevatória para 2 colaboradores da obra com certificado emitido",
            "Manutenção preventiva mensal das baterias, sensores de inclinação e freios eletromagnéticos"
        ],
        "obrigacoes_locatario": [
            "Utilização exclusiva por operadores treinados e portando cinto tipo paraquedista com talabarte duplo",
            "Proibição de operar a plataforma em rampas superiores a 25% ou em solo desnivelado/lama",
            "Ancoragem dos andaimes fachadeiros na estrutura de concreto a cada 4 metros com parafusos parabolt"
        ]
    },
    {
        "cod": "LOC-06",
        "nome_arquivo": "CONTRATO_LOC06_EQUIPAMENTOS_ESPECIAIS_CANTEIRO.md",
        "titulo": "CONTRATO DE LOCAÇÃO DE EQUIPAMENTOS MECÂNICOS DE PRODUÇÃO, TESTES E CAÇAMBAS PGRCC",
        "itens_equip": "EQ-08 (Compactador Sapo), EQ-09 (Betoneira 400L), EQ-12 (Projetora Argamassa), EQ-13 (Bomba Teste), EQ-15 (Bomba Vácuo) e EQ-16 (Caçambas)",
        "locador": "Casa do Construtor Locação de Ferramentas / EcoAçu Resíduos Ltda",
        "cnpj": "67.890.123/0001-45",
        "periodo": "18/09/2026 a 25/02/2027 (Sob Demanda / Semanas S01 a S25)",
        "cc": "CC-106, CC-201, CC-404, CC-405, CC-601, CC-608",
        "eap": "1.0.6, 1.1.2, 1.3.3, 1.5.2, 2.1.6, 2.3.4",
        "valor_total": 22650.00,
        "valor_mensal": 4530.00,
        "escopo": [
            "1 Compactador de percussão a gasolina 4 tempos (força de impacto 14 kN) para cavas e reaterro",
            "1 Betoneira elétrica 400 litros trifásica com grade protetora de cremalheira e botão de parada de emergência",
            "1 Máquina de projeção contínua de argamassa de emboço (capacidade 1,5 m³/h) com mangueira de 25m",
            "1 Bomba de teste hidrostático manual/elétrica com manômetro com certificado de calibração RBC (Portão 3)",
            "1 Bomba de vácuo duplo estágio 10 CFM com vacuômetro digital de alta precisão (< 500 microns) para HVAC",
            "2 Caçambas estacionárias metálicas 5 m³ para entulho com troca e transporte licenciado com emissão de CTR"
        ],
        "obrigacoes_locador": [
            "Equipamentos revisados, limpos, com cabos e tomadas industriais blindadas padrão steck",
            "Manômetro de ensaio hidrostático com laudo do laboratório RBC emitido há menos de 6 meses",
            "Destinação legal do entulho em aterro Classe A no Norte Fluminense com comprovação documental mensal"
        ],
        "obrigacoes_locatario": [
            "Limpeza das máquinas ao final de cada jornada de trabalho (proibido acúmulo de argamassa seca)",
            "Segregação adequada do entulho nas caçambas, proibindo queima ou mistura com lixo contaminado Classe D",
            "Operação restrita a profissionais treinados e utilizando os EPIs mandatórios do POP 03"
        ]
    }
]

def gerar_contratos_markdown():
    # 1. ÍNDICE MESTRE
    indice_md = os.path.join(OUTPUT_DIR, "INDICE_MESTRE_CONTRATOS_LOCACAO_EQUIPAMENTOS.md")
    with open(indice_md, "w", encoding="utf-8") as f:
        f.write(f"""# 🚜 ÍNDICE MESTRE: CONTRATOS DE LOCAÇÃO DE EQUIPAMENTOS & MÁQUINAS

> **Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Porto do Açu (SJB/RJ)  
> **Volume de Locação:** 17 Famílias de Equipamentos em 6 Macro-Pacotes Contratuais  
> **Valor Total Consolidado das Locações:** **R$ 141.499,98**  
> **Governança:** POP 04 (Equipamentos), POP 06 (Recebimento), NR-12, NR-18 e NR-35  
> **Planilha de Gestão e Controle:** [`PLANILHA_GESTAO_LOCACAO_EQUIPAMENTOS.xlsx`](file:///{OUTPUT_DIR.replace(chr(92), '/')}/PLANILHA_GESTAO_LOCACAO_EQUIPAMENTOS.xlsx)

---

## 1. Quadro Geral de Contratos de Locação Pré-Criados

| Contrato | Objeto da Locação de Equipamentos | Famílias Atendidas | Fornecedor Homologado | Prazo / Vigência | Centro Custo | Valor Total (R$) |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: |
""")
        for p in PACOTES_LOCACAO:
            f.write(f"| **[{p['cod']}]({p['nome_arquivo']})** | {p['titulo'][:55]}... | `{p['itens_equip'][:30]}...` | {p['locador'].split('/')[0].strip()} | {p['periodo'][:22]} | `{p['cc'].split('(')[0].strip()}` | **R$ {p['valor_total']:,.2f}** |\n")
            
        tot = sum(p['valor_total'] for p in PACOTES_LOCACAO)
        f.write(f"\n**VALOR TOTAL CONSOLIDADO DE LOCAÇÃO DE MÁQUINAS E INSTALAÇÕES:** **R$ {tot:,.2f}**\n\n---\n\n")
        f.write("""## 2. Protocolo de Entrada e Segurança de Equipamentos no Canteiro (POP 04)

Antes de qualquer equipamento iniciar operação no canteiro da OBRA_TMULT no Porto do Açu, o Engenheiro Residente e o Técnico de Segurança do Trabalho (TST) devem exigir:

1. **Checklist de Conformidade NR-12 / NR-18:**
   - Botões de parada de emergência funcionais e acessíveis;
   - Proteção física rígida de correias, polias e cremalheiras;
   - Aterramento elétrico temporário do chassi ligado à malha de terra da obra;
   - Alarme sonoro e giroflex acionados automaticamente na ré para máquinas móveis.
2. **Documentação de Operadores Terceirizados (POP 17):**
   - Atestado de Saúde Ocupacional (ASO) apto para a função;
   - Certificado de treinamento de operador de máquinas pesadas / plataformas (NR-11, NR-12, NR-18 e NR-35);
   - Ficha de entrega de EPIs com CAs vigentes.
3. **ART de Responsabilidade Técnica:**
   - Obrigatória para o Cimbramento Metálico (`LOC-04`), Andaimes Fachadeiros (`LOC-05`), Instalações de Containers (`LOC-01`) e Grupo Gerador (`LOC-03`).

---

## 3. Matriz de Manutenção e Substituição Preventiva (SLA)

| Pacote | Manutenção Programada | Tempo Máximo de Atendimento (SLA) | Penalidade por Indisponibilidade |
| :--- | :--- | :---: | :--- |
| **LOC-01 Módulos** | Sucção e limpeza sanitária 2x por semana | Até 24 horas úteis | Glosa diária de 5% sobre a locação |
| **LOC-02 Terraplenagem** | Revisão diária de graxa e nível de óleo pelo operador | Até 12 horas úteis | Desconto das horas paralisadas + reposição de maquinário |
| **LOC-03 Gerador** | Troca de filtros e óleo a cada 250 horas | Até 4 horas (Plantão 24/7) | Multa por risco de paralisação de concretagem |
| **LOC-04 Cimbramento** | Vistoria técnica antes da concretagem | Até 24 horas antes do lançamento | Bloqueio do Portão de Qualidade da Laje |
| **LOC-05 Andaimes/Plat.** | Carga de baterias e verificação mensal | Até 24 horas úteis | Substituição imediata por plataforma reserva |
| **LOC-06 Produção** | Limpeza diária e aferição de manômetros | Até 12 horas úteis | Troca imediata da bomba de argamassa |
""")
    print(f"Índice gerado: {indice_md}")

    # 2. CONTRATOS INDIVIDUAIS
    for p in PACOTES_LOCACAO:
        caminho_c = os.path.join(OUTPUT_DIR, p["nome_arquivo"])
        with open(caminho_c, "w", encoding="utf-8") as f:
            f.write(f"""# 🚜 INSTRUMENTO PARTICULAR DE CONTRATO DE LOCAÇÃO DE EQUIPAMENTOS: {p['cod']}
### {p['titulo']}

> **Empreendimento:** Edifício Administrativo TMULT (368,40 m²) — Terminal Multiuso (Porto do Açu - SJB/RJ)  
> **Locatária:** CONSTRUTORA EXECUTIVA DO PORTO LTDA  
> **Locadora:** {p['locador']} | **CNPJ:** {p['cnpj']}  
> **Valor Total do Contrato:** R$ {p['valor_total']:,.2f} | **Centro de Custo:** {p['cc']}  
> **Prazo e Vigência:** {p['periodo']} | **EAP:** {p['eap']}  
> **Governança:** POP 04 (Equipamentos) / NR-12 / NR-18 / NR-35

---

## CLÁUSULA PRIMEIRA — DO OBJETO E EQUIPAMENTOS LOCADOS
1.1. O presente instrumento tem por objeto a locação das máquinas, equipamentos e instalações provisórias descritos abaixo, correspondentes ao pacote **{p['cod']}** da Linha de Base 01 da OBRA_TMULT:
""")
            for esc in p["escopo"]:
                f.write(f"- {esc};\n")
                
            f.write(f"""
1.2. Os equipamentos destinam-se exclusivamente ao atendimento das obras de construção civil do Edifício Administrativo do Terminal Multiuso no Porto do Açu, sendo vedada a sublocação ou desvio de finalidade sem anuência prévia da LOCATÁRIA.

## CLÁUSULA SEGUNDA — DOS VALORES E FORMA DE PAGAMENTO
2.1. Pela locação dos bens, a LOCATÁRIA pagará à LOCADORA o valor global de **R$ {p['valor_total']:,.2f}**, em parcelas mensais vinculadas ao relatório de medição e efetiva disponibilidade operacional no canteiro.
2.2. **Condição de Pagamento:** Faturamento em D+30 dias corridos após a medição quinzenal aprovada pelo Engenheiro Residente e apresentação da Nota Fiscal com o Centro de Custo `{p['cc'].split('(')[0].strip()}`.
2.3. Não incidirá pagamento sobre dias ou horas em que o equipamento permanecer paralisado por quebra mecânica, falta de operador da LOCADORA ou não conformidade técnica com as normas de segurança (NR-12 / NR-18).

## CLÁUSULA TERCEIRA — DOS PRAZOS DE MOBILIZAÇÃO E DESMOBILIZAÇÃO
3.1. O prazo de entrega e início da locação no canteiro é impreterivelmente **{p['periodo'].split('a')[0].strip()}**, sob pena de multa diária de 1% sobre o valor da locação.
3.2. A desmobilização ocorrerá em **{p['periodo'].split('a')[1].strip()}**, devendo a LOCATÁRIA comunicar com 5 dias úteis de antecedência para vistoria conjunta de encerramento.

## CLÁUSULA QUARTA — DAS OBRIGAÇÕES DA LOCADORA
""")
            for ob_l in p["obrigacoes_locador"]:
                f.write(f"- {ob_l};\n")
                
            f.write(f"""
## CLÁUSULA QUINTA — DAS OBRIGAÇÕES DA LOCATÁRIA
""")
            for ob_t in p["obrigacoes_locatario"]:
                f.write(f"- {ob_t};\n")
                
            f.write(f"""
## CLÁUSULA SEXTA — DA SEGURANÇA DO TRABALHO E PORTÃO DE ENTRADA (POP 04 / NR-18)
6.1. Todos os equipamentos deverão ser submetidos à vistoria de entrada no canteiro, com preenchimento da **Ficha de Inspeção de Equipamento (FIE)** pelo TST da obra.
6.2. Nenhum operador da LOCADORA poderá adentrar o Porto do Açu sem portar o crachá de identificação, ASO com aptidão específica, certificados NR-11/12/18 e EPIs obrigatórios com CA válido.

---

## ANEXO I: CHECKLIST DE RECEBIMENTO TÉCNICO E CONFORMIDADE (POP 04)

| Item Verificado | Critério Normativo | Status Admissão | Responsável Vistoria |
| :--- | :--- | :---: | :---: |
| **Pintura e Estrutura** | Ausência de corrosão acentuada, trincas ou deformações nas chapas | [ ] Aprovado | Almoxarife / Eng. Residente |
| **Proteções Móveis (NR-12)**| Carenagens fixas com parafusos e travas de segurança operacionais | [ ] Aprovado | TST da Obra |
| **Sistema Elétrico (NR-10)**| Cabos íntegros sem emendas, tomadas industriais steck e aterramento | [ ] Aprovado | Eletricista de Manutenção |
| **Dispositivos de Emergência**| Botão tipo cogumelo com retenção e rearme manual testado in-loco | [ ] Aprovado | TST da Obra |
| **ART / Laudo do Fabricante**| ART recolhida por Responsável Técnico habilitado e registrada no CREA | [ ] Aprovado | Engenheiro Fiscal |

---

*Contrato pré-criado e auditado conforme a Linha de Base 01 da OBRA_TMULT.*
""")
        print(f"Contrato gerado: {caminho_c}")

def gerar_planilha_gestao_locacoes():
    caminho = os.path.join(OUTPUT_DIR, "PLANILHA_GESTAO_LOCACAO_EQUIPAMENTOS.xlsx")
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    
    ws = wb.create_sheet(title="Controle de Locações")
    ws.views.sheetView[0].showGridLines = True
    
    NAVY_HEADER = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    BLUE_HEADER = PatternFill(start_color="2B5B84", end_color="2B5B84", fill_type="solid")
    GOLD_HEADER = PatternFill(start_color="D99B26", end_color="D99B26", fill_type="solid")
    GRAY_LIGHT = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
    BLUE_LIGHT = PatternFill(start_color="E8EEF5", end_color="E8EEF5", fill_type="solid")
    
    FONT_TITLE = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    FONT_HEADER = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    FONT_BOLD = Font(name="Calibri", size=10, bold=True, color="1B365D")
    FONT_REGULAR = Font(name="Calibri", size=10, color="333333")
    
    BORDER_THIN = Border(
        left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'), bottom=Side(style='thin', color='DDDDDD')
    )
    BORDER_TOTAL = Border(
        top=Side(style='thin', color='1B365D'), bottom=Side(style='double', color='1B365D'),
        left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD')
    )

    # Título
    ws.merge_cells("A1:K1")
    ws["A1"] = "PAINEL DE GESTÃO DE CONTRATOS DE LOCAÇÃO DE EQUIPAMENTOS (OBRA_TMULT - R$ 141.499,98)"
    ws["A1"].font = FONT_TITLE
    ws["A1"].fill = NAVY_HEADER
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 26
    
    headers = [
        "Contrato", "Objeto da Locação", "Equipamentos Atendidos", "Locador Homologado",
        "Centro Custo", "EAP", "Mobilização", "Desmobilização", "Prazo", "Valor Mensal (R$)", "Valor Total (R$)"
    ]
    ws.row_dimensions[3].height = 24
    for c_i, h in enumerate(headers, start=1):
        cell = ws.cell(row=3, column=c_i, value=h)
        cell.font = FONT_HEADER
        cell.fill = BLUE_HEADER if c_i <= 8 else GOLD_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER_THIN
        
    for idx, p in enumerate(PACOTES_LOCACAO, start=4):
        ws.row_dimensions[idx].height = 20
        ws.cell(row=idx, column=1, value=p["cod"]).alignment = Alignment(horizontal="center")
        ws.cell(row=idx, column=2, value=p["titulo"].replace("CONTRATO DE LOCAÇÃO DE ", "")[:40]).alignment = Alignment(horizontal="left")
        ws.cell(row=idx, column=3, value=p["itens_equip"][:35]).alignment = Alignment(horizontal="left")
        ws.cell(row=idx, column=4, value=p["locador"].split('/')[0].strip()).alignment = Alignment(horizontal="left")
        ws.cell(row=idx, column=5, value=p["cc"].split('(')[0].strip()).alignment = Alignment(horizontal="center")
        ws.cell(row=idx, column=6, value=p["eap"]).alignment = Alignment(horizontal="center")
        ws.cell(row=idx, column=7, value=p["periodo"].split('a')[0].strip().split('(')[0].strip()).alignment = Alignment(horizontal="center")
        ws.cell(row=idx, column=8, value=p["periodo"].split('a')[1].strip().split('(')[0].strip()).alignment = Alignment(horizontal="center")
        ws.cell(row=idx, column=9, value=p["periodo"].split('(')[1].split('/')[0].strip()).alignment = Alignment(horizontal="center")
        
        c_vm = ws.cell(row=idx, column=10, value=p["valor_mensal"])
        c_vm.number_format = '"R$ "#,##0.00'
        c_vm.alignment = Alignment(horizontal="right")
        
        c_vt = ws.cell(row=idx, column=11, value=p["valor_total"])
        c_vt.number_format = '"R$ "#,##0.00'
        c_vt.font = FONT_BOLD
        c_vt.alignment = Alignment(horizontal="right")
        
        for c_i in range(1, 12):
            cell = ws.cell(row=idx, column=c_i)
            cell.border = BORDER_THIN
            if idx % 2 == 0:
                cell.fill = GRAY_LIGHT

    # Linha Totalizadora
    r_tot = 4 + len(PACOTES_LOCACAO)
    ws.row_dimensions[r_tot].height = 24
    ws.merge_cells(start_row=r_tot, start_column=1, end_row=r_tot, end_column=9)
    ws.cell(row=r_tot, column=1, value="TOTAL CONSOLIDADO DE LOCAÇÃO DE EQUIPAMENTOS:").font = FONT_BOLD
    ws.cell(row=r_tot, column=1).alignment = Alignment(horizontal="right", vertical="center")
    
    c_tot_vm = ws.cell(row=r_tot, column=10, value=f"=SUM(J4:J{r_tot-1})")
    c_tot_vm.number_format = '"R$ "#,##0.00'
    c_tot_vm.font = FONT_BOLD
    c_tot_vm.alignment = Alignment(horizontal="right")
    
    c_tot_vt = ws.cell(row=r_tot, column=11, value=f"=SUM(K4:K{r_tot-1})")
    c_tot_vt.number_format = '"R$ "#,##0.00'
    c_tot_vt.font = FONT_BOLD
    c_tot_vt.alignment = Alignment(horizontal="right")
    
    for c_i in range(1, 12):
        cell = ws.cell(row=r_tot, column=c_i)
        cell.fill = BLUE_LIGHT
        cell.border = BORDER_TOTAL

    ws.column_dimensions["A"].width = 11
    ws.column_dimensions["B"].width = 38
    ws.column_dimensions["C"].width = 32
    ws.column_dimensions["D"].width = 28
    ws.column_dimensions["E"].width = 14
    ws.column_dimensions["F"].width = 12
    ws.column_dimensions["G"].width = 14
    ws.column_dimensions["H"].width = 14
    ws.column_dimensions["I"].width = 12
    ws.column_dimensions["J"].width = 18
    ws.column_dimensions["K"].width = 18

    wb.save(caminho)
    print(f"Planilha de Locações gerada: {caminho}")

if __name__ == "__main__":
    gerar_contratos_markdown()
    gerar_planilha_gestao_locacoes()
