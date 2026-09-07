import { NextResponse } from 'next/server';
import { parseCSV } from '@/lib/csvParser';
import path from 'path';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const obra = searchParams.get('obra') || 'OBRA';
  
  const basePath = process.env.OBRA_PATH 
    ? process.env.OBRA_PATH.replace(/OBRA$/, obra)
    : path.resolve(process.cwd(), `../projetos/${obra}`);
    
  const filePath = path.join(basePath, '02_ORCAMENTO_BASE_E_CONTRATOS', 'TEMPLATE_ORCAMENTO_BASE.csv');
  
  try {
    const data = parseCSV(filePath);
    
    // Calcula o total
    let totalBaseline = 0;
    const itens = data.filter((item: any) => item['CUSTO_TOTAL'] && item['CUSTO_TOTAL'].trim() !== '');
    
    itens.forEach((item: any) => {
      const custoStr = item['CUSTO_TOTAL'].replace('R$', '').replace(/\./g, '').replace(',', '.').trim();
      const custo = parseFloat(custoStr);
      if (!isNaN(custo)) {
        totalBaseline += custo;
      }
    });

    return NextResponse.json({ itens, totalBaseline });
  } catch (error) {
    return NextResponse.json({ error: 'Falha ao ler orçamento base', details: error }, { status: 500 });
  }
}
