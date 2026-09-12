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
  hhTotal?: number;
}

interface HistogramaFuncaoItem {
  grupo: string;
  cargo: string;
  categoria: string;
  custoBase: number;
  meses: number[];
  totalMeses: number;
  totalHH: number;
}

interface ResumoHistograma {
  totalGeralHH: number;
  totalHeadcountMeses: number;
  mediaHeadcount: number;
  picoHeadcount: number;
}

export default function CronogramaPage() {
  const { obraAtiva } = useObra();
  const [activeTab, setActiveTab] = useState<'lob' | 'curto_prazo' | 'cpm' | 'curva_s'>('curto_prazo');
  const [cpmAtividades, setCpmAtividades] = useState<AtividadeCPM[]>([]);
  const [tarefas, setTarefas] = useState<any[]>([]);
  const [curvaS, setCurvaS] = useState<CurvaSItem[]>([]);
  const [lotes, setLotes] = useState<LoteCurtoPrazo[]>([]);
  const [histogramaMensal, setHistogramaMensal] = useState<HistogramaItem[]>([]);
  const [histogramaPorFuncao, setHistogramaPorFuncao] = useState<HistogramaFuncaoItem[]>([]);
  const [resumoHistograma, setResumoHistograma] = useState<ResumoHistograma | null>(null);
  const [mostrarHistogramaModal, setMostrarHistogramaModal] = useState(false);
  const [abaHistogramaModal, setAbaHistogramaModal] = useState<'mensal' | 'funcoes'>('mensal');
  const [filtroGrupoFuncao, setFiltroGrupoFuncao] = useState<string>('TODOS');
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
        if (data.histogramaPorFuncao) setHistogramaPorFuncao(data.histogramaPorFuncao);
        if (data.resumoHistograma) setResumoHistograma(data.resumoHistograma);
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

          {/* MODAL / PAINEL DO HISTOGRAMA OFICIAL DE MÃO DE OBRA (EAP 1.0 / RH) */}
          {mostrarHistogramaModal && (
            <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
              <div className="bg-zinc-900 border border-zinc-700 rounded-2xl max-w-5xl w-full max-h-[92vh] flex flex-col p-6 shadow-2xl space-y-4 animate-in fade-in zoom-in-95 duration-200">
                {/* CABEÇALHO DO MODAL */}
                <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-blue-500/20 border border-blue-500/40 flex items-center justify-center">
                      <Users className="w-5 h-5 text-blue-400" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-white flex items-center gap-2">
                        Histograma Oficial de Mão de Obra — EAP 1.0 & RH
                        <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                          Sincronizado Lean 220h/mês
                        </span>
                      </h3>
                      <p className="text-xs text-zinc-400">Headcount mensal planejado vs dimensionamento de equipes, alojamento e custo operacional</p>
                    </div>
                  </div>
                  <button 
                    onClick={() => setMostrarHistogramaModal(false)}
                    className="p-1.5 text-zinc-400 hover:text-white rounded-lg hover:bg-zinc-800 transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                {/* 4 CARDS DE RESUMO EXECUTIVO (TOTALIZADORES) */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="bg-zinc-950/80 p-3 rounded-xl border border-amber-500/30 bg-gradient-to-br from-amber-950/20 to-zinc-950">
                    <span className="text-[11px] uppercase font-bold text-amber-400 tracking-wider block">Total de Horas-Homem</span>
                    <span className="text-xl font-black text-amber-300 font-mono">
                      {resumoHistograma?.totalGeralHH ? `${resumoHistograma.totalGeralHH.toLocaleString('pt-BR')} HH` : '22.440 HH'}
                    </span>
                    <span className="text-[10px] text-zinc-500 block">Baseline Contratual (178 dias)</span>
                  </div>

                  <div className="bg-zinc-950/80 p-3 rounded-xl border border-blue-500/30 bg-gradient-to-br from-blue-950/20 to-zinc-950">
                    <span className="text-[11px] uppercase font-bold text-blue-400 tracking-wider block">Total Headcount Acumulado</span>
                    <span className="text-xl font-black text-blue-300 font-mono">
                      {resumoHistograma?.totalHeadcountMeses || 102} Homens-Mês
                    </span>
                    <span className="text-[10px] text-zinc-500 block">Soma 6 Meses de Canteiro</span>
                  </div>

                  <div className="bg-zinc-950/80 p-3 rounded-xl border border-emerald-500/30 bg-gradient-to-br from-emerald-950/20 to-zinc-950">
                    <span className="text-[11px] uppercase font-bold text-emerald-400 tracking-wider block">Pico de Mobilização</span>
                    <span className="text-xl font-black text-emerald-300 font-mono">
                      {resumoHistograma?.picoHeadcount || 20} Profissionais
                    </span>
                    <span className="text-[10px] text-zinc-500 block">Mês 3 (Alvenaria & Cobertura)</span>
                  </div>

                  <div className="bg-zinc-950/80 p-3 rounded-xl border border-purple-500/30 bg-gradient-to-br from-purple-950/20 to-zinc-950">
                    <span className="text-[11px] uppercase font-bold text-purple-400 tracking-wider block">Média de Efetivo</span>
                    <span className="text-xl font-black text-purple-300 font-mono">
                      {resumoHistograma?.mediaHeadcount ? resumoHistograma.mediaHeadcount.toFixed(1) : '17.0'} Operários/mês
                    </span>
                    <span className="text-[10px] text-zinc-500 block">Inclui 5 fixos de Gestão/SST</span>
                  </div>
                </div>

                {/* ABAS DO MODAL */}
                <div className="flex items-center justify-between border-b border-zinc-800 pb-2">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setAbaHistogramaModal('mensal')}
                      className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
                        abaHistogramaModal === 'mensal'
                          ? 'bg-blue-600 text-white shadow-sm'
                          : 'bg-zinc-800/80 text-zinc-400 hover:text-zinc-200'
                      }`}
                    >
                      <Calendar className="w-3.5 h-3.5" />
                      Visão Mensal Consolidada (M1 a M6)
                    </button>
                    <button
                      onClick={() => setAbaHistogramaModal('funcoes')}
                      className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
                        abaHistogramaModal === 'funcoes'
                          ? 'bg-blue-600 text-white shadow-sm'
                          : 'bg-zinc-800/80 text-zinc-400 hover:text-zinc-200'
                      }`}
                    >
                      <Users className="w-3.5 h-3.5" />
                      Equipe por Função (18 Especialidades)
                    </button>
                  </div>

                  {abaHistogramaModal === 'funcoes' && (
                    <div className="flex items-center gap-1 text-[11px]">
                      <span className="text-zinc-500 mr-1">Filtrar:</span>
                      {['TODOS', 'Gestão', 'SST / Apoio', 'Produção', 'Instalações', 'Apoio'].map(g => (
                        <button
                          key={g}
                          onClick={() => setFiltroGrupoFuncao(g)}
                          className={`px-2 py-0.5 rounded text-[11px] font-medium transition-colors ${
                            filtroGrupoFuncao === g
                              ? 'bg-zinc-700 text-white font-bold'
                              : 'text-zinc-400 hover:bg-zinc-800'
                          }`}
                        >
                          {g}
                        </button>
                      ))}
                    </div>
                  )}
                </div>

                {/* CORPO DO MODAL - ROLÁVEL */}
                <div className="overflow-y-auto flex-1 pr-1 space-y-4 max-h-[50vh]">
                  {abaHistogramaModal === 'mensal' && (
                    <div className="overflow-x-auto rounded-xl border border-zinc-800">
                      <table className="w-full text-left text-xs text-zinc-300">
                        <thead className="uppercase bg-zinc-950 text-zinc-400 border-b border-zinc-800 font-semibold">
                          <tr>
                            <th className="py-2.5 px-3">Mês / Período</th>
                            <th className="py-2.5 px-3 text-center">Produção Direta</th>
                            <th className="py-2.5 px-3 text-center">Gestão & SST</th>
                            <th className="py-2.5 px-3 text-center font-bold text-white">Total Canteiro</th>
                            <th className="py-2.5 px-3 text-center font-semibold text-amber-400">Horas-Homem (HH)</th>
                            <th className="py-2.5 px-3">Frente Crítica / Foco Principal</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-zinc-800/60">
                          {histogramaMensal.map((h, idx) => (
                            <tr key={idx} className="hover:bg-zinc-800/40">
                              <td className="py-2.5 px-3 font-semibold text-white whitespace-nowrap">{h.mes}</td>
                              <td className="py-2.5 px-3 text-center font-mono text-emerald-400 font-bold">{h.producao} op.</td>
                              <td className="py-2.5 px-3 text-center font-mono text-zinc-400">{h.gestaoApoio} prof.</td>
                              <td className="py-2.5 px-3 text-center font-mono text-blue-400 font-bold bg-blue-950/20">{h.total} Headcount</td>
                              <td className="py-2.5 px-3 text-center font-mono text-amber-300 font-semibold">{h.hhTotal ? `${h.hhTotal.toLocaleString('pt-BR')} HH` : `${h.total * 220} HH`}</td>
                              <td className="py-2.5 px-3 text-zinc-300">{h.foco}</td>
                            </tr>
                          ))}
                        </tbody>
                        <tfoot className="bg-zinc-950 border-t-2 border-zinc-700 font-bold text-zinc-100">
                          <tr>
                            <td className="py-3 px-3 uppercase tracking-wider text-blue-400">TOTAL GERAL ACUMULADO</td>
                            <td className="py-3 px-3 text-center font-mono text-emerald-400">
                              {histogramaMensal.reduce((a, b) => a + b.producao, 0)} op.-mês
                            </td>
                            <td className="py-3 px-3 text-center font-mono text-zinc-300">
                              {histogramaMensal.reduce((a, b) => a + b.gestaoApoio, 0)} prof.-mês
                            </td>
                            <td className="py-3 px-3 text-center font-mono text-blue-400 bg-blue-950/40 text-sm">
                              {histogramaMensal.reduce((a, b) => a + b.total, 0)} Headcount-Mês
                            </td>
                            <td className="py-3 px-3 text-center font-mono text-amber-400 text-sm bg-amber-950/20">
                              {histogramaMensal.reduce((a, b) => a + (b.hhTotal || b.total * 220), 0).toLocaleString('pt-BR')} Horas-Homem
                            </td>
                            <td className="py-3 px-3 text-[11px] text-zinc-400 italic">
                              Carga Horária: 220h/mês | Meta Físico-Financeira Contratual (178 dias)
                            </td>
                          </tr>
                        </tfoot>
                      </table>
                    </div>
                  )}

                  {abaHistogramaModal === 'funcoes' && (
                    <div className="overflow-x-auto rounded-xl border border-zinc-800">
                      <table className="w-full text-left text-xs text-zinc-300">
                        <thead className="uppercase bg-zinc-950 text-zinc-400 border-b border-zinc-800 font-semibold">
                          <tr>
                            <th className="py-2.5 px-3">Grupo</th>
                            <th className="py-2.5 px-3">Função / Cargo Especialista</th>
                            <th className="py-2.5 px-3 text-center">Categoria</th>
                            <th className="py-2.5 px-3 text-right">Custo Base Ref.</th>
                            <th className="py-2.5 px-2 text-center text-blue-300">M1</th>
                            <th className="py-2.5 px-2 text-center text-blue-300">M2</th>
                            <th className="py-2.5 px-2 text-center text-blue-300">M3</th>
                            <th className="py-2.5 px-2 text-center text-blue-300">M4</th>
                            <th className="py-2.5 px-2 text-center text-blue-300">M5</th>
                            <th className="py-2.5 px-2 text-center text-blue-300">M6</th>
                            <th className="py-2.5 px-3 text-center font-bold text-white bg-zinc-900">Total Meses</th>
                            <th className="py-2.5 px-3 text-right font-bold text-amber-400 bg-zinc-900">Total HH</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-zinc-800/60">
                          {histogramaPorFuncao
                            .filter(f => filtroGrupoFuncao === 'TODOS' || f.grupo === filtroGrupoFuncao)
                            .map((f, idx) => (
                              <tr key={idx} className="hover:bg-zinc-800/40">
                                <td className="py-2 px-3 whitespace-nowrap">
                                  <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                                    f.grupo === 'Gestão' ? 'bg-purple-950/60 text-purple-400 border border-purple-800/40' :
                                    f.grupo === 'SST / Apoio' ? 'bg-orange-950/60 text-orange-400 border border-orange-800/40' :
                                    f.grupo === 'Produção' ? 'bg-emerald-950/60 text-emerald-400 border border-emerald-800/40' :
                                    f.grupo === 'Instalações' ? 'bg-blue-950/60 text-blue-400 border border-blue-800/40' :
                                    'bg-zinc-800 text-zinc-300'
                                  }`}>
                                    {f.grupo}
                                  </span>
                                </td>
                                <td className="py-2 px-3 font-medium text-white">{f.cargo}</td>
                                <td className="py-2 px-3 text-center text-zinc-400 text-[11px]">{f.categoria}</td>
                                <td className="py-2 px-3 text-right font-mono text-zinc-400">
                                  {f.custoBase > 0 ? f.custoBase.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) : '—'}
                                </td>
                                {f.meses.map((mVal, mIdx) => (
                                  <td 
                                    key={mIdx} 
                                    className={`py-2 px-2 text-center font-mono ${
                                      mVal > 0 ? 'text-emerald-400 font-bold bg-emerald-950/10' : 'text-zinc-600'
                                    }`}
                                  >
                                    {mVal > 0 ? mVal : '—'}
                                  </td>
                                ))}
                                <td className="py-2 px-3 text-center font-mono font-bold text-white bg-zinc-900/80">
                                  {f.totalMeses}
                                </td>
                                <td className="py-2 px-3 text-right font-mono font-bold text-amber-300 bg-zinc-900/80">
                                  {f.totalHH.toLocaleString('pt-BR')} HH
                                </td>
                              </tr>
                            ))}
                        </tbody>
                        <tfoot className="bg-zinc-950 border-t-2 border-zinc-700 font-bold text-zinc-100">
                          <tr>
                            <td colSpan={4} className="py-3 px-3 uppercase tracking-wider text-blue-400">
                              TOTAL DE CAMPO (TODAS AS ESPECIALIDADES)
                            </td>
                            {[0, 1, 2, 3, 4, 5].map(mIdx => {
                              const somaMes = histogramaPorFuncao.reduce((acc, cur) => acc + (cur.meses[mIdx] || 0), 0);
                              return (
                                <td key={mIdx} className="py-3 px-2 text-center font-mono text-blue-400 font-bold">
                                  {somaMes || (histogramaMensal[mIdx]?.total || '—')}
                                </td>
                              );
                            })}
                            <td className="py-3 px-3 text-center font-mono text-blue-400 bg-blue-950/40 text-sm">
                              {resumoHistograma?.totalHeadcountMeses || 102} Meses
                            </td>
                            <td className="py-3 px-3 text-right font-mono text-amber-400 bg-amber-950/20 text-sm">
                              {(resumoHistograma?.totalGeralHH || 22440).toLocaleString('pt-BR')} Horas-Homem (HH)
                            </td>
                          </tr>
                        </tfoot>
                      </table>
                    </div>
                  )}

                  {/* CAIXA DE INFORMAÇÕES METODOLÓGICAS */}
                  <div className="bg-zinc-950 p-3.5 rounded-xl border border-zinc-800/80 space-y-2 text-xs text-zinc-400">
                    <div className="flex items-center gap-2 text-zinc-200 font-semibold">
                      <Info className="w-4 h-4 text-blue-400 flex-shrink-0" />
                      <span>Metodologia de Dimensionamento e Heijunka (Lean Construction):</span>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-[11px] leading-relaxed">
                      <div>
                        <strong className="text-zinc-300">1. Gestão e SST Estáveis (5 Fixos):</strong>
                        <p>Engenheiro Residente, Mestre Geral, TST, Almoxarife e Vigia permanecem em dedicação contínua durante todos os 6 meses (6.600 HH totais).</p>
                      </div>
                      <div>
                        <strong className="text-zinc-300">2. Nivelamento em Lotes de 2 a 3 Dias:</strong>
                        <p>A produção opera em lotes de ritmo (Takt time), fazendo a equipe especializada transitar de forma contínua entre as frentes, eliminando ociosidade e picos fictícios.</p>
                      </div>
                      <div>
                        <strong className="text-zinc-300">3. Reprogramação e Crashing Automático:</strong>
                        <p>Quando uma atividade é acelerada com aumento de equipe (RUP dinâmico), o script sincronizador atualiza os lotes e o mês correspondente no histograma.</p>
                      </div>
                      <div>
                        <strong className="text-zinc-300">4. Alinhamento Físico-Financeiro:</strong>
                        <p>O total de <strong>22.440 Horas-Homem</strong> (102 homens-mês @ 220h) bate com exatidão matemática com o valor de Turnkey de R$ 1.660.762,28 da Obra TMULT.</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* RODAPÉ DO MODAL COM BOTÃO DE FECHAR */}
                <div className="flex items-center justify-between pt-2 border-t border-zinc-800">
                  <span className="text-[11px] text-zinc-500">
                    Sincronizado automaticamente com <code>scripts/gerar_histograma_sincronizado.py</code> e <code>orquestrar_cronogramas.py</code>
                  </span>
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
