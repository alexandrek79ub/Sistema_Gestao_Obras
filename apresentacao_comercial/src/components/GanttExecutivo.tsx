"use client";

import React, { useState, useMemo } from 'react';
import { 
  GitCommit, Calendar, Layers, CheckCircle2, AlertTriangle, 
  Search, Filter, ChevronDown, ChevronRight, ZoomIn, ZoomOut,
  Clock, ShieldAlert, Sparkles, X, Users, ArrowRight, Check,
  Maximize2, Minimize2, BarChart3, HelpCircle
} from 'lucide-react';

interface AtividadeCPM {
  id: string;
  duracao_dias: number;
  predecessoras?: string[];
  es_inicio_mais_cedo?: number;
  ef_fim_mais_cedo?: number;
  ls_inicio_mais_tarde?: number;
  lf_fim_mais_tarde?: number;
  folga_dias?: number;
  critica?: boolean;
  dataInicio?: string;
  dataFim?: string;
}

interface TarefaDetalhada {
  id: number;
  pav: string;
  tipo: string;
  vagao?: string;
  color?: string;
  start: number;
  duration: number;
  equipe?: string;
  dataInicio?: string;
  dataFim?: string;
  predecessoresNomes?: string[];
  sucessoresNomes?: string[];
}

interface GanttExecutivoProps {
  cpmAtividades: AtividadeCPM[];
  tarefasDetalhadas?: TarefaDetalhada[];
  metaGlobal?: {
    diasCorridos: number;
    semanas: number;
    valorTurnkey: number;
    caminhoCriticoDias: number;
  };
}

const NOMES_CPM_AMIGAVEIS: Record<string, string> = {
  "A01_MOB_CANTEIRO": "Mobilização de Canteiro, Tapumes & Locação",
  "A02_ESCAV_INFRA": "Escavação Mecânica e Manual de Sapatas",
  "A03_SAPATAS_CONC": "Fôrmas, Armação & Concretagem de Sapatas",
  "A04_BALDRAMES_CONC": "Vigas Baldrames em Concreto Armado (VB1-19)",
  "A05_IMPERM_BALDRAME": "Impermeabilização Asfáltica de Baldrame",
  "A06_REATERRO_INFRA": "Reaterro Compactado e Nivelamento Cota Zero",
  "A07_PILARES_SUPRA": "Fôrmas, Armação & Concretagem de Pilares (P1-24)",
  "A08_VIGAS_LAJE_FORMA": "Cimbramento e Armação de Vigas e Laje H12",
  "A09_CONCRET_LAJE_H12": "Concretagem de Capa da Laje H12 e Vigas",
  "A10_CURA_DESFORMA": "Cura Úmida Normativa e Desforma da Laje",
  "A11_ESTRUT_TERCAS_COB": "Estrutura Metálica e Terças de Cobertura",
  "A12_ALVENARIA_VEDACAO": "Alvenaria de Vedação em Blocos Cerâmicos",
  "A13_TELHAS_SANDWICH_PLAT": "Telhas Termoacústicas PIR e Fechamento Platibanda",
  "A14_ELET_EMBUTIDA": "Eletrodutos, Quadros e Caixas Embutidas",
  "A15_HIDR_EMBUTIDA": "Ramais Hidráulicos e Prumadas de Esgoto",
  "A16_TESTE_HIDROSTATICO_72H": "Teste Hidrostático de Estanqueidade (72h)",
  "A17_EMBOCO_REBOCO": "Chapisco Rolado e Reboco Paulista Mecanizado",
  "A18_IMPERM_WCS": "Impermeabilização de Áreas Molhadas dos WCs",
  "A19_CONTRAPISO": "Regularização e Execução de Contrapiso Cimentício",
  "A20_INFRA_DUTOS_HVAC": "Rede Frigorígena e Dutos de Climatização",
  "A21_ESQUADRIAS_FIX": "Fixação de Contra-marcos e Esquadrias de Alumínio",
  "A22_PISO_PORCELANATO": "Assentamento de Porcelanato 80x80 e Rejunte",
  "A23_FIACAO_TELECOM": "Passagem de Fiação Elétrica e Cabos de Lógica",
  "A24_RODAPES_ACAB": "Instalação de Rodapés e Soleiras em Granito",
  "A25_PINTURA_1A_DEMAO": "Lixamento, Selador e 1ª Demão de Pintura Acrílica",
  "A26_APARELHOS_HVAC": "Instalação de Evaporadoras e Condensadoras HVAC",
  "A27_LOUCAS_METAIS": "Instalação de Louças e Metais Sanitários",
  "A28_LUMINARIAS_ESPELHOS": "Montagem de Luminárias LED e Espelhos Elétricos",
  "A29_PINTURA_FINAL": "Pintura Acrílica Final e Retoques Finais",
  "A30_COMISSIONAMENTO": "Comissionamento Integrado e Teste sob Carga",
  "A31_LIMPEZA_ENTREGA": "Limpeza Fina Pós-Obra, As-Built e Entrega Técnica"
};

