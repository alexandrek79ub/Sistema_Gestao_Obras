"use client";

import React, { useEffect, useState } from 'react';
import { useObra } from '@/context/ObraContext';
import {
  HardHat,
  ShieldCheck,
  AlertTriangle,
  UserX,
  Users,
  Calendar,
  Award,
  CheckCircle2,
  FileText,
  AlertCircle
} from 'lucide-react';

interface OperarioAso {
  id: string;
  nome: string;
  funcao: string;
  empresa: string;
  tipoAso: string;
  vencimento: string;
  diasParaVencer: number;
  status: 'APTO' | 'ALERTA_30D' | 'VENCIDO_BLOQUEADO';
  treinamentos: string[];
}

interface ProgramaLegal {
  programa: string;
  titular: string;
  emissao: string;
  vigencia: string;
  status: 'VIGENTE' | 'RENOVAR' | 'VENCIDO';
  responsavel: string;
}

interface SstResponse {
  success: boolean;
  obra: string;
  resumo: {
    efetivoTotal: number;
    totalProprios: number;
    totalTerceiros: number;
    aptos: number;
    alerta30d: number;
    bloqueados: number;
    indiceConformidade: number;
    diasSemAcidentes: number;
    taxaDdsSemanal: number;
    temaDdsSemana: string;
  };
  operarios: OperarioAso[];
  programasLegais: ProgramaLegal[];
}

