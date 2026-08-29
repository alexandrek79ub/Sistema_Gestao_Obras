import React from 'react';

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-50 selection:bg-cyan-500/30 overflow-x-hidden font-sans">
      
      {/* BACKGROUND ELEMENTS */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-blue-600/20 rounded-full blur-[120px] animate-pulse"></div>
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-cyan-500/20 rounded-full blur-[120px] animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      {/* NAVBAR */}
      <nav className="fixed w-full z-50 top-0 border-b border-zinc-800/50 bg-zinc-950/70 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="text-2xl font-black tracking-tighter">
            A11 <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">Sistemas</span>
          </div>
          <div className="hidden md:flex space-x-8 text-sm font-medium text-zinc-400">
            <a href="#hero" className="hover:text-white transition-colors">Início</a>
            <a href="#features" className="hover:text-white transition-colors">O Sistema</a>
            <a href="#ai" className="hover:text-white transition-colors">Inteligência 4.0</a>
            <a href="#contact" className="px-5 py-2 rounded-full bg-white/10 hover:bg-white/20 text-white transition-all">
              Agendar Demo
            </a>
          </div>
        </div>
      </nav>

      {/* MAIN CONTENT */}
      <main className="relative z-10 pt-32">
        
        {/* HERO SECTION */}
        <section id="hero" className="relative w-full pt-32 pb-40 flex flex-col items-center text-center overflow-hidden border-b border-zinc-800/50">
          {/* Background Image with Dark Overlay */}
          <div 
            className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat opacity-40 mix-blend-luminosity"
            style={{ backgroundImage: "url('/hero-bg.png')" }}
          ></div>
          <div className="absolute inset-0 z-0 bg-gradient-to-b from-zinc-950/80 via-zinc-950/60 to-zinc-950"></div>
          
          <div className="relative z-10 max-w-7xl mx-auto px-6 flex flex-col items-center">
            <div className="inline-flex items-center space-x-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-semibold mb-8 backdrop-blur-sm">
              <span className="w-2 h-2 rounded-full bg-blue-400 animate-ping"></span>
              <span>O Fim da Gestão de Obras no Escuro</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-black tracking-tight mb-8 leading-tight max-w-4xl drop-shadow-2xl">
              Sua Construtora rodando como uma <br className="hidden md:block"/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-400 to-teal-400 drop-shadow-sm">
                Máquina de Precisão.
              </span>
            </h1>
            
            <p className="text-lg md:text-xl text-zinc-300 max-w-2xl mb-12 drop-shadow-md font-medium">
              Um Ecossistema completo gerido por Inteligência Artificial. Controle diário, automação de processos via WhatsApp e compliance técnico inegociável.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <button className="px-8 py-4 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-bold text-lg hover:scale-105 transition-transform shadow-[0_0_40px_-10px_rgba(59,130,246,0.6)] border border-blue-400/30 backdrop-blur-md">
                Descubra o Método
              </button>
            </div>
          </div>
        </section>

        {/* FEATURES SECTION (What it does) */}
        <section id="features" className="py-24 border-t border-zinc-800/50 bg-zinc-900/30">
          <div className="max-w-7xl mx-auto px-6">
            <div className="mb-16">
              <h2 className="text-3xl md:text-5xl font-bold mb-4">Engenharia de Custos <span className="text-cyan-400">Blindada</span></h2>
              <p className="text-zinc-400 text-lg max-w-2xl">Não vendemos apenas software. Implementamos regras duras que protegem a margem de lucro da sua obra todos os dias.</p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Card 1 */}
              <div className="p-8 rounded-2xl bg-zinc-900/50 border border-zinc-800 hover:border-blue-500/50 transition-colors group">
                <div className="w-12 h-12 rounded-lg bg-blue-500/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <svg className="w-6 h-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold mb-3">Biblioteca de 23 POPs</h3>
                <p className="text-zinc-400">Nenhuma parede é rebocada sem a FVS assinada. Processos de qualidade e segurança (NR-18/NR-35) amarrados dentro do sistema.</p>
              </div>

              {/* Card 2 */}
              <div className="p-8 rounded-2xl bg-zinc-900/50 border border-zinc-800 hover:border-cyan-500/50 transition-colors group">
                <div className="w-12 h-12 rounded-lg bg-cyan-500/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <svg className="w-6 h-6 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.121 14.121L19 19m-7-7l7-7m-7 7l-2.879 2.879M12 12L9.121 9.121m0 5.758a3 3 0 10-4.243 4.243 3 3 0 004.243-4.243zm0-5.758a3 3 0 10-4.243-4.243 3 3 0 004.243 4.243z" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold mb-3">A Regra da Trena</h3>
                <p className="text-zinc-400">Fim do avanço presumido. O Módulo Financeiro trava o fluxo de caixa. O empreiteiro só recebe o que foi verificado fisicamente no canteiro.</p>
              </div>

              {/* Card 3 */}
              <div className="p-8 rounded-2xl bg-zinc-900/50 border border-zinc-800 hover:border-teal-500/50 transition-colors group">
                <div className="w-12 h-12 rounded-lg bg-teal-500/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <svg className="w-6 h-6 text-teal-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold mb-3">Regra UCC (Compras)</h3>
                <p className="text-zinc-400">Se o projeto pede 13m de aço, o sistema só permite comprar 2 barras de 12m. Trava automática contra desperdício logístico.</p>
              </div>
            </div>
          </div>
        </section>

        {/* AI AND AUTOMATION SECTION */}
        <section id="ai" className="py-24">
          <div className="max-w-7xl mx-auto px-6 flex flex-col lg:flex-row items-center gap-16">
            
            <div className="w-full lg:w-1/2">
              <div className="inline-block px-4 py-2 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-sm font-semibold mb-6">
                O PMO Virtual
              </div>
              <h2 className="text-4xl md:text-5xl font-bold mb-6">O Cérebro da Operação.</h2>
              <p className="text-lg text-zinc-400 mb-8">
                Esqueça relatórios estáticos. Nossa IA cruza a Linha de Base (Orçamento) com o Cronograma e atua antes do problema acontecer.
              </p>
              
              <ul className="space-y-6">
                <li className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-zinc-800 flex items-center justify-center text-purple-400">1</div>
                  <div>
                    <h4 className="font-bold text-lg text-white">Análise EVM em Tempo Real</h4>
                    <p className="text-zinc-400">Leitura contínua dos índices de prazo (SPI) e custo (CPI) para previsibilidade cirúrgica.</p>
                  </div>
                </li>
                <li className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-zinc-800 flex items-center justify-center text-purple-400">2</div>
                  <div>
                    <h4 className="font-bold text-lg text-white">Planos de Ação Autônomos</h4>
                    <p className="text-zinc-400">Se o caminho crítico atrasar, a IA sugere soluções imediatas: <em>"Contrate +2 pedreiros (R$ 3k) para recuperar o prazo."</em></p>
                  </div>
                </li>
              </ul>
            </div>

            {/* Dashboard Mockup Visual */}
            <div className="w-full lg:w-1/2 relative">
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 to-blue-500/20 blur-3xl rounded-full"></div>
              <div className="relative rounded-2xl bg-zinc-900/80 border border-zinc-700/50 backdrop-blur-xl p-6 shadow-2xl">
                <div className="flex items-center gap-2 mb-6 border-b border-zinc-800 pb-4">
                  <div className="w-3 h-3 rounded-full bg-red-500"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                  <div className="w-3 h-3 rounded-full bg-green-500"></div>
                  <span className="text-xs font-mono text-zinc-500 ml-2">A11_EVM_DASHBOARD.exe</span>
                </div>
                
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="p-4 rounded-xl bg-black/40 border border-zinc-800">
                    <div className="text-zinc-500 text-xs font-bold uppercase mb-1">SPI (Prazo)</div>
                    <div className="text-3xl font-black text-green-400">1.04</div>
                  </div>
                  <div className="p-4 rounded-xl bg-black/40 border border-zinc-800">
                    <div className="text-zinc-500 text-xs font-bold uppercase mb-1">CPI (Custo)</div>
                    <div className="text-3xl font-black text-green-400">1.02</div>
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
                  <div className="flex items-center gap-2 mb-2">
                    <svg className="w-5 h-5 text-purple-400" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a8 8 0 100 16 8 8 0 000-16zM9 9V5a1 1 0 112 0v4h2a1 1 0 110 2h-3a1 1 0 01-1-1z"/></svg>
                    <span className="text-sm font-bold text-purple-300">Ação Sugerida pela IA</span>
                  </div>
                  <p className="text-sm text-zinc-300">
                    O ritmo de alvenaria caiu 15%. Autorize +1 ajudante para o Pav. 3 para manter a Baseline.
                  </p>
                  <button className="mt-3 w-full py-2 bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold rounded-lg transition-colors">
                    Aprovar Aditivo (+R$ 1.200)
                  </button>
                </div>
              </div>
            </div>

          </div>
        </section>

        {/* AUTOMATIONS (WEBHOOK) SECTION */}
        <section className="py-24 border-t border-zinc-800/50 bg-zinc-900/30">
          <div className="max-w-7xl mx-auto px-6 text-center">
            <h2 className="text-3xl md:text-5xl font-bold mb-6">Despacho Diário via <span className="text-green-400">WhatsApp</span></h2>
            <p className="text-zinc-400 text-lg max-w-3xl mx-auto mb-16">
              Nossa arquitetura proprietária (Next.js + Evolution API) acorda antes do seu Mestre de Obras.
            </p>

            <div className="flex flex-col md:flex-row items-center justify-center gap-8">
              
              <div className="bg-black/50 p-6 rounded-2xl border border-zinc-800 max-w-sm text-left relative">
                <div className="absolute -top-3 -right-3 bg-green-500 text-black text-xs font-bold px-3 py-1 rounded-full shadow-lg">06:00 AM</div>
                <div className="flex items-center gap-3 mb-4 border-b border-zinc-800 pb-3">
                  <div className="w-10 h-10 bg-zinc-800 rounded-full flex items-center justify-center">
                    <svg className="w-6 h-6 text-green-400" fill="currentColor" viewBox="0 0 24 24"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.006c.106.005.249-.04.39.298.144.347.491 1.2.534 1.287.043.087.072.188.014.304-.058.116-.087.188-.173.289l-.26.304c-.087.086-.177.18-.076.354.101.174.449.741.964 1.201.662.591 1.221.774 1.394.86s.274.072.376-.043c.101-.116.433-.506.549-.68.116-.173.231-.145.39-.087s1.011.477 1.184.564.289.13.332.202c.045.072.045.419-.1.824zm-3.423-14.416c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm.029 18.88c-1.161 0-2.305-.292-3.318-.844l-3.677.964.984-3.595c-.607-1.052-.927-2.246-.926-3.468.001-5.824 4.74-10.563 10.564-10.563 5.826 0 10.564 4.738 10.564 10.563 0 5.825-4.738 10.563-10.564 10.563z"/></svg>
                  </div>
                  <div>
                    <h5 className="font-bold text-white text-sm">Robô A11</h5>
                    <span className="text-xs text-zinc-500">Encarregado de Alvenaria</span>
                  </div>
                </div>
                <p className="text-sm text-zinc-300">
                  "Bom dia, João! Suas metas para hoje na Obra Lumina são:<br/><br/>
                  1. Levantar Alvenaria Pav. 3.<br/>
                  2. Chapiscar Muro dos fundos.<br/><br/>
                  Lembre-se de não iniciar o reboco sem a FVS assinada. Bom trabalho!"
                </p>
              </div>

              <div className="text-left max-w-sm">
                <h3 className="text-2xl font-bold mb-4">Sem Desculpas. Sem Atrasos.</h3>
                <p className="text-zinc-400 mb-6">
                  O sistema lê o Kanban da obra e dispara webhooks universais, enviando as ordens do dia direto pro celular dos gatos/empreiteiros. Ninguém fica parado esperando o mestre de obras chegar.
                </p>
                <div className="flex gap-2">
                  <span className="px-3 py-1 bg-zinc-800 rounded-md text-xs font-mono text-zinc-400">Next.js</span>
                  <span className="px-3 py-1 bg-zinc-800 rounded-md text-xs font-mono text-zinc-400">Evolution API</span>
                  <span className="px-3 py-1 bg-zinc-800 rounded-md text-xs font-mono text-zinc-400">Webhooks</span>
                </div>
              </div>

            </div>
          </div>
        </section>

        {/* CALL TO ACTION */}
        <section id="contact" className="py-32 relative overflow-hidden">
          <div className="absolute inset-0 bg-blue-600/10 blur-3xl"></div>
          <div className="max-w-4xl mx-auto px-6 text-center relative z-10">
            <h2 className="text-4xl md:text-6xl font-black mb-8">Pare de construir com feeling.<br/>Construa com <span className="text-blue-400">Dados.</span></h2>
            <p className="text-xl text-zinc-400 mb-10">
              Implementamos o Ecossistema A11 na sua construtora em 30 dias. Chega de pagar avanço presumido.
            </p>
            <button className="px-10 py-5 rounded-full bg-white text-black font-black text-lg hover:bg-zinc-200 transition-colors shadow-2xl">
              Agendar Reunião Técnica
            </button>
          </div>
        </section>
        
      </main>

      <footer className="border-t border-zinc-800/50 py-8 text-center text-zinc-600 text-sm">
        <p>&copy; 2026 A11 Sistemas. Engenharia 4.0 Híbrida.</p>
      </footer>
    </div>
  );
}
