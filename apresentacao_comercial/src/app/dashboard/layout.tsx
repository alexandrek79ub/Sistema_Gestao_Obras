import Link from 'next/link';
import { LayoutDashboard, LineChart, FileText, CalendarDays, Wallet, Menu } from 'lucide-react';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-zinc-950 text-white overflow-hidden font-sans">
      
      {/* SIDEBAR */}
      <aside className="w-64 bg-zinc-900 border-r border-zinc-800 flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-zinc-800">
          <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white shadow-[0_0_15px_rgba(37,99,235,0.5)] mr-3">
            A11
          </div>
          <span className="font-bold text-lg tracking-tight">PMO Virtual</span>
        </div>
        
        <div className="p-4">
          <p className="text-xs font-semibold text-zinc-500 uppercase tracking-wider mb-4 px-2">Gestão 5D</p>
          <nav className="space-y-1">
            <Link href="/dashboard" className="flex items-center px-3 py-2.5 bg-blue-600/10 text-blue-400 hover:text-white hover:bg-blue-600/20 rounded-lg group transition-colors">
              <LayoutDashboard className="w-5 h-5 mr-3" />
              <span className="font-medium">Painel EVM</span>
            </Link>
            
            <Link href="/dashboard/orcamento" className="flex items-center px-3 py-2.5 text-zinc-400 hover:text-white hover:bg-zinc-800/50 rounded-lg group transition-colors">
              <Wallet className="w-5 h-5 mr-3" />
              <span className="font-medium">Orçamento Base</span>
            </Link>
            
            <Link href="/dashboard/cronograma" className="flex items-center px-3 py-2.5 text-zinc-400 hover:text-white hover:bg-zinc-800/50 rounded-lg group transition-colors">
              <CalendarDays className="w-5 h-5 mr-3" />
              <span className="font-medium">Linha de Balanço</span>
            </Link>

            <Link href="/dashboard/rdo" className="flex items-center px-3 py-2.5 text-zinc-400 hover:text-white hover:bg-zinc-800/50 rounded-lg group transition-colors">
              <FileText className="w-5 h-5 mr-3" />
              <span className="font-medium">Medições e RDO</span>
            </Link>
          </nav>
        </div>

        <div className="mt-auto p-4 border-t border-zinc-800">
          <div className="flex items-center">
            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-blue-500"></div>
            <div className="ml-3">
              <p className="text-sm font-medium text-white">Alexandre</p>
              <p className="text-xs text-zinc-500">Consultor PMO</p>
            </div>
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="flex-1 flex flex-col overflow-hidden bg-black/95">
        <header className="h-16 flex items-center justify-between px-8 border-b border-zinc-800 bg-zinc-900/50 backdrop-blur-md">
          <h2 className="text-xl font-semibold text-zinc-100">Projeto: Edifício Lumina</h2>
          <div className="flex items-center space-x-4">
            <span className="flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <span className="text-sm text-zinc-400">Sistema Ativo (Semana 03)</span>
          </div>
        </header>
        <div className="flex-1 overflow-y-auto p-8">
          {children}
        </div>
      </main>

    </div>
  );
}
