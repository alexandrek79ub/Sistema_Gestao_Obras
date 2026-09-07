"use client";

import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { AlertTriangle, CheckCircle2, ArrowDownRight, ArrowUpRight } from 'lucide-react';

export default function DashboardPage() {
  const [evmData, setEvmData] = useState<any[]>([]);
  const [bac, setBac] = useState<number>(0);
  const [spi, setSpi] = useState<number>(1);
  const [cpi, setCpi] = useState<number>(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/evm')
      .then(res => res.json())
      .then(data => {
        if (data.semanas) setEvmData(data.semanas);
        if (data.bac) setBac(data.bac);
        if (data.spi) setSpi(data.spi);
        if (data.cpi) setCpi(data.cpi);
        setLoading(false);
      })
      .catch(err => {
        console.error('Erro ao buscar EVM', err);
        setLoading(false);
      });
  }, []);

  const formatCurrency = (val: number) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);
  };

  const getIndicatorColor = (val: number) => {
    if (val >= 1.0) return 'text-emerald-500';
    if (val >= 0.85) return 'text-amber-500';
    return 'text-red-500';
  };

  const getIndicatorBorder = (val: number) => {
    if (val >= 1.0) return 'border-emerald-500/30 shadow-[0_0_20px_rgba(16,185,129,0.1)]';
    if (val >= 0.85) return 'border-amber-500/30 shadow-[0_0_20px_rgba(245,158,11,0.1)]';
    return 'border-red-500/30 shadow-[0_0_20px_rgba(239,68,68,0.1)]';
  };

  const getIndicatorBg = (val: number) => {
    if (val >= 1.0) return 'bg-emerald-500';
    if (val >= 0.85) return 'bg-amber-500';
    return 'bg-red-500';
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Painel de Diretoria (EVM)</h1>
          <p className="text-zinc-400 mt-1">Análise de Valor Agregado em tempo real.</p>
        </div>
        <button className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium transition-colors">
          Exportar PDF
        </button>
      </div>

      {loading ? (
        <div className="p-8 text-center text-zinc-500">Carregando painel EVM...</div>
      ) : (
        <>
          {/* KPI CARDS */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-4 opacity-10">
                <CheckCircle2 className="w-16 h-16 text-zinc-500" />
              </div>
              <p className="text-sm font-medium text-zinc-400 uppercase tracking-wider mb-2">Orçamento Total (BAC)</p>
              <p className="text-3xl font-bold text-white">{formatCurrency(bac)}</p>
              <div className="mt-4 flex items-center text-sm text-zinc-400">
                <span>Sincronizado com Orçamento Base</span>
              </div>
            </div>

            <div className={`bg-zinc-900 border rounded-xl p-6 relative overflow-hidden ${getIndicatorBorder(cpi)}`}>
              <div className={`absolute top-0 right-0 w-2 h-full ${getIndicatorBg(cpi)}`}></div>
              <p className={`text-sm font-medium uppercase tracking-wider mb-2 ${getIndicatorColor(cpi).replace('500', '400')}`}>Índice de Custo (CPI)</p>
              <div className="flex items-end space-x-3">
                <p className={`text-4xl font-bold ${getIndicatorColor(cpi)}`}>{cpi.toFixed(2)}</p>
                <span className={`flex items-center text-sm font-medium mb-1 ${getIndicatorColor(cpi).replace('500', '400')}`}>
                  {cpi >= 1.0 ? <ArrowUpRight className="w-4 h-4 mr-1" /> : <ArrowDownRight className="w-4 h-4 mr-1" />} 
                  {cpi >= 1.0 ? 'Conforme' : 'Estouro'}
                </span>
              </div>
              <p className="mt-4 text-sm text-zinc-400">
                Obra gastando R$ {cpi > 0 ? (1/cpi).toFixed(2) : '0,00'} para cada R$ 1,00 produzido.
              </p>
            </div>

            <div className={`bg-zinc-900 border rounded-xl p-6 relative overflow-hidden ${getIndicatorBorder(spi)}`}>
              <div className={`absolute top-0 right-0 w-2 h-full ${getIndicatorBg(spi)}`}></div>
              <p className={`text-sm font-medium uppercase tracking-wider mb-2 ${getIndicatorColor(spi).replace('500', '400')}`}>Índice de Prazo (SPI)</p>
              <div className="flex items-end space-x-3">
                <p className={`text-4xl font-bold ${getIndicatorColor(spi)}`}>{spi.toFixed(2)}</p>
                <span className={`flex items-center text-sm font-medium mb-1 ${getIndicatorColor(spi).replace('500', '400')}`}>
                  {spi >= 1.0 ? <ArrowUpRight className="w-4 h-4 mr-1" /> : <ArrowDownRight className="w-4 h-4 mr-1" />} 
                  {spi >= 1.0 ? 'Adiantado' : 'Atraso'}
                </span>
              </div>
              <p className="mt-4 text-sm text-zinc-400">
                Ritmo atual aponta {spi < 1 ? Math.round((1 - spi)*100) : 0}% de atraso.
              </p>
            </div>
          </div>

          {/* CHART SECTION */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 bg-zinc-900 border border-zinc-800 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-6">Curva S (Planejado vs Realizado)</h3>
              <div className="h-80 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={evmData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorVP" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                    <XAxis dataKey="name" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `R$${Math.round(value/1000)}k`} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', color: '#fff' }}
                      itemStyle={{ color: '#fff' }}
                      formatter={(value: any) => formatCurrency(value)}
                    />
                    <Legend iconType="circle" wrapperStyle={{ paddingTop: '20px' }}/>
                    <Area type="monotone" dataKey="VP" name="Valor Planejado (Curva S)" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorVP)" />
                    <Line type="monotone" dataKey="CR" name="Custo Real (Gasto)" stroke="#ef4444" strokeWidth={3} dot={{ r: 4 }} />
                    <Line type="monotone" dataKey="VA" name="Valor Agregado (Medição)" stroke="#10b981" strokeWidth={3} dot={{ r: 4 }} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* AI ACTION PLAN */}
            <div className="bg-gradient-to-b from-zinc-900 to-zinc-950 border border-zinc-800 rounded-xl p-6 flex flex-col">
              <div className="flex items-center space-x-2 mb-6">
                <span className="flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-2 w-2 rounded-full bg-blue-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                </span>
                <h3 className="text-lg font-semibold text-white">IA: Plano de Ação</h3>
              </div>
              
              <div className="flex-1 space-y-4">
                {cpi < 1 && (
                  <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20">
                    <div className="flex items-start">
                      <AlertTriangle className="w-5 h-5 text-red-400 mt-0.5 mr-3 shrink-0" />
                      <div>
                        <h4 className="text-sm font-medium text-red-400 mb-1">Estouro de Custo (CPI &lt; 1)</h4>
                        <p className="text-xs text-zinc-400">O custo real ultrapassou o agregado. Sugestão: Revisar apontamento de desperdício em insumos críticos.</p>
                      </div>
                    </div>
                  </div>
                )}

                {spi < 1 && (
                  <div className="p-4 rounded-lg bg-amber-500/10 border border-amber-500/20">
                    <div className="flex items-start">
                      <AlertTriangle className="w-5 h-5 text-amber-400 mt-0.5 mr-3 shrink-0" />
                      <div>
                        <h4 className="text-sm font-medium text-amber-400 mb-1">Atraso Crítico (SPI &lt; 1)</h4>
                        <p className="text-xs text-zinc-400">O cronograma descolou da linha de base. Risco de impacto na Linha de Balanço. Sugestão: Autorizar +2 ajudantes para recuperar prazo.</p>
                      </div>
                    </div>
                  </div>
                )}
                
                {spi >= 1 && cpi >= 1 && (
                  <div className="p-4 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                    <div className="flex items-start">
                      <CheckCircle2 className="w-5 h-5 text-emerald-400 mt-0.5 mr-3 shrink-0" />
                      <div>
                        <h4 className="text-sm font-medium text-emerald-400 mb-1">Projeto Saudável</h4>
                        <p className="text-xs text-zinc-400">O empreendimento está dentro da meta de custo e prazo estipulada.</p>
                      </div>
                    </div>
                  </div>
                )}
                
                <button className="w-full mt-4 py-3 bg-white/5 hover:bg-white/10 text-white rounded-lg text-sm font-medium border border-white/10 transition-colors">
                  Disparar Cobrança (WhatsApp)
                </button>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
