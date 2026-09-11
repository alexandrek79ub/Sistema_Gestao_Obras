"use client";

import React, { useEffect, useState } from 'react';
import { useObra } from '@/context/ObraContext';
import {
  Award,
  FolderCheck,
  FileCheck2,
  ShieldCheck,
  CheckCircle2,
  Clock,
  AlertCircle,
  FileText,
  Building,
  Key,
  ChevronRight
} from 'lucide-react';

interface ArquivoItem {
  nome: string;
  status: 'VALIDADO' | 'MINUTA' | 'PENDENTE';
  tipo: string;
}

interface PastaDataBook {
  numero: string;
  nome: string;
  descricao: string;
  totalDocumentos: number;
  documentosConcluidos: number;
  status: 'CONCLUIDO' | 'EM_ANDAMENTO' | 'PENDENTE';
  arquivos: ArquivoItem[];
}

interface GarantiaItem {
  subsistema: string;
  componente: string;
  garantiaLegal: string;
  garantiaRecomendada: string;
  manutencaoPreventiva: string;
}

interface DataBookResponse {
  success: boolean;
  obra: string;
  kpis: {
    totalPastas: number;
    pastasConcluidas: number;
    totalDocumentos: number;
    documentosValidados: number;
    progressoCloseout: number;
    statusTrp: string;
    statusTrd: string;
  };
  pastas: PastaDataBook[];
  garantiasNbr15575: GarantiaItem[];
}

