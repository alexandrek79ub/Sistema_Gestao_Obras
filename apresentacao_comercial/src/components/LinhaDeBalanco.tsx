"use client";

import React, { useState, useEffect, useRef } from 'react';
import { 
  ZoomIn, ZoomOut, Maximize2, Minimize2, Calendar, User, Clock, 
  ArrowUpRight, CheckCircle2, AlertTriangle, TrendingUp, Layers, Info, X,
  ShieldCheck, HelpCircle, Edit3, Save, Sliders, FastForward, Rewind, Check, RefreshCw, Loader2,
  Users, Zap
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
  predecessores?: number[];
  sucessores?: number[];
  predecessoresNomes?: string[];
  sucessoresNomes?: string[];
}

interface PontoVagao {
  id: number;
  pav: string;
  start: number;
  duration: number;
  dataInicio?: string;
  dataFim?: string;
  predecessoresNomes?: string[];
  sucessoresNomes?: string[];
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
  predecessoresNomes?: string[];
  sucessoresNomes?: string[];
}

interface ConflitoVisual {
  id: string;
  tipo: 'equipe_dupla' | 'conflito_espacial';
  equipe?: string;
  setor?: string;
  setores: string[];
  diaInicio: number;
  diaFim: number;
  tarefasIds: number[];
  descricao: string;
}


// Paleta de cores vibrantes, contrastantes e oficiais para Linhas de Balanço Lean
const COR_HEX_VAGOES: Record<string, { stroke: string; fill: string; badge: string; bgCard: string; border: string }> = {
  "01": { stroke: "#38bdf8", fill: "rgba(56, 189, 248, 0.28)", badge: "bg-sky-500", bgCard: "bg-sky-950/70", border: "border-sky-500" }, // Topografia & Canteiro
  "02": { stroke: "#3b82f6", fill: "rgba(59, 130, 246, 0.28)", badge: "bg-blue-600", bgCard: "bg-blue-950/70", border: "border-blue-500" }, // Fundações Sapatas
  "03": { stroke: "#2563eb", fill: "rgba(37, 99, 235, 0.28)", badge: "bg-blue-700", bgCard: "bg-blue-950/70", border: "border-blue-600" }, // Vigas Baldrames
  "04": { stroke: "#6366f1", fill: "rgba(99, 102, 241, 0.28)", badge: "bg-indigo-500", bgCard: "bg-indigo-950/70", border: "border-indigo-500" }, // Pilares Supraestrutura
  "05": { stroke: "#8b5cf6", fill: "rgba(139, 92, 246, 0.28)", badge: "bg-purple-500", bgCard: "bg-purple-950/70", border: "border-purple-500" }, // Vigas & Laje H12
  "06": { stroke: "#f59e0b", fill: "rgba(245, 158, 11, 0.28)", badge: "bg-amber-500", bgCard: "bg-amber-950/70", border: "border-amber-500" }, // Alvenaria de Vedação
  "07": { stroke: "#06b6d4", fill: "rgba(6, 182, 212, 0.28)", badge: "bg-cyan-500", bgCard: "bg-cyan-950/70", border: "border-cyan-500" }, // Cobertura Metálica
  "08": { stroke: "#10b981", fill: "rgba(16, 185, 129, 0.28)", badge: "bg-emerald-500", bgCard: "bg-emerald-950/70", border: "border-emerald-500" }, // Instalações Embutidas
  "09": { stroke: "#f97316", fill: "rgba(249, 115, 22, 0.28)", badge: "bg-orange-500", bgCard: "bg-orange-950/70", border: "border-orange-500" }, // Reboco Paulista
  "10": { stroke: "#ef4444", fill: "rgba(239, 68, 68, 0.28)", badge: "bg-red-500", bgCard: "bg-red-950/70", border: "border-red-500" }, // Pisos & Porcelanato
  "11": { stroke: "#a855f7", fill: "rgba(168, 85, 247, 0.28)", badge: "bg-purple-600", bgCard: "bg-purple-950/70", border: "border-purple-500" }, // Esquadrias de Alumínio
  "12": { stroke: "#0284c7", fill: "rgba(2, 132, 199, 0.28)", badge: "bg-sky-600", bgCard: "bg-sky-950/70", border: "border-sky-600" }, // Climatização HVAC
  "13": { stroke: "#eab308", fill: "rgba(234, 179, 8, 0.28)", badge: "bg-yellow-500", bgCard: "bg-yellow-950/70", border: "border-yellow-500" }, // Acabamentos Elétr./Hidr.
  "14": { stroke: "#d946ef", fill: "rgba(217, 70, 239, 0.28)", badge: "bg-fuchsia-600", bgCard: "bg-fuchsia-950/70", border: "border-fuchsia-500" }, // Pintura Acrílica Final
  "15": { stroke: "#14b8a6", fill: "rgba(20, 184, 166, 0.30)", badge: "bg-teal-600", bgCard: "bg-teal-950/70", border: "border-teal-500" }, // Comissionamento & Entrega
};