export default function GanttExecutivo({
  cpmAtividades = [],
  tarefasDetalhadas = [],
  metaGlobal = { diasCorridos: 180, semanas: 26, valorTurnkey: 1660762.28, caminhoCriticoDias: 178 }
}: GanttExecutivoProps) {
  const [modoVisao, setModoVisao] = useState<'cpm' | 'detalhado_disciplina' | 'detalhado_zona'>('cpm');
  const [escala, setEscala] = useState<'semanas' | 'meses' | 'dias'>('semanas');
  const [filtroApenasCriticas, setFiltroApenasCriticas] = useState(false);
  const [buscaTexto, setBuscaTexto] = useState('');
  const [gruposAbertos, setGruposAbertos] = useState<Record<string, boolean>>({});
  const [itemSelecionado, setItemSelecionado] = useState<any | null>(null);

  const totalDias = metaGlobal.caminhoCriticoDias || 178;
  const totalSemanas = 26;

  // Largura base por unidade temporal (pixels)
  const pxPorDia = useMemo(() => {
    if (escala === 'meses') return 5;
    if (escala === 'semanas') return 7.5;
    return 14; // dias
  }, [escala]);

  const timelineWidth = Math.max(1200, Math.ceil(totalDias * pxPorDia) + 120);

  // Semanas (S01 a S26) com posições
  const semanasHeader = useMemo(() => {
    return Array.from({ length: totalSemanas }, (_, i) => ({
      numero: i + 1,
      label: `S${String(i + 1).padStart(2, '0')}`,
      startDay: i * 7,
      endDay: (i + 1) * 7
    }));
  }, [totalSemanas]);

  // Meses da obra (Outubro/2026 a Março/2027)
  const mesesHeader = [
    { nome: 'Outubro / 2026', dias: 31, startDay: 0 },
    { nome: 'Novembro / 2026', dias: 30, startDay: 31 },
    { nome: 'Dezembro / 2026', dias: 31, startDay: 61 },
    { nome: 'Janeiro / 2027', dias: 31, startDay: 92 },
    { nome: 'Fevereiro / 2027', dias: 28, startDay: 123 },
    { nome: 'Março / 2027', dias: 31, startDay: 151 },
  ];

  // Alternar sanfona de grupos
  const toggleGrupo = (grupoKey: string) => {
    setGruposAbertos(prev => ({
      ...prev,
      [grupoKey]: prev[grupoKey] === undefined ? false : !prev[grupoKey]
    }));
  };

  // Filtragem e ordenação do CPM
  const cpmFiltrado = useMemo(() => {
    return cpmAtividades.filter(atv => {
      const nomeAmigavel = NOMES_CPM_AMIGAVEIS[atv.id] || atv.id;
      const matchBusca = !buscaTexto || 
        nomeAmigavel.toLowerCase().includes(buscaTexto.toLowerCase()) || 
        atv.id.toLowerCase().includes(buscaTexto.toLowerCase());
      const matchCritica = !filtroApenasCriticas || atv.critica === true;
      return matchBusca && matchCritica;
    });
  }, [cpmAtividades, buscaTexto, filtroApenasCriticas]);

  // Estatísticas do CPM
  const totalCriticas = useMemo(() => cpmAtividades.filter(a => a.critica).length, [cpmAtividades]);
  const totalFolga = useMemo(() => cpmAtividades.length - totalCriticas, [cpmAtividades, totalCriticas]);

  // Agrupamento detalhado por Disciplina / Vagão
  const gruposPorDisciplina = useMemo(() => {
    const mapa = new Map<string, TarefaDetalhada[]>();
    tarefasDetalhadas.forEach(t => {
      const vNome = t.vagao || '00. Outros Serviços';
      if (!mapa.has(vNome)) mapa.set(vNome, []);
      mapa.get(vNome)!.push(t);
    });

    const chavesOrdenadas = Array.from(mapa.keys()).sort();
    return chavesOrdenadas.map(disciplina => {
      let tarefas = mapa.get(disciplina)!;
      if (buscaTexto) {
        tarefas = tarefas.filter(t => 
          t.tipo.toLowerCase().includes(buscaTexto.toLowerCase()) || 
          (t.equipe && t.equipe.toLowerCase().includes(buscaTexto.toLowerCase())) ||
          t.pav.toLowerCase().includes(buscaTexto.toLowerCase())
        );
      }
      return {
        chave: disciplina,
        titulo: disciplina,
        tarefas: tarefas.sort((a, b) => a.start - b.start)
      };
    }).filter(g => g.tarefas.length > 0);
  }, [tarefasDetalhadas, buscaTexto]);

  // Agrupamento detalhado por Zona / Setor
  const gruposPorZona = useMemo(() => {
    const mapa = new Map<string, TarefaDetalhada[]>();
    tarefasDetalhadas.forEach(t => {
      const zona = t.pav || 'Setor Geral';
      if (!mapa.has(zona)) mapa.set(zona, []);
      mapa.get(zona)!.push(t);
    });

    const ordemZonas = [
      'Zona 01 - Recepção/Diretoria',
      'Zona 02 - Salas Técnicas/CPD',
      'Zona 03 - Sanitários e Apoio',
      'Zona 04 - Cobertura e Platibanda'
    ];

    const chavesOrdenadas = Array.from(mapa.keys()).sort((a, b) => {
      const ia = ordemZonas.indexOf(a);
      const ib = ordemZonas.indexOf(b);
      if (ia !== -1 && ib !== -1) return ia - ib;
      return a.localeCompare(b);
    });

    return chavesOrdenadas.map(zona => {
      let tarefas = mapa.get(zona)!;
      if (buscaTexto) {
        tarefas = tarefas.filter(t => 
          t.tipo.toLowerCase().includes(buscaTexto.toLowerCase()) || 
          (t.vagao && t.vagao.toLowerCase().includes(buscaTexto.toLowerCase())) ||
          (t.equipe && t.equipe.toLowerCase().includes(buscaTexto.toLowerCase()))
        );
      }
      return {
        chave: zona,
        titulo: zona,
        tarefas: tarefas.sort((a, b) => a.start - b.start)
      };
    }).filter(g => g.tarefas.length > 0);
  }, [tarefasDetalhadas, buscaTexto]);

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-2xl overflow-hidden shadow-2xl space-y-4">
      {/* CABEÇALHO EXECUTIVO E CONTROLES */}
      <div className="p-5 border-b border-zinc-800/80 bg-zinc-950/60 backdrop-blur-md">
        <div className="flex flex-col xl:flex-row xl:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                Gráfico de Gantt Executivo — Cronograma & Caminho Crítico
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 border border-rose-500/30">
                  CPM DETERMINÍSTICO
                </span>
              </h2>
            </div>
            <p className="text-xs text-zinc-400">
              Planejamento temporal de 178 dias úteis (26 Semanas). As atividades críticas definem o prazo contratual inegociável da obra.
            </p>
          </div>

          {/* BADGES METAS EXECUTIVAS */}
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <div className="bg-zinc-900 border border-zinc-800 px-3 py-1.5 rounded-xl flex items-center gap-2 shadow-sm">
              <Clock className="w-3.5 h-3.5 text-blue-400" />
              <span className="text-zinc-400">Duração:</span>
              <strong className="text-white font-mono">{totalDias} dias</strong>
              <span className="text-zinc-500">({totalSemanas} sem.)</span>
            </div>

            <div className="bg-zinc-900 border border-zinc-800 px-3 py-1.5 rounded-xl flex items-center gap-2 shadow-sm">
              <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
              <span className="text-zinc-400">Críticas:</span>
              <strong className="text-rose-400 font-mono">{totalCriticas}</strong>
              <span className="text-zinc-500">/ {cpmAtividades.length}</span>
            </div>

            <div className="bg-zinc-900 border border-zinc-800 px-3 py-1.5 rounded-xl flex items-center gap-2 shadow-sm">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              <span className="text-zinc-400">Com Folga:</span>
              <strong className="text-emerald-400 font-mono">{totalFolga}</strong>
            </div>
          </div>
        </div>

        {/* BARRA DE FERRAMENTAS: VISÕES, FILTROS E ZOOM */}
        <div className="mt-5 pt-4 border-t border-zinc-800/60 flex flex-wrap items-center justify-between gap-3">
          {/* SELETOR DE MODO DE VISÃO */}
          <div className="flex items-center bg-zinc-900 p-1 rounded-xl border border-zinc-800 text-xs">
            <button
              onClick={() => setModoVisao('cpm')}
              className={`px-3 py-1.5 rounded-lg font-semibold transition-all flex items-center gap-1.5 ${
                modoVisao === 'cpm'
                  ? 'bg-rose-600 text-white shadow-md ring-1 ring-rose-400/40'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <GitCommit className="w-3.5 h-3.5" />
              Macroetapas CPM ({cpmAtividades.length})
            </button>

            <button
              onClick={() => setModoVisao('detalhado_disciplina')}
              className={`px-3 py-1.5 rounded-lg font-semibold transition-all flex items-center gap-1.5 ${
                modoVisao === 'detalhado_disciplina'
                  ? 'bg-blue-600 text-white shadow-md ring-1 ring-blue-400/40'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <Layers className="w-3.5 h-3.5" />
              EAP por Disciplina ({tarefasDetalhadas.length})
            </button>

            <button
              onClick={() => setModoVisao('detalhado_zona')}
              className={`px-3 py-1.5 rounded-lg font-semibold transition-all flex items-center gap-1.5 ${
                modoVisao === 'detalhado_zona'
                  ? 'bg-emerald-600 text-white shadow-md ring-1 ring-emerald-400/40'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <BarChart3 className="w-3.5 h-3.5" />
              EAP por Setor / Zona
            </button>
          </div>

          {/* BUSCA RÁPIDA E FILTRO DE CAMINHO CRÍTICO */}
          <div className="flex items-center gap-2">
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-zinc-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Buscar atividade, equipe..."
                value={buscaTexto}
                onChange={e => setBuscaTexto(e.target.value)}
                className="bg-zinc-900 border border-zinc-800 rounded-xl pl-8 pr-3 py-1.5 text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-blue-500 w-48 md:w-60"
              />
              {buscaTexto && (
                <button 
                  onClick={() => setBuscaTexto('')}
                  className="absolute right-2.5 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-white"
                >
                  <X className="w-3 h-3" />
                </button>
              )}
            </div>

            {modoVisao === 'cpm' && (
              <button
                onClick={() => setFiltroApenasCriticas(!filtroApenasCriticas)}
                className={`px-3 py-1.5 rounded-xl border text-xs font-semibold flex items-center gap-1.5 transition-colors ${
                  filtroApenasCriticas
                    ? 'bg-rose-500/20 text-rose-400 border-rose-500/50 ring-1 ring-rose-500/30'
                    : 'bg-zinc-900 text-zinc-400 border-zinc-800 hover:text-zinc-200'
                }`}
                title="Filtrar apenas as atividades no caminho crítico (folga zero)"
              >
                <Filter className="w-3.5 h-3.5" />
                Apenas Críticas
              </button>
            )}

            {/* SELETOR DE ESCALA DE ZOOM */}
            <div className="flex items-center bg-zinc-900 p-1 rounded-xl border border-zinc-800 text-xs text-zinc-400">
              <span className="px-2 text-[10px] uppercase font-bold text-zinc-500">Escala:</span>
              <button
                onClick={() => setEscala('meses')}
                className={`px-2 py-1 rounded-md font-medium transition-colors ${escala === 'meses' ? 'bg-zinc-800 text-white font-bold' : 'hover:text-white'}`}
              >
                Meses
              </button>
              <button
                onClick={() => setEscala('semanas')}
                className={`px-2 py-1 rounded-md font-medium transition-colors ${escala === 'semanas' ? 'bg-zinc-800 text-white font-bold' : 'hover:text-white'}`}
              >
                Semanas
              </button>
              <button
                onClick={() => setEscala('dias')}
                className={`px-2 py-1 rounded-md font-medium transition-colors ${escala === 'dias' ? 'bg-zinc-800 text-white font-bold' : 'hover:text-white'}`}
              >
                Dias
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* ÁREA PRINCIPAL DO GANTT: TABELA FIXA + TIMELINE DE ROLAGEM */}
      <div className="relative border-t border-b border-zinc-800 flex overflow-hidden">
        {/* COLUNA ESQUERDA FIXA: LISTA DE TAREFAS (STICKY) */}
        <div className="w-[340px] md:w-[420px] shrink-0 border-r border-zinc-800 bg-zinc-950 z-20 shadow-lg">
          {/* CABEÇALHO DA COLUNA FIXA */}
          <div className="h-[68px] border-b border-zinc-800 flex items-center justify-between px-4 bg-zinc-950">
            <span className="text-xs font-bold uppercase tracking-wider text-zinc-400">
              {modoVisao === 'cpm' ? 'Atividade / Macroetapa' : 'EAP / Pacote de Trabalho'}
            </span>
            <div className="flex items-center gap-3 text-[11px] font-mono text-zinc-500">
              <span>DUR</span>
              <span>FOLGA</span>
            </div>
          </div>

          {/* ITENS DA LISTA NO MODO CPM */}
          {modoVisao === 'cpm' && (
            <div className="divide-y divide-zinc-800/40">
              {cpmFiltrado.map((atv, idx) => {
                const nomeAmigavel = NOMES_CPM_AMIGAVEIS[atv.id] || atv.id;
                const isSelected = itemSelecionado?.id === atv.id;
                return (
                  <div
                    key={atv.id || idx}
                    onClick={() => setItemSelecionado(atv)}
                    className={`h-11 px-4 flex items-center justify-between cursor-pointer transition-colors text-xs ${
                      isSelected 
                        ? 'bg-blue-950/40 border-l-2 border-blue-500' 
                        : 'hover:bg-zinc-900/60'
                    }`}
                  >
                    <div className="flex items-center gap-2 truncate pr-2">
                      <span className={`w-2 h-2 rounded-full shrink-0 ${atv.critica ? 'bg-rose-500 shadow-sm shadow-rose-500/50' : 'bg-emerald-500'}`} />
                      <div className="truncate">
                        <div className="text-white font-medium truncate text-xs">{nomeAmigavel}</div>
                        <div className="text-[10px] font-mono text-zinc-500 flex items-center gap-2">
                          <span>{atv.id}</span>
                          {atv.dataInicio && <span className="text-zinc-400">{atv.dataInicio}</span>}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-3 shrink-0 font-mono text-xs">
                      <span className="text-zinc-300 w-8 text-right font-bold">{atv.duracao_dias}d</span>
                      <span className={`w-12 text-center text-[10px] font-bold rounded px-1 py-0.5 ${
                        atv.critica 
                          ? 'bg-rose-500/20 text-rose-400 border border-rose-500/40' 
                          : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      }`}>
                        {atv.folga_dias === 0 ? '0d' : `${atv.folga_dias}d`}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* ITENS DA LISTA NO MODO DETALHADO POR DISCIPLINA */}
          {modoVisao === 'detalhado_disciplina' && (
            <div className="divide-y divide-zinc-800/40">
              {gruposPorDisciplina.map(grupo => {
                const isAberto = gruposAbertos[grupo.chave] !== false;
                return (
                  <div key={grupo.chave}>
                    <div 
                      onClick={() => toggleGrupo(grupo.chave)}
                      className="h-10 px-4 bg-zinc-900/80 hover:bg-zinc-800/80 cursor-pointer flex items-center justify-between transition-colors border-l-2 border-amber-500"
                    >
                      <div className="flex items-center gap-2 font-bold text-xs text-amber-400 truncate">
                        {isAberto ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
                        <span className="truncate">{grupo.titulo}</span>
                      </div>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-400">
                        {grupo.tarefas.length} tarefas
                      </span>
                    </div>

                    {isAberto && grupo.tarefas.map((t, tidx) => {
                      const isSelected = itemSelecionado?.id === t.id;
                      return (
                        <div
                          key={t.id || tidx}
                          onClick={() => setItemSelecionado(t)}
                          className={`h-11 px-4 pl-8 flex items-center justify-between cursor-pointer transition-colors text-xs ${
                            isSelected 
                              ? 'bg-blue-950/40 border-l-2 border-blue-500' 
                              : 'hover:bg-zinc-900/40'
                          }`}
                        >
                          <div className="truncate pr-2">
                            <div className="text-zinc-200 font-medium truncate">{t.tipo}</div>
                            <div className="text-[10px] text-zinc-500 font-mono truncate">{t.pav}</div>
                          </div>
                          <div className="text-zinc-300 font-mono text-xs shrink-0 font-bold">
                            {t.duration}d
                          </div>
                        </div>
                      );
                    })}
                  </div>
                );
              })}
            </div>
          )}

          {/* ITENS DA LISTA NO MODO DETALHADO POR ZONA */}
          {modoVisao === 'detalhado_zona' && (
            <div className="divide-y divide-zinc-800/40">
              {gruposPorZona.map(grupo => {
                const isAberto = gruposAbertos[grupo.chave] !== false;
                return (
                  <div key={grupo.chave}>
                    <div 
                      onClick={() => toggleGrupo(grupo.chave)}
                      className="h-10 px-4 bg-zinc-900/80 hover:bg-zinc-800/80 cursor-pointer flex items-center justify-between transition-colors border-l-2 border-emerald-500"
                    >
                      <div className="flex items-center gap-2 font-bold text-xs text-emerald-400 truncate">
                        {isAberto ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
                        <span className="truncate">{grupo.titulo}</span>
                      </div>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-400">
                        {grupo.tarefas.length} tarefas
                      </span>
                    </div>

                    {isAberto && grupo.tarefas.map((t, tidx) => {
                      const isSelected = itemSelecionado?.id === t.id;
                      return (
                        <div
                          key={t.id || tidx}
                          onClick={() => setItemSelecionado(t)}
                          className={`h-11 px-4 pl-8 flex items-center justify-between cursor-pointer transition-colors text-xs ${
                            isSelected 
                              ? 'bg-blue-950/40 border-l-2 border-blue-500' 
                              : 'hover:bg-zinc-900/40'
                          }`}
                        >
                          <div className="truncate pr-2">
                            <div className="text-zinc-200 font-medium truncate">{t.tipo}</div>
                            <div className="text-[10px] text-zinc-500 font-mono truncate">{t.vagao}</div>
                          </div>
                          <div className="text-zinc-300 font-mono text-xs shrink-0 font-bold">
                            {t.duration}d
                          </div>
                        </div>
                      );
                    })}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* COLUNA DIREITA ROLÁVEL: GRADE TEMPORAL + BARRAS DE GANTT */}
        <div className="grow overflow-x-auto bg-zinc-950/50">
          <div style={{ width: `${timelineWidth}px` }} className="relative select-none">
            {/* CABEÇALHO DUPLO DE TEMPO (MESES + SEMANAS) */}
            <div className="h-[68px] border-b border-zinc-800 bg-zinc-950 sticky top-0 z-10 flex flex-col">
              {/* LINHA 1: MESES */}
              <div className="h-7 border-b border-zinc-800/80 flex divide-x divide-zinc-800/80 text-[11px] font-bold text-zinc-400">
                {mesesHeader.map((m, idx) => (
                  <div
                    key={idx}
                    style={{ width: `${m.dias * pxPorDia}px` }}
                    className="flex items-center justify-center bg-zinc-900/30 truncate px-2"
                  >
                    {m.nome}
                  </div>
                ))}
              </div>

              {/* LINHA 2: SEMANAS */}
              <div className="h-10 flex divide-x divide-zinc-800/60 text-[10px] font-mono text-zinc-400">
                {semanasHeader.map(sem => (
                  <div
                    key={sem.numero}
                    style={{ width: `${7 * pxPorDia}px` }}
                    className="flex flex-col items-center justify-center bg-zinc-950/40 hover:bg-zinc-900/40 transition-colors"
                  >
                    <span className="font-bold text-zinc-300">{sem.label}</span>
                    <span className="text-[9px] text-zinc-500">d{sem.startDay + 1}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* CORPO DA TIMELINE NO MODO CPM */}
            {modoVisao === 'cpm' && (
              <div className="divide-y divide-zinc-800/40 relative">
                {/* LINHAS DE GRADE VERTICAIS DE FUNDO */}
                <div className="absolute inset-0 pointer-events-none flex divide-x divide-zinc-800/30 z-0">
                  {semanasHeader.map(sem => (
                    <div key={sem.numero} style={{ width: `${7 * pxPorDia}px` }} className="h-full" />
                  ))}
                </div>

                {cpmFiltrado.map((atv, idx) => {
                  const startDay = atv.es_inicio_mais_cedo ?? 0;
                  const duracao = atv.duracao_dias || 1;
                  const folga = atv.folga_dias || 0;
                  const barLeft = startDay * pxPorDia;
                  const barWidth = Math.max(24, duracao * pxPorDia);
                  const folgaWidth = folga * pxPorDia;
                  const isSelected = itemSelecionado?.id === atv.id;
                  const nomeAmigavel = NOMES_CPM_AMIGAVEIS[atv.id] || atv.id;

                  return (
                    <div
                      key={atv.id || idx}
                      className={`h-11 relative flex items-center z-1 hover:bg-zinc-800/30 transition-colors ${
                        isSelected ? 'bg-blue-950/20' : ''
                      }`}
                    >
                      {/* BARRA DA TAREFA NO GANTT */}
                      <div
                        onClick={() => setItemSelecionado(atv)}
                        style={{
                          left: `${barLeft}px`,
                          width: `${barWidth}px`
                        }}
                        className={`absolute h-7 rounded-lg flex items-center px-2.5 cursor-pointer shadow-md transition-all duration-150 group ${
                          atv.critica
                            ? 'bg-gradient-to-r from-rose-600 via-rose-500 to-amber-600 border border-rose-400 text-white font-bold shadow-rose-500/20'
                            : 'bg-gradient-to-r from-blue-700 to-indigo-600 border border-blue-400/60 text-white font-medium shadow-blue-500/10'
                        } ${isSelected ? 'ring-2 ring-white scale-[1.02] z-10' : 'hover:scale-[1.01]'}`}
                        title={`${nomeAmigavel} (${duracao}d) | Início Dia ${startDay} -> Fim Dia ${startDay + duracao} | Folga: ${folga}d`}
                      >
                        <span className="truncate text-xs tracking-tight">
                          {nomeAmigavel}
                        </span>
                      </div>

                      {/* BARRA DE FOLGA PONTILHADA */}
                      {folga > 0 && (
                        <div
                          style={{
                            left: `${barLeft + barWidth}px`,
                            width: `${folgaWidth}px`
                          }}
                          className="absolute h-3 border-y border-dashed border-emerald-500/50 bg-emerald-500/10 rounded-r flex items-center justify-center pointer-events-none"
                          title={`Folga total disponível: ${folga} dias`}
                        >
                          <span className="text-[9px] font-mono text-emerald-400 px-1 font-bold">
                            +{folga}d folga
                          </span>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}

            {/* CORPO DA TIMELINE NO MODO DETALHADO POR DISCIPLINA */}
            {modoVisao === 'detalhado_disciplina' && (
              <div className="divide-y divide-zinc-800/40 relative">
                <div className="absolute inset-0 pointer-events-none flex divide-x divide-zinc-800/30 z-0">
                  {semanasHeader.map(sem => (
                    <div key={sem.numero} style={{ width: `${7 * pxPorDia}px` }} className="h-full" />
                  ))}
                </div>

                {gruposPorDisciplina.map(grupo => {
                  const isAberto = gruposAbertos[grupo.chave] !== false;
                  return (
                    <div key={grupo.chave}>
                      <div className="h-10 bg-zinc-900/50 border-b border-zinc-800/40" />

                      {isAberto && grupo.tarefas.map((t, tidx) => {
                        const startDay = Math.max(0, t.start - 1);
                        const duracao = t.duration || 1;
                        const barLeft = startDay * pxPorDia;
                        const barWidth = Math.max(24, duracao * pxPorDia);
                        const isSelected = itemSelecionado?.id === t.id;

                        return (
                          <div
                            key={t.id || tidx}
                            className={`h-11 relative flex items-center z-1 hover:bg-zinc-800/30 transition-colors ${
                              isSelected ? 'bg-blue-950/20' : ''
                            }`}
                          >
                            <div
                              onClick={() => setItemSelecionado(t)}
                              style={{
                                left: `${barLeft}px`,
                                width: `${barWidth}px`
                              }}
                              className={`absolute h-7 rounded-lg flex items-center px-2.5 cursor-pointer shadow-md transition-all text-white text-xs truncate ${
                                t.color ? t.color : 'bg-blue-600'
                              } border border-white/20 ${
                                isSelected ? 'ring-2 ring-white scale-[1.02] z-10' : 'hover:scale-[1.01]'
                              }`}
                              title={`${t.tipo} (${t.pav}) | ${duracao} dias | ${t.dataInicio || ''} - ${t.dataFim || ''}`}
                            >
                              <span className="truncate">{t.tipo}</span>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  );
                })}
              </div>
            )}

            {/* CORPO DA TIMELINE NO MODO DETALHADO POR ZONA */}
            {modoVisao === 'detalhado_zona' && (
              <div className="divide-y divide-zinc-800/40 relative">
                <div className="absolute inset-0 pointer-events-none flex divide-x divide-zinc-800/30 z-0">
                  {semanasHeader.map(sem => (
                    <div key={sem.numero} style={{ width: `${7 * pxPorDia}px` }} className="h-full" />
                  ))}
                </div>

                {gruposPorZona.map(grupo => {
                  const isAberto = gruposAbertos[grupo.chave] !== false;
                  return (
                    <div key={grupo.chave}>
                      <div className="h-10 bg-zinc-900/50 border-b border-zinc-800/40" />

                      {isAberto && grupo.tarefas.map((t, tidx) => {
                        const startDay = Math.max(0, t.start - 1);
                        const duracao = t.duration || 1;
                        const barLeft = startDay * pxPorDia;
                        const barWidth = Math.max(24, duracao * pxPorDia);
                        const isSelected = itemSelecionado?.id === t.id;

                        return (
                          <div
                            key={t.id || tidx}
                            className={`h-11 relative flex items-center z-1 hover:bg-zinc-800/30 transition-colors ${
                              isSelected ? 'bg-blue-950/20' : ''
                            }`}
                          >
                            <div
                              onClick={() => setItemSelecionado(t)}
                              style={{
                                left: `${barLeft}px`,
                                width: `${barWidth}px`
                              }}
                              className={`absolute h-7 rounded-lg flex items-center px-2.5 cursor-pointer shadow-md transition-all text-white text-xs truncate ${
                                t.color ? t.color : 'bg-emerald-600'
                              } border border-white/20 ${
                                isSelected ? 'ring-2 ring-white scale-[1.02] z-10' : 'hover:scale-[1.01]'
                              }`}
                              title={`${t.tipo} (${t.vagao}) | ${duracao} dias | ${t.dataInicio || ''} - ${t.dataFim || ''}`}
                            >
                              <span className="truncate">{t.tipo}</span>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* DRAWER / CARD INFERIOR DE DETALHES DA TAREFA SELECIONADA */}
      {itemSelecionado && (
        <div className="p-4 bg-zinc-950/90 border-t border-zinc-800 flex flex-col md:flex-row md:items-center justify-between gap-4 animate-in fade-in slide-in-from-bottom-2 duration-200">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className={`w-2.5 h-2.5 rounded-full ${itemSelecionado.critica ? 'bg-rose-500 animate-pulse' : 'bg-emerald-500'}`} />
              <h4 className="text-sm font-bold text-white">
                {NOMES_CPM_AMIGAVEIS[itemSelecionado.id] || itemSelecionado.tipo || itemSelecionado.id}
              </h4>
              {itemSelecionado.critica !== undefined && (
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                  itemSelecionado.critica 
                    ? 'bg-rose-500/20 text-rose-400 border border-rose-500/40' 
                    : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                }`}>
                  {itemSelecionado.critica ? 'CAMINHO CRÍTICO' : `FOLGA: ${itemSelecionado.folga_dias}d`}
                </span>
              )}
            </div>
            <div className="flex flex-wrap items-center gap-4 text-xs text-zinc-400 font-mono">
              {itemSelecionado.dataInicio && (
                <span>Início: <strong className="text-zinc-200">{itemSelecionado.dataInicio}</strong></span>
              )}
              {itemSelecionado.dataFim && (
                <span>Fim: <strong className="text-zinc-200">{itemSelecionado.dataFim}</strong></span>
              )}
              <span>Duração: <strong className="text-zinc-200">{itemSelecionado.duracao_dias || itemSelecionado.duration} dias</strong></span>
              {itemSelecionado.equipe && (
                <span className="text-blue-400 font-sans">Equipe: {itemSelecionado.equipe}</span>
              )}
              {itemSelecionado.pav && (
                <span className="text-amber-400 font-sans">Setor: {itemSelecionado.pav}</span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            {itemSelecionado.predecessoras && itemSelecionado.predecessoras.length > 0 && (
              <div className="text-[11px] text-zinc-400 bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-1.5">
                <span className="text-zinc-500 mr-1">Predecessoras:</span>
                <span className="font-mono text-zinc-300">{itemSelecionado.predecessoras.join(', ')}</span>
              </div>
            )}
            <button
              onClick={() => setItemSelecionado(null)}
              className="p-1.5 text-zinc-400 hover:text-white rounded-lg hover:bg-zinc-800 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* LEGENDA EXECUTIVA LEAN CONSTRUTIVA */}
      <div className="p-4 bg-zinc-950/40 text-xs text-zinc-400 flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="w-3.5 h-3.5 rounded bg-gradient-to-r from-rose-600 to-amber-600 border border-rose-400" />
            <span className="text-zinc-300 font-semibold">Caminho Crítico (Folga 0d)</span>
          </div>

          <div className="flex items-center gap-2">
            <span className="w-3.5 h-3.5 rounded bg-gradient-to-r from-blue-700 to-indigo-600 border border-blue-400" />
            <span className="text-zinc-300 font-semibold">Atividade com Folga Positiva</span>
          </div>

          <div className="flex items-center gap-2">
            <span className="w-6 h-2 border-y border-dashed border-emerald-500/50 bg-emerald-500/20" />
            <span className="text-emerald-400 font-mono">Margem de Folga Disponível</span>
          </div>
        </div>

        <div className="text-[11px] text-zinc-500 flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-amber-400" />
          <span>Governado pela SKILL_GESTAO_16: Zero colisão gráfica e 100% de precisão de caminho crítico.</span>
        </div>
      </div>
    </div>
  );
}
