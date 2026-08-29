"use client";

import React, { useState } from 'react';
import { ZoomIn, ZoomOut, Maximize2, Minimize2 } from 'lucide-react';

// Dados espelhando o TEMPLATE_LINHA_DE_BALANCO.csv
// Eixo Y: Pavimentos (01 a 03)
// Eixo X: Dias corridos (1 a 22)
const tarefas = [
  // PAVIMENTO 01
  { id: 1, pav: 'Pavimento 01', start: 1, duration: 5, tipo: 'Estrutura', color: 'bg-blue-500' },
  { id: 2, pav: 'Pavimento 01', start: 6, duration: 4, tipo: 'Alvenaria', color: 'bg-amber-500' },
  { id: 3, pav: 'Pavimento 01', start: 10, duration: 3, tipo: 'Hidráulica', color: 'bg-emerald-500' },
  
  // PAVIMENTO 02
  { id: 4, pav: 'Pavimento 02', start: 6, duration: 5, tipo: 'Estrutura', color: 'bg-blue-500' },
  { id: 5, pav: 'Pavimento 02', start: 11, duration: 4, tipo: 'Alvenaria', color: 'bg-amber-500' },
  { id: 6, pav: 'Pavimento 02', start: 15, duration: 3, tipo: 'Hidráulica', color: 'bg-emerald-500' },
  
  // PAVIMENTO 03
  { id: 7, pav: 'Pavimento 03', start: 11, duration: 5, tipo: 'Estrutura', color: 'bg-blue-500' },
  { id: 8, pav: 'Pavimento 03', start: 16, duration: 4, tipo: 'Alvenaria', color: 'bg-amber-500' },
  { id: 9, pav: 'Pavimento 03', start: 20, duration: 3, tipo: 'Hidráulica', color: 'bg-emerald-500' },
];

const pavimentos = ['Pavimento 03', 'Pavimento 02', 'Pavimento 01'];
const totalDias = 22;

export default function LinhaDeBalanco() {
  const [zoomX, setZoomX] = useState(1);
  const [zoomY, setZoomY] = useState(1);

  const handleZoomInX = () => setZoomX(prev => Math.min(prev + 0.5, 3));
  const handleZoomOutX = () => setZoomX(prev => Math.max(prev - 0.5, 0.5));
  const handleZoomInY = () => setZoomY(prev => Math.min(prev + 0.5, 3));
  const handleZoomOutY = () => setZoomY(prev => Math.max(prev - 0.5, 0.5));

  const baseWidth = 800;
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
                <div className="w-24 text-sm font-medium text-zinc-400 group-hover:text-white transition-colors whitespace-nowrap">
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
                          gridColumnStart: tarefa.start,
                          gridColumnEnd: tarefa.start + tarefa.duration,
                          fontSize: `${Math.max(10, 12 * Math.min(zoomX, zoomY))}px`
                        }}
                        title={`${tarefa.tipo} no ${tarefa.pav} (Duração: ${tarefa.duration} dias)`}
                      >
                        <span className="truncate px-1 tracking-wide drop-shadow-md">{tarefa.tipo}</span>
                      </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
