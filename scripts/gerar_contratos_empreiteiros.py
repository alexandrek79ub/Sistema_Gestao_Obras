#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor Universal de Geração de Contratos Executivos com Empreiteiros.

Uso:
    python scripts/gerar_contratos_empreiteiros.py --obra OBRA_TMULT
    python scripts/gerar_contratos_empreiteiros.py --obra RESIDENCIAL_ALPHA
    python scripts/gerar_contratos_empreiteiros.py --dir projetos/OBRA_TMULT
"""

import os
import sys
import json
import argparse

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def parse_args():
    parser = argparse.ArgumentParser(description="Motor Universal de Contratos de Empreiteiros.")
    parser.add_argument("--obra", type=str, default="OBRA_TMULT", help="Nome da pasta da obra em projetos/")
    parser.add_argument("--dir", type=str, default=None, help="Caminho completo da pasta da obra")
    return parser.parse_args()

def fmt_moeda(val):
    if val is None:
        return "R$ 0,00"
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_num(val):
    if val is None:
        return "0,00"
    return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def gerar_contrato_individual(c, output_dir, titulo_obra, sigla, area_m2=368.4):
    caminho = os.path.join(output_dir, c["arquivo"])
    
    linhas = [
        f"# 📄 INSTRUMENTO PARTICULAR DE CONTRATO DE EMPREITADA CIVIL: {c['cod']}",
        f"### {c['titulo'].upper()}",
        "",
        f"> **Empreendimento:** {titulo_obra} ({area_m2:.2f} m²) — `{sigla}`  ",
        "> **Contratante:** CONSTRUTORA EXECUTIVA DO PORTO LTDA  ",
        "> **Contratada:** [NOME DA EMPRESA EMPREITEIRA HOMOLOGADA] | **CNPJ:** [__.__.___/____-__]  ",
        f"> **Valor Total do Contrato:** {fmt_moeda(c['valor_total'])} | **Centro de Custo:** {c['cc']}  ",
        f"> **Prazo Contratual:** {c['prazo']} | **Governança:** POP 17 / NR-18 / Skill Gestão 10",
        "",
        "---",
        "",
        "## CLÁUSULA PRIMEIRA — DO OBJETO",
        f"1.1. O presente contrato tem por objeto a execução, sob o regime de **Empreitada por Preço Unitário**, dos serviços de **{c['titulo']}**, correspondente ao pacote **{c['cod']}** da Linha de Base 01 da {sigla}.",
        f"1.2. O escopo compreende: {c['objeto']}, estritamente de acordo com as especificações técnicas, projetos executivos, cadernos de encargos e normas vigentes.",
        "",
        "## CLÁUSULA SEGUNDA — DO VALOR E DA FORMA DE PAGAMENTO",
        f"2.1. Pela execução dos serviços descritos no Anexo I, a CONTRATANTE pagará à CONTRATADA o valor global estimado de **{fmt_moeda(c['valor_total'])}** (preço fechado dos serviços listados).",
        "2.2. **Medição Quinzenal (Ciclos de 15 Dias):** As medições serão realizadas rigorosamente a cada 15 (quinze) dias corridos (1ª Quinzena: encerramento no dia 15; 2ª Quinzena: encerramento no último dia do mês), pelo Engenheiro Residente da CONTRATANTE mediante conferência física in-loco com trena/nível (Regra da Trena - POP 09), apurando o avanço real de serviços concluídos e aprovados. O pagamento será efetuado em D+5 dias úteis após a aprovação do Boletim de Medição Quinzenal (BMQ) e apresentação da Nota Fiscal com o Centro de Custo.",
        "2.3. **Retenção Técnica de Garantia (5%):** De todas as medições e faturamentos da CONTRATADA será retido o percentual de **5,0% (cinco por cento)** sobre o valor bruto da Nota Fiscal de Serviços.",
        "2.4. A devolução dos valores retidos ocorrerá após 90 (noventa) dias da entrega definitiva dos serviços do pacote, mediante apresentação do Termo de Recebimento Definitivo sem pendências e laudos técnicos comprobatórios.",
        "2.5. **Condição Sine Qua Non:** Nenhuma medição será liberada para pagamento se desacompanhada da respectiva **Ficha de Verificação de Serviço (FVS)** assinada sem não-conformidades em aberto.",
        "",
        "## CLÁUSULA TERCEIRA — DOS PRAZOS E CRONOGRAMA FÍSICO",
        f"3.1. O prazo total de vigência executiva é de **{c['prazo']}**, com início imediato após a emissão da Ordem de Serviço.",
        f"3.2. A CONTRATADA obriga-se a disponibilizar e manter no canteiro a equipe de pico de **{c['efetivo_pico']}**, sob pena de notificação e aplicação de multa por desmobilização imprevista.",
        "3.3. O não cumprimento das metas quinzenais do cronograma por culpa exclusiva da CONTRATADA sujeitará a aplicação de multa moratória de 0,5% por dia de atraso sobre o saldo contratual remanescente.",
        "",
        "## CLÁUSULA QUARTA — DA SEGURANÇA DO TRABALHO E SAÚDE (POP 17 / NR-18)",
        "4.1. NENHUM funcionário da CONTRATADA poderá adentrar o canteiro sem antes cumprir integralmente o **Portão de Segurança SST (POP 17)**:",
        "    a) Atestado de Saúde Ocupacional (ASO) apto para a função e para trabalho em altura (se aplicável);",
        "    b) Certificados válidos de treinamento de NR-18 e NR-35 assinados por instrutor habilitado;",
        "    c) Ficha de Entrega de EPIs com indicação do Certificado de Aprovação (CA) válido de cada item;",
        "    d) Registro em Carteira de Trabalho (CTPS) e comprovante de vínculo empregatício.",
        "4.2. O descumprimento de qualquer norma de segurança ensejará a paralisação imediata da frente de trabalho com paralisação do relógio de medição por conta exclusiva da CONTRATADA.",
        "",
        "---",
        "",
        "## ANEXO I: PLANILHA ORÇAMENTÁRIA ANALÍTICA DE SERVIÇOS",
        "",
        "| Item EAP | Descrição Pormenorizada do Serviço | Und | Qtd Contratada | Preço Unit. (R$) | Valor Total (R$) | Centro Custo |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: |"
    ]
    
    for it in c.get("itens_eap", []):
        pu_str = fmt_moeda(it.get('pu', 0.0))
        tot_str = fmt_moeda(it.get('tot', it.get('qtd', 0.0) * it.get('pu', 0.0)))
        qtd_str = fmt_num(it.get('qtd', 0.0))
        linhas.append(
            f"| `{it.get('eap', '')}` | {it.get('desc', '')} | {it.get('und', '')} | {qtd_str} | {pu_str} | **{tot_str}** | `{it.get('cc', '')}` |"
        )
        
    tot_contrato_str = fmt_moeda(c['valor_total'])
    linhas.extend([
        "",
        f"**VALOR TOTAL DO ANEXO I (REMUNERAÇÃO DA EMPREITADA):** **{tot_contrato_str}**",
        "",
        "---",
        "",
        "## ANEXO II: CADERNO DE ENCARGOS TÉCNICOS & SEQUÊNCIA CONSTRUTIVA",
        "",
        "A CONTRATADA deverá seguir rigorosamente a sequência executiva padronizada pelo PMO Virtual:",
        ""
    ])
    
    for seq in c.get("sequencia", []):
        linhas.append(f"- {seq}")
        
    linhas.extend([
        "",
        "---",
        "",
        "## ANEXO III: CRITÉRIOS DE MEDIÇÃO, ACEITAÇÃO E TOLERÂNCIAS NORMATIVAS",
        "",
        f"- **Normas Regulamentadoras e Técnicas Aplicáveis:** {c.get('normas', 'Normas ABNT e NR-18')};",
        f"- **Tolerâncias Máximas Admissíveis:** {c.get('tolerancias', 'Conforme NBR correspondente')};",
        f"- **Portão Bloqueante de Qualidade (FVS):** {c.get('fvs_bloqueante', 'FVS Aprovada')};",
        "- **Critério de Medição Física:** Toda medição exige conferência conjunta no local com trena/nível a laser entre o Mestre de Obras da Construtora e o Encarregado da Empreiteira;",
        "- **Critério de Glosa:** Serviços executados fora de prumo, nível, esquadro ou especificação serão demolidos e refeitos às custas exclusivas da CONTRATADA, com glosa imediata do valor correspondente.",
        "",
        "---",
        "",
        "## ANEXO IV: MATRIZ DE RESPONSABILIDADE DE FORNECIMENTO (RACI)",
        "",
        f"- **A CONTRATANTE (Construtora) Fornece Exclusivamente:** {c.get('fornecimento_construtora', 'Insumos principais e infraestrutura de canteiro')};",
        f"- **A CONTRATADA (Empreiteiro) Fornece Obrigatoriamente:** {c.get('fornecimento_empreiteiro', 'Ferramental e EPIs')}.",
        "",
        "---",
        "",
        f"{sigla}, _____ de _________________ de 2026.",
        "",
        "____________________________________________       ____________________________________________",
        "**Pela CONTRATANTE: Construtora Executiva**          **Pela CONTRATADA: Empreiteiro Responsável**",
        f"Nome: Eng. Residente ({sigla})                       Nome: Representante Legal",
        "CREA: ___________________                          CPF/CNPJ: __________________"
    ])
    
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"-> Contrato executivo gerado: {caminho}")

def gerar_indice_contratos(contratos, output_dir, titulo_obra, sigla, area_m2=368.4):
    caminho = os.path.join(output_dir, "INDICE_MESTRE_CONTRATOS_EMPREITEIROS.md")
    tot_val = sum(c.get("valor_total", 0.0) for c in contratos)
    
    linhas = [
        f"# 📑 CADERNO MESTRE DE CONTRATOS DE EMPREITEIROS ({len(contratos)} PACOTES)",
        "",
        f"> **Empreendimento:** {titulo_obra} ({area_m2:.2f} m²) — `{sigla}`  ",
        "> **Diretoria de Operações & Jurídico:** Minutas Padronizadas com Planilha, Sequência Construtiva e FVS  ",
        f"> **Total Orçado de Mão de Obra Especializada:** {fmt_moeda(tot_val)}  ",
        "> **Fase:** Linha de Base 01",
        "",
        "---",
        "",
        f"## 1. Visão Geral dos {len(contratos)} Contratos Pré-Criados",
        "",
        "Cada contrato abaixo já se encontra redigido, contendo os 4 anexos técnicos obrigatórios para assinatura imediata:",
        "",
        "| Cód. | Arquivo do Contrato | Especialidade da Empreitada | Vigência / Prazo | Efetivo Pico | Valor Total (R$) | Centro Custo | Portão Qualidade (FVS) |",
        "| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |"
    ]
    
    for c in contratos:
        val_str = fmt_moeda(c.get('valor_total', 0.0))
        prazo_str = c.get('prazo', '').split('(')[1].split('|')[0].strip() if '(' in c.get('prazo', '') else c.get('prazo', '')
        pico_str = c.get('efetivo_pico', '').split('(')[0].strip() if '(' in c.get('efetivo_pico', '') else c.get('efetivo_pico', '')
        fvs_str = c.get('fvs_bloqueante', '').split('(')[0].strip() if '(' in c.get('fvs_bloqueante', '') else c.get('fvs_bloqueante', '')
        linhas.append(
            f"| **{c['cod']}** | [`{c['arquivo']}`](file:///{output_dir.replace('\\', '/')}/{c['arquivo']}) | **{c['titulo']}** | {prazo_str} | {pico_str} | {val_str} | `{c['cc']}` | `{fvs_str}` |"
        )
        
    linhas.extend([
        "",
        f"**VALOR TOTAL CONSOLIDADO DOS {len(contratos)} CONTRATOS DE MÃO DE OBRA:** {fmt_moeda(tot_val)}",
        "",
        "---",
        "",
        "## 2. Padrão Governança e Regras de Retenção",
        "",
        "- **100% dos contratos** possuem cláusula vinculativa de retenção de **5% de garantia** por 90 dias;",
        "- **100% dos contratos** exigem aprovação prévia no **Portão SST (POP 17 / NR-18)** antes da mobilização;",
        "- **100% dos contratos** têm a medição atrelada à entrega da FVS assinada;",
        "- Toda Nota Fiscal emitida pelo empreiteiro deve carregar o **Centro de Custo (CC)** indicado em contrato.",
        "",
        "*Dossiê de Contratos disponível para emissão e assinatura pelo Gestor de Obras.*"
    ])
    
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"-> Índice Mestre de Contratos gerado: {caminho}")

def main():
    args = parse_args()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if args.dir:
        project_dir = os.path.abspath(args.dir)
    else:
        project_dir = os.path.join(base_dir, "projetos", args.obra)
        
    if not os.path.exists(project_dir):
        print(f"[ERRO] Diretório não encontrado: {project_dir}")
        sys.exit(1)
        
    config_file = os.path.join(project_dir, "config_obra.json")
    config = {}
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
            
    dados_obra = config.get("dados_obra", {})
    sigla = dados_obra.get("sigla", config.get("sigla_obra", os.path.basename(project_dir).replace("OBRA_", "")))
    titulo = dados_obra.get("nome_obra", config.get("nome_obra", f"Obra {sigla}"))
    area_m2 = float(dados_obra.get("area_construida_m2", config.get("area_construida_m2", 368.4)))
    
    contratos_json = os.path.join(project_dir, "02_ORCAMENTO_BASE_E_CONTRATOS", "contratos_empreiteiros.json")
    if not os.path.exists(contratos_json):
        print(f"[ERRO] Arquivo de contratos não encontrado: {contratos_json}")
        sys.exit(1)
        
    with open(contratos_json, "r", encoding="utf-8") as f:
        contratos = json.load(f)
        
    output_dir = os.path.join(project_dir, "02_ORCAMENTO_BASE_E_CONTRATOS", "CONTRATOS_EMPREITEIROS")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"=== MOTOR UNIVERSAL DE CONTRATOS DE EMPREITEIROS: {titulo} ({sigla}) ===")
    for c in contratos:
        gerar_contrato_individual(c, output_dir, titulo, sigla, area_m2=area_m2)
    gerar_indice_contratos(contratos, output_dir, titulo, sigla, area_m2=area_m2)
    print("=== CONTRATOS DE EMPREITEIROS GERADOS COM SUCESSO! ===")

if __name__ == "__main__":
    main()
