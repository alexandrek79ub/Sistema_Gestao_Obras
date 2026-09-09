import { NextResponse } from 'next/server';
import { parseCSV } from '@/lib/csvParser';
import path from 'path';
import fs from 'fs';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const obra = searchParams.get('obra') || 'OBRA';
  
  const basePath = process.env.OBRA_PATH 
    ? process.env.OBRA_PATH.replace(/OBRA$/, obra)
    : path.resolve(process.cwd(), `../projetos/${obra}`);
    
  const orcamentoDir = path.join(basePath, '02_ORCAMENTO_BASE_E_CONTRATOS');

  // Ordem de prioridade para encontrar o orçamento:
  // 1. ORCAMENTO_BASE_CONSOLIDADO.csv (gerado pelo motor mestre)
  // 2. ORCAMENTO_BASE_CONSOLIDADO_${obra}.csv (obras específicas)
  // 3. TEMPLATE_ORCAMENTO_BASE.csv (template legado / padrão)
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
