"use client";

import React, { useEffect, useState } from 'react';
import { useObra } from '@/context/ObraContext';
import {
  TrendingUp,
  DollarSign,
  ShoppingCart,
  Receipt,
  ArrowDownRight,
  ArrowUpRight,
  Clock,
  ShieldCheck,
  CheckCircle2,
  Calendar,
  Layers,
  Filter
} from 'lucide-react';
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';

interface FluxoMensal {
  mes: string;
  entradas: number;
  saidas: number;
  saldoOperacional: number;
  saldoAcumulado: number;
}

interface RequisicaoCompra {
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

interface MedicaoEmpreiteiro {
  quinzena: string;
  mes: string;
  valorBruto: number;
  retencao5: number;
  valorLiquido: number;
  status: 'PAGO' | 'EM_ANALISE' | 'A_MEDIR';
}

interface FinanceiroResponse {
  success: boolean;
  obra: string;
  kpis: {
    faturamentoTotal: number;
    desembolsoTotal: number;
    margemContratual: number;
    margemPercent: number;
    capitalGiroMaximo: number;
    mesPicoExposicao: string;
    totalRetencaoCaucao: number;
    totalPacotesSuprimentos: number;
    materiaisRcCount: number;
    equipamentosReCount: number;
  };
  fluxoMensal: FluxoMensal[];
  requisicoes: RequisicaoCompra[];
  medicoesQuinzenais: MedicaoEmpreiteiro[];
}

export default function FinanceiroPage() {
  const { obraAtiva } = useObra();
  const [data, setData] = useState<FinanceiroResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'FLUXO' | 'SUPRIMENTOS' | 'MEDICOES'>('FLUXO');
  const [filtroTipo, setFiltroTipo] = useState<string>('TODOS');

  useEffect(() => {
    async function carregarFinanceiro() {
      setLoading(true);
      try {
        const res = await fetch(`/api/financeiro?obra=${encodeURIComponent(obraAtiva)}`);
        const json: FinanceiroResponse = await res.json();
        setData(json);
      } catch (err) {
        console.error('Erro ao carregar dados financeiros:', err);
      } finally {
        setLoading(false);
      }
    }
    carregarFinanceiro();
  }, [obraAtiva]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="flex flex-col items-center space-y-3">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm text-zinc-400">Carregando fluxo de caixa e suprimentos ({obraAtiva})...</p>
        </div>
      </div>
    );
  }

  const kpis = data?.kpis || {
    faturamentoTotal: 1660762.28,
    desembolsoTotal: 1556867.83,
    margemContratual: 103894.45,
    margemPercent: 6.26,
    capitalGiroMaximo: -180621.7,
    mesPicoExposicao: 'Mês 3',
    totalRetencaoCaucao: 83038.11,
    totalPacotesSuprimentos: 41,
    materiaisRcCount: 24,
    equipamentosReCount: 17,
  };

  const fluxo = data?.fluxoMensal || [];
  const requisicoes = data?.requisicoes || [];
  const medicoes = data?.medicoesQuinzenais || [];

  const requisicoesFiltradas = requisicoes.filter((r) => {
    if (filtroTipo === 'TODOS') return true;
    return r.tipo === filtroTipo;
  });

