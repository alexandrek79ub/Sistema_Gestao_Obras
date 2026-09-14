"use client";

import { useEffect, useState } from 'react';
import { XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area, Line } from 'recharts';
import { AlertTriangle, CheckCircle2, ArrowDownRight, ArrowUpRight, HelpCircle, FileText } from 'lucide-react';
import { useObra } from '@/context/ObraContext';

interface EvmSemanaItem {
  semana: string;
  name?: string;
  data: string;
  VP?: number;
  CR?: number | null;
  VA?: number | null;
  spi?: number | null;
  cpi?: number | null;
  [key: string]: unknown;
}

interface ProvenienciaItem {
  origem?: string;
  dataAtualizacao?: string;
  detalhe?: string;
  orcamento?: string;
  cronograma?: string;
  [key: string]: unknown;
}

export default function DashboardPage() {
  const { obraAtiva } = useObra();
  const [evmData, setEvmData] = useState<EvmSemanaItem[]>([]);
  const [bac, setBac] = useState<number | null>(null);
  const [spi, setSpi] = useState<number | null>(null);
  const [cpi, setCpi] = useState<number | null>(null);
  const [modoDemo, setModoDemo] = useState<boolean>(false);
  const [statusEVM, setStatusEVM] = useState<string>('OK');
  const [mensagemEVM, setMensagemEVM] = useState<string | null>(null);
  const [proveniencia, setProveniencia] = useState<ProvenienciaItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!obraAtiva) {
      Promise.resolve().then(() => {
        setLoading(false);
        setError('Nenhuma obra disponível para consulta.');
      });
      return;
    }
    const controller = new AbortController();
    Promise.resolve().then(() => {
      setLoading(true);
      setError(null);
    });
    fetch(`/api/evm?obra=${encodeURIComponent(obraAtiva)}`, { signal: controller.signal })
      .then(async (res) => {
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Falha ao buscar EVM.');
        return data;
      })
      .then(data => {
        setEvmData(data.semanas || []);
        setBac(data.bac ?? null);
        setSpi(typeof data.spi === 'number' ? data.spi : null);
        setCpi(typeof data.cpi === 'number' ? data.cpi : null);
        setModoDemo(Boolean(data.modoDemo));
        setStatusEVM(data.status || 'OK');
        setMensagemEVM(data.mensagem || null);
        setProveniencia(data.proveniencia || null);
        setLoading(false);
      })
      .catch(err => {
        if (err.name !== 'AbortError') {
          console.error('Erro ao buscar EVM', err);
          setError(err instanceof Error ? err.message : 'Falha ao buscar EVM.');
          setLoading(false);
        }
      });
    return () => controller.abort();
  }, [obraAtiva]);

  const formatCurrency = (val: number | null | undefined) => {
    if (val === null || val === undefined) return '—';
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);
  };

  const getIndicatorColor = (val: number | null | undefined) => {
    if (val === null || val === undefined) return 'text-zinc-400';
    if (val >= 1.0) return 'text-emerald-500';
    if (val >= 0.85) return 'text-amber-500';
    return 'text-red-500';
  };

  const getIndicatorBorder = (val: number | null | undefined) => {
    if (val === null || val === undefined) return 'border-zinc-800 shadow-none';
    if (val >= 1.0) return 'border-emerald-500/30 shadow-[0_0_20px_rgba(16,185,129,0.1)]';
    if (val >= 0.85) return 'border-amber-500/30 shadow-[0_0_20px_rgba(245,158,11,0.1)]';
    return 'border-red-500/30 shadow-[0_0_20px_rgba(239,68,68,0.1)]';
  };

  const getIndicatorBg = (val: number | null | undefined) => {
    if (val === null || val === undefined) return 'bg-zinc-700';
    if (val >= 1.0) return 'bg-emerald-500';
    if (val >= 0.85) return 'bg-amber-500';
    return 'bg-red-500';
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Painel de Diretoria (EVM)</h1>
          <p className="text-zinc-400 mt-1">
            Análise de Valor Agregado oficial ({obraAtiva})
            {statusEVM ? <span className="ml-2 text-xs px-2 py-0.5 rounded bg-zinc-800 text-zinc-400 border border-zinc-700">Status: {statusEVM}</span> : null}
          </p>
        </div>
        <button className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium transition-colors">
          Exportar PDF
        </button>
      </div>

      {modoDemo && (
        <div className="p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl flex items-center gap-3 text-amber-300 text-sm">
          <AlertTriangle className="w-5 h-5 shrink-0 text-amber-400" />
          <div>
            <span className="font-bold">MODO DEMONSTRAÇÃO ATIVO:</span> Os indicadores exibidos nesta tela são simulados para demonstração e não representam medições reais desta obra.
          </div>
        </div>
      )}

      {loading ? (
        <div className="p-8 text-center text-zinc-500">Carregando painel EVM...</div>
      ) : error ? (
        <div className="p-8 text-center text-red-400">{error}</div>
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
                <span>{proveniencia?.orcamento ? `Fonte: ${proveniencia.orcamento}` : 'Sem orçamento base vinculado'}</span>
              </div>
            </div>

            <div className={`bg-zinc-900 border rounded-xl p-6 relative overflow-hidden ${getIndicatorBorder(cpi)}`}>
              <div className={`absolute top-0 right-0 w-2 h-full ${getIndicatorBg(cpi)}`}></div>
              <p className={`text-sm font-medium uppercase tracking-wider mb-2 ${getIndicatorColor(cpi).replace('500', '400')}`}>Índice de Custo (CPI)</p>
              <div className="flex items-end space-x-3">
                <p className={`text-4xl font-bold ${getIndicatorColor(cpi)}`}>{cpi !== null ? cpi.toFixed(2) : '—'}</p>
                <span className={`flex items-center text-sm font-medium mb-1 ${getIndicatorColor(cpi).replace('500', '400')}`}>
                  {cpi === null ? (
                    'Sem medição'
                  ) : cpi >= 1.0 ? (
                    <><ArrowUpRight className="w-4 h-4 mr-1" /> Conforme</>
                  ) : (
                    <><ArrowDownRight className="w-4 h-4 mr-1" /> Estouro</>
                  )}
                </span>
              </div>
              <p className="mt-4 text-sm text-zinc-400">
                {cpi !== null ? `Obra gastando R$ ${cpi > 0 ? (1/cpi).toFixed(2) : '0,00'} para cada R$ 1,00 produzido.` : 'Aguardando primeiro apontamento de custo real (CR).'}
              </p>
            </div>

            <div className={`bg-zinc-900 border rounded-xl p-6 relative overflow-hidden ${getIndicatorBorder(spi)}`}>
              <div className={`absolute top-0 right-0 w-2 h-full ${getIndicatorBg(spi)}`}></div>
              <p className={`text-sm font-medium uppercase tracking-wider mb-2 ${getIndicatorColor(spi).replace('500', '400')}`}>Índice de Prazo (SPI)</p>
              <div className="flex items-end space-x-3">
                <p className={`text-4xl font-bold ${getIndicatorColor(spi)}`}>{spi !== null ? spi.toFixed(2) : '—'}</p>
                <span className={`flex items-center text-sm font-medium mb-1 ${getIndicatorColor(spi).replace('500', '400')}`}>
                  {spi === null ? (
                    'Sem medição'
                  ) : spi >= 1.0 ? (
                    <><ArrowUpRight className="w-4 h-4 mr-1" /> Adiantado</>
                  ) : (
                    <><ArrowDownRight className="w-4 h-4 mr-1" /> Atraso</>
                  )}
                </span>
              </div>
              <p className="mt-4 text-sm text-zinc-400">
                {spi !== null ? (spi < 1 ? `Ritmo atual aponta ${Math.round((1 - spi)*100)}% de atraso.` : 'Dentro ou à frente do prazo planejado.') : 'Aguardando primeira medição física de avanço (VA).'}
              </p>
            </div>
          </div>

          {/* CHART SECTION */}
          {evmData.length === 0 ? (
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-8 text-center text-zinc-400">
              <FileText className="w-12 h-12 text-zinc-600 mx-auto mb-3" />
              <h3 className="text-lg font-medium text-white mb-1">Sem Dados de Curva S Registrados</h3>
              <p className="text-sm max-w-lg mx-auto text-zinc-500">
                {mensagemEVM || 'Execute os motores de cronograma e apontamento de campo para gerar as curvas oficiais desta obra.'}
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 bg-zinc-900 border border-zinc-800 rounded-xl p-6">
                <div className="flex justify-between items-center mb-6">
                  <h3 className="text-lg font-semibold text-white">Curva S (Planejado vs Realizado)</h3>
                  {proveniencia?.cronograma ? (
                    <span className="text-xs text-zinc-500 bg-zinc-800/60 px-2 py-1 rounded">Fonte: {proveniencia.cronograma}</span>
                  ) : null}
                </div>
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
                        formatter={(value) => formatCurrency(typeof value === 'number' ? value : Number(value) || 0)}
                      />
                      <Legend iconType="circle" wrapperStyle={{ paddingTop: '20px' }}/>
                      <Area type="monotone" dataKey="VP" name="Valor Planejado (Curva S)" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorVP)" />
                      {evmData.some(d => d.CR !== null && d.CR !== undefined) && (
                        <Line type="monotone" dataKey="CR" name="Custo Real (Gasto)" stroke="#ef4444" strokeWidth={3} dot={{ r: 4 }} />
                      )}
                      {evmData.some(d => d.VA !== null && d.VA !== undefined) && (
                        <Line type="monotone" dataKey="VA" name="Valor Agregado (Medição)" stroke="#10b981" strokeWidth={3} dot={{ r: 4 }} />
                      )}
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
                  {spi === null && cpi === null ? (
                    <div className="p-4 rounded-lg bg-zinc-800/40 border border-zinc-700/50">
                      <div className="flex items-start">
                        <HelpCircle className="w-5 h-5 text-zinc-400 mt-0.5 mr-3 shrink-0" />
                        <div>
                          <h4 className="text-sm font-medium text-zinc-300 mb-1">Aguardando Medições</h4>
                          <p className="text-xs text-zinc-400">O plano de ação será ativado automaticamente após o primeiro fechamento quinzenal de campo.</p>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <>
                      {cpi !== null && cpi < 1 && (
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

                      {spi !== null && spi < 1 && (
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
                      
                      {spi !== null && cpi !== null && spi >= 1 && cpi >= 1 && (
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
                    </>
                  )}
                  
                  <button className="w-full mt-4 py-3 bg-white/5 hover:bg-white/10 text-white rounded-lg text-sm font-medium border border-white/10 transition-colors">
                    Disparar Cobrança (WhatsApp)
                  </button>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
