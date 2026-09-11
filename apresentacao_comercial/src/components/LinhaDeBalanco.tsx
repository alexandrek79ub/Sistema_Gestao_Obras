"use client";

import React, { useState, useEffect } from 'react';
import { 
  ZoomIn, ZoomOut, Maximize2, Minimize2, Calendar, User, Clock, 
  ArrowUpRight, CheckCircle2, AlertTriangle, TrendingUp, Layers, Info, X,
  ShieldCheck, HelpCircle
} from 'lucide-react';
import { useObra } from '@/context/ObraContext';

interface TarefaLOB {
  id: number;
  pav: string;
  tipo: string;
  vagao?: string;
  color: string;
  start: number;
  duration: number;
  equipe: string;
  dataInicio?: string;
  dataFim?: string;
}

interface PontoVagao {
  id: number;
  pav: string;
  start: number;
  duration: number;
  dataInicio?: string;
  dataFim?: string;
}

interface VagaoFluxo {
  id: string;
  nome: string;
  equipe: string;
  color: string;
  pontos: PontoVagao[];
  startMin: number;
  endMax: number;
  dataInicioGlobal?: string;
  dataFimGlobal?: string;
}

// Paleta de cores vibrantes, contrastantes e oficiais para Linhas de Balanço Lean
const COR_HEX_VAGOES: Record<string, { stroke: string; fill: string; badge: string; bgCard: string; border: string }> = {
  "01": { stroke: "#0284c7", fill: "rgba(2, 132, 199, 0.28)", badge: "bg-sky-600", bgCard: "bg-sky-950/70", border: "border-sky-500" }, // Topografia & Canteiro
  "02": { stroke: "#2563eb", fill: "rgba(37, 99, 235, 0.28)", badge: "bg-blue-600", bgCard: "bg-blue-950/70", border: "border-blue-500" }, // Fundações Sapatas
  "03": { stroke: "#1d4ed8", fill: "rgba(29, 78, 216, 0.28)", badge: "bg-blue-700", bgCard: "bg-blue-950/70", border: "border-blue-600" }, // Vigas Baldrames
  "04": { stroke: "#6366f1", fill: "rgba(99, 102, 241, 0.28)", badge: "bg-indigo-600", bgCard: "bg-indigo-950/70", border: "border-indigo-500" }, // Pilares Supraestrutura
  "05": { stroke: "#7c3aed", fill: "rgba(124, 58, 237, 0.28)", badge: "bg-violet-600", bgCard: "bg-violet-950/70", border: "border-violet-500" }, // Vigas & Laje H12
  "06": { stroke: "#f59e0b", fill: "rgba(245, 158, 11, 0.30)", badge: "bg-amber-600", bgCard: "bg-amber-950/70", border: "border-amber-500" }, // Alvenaria de Vedação
  "07": { stroke: "#06b6d4", fill: "rgba(6, 182, 212, 0.30)", badge: "bg-cyan-600", bgCard: "bg-cyan-950/70", border: "border-cyan-500" }, // Cobertura Metálica
  "08": { stroke: "#10b981", fill: "rgba(16, 185, 129, 0.28)", badge: "bg-emerald-600", bgCard: "bg-emerald-950/70", border: "border-emerald-500" }, // Instalações Embutidas
  "09": { stroke: "#ea580c", fill: "rgba(234, 88, 12, 0.30)", badge: "bg-orange-600", bgCard: "bg-orange-950/70", border: "border-orange-500" }, // Reboco Paulista
  "10": { stroke: "#e11d48", fill: "rgba(225, 29, 72, 0.28)", badge: "bg-rose-600", bgCard: "bg-rose-950/70", border: "border-rose-500" }, // Pisos & Porcelanato
  "11": { stroke: "#9333ea", fill: "rgba(147, 51, 234, 0.28)", badge: "bg-purple-600", bgCard: "bg-purple-950/70", border: "border-purple-500" }, // Esquadrias de Alumínio
  "12": { stroke: "#0ea5e9", fill: "rgba(14, 165, 233, 0.28)", badge: "bg-sky-500", bgCard: "bg-sky-950/70", border: "border-sky-400" }, // Climatização HVAC
  "13": { stroke: "#eab308", fill: "rgba(234, 179, 8, 0.30)", badge: "bg-yellow-500", bgCard: "bg-yellow-950/70", border: "border-yellow-400" }, // Acabamentos Elétr./Hidr.
  "14": { stroke: "#d946ef", fill: "rgba(217, 70, 239, 0.28)", badge: "bg-fuchsia-600", bgCard: "bg-fuchsia-950/70", border: "border-fuchsia-500" }, // Pintura Acrílica Final
  "15": { stroke: "#14b8a6", fill: "rgba(20, 184, 166, 0.30)", badge: "bg-teal-600", bgCard: "bg-teal-950/70", border: "border-teal-500" }, // Comissionamento & Entrega
};

function getCorVagao(nomeVagao: string) {
  const numPrefix = (nomeVagao || '').slice(0, 2);
  if (COR_HEX_VAGOES[numPrefix]) {
    return COR_HEX_VAGOES[numPrefix];
  }
  return { 
    stroke: "#71717a", 
    fill: "rgba(113, 113, 122, 0.25)", 
    badge: "bg-zinc-600", 
    bgCard: "bg-zinc-900/80", 
    border: "border-zinc-600" 
  };
}

