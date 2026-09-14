"use client";

import { Wallet, ShieldAlert } from 'lucide-react';
import { useDadosDaObra } from '@/hooks/useDadosDaObra';

interface ItemOrcamento { COD_EAP: string; DESCRICAO_DO_SERVICO: string; UNIDADE: string; QUANTIDADE_TOTAL: string; CUSTO_UNITARIO_BDI: string; CUSTO_TOTAL: string; EMPREITEIRO_VINCULADO: string; }
interface RespostaOrcamento { itens: ItemOrcamento[]; totalBaseline: number; }

const RESPOSTA_INICIAL: RespostaOrcamento = { itens: [], totalBaseline: 0 };

export default function TabelaOrcamento() {
  const { data, loading, error } = useDadosDaObra<RespostaOrcamento>('/api/orcamento', RESPOSTA_INICIAL);
  const formatCurrency = (valor: number) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden mt-6">
      <div className="p-6 border-b border-zinc-800 flex justify-between items-center bg-zinc-950/50">
        <div><h3 className="text-lg font-semibold text-white flex items-center"><Wallet className="w-5 h-5 mr-2 text-blue-500" />Orçamento Base (Linha de Base Travada)</h3><p className="text-sm text-zinc-400 mt-1">Dados da obra selecionada</p></div>
        <div className="px-3 py-1 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full text-xs font-semibold">Total Baseline: {loading ? 'Carregando...' : formatCurrency(data.totalBaseline)}</div>
      </div>
      <div className="overflow-x-auto">
        {loading && <div className="p-8 text-center text-zinc-500">Carregando dados do orçamento...</div>}
        {!loading && error && <div className="p-8 text-center text-red-400">{error}</div>}
        {!loading && !error && data.itens.length === 0 && <div className="p-8 text-center text-zinc-500">Sem dados para esta obra.</div>}
        {!loading && !error && data.itens.length > 0 && <table className="w-full text-left text-sm text-zinc-300"><thead className="bg-zinc-950/50 text-zinc-400 uppercase text-xs font-semibold"><tr><th className="px-6 py-4">EAP</th><th className="px-6 py-4">Descrição do Serviço</th><th className="px-6 py-4 text-center">Unid.</th><th className="px-6 py-4 text-right">Qtd Total</th><th className="px-6 py-4 text-right">Custo Unit.</th><th className="px-6 py-4 text-right">Custo Total</th><th className="px-6 py-4">Empreiteiro (Recurso)</th><th className="px-6 py-4">Status UCC</th></tr></thead><tbody className="divide-y divide-zinc-800/50">{data.itens.map((item, index) => {
          const alerta = /\b(estaca|aço)\b/i.test(item.DESCRICAO_DO_SERVICO);
          return <tr key={`${item.COD_EAP}-${index}`} className="hover:bg-zinc-800/20 transition-colors"><td className="px-6 py-4 font-mono text-zinc-500">{item.COD_EAP}</td><td className="px-6 py-4 font-medium text-zinc-200">{item.DESCRICAO_DO_SERVICO}</td><td className="px-6 py-4 text-center">{item.UNIDADE}</td><td className="px-6 py-4 text-right">{item.QUANTIDADE_TOTAL}</td><td className="px-6 py-4 text-right">{item.CUSTO_UNITARIO_BDI || '—'}</td><td className="px-6 py-4 text-right font-semibold text-blue-400">{item.CUSTO_TOTAL || '—'}</td><td className="px-6 py-4 text-zinc-400">{item.EMPREITEIRO_VINCULADO}</td><td className="px-6 py-4">{alerta ? <span className="inline-flex items-center text-amber-400 text-xs font-medium"><ShieldAlert className="w-4 h-4 mr-1" />Trava UCC Ativa</span> : <span className="inline-flex items-center text-emerald-400 text-xs font-medium">Conforme</span>}</td></tr>;
        })}</tbody></table>}
      </div>
    </div>
  );
}
