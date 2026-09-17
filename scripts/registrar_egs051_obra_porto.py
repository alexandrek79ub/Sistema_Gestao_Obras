import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from motor_quantitativos.exportadores import exportar_artefatos

def main():
    db_path = Path("data/pmo_virtual.sqlite")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    obra_id = 3  # OBRA_PORTO
    agora = datetime.now(timezone.utc).isoformat()

    # 1. Registrar Nova Revisão para OBRA_PORTO
    cursor.execute("""
        INSERT INTO revisoes (obra_id, tipo, usuario, justificativa, origem, created_at)
        VALUES (?, 'QUANTITATIVO', 'auditor-engenharia', 
                'Levantamento nominal auditado da Prancha EGS-051 rev.A (Geometria das Vigas Baldrames)', 
                'auditoria-pranchas:EGS-051', ?)
    """, (obra_id, agora))
    revisao_id = cursor.lastrowid
    print(f"[1/4] Revisão criada para Obra {obra_id}: ID {revisao_id}")

    # 2. Itens auditados da Prancha EGS-051 rev.A
    prancha_051 = "AÇU-3.DES-2.3100-11-EGS-051 rev.A.pdf"
    
    itens = [
        {
            "cod_eap": "1.3.1",
            "descricao": "Locação da Obra e Gabarito Topográfico",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m²",
            "quantidade_liquida": 298.245,
            "expressao_matematica": "29.50 * 10.11",
            "prancha_referencia": prancha_051,
            "status": "LEVANTADO",
            "observacao": "Área de projeção do edifício conforme eixos de locação EGS-051 (29,50m x 10,11m).",
            "sinapi": "98458",
            "pu": 12.50,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.4",
            "descricao": "Escavação Manual/Mecanizada de Valas para Baldrames",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m³",
            "quantidade_liquida": 41.634,
            "expressao_matematica": "205.60 * 0.45 * 0.45",
            "prancha_referencia": prancha_051,
            "status": "LEVANTADO",
            "observacao": "Extensão total das vigas baldrames VB1 a VB19 (205,60m) com vala de 0,45m de largura e 0,45m de profundidade.",
            "sinapi": "93358",
            "pu": 55.00,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.4.1",
            "descricao": "Escavação Mecânica/Manual de Cavas para Sapatas Isoladas",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m³",
            "quantidade_liquida": 41.73,
            "expressao_matematica": "11 * 1.20 * 1.20 * 1.00 + 6 * 1.30 * 1.30 * 1.00 + 9 * 1.10 * 1.10 * 1.00 + 6 * 0.90 * 0.90 * 1.00",
            "prancha_referencia": prancha_051,
            "status": "LEVANTADO",
            "observacao": "Escavação das cavas com folga de 10cm de cada lado conforme locação EGS-051 cruzada com EGS-052.",
            "sinapi": "93358",
            "pu": 62.00,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.5",
            "descricao": "Apiloamento e Regularização de Fundo de Vala",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m²",
            "quantidade_liquida": 92.52,
            "expressao_matematica": "205.60 * 0.45",
            "prancha_referencia": prancha_051,
            "status": "LEVANTADO",
            "observacao": "Fundo de valas para vigas baldrames: 205,60m de extensão x 0,45m de largura.",
            "sinapi": "96523",
            "pu": 8.20,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.5.1",
            "descricao": "Apiloamento e Regularização de Fundo de Cava para Sapatas",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m²",
            "quantidade_liquida": 41.73,
            "expressao_matematica": "11 * 1.20 * 1.20 + 6 * 1.30 * 1.30 + 9 * 1.10 * 1.10 + 6 * 0.90 * 0.90",
            "prancha_referencia": prancha_051,
            "status": "LEVANTADO",
            "observacao": "Área de regularização de fundo de cava para 32 sapatas isoladas.",
            "sinapi": "96523",
            "pu": 8.20,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.6",
            "descricao": "Lastro de Concreto Magro e=5cm para Fundação de Baldrames",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m³",
            "quantidade_liquida": 4.626,
            "expressao_matematica": "205.60 * 0.45 * 0.05",
            "prancha_referencia": prancha_051,
            "status": "LEVANTADO",
            "observacao": "Concreto magro espessura 5cm sob as vigas baldrames.",
            "sinapi": "96527",
            "pu": 390.00,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.6.1",
            "descricao": "Lastro de Concreto Magro e=5cm para Sapatas Isoladas",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m³",
            "quantidade_liquida": 2.0865,
            "expressao_matematica": "11 * 1.20 * 1.20 * 0.05 + 6 * 1.30 * 1.30 * 0.05 + 9 * 1.10 * 1.10 * 0.05 + 6 * 0.90 * 0.90 * 0.05",
            "prancha_referencia": prancha_051,
            "status": "LEVANTADO",
            "observacao": "Concreto magro espessura 5cm sob as sapatas isoladas.",
            "sinapi": "96527",
            "pu": 390.00,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.11",
            "descricao": "Impermeabilização com Tinta Asfáltica em Baldrames (Topo + 2 Lados)",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m²",
            "quantidade_liquida": 215.88,
            "expressao_matematica": "205.60 * (0.25 + 2 * 0.40)",
            "prancha_referencia": prancha_051,
            "status": "LEVANTADO",
            "observacao": "Pintura betuminosa em 3 faces de contato: topo (0,25m) + laterais (2 x 0,40m) = 1,05m desenvolvimento.",
            "sinapi": "98546",
            "pu": 28.50,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.11.1",
            "descricao": "Impermeabilização com Tinta Asfáltica sobre Sapatas",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m²",
            "quantidade_liquida": 60.87,
            "expressao_matematica": "35.04 + (11 * 1.00 * 1.00 + 6 * 1.10 * 1.10 + 9 * 0.90 * 0.90 + 6 * 0.70 * 0.70) - (24 * 0.30 * 0.30 + 8 * 0.25 * 0.25)",
            "prancha_referencia": prancha_051,
            "status": "LEVANTADO",
            "observacao": "Topo e laterais de sapatas descontando projeção de pilares.",
            "sinapi": "98546",
            "pu": 28.50,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.13",
            "descricao": "Reaterro Manual/Mecanizado Compactado de Valas de Baldrames",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m³",
            "quantidade_liquida": 21.348,
            "expressao_matematica": "(205.60 * 0.45 * 0.45) - 15.66 - (205.60 * 0.45 * 0.05)",
            "prancha_referencia": prancha_051,
            "status": "LEVANTADO",
            "observacao": "Volume de cava (41,63m³) descontando o concreto das baldrames (15,66m³) e o lastro magro (4,63m³).",
            "sinapi": "96529",
            "pu": 36.00,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.13.1",
            "descricao": "Reaterro Compactado de Cavas de Sapatas",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m³",
            "quantidade_liquida": 31.243,
            "expressao_matematica": "41.73 - 8.40 - 2.087",
            "prancha_referencia": prancha_051,
            "status": "LEVANTADO",
            "observacao": "Volume de escavação (41,73m³) descontando o volume enterrado de concreto e lastro.",
            "sinapi": "96529",
            "pu": 36.00,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.14",
            "descricao": "Carga e Remoção de Terra Excedente (Bota-fora de Baldrames)",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m³",
            "quantidade_liquida": 20.286,
            "expressao_matematica": "15.66 + (205.60 * 0.45 * 0.05)",
            "prancha_referencia": prancha_051,
            "status": "LEVANTADO",
            "observacao": "Volume deslocado pelo concreto das vigas baldrames (15,66m³) + lastro magro (4,63m³).",
            "sinapi": "97914",
            "pu": 24.00,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.14.1",
            "descricao": "Bota-fora de Terra Excedente de Sapatas",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m³",
            "quantidade_liquida": 11.835,
            "expressao_matematica": "8.55 + 1.86 + 1.425",
            "prancha_referencia": prancha_051,
            "status": "LEVANTADO",
            "observacao": "Volume deslocado pelo concreto das sapatas (8,55m³), pedestais (1,86m³) e lastro (1,425m³).",
            "sinapi": "97914",
            "pu": 24.00,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        }
    ]

    for it in itens:
        cursor.execute("""
            INSERT INTO itens_quantitativo (
                obra_id, revisao_id, cod_eap, descricao, disciplina, unidade,
                quantidade_liquida, expressao_matematica, prancha_referencia,
                status, observacao, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            obra_id, revisao_id, it["cod_eap"], it["descricao"], it["disciplina"],
            it["unidade"], it["quantidade_liquida"], it["expressao_matematica"],
            it["prancha_referencia"], it["status"], it["observacao"], agora
        ))
        quant_id = cursor.lastrowid
        
        # Inserir no orçamento
        preco = it["pu"]
        bdi = 0.0
        custo_tot = round(it["quantidade_liquida"] * preco, 2)
        cursor.execute("""
            INSERT INTO itens_orcamento (
                obra_id, quantitativo_id, revisao_id, codigo_sinapi, centro_custo,
                fonte_preco, preco_unitario, bdi_pct, custo_total, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            obra_id, quant_id, revisao_id, it["sinapi"], it["centro_custo"],
            it["fonte"], preco, bdi, custo_tot, agora
        ))

    # Atualizar título e status da prancha EGS-051 em lista_desenhos para OBRA_PORTO
    cursor.execute("""
        UPDATE lista_desenhos 
        SET status = 'VIGENTE', 
            titulo = 'GEOMETRIA DAS VIGAS BALDRAMES',
            updated_at = ?
        WHERE obra_id = ? AND codigo LIKE '%EGS-051%'
    """, (agora, obra_id))

    conn.commit()
    print(f"[2/4] {len(itens)} itens inseridos com sucesso no SQLite para OBRA_PORTO (obra_id={obra_id})!")

    # 3. Exportar artefatos oficiais para o diretório de OBRA_PORTO
    saidas = exportar_artefatos(conn, obra_id)
    print("\n[3/4] Artefatos consolidados exportados:")
    for s in saidas:
        print(f" - {s}")

    conn.close()

if __name__ == "__main__":
    main()
