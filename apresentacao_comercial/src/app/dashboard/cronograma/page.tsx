"use client";

import React, { useState, useEffect } from 'react';
import LinhaDeBalanco from '@/components/LinhaDeBalanco';
import TremDeProducaoLean from '@/components/TremDeProducaoLean';
import GanttExecutivo from '@/components/GanttExecutivo';
import { useObra } from '@/context/ObraContext';
import { 
  Calendar, 
  Layers, 
  GitCommit, 
  TrendingUp, 
  AlertTriangle, 
  ExternalLink,
  ShieldCheck,
  Clock,
  CheckCircle2,
  Users,
  Truck,
  PackageCheck,
  Filter,
  Info,
  X,
  Train,
  Table as TableIcon
} from 'lucide-react';

interface AtividadeCPM {
  id: string;
  duracao_dias: number;
  es_inicio_mais_cedo?: number;
  ef_fim_mais_cedo?: number;
  ls_inicio_mais_tarde?: number;
  lf_fim_mais_tarde?: number;
  folga_dias?: number;
  critica?: boolean;
}

interface CurvaSItem {
  mes: string;
  fisicoPlan: number;
  financeiroPlan: number;
  valorMes: number;
}

interface LoteCurtoPrazo {
  codLote: string;
  semana: string;
  diasSemana?: string;
  dataInicio?: string;
  dataFim?: string;
  etapaZona?: string;
  vagaoEsteira?: string;
  setor: string;
  servico: string;
  metaFisica: string;
  duracaoDias: number;
  equipePrevista: string;
  headcount: number;
  equipamentos: string;
  materiaisUcc: string;
  rupMeta: string;
  status: string;
  rdoVinculado?: string;
}

interface HistogramaItem {
  mes: string;
  producao: number;
  gestaoApoio: number;
  total: number;
  foco: string;
}

