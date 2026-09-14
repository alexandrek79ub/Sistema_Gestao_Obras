import fs from 'fs';
import path from 'path';
import { NextResponse } from 'next/server';
import { parseCSV } from '@/lib/csvParser';
import { ErroObra, obterObraObrigatoria } from '@/lib/obra';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const { obra, diretorio } = obterObraObrigatoria(request);
    const url = new URL(request.url);
    const demo = url.searchParams.get('demo') === 'true';

    if (demo) {
      const demoBac = 1660762.28;
      const semanas = [
        { name: 'Semana 1', VP: demoBac * 0.08, CR: demoBac * 0.075, VA: demoBac * 0.07 },
        { name: 'Semana 2', VP: demoBac * 0.20, CR: demoBac * 0.19, VA: demoBac * 0.18 },
        { name: 'Semana 3', VP: demoBac * 0.38, CR: demoBac * 0.40, VA: demoBac * 0.33 },
        { name: 'Semana 4', VP: demoBac * 0.55 },
        { name: 'Semana 5', VP: demoBac * 0.75 },
        { name: 'Semana 6', VP: demoBac },
      ];
      const atual = semanas[2];
      const spi = Number(((atual.VA ?? 0) / atual.VP).toFixed(2));
      const cpi = Number(((atual.VA ?? 0) / (atual.CR ?? 1)).toFixed(2));
      return NextResponse.json({
        success: true,
        obra,
        modoDemo: true,
        rotulo: 'MODO DEMONSTRAÇÃO - DADOS SIMULADOS NÃO REAIS',
        proveniencia: { fonte: 'FIXTURE_DEMONSTRACAO', arquivo: null },
        semanas,
        spi,
        cpi,
        bac: demoBac,
        status: 'DEMO',
      });
    }

    // --- MODO PRODUÇÃO REAL: Exclusivamente derivado dos artefatos da obra ativa ---
    const orcamentoDir = path.join(diretorio, '02_ORCAMENTO_BASE_E_CONTRATOS');
    const candidatosOrc = [
      path.join(orcamentoDir, `ORCAMENTO_BASE_CONSOLIDADO_${obra}.csv`),
      path.join(orcamentoDir, 'ORCAMENTO_BASE_CONSOLIDADO.csv'),
    ];
    const arquivoOrc = candidatosOrc.find((c) => fs.existsSync(c));

    let bac: number | null = null;
    let statusOrc = 'not_found';
    if (arquivoOrc) {
      const csv = parseCSV<Record<string, string>>(arquivoOrc, {
        requiredHeaderGroups: [['CUSTO_TOTAL', 'Custo Total (R$)', 'Custo Total']],
      });
      if (csv.status === 'ok') {
        bac = csv.data.reduce((total, item) => {
          const valor = item.CUSTO_TOTAL || item['Custo Total (R$)'] || item['Custo Total'] || '';
          const custo = Number(valor.replace('R$', '').replace(/\./g, '').replace(',', '.').trim());
          return Number.isFinite(custo) ? total + custo : total;
        }, 0);
        statusOrc = 'ok';
      } else {
        statusOrc = csv.status;
      }
    }

    // 2. Verificar dados reais de medição e avanço físico (04_PRODUCAO_E_AVANCO)
    const producaoDir = path.join(diretorio, '04_PRODUCAO_E_AVANCO');
    const candidatosAvanco = [
      path.join(producaoDir, 'dados_avanco_fisico.json'),
      path.join(producaoDir, 'dados_evm.json'),
    ];
    const arquivoAvanco = candidatosAvanco.find((c) => fs.existsSync(c));

    if (arquivoAvanco) {
      try {
        const dadosAvanco = JSON.parse(fs.readFileSync(arquivoAvanco, 'utf-8'));
        return NextResponse.json({
          success: true,
          obra,
          modoDemo: false,
          proveniencia: {
            orcamento: arquivoOrc ? path.basename(arquivoOrc) : null,
            avanco: path.basename(arquivoAvanco),
          },
          semanas: dadosAvanco.semanas || [],
          spi: typeof dadosAvanco.spi === 'number' ? dadosAvanco.spi : null,
          cpi: typeof dadosAvanco.cpi === 'number' ? dadosAvanco.cpi : null,
          bac: bac ?? dadosAvanco.bac ?? null,
          status: 'OK',
        });
      } catch (err) {
        console.error('Erro ao ler arquivo de avanço físico:', err);
      }
    }

    // 3. Verificar cronograma físico-financeiro para curva planejada (VP)
    const planDir = path.join(diretorio, '03_PLANEJAMENTO_E_CRONOGRAMA');
    const candidatosCron = [
      path.join(planDir, `CRONOGRAMA_FISICO_FINANCEIRO_${obra}.csv`),
      path.join(planDir, 'CRONOGRAMA_FISICO_FINANCEIRO.csv'),
    ];
    const arquivoCron = candidatosCron.find((c) => fs.existsSync(c));

    if (arquivoCron) {
      const csvCron = parseCSV<Record<string, string>>(arquivoCron);
      if (csvCron.status === 'ok') {
        const headers = csvCron.headers;
        const colMeses = headers.filter((h) => /^R\$\s*Mês\s*\d+/i.test(h));
        let acumVp = 0;
        const semanasPlanejadas = colMeses.map((col, idx) => {
          const somaMes = csvCron.data.reduce((acc, row) => {
            const raw = (row[col] || '').replace('R$', '').replace(/\./g, '').replace(',', '.').trim();
            const n = parseFloat(raw);
            return Number.isFinite(n) ? acc + n : acc;
          }, 0);
          acumVp += somaMes;
          return {
            name: `Mês ${idx + 1}`,
            VP: Math.round(acumVp * 100) / 100,
            VA: null,
            CR: null,
          };
        });

        return NextResponse.json({
          success: true,
          obra,
          modoDemo: false,
          proveniencia: {
            orcamento: arquivoOrc ? path.basename(arquivoOrc) : null,
            cronograma: path.basename(arquivoCron),
            medicoes: null,
          },
          semanas: semanasPlanejadas,
          spi: null,
          cpi: null,
          bac,
          status: 'PLANEJADO_SEM_MEDICAO',
          mensagem: 'Curva S planejada carregada. Medições reais (VA e CR) ainda não registradas para a obra.',
        });
      }
    }

    // 4. Sem dados disponíveis
    return NextResponse.json({
      success: true,
      obra,
      modoDemo: false,
      proveniencia: {
        orcamento: arquivoOrc ? path.basename(arquivoOrc) : null,
        cronograma: null,
        medicoes: null,
      },
      semanas: [],
      spi: null,
      cpi: null,
      bac,
      status: 'SEM_DADOS',
      mensagem: 'Sem dados de cronograma físico-financeiro ou medições de campo para a obra.',
    });
  } catch (error: unknown) {
    if (error instanceof ErroObra) return NextResponse.json({ error: error.message }, { status: 400 });
    return NextResponse.json({ error: 'Falha ao ler EVM.' }, { status: 500 });
  }
}
