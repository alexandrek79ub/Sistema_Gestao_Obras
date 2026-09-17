import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path
from motor_quantitativos.exportadores import exportar_artefatos

def main():
    db_path = Path("data/pmo_virtual.sqlite")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    obra_id = 3 # OBRA_PORTO
    agora = datetime.now(timezone.utc).isoformat()

    # 1. Registrar Revisão 1 para OBRA_PORTO
    cursor.execute("""
        INSERT INTO revisoes (obra_id, tipo, usuario, justificativa, origem, created_at)
        VALUES (?, 'QUANTITATIVO', 'auditor-engenharia', 
                'Levantamento nominal auditado da Prancha EGS-052 rev.A (Armação de Sapatas e Arranques)', 
                'auditoria-pranchas:EGS-052', ?)
    """, (obra_id, agora))
    revisao_id = cursor.lastrowid
    print(f"Revisão criada para Obra {obra_id}: ID {revisao_id}")

    # 2. Itens auditados da Prancha EGS-052 rev.A
    prancha_052 = "AÇU-3.DES-2.3100-11-EGS-052 rev.A.pdf"
    
    itens = [
        {
            "cod_eap": "1.3.7.1",
            "descricao": "Fôrma de Madeira Compensada para Sapatas Isoladas",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m²",
            "quantidade_liquida": 35.88,
            "expressao_matematica": "11 * 2 * (1.00 + 1.00) * 0.30 + 6 * 2 * (1.10 + 1.10) * 0.30 + 9 * 2 * (0.90 + 0.90) * 0.30 + 6 * 2 * (0.70 + 0.70) * 0.30",
            "prancha_referencia": prancha_052,
            "status": "LEVANTADO",
            "observacao": "Auditado contra Prancha EGS-052: base h=0,30m para SE1. Valor idêntico ao resumo da prancha (35,88 m²).",
            "sinapi": "92443",
            "pu": 72.00,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.7.2",
            "descricao": "Fôrma de Madeira Compensada para Arranques de Pilares",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m²",
            "quantidade_liquida": 25.76,
            "expressao_matematica": "8 * (4 * 0.25) * 0.70 + 24 * (4 * 0.30) * 0.70",
            "prancha_referencia": prancha_052,
            "status": "LEVANTADO",
            "observacao": "Auditado contra Prancha EGS-052: 8 arranques 25x25 (5.60m²) + 24 arranques 30x30 (20.16m²).",
            "sinapi": "92412",
            "pu": 138.50,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.8.1",
            "descricao": "Armação Aço CA-50 em Sapatas e Arranques de Pilares",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "kg",
            "quantidade_liquida": 401.70,
            "expressao_matematica": "256.0 + 35.6 + 110.1",
            "prancha_referencia": prancha_052,
            "status": "LEVANTADO",
            "observacao": "Auditado contra Prancha EGS-052: Resumo do aço (256.0 kg sapatas + 145.7 kg arranques = 401.7 kg).",
            "sinapi": "92762",
            "pu": 14.50,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.9.1",
            "descricao": "Concreto Usinado C30 para Sapatas Isoladas",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m³",
            "quantidade_liquida": 8.55,
            "expressao_matematica": "11 * 1.00 * 1.00 * 0.30 + 6 * 1.10 * 1.10 * 0.30 + 9 * 0.90 * 0.90 * 0.30 + 6 * 0.70 * 0.70 * 0.30",
            "prancha_referencia": prancha_052,
            "status": "LEVANTADO",
            "observacao": "Auditado contra Prancha EGS-052: base h=0,30m para SE1. Valor idêntico ao resumo da prancha (8,55 m³).",
            "sinapi": "94970",
            "pu": 510.00,
            "fonte": "SINAPI-SP 07/2026",
            "centro_custo": "FUNDACOES"
        },
        {
            "cod_eap": "1.3.9.2",
            "descricao": "Concreto Usinado C30 para Arranques de Pilares",
            "disciplina": "Infraestrutura e Fundações",
            "unidade": "m³",
            "quantidade_liquida": 1.86,
            "expressao_matematica": "8 * 0.25 * 0.25 * 0.70 + 24 * 0.30 * 0.30 * 0.70",
            "prancha_referencia": prancha_052,
            "status": "LEVANTADO",
            "observacao": "Auditado contra Prancha EGS-052: 8 arranques 25x25 (0.35m³) + 24 arranques 30x30 (1.51m³).",
            "sinapi": "103672",
            "pu": 510.00,
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
        
        # Inserir também no orçamento
        preco = it["pu"]
        bdi = 0.0 # BDI padrão
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

    # Atualizar titulo da prancha EGS-052 em lista_desenhos para OBRA_PORTO
    cursor.execute("""
        UPDATE lista_desenhos 
        SET status = 'VIGENTE', 
            titulo = 'ARMAÇÃO DAS SAPATAS E ARRANQUES DOS PILARES',
            updated_at = ?
        WHERE obra_id = ? AND codigo LIKE '%EGS-052%'
    """, (agora, obra_id))

    conn.commit()
    print("5 itens inseridos com sucesso em itens_quantitativo e itens_orcamento para OBRA_PORTO!")

    # 3. Exportar artefatos oficiais para o diretório base de OBRA_PORTO
    saidas = exportar_artefatos(conn, obra_id)
    print("\nArtefatos exportados com sucesso para OBRA_PORTO:")
    for s in saidas:
        print(f" - {s}")

    conn.close()

if __name__ == "__main__":
    main()
