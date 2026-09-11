"use client";

import React, { useEffect, useState } from 'react';
import { useObra } from '@/context/ObraContext';
import {
  ShieldCheck,
  CheckCircle2,
  Clock,
  AlertOctagon,
  Lock,
  Unlock,
  ChevronDown,
  ChevronUp,
  FileBadge,
  Info
} from 'lucide-react';

interface FvsItem {
  id: string;
  codigo: string;
  titulo: string;
  norma: string;
  pop: string;
  contratoBloqueado: string;
  servicoLiberado: string;
  status: 'APROVADO' | 'EM_INSPECAO' | 'BLOQUEADO' | 'PENDENTE';
  dataUltimaInspecao?: string;
  responsavel?: string;
  toleranciaCritica: string;
  checklist: string[];
}

interface SubcontratoItem {
  codigo: string;
  nome: string;
  fvsCondicionante: string;
  statusMedicao: 'LIBERADO' | 'RETENCAO_QUALIDADE' | 'BLOQUEADO';
  retencaoTecnicaPercent: number;
}

interface QualidadeResponse {
  success: boolean;
  obra: string;
  resumo: {
    totalFvss: number;
    aprovadas: number;
    emInspecao: number;
    pendentes: number;
    taxaConformidade: number;
    contratosBloqueados: number;
  };
  fvss: FvsItem[];
  subcontratos: SubcontratoItem[];
}

