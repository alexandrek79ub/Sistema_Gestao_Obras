import LinhaDeBalanco from '@/components/LinhaDeBalanco';

export default function CronogramaPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white tracking-tight">Cronograma LOB</h1>
        <p className="text-zinc-400 mt-1">Gestão visual do fluxo de trabalho e ritmo de produção por andares.</p>
      </div>
      <LinhaDeBalanco />
    </div>
  );
}
