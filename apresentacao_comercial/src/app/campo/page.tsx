'use client';

import React, { useState, useRef } from 'react';
import {
  Sun,
  Users,
  CheckCircle2,
  XCircle,
  Send,
  MessageSquare,
  PenTool,
  ShieldCheck,
  Calendar,
  Clock,
  FileText,
  Trash2,
  Copy,
  Check
} from 'lucide-react';

type EfetivoKey =
  | 'mestre'
  | 'tst'
  | 'almoxarife'
  | 'pedreiros'
  | 'serventes'
  | 'armadores'
  | 'carpinteiros'
  | 'eletricistas'
  | 'encanadores';

interface EfetivoItem {
  label: string;
  key: EfetivoKey;
}

const ITENS_EFETIVO: EfetivoItem[] = [
  { label: 'Pedreiros de Alvenaria', key: 'pedreiros' },
  { label: 'Serventes / Ajudantes', key: 'serventes' },
  { label: 'Carpinteiros de Fôrma', key: 'carpinteiros' },
  { label: 'Armadores de Aço', key: 'armadores' },
  { label: 'Eletricistas Prediais', key: 'eletricistas' },
  { label: 'Encanadores / Instaladores', key: 'encanadores' },
  { label: 'Equipe de Gestão (Mestre/TST)', key: 'mestre' }
];

