"use client";

import React, { useEffect, useState } from 'react';
import { useObra } from '@/context/ObraContext';
import {
  FileText,
  Users,
  Sun,
  Clock,
  CheckCircle2,
  AlertTriangle,
  HardHat,
  Truck,
  Smartphone,
  Calendar,
  Layers
} from 'lucide-react';

interface RdoItem {
  id: string;
  arquivo: string;
  data: string;
  diaSemana?: string;
  climaManha: string;
  climaTarde: string;
  condicao: string;
  horasParalisacao: number;
  equipePropria: number;
  equipeTerceirizada: number;
  totalEfetivo: number;
  totalHH: number;
  equipamentos: string;
  frentesEap: string;
  fvsInspecionada: string;
  fvsResultado: string;
  ocorrencias: string;
}

interface RdoResponse {
  success: boolean;
  obra: string;
  resumo: {
    totalRdos: number;
    ultimoRdo: string;
    ultimaData: string;
    totalHHAcumulado: number;
    efetivoMedio: number;
    climaAtual: string;
    apontamentosPendentes: number;
  };
  rdos: RdoItem[];
  apontamentosCampo: unknown[];
}

export default function RdoPage() {
  const { obraAtiva } = useObra();
  const [data, setData] = useState<RdoResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedRdoId, setSelectedRdoId] = useState<string>('');

  useEffect(() => {
    async function carregarRdos() {
      setLoading(true);
      try {
        const res = await fetch(`/api/rdo?obra=${encodeURIComponent(obraAtiva)}`);
        const json: RdoResponse = await res.json();
        setData(json);
        if (json.rdos && json.rdos.length > 0) {
          setSelectedRdoId(json.rdos[0].id);
        }
      } catch (err) {
        console.error('Erro ao carregar RDOs:', err);
      } finally {
        setLoading(false);
      }
    }
    carregarRdos();
  }, [obraAtiva]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="flex flex-col items-center space-y-3">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm text-zinc-400">Carregando diários de obra ({obraAtiva})...</p>
        </div>
      </div>
    );
  }

  const rdos = data?.rdos || [];
  const resumo = data?.resumo || {
    totalRdos: 0,
    ultimoRdo: 'N/A',
    ultimaData: 'N/A',
    totalHHAcumulado: 0,
    efetivoMedio: 0,
    climaAtual: 'N/A',
    apontamentosPendentes: 0,
  };

  const selectedRdo = rdos.find((r) => r.id === selectedRdoId) || rdos[0];

  return (
    <div className="space-y-6">
      {/* CABEÇALHO */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-3">
            <FileText className="w-8 h-8 text-blue-500" />
            Diário de Obra & Produção (RDO)
          </h1>
          <p className="text-zinc-400 mt-1">
            Apontamento de efetivo, avanço de frentes da EAP, horas-homem e inspeções de qualidade.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs text-zinc-400">Diário Ativo:</span>
          <select
            value={selectedRdoId}
            onChange={(e) => setSelectedRdoId(e.target.value)}
            className="bg-zinc-900 text-white text-sm font-semibold border border-zinc-700 rounded-lg px-3 py-1.5 focus:outline-none focus:border-blue-500"
          >
            {rdos.map((r) => (
              <option key={r.id} value={r.id}>
                {r.id} — {r.data} {r.diaSemana ? `(${r.diaSemana})` : ''}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* KPI CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <div className="flex items-center justify-between">
            <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Total de Diários</p>
            <Calendar className="w-4 h-4 text-blue-400" />
          </div>
          <p className="text-2xl font-bold text-white mt-2">{resumo.totalRdos}</p>
          <p className="text-xs text-zinc-400 mt-1">Último: {resumo.ultimoRdo} ({resumo.ultimaData})</p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <div className="flex items-center justify-between">
            <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">HH Acumulado</p>
            <Clock className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-white mt-2">{resumo.totalHHAcumulado.toLocaleString('pt-BR')} h</p>
          <p className="text-xs text-zinc-400 mt-1">Horas-Homem no Canteiro</p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <div className="flex items-center justify-between">
            <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Efetivo Médio</p>
            <Users className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-white mt-2">{resumo.efetivoMedio} operários</p>
          <p className="text-xs text-zinc-400 mt-1">Próprios + Terceirizados</p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <div className="flex items-center justify-between">
            <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Clima / Turno</p>
            <Sun className="w-4 h-4 text-yellow-400" />
          </div>
          <p className="text-2xl font-bold text-white mt-2">{resumo.climaAtual}</p>
          <p className="text-xs text-emerald-400 mt-1 flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" /> Condição Praticável
          </p>
        </div>
      </div>

      {/* DETALHE DO RDO SELECIONADO */}
      {selectedRdo ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* COLUNA 1 & 2: CONTEÚDO PRINCIPAL DO RDO */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden">
              <div className="p-4 bg-zinc-950/60 border-b border-zinc-800 flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="px-2.5 py-1 bg-blue-500/20 text-blue-400 border border-blue-500/30 font-mono font-bold text-sm rounded-md">
                    {selectedRdo.id}
                  </span>
                  <span className="text-white font-semibold">
                    {selectedRdo.data} {selectedRdo.diaSemana ? `— ${selectedRdo.diaSemana}` : ''}
                  </span>
                </div>
                <span className="text-xs text-zinc-400 bg-zinc-800/80 px-2.5 py-1 rounded">
                  Arquivo: {selectedRdo.arquivo}
                </span>
              </div>

              <div className="p-6 space-y-6">
                {/* CLIMA E PRATICABILIDADE */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-zinc-950/40 p-4 rounded-lg border border-zinc-800/60">
                  <div>
                    <p className="text-xs text-zinc-400 uppercase font-bold">Turno Manhã</p>
                    <p className="text-zinc-200 font-medium mt-1">{selectedRdo.climaManha}</p>
                  </div>
                  <div>
                    <p className="text-xs text-zinc-400 uppercase font-bold">Turno Tarde</p>
                    <p className="text-zinc-200 font-medium mt-1">{selectedRdo.climaTarde}</p>
                  </div>
                  <div>
                    <p className="text-xs text-zinc-400 uppercase font-bold">Paralisação Chuva</p>
                    <p className="text-zinc-200 font-medium mt-1">
                      {selectedRdo.horasParalisacao > 0 ? (
                        <span className="text-amber-400 font-bold">{selectedRdo.horasParalisacao} horas</span>
                      ) : (
                        <span className="text-emerald-400 font-bold">0.0h (Sem impacto)</span>
                      )}
                    </p>
                  </div>
                </div>

                {/* EFETIVO PRESENTE */}
                <div>
                  <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-3 flex items-center gap-2">
                    <Users className="w-4 h-4 text-emerald-400" />
                    Efetivo Presente & HH Produzido
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
                    <div className="bg-zinc-800/30 p-3 rounded-lg border border-zinc-800/50">
                      <p className="text-xs text-zinc-400">Equipe Própria</p>
                      <p className="text-xl font-bold text-white mt-1">{selectedRdo.equipePropria}</p>
                      <p className="text-[10px] text-zinc-400">Gestão, TST, Vigia</p>
                    </div>
                    <div className="bg-zinc-800/30 p-3 rounded-lg border border-zinc-800/50">
                      <p className="text-xs text-zinc-400">Terceirizados</p>
                      <p className="text-xl font-bold text-white mt-1">{selectedRdo.equipeTerceirizada}</p>
                      <p className="text-[10px] text-zinc-400">Subempreiteiros</p>
                    </div>
                    <div className="bg-zinc-800/30 p-3 rounded-lg border border-zinc-800/50">
                      <p className="text-xs text-zinc-400">Total Pessoas</p>
                      <p className="text-xl font-bold text-emerald-400 mt-1">{selectedRdo.totalEfetivo}</p>
                      <p className="text-[10px] text-zinc-400">No Canteiro</p>
                    </div>
                    <div className="bg-zinc-800/30 p-3 rounded-lg border border-zinc-800/50">
                      <p className="text-xs text-zinc-400">HH no Dia</p>
                      <p className="text-xl font-bold text-blue-400 mt-1">{selectedRdo.totalHH} h</p>
                      <p className="text-[10px] text-zinc-400">Horas-Homem</p>
                    </div>
                  </div>
                </div>

                {/* FRENTES EAP E EQUIPAMENTOS */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-zinc-950/40 p-4 rounded-lg border border-zinc-800/60">
                    <h4 className="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                      <Layers className="w-3.5 h-3.5 text-blue-400" />
                      Frentes de Serviço EAP
                    </h4>
                    <p className="text-sm text-zinc-200 font-medium">{selectedRdo.frentesEap}</p>
                  </div>

                  <div className="bg-zinc-950/40 p-4 rounded-lg border border-zinc-800/60">
                    <h4 className="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                      <Truck className="w-3.5 h-3.5 text-amber-400" />
                      Equipamentos em Operação
                    </h4>
                    <p className="text-sm text-zinc-200 font-medium">{selectedRdo.equipamentos}</p>
                  </div>
                </div>

                {/* OCORRÊNCIAS E DIÁRIO DE BORDO */}
                <div className="bg-zinc-950/60 p-4 rounded-lg border border-zinc-800">
                  <h4 className="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-2">
                    Relato de Ocorrências e Diário de Bordo
                  </h4>
                  <p className="text-sm text-zinc-300 leading-relaxed whitespace-pre-wrap">
                    {selectedRdo.ocorrencias}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* COLUNA 3: PAINEL LATERAL (QUALIDADE & COLETA MOBILE) */}
          <div className="space-y-6">
            {/* INSPEÇÃO FVS VINCULADA */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-4">
              <h3 className="text-sm font-semibold text-white uppercase tracking-wider flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                Inspeção de Qualidade (FVS)
              </h3>
              <div className="bg-zinc-950/60 p-4 rounded-lg border border-zinc-800 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-xs text-zinc-400">Ficha Inspecionada:</span>
                  <span className="text-sm font-bold text-white font-mono">{selectedRdo.fvsInspecionada}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-zinc-400">Status da Inspeção:</span>
                  <span className="px-2 py-0.5 rounded text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    {selectedRdo.fvsResultado || 'Aprovado'}
                  </span>
                </div>
                <p className="text-xs text-zinc-400 pt-2 border-t border-zinc-800">
                  Serviço validado segundo a Regra da Trena (POP 09) e liberado para prosseguimento.
                </p>
              </div>
            </div>

            {/* STATUS DO APLICATIVO MOBILE */}
            <div className="bg-gradient-to-br from-zinc-900 to-zinc-950 border border-emerald-500/30 rounded-xl p-5 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2.5">
                  <div className="w-8 h-8 rounded-lg bg-emerald-500/20 flex items-center justify-center text-emerald-400">
                    <Smartphone className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-white">Coleta Mobile 4.0</h4>
                    <p className="text-[10px] text-emerald-400">Sincronização em Tempo Real</p>
                  </div>
                </div>
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
              </div>
              <p className="text-xs text-zinc-400 leading-relaxed">
                Mestres e encarregados podem apontar efetivo, clima, fotos e assinar FVSs diretamente no canteiro pelo celular.
              </p>
              <a
                href="/campo"
                target="_blank"
                rel="noreferrer"
                className="block text-center w-full py-2.5 px-4 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition-colors"
              >
                Abrir App de Coleta de Campo
              </a>
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-12 text-center">
          <FileText className="w-12 h-12 text-zinc-600 mx-auto mb-3" />
          <p className="text-lg font-semibold text-white">Nenhum RDO encontrado para esta obra</p>
          <p className="text-sm text-zinc-400 mt-1">
            Gere novos relatórios através do script: <code className="text-blue-400">python scripts/gerar_rdo.py --obra {obraAtiva}</code>
          </p>
        </div>
      )}
    </div>
  );
}