export default function CronogramaPage() {
  const { obraAtiva } = useObra();
  const [activeTab, setActiveTab] = useState<'lob' | 'curto_prazo' | 'cpm' | 'curva_s'>('curto_prazo');
  const [cpmAtividades, setCpmAtividades] = useState<AtividadeCPM[]>([]);
  const [tarefas, setTarefas] = useState<any[]>([]);
  const [curvaS, setCurvaS] = useState<CurvaSItem[]>([]);
  const [lotes, setLotes] = useState<LoteCurtoPrazo[]>([]);
  const [histogramaMensal, setHistogramaMensal] = useState<HistogramaItem[]>([]);
  const [mostrarHistogramaModal, setMostrarHistogramaModal] = useState(false);
  const [filtroSemana, setFiltroSemana] = useState<string>('Semana 01');
  const [modoCurtoPrazo, setModoCurtoPrazo] = useState<'trem' | 'tabela'>('trem');
  const [metaGlobal, setMetaGlobal] = useState<any>({
    diasCorridos: 180,
    semanas: 26,
    valorTurnkey: 1660762.28,
    caminhoCriticoDias: 178
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/cronograma?obra=${encodeURIComponent(obraAtiva)}`)
      .then(res => res.json())
      .then(data => {
        if (data.cpm) setCpmAtividades(data.cpm);
        if (data.tarefas) setTarefas(data.tarefas);
        if (data.curvaS) setCurvaS(data.curvaS);
        if (data.lotesCurtoPrazo) setLotes(data.lotesCurtoPrazo);
        if (data.histogramaMensal) setHistogramaMensal(data.histogramaMensal);
        if (data.metaGlobal) setMetaGlobal(data.metaGlobal);
        setLoading(false);
      })
      .catch(err => {
        console.error('Erro ao carregar dados complementares do cronograma', err);
        setLoading(false);
      });
  }, [obraAtiva]);

  const formatDescricaoCPM = (id: string) => {
    return id.replace(/^[A-Z0-9]+_/, '').replace(/_/g, ' ');
  };

  const semanasDisponiveis = Array.from(new Set(lotes.map(l => l.semana))).filter(Boolean);
  const lotesFiltrados = filtroSemana === 'TODAS' ? lotes : lotes.filter(l => l.semana === filtroSemana);

  // Diagnóstico de balanceamento semanal
  const semanaNum = filtroSemana === 'TODAS' ? null : parseInt(filtroSemana.replace(/\D/g, ''), 10);
  let mesRef = 'Mês 1 (Sem 01-04)';
  let tetoHistograma = 9;
  let totalHeadcountMes = 14;
  let focoFase = 'Fundações e Canteiro';
  if (semanaNum) {
    if (semanaNum <= 4) { mesRef = 'Mês 1 (Sem 01-04)'; tetoHistograma = 9; totalHeadcountMes = 14; focoFase = 'Canteiro, Escavação e Sapatas S1 a S32'; }
    else if (semanaNum <= 8) { mesRef = 'Mês 2 (Sem 05-08)'; tetoHistograma = 14; totalHeadcountMes = 19; focoFase = 'Baldrames VB1-19, Pilares P1-24 e Laje H12'; }
    else if (semanaNum <= 12) { mesRef = 'Mês 3 (Sem 09-12)'; tetoHistograma = 15; totalHeadcountMes = 20; focoFase = 'Alvenarias de Bloco e Cobertura PIR'; }
    else if (semanaNum <= 16) { mesRef = 'Mês 4 (Sem 13-16)'; tetoHistograma = 12; totalHeadcountMes = 17; focoFase = 'Reboco Mecanizado e Contrapisos'; }
    else if (semanaNum <= 20) { mesRef = 'Mês 5 (Sem 17-20)'; tetoHistograma = 11; totalHeadcountMes = 16; focoFase = 'Porcelanatos, Caixilhos e Redes Climatização'; }
    else { mesRef = 'Mês 6 (Sem 21-26)'; tetoHistograma = 11; totalHeadcountMes = 16; focoFase = 'Pintura Final, Aparelhos HVAC e Limpeza Fina'; }
  }

  // Efetivo de pico diário real da semana (devido à execução sequencial dos lotes de 2d cada)
  const maxHeadcountDiario = lotesFiltrados.length > 0 
    ? Math.max(...lotesFiltrados.map(l => l.headcount || 0)) 
    : 0;
  
  // Total de dias cobertos na semana e soma nominal
  const diasCobertos = lotesFiltrados.reduce((acc, l) => acc + (l.duracaoDias || 0), 0);
  const somaNominalLotes = lotesFiltrados.reduce((acc, l) => acc + (l.headcount || 0), 0);

  return (
    <div className="space-y-6">
      {/* HEADER EXECUTIVO */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-3">
            <Calendar className="w-8 h-8 text-blue-500" />
            Planejamento & Cronograma Integrado
          </h1>
          <p className="text-zinc-400 mt-1">
            Gestão 5D em 3 níveis: <span className="text-zinc-200 font-semibold">Longo Prazo</span> (Linha de Balanço & CPM), <span className="text-zinc-200 font-semibold">Médio Prazo</span> (Lookahead 4-6 sem) e <span className="text-zinc-200 font-semibold">Curto Prazo</span> (Lotes de Produção com Recursos Previstos).
          </p>
        </div>

        <a 
          href={`/projetos/${obraAtiva}/03_PLANEJAMENTO_E_CRONOGRAMA/CRONOGRAMA_DASHBOARD_INTERATIVO.html`}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 border border-blue-500/40 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          <ExternalLink className="w-4 h-4" />
          Dashboard HTML Plotly
        </a>
      </div>

      {/* CARDS DE KPIS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500 uppercase font-bold tracking-wider">Prazo Global</span>
            <Clock className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-1">{metaGlobal.diasCorridos} Dias</div>
          <span className="text-xs text-zinc-400">26 Semanas / 6 Meses Corridos</span>
        </div>

        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500 uppercase font-bold tracking-wider">Caminho Crítico (CPM)</span>
            <AlertTriangle className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-2xl font-bold text-rose-400 mt-1">{metaGlobal.caminhoCriticoDias} Dias</div>
          <span className="text-xs text-zinc-400">Folga Zero em 26 Macroatividades</span>
        </div>

        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500 uppercase font-bold tracking-wider">Lotes Programados</span>
            <Layers className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{lotes.length} Lotes</div>
          <span className="text-xs text-zinc-400">Frentes Enxutas de 1 a 2 Dias</span>
        </div>

        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500 uppercase font-bold tracking-wider">Controle Operacional</span>
            <ShieldCheck className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-amber-400 mt-1">Previsto × RDO</div>
          <span className="text-xs text-zinc-400">Auditoria Diária de Efetivo & Metas</span>
        </div>
      </div>

      {/* TABS SELECTOR */}
      <div className="flex border-b border-zinc-800 gap-2 overflow-x-auto">
        <button
          onClick={() => setActiveTab('curto_prazo')}
          className={`pb-3 px-4 text-sm font-semibold border-b-2 transition-colors flex items-center gap-2 whitespace-nowrap ${
            activeTab === 'curto_prazo' 
              ? 'border-emerald-500 text-emerald-400' 
              : 'border-transparent text-zinc-400 hover:text-zinc-200'
          }`}
        >
          <PackageCheck className="w-4 h-4" />
          Curto Prazo: Lotes & Recursos Previstos (Plano Semanal)
        </button>

        <button
          onClick={() => setActiveTab('lob')}
          className={`pb-3 px-4 text-sm font-semibold border-b-2 transition-colors flex items-center gap-2 whitespace-nowrap ${
            activeTab === 'lob' 
              ? 'border-blue-500 text-blue-400' 
              : 'border-transparent text-zinc-400 hover:text-zinc-200'
          }`}
        >
          <Layers className="w-4 h-4" />
          Longo Prazo: Linha de Balanço (LOB 180 Dias)
          <span className="text-[10px] bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 px-2 py-0.5 rounded-full font-bold uppercase tracking-wider animate-pulse">
            Interativo • Editar CSV
          </span>
        </button>

        <button
          onClick={() => setActiveTab('cpm')}
          className={`pb-3 px-4 text-sm font-semibold border-b-2 transition-colors flex items-center gap-2 whitespace-nowrap ${
            activeTab === 'cpm' 
              ? 'border-rose-500 text-rose-400' 
              : 'border-transparent text-zinc-400 hover:text-zinc-200'
          }`}
        >
          <GitCommit className="w-4 h-4" />
          Gráfico de Gantt & Caminho Crítico (CPM)
          <span className="text-[10px] bg-rose-500/20 text-rose-400 border border-rose-500/40 px-2 py-0.5 rounded-full font-bold uppercase tracking-wider animate-pulse">
            Executivo
          </span>
        </button>

        <button
          onClick={() => setActiveTab('curva_s')}
          className={`pb-3 px-4 text-sm font-semibold border-b-2 transition-colors flex items-center gap-2 whitespace-nowrap ${
            activeTab === 'curva_s' 
              ? 'border-blue-500 text-blue-400' 
              : 'border-transparent text-zinc-400 hover:text-zinc-200'
          }`}
        >
          <TrendingUp className="w-4 h-4" />
          Curva S Físico-Financeira
        </button>
      </div>

      {/* ABA CURTO PRAZO: LOTES E RECURSOS PREVISTOS (O PREVISTO QUE ENTRA NO CAMPO) */}
      {activeTab === 'curto_prazo' && (
        <div className="space-y-6">
          {/* BARRA SUPERIOR DE MODO (TREM vs TABELA) & HISTOGRAMA */}
          <div className="bg-zinc-900/90 border border-zinc-800 rounded-2xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg backdrop-blur-sm">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500/20 to-emerald-500/20 border border-amber-500/30 flex items-center justify-center text-amber-400">
                <Train className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  Programação de Curto Prazo (Linha de Produção Lean)
                  <span className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 px-2 py-0.5 rounded-full text-[10px] font-bold">
                    TAKT TIME 3 DIAS
                  </span>
                </h3>
                <p className="text-xs text-zinc-400">
                  Visualização da esteira contínua em formato vagão ou tabela analítica detalhada de lotes.
                </p>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              {/* SELETOR DE MODO: TREM vs TABELA */}
              <div className="bg-zinc-950 p-1 rounded-xl border border-zinc-800 flex items-center">
                <button
                  onClick={() => setModoCurtoPrazo('trem')}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-2 ${
                    modoCurtoPrazo === 'trem'
                      ? 'bg-amber-500 text-black shadow-lg shadow-amber-500/20'
                      : 'text-zinc-400 hover:text-white'
                  }`}
                >
                  <Train className="w-4 h-4" />
                  Trem de Produção (Vagões)
                </button>
                <button
                  onClick={() => setModoCurtoPrazo('tabela')}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-2 ${
                    modoCurtoPrazo === 'tabela'
                      ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20'
                      : 'text-zinc-400 hover:text-white'
                  }`}
                >
                  <TableIcon className="w-4 h-4" />
                  Tabela Analítica de Lotes
                </button>
              </div>

              <button
                onClick={() => setMostrarHistogramaModal(true)}
                className="inline-flex items-center gap-1.5 bg-blue-950/60 hover:bg-blue-900/60 text-blue-300 border border-blue-800/60 px-3.5 py-2 rounded-xl text-xs font-semibold transition-colors"
              >
                <Users className="w-4 h-4" />
                Histograma EAP 1.0
              </button>
            </div>
          </div>

          {/* MODO 1: TREM DE PRODUÇÃO LEAN (VAGÕES CONTÍNUOS COM DATAS NO RODAPÉ) */}
          {modoCurtoPrazo === 'trem' && (
            <TremDeProducaoLean lotes={lotes} />
          )}

          {/* MODO 2: TABELA ANALÍTICA DE LOTES */}
          {modoCurtoPrazo === 'tabela' && (
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                <div>
                  <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                    Detalhamento dos Lotes e Recursos Previstos
                  </h3>
                  <p className="text-sm text-zinc-400 mt-0.5">
                    Estes são os lotes calculados pelo sistema que montam as frentes de trabalho. O RDO aponta o real contra este plano.
                  </p>
                </div>

                <div className="flex items-center gap-2 bg-zinc-950 px-3 py-1.5 rounded-lg border border-zinc-800">
                  <Filter className="w-4 h-4 text-zinc-400" />
                  <span className="text-xs text-zinc-400 font-medium">Semana:</span>
                  <select
                    value={filtroSemana}
                    onChange={(e) => setFiltroSemana(e.target.value)}
                    className="bg-transparent text-xs text-white font-semibold focus:outline-none cursor-pointer"
                  >
                    <option value="TODAS" className="bg-zinc-900 text-white">Todas as Semanas (Visão Geral)</option>
                    {semanasDisponiveis.map((sem) => (
                      <option key={sem} value={sem} className="bg-zinc-900 text-white">{sem}</option>
                    ))}
                  </select>
                </div>
              </div>

            {/* DIAGNÓSTICO DE BALANCEAMENTO & NIVELAMENTO DE EFETIVO (LEAN CONSTRUCTION) */}
            <div className="bg-gradient-to-r from-blue-950/40 via-zinc-900 to-emerald-950/30 border border-blue-800/40 rounded-xl p-4 mb-6">
              <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-blue-500/20 border border-blue-500/40 flex items-center justify-center shrink-0">
                    <Users className="w-5 h-5 text-blue-400" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h4 className="text-sm font-bold text-white tracking-wider">
                        {filtroSemana === 'TODAS' 
                          ? 'Diagnóstico Geral: 52 Lotes Nivelados ao Longo de 26 Semanas' 
                          : `Diagnóstico de Balanceamento & Nivelamento — ${filtroSemana}`}
                      </h4>
                      <span className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 px-2 py-0.5 rounded text-[10px] font-bold">
                        100% NIVELADO
                      </span>
                    </div>
                    <p className="text-xs text-zinc-400 mt-0.5 max-w-2xl">
                      {filtroSemana === 'TODAS'
                        ? 'Todas as frentes de trabalho foram distribuídas sequencialmente (Seg-Ter, Qua-Qui, Sex-Sáb), respeitando o teto de contratação mensal do Histograma.'
                        : `Lotes sequenciais nos 6 dias úteis. A mesma equipe transita entre as frentes (${focoFase}), garantindo fluxo contínuo sem acúmulo de pessoas nem dias ociosos.`}
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 w-full lg:w-auto shrink-0">
                  <div className="bg-zinc-950/70 border border-zinc-800 rounded-lg px-3 py-2 text-center">
                    <span className="text-[10px] text-zinc-500 uppercase font-semibold block">Efetivo Real Diário</span>
                    <span className="text-sm font-bold text-emerald-400">
                      {filtroSemana === 'TODAS' ? '8 a 14 Operários' : `${maxHeadcountDiario} Operários`}
                    </span>
                    <span className="text-[9px] text-zinc-400 block">
                      {filtroSemana === 'TODAS' ? 'Faixa diária de pico' : `Soma nominal: ${somaNominalLotes}`}
                    </span>
                  </div>

                  <div className="bg-zinc-950/70 border border-zinc-800 rounded-lg px-3 py-2 text-center">
                    <span className="text-[10px] text-zinc-500 uppercase font-semibold block">Teto Histograma EAP</span>
                    <span className="text-sm font-bold text-blue-400">
                      {filtroSemana === 'TODAS' ? '14 a 20 Total' : `${tetoHistograma} Prod. / ${totalHeadcountMes} Total`}
                    </span>
                    <span className="text-[9px] text-zinc-400 block">{mesRef}</span>
                  </div>

                  <div className="bg-zinc-950/70 border border-zinc-800 rounded-lg px-3 py-2 text-center">
                    <span className="text-[10px] text-zinc-500 uppercase font-semibold block">Dias Programados</span>
                    <span className="text-sm font-bold text-amber-400">
                      {filtroSemana === 'TODAS' ? '26 Semanas (100%)' : `${diasCobertos} de 6 Dias`}
                    </span>
                    <span className="text-[9px] text-zinc-400 block">Segunda a Sábado</span>
                  </div>

                  <div className="bg-zinc-950/70 border border-zinc-800 rounded-lg px-3 py-2 text-center">
                    <span className="text-[10px] text-zinc-500 uppercase font-semibold block">Ociosidade da Equipe</span>
                    <span className="text-sm font-bold text-emerald-400">0% Ociosa</span>
                    <span className="text-[9px] text-zinc-400 block">Fluxo Contínuo Lean</span>
                  </div>
                </div>
              </div>
            </div>

            {/* TABELA DE LOTES DE CURTO PRAZO */}
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-zinc-300">
                <thead className="text-xs uppercase bg-zinc-950/80 text-zinc-400 border-b border-zinc-800">
                  <tr>
                    <th className="py-3 px-4">Lote / Semana</th>
                    <th className="py-3 px-4">Programação (Dias)</th>
                    <th className="py-3 px-4">Etapa (Zona Takt)</th>
                    <th className="py-3 px-4">Vagão & Serviço Programado (Esteira Lean)</th>
                    <th className="py-3 px-4">Recursos Humanos Previstos</th>
                    <th className="py-3 px-4">Equipamentos Previstos</th>
                    <th className="py-3 px-4">Insumos UCC Requisitados</th>
                    <th className="py-3 px-4 text-center">Status / RDO</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-800/60">
                  {lotesFiltrados.length === 0 ? (
                    <tr>
                      <td colSpan={8} className="text-center py-8 text-zinc-500">
                        Nenhum lote encontrado para esta semana.
                      </td>
                    </tr>
                  ) : (
                    lotesFiltrados.map((lote) => {
                      const isConcluido = lote.status === 'CONCLUIDO';
                      const isAndamento = lote.status === 'EM_ANDAMENTO';
                      return (
                        <tr key={lote.codLote} className="hover:bg-zinc-800/40 transition-colors">
                          <td className="py-3 px-4 whitespace-nowrap">
                            <span className="font-mono text-xs font-bold text-emerald-400 block">{lote.codLote}</span>
                            <span className="text-[11px] text-zinc-500">{lote.semana} ({lote.duracaoDias}d)</span>
                          </td>
                          <td className="py-3 px-4 whitespace-nowrap">
                            <span className="inline-block bg-blue-950/60 text-blue-300 border border-blue-800/50 px-2 py-1 rounded text-xs font-medium">
                              {lote.diasSemana || `Dias 1 a ${lote.duracaoDias}`}
                            </span>
                            {lote.dataInicio && lote.dataFim && (
                              <span className="block text-[11px] text-amber-400 font-mono mt-1">
                                {lote.dataInicio} a {lote.dataFim}
                              </span>
                            )}
                          </td>
                          <td className="py-3 px-4 font-medium text-xs whitespace-nowrap">
                            <span className="inline-block bg-zinc-800/80 text-zinc-200 border border-zinc-700 px-2 py-1 rounded font-semibold">
                              {lote.etapaZona || lote.setor}
                            </span>
                          </td>
                          <td className="py-3 px-4">
                            {lote.vagaoEsteira && (
                              <span className="inline-block bg-purple-950/60 text-purple-300 border border-purple-800/50 px-2 py-0.5 rounded text-[10px] font-mono font-semibold mb-1">
                                {lote.vagaoEsteira}
                              </span>
                            )}
                            <div className="font-semibold text-zinc-100 text-xs">{lote.servico}</div>
                            <div className="text-[11px] text-emerald-400/90 font-mono mt-0.5">Meta: {lote.metaFisica}</div>
                            <div className="text-[10px] text-zinc-500 font-mono">RUP Meta: {lote.rupMeta}</div>
                          </td>
                          <td className="py-3 px-4">
                            <div className="flex items-center gap-1.5 text-xs text-zinc-200">
                              <Users className="w-3.5 h-3.5 text-blue-400 shrink-0" />
                              <span>{lote.equipePrevista}</span>
                            </div>
                            <div className="flex items-center gap-2 mt-0.5">
                              <span className="text-[10px] text-emerald-400 font-mono font-semibold">{lote.headcount} operários alocados</span>
                              <span className="text-[9px] text-zinc-500 font-mono">• Fluxo Contínuo</span>
                            </div>
                          </td>
                          <td className="py-3 px-4">
                            <div className="flex items-center gap-1.5 text-xs text-zinc-300">
                              <Truck className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                              <span className="truncate max-w-[160px]" title={lote.equipamentos}>{lote.equipamentos}</span>
                            </div>
                          </td>
                          <td className="py-3 px-4 text-xs text-zinc-400 max-w-[180px]">
                            <span className="truncate block" title={lote.materiaisUcc}>{lote.materiaisUcc}</span>
                          </td>
                          <td className="py-3 px-4 text-center whitespace-nowrap">
                            {isConcluido ? (
                              <div className="inline-flex flex-col items-center">
                                <span className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 px-2 py-0.5 rounded text-[11px] font-bold">
                                  CONCLUÍDO
                                </span>
                                {lote.rdoVinculado && (
                                  <a 
                                    href="/dashboard/rdo" 
                                    className="text-[10px] text-blue-400 hover:underline font-mono mt-1"
                                  >
                                    Ver no {lote.rdoVinculado}
                                  </a>
                                )}
                              </div>
                            ) : isAndamento ? (
                              <div className="inline-flex flex-col items-center">
                                <span className="bg-blue-500/20 text-blue-400 border border-blue-500/40 px-2 py-0.5 rounded text-[11px] font-bold animate-pulse">
                                  EM ANDAMENTO
                                </span>
                                {lote.rdoVinculado && (
                                  <a 
                                    href="/dashboard/rdo" 
                                    className="text-[10px] text-blue-400 hover:underline font-mono mt-1"
                                  >
                                    Ver no {lote.rdoVinculado}
                                  </a>
                                )}
                              </div>
                            ) : (
                              <span className="bg-zinc-800 text-zinc-400 border border-zinc-700 px-2 py-0.5 rounded text-[11px] font-semibold">
                                PROGRAMADO
                              </span>
                            )}
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>
          )}

          {/* MODAL / PAINEL DO HISTOGRAMA MENSAL DE MÃO DE OBRA (EAP 1.0 / RH) */}
          {mostrarHistogramaModal && (
            <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
              <div className="bg-zinc-900 border border-zinc-700 rounded-2xl max-w-3xl w-full p-6 shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-200">
                <div className="flex items-center justify-between border-b border-zinc-800 pb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-blue-500/20 border border-blue-500/40 flex items-center justify-center">
                      <Users className="w-5 h-5 text-blue-400" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-white">Histograma Oficial de Mão de Obra — EAP 1.0 & RH</h3>
                      <p className="text-xs text-zinc-400">Headcount mensal planejado vs capacidade de alojamento, transporte e vivência</p>
                    </div>
                  </div>
                  <button 
                    onClick={() => setMostrarHistogramaModal(false)}
                    className="p-1.5 text-zinc-400 hover:text-white rounded-lg hover:bg-zinc-800 transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs text-zinc-300">
                    <thead className="uppercase bg-zinc-950 text-zinc-400 border-b border-zinc-800">
                      <tr>
                        <th className="py-2.5 px-3">Mês / Período</th>
                        <th className="py-2.5 px-3 text-center">Produção Direta</th>
                        <th className="py-2.5 px-3 text-center">Gestão & SST</th>
                        <th className="py-2.5 px-3 text-center font-bold text-white">Total Canteiro</th>
                        <th className="py-2.5 px-3">Frente Crítica / Foco Principal</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-zinc-800/60">
                      {histogramaMensal.map((h, idx) => (
                        <tr key={idx} className="hover:bg-zinc-800/40">
                          <td className="py-2.5 px-3 font-semibold text-white whitespace-nowrap">{h.mes}</td>
                          <td className="py-2.5 px-3 text-center font-mono text-emerald-400 font-bold">{h.producao} operários</td>
                          <td className="py-2.5 px-3 text-center font-mono text-zinc-400">{h.gestaoApoio} profissionais</td>
                          <td className="py-2.5 px-3 text-center font-mono text-blue-400 font-bold bg-blue-950/20">{h.total} Headcount</td>
                          <td className="py-2.5 px-3 text-zinc-300">{h.foco}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <div className="bg-zinc-950 p-4 rounded-xl border border-zinc-800/80 space-y-2 text-xs text-zinc-400">
                  <div className="flex items-center gap-2 text-zinc-200 font-semibold">
                    <Info className="w-4 h-4 text-blue-400" />
                    <span>Princípio do Balanceamento Semanal (Lean Construction):</span>
                  </div>
                  <p>
                    O canteiro opera com a equipe base contratada para o mês (ex: 9 a 10 no Mês 1, 14 no Mês 2). 
                    As frentes de trabalho são programadas em lotes de 2 a 3 dias úteis para que <strong className="text-zinc-200">a mesma equipe se mova continuamente</strong> entre as atividades. 
                    Isso elimina picos fictícios de mão de obra e impede que ocorram dias de ociosidade no canteiro.
                  </p>
                </div>

                <div className="flex justify-end">
                  <button
                    onClick={() => setMostrarHistogramaModal(false)}
                    className="bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-4 py-2 rounded-lg transition-colors"
                  >
                    Fechar Histograma
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ABA 1: LINHA DE BALANÇO (LONGO PRAZO 180 DIAS) */}
      {activeTab === 'lob' && (
        <div className="space-y-4">
          <LinhaDeBalanco />
        </div>
      )}

      {/* ABA 2: GRÁFICO DE GANTT EXECUTIVO & CAMINHO CRÍTICO CPM */}
      {activeTab === 'cpm' && (
        <div className="space-y-6">
          {/* COMPONENTE PRINCIPAL: GRÁFICO DE GANTT EXECUTIVO INTERATIVO */}
          <GanttExecutivo 
            cpmAtividades={cpmAtividades} 
            tarefasDetalhadas={tarefas} 
            metaGlobal={metaGlobal} 
          />

          {/* AUDITORIA DETERMINÍSTICA: TABELA DE PRECEDÊNCIAS CPM */}
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
            <div className="flex justify-between items-center mb-4">
              <div>
                <h3 className="text-base font-semibold text-white">Auditoria Matemática de Precedências (CPM Determinístico)</h3>
                <p className="text-xs text-zinc-400">
                  Cálculo algorítmico (Forward/Backward pass) com Teoria dos Grafos via <span className="font-mono text-zinc-300">calcular_cpm.py</span>.
                </p>
              </div>
              <span className="text-xs bg-zinc-800 text-zinc-400 border border-zinc-700 px-3 py-1 rounded-full font-bold">
                {cpmAtividades.length} Macroatividades
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-zinc-300">
                <thead className="text-[11px] uppercase bg-zinc-950/80 text-zinc-400 border-b border-zinc-800">
                  <tr>
                    <th className="py-2.5 px-3">ID</th>
                    <th className="py-2.5 px-3">Macroatividade</th>
                    <th className="py-2.5 px-3 text-center">Duração</th>
                    <th className="py-2.5 px-3 text-center">Início Cedo</th>
                    <th className="py-2.5 px-3 text-center">Fim Cedo</th>
                    <th className="py-2.5 px-3 text-center">Folga Total</th>
                    <th className="py-2.5 px-3 text-center">Status Crítico</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-800/60">
                  {cpmAtividades.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="text-center py-6 text-zinc-500">
                        Carregando dados de caminho crítico...
                      </td>
                    </tr>
                  ) : (
                    cpmAtividades.map((atv, idx) => {
                      const isCritica = atv.critica !== false;
                      return (
                        <tr key={atv.id || idx} className="hover:bg-zinc-800/40 transition-colors">
                          <td className="py-2 px-3 font-mono text-xs text-blue-400 font-bold">{atv.id}</td>
                          <td className="py-2 px-3 font-medium text-white">{formatDescricaoCPM(atv.id)}</td>
                          <td className="py-2 px-3 text-center font-mono">{atv.duracao_dias}d</td>
                          <td className="py-2 px-3 text-center font-mono text-zinc-400">Dia {atv.es_inicio_mais_cedo ?? '-'}</td>
                          <td className="py-2 px-3 text-center font-mono text-zinc-400">Dia {atv.ef_fim_mais_cedo ?? '-'}</td>
                          <td className="py-2 px-3 text-center font-mono">
                            {atv.folga_dias !== undefined ? `${atv.folga_dias}d` : '0d'}
                          </td>
                          <td className="py-2 px-3 text-center">
                            {isCritica ? (
                              <span className="bg-rose-500/20 text-rose-400 border border-rose-500/40 px-2 py-0.5 rounded text-[11px] font-bold">
                                CRÍTICA (0d)
                              </span>
                            ) : (
                              <span className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 px-2 py-0.5 rounded text-[11px] font-bold">
                                Folga ({atv.folga_dias}d)
                              </span>
                            )}
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ABA 3: CURVA S */}
      {activeTab === 'curva_s' && (
        <div className="space-y-6">
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
            <h3 className="text-lg font-semibold text-white mb-2">Tabela da Curva S Oficial (Baseline 01)</h3>
            <p className="text-sm text-zinc-400 mb-4">
              Distribuição dos R$ 1.660.762,28 ao longo dos 6 meses de produção civil.
            </p>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-zinc-300">
                <thead className="text-xs uppercase bg-zinc-950/80 text-zinc-400 border-b border-zinc-800">
                  <tr>
                    <th className="py-3 px-4">Mês</th>
                    <th className="py-3 px-4 text-right">Faturamento Previsto (R$)</th>
                    <th className="py-3 px-4 text-center">% Físico Acumulado</th>
                    <th className="py-3 px-4 text-center">% Financeiro Acumulado</th>
                    <th className="py-3 px-4 text-center">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-800/60">
                  {curvaS.map((item, idx) => (
                    <tr key={idx} className="hover:bg-zinc-800/40 transition-colors">
                      <td className="py-3 px-4 font-bold text-white">{item.mes}</td>
                      <td className="py-3 px-4 text-right font-mono text-emerald-400">
                        {item.valorMes.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
                      </td>
                      <td className="py-3 px-4 text-center font-bold text-blue-400">{item.fisicoPlan}%</td>
                      <td className="py-3 px-4 text-center font-bold text-amber-400">{item.financeiroPlan}%</td>
                      <td className="py-3 px-4 text-center">
                        <span className="text-xs bg-zinc-800 text-zinc-300 px-2 py-0.5 rounded">
                          Planejado
                        </span>
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
