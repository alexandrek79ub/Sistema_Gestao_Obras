"use client";

import React, { useState, useEffect } from 'react';
import { ZoomIn, ZoomOut, Maximize2, Minimize2 } from 'lucide-react';

export default function LinhaDeBalanco() {
  const [zoomX, setZoomX] = useState(1);
  const [zoomY, setZoomY] = useState(1);
  
  const [tarefas, setTarefas] = useState<any[]>([]);
  const [pavimentos, setPavimentos] = useState<string[]>([]);
  const [totalDias, setTotalDias] = useState(22);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/cronograma')
      .then(res => res.json())
      .then(data => {
        if (data.tarefas) {
          setTarefas(data.tarefas);
          setPavimentos(data.pavimentos);
          
          // Calcular totalDias dinâmico baseado na última tarefa
          let maxDay = 0;
          data.tarefas.forEach((t: any) => {
            const end = t.start + t.duration;
            if (end > maxDay) maxDay = end;
          });
          setTotalDias(Math.max(22, maxDay + 2)); // Pelo menos 22 dias, ou o maximo + 2
        }
        setLoading(false);
      })
      .catch(err => {
        console.error('Erro ao buscar cronograma', err);
        setLoading(false);
      });
  }, []);

  const handleZoomInX = () => setZoomX(prev => Math.min(prev + 0.5, 3));
  const handleZoomOutX = () => setZoomX(prev => Math.max(prev - 0.5, 0.5));
  const handleZoomInY = () => setZoomY(prev => Math.min(prev + 0.5, 3));
  const handleZoomOutY = () => setZoomY(prev => Math.max(prev - 0.5, 0.5));

  const baseWidth = totalDias * 35; // Aproximadamente 35px por dia
  const baseHeight = 40;

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 mt-6 overflow-hidden">
      <div className="flex flex-col md:flex-row md:justify-between items-start mb-6">
        <div className="mb-4 md:mb-0">
          <h3 className="text-lg font-semibold text-white mb-2">Linha de Balanço (Padrão de Mercado)</h3>
          <p className="text-sm text-zinc-400">Gantt por Pavimento com controles dinâmicos de escala espacial e temporal.</p>
        </div>
        
        <div className="flex flex-col space-y-3 items-end">
          {/* LEGENDA */}
          <div className="flex space-x-4 text-xs font-medium text-zinc-300">
            <div className="flex items-center"><span className="w-3 h-3 rounded-sm bg-blue-500 mr-2"></span>Estrutura</div>
            <div className="flex items-center"><span className="w-3 h-3 rounded-sm bg-amber-500 mr-2"></span>Alvenaria</div>
            <div className="flex items-center"><span className="w-3 h-3 rounded-sm bg-emerald-500 mr-2"></span>Hidráulica</div>
          </div>

          {/* CONTROLES DE ZOOM */}
          <div className="flex space-x-3">
            <div className="flex items-center space-x-2 bg-zinc-950/80 p-1.5 rounded-lg border border-zinc-800">
              <span className="text-[10px] text-zinc-500 ml-1 font-bold uppercase tracking-wider">Tempo (X)</span>
              <button onClick={handleZoomOutX} className="p-1 hover:bg-zinc-800 rounded text-zinc-400 hover:text-white transition-colors" title="Comprimir Tempo"><ZoomOut className="w-3.5 h-3.5" /></button>
              <span className="text-xs font-mono w-8 text-center text-zinc-300">{Math.round(zoomX * 100)}%</span>
              <button onClick={handleZoomInX} className="p-1 hover:bg-zinc-800 rounded text-zinc-400 hover:text-white transition-colors" title="Expandir Tempo"><ZoomIn className="w-3.5 h-3.5" /></button>
            </div>
            
            <div className="flex items-center space-x-2 bg-zinc-950/80 p-1.5 rounded-lg border border-zinc-800">
              <span className="text-[10px] text-zinc-500 ml-1 font-bold uppercase tracking-wider">Andar (Y)</span>
              <button onClick={handleZoomOutY} className="p-1 hover:bg-zinc-800 rounded text-zinc-400 hover:text-white transition-colors" title="Achatar Andares"><Minimize2 className="w-3.5 h-3.5" /></button>
              <span className="text-xs font-mono w-8 text-center text-zinc-300">{Math.round(zoomY * 100)}%</span>
              <button onClick={handleZoomInY} className="p-1 hover:bg-zinc-800 rounded text-zinc-400 hover:text-white transition-colors" title="Expandir Andares"><Maximize2 className="w-3.5 h-3.5" /></button>
            </div>
          </div>
        </div>
      </div>

      <div className="w-full overflow-x-auto pb-4 scrollbar-thin scrollbar-thumb-zinc-700 scrollbar-track-zinc-900">
        {loading ? (
          <div className="p-8 text-center text-zinc-500">Carregando dados da linha de balanço...</div>
        ) : (
          <div style={{ minWidth: `${baseWidth * zoomX}px` }} className="transition-all duration-300 ease-in-out">
            {/* HEADER DOS DIAS */}
            <div className="flex border-b border-zinc-800 pb-2 mb-4 ml-24">
              {Array.from({ length: totalDias }).map((_, i) => (
                <div key={i} className="flex-1 text-center text-xs text-zinc-500 font-mono border-l border-zinc-800/30">
                  {i + 1}
                </div>
              ))}
            </div>

            {/* MATRIZ DE PAVIMENTOS */}
            <div className="space-y-4">
              {pavimentos.map((pav) => (
                <div key={pav} className="flex items-center group">
                  <div className="w-24 text-sm font-medium text-zinc-400 group-hover:text-white transition-colors whitespace-nowrap overflow-hidden text-ellipsis mr-2">
                    {pav}
                  </div>
                  
                  {/* GRID DE DIAS DO PAVIMENTO */}
                  <div 
                    className="flex-1 grid gap-[2px] relative bg-zinc-950/30 rounded-md border border-zinc-800/50 p-1 transition-all duration-300 ease-in-out"
                    style={{ 
                      gridTemplateColumns: `repeat(${totalDias}, minmax(0, 1fr))`,
                      height: `${baseHeight * zoomY}px`
                    }}
                  >
                    {/* LINHAS GUIAS VERTICAIS */}
                    {Array.from({ length: totalDias }).map((_, i) => (
                      <div key={i} className="border-r border-dashed border-zinc-800/50 h-full absolute" style={{ left: `${(i + 1) * (100 / totalDias)}%` }}></div>
                    ))}

                    {/* RENDERIZAR OS BLOCOS (RETÂNGULOS) */}
                    {tarefas
                      .filter((t) => t.pav === pav)
                      .map((tarefa) => (
                        <div
                          key={tarefa.id}
                          className={`${tarefa.color} rounded shadow-[0_2px_10px_rgba(0,0,0,0.3)] flex items-center justify-center font-bold text-white/95 overflow-hidden relative z-10 transition-transform hover:scale-[1.02] cursor-pointer hover:shadow-lg`}
                          style={{
                            gridColumnStart: Math.max(1, tarefa.start),
                            gridColumnEnd: Math.max(1, tarefa.start) + tarefa.duration,
                            fontSize: `${Math.max(10, 12 * Math.min(zoomX, zoomY))}px`
                          }}
                          title={`${tarefa.tipo} no ${tarefa.pav} (Duração: ${tarefa.duration} dias, Início: Dia ${tarefa.start})`}
                        >
                          <span className="truncate px-1 tracking-wide drop-shadow-md">{tarefa.tipo}</span>
                        </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
