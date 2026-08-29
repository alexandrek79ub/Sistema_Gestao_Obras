import { FileText, Users, CloudRain, Clock, CheckCircle2, ShieldAlert } from 'lucide-react';

export default function RdoPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white tracking-tight">Medições e RDO</h1>
        <p className="text-zinc-400 mt-1">Apontamento de Efetivo e Verificação de Serviços Diários.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* RDO MOCKUP */}
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden flex flex-col">
          <div className="bg-zinc-950/50 p-4 border-b border-zinc-800 flex justify-between items-center">
            <h3 className="text-lg font-semibold text-white flex items-center">
              <FileText className="w-5 h-5 mr-2 text-blue-500" />
              Relatório Diário de Obra (RDO)
            </h3>
            <span className="px-2 py-1 bg-zinc-800 text-zinc-300 text-xs rounded-md">29/08/2026</span>
          </div>
          
          <div className="p-6 space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-zinc-950/50 border border-zinc-800 p-4 rounded-lg flex items-center">
                <CloudRain className="w-8 h-8 text-blue-400 mr-4" />
                <div>
                  <p className="text-xs text-zinc-500 uppercase font-bold">Clima</p>
                  <p className="text-zinc-200 font-medium">Chuva Forte (Tarde)</p>
                </div>
              </div>
              <div className="bg-zinc-950/50 border border-zinc-800 p-4 rounded-lg flex items-center">
                <Users className="w-8 h-8 text-emerald-400 mr-4" />
                <div>
                  <p className="text-xs text-zinc-500 uppercase font-bold">Efetivo Total</p>
                  <p className="text-zinc-200 font-medium">12 Funcionários</p>
                </div>
              </div>
            </div>

            <div>
              <h4 className="text-sm font-semibold text-zinc-300 mb-3 uppercase tracking-wider">Mão de Obra e Atividades</h4>
              <div className="space-y-3">
                <div className="flex justify-between items-center bg-zinc-800/30 p-3 rounded-md border border-zinc-800/50">
                  <div>
                    <p className="text-zinc-200 text-sm font-medium">Empreiteiro João (Estrutura)</p>
                    <p className="text-zinc-500 text-xs">Montagem de Fôrmas no Pav. 02</p>
                  </div>
                  <div className="text-right">
                    <span className="text-zinc-300 text-sm">4 Oficiais, 2 Ajud.</span>
                    <p className="text-emerald-400 text-xs flex items-center justify-end mt-1"><CheckCircle2 className="w-3 h-3 mr-1" /> Ritmo OK</p>
                  </div>
                </div>
                
                <div className="flex justify-between items-center bg-amber-500/10 p-3 rounded-md border border-amber-500/20">
                  <div>
                    <p className="text-amber-400 text-sm font-medium">Empreiteiro Silva (Alvenaria)</p>
                    <p className="text-zinc-500 text-xs">Elevação no Pav. 01</p>
                  </div>
                  <div className="text-right">
                    <span className="text-zinc-300 text-sm">2 Oficiais, 1 Ajud.</span>
                    <p className="text-amber-500 text-xs flex items-center justify-end mt-1"><ShieldAlert className="w-3 h-3 mr-1" /> Atraso Notificado</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* FVS E MEDIÇÕES MOCKUP */}
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden flex flex-col">
          <div className="bg-zinc-950/50 p-4 border-b border-zinc-800 flex justify-between items-center">
            <h3 className="text-lg font-semibold text-white flex items-center">
              <CheckCircle2 className="w-5 h-5 mr-2 text-emerald-500" />
              Liberação FVS (Regra da Trena)
            </h3>
            <span className="px-2 py-1 bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs rounded-md">Pronto para Medição</span>
          </div>

          <div className="p-6">
            <div className="space-y-6">
              <div className="pb-4 border-b border-zinc-800/50">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="text-sm font-medium text-white">FVS 01 - Alvenaria de Vedação (Pavimento 01)</h4>
                  <span className="text-xs bg-zinc-800 text-zinc-400 px-2 py-1 rounded">Resp: Silva</span>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-xs">
                    <span className="text-zinc-400">Prumo e Esquadro verificado?</span>
                    <span className="text-emerald-400 font-medium">Sim (Erro &lt; 5mm)</span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span className="text-zinc-400">Amarração e Encunhamento?</span>
                    <span className="text-emerald-400 font-medium">Sim (Espuma expansiva PU)</span>
                  </div>
                  <div className="flex justify-between text-xs bg-blue-500/10 p-2 rounded border border-blue-500/20 mt-2">
                    <span className="text-blue-400 font-bold uppercase">Volume Físico Aprovado</span>
                    <span className="text-white font-mono font-bold">120 m²</span>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-r from-zinc-950 to-zinc-900 border border-zinc-800 rounded-lg p-5">
                <h4 className="text-sm font-bold text-white mb-4">Gatilho de Pagamento Mensal</h4>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-zinc-400">Empreiteiro Silva (Alvenaria)</span>
                  <span className="text-zinc-300">Total Produzido: 120 m²</span>
                </div>
                <div className="flex justify-between text-sm mb-4">
                  <span className="text-zinc-400">Valor Acordado em Contrato</span>
                  <span className="text-zinc-300">R$ 28,00 / m²</span>
                </div>
                <div className="border-t border-zinc-800 pt-3 flex justify-between items-center">
                  <span className="text-zinc-300 font-medium uppercase text-xs">Total Liberado para Faturamento</span>
                  <span className="text-xl font-bold text-emerald-400">R$ 3.360,00</span>
                </div>
                <button className="w-full mt-4 bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-2 rounded transition-colors text-sm">
                  Aprovar Medição e Notificar Financeiro
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
