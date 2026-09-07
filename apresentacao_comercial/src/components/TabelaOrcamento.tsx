"use client";

import { Wallet, ShieldAlert } from 'lucide-react';
import { useEffect, useState } from 'react';

export default function TabelaOrcamento() {
  const [orcamentoData, setOrcamentoData] = useState<any[]>([]);
  const [totalBaseline, setTotalBaseline] = useState<number>(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/orcamento')
      .then(res => res.json())
      .then(data => {
        if (data.itens) {
          // Formatando os dados da API
          const formatted = data.itens.map((item: any) => ({
            eap: item['COD_EAP'],
            desc: item['DESCRICAO_DO_SERVICO'],
            unid: item['UNIDADE'],
            qtd: item['QUANTIDADE_TOTAL'],
            preco: item['CUSTO_UNITARIO_BDI'],
            total: item['CUSTO_TOTAL'],
            resp: item['EMPREITEIRO_VINCULADO'],
            status: item['DESCRICAO_DO_SERVICO'].toLowerCase().includes('estaca') || item['DESCRICAO_DO_SERVICO'].toLowerCase().includes('aço') ? 'alert' : 'ok'
          })).filter((item: any) => item.eap && item.desc);
          
          setOrcamentoData(formatted);
          setTotalBaseline(data.totalBaseline);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error('Erro ao buscar orçamento', err);
        setLoading(false);
      });
  }, []);

  const formatCurrency = (val: number) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);
  };

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden mt-6">
      <div className="p-6 border-b border-zinc-800 flex justify-between items-center bg-zinc-950/50">
        <div>
          <h3 className="text-lg font-semibold text-white flex items-center">
            <Wallet className="w-5 h-5 mr-2 text-blue-500" />
            Orçamento Base (Linha de Base Travada)
          </h3>
          <p className="text-sm text-zinc-400 mt-1">Sincronizado com TEMPLATE_ORCAMENTO_BASE.csv</p>
        </div>
        <div className="px-3 py-1 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full text-xs font-semibold">
          Total Baseline: {loading ? 'Carregando...' : formatCurrency(totalBaseline)}
        </div>
      </div>
      
      <div className="overflow-x-auto">
        {loading ? (
          <div className="p-8 text-center text-zinc-500">Carregando dados do orçamento...</div>
        ) : (
          <table className="w-full text-left text-sm text-zinc-300">
            <thead className="bg-zinc-950/50 text-zinc-400 uppercase text-xs font-semibold">
              <tr>
                <th className="px-6 py-4">EAP</th>
                <th className="px-6 py-4">Descrição do Serviço</th>
                <th className="px-6 py-4 text-center">Unid.</th>
                <th className="px-6 py-4 text-right">Qtd Total</th>
                <th className="px-6 py-4 text-right">Custo Unit.</th>
                <th className="px-6 py-4 text-right">Custo Total</th>
                <th className="px-6 py-4">Empreiteiro (Recurso)</th>
                <th className="px-6 py-4">Status UCC</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/50">
              {orcamentoData.map((item, index) => (
                <tr key={index} className="hover:bg-zinc-800/20 transition-colors">
                  <td className="px-6 py-4 font-mono text-zinc-500">{item.eap}</td>
                  <td className="px-6 py-4 font-medium text-zinc-200">{item.desc}</td>
                  <td className="px-6 py-4 text-center">{item.unid}</td>
                  <td className="px-6 py-4 text-right">{item.qtd}</td>
                  <td className="px-6 py-4 text-right">{item.preco}</td>
                  <td className="px-6 py-4 text-right font-semibold text-blue-400">{item.total}</td>
                  <td className="px-6 py-4 text-zinc-400">{item.resp}</td>
                  <td className="px-6 py-4">
                    {item.status === 'alert' ? (
                      <span className="inline-flex items-center text-amber-400 text-xs font-medium">
                        <ShieldAlert className="w-4 h-4 mr-1" />
                        Trava UCC Ativa
                      </span>
                    ) : (
                      <span className="inline-flex items-center text-emerald-400 text-xs font-medium">
                        Conforme
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