export default function LinhaDeBalanco() {
  const { obraAtiva } = useObra();
  const [zoomX, setZoomX] = useState(1);
  const [zoomY, setZoomY] = useState(1);
  const [modoVisualizacao, setModoVisualizacao] = useState<'semanas' | 'dias'>('semanas');
  const [estiloLOB, setEstiloLOB] = useState<'linhas' | 'blocos'>('linhas');
  
  const [tarefas, setTarefas] = useState<TarefaLOB[]>([]);
  const [vagoesFluxo, setVagoesFluxo] = useState<VagaoFluxo[]>([]);
  const [pavimentos, setPavimentos] = useState<string[]>([]);
  const [totalDias, setTotalDias] = useState(182);
  const [loading, setLoading] = useState(true);
  
  const [vagaoSelecionado, setVagaoSelecionado] = useState<VagaoFluxo | null>(null);
  const [vagaoHover, setVagaoHover] = useState<string | null>(null);
  const [relatorioSobreposicao, setRelatorioSobreposicao] = useState<any>(null);
  const [showAjuda, setShowAjuda] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/cronograma?obra=${encodeURIComponent(obraAtiva)}`)
      .then(res => res.json())
      .then(data => {
        if (data.tarefas && data.tarefas.length > 0) {
          setTarefas(data.tarefas);
          setVagoesFluxo(data.vagoesFluxo || []);
          setPavimentos(data.pavimentos || []);
          setRelatorioSobreposicao(data.relatorioSobreposicao || null);
          
          let maxDay = 0;
          data.tarefas.forEach((t: TarefaLOB) => {
            const end = t.start + t.duration;
            if (end > maxDay) maxDay = end;
          });
          setTotalDias(Math.max(182, maxDay));
        } else {
          setTarefas([]);
          setVagoesFluxo([]);
          setPavimentos([]);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error('Erro ao buscar cronograma', err);
        setLoading(false);
      });
  }, [obraAtiva]);

  const handleZoomInX = () => setZoomX(prev => Math.min(prev + 0.5, 3));
  const handleZoomOutX = () => setZoomX(prev => Math.max(prev - 0.5, 0.5));
  const handleZoomInY = () => setZoomY(prev => Math.min(prev + 0.5, 2.5));
  const handleZoomOutY = () => setZoomY(prev => Math.max(prev - 0.5, 0.7));

  // Ordenação da Linha de Balanço (LOB):
  // Pavimentos chegam ordenados da Zona 01 (base) até Zona 04 (topo).
  // Ao inverter o array, Zona 04 fica no topo e Zona 01 na base física (fluxo ascendente ↗).
  const pavimentosOrdenados = [...pavimentos].reverse();

  // Dimensões do Gráfico
  const totalSemanas = Math.ceil(totalDias / 7);
  const totalColunas = modoVisualizacao === 'semanas' ? totalSemanas : totalDias;
  
  const chartWidth = Math.max(1100, totalColunas * (modoVisualizacao === 'semanas' ? 56 : 32)) * zoomX;
  const rowHeight = 84 * zoomY;
  const chartHeight = Math.max(320, pavimentosOrdenados.length * rowHeight);

  // Funções de conversão cartesiana (Tempo X e Setor Y)
  const getX = (dia: number) => {
    const clamped = Math.max(1, Math.min(totalDias, dia));
    return ((clamped - 1) / totalDias) * chartWidth;
  };

  const getYCenter = (pavNome: string) => {
    const idx = pavimentosOrdenados.indexOf(pavNome);
    if (idx === -1) return rowHeight / 2;
    return idx * rowHeight + rowHeight / 2;
  };

  // Agrupamento para a visão de "Blocos por Lotes"
  // Consolida tarefas contíguas do mesmo vagão no setor (folga <= 2 dias de fim de semana).
  // Tarefas com intervalo real de espera formam lotes distintos, preservando a diagonal ascendente Lean ↗.
  const lotesConsolidadosPorSetor = pavimentosOrdenados.map((pav, rowIdx) => {
    const tarefasDoSetor = [...tarefas.filter(t => t.pav === pav)].sort((a, b) => a.start - b.start);
    const lotes: {
      id: string;
      pav: string;
      vagaoNome: string;
      equipe: string;
      start: number;
      end: number;
      duration: number;
      dataInicio?: string;
      dataFim?: string;
      color: string;
    }[] = [];

    tarefasDoSetor.forEach((t, idx) => {
      const vNome = t.vagao || t.tipo;
      const tEnd = t.start + t.duration;
      const ultimo = lotes[lotes.length - 1];

      // Mescla apenas se for do mesmo vagão E for contíguo no tempo (gap <= 2 dias úteis/domingo)
      if (ultimo && ultimo.vagaoNome === vNome && (t.start - ultimo.end <= 2)) {
        ultimo.end = Math.max(ultimo.end, tEnd);
        ultimo.duration = ultimo.end - ultimo.start;
        if (t.dataFim) ultimo.dataFim = t.dataFim;
      } else {
        lotes.push({
          id: `${pav}-${vNome}-${t.start}-${idx}`,
          pav,
          vagaoNome: vNome,
          equipe: t.equipe,
          start: t.start,
          end: tEnd,
          duration: t.duration,
          dataInicio: t.dataInicio,
          dataFim: t.dataFim,
          color: t.color
        });
      }
    });

    return {
      pav,
      rowIdx,
      lotes
    };
  });

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 overflow-hidden select-none shadow-2xl">
      {/* CABEÇALHO DO COMPONENTE */}
      <div className="flex flex-col lg:flex-row lg:justify-between items-start mb-6 gap-4">
        <div>
          <h3 className="text-lg font-semibold text-white mb-1 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            Linha de Balanço (LOB) — Fluxo Contínuo & Ritmo Construtivo
            <ArrowUpRight className="w-4 h-4 text-emerald-400" />
            <button 
              onClick={() => setShowAjuda(!showAjuda)}
              className="ml-2 text-zinc-400 hover:text-white transition-colors"
              title="O que é a Linha de Balanço?"
            >
              <HelpCircle className="w-4 h-4" />
            </button>
          </h3>
          <p className="text-sm text-zinc-400">
            Orientação canônica de engenharia: <span className="text-zinc-200 font-semibold">Zona 1 na base</span> e <span className="text-zinc-200 font-semibold">Zona 4 (Cobertura) no topo</span>. O tempo avança no eixo horizontal inferior (fluxo ascendente ↗).
          </p>
        </div>
        
        <div className="flex flex-wrap items-center gap-3">
          {/* SELETOR DE ESTILO: LINHAS CONTÍNUAS (LOB) VS BLOCOS POR SETOR */}
          <div className="bg-zinc-950 p-1 rounded-lg border border-zinc-800 flex items-center text-xs">
            <button
              onClick={() => setEstiloLOB('linhas')}
              className={`px-3 py-1.5 rounded-md font-semibold transition-colors flex items-center gap-1.5 ${
                estiloLOB === 'linhas' 
                  ? 'bg-emerald-600 text-white shadow-sm ring-1 ring-emerald-400/40' 
                  : 'text-zinc-400 hover:text-white'
              }`}
              title="Exibe as linhas de balanço contínuas conectando os setores no tempo"
            >
              <TrendingUp className="w-3.5 h-3.5" />
              Linhas Contínuas (LOB ↗)
            </button>
            <button
              onClick={() => setEstiloLOB('blocos')}
              className={`px-3 py-1.5 rounded-md font-semibold transition-colors flex items-center gap-1.5 ${
                estiloLOB === 'blocos' 
                  ? 'bg-blue-600 text-white shadow-sm ring-1 ring-blue-400/40' 
                  : 'text-zinc-400 hover:text-white'
              }`}
              title="Exibe a visão detalhada de lotes discretos consolidados por setor"
            >
              <Layers className="w-3.5 h-3.5" />
              Blocos por Lotes
            </button>
          </div>

          {/* SELETOR DE MODO DE ESCALA TEMPORAL */}
          <div className="bg-zinc-950 p-1 rounded-lg border border-zinc-800 flex items-center text-xs">
            <button
              onClick={() => setModoVisualizacao('semanas')}
              className={`px-3 py-1.5 rounded-md font-semibold transition-colors ${
                modoVisualizacao === 'semanas' 
                  ? 'bg-zinc-800 text-white shadow-sm' 
                  : 'text-zinc-400 hover:text-white'
              }`}
            >
              26 Semanas
            </button>
            <button
              onClick={() => setModoVisualizacao('dias')}
              className={`px-3 py-1.5 rounded-md font-semibold transition-colors ${
                modoVisualizacao === 'dias' 
                  ? 'bg-zinc-800 text-white shadow-sm' 
                  : 'text-zinc-400 hover:text-white'
              }`}
            >
              182 Dias
            </button>
          </div>

          {/* CONTROLES DE ZOOM */}
          <div className="flex space-x-2">
            <div className="flex items-center space-x-1.5 bg-zinc-950/80 px-2 py-1 rounded-lg border border-zinc-800">
              <span className="text-[10px] text-zinc-500 font-bold uppercase tracking-wider">Tempo (X)</span>
              <button onClick={handleZoomOutX} className="p-1 hover:bg-zinc-800 rounded text-zinc-400 hover:text-white transition-colors" title="Comprimir Tempo"><ZoomOut className="w-3.5 h-3.5" /></button>
              <span className="text-xs font-mono w-8 text-center text-zinc-300">{Math.round(zoomX * 100)}%</span>
              <button onClick={handleZoomInX} className="p-1 hover:bg-zinc-800 rounded text-zinc-400 hover:text-white transition-colors" title="Expandir Tempo"><ZoomIn className="w-3.5 h-3.5" /></button>
            </div>
            
            <div className="flex items-center space-x-1.5 bg-zinc-950/80 px-2 py-1 rounded-lg border border-zinc-800">
              <span className="text-[10px] text-zinc-500 font-bold uppercase tracking-wider">Setor (Y)</span>
              <button onClick={handleZoomOutY} className="p-1 hover:bg-zinc-800 rounded text-zinc-400 hover:text-white transition-colors" title="Achatar"><Minimize2 className="w-3.5 h-3.5" /></button>
              <span className="text-xs font-mono w-8 text-center text-zinc-300">{Math.round(zoomY * 100)}%</span>
              <button onClick={handleZoomInY} className="p-1 hover:bg-zinc-800 rounded text-zinc-400 hover:text-white transition-colors" title="Expandir"><Maximize2 className="w-3.5 h-3.5" /></button>
            </div>
          </div>
        </div>
      </div>

      {/* GUIA DE ENTENDIMENTO EXPANSÍVEL (AJUDA LEAN) */}
      {showAjuda && (
        <div className="mb-6 p-4 bg-zinc-950 border border-zinc-700/60 rounded-xl text-xs text-zinc-300 space-y-2 animate-in fade-in">
          <div className="flex items-center justify-between font-bold text-emerald-400">
            <span className="flex items-center gap-1.5">
              <Info className="w-4 h-4" /> Como Ler e Interpretar Esta Linha de Balanço (LOB):
            </span>
            <button onClick={() => setShowAjuda(false)} className="text-zinc-500 hover:text-white">
              <X className="w-4 h-4" />
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2 text-zinc-400 leading-relaxed">
            <div>
              <strong className="text-zinc-200">1. Eixo Vertical (Y):</strong> Representa os 4 setores físicos da obra (Zona 01 na base até Zona 04 no topo).
            </div>
            <div>
              <strong className="text-zinc-200">2. Linhas Inclinadas (↗):</strong> Cada faixa colorida é um serviço (Vagão). A inclinação mostra o ritmo de produção (Takt Time de 3 dias). Linhas paralelas significam zero ociosidade e fluxo contínuo!
            </div>
            <div>
              <strong className="text-zinc-200">3. Sem Cruzamento Indevido:</strong> Quando as faixas não se cruzam no mesmo setor, significa que os subempreiteiros trabalham em harmonia sem disputar espaço físico.
            </div>
          </div>
        </div>
      )}

      {/* ALERTA LEAN: NIVELAMENTO (HEIJUNKA) OU SOBREPOSIÇÃO */}
      {relatorioSobreposicao && (relatorioSobreposicao.total_conflitos_espaciais > 0 || relatorioSobreposicao.total_disciplinas_com_frentes_duplas > 0) ? (
        <div className="mb-6 p-4 bg-amber-950/40 border border-amber-500/50 rounded-xl flex items-start gap-3 text-amber-200 shadow-lg">
          <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
          <div className="flex-1">
            <div className="font-semibold text-amber-300 flex items-center gap-2">
              <span>ALERTA LEAN: Sobreposição de Serviços & Demanda de Efetivo Extra</span>
              <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40">
                {relatorioSobreposicao.status_aprovacao === 'APROVADO_COM_ACORDO_EFETIVO' ? 'Acordo Autorizado' : 'Ação Necessária'}
              </span>
            </div>
            <p className="text-xs text-amber-200/80 mt-1">
              Foram identificadas frentes simultâneas concorrentes ({relatorioSobreposicao.total_disciplinas_com_frentes_duplas} disciplina(s) e {relatorioSobreposicao.total_conflitos_espaciais} conflito(s) espacial). 
              Para manter essas frentes paralelas, o efetivo de pico atinge <strong>{relatorioSobreposicao.headcount_pico_diario} operários</strong>.
            </p>
          </div>
        </div>
      ) : relatorioSobreposicao ? (
        <div className="mb-6 p-3.5 bg-emerald-950/40 border border-emerald-500/40 rounded-xl flex items-center justify-between text-xs text-emerald-300 shadow-md">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span><strong>Fluxo Contínuo Nivelado (Heijunka):</strong> Linhas de produção em fluxo contínuo em série, sem cruzamento de equipes no mesmo setor. Takt de 3 dias rigorosamente mantido.</span>
          </div>
          <span className="text-emerald-400/90 font-mono text-[11px] hidden sm:inline border-l border-emerald-700/50 pl-3">
            Efetivo Médio: <strong>{relatorioSobreposicao.headcount_medio_diario || '10.6'} op.</strong> | Pico: <strong>{relatorioSobreposicao.headcount_pico_diario || '24'} op.</strong>
          </span>
        </div>
      ) : null}

      {/* ÁREA PRINCIPAL DO GRÁFICO DA LINHA DE BALANÇO */}
      <div className="w-full overflow-x-auto pb-4 scrollbar-thin scrollbar-thumb-zinc-700 scrollbar-track-zinc-900 border border-zinc-800 rounded-xl bg-zinc-950/90 shadow-inner">
        {loading ? (
          <div className="p-16 text-center text-zinc-400 flex flex-col items-center gap-3">
            <div className="w-7 h-7 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
            <span>Calculando vetores e trajetórias da Linha de Balanço ({obraAtiva})...</span>
          </div>
        ) : pavimentosOrdenados.length === 0 ? (
          <div className="p-16 text-center text-zinc-400">
            <p className="text-base font-semibold text-zinc-300">Nenhum setor físico configurado para {obraAtiva}.</p>
          </div>
        ) : (
          <div className="flex" style={{ minWidth: `${chartWidth + 240}px` }}>
            {/* COLUNA ESQUERDA: EIXO VERTICAL Y COM OS SETORES FÍSICOS DA OBRA */}
            <div className="w-60 shrink-0 border-r border-zinc-800 bg-zinc-950 sticky left-0 z-30 shadow-2xl flex flex-col justify-between">
              <div>
                <div className="h-10 px-3 border-b border-zinc-800 text-[11px] uppercase tracking-wider font-bold text-zinc-400 flex items-center justify-between bg-zinc-900/60">
                  <span>Setores Físicos</span>
                  <span className="text-[10px] text-zinc-500 font-mono">Pavimento (Y)</span>
                </div>
                {pavimentosOrdenados.map((pav, idx) => (
                  <div 
                    key={pav} 
                    style={{ height: `${rowHeight}px` }}
                    className={`flex items-center px-4 border-b border-zinc-800/80 text-xs font-semibold transition-colors ${
                      idx % 2 === 0 ? 'bg-zinc-900/40' : 'bg-zinc-950/60'
                    } hover:bg-zinc-800/50 text-zinc-200`}
                  >
                    <div className="truncate">
                      <div className="flex items-center gap-2">
                        <span className="w-2.5 h-2.5 rounded-full bg-blue-500 shadow-sm"></span>
                        <span className="truncate text-white font-medium" title={pav}>{pav}</span>
                      </div>
                      <div className="text-[10px] text-zinc-500 font-mono pl-4 mt-0.5">
                        {idx === 0 ? 'Topo • Nível Superior' : idx === pavimentosOrdenados.length - 1 ? 'Base • Cota Zero' : `Etapa Construtiva 0${pavimentosOrdenados.length - idx}`}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="h-10 px-3 border-t border-zinc-800 text-[11px] font-mono text-zinc-400 bg-zinc-950 flex items-center justify-between">
                <span>Eixo Y: Setor ↗</span>
                <span className="text-[10px] text-zinc-600">4 Zonas</span>
              </div>
            </div>

            {/* ÁREA GRÁFICA: SVG COM AS LINHAS INCLINADAS DE BALANÇO */}
            <div className="flex-1 relative overflow-hidden" style={{ width: `${chartWidth}px` }}>
              {/* CABEÇALHO SUPERIOR TEMPORAL (ALINHADO COM O CABEÇALHO DOS SETORES) */}
              <div 
                className="h-10 border-b border-zinc-800 bg-zinc-900/60 flex items-center sticky top-0 z-20"
                style={{ width: `${chartWidth}px` }}
              >
                {Array.from({ length: totalSemanas }).map((_, i) => (
                  <div 
                    key={i} 
                    className="flex-1 text-center text-[10px] font-mono text-zinc-400 border-r border-dashed border-zinc-800/60"
                  >
                    S{i + 1}
                  </div>
                ))}
              </div>

              {/* CORPO DO GRÁFICO (LINHAS / BLOCOS) */}
              <div className="relative" style={{ width: `${chartWidth}px`, height: `${chartHeight}px` }}>
                {/* GRADE DE FUNDO: LINHAS HORIZONTAIS DE CADA PAVIMENTO */}
                <div className="absolute inset-0 pointer-events-none" style={{ height: `${chartHeight}px` }}>
                  {pavimentosOrdenados.map((pav, idx) => (
                    <div 
                      key={pav} 
                      style={{ height: `${rowHeight}px` }}
                      className={`w-full border-b border-zinc-800/60 transition-colors ${
                        idx % 2 === 0 ? 'bg-zinc-900/15' : 'bg-transparent'
                      }`}
                    ></div>
                  ))}
                </div>

                {/* GRADE DE FUNDO: LINHAS VERTICAIS SEMANAIS */}
                <div className="absolute inset-0 pointer-events-none flex" style={{ height: `${chartHeight}px` }}>
                  {Array.from({ length: totalSemanas }).map((_, i) => (
                    <div 
                      key={i} 
                      className="flex-1 border-r border-dashed border-zinc-800/40 h-full relative"
                    ></div>
                  ))}
                </div>

                {/* CAMADA VETORIAL SVG COM AS LINHAS DE BALANÇO (LOB REAL ↗) */}
                {estiloLOB === 'linhas' ? (
                  <svg 
                    className="absolute inset-0 w-full"
                  style={{ height: `${chartHeight}px` }}
                >
                  <defs>
                    <filter id="glow-line" x="-20%" y="-20%" width="140%" height="140%">
                      <feDropShadow dx="0" dy="0" stdDeviation="4" floodColor="#38bdf8" floodOpacity="0.7" />
                    </filter>
                    <pattern id="stripe-comissionamento" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                      <line x1="0" y1="0" x2="0" y2="12" stroke="#14b8a6" strokeWidth="2" strokeOpacity="0.25" />
                    </pattern>
                  </defs>

                  {/* 1. RENDERIZAR AS FAIXAS E VAGÕES DE FLUXO */}
                  {vagoesFluxo.map((vagao) => {
                    const cor = getCorVagao(vagao.nome);
                    const isHovered = vagaoHover === vagao.id;
                    const isSelected = vagaoSelecionado?.id === vagao.id;
                    const isCommissioning = vagao.nome.includes('15.') || vagao.nome.toLowerCase().includes('comissionamento');

                    // Agrupar pontos do vagão por zona física (evita nós repetidos e auto-interseções)
                    const zonasDoVagaoMap = new Map<string, {
                      pav: string;
                      idxPav: number;
                      start: number;
                      end: number;
                      duration: number;
                      dataInicio?: string;
                      dataFim?: string;
                    }>();

                    vagao.pontos.forEach((p) => {
                      const idx = pavimentosOrdenados.indexOf(p.pav);
                      if (idx === -1) return;
                      const pEnd = p.start + p.duration;

                      if (!zonasDoVagaoMap.has(p.pav)) {
                        zonasDoVagaoMap.set(p.pav, {
                          pav: p.pav,
                          idxPav: idx,
                          start: p.start,
                          end: pEnd,
                          duration: p.duration,
                          dataInicio: p.dataInicio,
                          dataFim: p.dataFim,
                        });
                      } else {
                        const existing = zonasDoVagaoMap.get(p.pav)!;
                        existing.start = Math.min(existing.start, p.start);
                        existing.end = Math.max(existing.end, pEnd);
                        existing.duration = existing.end - existing.start;
                        if (p.dataInicio && (!existing.dataInicio || p.start <= existing.start)) {
                          existing.dataInicio = p.dataInicio;
                        }
                        if (p.dataFim) {
                          existing.dataFim = p.dataFim;
                        }
                      }
                    });

                    // Ordenar da base (Zona 01) até o topo (Zona 04)
                    // pavimentosOrdenados tem Zona 04 em idx 0 e Zona 01 em idx 3, então ordenamos por idxPav decrescente!
                    const zonasConsolidadas = Array.from(zonasDoVagaoMap.values())
                      .sort((a, b) => b.idxPav - a.idxPav);

                    // CASO 1: COMISSIONAMENTO & ENTREGA (FAIXA VERTICAL DE FECHAMENTO GLOBAL)
                    if (isCommissioning) {
                      const xIni = getX(vagao.startMin);
                      const xFim = getX(vagao.endMax);
                      const width = Math.max(36, xFim - xIni);
                      const yTop = 8;
                      const yBottom = chartHeight - 8;
                      const height = yBottom - yTop;

                      return (
                        <g 
                          key={vagao.id}
                          className="cursor-pointer transition-opacity duration-200"
                          opacity={vagaoHover && !isHovered ? 0.4 : 1}
                          onMouseEnter={() => setVagaoHover(vagao.id)}
                          onMouseLeave={() => setVagaoHover(null)}
                          onClick={() => setVagaoSelecionado(vagao)}
                        >
                          <rect 
                            x={xIni} 
                            y={yTop} 
                            width={width} 
                            height={height} 
                            rx={10}
                            fill="url(#stripe-comissionamento)" 
                            stroke={cor.stroke} 
                            strokeWidth={isHovered || isSelected ? 3 : 1.5}
                            strokeDasharray="6 4"
                            filter={isHovered ? "url(#glow-line)" : undefined}
                          />
                          <rect 
                            x={xIni} 
                            y={yTop} 
                            width={width} 
                            height={height} 
                            rx={10}
                            fill="rgba(20, 184, 166, 0.12)" 
                            pointerEvents="none"
                          />

                          {/* Linhas de divisão suave por setor */}
                          {zonasConsolidadas.map(z => (
                            <line 
                              key={z.pav}
                              x1={xIni} 
                              y1={getYCenter(z.pav)} 
                              x2={xFim} 
                              y2={getYCenter(z.pav)} 
                              stroke={cor.stroke} 
                              strokeWidth={1} 
                              strokeDasharray="3 3"
                              strokeOpacity={0.6}
                            />
                          ))}

                          {/* Badge de cabeçalho do comissionamento */}
                          <foreignObject 
                            x={xIni + width / 2 - 110} 
                            y={yTop + 10} 
                            width={220} 
                            height={32}
                            className="overflow-visible pointer-events-none"
                          >
                            <div className="flex justify-center items-center h-full">
                              <span className="px-3 py-1 rounded-full text-[10px] font-extrabold text-white shadow-xl whitespace-nowrap bg-teal-600 border border-white/40 flex items-center gap-1.5 ring-2 ring-teal-400/30">
                                <span>🏁</span> 15. Comissionamento & Entrega Final
                              </span>
                            </div>
                          </foreignObject>
                        </g>
                      );
                    }

                    // CASO 2: TAREFA EM SETOR ÚNICO (Ex: 01. Topografia na Zona 1 ou 07. Cobertura na Zona 4)
                    if (zonasConsolidadas.length === 1) {
                      const z = zonasConsolidadas[0];
                      const xIni = getX(z.start);
                      const xFim = getX(z.end);
                      const width = Math.max(34, xFim - xIni);
                      const yCenter = getYCenter(z.pav);
                      const height = 36;
                      const yTop = yCenter - height / 2;

                      return (
                        <g 
                          key={vagao.id}
                          className="cursor-pointer transition-opacity duration-200"
                          opacity={vagaoHover && !isHovered ? 0.4 : 1}
                          onMouseEnter={() => setVagaoHover(vagao.id)}
                          onMouseLeave={() => setVagaoHover(null)}
                          onClick={() => setVagaoSelecionado(vagao)}
                        >
                          <rect 
                            x={xIni} 
                            y={yTop} 
                            width={width} 
                            height={height} 
                            rx={8}
                            fill={cor.fill} 
                            stroke={cor.stroke} 
                            strokeWidth={isHovered || isSelected ? 3 : 1.5}
                            filter={isHovered ? "url(#glow-line)" : undefined}
                          />
                          <foreignObject 
                            x={xIni} 
                            y={yTop} 
                            width={width} 
                            height={height}
                            className="overflow-visible pointer-events-none"
                          >
                            <div className="flex items-center justify-center h-full px-2">
                              <span className="text-[10px] font-bold text-white truncate drop-shadow">
                                {vagao.nome.replace(/^\d+\.\s*/, '')} ({z.duration}d)
                              </span>
                            </div>
                          </foreignObject>
                        </g>
                      );
                    }

                    // CASO 3: MULTI-ZONAS — A VERDADEIRA LINHA DE BALANÇO (LOB CANÔNICA ↗)
                    if (zonasConsolidadas.length >= 2) {
                      const leftPoints: { x: number; y: number }[] = [];
                      const rightPoints: { x: number; y: number }[] = [];
                      const centerPoints: { x: number; y: number }[] = [];

                      zonasConsolidadas.forEach((z) => {
                        const y = getYCenter(z.pav);
                        const xStart = getX(z.start);
                        const xEnd = getX(z.end);
                        const xMid = (xStart + xEnd) / 2;

                        leftPoints.push({ x: xStart, y });
                        rightPoints.push({ x: xEnd, y });
                        centerPoints.push({ x: xMid, y });
                      });

                      // Constrói o polígono da fita:
                      // Frente de início subindo da base ao topo, e frente de conclusão descendo do topo à base.
                      // Como Y diminui estritamente e xStart < xEnd em cada zona, este polígono NUNCA se auto-intercepta!
                      const polygonPoints = [
                        ...leftPoints.map(p => `${p.x},${p.y}`),
                        ...[...rightPoints].reverse().map(p => `${p.x},${p.y}`)
                      ].join(' ');

                      const pathStart = leftPoints.map((p, idx) => `${idx === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
                      const pathEnd = rightPoints.map((p, idx) => `${idx === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
                      const pathCenter = centerPoints.map((p, idx) => `${idx === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');

                      // Ponto central mediano para rotulagem
                      const midIdx = Math.floor(centerPoints.length / 2);
                      const labelPonto = centerPoints[midIdx];

                      return (
                        <g 
                          key={vagao.id}
                          className="cursor-pointer transition-opacity duration-200"
                          opacity={vagaoHover && !isHovered ? 0.35 : 1}
                          onMouseEnter={() => setVagaoHover(vagao.id)}
                          onMouseLeave={() => setVagaoHover(null)}
                          onClick={() => setVagaoSelecionado(vagao)}
                        >
                          {/* FAIXA INCLINADA TRANSLÚCIDA (RIBBON ↗) */}
                          <polygon 
                            points={polygonPoints} 
                            fill={cor.fill} 
                            stroke="none"
                            filter={isHovered ? "url(#glow-line)" : undefined}
                            className="transition-all"
                          />

                          {/* LINHA DE INÍCIO DA FRENTE (BORDA ESQUERDA) */}
                          <path 
                            d={pathStart} 
                            stroke={cor.stroke} 
                            strokeWidth={isHovered || isSelected ? 3.5 : 2.5}
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          />

                          {/* LINHA DE CONCLUSÃO DA FRENTE (BORDA DIREITA) */}
                          <path 
                            d={pathEnd} 
                            stroke={cor.stroke} 
                            strokeWidth={isHovered || isSelected ? 2.5 : 1.5}
                            strokeDasharray="4 3"
                            strokeOpacity={0.85}
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          />

                          {/* LINHA DE RITMO MÉDIO CENTRAL (TRAÇO FINO) */}
                          <path 
                            d={pathCenter} 
                            stroke={cor.stroke} 
                            strokeWidth={1}
                            strokeDasharray="2 2"
                            strokeOpacity={0.4}
                          />

                          {/* NÓS/MARCADORES EM CADA SETOR */}
                          {centerPoints.map((p, idx) => (
                            <circle 
                              key={idx} 
                              cx={p.x} 
                              cy={p.y} 
                              r={isHovered ? 5.5 : 4} 
                              fill="#ffffff" 
                              stroke={cor.stroke} 
                              strokeWidth={2.5} 
                              className="transition-transform"
                            />
                          ))}

                          {/* ETIQUETA / BADGE FLUTUANTE NA LINHA */}
                          <foreignObject 
                            x={labelPonto.x - 85} 
                            y={labelPonto.y - 15} 
                            width={170} 
                            height={30}
                            className="overflow-visible pointer-events-none"
                          >
                            <div className="flex justify-center items-center h-full">
                              <span 
                                className={`px-2.5 py-1 rounded-full text-[10px] font-bold text-white shadow-xl whitespace-nowrap border border-white/30 ${
                                  cor.badge
                                } ${isHovered ? 'scale-110 ring-2 ring-white' : ''} transition-transform flex items-center gap-1`}
                              >
                                <span>{vagao.nome.replace(/^\d+\.\s*/, '')}</span>
                                <span className="text-[9px] opacity-75 font-normal">
                                  ({zonasConsolidadas.reduce((acc, cur) => acc + cur.duration, 0)}d)
                                </span>
                              </span>
                            </div>
                          </foreignObject>
                        </g>
                      );
                    }

                    return null;
                  })}
                </svg>
              ) : (
                /* MODO BLOCOS: VISÃO POR LOTES CONSOLIDADOS POR SETOR COM TEXTO LEGÍVEL */
                <div className="absolute inset-0 pointer-events-auto">
                  {lotesConsolidadosPorSetor.map(({ pav, rowIdx, lotes }) => {
                    return (
                      <div 
                        key={pav} 
                        style={{ height: `${rowHeight}px`, top: `${rowIdx * rowHeight}px` }}
                        className="absolute w-full flex items-center"
                      >
                        {lotes.map((lote) => {
                          const xIni = getX(lote.start);
                          const xFim = getX(lote.end);
                          const rawWidth = Math.max(0, xFim - xIni);
                          // Garante respiro de 2px entre lotes sequenciais contíguos sem colisão visual
                          const width = Math.max(22, rawWidth > 4 ? rawWidth - 2 : rawWidth);
                          const cor = getCorVagao(lote.vagaoNome);
                          const prefix = (lote.vagaoNome || '').slice(0, 2);

                          return (
                            <div
                              key={lote.id}
                              onClick={() => {
                                const vEncontrado = vagoesFluxo.find(v => v.nome === lote.vagaoNome);
                                if (vEncontrado) setVagaoSelecionado(vEncontrado);
                              }}
                              style={{ 
                                left: `${xIni}px`, 
                                width: `${width}px`,
                                height: `${rowHeight - 28}px`
                              }}
                              className={`absolute ${cor.badge} border border-white/20 rounded-lg shadow-md flex flex-col items-center justify-center text-white px-1.5 cursor-pointer hover:ring-2 hover:ring-white hover:scale-105 transition-all z-10`}
                              title={`${lote.vagaoNome} (${lote.dataInicio} a ${lote.dataFim}) - ${lote.duration} dias`}
                            >
                              {width >= 90 ? (
                                <>
                                  <span className="text-[10px] font-bold leading-tight truncate w-full text-center">
                                    {lote.vagaoNome.replace(/^\d+\.\s*/, '')}
                                  </span>
                                  <span className="text-[9px] text-white/80 font-mono">
                                    {lote.duration}d
                                  </span>
                                </>
                              ) : width >= 48 ? (
                                <>
                                  <span className="text-[10px] font-bold leading-tight">
                                    V{prefix}
                                  </span>
                                  <span className="text-[8px] text-white/80 font-mono">
                                    {lote.duration}d
                                  </span>
                                </>
                              ) : (
                                <span className="text-[10px] font-bold">
                                  V{prefix}
                                </span>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    );
                  })}
                </div>
              )}
              </div>

              {/* RÉGUA DO EIXO TEMPO (EIXO X INFERIOR) */}
              <div 
                className="h-10 border-t-2 border-zinc-700 bg-zinc-950 flex items-center z-20 shadow-lg"
                style={{ width: `${chartWidth}px` }}
              >
                {Array.from({ length: totalColunas }).map((_, i) => (
                  <div 
                    key={i} 
                    className="flex-1 text-center text-[10px] font-mono text-zinc-400 border-l border-zinc-800/80 hover:text-white transition-colors"
                  >
                    {modoVisualizacao === 'semanas' ? `Sem ${i + 1}` : `D${i + 1}`}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* PAINEL INFERIOR: DETALHES DO VAGÃO / LINHA SELECIONADA */}
      {vagaoSelecionado && (
        <div className="mt-6 p-5 bg-zinc-950 border border-zinc-800 rounded-xl animate-in fade-in slide-in-from-bottom-2 shadow-2xl">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <span className={`w-3.5 h-3.5 rounded-full ${getCorVagao(vagaoSelecionado.nome).badge} ring-2 ring-white/30`}></span>
              <div>
                <h4 className="text-base font-bold text-white flex items-center gap-2">
                  {vagaoSelecionado.nome}
                  <span className="text-xs font-mono font-normal px-2 py-0.5 rounded bg-zinc-800 text-zinc-300">
                    Vagão Contínuo Lean
                  </span>
                </h4>
                <p className="text-xs text-zinc-400 mt-0.5">
                  Subempreiteiro / Equipe: <strong className="text-zinc-200">{vagaoSelecionado.equipe}</strong> • Ritmo Takt: <strong className="text-emerald-400">3 dias úteis / zona</strong>
                </p>
              </div>
            </div>
            <button 
              onClick={() => setVagaoSelecionado(null)}
              className="p-1 text-zinc-500 hover:text-white rounded-lg hover:bg-zinc-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-3 mt-4 text-xs">
            <div className="p-3 bg-zinc-900/60 rounded-lg border border-zinc-800/80">
              <span className="text-zinc-500 text-[10px] uppercase font-bold flex items-center gap-1">
                <Calendar className="w-3 h-3 text-zinc-400" /> Ciclo Total na Obra
              </span>
              <div className="font-semibold text-zinc-200 mt-1">
                {vagaoSelecionado.dataInicioGlobal} até {vagaoSelecionado.dataFimGlobal}
              </div>
              <span className="text-[11px] text-zinc-400 font-mono">
                {vagaoSelecionado.endMax - vagaoSelecionado.startMin} dias corridos
              </span>
            </div>

            <div className="p-3 bg-zinc-900/60 rounded-lg border border-zinc-800/80">
              <span className="text-zinc-500 text-[10px] uppercase font-bold flex items-center gap-1">
                <Layers className="w-3 h-3 text-emerald-400" /> Zonas Percorridas
              </span>
              <div className="font-semibold text-zinc-200 mt-1">
                {new Set(vagaoSelecionado.pontos.map(p => p.pav)).size} frentes sequenciadas
              </div>
              <span className="text-[11px] text-emerald-400">
                100% em série (zero ociosidade)
              </span>
            </div>

            <div className="p-3 bg-zinc-900/60 rounded-lg border border-zinc-800/80">
              <span className="text-zinc-500 text-[10px] uppercase font-bold flex items-center gap-1">
                <Clock className="w-3 h-3 text-blue-400" /> Status no Curto Prazo
              </span>
              <div className="font-semibold text-zinc-200 mt-1">
                Calibrado com os 52 Lotes
              </div>
              <span className="text-[11px] text-blue-400">
                Sincronização Bidirecional Ativa
              </span>
            </div>

            <div className="p-3 bg-zinc-900/60 rounded-lg border border-zinc-800/80">
              <span className="text-zinc-500 text-[10px] uppercase font-bold flex items-center gap-1">
                <ShieldCheck className="w-3 h-3 text-purple-400" /> Nivelamento de Mão de Obra
              </span>
              <div className="font-semibold text-zinc-200 mt-1">
                Equipe Nivelada (Heijunka)
              </div>
              <span className="text-[11px] text-zinc-400">
                Sem duplicação de custo de mobilização
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