export default function SstPage() {
  const { obraAtiva } = useObra();
  const [data, setData] = useState<SstResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [filtroStatus, setFiltroStatus] = useState<string>('TODOS');

  useEffect(() => {
    async function carregarSst() {
      setLoading(true);
      try {
        const res = await fetch(`/api/sst?obra=${encodeURIComponent(obraAtiva)}`);
        const json: SstResponse = await res.json();
        setData(json);
      } catch (err) {
        console.error('Erro ao carregar SST:', err);
      } finally {
        setLoading(false);
      }
    }
    carregarSst();
  }, [obraAtiva]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="flex flex-col items-center space-y-3">
          <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm text-zinc-400">Carregando painel de conformidade SST ({obraAtiva})...</p>
        </div>
      </div>
    );
  }

  const resumo = data?.resumo || {
    efetivoTotal: 13,
    totalProprios: 5,
    totalTerceiros: 8,
    aptos: 12,
    alerta30d: 1,
    bloqueados: 0,
    indiceConformidade: 100,
    diasSemAcidentes: 18,
    taxaDdsSemanal: 100,
    temaDdsSemana: 'Uso obrigatório de EPI e trabalho em altura NR-35',
  };

  const operarios = data?.operarios || [];
  const programas = data?.programasLegais || [];

  const operariosFiltrados = operarios.filter((op) => {
    if (filtroStatus === 'TODOS') return true;
    return op.status === filtroStatus;
  });

  return (
    <div className="space-y-6">
      {/* CABEÇALHO */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-3">
            <HardHat className="w-8 h-8 text-amber-500" />
            Segurança do Trabalho (SST) & Compliance RH
          </h1>
          <p className="text-zinc-400 mt-1">
            Controle de portaria, semáforo de ASOs em D-30, programas legais (PGR/PCMSO) e matriz de NRs.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-3 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-bold rounded-lg flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4" /> {resumo.diasSemAcidentes} Dias Sem Acidentes
          </span>
        </div>
      </div>

      {/* KPI CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <div className="flex items-center justify-between">
            <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Efetivo Cadastrado</p>
            <Users className="w-4 h-4 text-blue-400" />
          </div>
          <p className="text-2xl font-bold text-white mt-2">{resumo.efetivoTotal} colaboradores</p>
          <p className="text-xs text-zinc-400 mt-1">
            {resumo.totalProprios} Próprios | {resumo.totalTerceiros} Terceirizados
          </p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <div className="flex items-center justify-between">
            <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Aptos na Portaria</p>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-emerald-400 mt-2">{resumo.aptos}</p>
          <p className="text-xs text-emerald-400/80 mt-1">ASO e Treinamentos Válidos</p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <div className="flex items-center justify-between">
            <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Alerta Vencendo (D-30)</p>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-amber-400 mt-2">{resumo.alerta30d}</p>
          <p className="text-xs text-amber-400/80 mt-1">Renovação Programada</p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <div className="flex items-center justify-between">
            <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Bloqueio Portaria</p>
            <UserX className="w-4 h-4 text-rose-400" />
          </div>
          <p className="text-2xl font-bold text-rose-400 mt-2">{resumo.bloqueados}</p>
          <p className="text-xs text-rose-400/80 mt-1">Acesso Interditado no Canteiro</p>
        </div>
      </div>

      {/* BANNER DO PROGRAMA SEMANAL DE DDS */}
      <div className="bg-gradient-to-r from-amber-500/10 via-zinc-900 to-zinc-900 border border-amber-500/30 p-5 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 bg-amber-500/20 text-amber-400 font-bold text-xs uppercase rounded">
              DDS da Semana (Semana 03)
            </span>
            <span className="text-xs text-zinc-400">Taxa de Realização: {resumo.taxaDdsSemanal}%</span>
          </div>
          <h3 className="text-base font-semibold text-white">{resumo.temaDdsSemana}</h3>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-right">
            <p className="text-xs text-zinc-400">Instrutor Responsável</p>
            <p className="text-xs font-semibold text-zinc-200">Carlos Eduardo (TST)</p>
          </div>
        </div>
      </div>

      {/* PAINEL SEMAFÓRICO DE ASOS */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden">
        <div className="p-4 bg-zinc-950/60 border-b border-zinc-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <Users className="w-4 h-4 text-blue-400" />
            Controle Individual de ASOs e Acesso de Portaria
          </h3>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setFiltroStatus('TODOS')}
              className={`px-2.5 py-1 text-xs rounded-md font-medium transition-colors ${
                filtroStatus === 'TODOS' ? 'bg-blue-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:text-white'
              }`}
            >
              Todos ({operarios.length})
            </button>
            <button
              onClick={() => setFiltroStatus('APTO')}
              className={`px-2.5 py-1 text-xs rounded-md font-medium transition-colors ${
                filtroStatus === 'APTO' ? 'bg-emerald-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:text-white'
              }`}
            >
              Aptos ({resumo.aptos})
            </button>
            <button
              onClick={() => setFiltroStatus('ALERTA_30D')}
              className={`px-2.5 py-1 text-xs rounded-md font-medium transition-colors ${
                filtroStatus === 'ALERTA_30D' ? 'bg-amber-600 text-white' : 'bg-zinc-800 text-zinc-400 hover:text-white'
              }`}
            >
              Alerta ({resumo.alerta30d})
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-zinc-950/40 text-xs uppercase font-bold text-zinc-400 border-b border-zinc-800">
              <tr>
                <th className="py-3 px-4">Operário / Colaborador</th>
                <th className="py-3 px-4">Função / Cargo</th>
                <th className="py-3 px-4">Empresa Vinculada</th>
                <th className="py-3 px-4">Vencimento ASO</th>
                <th className="py-3 px-4">Treinamentos NRs</th>
                <th className="py-3 px-4 text-center">Status Portaria</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/60 text-xs">
              {operariosFiltrados.map((op) => (
                <tr key={op.id} className="hover:bg-zinc-800/30 transition-colors">
                  <td className="py-3 px-4">
                    <p className="font-semibold text-white">{op.nome}</p>
                    <p className="text-[10px] text-zinc-500 font-mono">{op.id} • {op.tipoAso}</p>
                  </td>
                  <td className="py-3 px-4 text-zinc-300 font-medium">{op.funcao}</td>
                  <td className="py-3 px-4 text-zinc-400">{op.empresa}</td>
                  <td className="py-3 px-4">
                    <p className="font-mono text-zinc-200">{op.vencimento}</p>
                    <p className="text-[10px] text-zinc-500">{op.diasParaVencer} dias restantes</p>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex flex-wrap gap-1">
                      {op.treinamentos.map((t) => (
                        <span key={t} className="px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-300 text-[10px] font-mono">
                          {t}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="py-3 px-4 text-center">
                    {op.status === 'APTO' ? (
                      <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 inline-flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3" /> Apto
                      </span>
                    ) : op.status === 'ALERTA_30D' ? (
                      <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30 inline-flex items-center gap-1">
                        <AlertCircle className="w-3 h-3" /> Vence &lt; 30d
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30 inline-flex items-center gap-1">
                        <UserX className="w-3 h-3" /> Bloqueado
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* QUADRO DE PROGRAMAS LEGAIS */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden">
        <div className="p-4 bg-zinc-950/60 border-b border-zinc-800 flex justify-between items-center">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <FileText className="w-4 h-4 text-purple-400" />
            Programas Legais e Documentação Ambiental (NR-01, NR-07, NR-09, NR-18)
          </h3>
          <span className="text-xs text-zinc-400">Renovação Anual Obrigatória</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-zinc-950/40 text-xs uppercase font-bold text-zinc-400 border-b border-zinc-800">
              <tr>
                <th className="py-3 px-4">Programa / Laudo</th>
                <th className="py-3 px-4">Titular Responsável</th>
                <th className="py-3 px-4">Emissão</th>
                <th className="py-3 px-4">Vigência Final</th>
                <th className="py-3 px-4">Responsável Técnico</th>
                <th className="py-3 px-4 text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/60 text-xs">
              {programas.map((prog, idx) => (
                <tr key={idx} className="hover:bg-zinc-800/30 transition-colors">
                  <td className="py-3 px-4 font-semibold text-white">{prog.programa}</td>
                  <td className="py-3 px-4 text-zinc-400">{prog.titular}</td>
                  <td className="py-3 px-4 font-mono text-zinc-400">{prog.emissao}</td>
                  <td className="py-3 px-4 font-mono text-zinc-300">{prog.vigencia}</td>
                  <td className="py-3 px-4 text-zinc-400">{prog.responsavel}</td>
                  <td className="py-3 px-4 text-center">
                    <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                      🟢 Vigente
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
