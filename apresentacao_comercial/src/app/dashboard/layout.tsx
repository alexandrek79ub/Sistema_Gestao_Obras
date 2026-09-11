import SidebarNav from '@/components/SidebarNav';
import { ObraProvider } from '@/context/ObraContext';
import ProjectSelector from '@/components/ProjectSelector';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <ObraProvider>
      <div className="flex h-screen bg-zinc-950 text-white overflow-hidden font-sans">
        
        {/* SIDEBAR */}
        <aside className="w-64 bg-zinc-900 border-r border-zinc-800 flex flex-col">
          <div className="h-16 flex items-center px-6 border-b border-zinc-800">
            <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white shadow-[0_0_15px_rgba(37,99,235,0.5)] mr-3">
              A11
            </div>
            <span className="font-bold text-lg tracking-tight">PMO Virtual</span>
          </div>
          
          <SidebarNav />

          <div className="p-4 border-t border-zinc-800 bg-zinc-900/60">
            <div className="flex items-center">
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 flex items-center justify-center text-xs font-bold text-white shadow-sm">
                PMO
              </div>
              <div className="ml-3 min-w-0">
                <p className="text-xs font-semibold text-white truncate">Eng. Alexandre</p>
                <p className="text-[10px] text-zinc-400 truncate">Consultoria PMO Virtual</p>
              </div>
            </div>
          </div>
        </aside>

        {/* MAIN CONTENT */}
        <main className="flex-1 flex flex-col overflow-hidden bg-black/95">
          <header className="h-16 flex items-center justify-between px-8 border-b border-zinc-800 bg-zinc-900/50 backdrop-blur-md">
            <ProjectSelector />
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
    </ObraProvider>
  );
}
