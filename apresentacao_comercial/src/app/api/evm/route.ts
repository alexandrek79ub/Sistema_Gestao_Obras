import { NextResponse } from 'next/server';
import { parseCSV } from '@/lib/csvParser';
import path from 'path';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const obra = searchParams.get('obra') || 'OBRA';
  
  const basePath = process.env.OBRA_PATH 
    ? process.env.OBRA_PATH.replace(/OBRA$/, obra)
    : path.resolve(process.cwd(), `../projetos/${obra}`);
    
  const orcamentoPath = path.join(basePath, '02_ORCAMENTO_BASE_E_CONTRATOS', 'TEMPLATE_ORCAMENTO_BASE.csv');
  
  try {
    const data = parseCSV(orcamentoPath);
    
    // Calcula o BAC (Orçamento Total)
    let bac = 0;
    const itens = data.filter((item: any) => item['CUSTO_TOTAL'] && item['CUSTO_TOTAL'].trim() !== '');
    
    itens.forEach((item: any) => {
      const custoStr = item['CUSTO_TOTAL'].replace('R$', '').replace(/\./g, '').replace(',', '.').trim();
      const custo = parseFloat(custoStr);
      if (!isNaN(custo)) {
        bac += custo;
      }
    });

    // Mock das medições e NFs (Sprint 2 simplificado, já que os dados reais de avanço ainda não existem em CSV estruturado)
    const evmData = [
      { name: 'Semana 1', VP: bac * 0.08, CR: bac * 0.075, VA: bac * 0.07 },
      { name: 'Semana 2', VP: bac * 0.20, CR: bac * 0.19, VA: bac * 0.18 },
      { name: 'Semana 3', VP: bac * 0.38, CR: bac * 0.40, VA: bac * 0.33 }, // Descolamento na semana 3
      { name: 'Semana 4', VP: bac * 0.55 },
      { name: 'Semana 5', VP: bac * 0.75 },
      { name: 'Semana 6', VP: bac * 1.00 }
    ];

    // Na Semana 3 (atual):
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
    return NextResponse.json({ error: 'Falha ao ler EVM', details: error }, { status: 500 });
  }
}
