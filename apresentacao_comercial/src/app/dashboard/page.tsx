"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { AlertTriangle, CheckCircle2, ArrowDownRight, ArrowUpRight } from 'lucide-react';

const evmData = [
  { name: 'Semana 1', VP: 10000, CR: 9500, VA: 9000 },
  { name: 'Semana 2', VP: 25000, CR: 24000, VA: 22000 },
  { name: 'Semana 3', VP: 45000, CR: 48000, VA: 40000 }, // Descolamento na semana 3
  { name: 'Semana 4', VP: 65000 },
  { name: 'Semana 5', VP: 90000 },
  { name: 'Semana 6', VP: 120000 }
];

export default function DashboardPage() {
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

      {/* KPI CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-10">
            <CheckCircle2 className="w-16 h-16 text-zinc-500" />
          </div>
          <p className="text-sm font-medium text-zinc-400 uppercase tracking-wider mb-2">Orçamento Total (BAC)</p>
          <p className="text-3xl font-bold text-white">R$ 120.000</p>
          <div className="mt-4 flex items-center text-sm text-zinc-400">
            <span>Baseline Travada (15/10/2026)</span>
          </div>
        </div>

        <div className="bg-zinc-900 border border-red-500/30 rounded-xl p-6 relative overflow-hidden shadow-[0_0_20px_rgba(239,68,68,0.1)]">
          <div className="absolute top-0 right-0 w-2 h-full bg-red-500"></div>
          <p className="text-sm font-medium text-red-400 uppercase tracking-wider mb-2">Índice de Custo (CPI)</p>
          <div className="flex items-end space-x-3">
            <p className="text-4xl font-bold text-red-500">0.83</p>
            <span className="flex items-center text-red-400 text-sm font-medium mb-1">
              <ArrowDownRight className="w-4 h-4 mr-1" /> Estouro
            </span>
          </div>
          <p className="mt-4 text-sm text-zinc-400">Obra gastando R$ 1,20 para cada R$ 1,00 produzido.</p>
        </div>

        <div className="bg-zinc-900 border border-amber-500/30 rounded-xl p-6 relative overflow-hidden shadow-[0_0_20px_rgba(245,158,11,0.1)]">
          <div className="absolute top-0 right-0 w-2 h-full bg-amber-500"></div>
          <p className="text-sm font-medium text-amber-400 uppercase tracking-wider mb-2">Índice de Prazo (SPI)</p>
          <div className="flex items-end space-x-3">
            <p className="text-4xl font-bold text-amber-500">0.88</p>
            <span className="flex items-center text-amber-400 text-sm font-medium mb-1">
              <ArrowDownRight className="w-4 h-4 mr-1" /> Atraso
            </span>
          </div>
          <p className="mt-4 text-sm text-zinc-400">Ritmo atual aponta 12% de atraso na entrega.</p>
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
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `R$${value/1000}k`} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
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
            <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20">
              <div className="flex items-start">
                <AlertTriangle className="w-5 h-5 text-red-400 mt-0.5 mr-3 shrink-0" />
                <div>
                  <h4 className="text-sm font-medium text-red-400 mb-1">Estouro na Alvenaria</h4>
                  <p className="text-xs text-zinc-400">O custo real (CR) ultrapassou o agregado (VA) em R$ 8.000 na Semana 3. Causa raiz: Desperdício de UCC detectado nos relatórios de suprimentos.</p>
                </div>
              </div>
            </div>

            <div className="p-4 rounded-lg bg-amber-500/10 border border-amber-500/20">
              <div className="flex items-start">
                <AlertTriangle className="w-5 h-5 text-amber-400 mt-0.5 mr-3 shrink-0" />
                <div>
                  <h4 className="text-sm font-medium text-amber-400 mb-1">Atraso de Estrutura</h4>
                  <p className="text-xs text-zinc-400">O Empreiteiro João está 2 dias atrasado no Pavimento 02. Risco de chocar com a equipe de Alvenaria (Linha de Balanço).</p>
                </div>
              </div>
            </div>
            
            <button className="w-full mt-4 py-3 bg-white/5 hover:bg-white/10 text-white rounded-lg text-sm font-medium border border-white/10 transition-colors">
              Disparar Cobrança (WhatsApp)
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