export default function CampoMobilePage() {
  const [activeTab, setActiveTab] = useState<'rdo' | 'fvs' | 'whatsapp'>('rdo');
  const [obra, setObra] = useState('OBRA_TMULT');
  const [dataHoje, setDataHoje] = useState(new Date().toISOString().split('T')[0]);

  // Estado do RDO
  const [climaManha, setClimaManha] = useState('Sol');
  const [climaTarde, setClimaTarde] = useState('Sol');
  const [horasParalisadas, setHorasParalisadas] = useState(0);
  const [motivoParalisacao, setMotivoParalisacao] = useState('Chuva forte no período da tarde');

  // Efetivo com contadores rápidos
  const [efetivo, setEfetivo] = useState<Record<EfetivoKey, number>>({
    mestre: 1,
    tst: 1,
    almoxarife: 1,
    pedreiros: 6,
    serventes: 4,
    armadores: 2,
    carpinteiros: 2,
    eletricistas: 0,
    encanadores: 0
  });

  const [servicosEap, setServicosEap] = useState<string[]>([
    '1.3.2 Escavação e Lastro de Sapatas'
  ]);
  const [ocorrencias, setOcorrencias] = useState('');

  // Estado da FVS
  const [fvsCodigo, setFvsCodigo] = useState('FVS-01');
  const [fvsTolerancia, setFvsTolerancia] = useState('Desvio linear < 2mm');
  const [fvsStatus, setFvsStatus] = useState<'Aprovado' | 'Reprovado'>('Aprovado');
  const [fvsChecklist, setFvsChecklist] = useState<Record<string, boolean>>({
    'Locação dos eixos e conferência do esquadro': true,
    'Nível a laser e amarração topográfica com RN': true,
    'Gabarito rígido travado com tábua corrida': true
  });
  const [hasSignature, setHasSignature] = useState(false);

  // Estados de feedback
  const [enviando, setEnviando] = useState(false);
  const [mensagemSucesso, setMensagemSucesso] = useState<string | null>(null);
  const [mensagemErro, setMensagemErro] = useState<string | null>(null);
  const [copiado, setCopiado] = useState(false);

  // Canvas de assinatura
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const isDrawing = useRef(false);

  const startDrawing = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    isDrawing.current = true;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const x = 'touches' in e ? e.touches[0].clientX - rect.left : e.clientX - rect.left;
    const y = 'touches' in e ? e.touches[0].clientY - rect.top : e.clientY - rect.top;

    ctx.beginPath();
    ctx.moveTo(x, y);
  };

  const draw = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    if (!isDrawing.current) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const x = 'touches' in e ? e.touches[0].clientX - rect.left : e.clientX - rect.left;
    const y = 'touches' in e ? e.touches[0].clientY - rect.top : e.clientY - rect.top;

    ctx.lineTo(x, y);
    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    ctx.stroke();
    setHasSignature(true);
  };

  const stopDrawing = () => {
    isDrawing.current = false;
  };

  const clearSignature = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    setHasSignature(false);
  };

  // Cálculos de Headcount
  const totalProprio = efetivo.mestre + efetivo.tst + efetivo.almoxarife;
  const totalTerceiro =
    efetivo.pedreiros +
    efetivo.serventes +
    efetivo.armadores +
    efetivo.carpinteiros +
    efetivo.eletricistas +
    efetivo.encanadores;
  const totalEfetivo = totalProprio + totalTerceiro;
  const totalHH = Math.max(0, totalEfetivo * 8.8 - horasParalisadas * totalEfetivo).toFixed(1);

  const updateCount = (key: EfetivoKey, delta: number) => {
    setEfetivo((prev) => ({
      ...prev,
      [key]: Math.max(0, prev[key] + delta)
    }));
  };

  const toggleEap = (item: string) => {
    setServicosEap((prev) =>
      prev.includes(item) ? prev.filter((i) => i !== item) : [...prev, item]
    );
  };

  const toggleChecklistItem = (item: string) => {
    setFvsChecklist((prev) => ({
      ...prev,
      [item]: !prev[item]
    }));
  };

  // Enviar RDO para a API
  const handleEnviarRdo = async () => {
    setEnviando(true);
    setMensagemSucesso(null);
    setMensagemErro(null);

    const payload = {
      tipo: 'rdo',
      obra,
      data: dataHoje.split('-').reverse().join('/'),
      clima_m: climaManha,
      clima_t: climaTarde,
      h_paral: horasParalisadas,
      ef_prop: totalProprio,
      ef_terc: totalTerceiro,
      hh: parseFloat(totalHH),
      eap: servicosEap.join('; ') || 'EAP Geral de Canteiro',
      fvs: fvsCodigo,
      fvs_status: fvsStatus === 'Aprovado' ? '🟢 Aprovado' : '🔴 Reprovado',
      obs:
        ocorrencias ||
        `Dia produtivo. Total de ${totalEfetivo} pessoas no canteiro. ${horasParalisadas > 0 ? `Paralisação: ${horasParalisadas}h por ${motivoParalisacao}` : 'Sem impedimentos.'}`
    };

    try {
      const res = await fetch('/api/apontamento-campo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.success) {
        setMensagemSucesso(`✅ RDO gravado com sucesso! Arquivo inserido no Painel.`);
      } else {
        setMensagemErro(`❌ Erro: ${data.error || 'Falha na transmissão'}`);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Erro de conexão';
      setMensagemErro(`❌ Erro de conexão: ${msg}`);
    } finally {
      setEnviando(false);
    }
  };

  // Enviar FVS para a API
  const handleEnviarFvs = async () => {
    setEnviando(true);
    setMensagemSucesso(null);
    setMensagemErro(null);

    const payload = {
      tipo: 'fvs',
      obra,
      codigo: fvsCodigo,
      data: dataHoje.split('-').reverse().join('/'),
      status: fvsStatus === 'Aprovado' ? '🟢 Aprovado' : '🔴 Reprovado',
      responsavel: 'Mestre João Silva / Eng. Alexandre',
      medicao_tolerancia: fvsTolerancia,
      itens_conferidos: Object.keys(fvsChecklist).filter((k) => fvsChecklist[k]),
      observacoes: ocorrencias || 'Inspeção técnica em conformidade com as tolerâncias normativas da ABNT.',
      assinatura: hasSignature ? 'Assinado Digitalmente no Canvas de Campo' : 'Assinatura Pendente'
    };

    try {
      const res = await fetch('/api/apontamento-campo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.success) {
        setMensagemSucesso(`🛡️ Inspeção ${fvsCodigo} homologada! Medição correspondente liberada.`);
      } else {
        setMensagemErro(`❌ Erro: ${data.error || 'Falha na transmissão da FVS'}`);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Erro de conexão';
      setMensagemErro(`❌ Erro de conexão: ${msg}`);
    } finally {
      setEnviando(false);
    }
  };

  // Gerar texto para o WhatsApp
  const mensagemWhatsApp = `*📋 RDO DIÁRIO — ${obra}*
📅 Data: ${dataHoje.split('-').reverse().join('/')}
☀️ Clima: Manhã ${climaManha} | Tarde ${climaTarde}
👷 Efetivo Total: ${totalEfetivo} pessoas (${totalProprio} Gestão / ${totalTerceiro} Terceirizados)
⏱️ Horas Trabalhadas: ${totalHH} HH ${horasParalisadas > 0 ? `(⚠️ ${horasParalisadas}h paralisadas por ${motivoParalisacao})` : '(Sem paralisação)'}
🔨 Frentes EAP: ${servicosEap.join(', ')}
🛡️ Inspeção: ${fvsCodigo} — ${fvsStatus === 'Aprovado' ? '🟢 Aprovada' : '🔴 Pendente'}
📝 Ocorrências: ${ocorrencias || 'Dia de produção normal dentro do cronograma.'}
_Enviado via Antigravity Mobile 4.0_`;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(mensagemWhatsApp);
    setCopiado(true);
    setTimeout(() => setCopiado(false), 2500);
  };

  const openWhatsApp = () => {
    const encoded = encodeURIComponent(mensagemWhatsApp);
    window.open(`https://api.whatsapp.com/send?text=${encoded}`, '_blank');
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 pb-20 select-none">
      {/* CABEÇALHO FIXO MOBILE */}
      <header className="sticky top-0 z-50 bg-zinc-900/90 backdrop-blur-md border-b border-zinc-800 px-4 py-3 shadow-lg">
        <div className="max-w-md mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-9 h-9 rounded-xl bg-blue-600 flex items-center justify-center text-white font-black shadow-blue-500/30 shadow-md">
              A11
            </div>
            <div>
              <h1 className="text-base font-bold tracking-tight text-white flex items-center">
                Coleta Digital
                <span className="ml-1.5 px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                  4.0
                </span>
              </h1>
              <p className="text-xs text-zinc-400">Mestre & Encarregados de Campo</p>
            </div>
          </div>

          <select
            value={obra}
            onChange={(e) => setObra(e.target.value)}
            className="bg-zinc-800 text-xs text-zinc-200 border border-zinc-700 rounded-lg px-2.5 py-1.5 font-medium outline-none focus:border-blue-500"
          >
            <option value="OBRA_TMULT">TMULT (Porto do Açu)</option>
            <option value="_TEMPLATE_OBRA_NOVA">Obra Nova (Template)</option>
          </select>
        </div>
      </header>

      {/* NAVEGAÇÃO DE ABAS */}
      <div className="max-w-md mx-auto px-4 pt-3">
        <div className="grid grid-cols-3 gap-1 bg-zinc-900 p-1 rounded-xl border border-zinc-800">
          <button
            onClick={() => setActiveTab('rdo')}
            className={`py-2 px-1 text-xs font-bold rounded-lg flex flex-col items-center justify-center transition-all ${
              activeTab === 'rdo'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <FileText className="w-4 h-4 mb-0.5" />
            RDO Diário
          </button>

          <button
            onClick={() => setActiveTab('fvs')}
            className={`py-2 px-1 text-xs font-bold rounded-lg flex flex-col items-center justify-center transition-all ${
              activeTab === 'fvs'
                ? 'bg-emerald-600 text-white shadow-md'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <ShieldCheck className="w-4 h-4 mb-0.5" />
            FVS Qualidade
          </button>

          <button
            onClick={() => setActiveTab('whatsapp')}
            className={`py-2 px-1 text-xs font-bold rounded-lg flex flex-col items-center justify-center transition-all ${
              activeTab === 'whatsapp'
                ? 'bg-emerald-700 text-white shadow-md'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <MessageSquare className="w-4 h-4 mb-0.5" />
            WhatsApp
          </button>
        </div>
      </div>

      {/* FEEDBACKS FLUTUANTES */}
      {mensagemSucesso && (
        <div className="max-w-md mx-auto px-4 mt-3">
          <div className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 p-3 rounded-xl text-xs flex items-center shadow-lg animate-fade-in">
            <CheckCircle2 className="w-5 h-5 mr-2 shrink-0 text-emerald-400" />
            <span>{mensagemSucesso}</span>
          </div>
        </div>
      )}

      {mensagemErro && (
        <div className="max-w-md mx-auto px-4 mt-3">
          <div className="bg-rose-500/10 border border-rose-500/30 text-rose-300 p-3 rounded-xl text-xs flex items-center shadow-lg">
            <XCircle className="w-5 h-5 mr-2 shrink-0 text-rose-400" />
            <span>{mensagemErro}</span>
          </div>
        </div>
      )}

      {/* CORPO PRINCIPAL */}
      <main className="max-w-md mx-auto px-4 mt-3 space-y-4">
        {/* ========================================================================= */}
        {/* ABA 1: RDO RÁPIDO */}
        {/* ========================================================================= */}
        {activeTab === 'rdo' && (
          <div className="space-y-4">
            {/* DATA */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 shadow-sm">
              <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-2 flex items-center">
                <Calendar className="w-3.5 h-3.5 mr-1.5 text-blue-400" />
                Data de Apontamento
              </label>
              <input
                type="date"
                value={dataHoje}
                onChange={(e) => setDataHoje(e.target.value)}
                className="w-full bg-zinc-950 border border-zinc-700 rounded-xl px-3 py-2.5 text-sm font-semibold text-white outline-none focus:border-blue-500"
              />
            </div>

            {/* CONDIÇÕES DE CLIMA */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 shadow-sm">
              <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-2 flex items-center">
                <Sun className="w-3.5 h-3.5 mr-1.5 text-amber-400" />
                Condição do Clima
              </label>
              <div className="grid grid-cols-2 gap-2 mb-3">
                <div>
                  <span className="text-[11px] text-zinc-500 font-medium block mb-1">Manhã</span>
                  <div className="grid grid-cols-2 gap-1.5">
                    {['Sol', 'Nublado', 'Chuva Leve', 'Chuva Forte'].map((c) => (
                      <button
                        key={c}
                        onClick={() => setClimaManha(c)}
                        className={`py-2 px-1 text-xs rounded-xl font-semibold border transition-all ${
                          climaManha === c
                            ? 'bg-blue-600 text-white border-blue-500 shadow-sm'
                            : 'bg-zinc-950 text-zinc-400 border-zinc-800 hover:border-zinc-700'
                        }`}
                      >
                        {c}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <span className="text-[11px] text-zinc-500 font-medium block mb-1">Tarde</span>
                  <div className="grid grid-cols-2 gap-1.5">
                    {['Sol', 'Nublado', 'Chuva Leve', 'Chuva Forte'].map((c) => (
                      <button
                        key={c}
                        onClick={() => setClimaTarde(c)}
                        className={`py-2 px-1 text-xs rounded-xl font-semibold border transition-all ${
                          climaTarde === c
                            ? 'bg-blue-600 text-white border-blue-500 shadow-sm'
                            : 'bg-zinc-950 text-zinc-400 border-zinc-800 hover:border-zinc-700'
                        }`}
                      >
                        {c}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* PARALISAÇÃO POR CLIMA */}
              <div className="pt-2 border-t border-zinc-800/80">
                <div className="flex justify-between items-center mb-1.5">
                  <span className="text-xs text-zinc-300 font-medium flex items-center">
                    <Clock className="w-3.5 h-3.5 mr-1 text-rose-400" />
                    Horas Paralisadas por Chuva:
                  </span>
                  <span className="text-xs font-bold text-rose-400 font-mono">
                    {horasParalisadas.toFixed(1)} h
                  </span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="8.8"
                  step="0.5"
                  value={horasParalisadas}
                  onChange={(e) => setHorasParalisadas(parseFloat(e.target.value))}
                  className="w-full accent-rose-500"
                />
                {horasParalisadas > 0 && (
                  <input
                    type="text"
                    value={motivoParalisacao}
                    onChange={(e) => setMotivoParalisacao(e.target.value)}
                    placeholder="Motivo da paralisação (ex: Chuva forte, falta de material)"
                    className="mt-2 w-full bg-zinc-950 border border-zinc-800 rounded-lg px-3 py-2 text-xs text-white outline-none focus:border-rose-500"
                  />
                )}
              </div>
            </div>

            {/* EFETIVO DE CANTEIRO (HEADCOUNT) */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 shadow-sm space-y-3">
              <div className="flex justify-between items-center">
                <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider flex items-center">
                  <Users className="w-3.5 h-3.5 mr-1.5 text-emerald-400" />
                  Efetivo no Canteiro
                </label>
                <div className="bg-zinc-800 px-2.5 py-1 rounded-lg text-xs font-bold text-emerald-400">
                  Total: {totalEfetivo} ({totalHH} HH)
                </div>
              </div>

              {/* CONTADORES RÁPIDOS */}
              <div className="space-y-2 pt-1">
                {ITENS_EFETIVO.map((item) => (
                  <div
                    key={item.key}
                    className="flex justify-between items-center bg-zinc-950 px-3 py-2 rounded-xl border border-zinc-800/80"
                  >
                    <span className="text-xs font-medium text-zinc-300">{item.label}</span>
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => updateCount(item.key, -1)}
                        className="w-8 h-8 rounded-lg bg-zinc-800 text-zinc-200 font-black text-sm flex items-center justify-center active:bg-zinc-700"
                      >
                        -
                      </button>
                      <span className="w-7 text-center font-bold text-sm text-white font-mono">
                        {efetivo[item.key]}
                      </span>
                      <button
                        onClick={() => updateCount(item.key, 1)}
                        className="w-8 h-8 rounded-lg bg-blue-600 text-white font-black text-sm flex items-center justify-center active:bg-blue-500 shadow-sm"
                      >
                        +
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* FRENTES EAP EXECUTADAS */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 shadow-sm">
              <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider block mb-2">
                Frentes EAP Executadas Hoje
              </label>
              <div className="grid grid-cols-1 gap-1.5">
                {[
                  '1.3.1 Gabarito e Locação Topográfica',
                  '1.3.2 Escavação e Lastro de Sapatas',
                  '1.3.3 Armaduras e Formas de Fundação',
                  '1.3.4 Concretagem de Blocos/Sapatas',
                  '1.4.1 Pilares e Vigas de Concreto',
                  '2.1.1 Alvenaria de Vedação Blocos 14x19x39',
                  '3.1.1 Eletrodutos e Caixas em Laje/Parede'
                ].map((servico) => {
                  const active = servicosEap.includes(servico);
                  return (
                    <button
                      key={servico}
                      onClick={() => toggleEap(servico)}
                      className={`py-2 px-3 rounded-xl text-left text-xs font-medium border flex items-center justify-between transition-all ${
                        active
                          ? 'bg-blue-950/40 text-blue-300 border-blue-600/50'
                          : 'bg-zinc-950 text-zinc-400 border-zinc-800 hover:border-zinc-700'
                      }`}
                    >
                      <span>{servico}</span>
                      {active ? (
                        <CheckCircle2 className="w-4 h-4 text-blue-400 shrink-0" />
                      ) : (
                        <div className="w-4 h-4 rounded-full border border-zinc-700 shrink-0" />
                      )}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* OCORRÊNCIAS */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 shadow-sm">
              <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider block mb-2">
                Ocorrências e Diário de Bordo
              </label>
              <textarea
                value={ocorrencias}
                onChange={(e) => setOcorrencias(e.target.value)}
                placeholder="Ex: Concretagem das sapatas S11 a S15 concluída. Caminhão usina entregou 8m³ com abatimento 10cm aprovado..."
                rows={3}
                className="w-full bg-zinc-950 border border-zinc-800 rounded-xl p-3 text-xs text-zinc-200 outline-none focus:border-blue-500"
              />
            </div>

            {/* BOTÃO DE TRANSMISSÃO */}
            <button
              onClick={handleEnviarRdo}
              disabled={enviando}
              className="w-full py-4 rounded-2xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm tracking-wide shadow-blue-500/20 shadow-lg flex items-center justify-center space-x-2 active:scale-[0.99] transition-all disabled:opacity-50"
            >
              <Send className="w-4 h-4" />
              <span>{enviando ? 'Gravando e Transmitindo...' : 'Gravar e Transmitir RDO Diário'}</span>
            </button>
          </div>
        )}

        {/* ========================================================================= */}
        {/* ABA 2: FVS QUALIDADE */}
        {/* ========================================================================= */}
        {activeTab === 'fvs' && (
          <div className="space-y-4">
            {/* SELEÇÃO DA FVS */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 shadow-sm">
              <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-2 flex items-center">
                <ShieldCheck className="w-3.5 h-3.5 mr-1.5 text-emerald-400" />
                Ficha de Verificação de Serviço (FVS)
              </label>
              <select
                value={fvsCodigo}
                onChange={(e) => setFvsCodigo(e.target.value)}
                className="w-full bg-zinc-950 border border-zinc-700 rounded-xl px-3 py-2.5 text-sm font-semibold text-white outline-none focus:border-emerald-500 mb-3"
              >
                <option value="FVS-01">FVS-01: Topografia e Locação de Eixos</option>
                <option value="FVS-02">FVS-02: Fundações e Escavação de Valas</option>
                <option value="FVS-03">FVS-03: Estrutura, Fôrmas e Concretagem</option>
                <option value="FVS-04">FVS-04: Alvenaria de Vedação</option>
                <option value="FVS-05">FVS-05: Impermeabilização e Estanqueidade 72h</option>
                <option value="FVS-06">FVS-06: Instalações Hidráulicas (Pressão)</option>
                <option value="FVS-07">FVS-07: Instalações Elétricas e SPDA</option>
                <option value="FVS-08">FVS-08: Cobertura e Esquadrias</option>
              </select>

              {/* Status do Parecer */}
              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={() => setFvsStatus('Aprovado')}
                  className={`py-2.5 px-3 rounded-xl text-xs font-bold border flex items-center justify-center space-x-2 transition-all ${
                    fvsStatus === 'Aprovado'
                      ? 'bg-emerald-600 text-white border-emerald-500 shadow-md shadow-emerald-600/30'
                      : 'bg-zinc-950 text-zinc-400 border-zinc-800'
                  }`}
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Aprovado (Liberar)</span>
                </button>

                <button
                  onClick={() => setFvsStatus('Reprovado')}
                  className={`py-2.5 px-3 rounded-xl text-xs font-bold border flex items-center justify-center space-x-2 transition-all ${
                    fvsStatus === 'Reprovado'
                      ? 'bg-rose-600 text-white border-rose-500 shadow-md shadow-rose-600/30'
                      : 'bg-zinc-950 text-zinc-400 border-zinc-800'
                  }`}
                >
                  <XCircle className="w-4 h-4" />
                  <span>Reprovado (Bloquear)</span>
                </button>
              </div>
            </div>

            {/* CHECKLIST ESPECÍFICO */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 shadow-sm">
              <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider block mb-2">
                Critérios Técnicos Obrigatórios (POP / NBR)
              </label>
              <div className="space-y-2">
                {Object.keys(fvsChecklist).map((item) => (
                  <button
                    key={item}
                    type="button"
                    onClick={() => toggleChecklistItem(item)}
                    className={`w-full text-left p-2.5 rounded-xl border text-xs flex items-center justify-between transition-all ${
                      fvsChecklist[item]
                        ? 'bg-emerald-950/30 border-emerald-500/50 text-emerald-300'
                        : 'bg-zinc-950 border-zinc-800 text-zinc-400'
                    }`}
                  >
                    <span>{item}</span>
                    {fvsChecklist[item] ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    ) : (
                      <XCircle className="w-4 h-4 text-zinc-600 shrink-0" />
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* MEDIÇÃO DA TRENA E TOLERÂNCIA */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 shadow-sm">
              <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider block mb-2">
                Tolerância e Medição de Campo (Trena / Nível)
              </label>
              <input
                type="text"
                value={fvsTolerancia}
                onChange={(e) => setFvsTolerancia(e.target.value)}
                placeholder="Ex: Desvio medido 2mm; Abatimento slump = 10,5cm..."
                className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-3 py-2.5 text-xs text-white outline-none focus:border-emerald-500"
              />
            </div>

            {/* CANVAS DE ASSINATURA DIGITAL */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 shadow-sm">
              <div className="flex justify-between items-center mb-2">
                <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider flex items-center">
                  <PenTool className="w-3.5 h-3.5 mr-1.5 text-emerald-400" />
                  Assinatura na Tela (Dedo / Stylus)
                </label>
                <button
                  onClick={clearSignature}
                  className="text-[11px] text-zinc-500 hover:text-zinc-300 flex items-center"
                >
                  <Trash2 className="w-3 h-3 mr-1" />
                  Limpar
                </button>
              </div>

              <div className="bg-zinc-950 border border-zinc-800 rounded-xl overflow-hidden touch-none relative">
                <canvas
                  ref={canvasRef}
                  width={340}
                  height={130}
                  onMouseDown={startDrawing}
                  onMouseMove={draw}
                  onMouseUp={stopDrawing}
                  onMouseLeave={stopDrawing}
                  onTouchStart={startDrawing}
                  onTouchMove={draw}
                  onTouchEnd={stopDrawing}
                  className="w-full h-32 cursor-crosshair"
                />
                {!hasSignature && (
                  <div className="absolute inset-0 flex items-center justify-center pointer-events-none text-zinc-600 text-xs font-medium">
                    Toque e assine aqui com o dedo
                  </div>
                )}
              </div>
              <p className="text-[10px] text-zinc-500 mt-1.5 text-right">
                {hasSignature ? '🟢 Assinatura capturada' : '⚪ Aguardando assinatura'}
              </p>
            </div>

            {/* BOTÃO DE HOMOLOGAÇÃO */}
            <button
              onClick={handleEnviarFvs}
              disabled={enviando}
              className="w-full py-4 rounded-2xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm tracking-wide shadow-emerald-500/20 shadow-lg flex items-center justify-center space-x-2 active:scale-[0.99] transition-all disabled:opacity-50"
            >
              <ShieldCheck className="w-4 h-4" />
              <span>{enviando ? 'Homologando Inspeção...' : `Homologar ${fvsCodigo} e Desbloquear Medição`}</span>
            </button>
          </div>
        )}

        {/* ========================================================================= */}
        {/* ABA 3: WHATSAPP ASSISTANT */}
        {/* ========================================================================= */}
        {activeTab === 'whatsapp' && (
          <div className="space-y-4">
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 shadow-sm">
              <div className="flex justify-between items-center mb-2">
                <label className="text-xs font-semibold text-emerald-400 uppercase tracking-wider flex items-center">
                  <MessageSquare className="w-3.5 h-3.5 mr-1.5" />
                  Mensagem Estruturada de WhatsApp
                </label>
                <span className="text-[10px] bg-emerald-950 text-emerald-400 px-2 py-0.5 rounded-md border border-emerald-800">
                  Pronto para Envio
                </span>
              </div>
              <p className="text-xs text-zinc-400 mb-3">
                Esta mensagem é gerada automaticamente com os dados preenchidos no RDO para envio rápido no grupo da obra.
              </p>

              <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-3 text-xs font-mono text-zinc-300 whitespace-pre-wrap leading-relaxed">
                {mensagemWhatsApp}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={copyToClipboard}
                className="py-3.5 px-3 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-white text-xs font-bold flex items-center justify-center space-x-1.5 active:scale-[0.99] transition-all"
              >
                {copiado ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                <span>{copiado ? 'Copiado!' : 'Copiar Texto'}</span>
              </button>

              <button
                onClick={openWhatsApp}
                className="py-3.5 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold flex items-center justify-center space-x-1.5 shadow-emerald-600/30 shadow-md active:scale-[0.99] transition-all"
              >
                <Send className="w-4 h-4" />
                <span>Abrir WhatsApp</span>
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
