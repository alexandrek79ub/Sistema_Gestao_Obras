import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';
import { parseCSV } from '@/lib/csvParser';

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
  const { searchParams } = new URL(request.url);
  const obra = searchParams.get('obra') || 'OBRA_TMULT';

  const basePath = process.env.OBRA_PATH
    ? process.env.OBRA_PATH.replace(/OBRA$/, obra)
    : path.resolve(process.cwd(), `../projetos/${obra}`);

  const supDir = path.join(basePath, '05_SUPRIMENTOS_E_FINANCEIRO');
  const fluxoCsvPath = path.join(supDir, `FLUXO_DE_CAIXA_${obra}.csv`);
  const fluxoCsvDefault = path.join(supDir, 'FLUXO_DE_CAIXA_TMULT.csv');
  const trackerJsonPath = path.join(supDir, 'dados_tracker_suprimentos.json');

  // 1. Dados do Gráfico de Fluxo de Caixa (Mensal M1 a M7)
  let fluxoMensal: FluxoMensal[] = [
    { mes: 'Mês 1', entradas: 0, saidas: 105467.76, saldoOperacional: -105467.76, saldoAcumulado: -105467.76 },
    { mes: 'Mês 2', entradas: 155269.92, saidas: 202190.46, saldoOperacional: -46920.54, saldoAcumulado: -152388.30 },
    { mes: 'Mês 3', entradas: 264001.06, saidas: 292234.46, saldoOperacional: -28233.40, saldoAcumulado: -180621.70 },
    { mes: 'Mês 4', entradas: 348054.46, saidas: 290517.52, saldoOperacional: 57536.94, saldoAcumulado: -123084.76 },
    { mes: 'Mês 5', entradas: 233397.32, saidas: 259914.12, saldoOperacional: -26516.80, saldoAcumulado: -149601.56 },
    { mes: 'Mês 6', entradas: 304396.06, saidas: 287957.98, saldoOperacional: 16438.08, saldoAcumulado: -133163.48 },
    { mes: 'Mês 7 (TRD)', entradas: 355643.46, saidas: 118585.53, saldoOperacional: 237057.93, saldoAcumulado: 103894.45 },
  ];

  // Tentativa de leitura dinâmica do CSV de fluxo se existir
  const caminhoFluxo = fs.existsSync(fluxoCsvPath) ? fluxoCsvPath : (fs.existsSync(fluxoCsvDefault) ? fluxoCsvDefault : null);
  if (caminhoFluxo) {
    try {
      const rows = parseCSV<Record<string, string>>(caminhoFluxo);
      const rowEntradas = rows.find(r => (r['Conta / Rubrica Financeira'] || '').includes('TOTAL DE ENTRADAS'));
      const rowSaidas = rows.find(r => (r['Conta / Rubrica Financeira'] || '').includes('TOTAL DE SAÍDAS'));
      const rowSaldoAcum = rows.find(r => (r['Conta / Rubrica Financeira'] || '').includes('Saldo de Caixa Acumulado'));

      if (rowEntradas && rowSaidas && rowSaldoAcum) {
        const meses = ['Mês 1', 'Mês 2', 'Mês 3', 'Mês 4', 'Mês 5', 'Mês 6', 'Mês 7'];
        const dinFluxo: FluxoMensal[] = [];
        for (const m of meses) {
          const ent = parseFloat(rowEntradas[m] || '0') || 0;
          const sai = parseFloat(rowSaidas[m] || '0') || 0;
          const acum = parseFloat(rowSaldoAcum[m] || '0') || 0;
          dinFluxo.push({
            mes: m,
            entradas: ent,
            saidas: sai,
            saldoOperacional: ent - sai,
            saldoAcumulado: acum,
          });
        }
        if (dinFluxo.length > 0) {
          fluxoMensal = dinFluxo;
        }
      }
    } catch (csvErr) {
      console.error('Erro ao ler CSV de fluxo:', csvErr);
    }
  }

  // 2. Requisições de Compras (dados_tracker_suprimentos.json)
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

  // 3. Medições Quinzenais Evolutivas (Padrão 12 quinzenas c/ Retenção 5%)
  const medicoesQuinzenais: MedicaoEmpreiteiro[] = [
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
    kpis: {
      faturamentoTotal: 1660762.28,
      desembolsoTotal: 1556867.83,
      margemContratual: 103894.45,
      margemPercent: 6.26,
      capitalGiroMaximo: -180621.70,
      mesPicoExposicao: 'Mês 3',
      totalRetencaoCaucao: 83038.11,
      totalPacotesSuprimentos: requisicoes.length || 41,
      materiaisRcCount: requisicoes.filter(r => r.tipo === 'MATERIAL').length || 24,
      equipamentosReCount: requisicoes.filter(r => r.tipo === 'EQUIPAMENTO').length || 17,
    },
    fluxoMensal,
    requisicoes,
    medicoesQuinzenais,
  });
}