export default function QualidadePage() {
  const { obraAtiva } = useObra();
  const [data, setData] = useState<QualidadeResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [expandedFvs, setExpandedFvs] = useState<string | null>('fvs-01');

  useEffect(() => {
    async function carregarQualidade() {
      setLoading(true);
      try {
        const res = await fetch(`/api/qualidade?obra=${encodeURIComponent(obraAtiva)}`);
        const json: QualidadeResponse = await res.json();
        setData(json);
      } catch (err) {
        console.error('Erro ao carregar qualidade:', err);
      } finally {
        setLoading(false);
      }
    }
    carregarQualidade();
  }, [obraAtiva]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="flex flex-col items-center space-y-3">
          <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm text-zinc-400">Carregando governança de qualidade ({obraAtiva})...</p>
        </div>
      </div>
    );
  }

  const fvss = data?.fvss || [];
  const subcontratos = data?.subcontratos || [];
  const resumo = data?.resumo || {
    totalFvss: 8,
    aprovadas: 2,
    emInspecao: 1,
    pendentes: 5,
    taxaConformidade: 25,
    contratosBloqueados: 7,
  };

  const getStatusBadge = (status: FvsItem['status']) => {
    switch (status) {
      case 'APROVADO':
        return (
          <span className="px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" /> Aprovado (Liberado)
          </span>
        );
      case 'EM_INSPECAO':
        return (
          <span className="px-2.5 py-1 rounded-md text-xs font-bold bg-amber-500/15 text-amber-400 border border-amber-500/30 flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5" /> Em Inspeção (Canteiro)
          </span>
        );
      case 'BLOQUEADO':
      case 'PENDENTE':
      default:
        return (
          <span className="px-2.5 py-1 rounded-md text-xs font-bold bg-zinc-800 text-zinc-400 border border-zinc-700 flex items-center gap-1.5">
            <Lock className="w-3.5 h-3.5" /> Bloqueado / Aguardando
          </span>
        );
    }
  };

  const toggleExpand = (id: string) => {
    setExpandedFvs(expandedFvs === id ? null : id);
  };

  return (
    <div className="space-y-6">
      {/* CABEÇALHO */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-3">
            <ShieldCheck className="w-8 h-8 text-emerald-500" />
            Qualidade Executiva & FVS Bloqueantes
          </h1>
          <p className="text-zinc-400 mt-1">
            Governança de campo segundo PBQP-H Nível A, ISO 9001 e travas compulsórias de medições (SUB-01 a SUB-08).
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-semibold rounded-lg flex items-center gap-1.5">
            <FileBadge className="w-4 h-4" /> PBQP-H Homologado
          </span>
        </div>
      </div>

      {/* KPI CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Conformidade Global</p>
          <p className="text-2xl font-bold text-emerald-400 mt-2">{resumo.taxaConformidade}%</p>
          <p className="text-xs text-zinc-400 mt-1">{resumo.aprovadas} de {resumo.totalFvss} FVSs Aprovadas</p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Aprovadas (Verde)</p>
          <p className="text-2xl font-bold text-white mt-2">{resumo.aprovadas}</p>
          <p className="text-xs text-emerald-400 mt-1 flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" /> Liberam Medições
          </p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Em Inspeção (Amarelo)</p>
          <p className="text-2xl font-bold text-amber-400 mt-2">{resumo.emInspecao}</p>
          <p className="text-xs text-zinc-400 mt-1">Conferência com Trena / Laser</p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Contratos Bloqueados</p>
          <p className="text-2xl font-bold text-rose-400 mt-2">{resumo.contratosBloqueados}</p>
          <p className="text-xs text-rose-400/80 mt-1 flex items-center gap-1">
            <Lock className="w-3 h-3" /> Travas Anti-Avanço Indevido
          </p>
        </div>
      </div>

      {/* AVISO DO PRINCÍPIO DA LIBERAÇÃO EM CASCATA */}
      <div className="bg-blue-500/10 border border-blue-500/20 p-4 rounded-xl flex items-start space-x-3">
        <Info className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
        <div className="text-xs text-zinc-300 leading-relaxed">
          <span className="font-bold text-blue-300">Regra dos Portões de Qualidade:</span> O setor financeiro está tecnicamente proibido de autorizar notas fiscais ou medições quinzenais de subempreiteiros sem que a FVS correspondente esteja com status <span className="text-emerald-400 font-semibold">APROVADO</span> e retenção técnica de 5% discriminada.
        </div>
      </div>

      {/* GRADE DAS 8 FVSs NORMATIVAS */}
      <div>
        <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <span>Caderno Mestre das 8 FVSs Normativas</span>
          <span className="text-xs text-zinc-400 font-normal">(Clique para expandir checklist e tolerâncias)</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {fvss.map((fvs) => {
            const isExpanded = expandedFvs === fvs.id;
            return (
              <div
                key={fvs.id}
                className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden hover:border-zinc-700 transition-colors"
              >
                <div
                  onClick={() => toggleExpand(fvs.id)}
                  className="p-5 cursor-pointer flex items-start justify-between gap-4 select-none bg-zinc-950/40"
                >
                  <div className="space-y-1.5 flex-1 min-w-0">
                    <div className="flex items-center space-x-2">
                      <span className="px-2 py-0.5 bg-zinc-800 text-zinc-200 font-mono font-bold text-xs rounded">
                        {fvs.codigo}
                      </span>
                      <span className="text-xs text-zinc-400 font-mono">{fvs.norma}</span>
                    </div>
                    <h3 className="text-sm font-semibold text-white truncate">{fvs.titulo}</h3>
                    <p className="text-xs text-zinc-400">
                      <span className="text-zinc-500">Bloqueia:</span> {fvs.contratoBloqueado}
                    </p>
                  </div>

                  <div className="flex flex-col items-end space-y-2">
                    {getStatusBadge(fvs.status)}
                    <button className="text-zinc-500 hover:text-zinc-300 transition-colors">
                      {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* DETALHAMENTO EXPANSÍVEL */}
                {isExpanded && (
                  <div className="p-5 border-t border-zinc-800 bg-zinc-950/70 space-y-4 text-xs">
                    <div>
                      <p className="font-bold text-zinc-300 uppercase tracking-wider mb-1">
                        Serviço Sucessor Condicionado:
                      </p>
                      <p className="text-zinc-300 bg-zinc-900 p-2.5 rounded-lg border border-zinc-800">
                        {fvs.servicoLiberado}
                      </p>
                    </div>

                    <div>
                      <p className="font-bold text-amber-400 uppercase tracking-wider mb-1">
                        Tolerâncias Normativas Críticas:
                      </p>
                      <p className="text-zinc-300 bg-amber-500/10 border border-amber-500/20 p-2.5 rounded-lg">
                        {fvs.toleranciaCritica}
                      </p>
                    </div>

                    <div>
                      <p className="font-bold text-zinc-300 uppercase tracking-wider mb-2">
                        Checklist Mínimo Obrigatório:
                      </p>
                      <ul className="space-y-1.5">
                        {fvs.checklist.map((item, idx) => (
                          <li key={idx} className="flex items-start text-zinc-400">
                            <span className="w-4 h-4 rounded-full bg-zinc-800 text-zinc-300 flex items-center justify-center text-[10px] font-bold mr-2 flex-shrink-0 mt-0.5">
                              {idx + 1}
                            </span>
                            <span>{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {fvs.dataUltimaInspecao && (
                      <div className="pt-2 border-t border-zinc-800 flex justify-between items-center text-[11px] text-zinc-400">
                        <span>Última Inspeção: {fvs.dataUltimaInspecao}</span>
                        <span>Resp: {fvs.responsavel}</span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* MATRIZ DE TRAVAS CONTRATUAIS DOS SUBCONTRATOS (SUB-01 a SUB-08) */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden">
        <div className="p-4 bg-zinc-950/60 border-b border-zinc-800 flex justify-between items-center">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <Lock className="w-4 h-4 text-amber-400" />
            Matriz de Governança dos Subcontratos & Liberação Financeira
          </h3>
          <span className="text-xs text-zinc-400">8 Pacotes Homologados</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-zinc-950/40 text-xs uppercase font-bold text-zinc-400 border-b border-zinc-800">
              <tr>
                <th className="py-3 px-4">Contrato</th>
                <th className="py-3 px-4">Disciplina / Escopo</th>
                <th className="py-3 px-4">FVSs Condicionantes</th>
                <th className="py-3 px-4">Status Liberação</th>
                <th className="py-3 px-4 text-right">Retenção Técnica</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/60 text-xs">
              {subcontratos.map((sub) => (
                <tr key={sub.codigo} className="hover:bg-zinc-800/30 transition-colors">
                  <td className="py-3.5 px-4 font-mono font-bold text-blue-400">{sub.codigo}</td>
                  <td className="py-3.5 px-4 font-medium text-white">{sub.nome}</td>
                  <td className="py-3.5 px-4 text-zinc-300 font-mono text-[11px]">{sub.fvsCondicionante}</td>
                  <td className="py-3.5 px-4">
                    {sub.statusMedicao === 'LIBERADO' ? (
                      <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center gap-1 w-fit">
                        <Unlock className="w-3 h-3" /> Liberado p/ Medir
                      </span>
                    ) : sub.statusMedicao === 'RETENCAO_QUALIDADE' ? (
                      <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30 flex items-center gap-1 w-fit">
                        <Clock className="w-3 h-3" /> Parcial (Aguardando FVS-03)
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30 flex items-center gap-1 w-fit">
                        <Lock className="w-3 h-3" /> Bloqueado (FVS Pendente)
                      </span>
                    )}
                  </td>
                  <td className="py-3.5 px-4 text-right font-mono font-bold text-zinc-300">
                    {sub.retencaoTecnicaPercent.toFixed(1)}%
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