  const formatCurrency = (val: number) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);
  };

  return (
    <div className="space-y-6">
      {/* CABEÇALHO */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-3">
            <TrendingUp className="w-8 h-8 text-blue-500" />
            Fluxo de Caixa, Suprimentos & Medições
          </h1>
          <p className="text-zinc-400 mt-1">
            Modelagem financeira dos 7 meses, controle de compras em UCC e medições de empreiteiros com retenção de 5%.
          </p>
        </div>

        {/* NAVEGAÇÃO DE ABAS */}
        <div className="flex bg-zinc-900 border border-zinc-800 p-1 rounded-xl">
          <button
            onClick={() => setActiveTab('FLUXO')}
            className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'FLUXO' ? 'bg-blue-600 text-white shadow' : 'text-zinc-400 hover:text-white'
            }`}
          >
            Fluxo de Caixa
          </button>
          <button
            onClick={() => setActiveTab('SUPRIMENTOS')}
            className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'SUPRIMENTOS' ? 'bg-blue-600 text-white shadow' : 'text-zinc-400 hover:text-white'
            }`}
          >
            Suprimentos (RCs)
          </button>
          <button
            onClick={() => setActiveTab('MEDICOES')}
            className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'MEDICOES' ? 'bg-blue-600 text-white shadow' : 'text-zinc-400 hover:text-white'
            }`}
          >
            Medições (Retenção 5%)
          </button>
        </div>
      </div>

      {/* KPI CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Faturamento Total</p>
          <p className="text-xl font-bold text-white mt-1.5">{formatCurrency(kpis.faturamentoTotal)}</p>
          <p className="text-[11px] text-zinc-400 mt-1">Receita Líquida + Retenções</p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Desembolso Previsto</p>
          <p className="text-xl font-bold text-zinc-200 mt-1.5">{formatCurrency(kpis.desembolsoTotal)}</p>
          <p className="text-[11px] text-zinc-400 mt-1">Materiais, MO, Locações, BDI</p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Margem Bruta Final</p>
          <p className="text-xl font-bold text-emerald-400 mt-1.5">{formatCurrency(kpis.margemContratual)}</p>
          <p className="text-[11px] text-emerald-400 mt-1 font-semibold">{kpis.margemPercent.toFixed(2)}% de Margem</p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Pico Capital de Giro</p>
          <p className="text-xl font-bold text-rose-400 mt-1.5">{formatCurrency(kpis.capitalGiroMaximo)}</p>
          <p className="text-[11px] text-zinc-400 mt-1">Exposição máxima no {kpis.mesPicoExposicao}</p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Caução Retida (5%)</p>
          <p className="text-xl font-bold text-amber-400 mt-1.5">{formatCurrency(kpis.totalRetencaoCaucao)}</p>
          <p className="text-[11px] text-zinc-400 mt-1">Devolução no TRD (Mês 7)</p>
        </div>
      </div>

      {/* CONTEÚDO DA ABA SELECIONADA */}
      {activeTab === 'FLUXO' && (
        <div className="space-y-6">
          {/* GRÁFICO RECHARTS DE FLUXO DE CAIXA */}
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
            <h3 className="text-base font-semibold text-white mb-6 flex items-center justify-between">
              <span>Curva de Entradas, Saídas e Saldo Acumulado (7 Meses)</span>
              <span className="text-xs font-normal text-zinc-400">Valores em R$</span>
            </h3>

            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={fluxo} margin={{ top: 10, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                  <XAxis dataKey="mes" stroke="#71717a" fontSize={12} />
                  <YAxis
                    stroke="#71717a"
                    fontSize={12}
                    tickFormatter={(val) => `R$ ${(val / 1000).toFixed(0)}k`}
                  />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '8px' }}
                    formatter={(value: unknown) => [formatCurrency(Number(value) || 0), '']}
                  />
                  <Legend />
                  <Bar dataKey="entradas" name="Entradas (Faturamento)" fill="#10b981" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="saidas" name="Saídas (Desembolsos)" fill="#ef4444" radius={[4, 4, 0, 0]} />
                  <Line
                    type="monotone"
                    dataKey="saldoAcumulado"
                    name="Saldo Acumulado de Caixa"
                    stroke="#3b82f6"
                    strokeWidth={3}
                    dot={{ r: 5 }}
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* TABELA CONSOLIDADA DE FLUXO */}
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden">
            <div className="p-4 bg-zinc-950/60 border-b border-zinc-800">
              <h4 className="text-sm font-semibold text-white">Demonstrativo de Fluxo Financeiro Mês a Mês</h4>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-zinc-950/40 text-xs uppercase font-bold text-zinc-400 border-b border-zinc-800">
                  <tr>
                    <th className="py-3 px-4">Mês de Referência</th>
                    <th className="py-3 px-4 text-right">Entradas (Inflow)</th>
                    <th className="py-3 px-4 text-right">Saídas (Outflow)</th>
                    <th className="py-3 px-4 text-right">Saldo Operacional</th>
                    <th className="py-3 px-4 text-right">Saldo Acumulado</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-800/60 text-xs">
                  {fluxo.map((f, idx) => (
                    <tr key={idx} className="hover:bg-zinc-800/30 transition-colors">
                      <td className="py-3.5 px-4 font-semibold text-white">{f.mes}</td>
                      <td className="py-3.5 px-4 text-right font-mono text-emerald-400">
                        {formatCurrency(f.entradas)}
                      </td>
                      <td className="py-3.5 px-4 text-right font-mono text-rose-400">
                        {formatCurrency(f.saidas)}
                      </td>
                      <td className={`py-3.5 px-4 text-right font-mono font-bold ${
                        f.saldoOperacional >= 0 ? 'text-emerald-400' : 'text-rose-400'
                      }`}>
                        {formatCurrency(f.saldoOperacional)}
                      </td>
                      <td className={`py-3.5 px-4 text-right font-mono font-bold ${
                        f.saldoAcumulado >= 0 ? 'text-emerald-400' : 'text-rose-400'
                      }`}>
                        {formatCurrency(f.saldoAcumulado)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'SUPRIMENTOS' && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-zinc-900 border border-zinc-800 p-4 rounded-xl">
            <div className="flex items-center space-x-2">
              <ShoppingCart className="w-5 h-5 text-blue-400" />
              <h3 className="text-sm font-semibold text-white">
                Tracker Mestre de Suprimentos ({requisicoes.length} Pacotes Mapeados)
              </h3>
            </div>

            <div className="flex items-center space-x-2">
              <button
                onClick={() => setFiltroTipo('TODOS')}
                className={`px-3 py-1 text-xs rounded-md font-medium transition-colors ${
                  filtroTipo === 'TODOS' ? 'bg-blue-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:text-white'
                }`}
              >
                Todos ({requisicoes.length})
              </button>
              <button
                onClick={() => setFiltroTipo('MATERIAL')}
                className={`px-3 py-1 text-xs rounded-md font-medium transition-colors ${
                  filtroTipo === 'MATERIAL' ? 'bg-blue-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:text-white'
                }`}
              >
                Materiais ({kpis.materiaisRcCount})
              </button>
              <button
                onClick={() => setFiltroTipo('EQUIPAMENTO')}
                className={`px-3 py-1 text-xs rounded-md font-medium transition-colors ${
                  filtroTipo === 'EQUIPAMENTO' ? 'bg-blue-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:text-white'
                }`}
              >
                Locações ({kpis.equipamentosReCount})
              </button>
            </div>
          </div>

          <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden">
            <div className="overflow-x-auto max-h-[500px]">
              <table className="w-full text-left text-sm">
                <thead className="bg-zinc-950/80 text-xs uppercase font-bold text-zinc-400 border-b border-zinc-800 sticky top-0 backdrop-blur-md">
                  <tr>
                    <th className="py-3 px-4">ID</th>
                    <th className="py-3 px-4">Tipo</th>
                    <th className="py-3 px-4">Pacote / Insumo</th>
                    <th className="py-3 px-4">Centro Custo</th>
                    <th className="py-3 px-4">Lead Time</th>
                    <th className="py-3 px-4">Ponto de Pedido</th>
                    <th className="py-3 px-4">Entrega Canteiro</th>
                    <th className="py-3 px-4 text-right">Budget Previsto</th>
                    <th className="py-3 px-4 text-center">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-800/60 text-xs">
                  {requisicoesFiltradas.map((req) => (
                    <tr key={req.id} className="hover:bg-zinc-800/30 transition-colors">
                      <td className="py-3 px-4 font-mono font-bold text-blue-400">{req.id}</td>
                      <td className="py-3 px-4">
                        <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                          req.tipo === 'MATERIAL'
                            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                            : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                        }`}>
                          {req.tipo}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-medium text-white max-w-xs truncate">{req.pacote}</td>
                      <td className="py-3 px-4 text-zinc-400 font-mono">{req.centroCusto}</td>
                      <td className="py-3 px-4 text-zinc-300">{req.leadTimeDias} dias</td>
                      <td className="py-3 px-4 font-mono text-zinc-400">{req.dataDisparo}</td>
                      <td className="py-3 px-4 font-mono text-zinc-200">{req.dataCanteiro}</td>
                      <td className="py-3 px-4 text-right font-mono font-semibold text-zinc-200">
                        {formatCurrency(req.budget)}
                      </td>
                      <td className="py-3 px-4 text-center">
                        <span className="text-[11px] font-medium">{req.semaforo}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'MEDICOES' && (
        <div className="space-y-4">
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-3">
            <h3 className="text-base font-semibold text-white flex items-center gap-2">
              <Receipt className="w-5 h-5 text-amber-400" />
              Quadro Geral de Medições Quinzenais Evolutivas (12 Ciclos)
            </h3>
            <p className="text-xs text-zinc-400 leading-relaxed">
              Cada medição sofre retenção técnica compulsória de <strong className="text-white">5,0%</strong> em garantia. O montante caucionado (R$ 83.038,11) é liberado exclusivamente no Mês 7 após a assinatura do Termo de Recebimento Definitivo (TRD).
            </p>
          </div>

          <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-zinc-950/40 text-xs uppercase font-bold text-zinc-400 border-b border-zinc-800">
                  <tr>
                    <th className="py-3 px-4">Quinzena</th>
                    <th className="py-3 px-4">Mês de Referência</th>
                    <th className="py-3 px-4 text-right">Medição Bruta</th>
                    <th className="py-3 px-4 text-right">Retenção Técnica (-5%)</th>
                    <th className="py-3 px-4 text-right">Valor Líquido NF-e</th>
                    <th className="py-3 px-4 text-center">Status Pagamento</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-800/60 text-xs">
                  {medicoes.map((m) => (
                    <tr key={m.quinzena} className="hover:bg-zinc-800/30 transition-colors">
                      <td className="py-3.5 px-4 font-mono font-bold text-blue-400">{m.quinzena}</td>
                      <td className="py-3.5 px-4 font-medium text-white">{m.mes}</td>
                      <td className="py-3.5 px-4 text-right font-mono text-zinc-200">
                        {formatCurrency(m.valorBruto)}
                      </td>
                      <td className="py-3.5 px-4 text-right font-mono text-amber-400">
                        - {formatCurrency(m.retencao5)}
                      </td>
                      <td className="py-3.5 px-4 text-right font-mono font-bold text-emerald-400">
                        {formatCurrency(m.valorLiquido)}
                      </td>
                      <td className="py-3.5 px-4 text-center">
                        {m.status === 'PAGO' ? (
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                            Liberado & Pago
                          </span>
                        ) : m.status === 'EM_ANALISE' ? (
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">
                            Em Auditoria de Campo
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-zinc-800 text-zinc-400">
                            A Medir
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
