import TabelaOrcamento from '@/components/TabelaOrcamento';

export default function OrcamentoPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white tracking-tight">Orçamento Base</h1>
        <p className="text-zinc-400 mt-1">Gestão de custos, compras e acompanhamento de baseline.</p>
      </div>
      <TabelaOrcamento />
    </div>
  );
}
