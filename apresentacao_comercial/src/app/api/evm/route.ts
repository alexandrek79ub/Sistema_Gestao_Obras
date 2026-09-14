import fs from 'fs';
import path from 'path';
import { NextResponse } from 'next/server';
import { parseCSV } from '@/lib/csvParser';
import { ErroObra, obterObraObrigatoria } from '@/lib/obra';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const { obra, diretorio } = obterObraObrigatoria(request);
    const orcamentoDir = path.join(diretorio, '02_ORCAMENTO_BASE_E_CONTRATOS');
    const candidatos = [path.join(orcamentoDir, 'ORCAMENTO_BASE_CONSOLIDADO.csv'), path.join(orcamentoDir, `ORCAMENTO_BASE_CONSOLIDADO_${obra}.csv`)];
    const arquivo = candidatos.find((candidato) => fs.existsSync(candidato));
    if (!arquivo) return NextResponse.json({ error: 'Orçamento base não encontrado para a obra selecionada.' }, { status: 404 });

    const csv = parseCSV<Record<string, string>>(arquivo, { requiredHeaderGroups: [['CUSTO_TOTAL', 'Custo Total (R$)', 'Custo Total']] });
    if (csv.status !== 'ok' && csv.status !== 'empty') return NextResponse.json({ error: csv.error, status: csv.status }, { status: csv.status === 'not_found' ? 404 : 422 });

    const bac = csv.data.reduce((total, item) => {
      const valor = item.CUSTO_TOTAL || item['Custo Total (R$)'] || item['Custo Total'] || '';
      const custo = Number(valor.replace('R$', '').replace(/\./g, '').replace(',', '.').trim());
      return Number.isFinite(custo) ? total + custo : total;
    }, 0);

    const semanas = [
      { name: 'Semana 1', VP: bac * 0.08, CR: bac * 0.075, VA: bac * 0.07 },
      { name: 'Semana 2', VP: bac * 0.20, CR: bac * 0.19, VA: bac * 0.18 },
      { name: 'Semana 3', VP: bac * 0.38, CR: bac * 0.40, VA: bac * 0.33 },
      { name: 'Semana 4', VP: bac * 0.55 },
      { name: 'Semana 5', VP: bac * 0.75 },
      { name: 'Semana 6', VP: bac },
    ];
    const atual = semanas[2];
    const spi = atual.VP > 0 ? Number(((atual.VA ?? 0) / atual.VP).toFixed(2)) : 1;
    const cpi = (atual.CR ?? 0) > 0 ? Number(((atual.VA ?? 0) / (atual.CR ?? 1)).toFixed(2)) : 1;
    return NextResponse.json({ obra, semanas, spi, cpi, bac, status: csv.status });
  } catch (error: unknown) {
    if (error instanceof ErroObra) return NextResponse.json({ error: error.message }, { status: 400 });
    return NextResponse.json({ error: 'Falha ao ler EVM.' }, { status: 500 });
  }
}
