"use client";

import React, { useState, useEffect } from 'react';
import { ZoomIn, ZoomOut, Maximize2, Minimize2, Calendar, User, Clock, ArrowUpRight, CheckCircle2 } from 'lucide-react';
import { useObra } from '@/context/ObraContext';

interface TarefaLOB {
  id: number;
  pav: string;
  tipo: string;
  color: string;
  start: number;
  duration: number;
  equipe: string;
  dataInicio?: string;
  dataFim?: string;
}

export default function LinhaDeBalanco() {
  const { obraAtiva } = useObra();
  const [zoomX, setZoomX] = useState(1);
  const [zoomY, setZoomY] = useState(1);
  const [modoVisualizacao, setModoVisualizacao] = useState<'semanas' | 'dias'>('semanas');
  
  const [tarefas, setTarefas] = useState<TarefaLOB[]>([]);
  const [pavimentos, setPavimentos] = useState<string[]>([]);
  const [totalDias, setTotalDias] = useState(180);
  const [loading, setLoading] = useState(true);
  const [tarefaSelecionada, setTarefaSelecionada] = useState<TarefaLOB | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/cronograma?obra=${encodeURIComponent(obraAtiva)}`)
      .then(res => res.json())
      .then(data => {
        if (data.tarefas && data.tarefas.length > 0) {
          setTarefas(data.tarefas);
          setPavimentos(data.pavimentos || []);
          
          let maxDay = 0;
          data.tarefas.forEach((t: TarefaLOB) => {
            const end = t.start + t.duration;
            if (end > maxDay) maxDay = end;
          });
          setTotalDias(Math.max(180, maxDay));
        } else {
          setTarefas([]);
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
  const handleZoomInY = () => setZoomY(prev => Math.min(prev + 0.5, 3));
  const handleZoomOutY = () => setZoomY(prev => Math.max(prev - 0.5, 0.5));

  // Ordenação Clássica da Linha de Balanço (LOB):
  // Setor 05 (Cobertura) no TOPO, Setor 01 (Fundações/Cota Zero) na BASE.
  // Assim a obra sobe da esquerda para a direita no tempo (↗).
  const pavimentosOrdenados = [...pavimentos].sort().reverse();

  // Escala de Tempo: Semanas (26 semanas) ou Dias Corridos (180 dias)
  const totalSemanas = Math.ceil(totalDias / 7);
  const totalColunas = modoVisualizacao === 'semanas' ? totalSemanas : totalDias;
  
  const baseWidth = modoVisualizacao === 'semanas' 
    ? Math.max(900, totalColunas * 48)
    : Math.max(1200, totalColunas * 28);
  const baseHeight = 44;

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 overflow-hidden">
      {/* CABEÇALHO DO COMPONENTE */}
      <div className="flex flex-col lg:flex-row lg:justify-between items-start mb-6 gap-4">
        <div>
          <h3 className="text-lg font-semibold text-white mb-1 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            Linha de Balanço (LOB) — Fluxo Contínuo & Ritmo Construtivo
            <ArrowUpRight className="w-4 h-4 text-emerald-400" />
          </h3>
          <p className="text-sm text-zinc-400">
            Orientação padrão de engenharia: <span className="text-zinc-200 font-semibold">Setor 1 na base</span> e <span className="text-zinc-200 font-semibold">Setor 5 no topo</span>, com o tempo avançando no eixo X inferior (fluxo ascendente ↗).
          </p>
        </div>
        
        <div className="flex flex-wrap items-center gap-3">
          {/* SELETOR DE MODO DE ESCALA TEMPORAL */}
          <div className="bg-zinc-950 p-1 rounded-lg border border-zinc-800 flex items-center text-xs">
            <button
              onClick={() => setModoVisualizacao('semanas')}
              className={`px-3 py-1 rounded-md font-semibold transition-colors ${
                modoVisualizacao === 'semanas' 
                  ? 'bg-blue-600 text-white shadow-sm' 
                  : 'text-zinc-400 hover:text-white'
              }`}
            >
              26 Semanas (6 Meses)
            </button>
            <button
              onClick={() => setModoVisualizacao('dias')}
              className={`px-3 py-1 rounded-md font-semibold transition-colors ${
                modoVisualizacao === 'dias' 
                  ? 'bg-blue-600 text-white shadow-sm' 
                  : 'text-zinc-400 hover:text-white'
              }`}
            >
              180 Dias Corridos
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

      {/* LEGENDA DE DISCIPLINAS */}
      <div className="flex flex-wrap gap-4 text-xs font-medium text-zinc-300 bg-zinc-950/50 p-3 rounded-lg border border-zinc-800/80 mb-6">
        <span className="text-zinc-500 text-[11px] uppercase font-bold tracking-wider mr-1">Disciplinas:</span>
        <div className="flex items-center"><span className="w-3 h-3 rounded-sm bg-blue-600 mr-1.5"></span>Estruturas & Fundações</div>
        <div className="flex items-center"><span className="w-3 h-3 rounded-sm bg-amber-600 mr-1.5"></span>Alvenaria</div>
        <div className="flex items-center"><span className="w-3 h-3 rounded-sm bg-yellow-600 mr-1.5"></span>Elétrica & Lógica</div>
        <div className="flex items-center"><span className="w-3 h-3 rounded-sm bg-emerald-600 mr-1.5"></span>Hidráulica</div>
        <div className="flex items-center"><span className="w-3 h-3 rounded-sm bg-orange-600 mr-1.5"></span>Reboco & Emboço</div>
        <div className="flex items-center"><span className="w-3 h-3 rounded-sm bg-indigo-600 mr-1.5"></span>Acabamentos & Pisos</div>
        <div className="flex items-center"><span className="w-3 h-3 rounded-sm bg-purple-600 mr-1.5"></span>Pintura & Esquadrias</div>
        <div className="flex items-center"><span className="w-3 h-3 rounded-sm bg-cyan-600 mr-1.5"></span>Coberturas</div>
      </div>

      <div className="w-full overflow-x-auto pb-4 scrollbar-thin scrollbar-thumb-zinc-700 scrollbar-track-zinc-900">
        {loading ? (
          <div className="p-12 text-center text-zinc-400 flex flex-col items-center gap-3">
            <div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            <span>Carregando dados da Linha de Balanço ({obraAtiva})...</span>
          </div>
        ) : pavimentosOrdenados.length === 0 ? (
          <div className="p-12 text-center text-zinc-400 bg-zinc-950/40 rounded-lg border border-zinc-800">
            <p className="text-base font-semibold text-zinc-300">Nenhum pacote de Linha de Balanço configurado para {obraAtiva}.</p>
            <p className="text-sm text-zinc-500 mt-1">Verifique o arquivo LINHA_DE_BALANCO.csv na pasta 03_PLANEJAMENTO_E_CRONOGRAMA.</p>
          </div>
        ) : (
          <div style={{ minWidth: `${baseWidth * zoomX}px` }} className="transition-all duration-300 ease-in-out">
            {/* MATRIZ DE PAVIMENTOS / SETORES (SETOR 5 EM CIMA, SETOR 1 EMBAIXO) */}
            <div className="space-y-4">
              {pavimentosOrdenados.map((pav) => (
                <div key={pav} className="flex items-center group">
                  <div 
                    className="w-56 text-xs font-semibold text-zinc-300 group-hover:text-blue-400 transition-colors whitespace-nowrap overflow-hidden text-ellipsis mr-3 bg-zinc-950/60 px-2.5 py-1.5 rounded border border-zinc-800/80"
                    title={pav}
                  >
                    {pav}
                  </div>
                  
                  {/* GRID DO PAVIMENTO */}
                  <div 
                    className="flex-1 grid gap-[2px] relative bg-zinc-950/40 rounded-md border border-zinc-800/60 p-1 transition-all duration-300 ease-in-out"
                    style={{ 
                      gridTemplateColumns: `repeat(${totalColunas}, minmax(0, 1fr))`,
                      height: `${baseHeight * zoomY}px`
                    }}
                  >
                    {/* LINHAS GUIAS VERTICAIS */}
                    {Array.from({ length: totalColunas }).map((_, i) => (
                      <div key={i} className="border-r border-dashed border-zinc-800/40 h-full absolute pointer-events-none" style={{ left: `${(i + 1) * (100 / totalColunas)}%` }}></div>
                    ))}

                    {/* RENDERIZAR OS BLOCOS (RETÂNGULOS) */}
                    {tarefas
                      .filter((t) => t.pav === pav)
                      .map((tarefa) => {
                        const colStart = modoVisualizacao === 'semanas'
                          ? Math.max(1, Math.ceil(tarefa.start / 7))
                          : Math.max(1, tarefa.start);
                        
                        const colSpan = modoVisualizacao === 'semanas'
                          ? Math.max(1, Math.round(tarefa.duration / 7) || 1)
                          : Math.max(1, tarefa.duration);

                        return (
                          <div
                            key={tarefa.id}
                            onClick={() => setTarefaSelecionada(tarefa)}
                            className={`${tarefa.color} rounded shadow-md flex items-center justify-center font-semibold text-white/95 overflow-hidden relative z-10 transition-all hover:scale-[1.02] cursor-pointer hover:ring-2 hover:ring-white/80 hover:z-20`}
                            style={{
                              gridColumnStart: colStart,
                              gridColumnEnd: colStart + colSpan,
                              fontSize: `${Math.max(10, 11 * Math.min(zoomX, zoomY))}px`
                            }}
                            title={`${tarefa.tipo} — ${tarefa.pav}\nEquipe: ${tarefa.equipe}\nDuração: ${tarefa.duration} dias úteis (${tarefa.dataInicio} a ${tarefa.dataFim})`}
                          >
                            <span className="truncate px-1 tracking-wide drop-shadow">{tarefa.tipo}</span>
                          </div>
                        );
                      })}
                  </div>
                </div>
              ))}
            </div>

            {/* EIXO X INFERIOR: RÉGUA DE TEMPO NA BASE (PADRÃO CARTESIANO DE ENGENHARIA) */}
            <div className="flex border-t-2 border-zinc-700/80 pt-3 mt-4 ml-56">
              {Array.from({ length: totalColunas }).map((_, i) => (
                <div key={i} className="flex-1 text-center text-xs text-zinc-400 font-mono border-l border-zinc-800/60">
                  {modoVisualizacao === 'semanas' ? `Sem ${i + 1}` : `D${i + 1}`}
                </div>
              ))}
            </div>
            
            <div className="text-right text-[11px] text-zinc-500 font-mono mt-1 pr-2">
              {modoVisualizacao === 'semanas' 
                ? '← Eixo do Tempo: 26 Semanas (180 Dias Corridos / 6 Meses) →' 
                : '← Eixo do Tempo: 180 Dias Corridos de Produção Civil →'}
            </div>
          </div>
        )}
      </div>

      {/* MODAL / CARD DE DETALHE DA TAREFA SELECIONADA */}
      {tarefaSelecionada && (
        <div className="mt-6 bg-zinc-950 border border-blue-500/30 rounded-lg p-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className={`w-3 h-3 rounded-full ${tarefaSelecionada.color}`}></span>
              <h4 className="text-white font-bold text-sm">{tarefaSelecionada.tipo}</h4>
              <span className="text-xs bg-zinc-800 text-zinc-300 px-2 py-0.5 rounded font-mono">{tarefaSelecionada.pav}</span>
            </div>
            <div className="flex flex-wrap gap-4 text-xs text-zinc-400 pt-1">
              <span className="flex items-center gap-1"><User className="w-3.5 h-3.5 text-blue-400" /> {tarefaSelecionada.equipe}</span>
              <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5 text-amber-400" /> {tarefaSelecionada.duration} dias úteis</span>
              {tarefaSelecionada.dataInicio && (
                <span className="flex items-center gap-1"><Calendar className="w-3.5 h-3.5 text-emerald-400" /> {tarefaSelecionada.dataInicio} até {tarefaSelecionada.dataFim}</span>
              )}
            </div>
          </div>
          <button 
            onClick={() => setTarefaSelecionada(null)}
            className="text-xs text-zinc-400 hover:text-white bg-zinc-800 hover:bg-zinc-700 px-3 py-1.5 rounded transition-colors"
          >
            Fechar Detalhes
          </button>
        </div>
      )}
    </div>
  );
}
