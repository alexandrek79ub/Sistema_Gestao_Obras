"use client";

import { Wallet, ShieldAlert } from 'lucide-react';

const orcamentoData = [
  { eap: "01.01.00", desc: "Tapume de chapa de madeira", unid: "m2", qtd: 150, preco: "R$ 85,00", total: "R$ 12.750,00", resp: "Equipe Própria", status: "ok" },
  { eap: "01.02.00", desc: "Locação da obra (Gabarito)", unid: "m2", qtd: 300, preco: "R$ 15,00", total: "R$ 4.500,00", resp: "Topografia Alfa", status: "ok" },
  { eap: "02.01.00", desc: "Estaca Escavada (diâm 30cm)", unid: "m", qtd: 400, preco: "R$ 65,00", total: "R$ 26.000,00", resp: "Fundações XYZ", status: "alert" },
  { eap: "02.02.00", desc: "Concreto Usinado fck 30 MPa", unid: "m3", qtd: 35, preco: "R$ 450,00", total: "R$ 15.750,00", resp: "Concreteira Beta", status: "ok" },
  { eap: "03.01.00", desc: "Fôrma de madeira (vigas/pilares)", unid: "m2", qtd: 850, preco: "R$ 75,00", total: "R$ 63.750,00", resp: "Empreiteiro João", status: "ok" },
  { eap: "03.02.00", desc: "Aço CA-50 (Armadura)", unid: "kg", qtd: 4500, preco: "R$ 12,50", total: "R$ 56.250,00", resp: "Gerdau", status: "alert" },
];

export default function TabelaOrcamento() {
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
          Total Baseline: R$ 179.000,00
        </div>
      </div>
      
      <div className="overflow-x-auto">
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
      </div>
    </div>
  );
}