// Headcount padrão planejado por vagão (baseline de produtividade e dimensionamento RUP)
const HEADCOUNT_PADRAO_VAGAO: Record<string, number> = {
  "01": 7,  // Topografia & Canteiro
  "02": 7,  // Fundações Sapatas
  "03": 8,  // Vigas Baldrames
  "04": 14, // Pilares Supraestrutura
  "05": 14, // Vigas & Laje H12
  "06": 10, // Alvenaria de Vedação
  "07": 9,  // Cobertura Metálica
  "08": 8,  // Instalações Embutidas
  "09": 8,  // Reboco Paulista
  "10": 10, // Pisos & Porcelanato
  "11": 6,  // Esquadrias de Alumínio
  "12": 6,  // Climatização HVAC
  "13": 8,  // Acabamentos Elétr./Hidr.
  "14": 8,  // Pintura Acrílica Final
  "15": 12  // Comissionamento & Entrega
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

function parseDateBR(dateStr: string): Date | null {
  if (!dateStr) return null;
  const clean = dateStr.trim().replace(/^"|"$/g, '');
  if (clean.includes('/')) {
    const parts = clean.split('/');
    if (parts.length === 3) {
      const [d, m, y] = parts;
      const fullYear = y.length === 2 ? `20${y}` : y;
      return new Date(parseInt(fullYear, 10), parseInt(m, 10) - 1, parseInt(d, 10));
    }
  } else if (clean.includes('-')) {
    const parts = clean.split('-');
    if (parts.length === 3) {
      const [y, m, d] = parts;
      return new Date(parseInt(y, 10), parseInt(m, 10) - 1, parseInt(d, 10));
    }
  }
  return null;
}

function formatDateBR(d: Date): string {
  const day = String(d.getDate()).padStart(2, '0');
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const year = d.getFullYear();
  return `${day}/${month}/${year}`;
}

function addWorkingDays(date: Date, days: number): Date {
  const current = new Date(date);
  let added = 0;
  const step = days >= 0 ? 1 : -1;
  const absDays = Math.abs(days);
  while (added < absDays) {
    current.setDate(current.getDate() + step);
    if (current.getDay() !== 0) { // Sunday = 0
      added++;
    }
  }
  return current;
}

function calcularDataFim(dataInicioStr: string, duracaoDias: number): string {
  const d = parseDateBR(dataInicioStr);
  if (!d || isNaN(d.getTime()) || duracaoDias <= 0) return '';
  if (duracaoDias === 1) return formatDateBR(d);
  const end = addWorkingDays(d, duracaoDias - 1);
  return formatDateBR(end);
}

function calcularDuracaoDias(dataInicioStr: string, dataFimStr: string): number {
  const dIni = parseDateBR(dataInicioStr);
  const dFim = parseDateBR(dataFimStr);
  if (!dIni || !dFim || isNaN(dIni.getTime()) || isNaN(dFim.getTime()) || dFim < dIni) return 3;
  let count = 0;
  const cur = new Date(dIni);
  while (cur <= dFim) {
    if (cur.getDay() !== 0) count++;
    cur.setDate(cur.getDate() + 1);
  }
  return Math.max(1, count);
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
  const [showBannerConflito, setShowBannerConflito] = useState(false);

  // Estados de Edição Interativa, Autonomia e RUP
  const [isEditando, setIsEditando] = useState(false);
  const [pontoEditando, setPontoEditando] = useState<PontoVagao | null>(null);
  const [editVagaoNome, setEditVagaoNome] = useState('');
  const [editDataInicio, setEditDataInicio] = useState('');
  const [editDataFim, setEditDataFim] = useState('');
  const [editEquipe, setEditEquipe] = useState('');
  const [editDuracao, setEditDuracao] = useState(3);
  const [origDuracao, setOrigDuracao] = useState(3);
  const [baseHeadcount, setBaseHeadcount] = useState(8);
  const [editHeadcount, setEditHeadcount] = useState(8);
  const [empurrarSucessores, setEmpurrarSucessores] = useState(true);
  const [deslocarPredecessores, setDeslocarPredecessores] = useState(false);
  const [aplicarEmTodoVagao, setAplicarEmTodoVagao] = useState(false);
  const [predecessoresAtuais, setPredecessoresAtuais] = useState<string[]>([]);
  const [sucessoresAtuais, setSucessoresAtuais] = useState<string[]>([]);
  const [salvando, setSalvando] = useState(false);
  const [toastMsg, setToastMsg] = useState<{ tipo: 'success' | 'error' | 'info'; texto: string } | null>(null);

  const carregarDadosCronograma = (silent = false) => {
    if (!silent) setLoading(true);
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

          if (vagaoSelecionado && data.vagoesFluxo) {
            const atualizado = data.vagoesFluxo.find((v: VagaoFluxo) => v.nome === vagaoSelecionado.nome);
            if (atualizado) setVagaoSelecionado(atualizado);
          }
        } else {
          setTarefas([]);
          setVagoesFluxo([]);
          setPavimentos([]);
        }
        if (!silent) setLoading(false);
      })
      .catch(err => {
        console.error('Erro ao buscar cronograma', err);
        if (!silent) setLoading(false);
      });
  };

  useEffect(() => {
    carregarDadosCronograma();
  }, [obraAtiva]);

  useEffect(() => {
    if (toastMsg) {
      const timer = setTimeout(() => setToastMsg(null), 4000);
      return () => clearTimeout(timer);
    }
  }, [toastMsg]);

  const handleAbrirEdicao = (ponto: PontoVagao, vagao: VagaoFluxo) => {
    setPontoEditando(ponto);
    setEditVagaoNome(vagao.nome);
    setEditDataInicio(ponto.dataInicio || '');
    const dur = ponto.duration || 3;
    setEditDuracao(dur);
    setOrigDuracao(dur);
    
    const prefix = (vagao.nome || '').slice(0, 2);
    const baseHc = HEADCOUNT_PADRAO_VAGAO[prefix] || 8;
    setBaseHeadcount(baseHc);
    setEditHeadcount(baseHc);

    // Recalcular data de término consistente com o início e a duração
    const computedFim = ponto.dataInicio && dur > 0 
      ? calcularDataFim(ponto.dataInicio, dur) 
      : (ponto.dataFim || '');
    setEditDataFim(computedFim);
    setEditEquipe(vagao.equipe || 'SUB-01 Estruturas e Concreto');
    setEmpurrarSucessores(true);
    setDeslocarPredecessores(false);
    setAplicarEmTodoVagao(false);

    // Mapeia predecessoras e sucessoras da frente específica
    const tOrig = tarefas.find(t => t.id === ponto.id);
    setPredecessoresAtuais(tOrig?.predecessoresNomes || vagao.predecessoresNomes || []);
    setSucessoresAtuais(tOrig?.sucessoresNomes || vagao.sucessoresNomes || []);

    setIsEditando(true);
  };

  const handleSalvarEdicao = async () => {
    if (!pontoEditando) return;
    setSalvando(true);
    try {
      const res = await fetch('/api/cronograma', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          obra: obraAtiva,
          acao: 'atualizar_tarefa',
          tarefa: {
            id: pontoEditando.id,
            pav: pontoEditando.pav,
            dataInicio: editDataInicio,
            dataFim: editDataFim,
            equipe: editEquipe,
            duration: editDuracao,
            headcount: editHeadcount
          },
          empurrarSucessores,
          deslocarPredecessores,
          aplicarEmTodoVagao
        })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        setToastMsg({ 
          tipo: 'success', 
          texto: data.message || '✅ Alteração salva no CSV e sincronizada com sucesso!'
        });
        setIsEditando(false);
        carregarDadosCronograma();
      } else {
        setToastMsg({ tipo: 'error', texto: data.error || 'Erro ao salvar alteração' });
      }
    } catch (err) {
      setToastMsg({ tipo: 'error', texto: 'Erro de conexão com o servidor' });
    } finally {
      setSalvando(false);
    }
  };

  const handleDeslocarVagao = async (dias: number, deslocarSucessores: boolean = true) => {
    if (!vagaoSelecionado || vagaoSelecionado.pontos.length === 0) return;
    setSalvando(true);
    try {
      const primeiroPonto = vagaoSelecionado.pontos[0];
      const res = await fetch('/api/cronograma', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          obra: obraAtiva,
          acao: 'deslocar',
          id: primeiroPonto.id,
          dias,
          deslocarSucessores,
          deslocarPredecessores: dias < 0
        })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        setToastMsg({ 
          tipo: 'success', 
          texto: `✅ Deslocamento de ${dias > 0 ? '+' : ''}${dias} dias salvo no CSV e propagado!` 
        });
        carregarDadosCronograma();
      } else {
        setToastMsg({ tipo: 'error', texto: data.error || 'Erro ao deslocar' });
      }
    } catch (err) {
      setToastMsg({ tipo: 'error', texto: 'Falha ao conectar com o backend' });
    } finally {
      setSalvando(false);
    }
  };

  const handleDeslocarVagaoInteiro = async (dias: number, deslocarSucessores: boolean = true, deslocarPredecessores: boolean = false) => {
    if (!vagaoSelecionado || vagaoSelecionado.pontos.length === 0) return;
    setSalvando(true);
    try {
      const res = await fetch('/api/cronograma', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          obra: obraAtiva,
          acao: 'deslocar_vagao',
          vagaoNome: vagaoSelecionado.nome,
          dias,
          deslocarSucessores,
          deslocarPredecessores
        })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        setToastMsg({ 
          tipo: 'success', 
          texto: `✅ Vagão '${vagaoSelecionado.nome.replace(/^\d+\.\s*/, '')}' deslocado em ${dias > 0 ? '+' : ''}${dias} dias em todas as zonas com cascata!` 
        });
        carregarDadosCronograma();
      } else {
        setToastMsg({ tipo: 'error', texto: data.error || 'Erro ao deslocar vagão' });
      }
    } catch (err) {
      setToastMsg({ tipo: 'error', texto: 'Falha ao conectar com o backend' });
    } finally {
      setSalvando(false);
    }
  };


  // Detecção Dinâmica de Sobreposição de Equipes (Dupla Frente) e Conflitos Espaciais
  const conflitosVisuais = React.useMemo(() => {
    if (!tarefas || tarefas.length === 0) return [];
    
    const conflitosPorDia: { dia: number; tipo: 'equipe_dupla' | 'conflito_espacial'; equipe?: string; setor?: string; tarefas: TarefaLOB[] }[] = [];
    
    for (let d = 1; d <= totalDias; d++) {
      const ativas = tarefas.filter(t => d >= t.start && d < t.start + t.duration);
      
      // 1. Detectar mesma equipe em múltiplos setores no mesmo dia
      const mapEquipe = new Map<string, TarefaLOB[]>();
      ativas.forEach(t => {
        if (t.equipe && !t.equipe.toLowerCase().includes('própria') && !t.equipe.toLowerCase().includes('turnkey')) {
          const list = mapEquipe.get(t.equipe) || [];
          list.push(t);
          mapEquipe.set(t.equipe, list);
        }
      });

      mapEquipe.forEach((taskList, eq) => {
        const setores = new Set(taskList.map(t => t.pav));
        if (setores.size > 1) {
          conflitosPorDia.push({
            dia: d,
            tipo: 'equipe_dupla',
            equipe: eq,
            tarefas: taskList
          });
        }
      });

      // 2. Detectar equipes diferentes no mesmo setor no mesmo dia
      const mapSetor = new Map<string, TarefaLOB[]>();
      ativas.forEach(t => {
        const list = mapSetor.get(t.pav) || [];
        list.push(t);
        mapSetor.set(t.pav, list);
      });

      mapSetor.forEach((taskList, pav) => {
        const eqDistintas = new Set(taskList.map(t => t.equipe));
        if (taskList.length > 1 && eqDistintas.size > 1) {
          conflitosPorDia.push({
            dia: d,
            tipo: 'conflito_espacial',
            setor: pav,
            tarefas: taskList
          });
        }
      });
    }

    if (conflitosPorDia.length === 0) return [];

    // Agrupar dias contíguos
    const conflitosConsolidados: ConflitoVisual[] = [];
    const agrupados = new Map<string, typeof conflitosPorDia>();

    conflitosPorDia.forEach(item => {
      const chave = item.tipo === 'equipe_dupla' ? `eq_${item.equipe}` : `setor_${item.setor}`;
      const list = agrupados.get(chave) || [];
      list.push(item);
      agrupados.set(chave, list);
    });

    agrupados.forEach((itens, chave) => {
      itens.sort((a, b) => a.dia - b.dia);
      let dIni = itens[0].dia;
      let dPrev = itens[0].dia;
      let tIds = new Set<number>(itens[0].tarefas.map(t => t.id));
      let setSet = new Set<string>(itens[0].tarefas.map(t => t.pav));

      for (let i = 1; i < itens.length; i++) {
        const cur = itens[i];
        if (cur.dia === dPrev + 1) {
          dPrev = cur.dia;
          cur.tarefas.forEach(t => {
            tIds.add(t.id);
            setSet.add(t.pav);
          });
        } else {
          const sample = itens[i - 1];
          conflitosConsolidados.push({
            id: `${chave}_${dIni}_${dPrev}`,
            tipo: sample.tipo,
            equipe: sample.equipe,
            setor: sample.setor,
            setores: Array.from(setSet),
            diaInicio: dIni,
            diaFim: dPrev + 1,
            tarefasIds: Array.from(tIds),
            descricao: sample.tipo === 'equipe_dupla'
              ? `⚠️ Dupla Frente: ${sample.equipe} em ${setSet.size} setores simultâneos (+1 equipe necessária)`
              : `⚠️ Conflito Espacial no setor ${sample.setor}`
          });
          dIni = cur.dia;
          dPrev = cur.dia;
          tIds = new Set<number>(cur.tarefas.map(t => t.id));
          setSet = new Set<string>(cur.tarefas.map(t => t.pav));
        }
      }

      const last = itens[itens.length - 1];
      conflitosConsolidados.push({
        id: `${chave}_${dIni}_${dPrev}`,
        tipo: last.tipo,
        equipe: last.equipe,
        setor: last.setor,
        setores: Array.from(setSet),
        diaInicio: dIni,
        diaFim: dPrev + 1,
        tarefasIds: Array.from(tIds),
        descricao: last.tipo === 'equipe_dupla'
          ? `⚠️ Dupla Frente: ${last.equipe} em ${setSet.size} setores simultâneos (+1 equipe necessária)`
          : `⚠️ Conflito Espacial (${Array.from(setSet).join(', ')})`
      });
    });

    return conflitosConsolidados;
  }, [tarefas, totalDias]);

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
      tarefaId: number;
      tarefa: TarefaLOB;
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
      lotes.push({
        id: `${pav}-${vNome}-${t.start}-${idx}`,
        tarefaId: t.id,
        tarefa: t,
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

          {/* BOTÃO DE RECARREGAR / SINCRONIZAR */}
          <button
            onClick={() => carregarDadosCronograma(false)}
            disabled={loading || salvando}
            className="px-3 py-1.5 rounded-lg bg-zinc-950 hover:bg-zinc-800 text-zinc-300 hover:text-white border border-zinc-800 text-xs flex items-center gap-1.5 transition-colors font-medium cursor-pointer"
            title="Recarregar dados do backend e verificar sincronização"
          >
            <RefreshCw className={`w-3.5 h-3.5 text-blue-400 ${loading ? 'animate-spin' : ''}`} />
            Sincronizar
          </button>

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

      {/* BANNER DISCRETO E COLAPSÁVEL DE CONFLITOS DE ORÇAMENTO (NÃO BLOQUEIA EDIÇÃO) */}
      {conflitosVisuais.length > 0 && (
        <div className="mb-4 bg-zinc-950/90 border border-zinc-800 rounded-xl overflow-hidden shadow-md text-xs">
          <div className="px-4 py-2.5 flex items-center justify-between gap-3 bg-zinc-900/60">
            <div className="flex items-center gap-2 text-zinc-300">
              <span className="w-2 h-2 rounded-full bg-amber-400"></span>
              <span className="font-medium text-zinc-200">
                Sobreposições de Equipe Mapeadas no Orçamento Baseline:
              </span>
              <span className="font-mono text-zinc-400">
                {conflitosVisuais.length} intervalo{conflitosVisuais.length > 1 ? 's' : ''} pré-existente{conflitosVisuais.length > 1 ? 's' : ''}
              </span>
            </div>
            <button
              onClick={() => setShowBannerConflito(!showBannerConflito)}
              className="text-xs text-blue-400 hover:text-blue-300 font-semibold cursor-pointer flex items-center gap-1"
            >
              {showBannerConflito ? 'Ocultar Detalhes ▲' : 'Ver Detalhes ▼'}
            </button>
          </div>

          {showBannerConflito && (
            <div className="p-4 border-t border-zinc-800/80 bg-zinc-950/80 space-y-2 animate-in fade-in duration-150">
              <p className="text-zinc-400">
                Intervalos onde a mesma equipe está alocada em frentes simultâneas no orçamento original (ex: fundações/estruturas). 
                Ao mover atividades com folga, o sistema permite ajustar livremente os prazos sem gerar travas.
              </p>
              <div className="flex flex-wrap gap-2 pt-1">
                {conflitosVisuais.map((c, idx) => (
                  <span key={idx} className="px-2 py-1 rounded bg-zinc-900 border border-zinc-700/60 text-[11px] text-zinc-300 font-mono">
                    <strong className="text-amber-400">{c.equipe}</strong> ({c.setores.join(', ')}): Dias {c.diaInicio} a {c.diaFim}
                  </span>
                ))}
              </div>
            </div>
          )}
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
                    <filter id="glow-conflito" x="-20%" y="-20%" width="140%" height="140%">
                      <feDropShadow dx="0" dy="0" stdDeviation="6" floodColor="#ef4444" floodOpacity="0.9" />
                    </filter>
                    <pattern id="stripe-comissionamento" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                      <line x1="0" y1="0" x2="0" y2="12" stroke="#14b8a6" strokeWidth="2" strokeOpacity="0.25" />
                    </pattern>
                    <pattern id="stripe-sobreposicao" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                      <line x1="0" y1="0" x2="0" y2="12" stroke="#ef4444" strokeWidth="2.5" strokeOpacity="0.45" />
                    </pattern>
                  </defs>

                  {/* CAMADA VISUAL DE CONFLITOS E SOBREPOSIÇÃO DE EQUIPES (DUPLA FRENTE) */}
                  {conflitosVisuais.map((c) => {
                    const xIni = getX(c.diaInicio);
                    const xFim = getX(c.diaFim);
                    const w = Math.max(34, xFim - xIni);
                    return (
                      <g key={c.id} className="animate-in fade-in">
                        {/* Faixa vertical hachurada com destaque de risco */}
                        <rect
                          x={xIni}
                          y={4}
                          width={w}
                          height={chartHeight - 8}
                          fill="url(#stripe-sobreposicao)"
                          stroke="#ef4444"
                          strokeWidth={1.5}
                          strokeDasharray="4 3"
                          rx={6}
                          opacity={0.55}
                          className="pointer-events-none"
                        />
                        {/* Pin / Badge Flutuante no Topo com aviso de demanda de equipe */}
                        <foreignObject
                          x={Math.max(4, xIni + w / 2 - 120)}
                          y={6}
                          width={240}
                          height={36}
                          className="overflow-visible pointer-events-auto"
                        >
                          <div 
                            className="px-2.5 py-1 rounded-full bg-rose-950/95 border border-rose-500 text-rose-200 text-[10px] font-bold shadow-2xl flex items-center justify-center gap-1.5 ring-2 ring-rose-500/40 backdrop-blur-md cursor-help hover:scale-105 transition-transform"
                            title={c.descricao}
                          >
                            <AlertTriangle className="w-3.5 h-3.5 text-rose-400 shrink-0 animate-bounce" />
                            <span className="truncate">{c.descricao}</span>
                          </div>
                        </foreignObject>
                      </g>
                    );
                  })}

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
                      const ponto0 = vagao.pontos[0];
                      const temConflito1 = ponto0 ? conflitosVisuais.some(c => c.tarefasIds.includes(ponto0.id)) : false;

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
                            stroke={temConflito1 ? "#ef4444" : cor.stroke} 
                            strokeWidth={temConflito1 ? 3 : (isHovered || isSelected ? 3 : 1.5)}
                            strokeDasharray="6 4"
                            filter={temConflito1 ? "url(#glow-conflito)" : (isHovered ? "url(#glow-line)" : undefined)}
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
                      const pontoZ = vagao.pontos.find(p => p.pav === z.pav) || vagao.pontos[0];
                      const temConflito2 = pontoZ ? conflitosVisuais.some(c => c.tarefasIds.includes(pontoZ.id)) : false;

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
                            stroke={temConflito2 ? "#ef4444" : cor.stroke} 
                            strokeWidth={temConflito2 ? 3.5 : (isHovered || isSelected ? 3 : 1.5)}
                            strokeDasharray={temConflito2 ? "4 2" : undefined}
                            filter={temConflito2 ? "url(#glow-conflito)" : (isHovered ? "url(#glow-line)" : undefined)}
                          />
                          <foreignObject 
                            x={xIni} 
                            y={yTop} 
                            width={width} 
                            height={height}
                            className="overflow-visible pointer-events-none"
                          >
                            <div className="flex items-center justify-center h-full px-2">
                              <span className="text-[10px] font-bold text-white truncate drop-shadow flex items-center gap-1">
                                {temConflito2 && <span className="animate-bounce">⚠️</span>}
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

                      const polygonPoints = [
                        ...leftPoints.map(p => `${p.x},${p.y}`),
                        ...[...rightPoints].reverse().map(p => `${p.x},${p.y}`)
                      ].join(' ');

                      const pathStart = leftPoints.map((p, idx) => `${idx === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
                      const pathEnd = rightPoints.map((p, idx) => `${idx === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
                      const pathCenter = centerPoints.map((p, idx) => `${idx === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');

                      const midIdx = Math.floor(centerPoints.length / 2);
                      const labelPonto = centerPoints[midIdx];
                      const primeiroP = vagao.pontos[0];
                      const temConflito3 = vagao.pontos.some(p => conflitosVisuais.some(c => c.tarefasIds.includes(p.id)));

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
                            stroke={temConflito3 ? "#ef4444" : "none"}
                            strokeWidth={temConflito3 ? 2 : 0}
                            filter={temConflito3 ? "url(#glow-conflito)" : (isHovered ? "url(#glow-line)" : undefined)}
                            className="transition-all"
                          />

                          {/* LINHA DE INÍCIO DA FRENTE (BORDA ESQUERDA) */}
                          <path 
                            d={pathStart} 
                            stroke={temConflito3 ? "#ef4444" : cor.stroke} 
                            strokeWidth={temConflito3 ? 4 : (isHovered || isSelected ? 3.5 : 2.5)}
                            strokeDasharray={temConflito3 ? "6 3" : undefined}
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

                          {/* NÓS/MARCADORES EM CADA SETOR COM ARRASTE DIRETO POR SETOR */}
                          {centerPoints.map((p, idx) => {
                            const z = zonasConsolidadas[idx];
                            const pontoZ = vagao.pontos.find(pt => pt.pav === z?.pav) || vagao.pontos[0];
                            return (
                              <circle 
                                key={idx} 
                                cx={p.x} 
                                cy={p.y} 
                                r={isHovered ? 6 : 4.5} 
                                fill="#ffffff" 
                                stroke={temConflito3 ? "#ef4444" : cor.stroke} 
                                strokeWidth={2.5} 
                                className="cursor-pointer hover:scale-125 transition-transform"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  setVagaoSelecionado(vagao);
                                }}
                              />
                            );
                          })}

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
                                className={`px-2.5 py-1 rounded-full text-[10px] font-bold text-white shadow-xl whitespace-nowrap border ${
                                  temConflito3 ? 'bg-rose-950 border-rose-500 ring-2 ring-rose-500 animate-pulse' : `${cor.badge} border-white/30`
                                } ${isHovered ? 'scale-110 ring-2 ring-white' : ''} transition-transform flex items-center gap-1`}
                              >
                                {temConflito3 && <span>⚠️</span>}
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
                          const temConflito = conflitosVisuais.some(c => c.tarefasIds.includes(lote.tarefaId));

                          return (
                            <div
                              key={lote.id}
                              onClick={(e) => {
                                e.stopPropagation();
                                const vEncontrado = vagoesFluxo.find(v => v.nome === lote.vagaoNome);
                                if (vEncontrado) setVagaoSelecionado(vEncontrado);
                              }}
                              style={{ 
                                left: `${xIni}px`, 
                                width: `${width}px`, 
                                height: `${rowHeight - 28}px`,
                              }}
                              className={`absolute ${cor.badge} border ${
                                temConflito ? 'border-rose-400 ring-2 ring-rose-500 animate-pulse' : 'border-white/20'
                              } rounded-lg shadow-md flex flex-col items-center justify-center text-white px-1.5 cursor-pointer hover:ring-2 hover:ring-white hover:scale-[1.02] transition-transform z-10 select-none`}
                              title={`${lote.vagaoNome} (${lote.dataInicio} a ${lote.dataFim}) - ${lote.duration} dias. Clique para ver detalhes.`}
                            >
                              {width >= 90 ? (
                                <>
                                  <span className="text-[10px] font-bold leading-tight truncate w-full text-center flex items-center justify-center gap-1">
                                    {temConflito && <span>⚠️</span>}
                                    {lote.vagaoNome.replace(/^\d+\.\s*/, '')}
                                  </span>
                                  <span className="text-[9px] text-white/80 font-mono">
                                    {lote.duration}d
                                  </span>
                                </>
                              ) : width >= 48 ? (
                                <>
                                  <span className="text-[10px] font-bold leading-tight flex items-center gap-0.5">
                                    {temConflito && <span>⚠️</span>}
                                    V{prefix}
                                  </span>
                                  <span className="text-[8px] text-white/80 font-mono">
                                    {lote.duration}d
                                  </span>
                                </>
                              ) : (
                                <span className="text-[10px] font-bold flex items-center gap-0.5">
                                  {temConflito && <span>⚠️</span>}
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

      {/* PAINEL INFERIOR: DETALHES DO VAGÃO OU GUIA DE INTERAÇÃO */}
      {vagaoSelecionado ? (
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

          {/* PAINEL DE AJUSTE DIRETO POR ZONA / DESLOCAMENTO DO VAGÃO (AUTONOMIA DO USUÁRIO) */}
          <div className="mt-5 pt-4 border-t border-zinc-800/90">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3">
              <span className="text-xs font-bold uppercase text-zinc-300 tracking-wider flex items-center gap-1.5">
                <Sliders className="w-4 h-4 text-blue-400" />
                Ajuste Rápido do Vagão Inteiro (Gravação no CSV):
              </span>
              
              {/* ATALHOS DE DESLOCAMENTO EM BLOCO SINCRONIZADO */}
              <div className="flex items-center gap-2 flex-wrap">
                <button 
                  onClick={() => handleDeslocarVagaoInteiro(-3, false, true)}
                  disabled={salvando}
                  className="px-2.5 py-1 text-xs rounded-md bg-zinc-900 hover:bg-zinc-800 text-amber-300 border border-amber-500/40 flex items-center gap-1 transition-colors cursor-pointer"
                  title="Adiantar todo este vagão em 3 dias úteis puxando predecessoras se necessário"
                >
                  <Rewind className="w-3 h-3 text-amber-400" /> Mover Vagão (-3d)
                </button>
                <button 
                  onClick={() => handleDeslocarVagaoInteiro(3, false, false)}
                  disabled={salvando}
                  className="px-2.5 py-1 text-xs rounded-md bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-700 flex items-center gap-1 transition-colors cursor-pointer"
                  title="Atrasar todo este vagão em 3 dias úteis sem empurrar sucessoras"
                >
                  <FastForward className="w-3 h-3 text-emerald-400" /> Mover Vagão (+3d)
                </button>
                <button 
                  onClick={() => handleDeslocarVagaoInteiro(3, true, false)}
                  disabled={salvando}
                  className="px-2.5 py-1 text-xs rounded-md bg-purple-950/70 hover:bg-purple-900/70 text-purple-200 border border-purple-500/60 flex items-center gap-1.5 transition-colors cursor-pointer font-medium shadow-sm"
                  title="Empurrar este vagão e todas as atividades sucessoras em cascata (+3d)"
                >
                  <FastForward className="w-3 h-3 text-purple-400" /> Cascata Completa (+3d)
                </button>
              </div>
            </div>

            {/* CARTÕES DE CADA SETOR DO VAGÃO COM BOTÃO DE EDIÇÃO */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
              {vagaoSelecionado.pontos.map((p) => (
                <div 
                  key={p.id}
                  className="p-3 bg-zinc-900/80 rounded-lg border border-zinc-800 hover:border-zinc-700 flex flex-col justify-between transition-all"
                >
                  <div>
                    <div className="flex items-center justify-between gap-1">
                      <span className="text-[11px] font-bold text-zinc-200 truncate block">
                        {p.pav}
                      </span>
                      <span className="text-[10px] text-zinc-400 bg-zinc-800 px-1.5 py-0.5 rounded font-mono">
                        ID: {p.id}
                      </span>
                    </div>
                    <div className="text-[11px] text-zinc-300 font-mono mt-1">
                      📅 {p.dataInicio || 'Início'} ➔ {p.dataFim || 'Fim'}
                    </div>
                    <div className="flex items-center justify-between text-[10px] mt-1 text-zinc-400">
                      <span className="text-emerald-400 font-medium">
                        Ritmo: {p.duration} dias úteis
                      </span>
                    </div>

                    {/* BADGES DE PRECEDÊNCIAS */}
                    <div className="mt-2 pt-2 border-t border-zinc-800/80 space-y-1 text-[10px]">
                      {p.predecessoresNomes && p.predecessoresNomes.length > 0 && (
                        <div className="text-amber-400/90 truncate flex items-center gap-1" title={`Predecessoras: ${p.predecessoresNomes.join(', ')}`}>
                          <span className="font-bold">⬅ Pred:</span>
                          <span className="truncate">{p.predecessoresNomes.join(', ')}</span>
                        </div>
                      )}
                      {p.sucessoresNomes && p.sucessoresNomes.length > 0 && (
                        <div className="text-blue-400/90 truncate flex items-center gap-1" title={`Sucessoras: ${p.sucessoresNomes.join(', ')}`}>
                          <span className="font-bold">➡ Suc:</span>
                          <span className="truncate">{p.sucessoresNomes.join(', ')}</span>
                        </div>
                      )}
                    </div>
                  </div>
                  <button
                    onClick={() => handleAbrirEdicao(p, vagaoSelecionado)}
                    className="mt-3 w-full py-1.5 text-[11px] rounded bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 border border-blue-500/30 flex items-center justify-center gap-1.5 font-medium transition-colors cursor-pointer"
                  >
                    <Edit3 className="w-3 h-3" /> Editar Prazos & RUP
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <div className="mt-6 p-4 bg-zinc-950/80 border border-dashed border-blue-500/30 rounded-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs text-zinc-300 animate-in fade-in">
          <div className="flex items-center gap-3">
            <span className="p-2.5 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20 shrink-0">
              <Sliders className="w-5 h-5" />
            </span>
            <div>
              <p className="font-semibold text-white flex items-center gap-2">
                <span>🖱️ Modo Interativo Ativo:</span>
                <span className="text-zinc-400 font-normal">Clique em qualquer linha colorida ou bloco no gráfico acima</span>
              </p>
              <p className="text-[11px] text-zinc-400 mt-0.5">
                Ao clicar em um vagão, abrirá aqui o painel de <strong>ajuste rápido (-3d, +3d, Cascata Completa)</strong>, <strong>redimensionamento de equipe via RUP</strong> e <strong>sincronização automática com o Curto Prazo (52 Lotes)</strong>.
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <span className="text-[11px] font-mono text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded-lg">
              Gravação Direta no CSV Ativa
            </span>
          </div>
        </div>
      )}

      {/* MODAL DE EDIÇÃO DIRETA DA TAREFA NO BACKEND COM REDIMENSIONAMENTO RUP */}
      {isEditando && pontoEditando && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in duration-150 overflow-y-auto">
          <div className="bg-zinc-900 border border-zinc-700 rounded-2xl p-6 max-w-lg w-full shadow-2xl animate-in zoom-in-95 duration-150 my-auto">
            <div className="flex items-start justify-between mb-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 font-bold">
                    Edição LOB & Curto Prazo
                  </span>
                  <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold">
                    Cálculo RUP Ativo
                  </span>
                </div>
                <h4 className="text-base font-bold text-white mt-1.5">
                  {editVagaoNome}
                </h4>
                <p className="text-xs text-zinc-400 mt-0.5">
                  Frente: <strong className="text-zinc-200">{pontoEditando.pav}</strong>
                </p>
              </div>
              <button 
                onClick={() => setIsEditando(false)}
                className="p-1 text-zinc-500 hover:text-white rounded-lg hover:bg-zinc-800 transition-colors cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-4 text-xs">
              {/* DATAS DE INÍCIO E FIM */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-zinc-400 mb-1 font-medium">Data Início (DD/MM/AAAA)</label>
                  <input 
                    type="text" 
                    value={editDataInicio} 
                    onChange={(e) => {
                      const val = e.target.value;
                      setEditDataInicio(val);
                      if (val.length === 10 && editDuracao > 0) {
                        const newFim = calcularDataFim(val, editDuracao);
                        if (newFim) setEditDataFim(newFim);
                      }
                    }}
                    placeholder="01/10/2026"
                    className="w-full px-3 py-2 rounded-lg bg-zinc-950 border border-zinc-700 text-zinc-100 focus:outline-none focus:border-blue-500 font-mono text-xs"
                  />
                </div>
                <div>
                  <label className="block text-zinc-400 mb-1 font-medium flex items-center justify-between">
                    <span>Data Fim (DD/MM/AAAA)</span>
                    <span className="text-[10px] text-emerald-400 font-mono">Auto-calculada</span>
                  </label>
                  <input 
                    type="text" 
                    value={editDataFim} 
                    onChange={(e) => {
                      const val = e.target.value;
                      setEditDataFim(val);
                      if (val.length === 10 && editDataInicio.length === 10) {
                        const newDur = calcularDuracaoDias(editDataInicio, val);
                        setEditDuracao(newDur);
                        // Recalcula Headcount pela RUP
                        const hc = Math.max(1, Math.ceil(baseHeadcount * (origDuracao / (newDur || 1))));
                        setEditHeadcount(hc);
                      }
                    }}
                    placeholder="03/10/2026"
                    className="w-full px-3 py-2 rounded-lg bg-zinc-950 border border-zinc-700 text-zinc-100 focus:outline-none focus:border-blue-500 font-mono text-xs"
                  />
                </div>
              </div>

              {/* DURAÇÃO E CONTROLES DE RITMO */}
              <div>
                <label className="block text-zinc-400 mb-1 font-medium flex items-center justify-between">
                  <span>Ritmo / Duração (Dias Úteis)</span>
                  <span className="text-[10px] text-blue-400">Pula Domingos (Calendário Lean)</span>
                </label>
                <div className="flex items-center gap-2">
                  <input 
                    type="number" 
                    value={editDuracao} 
                    onChange={(e) => {
                      const dur = parseInt(e.target.value, 10) || 1;
                      setEditDuracao(dur);
                      // Recalcula RUP Dinâmica
                      const hc = Math.max(1, Math.ceil(baseHeadcount * (origDuracao / dur)));
                      setEditHeadcount(hc);
                      if (editDataInicio) {
                        const newFim = calcularDataFim(editDataInicio, dur);
                        if (newFim) setEditDataFim(newFim);
                      }
                    }}
                    min={1}
                    max={60}
                    className="w-full px-3 py-2 rounded-lg bg-zinc-950 border border-zinc-700 text-zinc-100 focus:outline-none focus:border-blue-500 font-mono text-xs"
                  />
                  <div className="flex items-center gap-1 shrink-0">
                    <button
                      type="button"
                      onClick={() => {
                        const newDur = Math.max(1, editDuracao - 1);
                        setEditDuracao(newDur);
                        const hc = Math.max(1, Math.ceil(baseHeadcount * (origDuracao / newDur)));
                        setEditHeadcount(hc);
                        if (editDataInicio) setEditDataFim(calcularDataFim(editDataInicio, newDur));
                      }}
                      className="px-2.5 py-1.5 rounded bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs font-bold transition-colors cursor-pointer"
                      title="Diminuir 1 dia útil (Crashing - Aumenta equipe)"
                    >
                      -1d
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        const newDur = editDuracao + 1;
                        setEditDuracao(newDur);
                        const hc = Math.max(1, Math.ceil(baseHeadcount * (origDuracao / newDur)));
                        setEditHeadcount(hc);
                        if (editDataInicio) setEditDataFim(calcularDataFim(editDataInicio, newDur));
                      }}
                      className="px-2.5 py-1.5 rounded bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs font-bold transition-colors cursor-pointer"
                      title="Aumentar 1 dia útil (Leveling - Reduz equipe)"
                    >
                      +1d
                    </button>
                  </div>
                </div>
              </div>

              {/* CARD DE REDIMENSIONAMENTO DE EQUIPE BASEADO NA RUP */}
              <div className="p-3.5 bg-zinc-950/80 border border-zinc-800 rounded-xl space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-zinc-200 flex items-center gap-1.5">
                    <Users className="w-4 h-4 text-purple-400" />
                    Dimensionamento de Efetivo (RUP):
                  </span>
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold ${
                    editDuracao < origDuracao
                      ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                      : editDuracao > origDuracao
                      ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                      : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  }`}>
                    {editDuracao < origDuracao 
                      ? '⚡ Crashing (Aceleração)' 
                      : editDuracao > origDuracao 
                      ? '⚖️ Nivelamento (Diluição)' 
                      : '✓ Ritmo Nominal'}
                  </span>
                </div>
                
                <div className="grid grid-cols-2 gap-3 items-center pt-1">
                  <div>
                    <label className="text-[11px] text-zinc-400 block mb-1">
                      Efetivo Previsto (Headcount):
                    </label>
                    <div className="flex items-center gap-2">
                      <input 
                        type="number"
                        min={1}
                        max={50}
                        value={editHeadcount}
                        onChange={(e) => setEditHeadcount(Math.max(1, parseInt(e.target.value, 10) || 1))}
                        className="w-20 px-2.5 py-1.5 rounded-lg bg-zinc-900 border border-zinc-700 text-zinc-100 font-mono text-xs font-bold focus:outline-none focus:border-purple-500"
                      />
                      <span className="text-zinc-400 text-xs">operários</span>
                    </div>
                  </div>
                  <div className="text-[11px] text-zinc-400 border-l border-zinc-800 pl-3">
                    <div className="text-zinc-300 font-medium">
                      Base: <span className="font-mono text-zinc-100">{baseHeadcount} op.</span> ({origDuracao}d)
                    </div>
                    <div className="text-[10px] text-zinc-500 mt-0.5">
                      Fórmula: H = ⌈H₀ × (D₀ / D)⌉
                    </div>
                  </div>
                </div>

                <p className="text-[10px] text-zinc-500 pt-1 leading-tight">
                  ℹ️ Atualiza automaticamente o <strong>PROGRAMACAO_CURTO_PRAZO (52 Lotes)</strong> com a nova duração e efetivo proporcional.
                </p>
              </div>

              {/* PRECEDÊNCIAS / SUCESSORAS CONECTADAS */}
              {(predecessoresAtuais.length > 0 || sucessoresAtuais.length > 0) && (
                <div className="p-3 bg-zinc-950/60 border border-zinc-800/80 rounded-xl space-y-2 text-[11px]">
                  <span className="font-semibold text-zinc-300 block">
                    Conexões na Rede LOB:
                  </span>
                  {predecessoresAtuais.length > 0 && (
                    <div className="text-amber-300/90">
                      <span className="font-bold">⬅ Predecessoras Imediatas:</span>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {predecessoresAtuais.map((p, i) => (
                          <span key={i} className="px-1.5 py-0.5 rounded bg-amber-950/60 border border-amber-800/50 text-[10px] font-mono">
                            {p}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  {sucessoresAtuais.length > 0 && (
                    <div className="text-blue-300/90 pt-1">
                      <span className="font-bold">➡ Sucessoras Imediatas:</span>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {sucessoresAtuais.map((s, i) => (
                          <span key={i} className="px-1.5 py-0.5 rounded bg-blue-950/60 border border-blue-800/50 text-[10px] font-mono">
                            {s}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* OPÇÕES DE PROPAGAÇÃO EM CASCATA */}
              <div className="space-y-2 pt-1">
                {/* CHECKBOX SUCESSORES (FORWARD) */}
                <div className="p-2.5 bg-blue-950/30 border border-blue-800/40 rounded-lg flex items-start gap-2.5">
                  <input 
                    type="checkbox" 
                    id="empurrar-sucessores-modal"
                    checked={empurrarSucessores}
                    onChange={(e) => setEmpurrarSucessores(e.target.checked)}
                    className="mt-0.5 rounded border-zinc-700 bg-zinc-950 text-blue-500 focus:ring-0 cursor-pointer w-4 h-4"
                  />
                  <label htmlFor="empurrar-sucessores-modal" className="cursor-pointer select-none">
                    <span className="font-semibold text-white block text-xs">
                      Empurrar atividades sucessoras (Forward - Cascata Lean)
                    </span>
                    <span className="text-[10px] text-zinc-400 block mt-0.5 leading-tight">
                      Recalcula e desloca as tarefas posteriores para preservar a folga mínima e evitar sobreposição física.
                    </span>
                  </label>
                </div>

                {/* CHECKBOX PREDECESSORES (BACKWARD) */}
                <div className="p-2.5 bg-amber-950/30 border border-amber-800/40 rounded-lg flex items-start gap-2.5">
                  <input 
                    type="checkbox" 
                    id="deslocar-predecessores-modal"
                    checked={deslocarPredecessores}
                    onChange={(e) => setDeslocarPredecessores(e.target.checked)}
                    className="mt-0.5 rounded border-zinc-700 bg-zinc-950 text-amber-500 focus:ring-0 cursor-pointer w-4 h-4"
                  />
                  <label htmlFor="deslocar-predecessores-modal" className="cursor-pointer select-none">
                    <span className="font-semibold text-amber-200 block text-xs">
                      Antecipar predecessoras se houver conflito de início (Backward)
                    </span>
                    <span className="text-[10px] text-zinc-400 block mt-0.5 leading-tight">
                      Se puxar a data para antes do término da antecessora, antecipa a antecessora mantendo o vínculo.
                    </span>
                  </label>
                </div>

                {/* CHECKBOX REPLICAR EM TODO O VAGÃO */}
                <div className="p-2.5 bg-zinc-950/60 border border-zinc-800 rounded-lg flex items-start gap-2.5">
                  <input 
                    type="checkbox" 
                    id="aplicar-todo-vagao-modal"
                    checked={aplicarEmTodoVagao}
                    onChange={(e) => setAplicarEmTodoVagao(e.target.checked)}
                    className="mt-0.5 rounded border-zinc-700 bg-zinc-950 text-purple-500 focus:ring-0 cursor-pointer w-4 h-4"
                  />
                  <label htmlFor="aplicar-todo-vagao-modal" className="cursor-pointer select-none">
                    <span className="font-semibold text-zinc-200 block text-xs">
                      Replicar esta duração e equipe em TODAS as 4 Zonas deste vagão
                    </span>
                    <span className="text-[10px] text-zinc-400 block mt-0.5 leading-tight">
                      Garante Takt Time uniforme (produção em linha Heijunka sem quebra de ritmo entre setores).
                    </span>
                  </label>
                </div>
              </div>

              {/* SELEÇÃO DE EQUIPE */}
              <div>
                <label className="block text-zinc-400 mb-1 font-medium">Equipe / Subempreiteiro Responsável</label>
                <select
                  value={editEquipe}
                  onChange={(e) => setEditEquipe(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-zinc-950 border border-zinc-700 text-zinc-100 focus:outline-none focus:border-blue-500 text-xs"
                >
                  <option value="SUB-01 Estruturas e Concreto">SUB-01 Estruturas e Concreto</option>
                  <option value="SUB-01 Topografia e Locação">SUB-01 Topografia e Locação</option>
                  <option value="SUB-02 Alvenaria e Revestimento">SUB-02 Alvenaria e Revestimento</option>
                  <option value="SUB-03 Elétrica e Lógica">SUB-03 Elétrica e Lógica</option>
                  <option value="SUB-04 Hidráulica e Sanitários">SUB-04 Hidráulica e Sanitários</option>
                  <option value="SUB-05 Acabamentos e Pisos">SUB-05 Acabamentos e Pisos</option>
                  <option value="SUB-06 Pintura">SUB-06 Pintura</option>
                  <option value="SUB-07 Coberturas Metálicas">SUB-07 Coberturas Metálicas</option>
                  <option value="SUB-07 Caixilharia e Esquadrias">SUB-07 Caixilharia e Esquadrias</option>
                  <option value="SUB-08 Climatização e HVAC">SUB-08 Climatização e HVAC</option>
                  <option value="Equipe Própria / Turnkey">Equipe Própria / Turnkey</option>
                </select>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2.5 mt-6 pt-4 border-t border-zinc-800">
              <button 
                onClick={() => setIsEditando(false)}
                disabled={salvando}
                className="px-4 py-2 text-xs font-semibold text-zinc-400 hover:text-white rounded-lg hover:bg-zinc-800 transition-colors cursor-pointer"
              >
                Cancelar
              </button>
              <button 
                onClick={handleSalvarEdicao}
                disabled={salvando}
                className="px-4 py-2 text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-500 rounded-lg shadow-md flex items-center gap-1.5 transition-colors cursor-pointer disabled:opacity-50"
              >
                {salvando ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    Gravando no CSV & Sincronizando...
                  </>
                ) : (
                  <>
                    <Save className="w-3.5 h-3.5" />
                    Salvar e Sincronizar LOB + Curto Prazo
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}


      {/* NOTIFICAÇÃO TOAST FLUTUANTE */}
      {toastMsg && (
        <div className={`fixed bottom-6 right-6 z-50 p-4 rounded-xl shadow-2xl border flex items-center gap-2.5 text-xs font-semibold animate-in slide-in-from-bottom-5 duration-200 ${
          toastMsg.tipo === 'success'
            ? 'bg-emerald-950/90 border-emerald-500 text-emerald-200'
            : toastMsg.tipo === 'error'
            ? 'bg-red-950/90 border-red-500 text-red-200'
            : 'bg-zinc-900 border-zinc-700 text-zinc-200'
        }`}>
          {toastMsg.tipo === 'success' && <Check className="w-4 h-4 text-emerald-400" />}
          {toastMsg.tipo === 'error' && <AlertTriangle className="w-4 h-4 text-red-400" />}
          {toastMsg.tipo === 'info' && <Info className="w-4 h-4 text-blue-400" />}
          <span>{toastMsg.texto}</span>
        </div>
      )}
    </div>
  );
}
