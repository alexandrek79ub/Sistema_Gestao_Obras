import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';
import { parseCSV } from '@/lib/csvParser';
import { ErroObra, obterObraObrigatoria } from '@/lib/obra';

export const dynamic = 'force-dynamic';

export interface FluxoMensal {
  mes: string;
  entradas: number;
  saidas: number;
  saldoOperacional: number;
  saldoAcumulado: number;
}

export interface RequisicaoCompra {
  id: string;
  tipo: string;
  pacote: string;
  centroCusto: string;
  disciplina: string;
  dataDisparo: string;
  dataCanteiro: string;
  leadTimeDias: string;
  estagio: string;
  semaforo: string;
  budget: number;
}

export interface MedicaoEmpreiteiro {
  quinzena: string;
  mes: string;
  valorBruto: number;
  retencao5: number;
  valorLiquido: number;
  status: 'PAGO' | 'EM_ANALISE' | 'A_MEDIR';
}

export async function GET(request: Request) {
  try {
    const { obra, diretorio } = obterObraObrigatoria(request);
    const url = new URL(request.url);
    const demo = url.searchParams.get('demo') === 'true';

    if (demo) {
      const demoFluxo: FluxoMensal[] = [
        { mes: 'Mês 1', entradas: 0, saidas: 105467.76, saldoOperacional: -105467.76, saldoAcumulado: -105467.76 },
        { mes: 'Mês 2', entradas: 155269.92, saidas: 202190.46, saldoOperacional: -46920.54, saldoAcumulado: -152388.30 },
        { mes: 'Mês 3', entradas: 264001.06, saidas: 292234.46, saldoOperacional: -28233.40, saldoAcumulado: -180621.70 },
        { mes: 'Mês 4', entradas: 348054.46, saidas: 290517.52, saldoOperacional: 57536.94, saldoAcumulado: -123084.76 },
        { mes: 'Mês 5', entradas: 233397.32, saidas: 259914.12, saldoOperacional: -26516.80, saldoAcumulado: -149601.56 },
        { mes: 'Mês 6', entradas: 304396.06, saidas: 287957.98, saldoOperacional: 16438.08, saldoAcumulado: -133163.48 },
        { mes: 'Mês 7 (TRD)', entradas: 355643.46, saidas: 118585.53, saldoOperacional: 237057.93, saldoAcumulado: 103894.45 },
      ];
      const demoMedicoes: MedicaoEmpreiteiro[] = [
        { quinzena: 'Q01', mes: 'Mês 1 (1ª)', valorBruto: 78500.0, retencao5: 3925.0, valorLiquido: 74575.0, status: 'PAGO' },
        { quinzena: 'Q02', mes: 'Mês 1 (2ª)', valorBruto: 84942.02, retencao5: 4247.1, valorLiquido: 80694.92, status: 'EM_ANALISE' },
        { quinzena: 'Q03', mes: 'Mês 2 (1ª)', valorBruto: 135000.0, retencao5: 6750.0, valorLiquido: 128250.0, status: 'A_MEDIR' },
        { quinzena: 'Q04', mes: 'Mês 2 (2ª)', valorBruto: 142895.85, retencao5: 7144.79, valorLiquido: 135751.06, status: 'A_MEDIR' },
        { quinzena: 'Q05', mes: 'Mês 3 (1ª)', valorBruto: 180000.0, retencao5: 9000.0, valorLiquido: 171000.0, status: 'A_MEDIR' },
        { quinzena: 'Q06', mes: 'Mês 3 (2ª)', valorBruto: 186373.12, retencao5: 9318.66, valorLiquido: 177054.46, status: 'A_MEDIR' },
        { quinzena: 'Q07', mes: 'Mês 4 (1ª)', valorBruto: 120000.0, retencao5: 6000.0, valorLiquido: 114000.0, status: 'A_MEDIR' },
        { quinzena: 'Q08', mes: 'Mês 4 (2ª)', valorBruto: 125681.39, retencao5: 6284.07, valorLiquido: 119397.32, status: 'A_MEDIR' },
        { quinzena: 'Q09', mes: 'Mês 5 (1ª)', valorBruto: 160000.0, retencao5: 8000.0, valorLiquido: 152000.0, status: 'A_MEDIR' },
        { quinzena: 'Q10', mes: 'Mês 5 (2ª)', valorBruto: 160416.9, retencao5: 8020.84, valorLiquido: 152396.06, status: 'A_MEDIR' },
        { quinzena: 'Q11', mes: 'Mês 6 (1ª)', valorBruto: 140000.0, retencao5: 7000.0, valorLiquido: 133000.0, status: 'A_MEDIR' },
        { quinzena: 'Q12', mes: 'Mês 6 (2ª)', valorBruto: 146953.0, retencao5: 7347.65, valorLiquido: 139605.35, status: 'A_MEDIR' },
      ];
      return NextResponse.json({
        success: true,
        obra,
        modoDemo: true,
        rotulo: 'MODO DEMONSTRAÇÃO - DADOS SIMULADOS NÃO REAIS',
        proveniencia: { fonte: 'FIXTURE_DEMONSTRACAO' },
        kpis: {
          faturamentoTotal: 1660762.28,
          desembolsoTotal: 1556867.83,
          margemContratual: 103894.45,
          margemPercent: 6.26,
          capitalGiroMaximo: -180621.70,
          mesPicoExposicao: 'Mês 3',
          totalRetencaoCaucao: 83038.11,
          totalPacotesSuprimentos: 41,
          materiaisRcCount: 24,
          equipamentosReCount: 17,
        },
        fluxoMensal: demoFluxo,
        requisicoes: [],
        medicoesQuinzenais: demoMedicoes,
      });
    }

    // --- MODO PRODUÇÃO REAL: Exclusivamente derivado dos arquivos da obra ativa ---
    const supDir = path.join(diretorio, '05_SUPRIMENTOS_E_FINANCEIRO');
    const candidatosFluxo = [
      path.join(supDir, `FLUXO_DE_CAIXA_${obra}.csv`),
      path.join(supDir, 'FLUXO_DE_CAIXA.csv'),
    ];
    const caminhoFluxo = candidatosFluxo.find((c) => fs.existsSync(c));

    const fluxoMensal: FluxoMensal[] = [];
    let kpis = {
      faturamentoTotal: 0,
      desembolsoTotal: 0,
      margemContratual: 0,
      margemPercent: 0,
      capitalGiroMaximo: 0,
      mesPicoExposicao: 'N/A',
      totalRetencaoCaucao: 0,
    };

    if (caminhoFluxo) {
      try {
        const csvFluxo = parseCSV<Record<string, string>>(caminhoFluxo);
        if (csvFluxo.status === 'ok') {
          const rows = csvFluxo.data;
          const rowEntradas = rows.find((r) => {
            const rub = r['Conta / Rubrica Financeira'] || '';
            return rub.includes('TOTAL DE ENTRADAS') || rub.includes('1. ENTRADAS');
          });
          const rowSaidas = rows.find((r) => {
            const rub = r['Conta / Rubrica Financeira'] || '';
            return rub.includes('TOTAL DE SAÍDAS') || rub.includes('2. SAÍDAS');
          });
          const rowSaldoAcum = rows.find((r) => {
            const rub = r['Conta / Rubrica Financeira'] || '';
            return rub.includes('Saldo de Caixa Acumulado') || rub.includes('3.2 Saldo');
          });
          const rowRetencao = rows.find((r) => {
            const rub = r['Conta / Rubrica Financeira'] || '';
            return rub.includes('Retenção Técnica') || rub.includes('1.2 Retenção');
          });

          // Detectar colunas de meses dinamicamente
          const headers = csvFluxo.headers;
          const colMeses = headers.filter((h) => /^Mês\s*\d+/i.test(h));

          if (rowEntradas && rowSaidas) {
            let menorSaldo = 0;
            let mesPico = 'N/A';

            for (const m of colMeses) {
              const ent = parseFloat((rowEntradas[m] || '0').replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 0;
              const sai = parseFloat((rowSaidas[m] || '0').replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 0;
              const acum = rowSaldoAcum
                ? parseFloat((rowSaldoAcum[m] || '0').replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 0
                : 0;

              if (acum < menorSaldo) {
                menorSaldo = acum;
                mesPico = m;
              }

              fluxoMensal.push({
                mes: m,
                entradas: ent,
                saidas: sai,
                saldoOperacional: Math.round((ent - sai) * 100) / 100,
                saldoAcumulado: acum,
              });
            }

            const fatTotal = rowEntradas['Total Consolidado (R$)']
              ? parseFloat(rowEntradas['Total Consolidado (R$)'].replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 0
              : fluxoMensal.reduce((acc, f) => acc + f.entradas, 0);

            const desTotal = rowSaidas['Total Consolidado (R$)']
              ? parseFloat(rowSaidas['Total Consolidado (R$)'].replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 0
              : fluxoMensal.reduce((acc, f) => acc + f.saidas, 0);

            const margem = fatTotal - desTotal;
            const margemPct = fatTotal > 0 ? Number(((margem / fatTotal) * 100).toFixed(2)) : 0;

            const totRetencao = rowRetencao && rowRetencao['Total Consolidado (R$)']
              ? parseFloat(rowRetencao['Total Consolidado (R$)'].replace('R$', '').replace(/\./g, '').replace(',', '.').trim()) || 0
              : 0;

            kpis = {
              faturamentoTotal: Math.round(fatTotal * 100) / 100,
              desembolsoTotal: Math.round(desTotal * 100) / 100,
              margemContratual: Math.round(margem * 100) / 100,
              margemPercent: margemPct,
              capitalGiroMaximo: Math.round(menorSaldo * 100) / 100,
              mesPicoExposicao: mesPico,
              totalRetencaoCaucao: Math.round(totRetencao * 100) / 100,
            };
          }
        }
      } catch (err) {
        console.error('Erro ao ler CSV de fluxo:', err);
      }
    }

    // 2. Requisições de Compras (dados_tracker_suprimentos.json da obra ativa)
    const trackerJsonPath = path.join(supDir, 'dados_tracker_suprimentos.json');
    let requisicoes: RequisicaoCompra[] = [];
    if (fs.existsSync(trackerJsonPath)) {
      try {
        const trackerRaw = JSON.parse(fs.readFileSync(trackerJsonPath, 'utf-8'));
        if (Array.isArray(trackerRaw)) {
          requisicoes = trackerRaw.map((item: Record<string, string | number>) => ({
            id: String(item.ID_Requisicao || ''),
            tipo: String(item.Tipo_Suprimento || 'MATERIAL'),
            pacote: String(item.Pacote_Insumo_Equipamento || ''),
            centroCusto: String(item.Centro_Custo_CC || ''),
            disciplina: String(item.Disciplina || ''),
            dataDisparo: String(item.Data_Disparo || ''),
            dataCanteiro: String(item.Data_Canteiro || ''),
            leadTimeDias: String(item.Lead_Time_Dias || '15'),
            estagio: String(item.Estagio_Pipeline || '1. PENDENTE_SUPRIMENTOS'),
            semaforo: String(item.Semaforo || '🟢 NO PRAZO'),
            budget: parseFloat(String(item['Budget_R$'] || '0')) || 0,
          }));
        }
      } catch (jErr) {
        console.error('Erro ao ler tracker suprimentos:', jErr);
      }
    }

    // 3. Medições Quinzenais Reais da Obra Ativa
    const contratosDir = path.join(diretorio, '02_ORCAMENTO_BASE_E_CONTRATOS', 'CONTRATOS_EMPREITEIROS');
    const candCalendario = [
      path.join(contratosDir, `CALENDARIO_MEDICOES_QUINZENAIS_${obra}.md`),
      path.join(contratosDir, 'CALENDARIO_MEDICOES_QUINZENAIS.md'),
    ];
    const arqCalendario = candCalendario.find((c) => fs.existsSync(c));

    const medicoesQuinzenais: MedicaoEmpreiteiro[] = [];
    if (arqCalendario) {
      try {
        const mdText = fs.readFileSync(arqCalendario, 'utf-8');
        const linhas = mdText.split('\n');
        for (const linha of linhas) {
          const match = linha.match(/\|\s*\*\*(Q\d+)\*\*\s*\|\s*([^|]+)\|\s*`([^`]+)`\s*\|\s*\*\*([^*]+)\*\*/i);
          if (match) {
            const quinzena = match[1].trim();
            const mes = match[2].trim();
            medicoesQuinzenais.push({
              quinzena,
              mes,
              valorBruto: 0,
              retencao5: 0,
              valorLiquido: 0,
              status: 'A_MEDIR',
            });
          }
        }
      } catch (calErr) {
        console.error('Erro ao ler calendário de medições:', calErr);
      }
    }

    const hasData = fluxoMensal.length > 0 || requisicoes.length > 0 || medicoesQuinzenais.length > 0;

    return NextResponse.json({
      success: true,
      obra,
      modoDemo: false,
      status: hasData ? 'OK' : 'SEM_DADOS',
      proveniencia: {
        fluxoCsv: caminhoFluxo ? path.basename(caminhoFluxo) : null,
        trackerJson: fs.existsSync(trackerJsonPath) ? path.basename(trackerJsonPath) : null,
        calendarioMedicoes: arqCalendario ? path.basename(arqCalendario) : null,
      },
      kpis: {
        ...kpis,
        totalPacotesSuprimentos: requisicoes.length,
        materiaisRcCount: requisicoes.filter((r) => r.tipo === 'MATERIAL').length,
        equipamentosReCount: requisicoes.filter((r) => r.tipo === 'EQUIPAMENTO').length,
      },
      fluxoMensal,
      requisicoes,
      medicoesQuinzenais,
    });
  } catch (error: unknown) {
    if (error instanceof ErroObra) return NextResponse.json({ error: error.message }, { status: 400 });
    return NextResponse.json({ error: 'Falha ao ler financeiro.' }, { status: 500 });
  }
}
