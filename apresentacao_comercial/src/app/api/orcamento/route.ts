import { NextResponse } from 'next/server';
import { parseCSV } from '@/lib/csvParser';
import path from 'path';
import fs from 'fs';
import { getDb } from '@/lib/db';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const obra = searchParams.get('obra') || 'OBRA';
  
  // 1. Tentar buscar direto do SQLite oficial (SSOT)
  try {
    const db = getDb();
    if (db) {
      const obraRow = db.prepare(
        'SELECT id, codigo, nome FROM obras WHERE UPPER(codigo) = UPPER(?) OR UPPER(nome) = UPPER(?) LIMIT 1'
      ).get(obra, obra) as { id: number; codigo: string; nome: string } | undefined;

      if (obraRow) {
        const sql = `
          SELECT 
            q.cod_eap AS COD_EAP,
            q.descricao AS DESCRICAO_DO_SERVICO,
            q.disciplina AS DISCIPLINA,
            q.unidade AS UNIDADE,
            q.quantidade_liquida AS QUANTIDADE_TOTAL,
            COALESCE(
              CASE WHEN o.bdi_pct > 0 THEN ROUND(o.preco_unitario * (1 + o.bdi_pct / 100.0), 2) ELSE o.preco_unitario END,
              0
            ) AS CUSTO_UNITARIO_BDI,
            COALESCE(o.custo_total, 0) AS CUSTO_TOTAL,
            'Engenharia' AS EMPREITEIRO_VINCULADO,
            q.prancha_referencia AS PRANCHA_REFERENCIA,
            COALESCE(o.fonte_preco, '') AS FONTE_PRECO,
            q.status AS STATUS,
            COALESCE(o.codigo_sinapi, '') AS CODIGO_SINAPI,
            COALESCE(o.centro_custo, '') AS CENTRO_CUSTO,
            COALESCE(o.custo_material, 0) AS CUSTO_MATERIAL,
            COALESCE(o.custo_mao_obra, 0) AS CUSTO_MAO_OBRA,
            COALESCE(o.custo_equipamento, 0) AS CUSTO_EQUIPAMENTO,
            COALESCE(o.bdi_pct, 0) AS BDI_PCT
          FROM itens_quantitativo q
          LEFT JOIN itens_orcamento o ON o.quantitativo_id = q.id AND o.obra_id = q.obra_id
          WHERE q.obra_id = ?
          ORDER BY q.disciplina, q.cod_eap, q.prancha_referencia
        `;
        const itensDb = db.prepare(sql).all(obraRow.id) as Array<Record<string, any>>;
        if (itensDb && itensDb.length > 0) {
          let totalBaseline = 0;
          const itens = itensDb.map(r => {
            const total = Number(r.CUSTO_TOTAL) || 0;
            totalBaseline += total;
            return {
              ...r,
              QUANTIDADE_TOTAL: String(r.QUANTIDADE_TOTAL),
              CUSTO_UNITARIO_BDI: String(r.CUSTO_UNITARIO_BDI),
              CUSTO_TOTAL: String(r.CUSTO_TOTAL)
            };
          });

          return NextResponse.json({
            itens,
            totalBaseline,
            arquivoOrigem: 'SQLite (pmo_virtual.sqlite)'
          });
        }
      }
    }
  } catch (err) {
    console.warn('Erro ao consultar orçamento no SQLite, usando fallback CSV:', err);
  }

  // 2. Fallback para arquivos CSV existentes
  const basePath = process.env.OBRA_PATH 
    ? process.env.OBRA_PATH.replace(/OBRA$/, obra)
    : path.resolve(process.cwd(), `../projetos/${obra}`);
    
  const orcamentoDir = path.join(basePath, '02_ORCAMENTO_BASE_E_CONTRATOS');

  const candidatos = [
    path.join(orcamentoDir, 'ORCAMENTO_BASE_CONSOLIDADO.csv'),
    path.join(orcamentoDir, `ORCAMENTO_BASE_CONSOLIDADO_${obra}.csv`),
    path.join(orcamentoDir, 'TEMPLATE_ORCAMENTO_BASE.csv')
  ];

  const filePath = candidatos.find(p => fs.existsSync(p)) || candidatos[2];
  
  try {
    const rawData = parseCSV<Record<string, string>>(filePath);

    
    let totalBaseline = 0;
    const itens = rawData.map(item => {
      const eap = item['COD_EAP'] || item['Código EAP'] || item['Codigo EAP'] || '';
      const desc = item['DESCRICAO_DO_SERVICO'] || item['Item / Descricao'] || item['Descricao'] || '';
      const unid = item['UNIDADE'] || item['Unidade UCC'] || item['Unidade Proj'] || '';
      const qtd = item['QUANTIDADE_TOTAL'] || item['Qtd Comercial UCC'] || item['Qtd Projeto'] || '0';
      const preco = item['CUSTO_UNITARIO_BDI'] || item['Preço Unitário (R$)'] || item['Preco Unitario'] || '-';
      const total = item['CUSTO_TOTAL'] || item['Custo Total (R$)'] || item['Custo Total'] || '';
      const resp = item['EMPREITEIRO_VINCULADO'] || item['Disciplina'] || 'Engenharia';
      
      if (total && total.trim() !== '' && total !== '-') {
        const custoStr = total.replace('R$', '').replace(/\./g, '').replace(',', '.').trim();
        const custo = parseFloat(custoStr);
        if (!isNaN(custo)) {
          totalBaseline += custo;
        }
      }

      return {
        ...item,
        COD_EAP: eap,
        DESCRICAO_DO_SERVICO: desc,
        UNIDADE: unid,
        QUANTIDADE_TOTAL: qtd,
        CUSTO_UNITARIO_BDI: preco,
        CUSTO_TOTAL: total,
        EMPREITEIRO_VINCULADO: resp
      };
    }).filter(item => item.COD_EAP && item.DESCRICAO_DO_SERVICO);

    return NextResponse.json({ 
      itens, 
      totalBaseline, 
      arquivoOrigem: path.basename(filePath) 
    });
  } catch (error) {
    return NextResponse.json({ error: 'Falha ao ler orçamento base', details: String(error) }, { status: 500 });
  }
}