export default function DataBookPage() {
  const { obraAtiva } = useObra();
  const [data, setData] = useState<DataBookResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'PASTAS' | 'GARANTIAS' | 'CLOSEOUT'>('PASTAS');
  const [selectedFolder, setSelectedFolder] = useState<string>('01');

  useEffect(() => {
    async function carregarDataBook() {
      setLoading(true);
      try {
        const res = await fetch(`/api/databook?obra=${encodeURIComponent(obraAtiva)}`);
        const json: DataBookResponse = await res.json();
        setData(json);
      } catch (err) {
        console.error('Erro ao carregar databook:', err);
      } finally {
        setLoading(false);
      }
    }
    carregarDataBook();
  }, [obraAtiva]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="flex flex-col items-center space-y-3">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm text-zinc-400">Carregando acervo do DataBook ({obraAtiva})...</p>
        </div>
      </div>
    );
  }

  const kpis = data?.kpis || {
    totalPastas: 5,
    pastasConcluidas: 1,
    totalDocumentos: 17,
    documentosValidados: 9,
    progressoCloseout: 53,
    statusTrp: 'Em Elaboração (D-0)',
    statusTrd: 'Condicionado ao DataBook 100%',
  };

  const pastas = data?.pastas || [];
  const garantias = data?.garantiasNbr15575 || [];
  const activePasta = pastas.find((p) => p.numero === selectedFolder) || pastas[0];

  return (
    <div className="space-y-6">
      {/* CABEÇALHO */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-3">
            <Award className="w-8 h-8 text-indigo-400" />
            DataBook, As-Built & Closeout NBR 15575
          </h1>
          <p className="text-zinc-400 mt-1">
            Acervo documental permanente, projetos as-built, laudos de ensaios e termos de recebimento (TRP/TRD).
          </p>
        </div>

        {/* NAVEGAÇÃO DE ABAS */}
        <div className="flex bg-zinc-900 border border-zinc-800 p-1 rounded-xl">
          <button
            onClick={() => setActiveTab('PASTAS')}
            className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'PASTAS' ? 'bg-indigo-600 text-white shadow' : 'text-zinc-400 hover:text-white'
            }`}
          >
            As 5 Pastas do Acervo
          </button>
          <button
            onClick={() => setActiveTab('GARANTIAS')}
            className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'GARANTIAS' ? 'bg-indigo-600 text-white shadow' : 'text-zinc-400 hover:text-white'
            }`}
          >
            Garantias NBR 15575
          </button>
          <button
            onClick={() => setActiveTab('CLOSEOUT')}
            className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'CLOSEOUT' ? 'bg-indigo-600 text-white shadow' : 'text-zinc-400 hover:text-white'
            }`}
          >
            Roteiro Closeout
          </button>
        </div>
      </div>

      {/* KPI CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Progresso Closeout</p>
          <div className="flex items-baseline space-x-2 mt-2">
            <p className="text-2xl font-bold text-indigo-400">{kpis.progressoCloseout}%</p>
            <span className="text-xs text-zinc-400">compilado</span>
          </div>
          <div className="w-full bg-zinc-800 h-1.5 rounded-full mt-2 overflow-hidden">
            <div
              className="bg-indigo-500 h-1.5 rounded-full transition-all"
              style={{ width: `${kpis.progressoCloseout}%` }}
            ></div>
          </div>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Pastas Concluídas</p>
          <p className="text-2xl font-bold text-white mt-2">
            {kpis.pastasConcluidas} <span className="text-sm font-normal text-zinc-500">de {kpis.totalPastas}</span>
          </p>
          <p className="text-xs text-emerald-400 mt-1 flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" /> Pasta 03 100% Homologada
          </p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Documentos Validados</p>
          <p className="text-2xl font-bold text-white mt-2">
            {kpis.documentosValidados} <span className="text-sm font-normal text-zinc-500">de {kpis.totalDocumentos}</span>
          </p>
          <p className="text-xs text-zinc-400 mt-1">Laudos, As-Built, Manuais</p>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 p-4 rounded-xl">
          <p className="text-xs text-zinc-400 uppercase font-bold tracking-wider">Status Recebimento</p>
          <p className="text-lg font-bold text-amber-400 mt-2 truncate">{kpis.statusTrp}</p>
          <p className="text-xs text-zinc-400 mt-1">TRD libera caução de R$ 83k</p>
        </div>
      </div>

      {/* CONTEÚDO DAS ABAS */}
      {activeTab === 'PASTAS' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* COLUNA ESQUERDA: LISTA DAS 5 PASTAS */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-2">
              Pastas Canônicas de Entrega
            </h3>
            {pastas.map((pasta) => {
              const isSelected = selectedFolder === pasta.numero;
              return (
                <div
                  key={pasta.numero}
                  onClick={() => setSelectedFolder(pasta.numero)}
                  className={`p-4 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-indigo-600/15 border-indigo-500/50 shadow-sm'
                      : 'bg-zinc-900 border-zinc-800 hover:border-zinc-700'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3 min-w-0">
                      <span
                        className={`w-7 h-7 rounded-lg flex items-center justify-center font-mono text-xs font-bold ${
                          isSelected ? 'bg-indigo-500 text-white' : 'bg-zinc-800 text-zinc-300'
                        }`}
                      >
                        {pasta.numero}
                      </span>
                      <p className="text-sm font-semibold text-white truncate">{pasta.nome}</p>
                    </div>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                        pasta.status === 'CONCLUIDO'
                          ? 'bg-emerald-500/20 text-emerald-400'
                          : 'bg-amber-500/20 text-amber-400'
                      }`}
                    >
                      {pasta.status === 'CONCLUIDO' ? '100%' : `${pasta.documentosConcluidos}/${pasta.totalDocumentos}`}
                    </span>
                  </div>
                  <p className="text-xs text-zinc-400 mt-2 line-clamp-2">{pasta.descricao}</p>
                </div>
              );
            })}
          </div>

          {/* COLUNA DIREITA: DOCUMENTOS DA PASTA SELECIONADA */}
          <div className="lg:col-span-2 space-y-4">
            {activePasta && (
              <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden">
                <div className="p-5 bg-zinc-950/60 border-b border-zinc-800 flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <FolderCheck className="w-5 h-5 text-indigo-400" />
                    <div>
                      <h3 className="text-base font-semibold text-white">
                        Pasta {activePasta.numero} — {activePasta.nome}
                      </h3>
                      <p className="text-xs text-zinc-400 mt-0.5">{activePasta.descricao}</p>
                    </div>
                  </div>
                  <span className="text-xs bg-zinc-800 text-zinc-300 px-2.5 py-1 rounded">
                    {activePasta.arquivos.length} arquivos
                  </span>
                </div>

                <div className="p-5 space-y-3">
                  {activePasta.arquivos.map((arq, idx) => (
                    <div
                      key={idx}
                      className="flex items-center justify-between p-3.5 bg-zinc-950/40 rounded-lg border border-zinc-800/80 hover:border-zinc-700 transition-colors"
                    >
                      <div className="flex items-center space-x-3 min-w-0">
                        <FileText className="w-4 h-4 text-zinc-400 flex-shrink-0" />
                        <div className="min-w-0">
                          <p className="text-sm font-medium text-zinc-200 truncate">{arq.nome}</p>
                          <p className="text-[11px] text-zinc-500">{arq.tipo}</p>
                        </div>
                      </div>

                      <div>
                        {arq.status === 'VALIDADO' ? (
                          <span className="px-2.5 py-1 rounded text-[11px] font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 flex items-center gap-1">
                            <CheckCircle2 className="w-3 h-3" /> Validado
                          </span>
                        ) : arq.status === 'MINUTA' ? (
                          <span className="px-2.5 py-1 rounded text-[11px] font-bold bg-amber-500/15 text-amber-400 border border-amber-500/30 flex items-center gap-1">
                            <Clock className="w-3 h-3" /> Minuta em Edição
                          </span>
                        ) : (
                          <span className="px-2.5 py-1 rounded text-[11px] font-bold bg-zinc-800 text-zinc-400 flex items-center gap-1">
                            <AlertCircle className="w-3 h-3" /> Aguardando Emissão
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {activeTab === 'GARANTIAS' && (
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden">
          <div className="p-4 bg-zinc-950/60 border-b border-zinc-800 flex justify-between items-center">
            <h3 className="text-base font-semibold text-white flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              Matriz Oficial de Prazos de Garantia (Código Civil & NBR 15575)
            </h3>
            <span className="text-xs text-zinc-400">Garantia Técnica Homologada</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-zinc-950/40 text-xs uppercase font-bold text-zinc-400 border-b border-zinc-800">
                <tr>
                  <th className="py-3 px-4">Subsistema Construtivo</th>
                  <th className="py-3 px-4">Componente Específico</th>
                  <th className="py-3 px-4 text-center">Garantia Legal</th>
                  <th className="py-3 px-4 text-center">Garantia Praticada</th>
                  <th className="py-3 px-4">Manutenção Preventiva Obrigatória</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800/60 text-xs">
                {garantias.map((g, idx) => (
                  <tr key={idx} className="hover:bg-zinc-800/30 transition-colors">
                    <td className="py-3.5 px-4 font-semibold text-white">{g.subsistema}</td>
                    <td className="py-3.5 px-4 text-zinc-300">{g.componente}</td>
                    <td className="py-3.5 px-4 text-center font-bold text-blue-400">{g.garantiaLegal}</td>
                    <td className="py-3.5 px-4 text-center font-bold text-emerald-400">{g.garantiaRecomendada}</td>
                    <td className="py-3.5 px-4 text-zinc-400 leading-relaxed">{g.manutencaoPreventiva}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'CLOSEOUT' && (
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 space-y-6">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <Key className="w-5 h-5 text-amber-400" />
            Roteiro Cronológico de Entrega e Desmobilização (D-45 a D+15)
          </h3>

          <div className="space-y-4">
            <div className="flex items-start space-x-4 p-4 rounded-xl bg-zinc-950/50 border border-zinc-800">
              <span className="px-2.5 py-1 rounded bg-blue-500/20 text-blue-400 font-mono font-bold text-xs">
                D-45
              </span>
              <div>
                <h4 className="text-sm font-semibold text-white">Fase 1: Pré-Encerramento & Auditoria de Pendências</h4>
                <p className="text-xs text-zinc-400 mt-1 leading-relaxed">
                  Confronto físico dos 158 itens da EAP no canteiro, notificação de subempreiteiros para entrega dos desenhos marcados em vermelho para o As-Built e resgate de todos os laudos laboratoriais de concreto.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4 p-4 rounded-xl bg-zinc-950/50 border border-zinc-800">
              <span className="px-2.5 py-1 rounded bg-amber-500/20 text-amber-400 font-mono font-bold text-xs">
                D-15
              </span>
              <div>
                <h4 className="text-sm font-semibold text-white">Fase 2: Limpeza Fina e Desmobilização Logística</h4>
                <p className="text-xs text-zinc-400 mt-1 leading-relaxed">
                  Limpeza fina de entrega (esquadrias, vidros, pisos e louças desengorduradas), devolução de containers NR-18 e transição da energia provisória de canteiro para o padrão homologado pela concessionária.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4 p-4 rounded-xl bg-zinc-950/50 border border-zinc-800">
              <span className="px-2.5 py-1 rounded bg-indigo-500/20 text-indigo-400 font-mono font-bold text-xs">
                D-0
              </span>
              <div>
                <h4 className="text-sm font-semibold text-white">Fase 3: Vistoria Conjunta & Termo de Recebimento Provisório (TRP)</h4>
                <p className="text-xs text-zinc-400 mt-1 leading-relaxed">
                  Inspeção com fiscalização do cliente através do checklist de vistoria de entrega das chaves. Emissão da Punch List com prazo de 15 dias corridos para eventuais retoques pontuais.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4 p-4 rounded-xl bg-zinc-950/50 border border-zinc-800">
              <span className="px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-400 font-mono font-bold text-xs">
                D+15
              </span>
              <div>
                <h4 className="text-sm font-semibold text-white">Fase 4: Entrega Técnica Definitiva (TRD) & Liberação da Retenção</h4>
                <p className="text-xs text-zinc-400 mt-1 leading-relaxed">
                  Assinatura do Termo de Recebimento Definitivo, entrega das 5 pastas encadernadas do DataBook e liberação final do saldo de retenção contratual (5,0% = R$ 83.038,11).
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
