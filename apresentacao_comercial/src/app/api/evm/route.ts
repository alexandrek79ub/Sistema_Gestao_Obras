import { NextResponse } from 'next/server';
import { parseCSV } from '@/lib/csvParser';
import path from 'path';
import fs from 'fs';
import { getDb } from '@/lib/db';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const obra = searchParams.get('obra') || 'OBRA';
  
  try {
    let bac = 0;
    let bacCalculado = false;

    // 1. Tentar calcular BAC direto do SQLite
    try {
      const db = getDb();
      if (db) {
        const obraRow = db.prepare(
          'SELECT id FROM obras WHERE UPPER(codigo) = UPPER(?) OR UPPER(nome) = UPPER(?) LIMIT 1'
        ).get(obra, obra) as { id: number } | undefined;

        if (obraRow) {
          const row = db.prepare(
            'SELECT COALESCE(SUM(custo_total), 0) as total FROM itens_orcamento WHERE obra_id = ?'
          ).get(obraRow.id) as { total: number } | undefined;

          if (row && Number(row.total) > 0) {
            bac = Number(row.total);
            bacCalculado = true;
          }
        }
      }
    } catch (err) {
      console.warn('Erro ao calcular BAC no SQLite, usando fallback:', err);
    }

    // 2. Fallback CSV se o SQLite não calculou
    if (!bacCalculado) {
      const basePath = process.env.OBRA_PATH 
        ? process.env.OBRA_PATH.replace(/OBRA$/, obra)
        : path.resolve(process.cwd(), `../projetos/${obra}`);
        
      const orcamentoDir = path.join(basePath, '02_ORCAMENTO_BASE_E_CONTRATOS');
      const candidatosOrcamento = [
        path.join(orcamentoDir, 'ORCAMENTO_BASE_CONSOLIDADO.csv'),
        path.join(orcamentoDir, `ORCAMENTO_BASE_CONSOLIDADO_${obra}.csv`),
        path.join(orcamentoDir, 'TEMPLATE_ORCAMENTO_BASE.csv')
      ];
      const orcamentoPath = candidatosOrcamento.find(p => fs.existsSync(p)) || candidatosOrcamento[2];
      
      const data = parseCSV(orcamentoPath);
      data.forEach((item: any) => {
        const rawCusto = item['CUSTO_TOTAL'] || item['Custo Total (R$)'] || item['Custo Total'] || '';
        if (rawCusto && rawCusto.trim() !== '' && rawCusto !== '-') {
          const custoStr = rawCusto.replace('R$', '').replace(/\./g, '').replace(',', '.').trim();
          const custo = parseFloat(custoStr);
          if (!isNaN(custo)) {
            bac += custo;
          }
        }
      });
    }

    // Mock das medições e NFs (Sprint 2 simplificado, já que os dados reais de avanço ainda não existem em CSV estruturado)
    const evmData = [
      { name: 'Semana 1', VP: bac * 0.08, CR: bac * 0.075, VA: bac * 0.07 },
      { name: 'Semana 2', VP: bac * 0.20, CR: bac * 0.19, VA: bac * 0.18 },
      { name: 'Semana 3', VP: bac * 0.38, CR: bac * 0.40, VA: bac * 0.33 },
      { name: 'Semana 4', VP: bac * 0.55 },
      { name: 'Semana 5', VP: bac * 0.75 },
      { name: 'Semana 6', VP: bac * 1.00 }
    ];

    const currentVP = evmData[2].VP;
    const currentCR = evmData[2].CR!;
    const currentVA = evmData[2].VA!;

    const spi = currentVP > 0 ? (currentVA / currentVP).toFixed(2) : 1;
    const cpi = currentCR > 0 ? (currentVA / currentCR).toFixed(2) : 1;

    return NextResponse.json({ 
      semanas: evmData, 
      spi: parseFloat(spi as string), 
      cpi: parseFloat(cpi as string), 
      bac 
    });
  } catch (error) {
    return NextResponse.json({ error: 'Falha ao processar EVM', details: String(error) }, { status: 500 });
  }
}
