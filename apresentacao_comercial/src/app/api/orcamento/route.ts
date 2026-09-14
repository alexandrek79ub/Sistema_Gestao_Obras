import fs from 'fs';
import path from 'path';
import { NextResponse } from 'next/server';
import { parseCSV } from '@/lib/csvParser';
import { ErroObra, obterObraObrigatoria } from '@/lib/obra';

export const dynamic = 'force-dynamic';

const CONTRATO_ORCAMENTO = {
  requiredHeaderGroups: [
    ['CIA', 'COD_EAP', 'Código EAP', 'Codigo EAP'],
    ['SERVICO', 'DESCRICAO_DO_SERVICO', 'Item / Descricao', 'Descricao'],
    ['CUSTO_TOTAL', 'Custo Total (R$)', 'Custo Total'],
  ],
};

function respostaErroCsv(status: string, error?: string) {
  const httpStatus = status === 'not_found' ? 404 : status === 'empty' ? 200 : 422;
  return NextResponse.json({ error: error || 'Falha ao ler orçamento base.', status, itens: [], totalBaseline: 0 }, { status: httpStatus });
}

export async function GET(request: Request) {
  try {
    const { obra, diretorio } = obterObraObrigatoria(request);
    const orcamentoDir = path.join(diretorio, '02_ORCAMENTO_BASE_E_CONTRATOS');
    const candidatos = [
      path.join(orcamentoDir, 'ORCAMENTO_BASE_CONSOLIDADO.csv'),
      path.join(orcamentoDir, `ORCAMENTO_BASE_CONSOLIDADO_${obra}.csv`),
      path.join(orcamentoDir, 'TEMPLATE_ORCAMENTO_BASE.csv'),
    ];
    const filePath = candidatos.find((candidato) => fs.existsSync(candidato));
    if (!filePath) return respostaErroCsv('not_found', 'Orçamento base não encontrado para a obra selecionada.');

    const csv = parseCSV<Record<string, string>>(filePath, CONTRATO_ORCAMENTO);
    if (csv.status !== 'ok' && csv.status !== 'empty') return respostaErroCsv(csv.status, csv.error);

    let totalBaseline = 0;
    const itens = csv.data.map((item) => {
      const eap = item.COD_EAP || item['Código EAP'] || item['Codigo EAP'] || item.CIA || '';
      const descricao = item.DESCRICAO_DO_SERVICO || item['Item / Descricao'] || item.Descricao || item.SERVICO || '';
      const total = item.CUSTO_TOTAL || item['Custo Total (R$)'] || item['Custo Total'] || '';
      const custo = Number(total.replace('R$', '').replace(/\./g, '').replace(',', '.').trim());
      if (Number.isFinite(custo)) totalBaseline += custo;
      return {
        ...item,
        COD_EAP: eap,
        DESCRICAO_DO_SERVICO: descricao,
        UNIDADE: item.UNIDADE || item['Unidade UCC'] || item.UNIDADE_MEDIDA || '',
        QUANTIDADE_TOTAL: item.QUANTIDADE_TOTAL || item['Qtd Comercial UCC'] || item.QUANTIDADE_UCC || item.QUANTIDADE || '0',
        CUSTO_UNITARIO_BDI: item.CUSTO_UNITARIO_BDI || item['Preço Unitário (R$)'] || item.PRECO_UNIT || '',
        CUSTO_TOTAL: total,
        EMPREITEIRO_VINCULADO: item.EMPREITEIRO_VINCULADO || item.Disciplina || item.DISCIPLINA || '',
      };
    }).filter((item) => item.COD_EAP && item.DESCRICAO_DO_SERVICO);

    return NextResponse.json({ obra, itens, totalBaseline, arquivoOrigem: path.basename(filePath), status: csv.status });
  } catch (error: unknown) {
    if (error instanceof ErroObra) return NextResponse.json({ error: error.message }, { status: 400 });
    return NextResponse.json({ error: 'Falha ao ler orçamento base.' }, { status: 500 });
  }
}
