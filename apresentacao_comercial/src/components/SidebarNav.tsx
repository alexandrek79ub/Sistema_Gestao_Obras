"use client";

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Wallet,
  CalendarDays,
  FileText,
  ShieldCheck,
  TrendingUp,
  HardHat,
  Award,
  Smartphone,
  ChevronRight
} from 'lucide-react';

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
}

interface NavSection {
  title: string;
  items: NavItem[];
}

const navSections: NavSection[] = [
  {
    title: 'Engenharia & Custos',
    items: [
      { name: 'Painel EVM (Curva S)', href: '/dashboard', icon: LayoutDashboard },
      { name: 'Orçamento Base', href: '/dashboard/orcamento', icon: Wallet },
      { name: 'Cronograma & Gantt', href: '/dashboard/cronograma', icon: CalendarDays },
    ],
  },
  {
    title: 'Canteiro & Produção',
    items: [
      { name: 'Medições & RDO Diário', href: '/dashboard/rdo', icon: FileText },
      { name: 'Qualidade & FVS', href: '/dashboard/qualidade', icon: ShieldCheck, badge: 'Travas' },
    ],
  },
  {
    title: 'Gestão & Suporte',
    items: [
      { name: 'Caixa & Suprimentos', href: '/dashboard/financeiro', icon: TrendingUp },
      { name: 'Segurança & SST', href: '/dashboard/sst', icon: HardHat },
      { name: 'DataBook & Closeout', href: '/dashboard/databook', icon: Award },
    ],
  },
];

export default function SidebarNav() {
  const pathname = usePathname();

  const isActive = (href: string) => {
    if (href === '/dashboard') {
      return pathname === '/dashboard';
    }
    return pathname.startsWith(href);
  };

  return (
    <div className="flex-1 flex flex-col justify-between overflow-y-auto px-4 py-2 space-y-6">
      <div className="space-y-6">
        {navSections.map((section) => (
          <div key={section.title}>
            <p className="text-[11px] font-bold text-zinc-400 uppercase tracking-wider mb-2 px-2">
              {section.title}
            </p>
            <nav className="space-y-1">
              {section.items.map((item) => {
                const active = isActive(item.href);
                const Icon = item.icon;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium transition-all group ${
                      active
                        ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30 shadow-sm'
                        : 'text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/60'
                    }`}
                  >
                    <div className="flex items-center min-w-0">
                      <Icon
                        className={`w-4 h-4 mr-3 flex-shrink-0 transition-colors ${
                          active ? 'text-blue-400' : 'text-zinc-500 group-hover:text-zinc-300'
                        }`}
                      />
                      <span className="truncate">{item.name}</span>
                    </div>
                    {item.badge ? (
                      <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30">
                        {item.badge}
                      </span>
                    ) : (
                      active && <ChevronRight className="w-3.5 h-3.5 text-blue-400 opacity-80" />
                    )}
                  </Link>
                );
              })}
            </nav>
          </div>
        ))}
      </div>

      {/* ATALHO COLETA MOBILE 4.0 */}
      <div className="pt-2 border-t border-zinc-800/80">
        <Link
          href="/campo"
          target="_blank"
          className="flex items-center justify-between p-3 rounded-xl bg-gradient-to-r from-emerald-500/10 to-teal-500/10 border border-emerald-500/30 text-emerald-400 hover:border-emerald-500/60 hover:from-emerald-500/20 hover:to-teal-500/20 transition-all shadow-sm group"
        >
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/20 flex items-center justify-center text-emerald-400 group-hover:scale-105 transition-transform">
              <Smartphone className="w-4 h-4" />
            </div>
            <div>
              <p className="text-xs font-semibold text-zinc-200">App Campo Mobile</p>
              <p className="text-[10px] text-emerald-400/80 font-medium">Coleta 4.0 (RDO & FVS)</p>
            </div>
          </div>
          <span className="text-[10px] font-bold bg-emerald-500/20 text-emerald-300 px-1.5 py-0.5 rounded">
            PWA
          </span>
        </Link>
      </div>
    </div>
  );
}
