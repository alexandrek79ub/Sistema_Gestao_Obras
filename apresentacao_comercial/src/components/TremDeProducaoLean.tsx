"use client";

import React, { useState } from 'react';
import { 
  Train, 
  Layers, 
  Users, 
  Clock, 
  ShieldCheck, 
  Calendar, 
  Sparkles, 
  CheckCircle2, 
  ArrowRight,
  Info,
  Hammer,
  Truck,
  Building2,
  Paintbrush,
  Zap,
  Filter,
  Droplets,
  Wind,
  Wrench
} from 'lucide-react';

interface LoteCurtoPrazo {
  codLote: string;
  semana: string;
  diasSemana?: string;
  etapaZona?: string;
  vagaoEsteira?: string;
  setor: string;
  servico: string;
  metaFisica: string;
  duracaoDias: number;
  equipePrevista: string;
  headcount: number;
  equipamentos: string;
  materiaisUcc: string;
  rupMeta: string;
  status: string;
  rdoVinculado?: string;
}

interface TremProps {
  lotes: LoteCurtoPrazo[];
}

export default function TremDeProducaoLean({ lotes }: TremProps) {
  const [visaoModo, setVisaoModo] = useState<'equipes' | 'zonas'>('equipes');
  const [faseFiltro, setFaseFiltro] = useState<string>('FASE_1');
  const [loteSelecionado, setLoteSelecionado] = useState<LoteCurtoPrazo | null>(null);

  // Mapeamento dos 52 ciclos takt de toda a obra (Semanas 01 a 26 - 180 dias corridos)
  const ciclosTakt = [
    // FASE 1: FUNDAÇÕES E ESTRUTURA (SEMANAS 01 A 08 - CICLOS 01 A 16)
    { ciclo: 'Ciclo 01', semana: 'Semana 01', dias: 'Dias 01 a 03 (Seg-Qua)', datas: '01/10 a 03/10/26', mes: 'Mês 1', fase: 'FASE_1' },
    { ciclo: 'Ciclo 02', semana: 'Semana 01', dias: 'Dias 04 a 06 (Qui-Sáb)', datas: '05/10 a 07/10/26', mes: 'Mês 1', fase: 'FASE_1' },
    { ciclo: 'Ciclo 03', semana: 'Semana 02', dias: 'Dias 07 a 09 (Seg-Qua)', datas: '08/10 a 10/10/26', mes: 'Mês 1', fase: 'FASE_1' },
    { ciclo: 'Ciclo 04', semana: 'Semana 02', dias: 'Dias 10 a 12 (Qui-Sáb)', datas: '12/10 a 14/10/26', mes: 'Mês 1', fase: 'FASE_1' },
    { ciclo: 'Ciclo 05', semana: 'Semana 03', dias: 'Dias 13 a 15 (Seg-Qua)', datas: '15/10 a 17/10/26', mes: 'Mês 1', fase: 'FASE_1' },
    { ciclo: 'Ciclo 06', semana: 'Semana 03', dias: 'Dias 16 a 18 (Qui-Sáb)', datas: '19/10 a 21/10/26', mes: 'Mês 1', fase: 'FASE_1' },
    { ciclo: 'Ciclo 07', semana: 'Semana 04', dias: 'Dias 19 a 21 (Seg-Qua)', datas: '22/10 a 24/10/26', mes: 'Mês 1', fase: 'FASE_1' },
    { ciclo: 'Ciclo 08', semana: 'Semana 04', dias: 'Dias 22 a 24 (Qui-Sáb)', datas: '26/10 a 28/10/26', mes: 'Mês 1', fase: 'FASE_1' },
    
    { ciclo: 'Ciclo 09', semana: 'Semana 05', dias: 'Dias 25 a 27 (Seg-Qua)', datas: '29/10 a 31/10/26', mes: 'Mês 2', fase: 'FASE_1' },
    { ciclo: 'Ciclo 10', semana: 'Semana 05', dias: 'Dias 28 a 30 (Qui-Sáb)', datas: '02/11 a 04/11/26', mes: 'Mês 2', fase: 'FASE_1' },
    { ciclo: 'Ciclo 11', semana: 'Semana 06', dias: 'Dias 31 a 33 (Seg-Qua)', datas: '05/11 a 07/11/26', mes: 'Mês 2', fase: 'FASE_1' },
    { ciclo: 'Ciclo 12', semana: 'Semana 06', dias: 'Dias 34 a 36 (Qui-Sáb)', datas: '09/11 a 11/11/26', mes: 'Mês 2', fase: 'FASE_1' },
    { ciclo: 'Ciclo 13', semana: 'Semana 07', dias: 'Dias 37 a 39 (Seg-Qua)', datas: '12/11 a 14/11/26', mes: 'Mês 2', fase: 'FASE_1' },
    { ciclo: 'Ciclo 14', semana: 'Semana 07', dias: 'Dias 40 a 42 (Qui-Sáb)', datas: '16/11 a 18/11/26', mes: 'Mês 2', fase: 'FASE_1' },
    { ciclo: 'Ciclo 15', semana: 'Semana 08', dias: 'Dias 43 a 45 (Seg-Qua)', datas: '19/11 a 21/11/26', mes: 'Mês 2', fase: 'FASE_1' },
    { ciclo: 'Ciclo 16', semana: 'Semana 08', dias: 'Dias 46 a 48 (Qui-Sáb)', datas: '23/11 a 25/11/26', mes: 'Mês 2', fase: 'FASE_1' },

    // FASE 2: ALVENARIAS E COBERTURA METÁLICA (SEMANAS 09 A 12 - CICLOS 17 A 24)
    { ciclo: 'Ciclo 17', semana: 'Semana 09', dias: 'Dias 49 a 51 (Seg-Qua)', datas: '26/11 a 28/11/26', mes: 'Mês 3', fase: 'FASE_2' },
    { ciclo: 'Ciclo 18', semana: 'Semana 09', dias: 'Dias 52 a 54 (Qui-Sáb)', datas: '30/11 a 02/12/26', mes: 'Mês 3', fase: 'FASE_2' },
    { ciclo: 'Ciclo 19', semana: 'Semana 10', dias: 'Dias 55 a 57 (Seg-Qua)', datas: '03/12 a 05/12/26', mes: 'Mês 3', fase: 'FASE_2' },
    { ciclo: 'Ciclo 20', semana: 'Semana 10', dias: 'Dias 58 a 60 (Qui-Sáb)', datas: '07/12 a 09/12/26', mes: 'Mês 3', fase: 'FASE_2' },
    { ciclo: 'Ciclo 21', semana: 'Semana 11', dias: 'Dias 61 a 63 (Seg-Qua)', datas: '10/12 a 12/12/26', mes: 'Mês 3', fase: 'FASE_2' },
    { ciclo: 'Ciclo 22', semana: 'Semana 11', dias: 'Dias 64 a 66 (Qui-Sáb)', datas: '14/12 a 16/12/26', mes: 'Mês 3', fase: 'FASE_2' },
    { ciclo: 'Ciclo 23', semana: 'Semana 12', dias: 'Dias 67 a 69 (Seg-Qua)', datas: '17/12 a 19/12/26', mes: 'Mês 3', fase: 'FASE_2' },
    { ciclo: 'Ciclo 24', semana: 'Semana 12', dias: 'Dias 70 a 72 (Qui-Sáb)', datas: '21/12 a 23/12/26', mes: 'Mês 3', fase: 'FASE_2' },

    // FASE 3: REBOCO, IMPERMEABILIZAÇÃO E PORCELANATOS (SEMANAS 13 A 16 - CICLOS 25 A 32)
    { ciclo: 'Ciclo 25', semana: 'Semana 13', dias: 'Dias 73 a 75 (Seg-Qua)', datas: '24/12 a 26/12/26', mes: 'Mês 4', fase: 'FASE_3' },
    { ciclo: 'Ciclo 26', semana: 'Semana 13', dias: 'Dias 76 a 78 (Qui-Sáb)', datas: '28/12 a 30/12/26', mes: 'Mês 4', fase: 'FASE_3' },
    { ciclo: 'Ciclo 27', semana: 'Semana 14', dias: 'Dias 79 a 81 (Seg-Qua)', datas: '31/12 a 02/01/27', mes: 'Mês 4', fase: 'FASE_3' },
    { ciclo: 'Ciclo 28', semana: 'Semana 14', dias: 'Dias 82 a 84 (Qui-Sáb)', datas: '04/01 a 06/01/27', mes: 'Mês 4', fase: 'FASE_3' },
    { ciclo: 'Ciclo 29', semana: 'Semana 15', dias: 'Dias 85 a 87 (Seg-Qua)', datas: '07/01 a 09/01/27', mes: 'Mês 4', fase: 'FASE_3' },
    { ciclo: 'Ciclo 30', semana: 'Semana 15', dias: 'Dias 88 a 90 (Qui-Sáb)', datas: '11/01 a 13/01/27', mes: 'Mês 4', fase: 'FASE_3' },
    { ciclo: 'Ciclo 31', semana: 'Semana 16', dias: 'Dias 91 a 93 (Seg-Qua)', datas: '14/01 a 16/01/27', mes: 'Mês 4', fase: 'FASE_3' },
    { ciclo: 'Ciclo 32', semana: 'Semana 16', dias: 'Dias 94 a 96 (Qui-Sáb)', datas: '18/01 a 20/01/27', mes: 'Mês 4', fase: 'FASE_3' },

    // FASE 4: INSTALAÇÕES MEP, ESQUADRIAS E CLIMATIZAÇÃO HVAC (SEMANAS 17 A 20 - CICLOS 33 A 40)
    { ciclo: 'Ciclo 33', semana: 'Semana 17', dias: 'Dias 97 a 99 (Seg-Qua)', datas: '21/01 a 23/01/27', mes: 'Mês 5', fase: 'FASE_4' },
    { ciclo: 'Ciclo 34', semana: 'Semana 17', dias: 'Dias 100 a 102 (Qui-Sáb)', datas: '25/01 a 27/01/27', mes: 'Mês 5', fase: 'FASE_4' },
    { ciclo: 'Ciclo 35', semana: 'Semana 18', dias: 'Dias 103 a 105 (Seg-Qua)', datas: '28/01 a 30/01/27', mes: 'Mês 5', fase: 'FASE_4' },
    { ciclo: 'Ciclo 36', semana: 'Semana 18', dias: 'Dias 106 a 108 (Qui-Sáb)', datas: '01/02 a 03/02/27', mes: 'Mês 5', fase: 'FASE_4' },
    { ciclo: 'Ciclo 37', semana: 'Semana 19', dias: 'Dias 109 a 111 (Seg-Qua)', datas: '04/02 a 06/02/27', mes: 'Mês 5', fase: 'FASE_4' },
    { ciclo: 'Ciclo 38', semana: 'Semana 19', dias: 'Dias 112 a 114 (Qui-Sáb)', datas: '08/02 a 10/02/27', mes: 'Mês 5', fase: 'FASE_4' },
    { ciclo: 'Ciclo 39', semana: 'Semana 20', dias: 'Dias 115 a 117 (Seg-Qua)', datas: '11/02 a 13/02/27', mes: 'Mês 5', fase: 'FASE_4' },
    { ciclo: 'Ciclo 40', semana: 'Semana 20', dias: 'Dias 118 a 120 (Qui-Sáb)', datas: '15/02 a 17/02/27', mes: 'Mês 5', fase: 'FASE_4' },

    // FASE 5: PINTURA, COMISSIONAMENTO E HANDOVER TURNKEY (SEMANAS 21 A 26 - CICLOS 41 A 52)
    { ciclo: 'Ciclo 41', semana: 'Semana 21', dias: 'Dias 121 a 123 (Seg-Qua)', datas: '18/02 a 20/02/27', mes: 'Mês 6', fase: 'FASE_5' },
    { ciclo: 'Ciclo 42', semana: 'Semana 21', dias: 'Dias 124 a 126 (Qui-Sáb)', datas: '22/02 a 24/02/27', mes: 'Mês 6', fase: 'FASE_5' },
    { ciclo: 'Ciclo 43', semana: 'Semana 22', dias: 'Dias 127 a 129 (Seg-Qua)', datas: '25/02 a 27/02/27', mes: 'Mês 6', fase: 'FASE_5' },
    { ciclo: 'Ciclo 44', semana: 'Semana 22', dias: 'Dias 130 a 132 (Qui-Sáb)', datas: '01/03 a 03/03/27', mes: 'Mês 6', fase: 'FASE_5' },
    { ciclo: 'Ciclo 45', semana: 'Semana 23', dias: 'Dias 133 a 135 (Seg-Qua)', datas: '04/03 a 06/03/27', mes: 'Mês 6', fase: 'FASE_5' },
    { ciclo: 'Ciclo 46', semana: 'Semana 23', dias: 'Dias 136 a 138 (Qui-Sáb)', datas: '08/03 a 10/03/27', mes: 'Mês 6', fase: 'FASE_5' },
    { ciclo: 'Ciclo 47', semana: 'Semana 24', dias: 'Dias 139 a 141 (Seg-Qua)', datas: '11/03 a 13/03/27', mes: 'Mês 6', fase: 'FASE_5' },
    { ciclo: 'Ciclo 48', semana: 'Semana 24', dias: 'Dias 142 a 144 (Qui-Sáb)', datas: '15/03 a 17/03/27', mes: 'Mês 6', fase: 'FASE_5' },
    { ciclo: 'Ciclo 49', semana: 'Semana 25', dias: 'Dias 145 a 147 (Seg-Qua)', datas: '18/03 a 20/03/27', mes: 'Mês 6', fase: 'FASE_5' },
    { ciclo: 'Ciclo 50', semana: 'Semana 25', dias: 'Dias 148 a 150 (Qui-Sáb)', datas: '22/03 a 24/03/27', mes: 'Mês 6', fase: 'FASE_5' },
    { ciclo: 'Ciclo 51', semana: 'Semana 26', dias: 'Dias 151 a 153 (Seg-Qua)', datas: '25/03 a 27/03/27', mes: 'Mês 6', fase: 'FASE_5' },
    { ciclo: 'Ciclo 52', semana: 'Semana 26', dias: 'Dias 154 a 156 (Qui-Sáb)', datas: '29/03 a 31/03/27', mes: 'Mês 6', fase: 'FASE_5' },
  ];

  // Filtrar ciclos conforme seleção de fase
  const ciclosFiltrados = faseFiltro === 'TODAS' 
    ? ciclosTakt 
    : ciclosTakt.filter(c => c.fase === faseFiltro);

  // Lista Completa de Equipes Especializadas (Vagões de Especialidade Lean)
  const equipesLean = [
    {
      id: 'carpintaria',
      nome: 'Equipe de Carpintaria de Fôrmas',
      efetivo: '4 Carpinteiros Oficiais',
      cor: 'border-blue-500 bg-blue-950/40 text-blue-300',
      tagCor: 'bg-blue-500/20 text-blue-400 border-blue-500/40',
      icone: Hammer
    },
    {
      id: 'armacao',
      nome: 'Equipe de Ferragens & Armação',
      efetivo: '3 Armadores CA-50/60',
      cor: 'border-rose-500 bg-rose-950/40 text-rose-300',
      tagCor: 'bg-rose-500/20 text-rose-400 border-rose-500/40',
      icone: Zap
    },
    {
      id: 'concretagem',
      nome: 'Equipe de Concretagem & Desforma',
      efetivo: '2 Pedreiros + 5 Serventes',
      cor: 'border-emerald-500 bg-emerald-950/40 text-emerald-300',
      tagCor: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40',
      icone: Building2
    },
    {
      id: 'escavacao',
      nome: 'Equipe de Terraplenagem & Canteiro',
      efetivo: '1 Operador + 1 Topógrafo + 4 Serventes',
      cor: 'border-amber-500 bg-amber-950/40 text-amber-300',
      tagCor: 'bg-amber-500/20 text-amber-400 border-amber-500/40',
      icone: Truck
    },
    {
      id: 'alvenaria',
      nome: 'Equipe de Alvenarias & Reboco',
      efetivo: '5 Pedreiros + 5 Serventes (SUB-02)',
      cor: 'border-purple-500 bg-purple-950/40 text-purple-300',
      tagCor: 'bg-purple-500/20 text-purple-400 border-purple-500/40',
      icone: Building2
    },
    {
      id: 'cobertura',
      nome: 'Equipe de Cobertura & Esquadrias',
      efetivo: '3 Montadores + 2 Ajudantes',
      cor: 'border-cyan-500 bg-cyan-950/40 text-cyan-300',
      tagCor: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/40',
      icone: Sparkles
    },
    {
      id: 'instalacoes',
      nome: 'Equipe de Instalações MEP (Elétrica & Hidráulica)',
      efetivo: '2 Eletricistas + 2 Encanadores + 4 Serventes (SUB-03/04)',
      cor: 'border-orange-500 bg-orange-950/40 text-orange-300',
      tagCor: 'bg-orange-500/20 text-orange-400 border-orange-500/40',
      icone: Zap
    },
    {
      id: 'revestimentos',
      nome: 'Equipe de Revestimentos & Porcelanato',
      efetivo: '3 Ladrilhistas + 3 Ajudantes (SUB-05)',
      cor: 'border-indigo-500 bg-indigo-950/40 text-indigo-300',
      tagCor: 'bg-indigo-500/20 text-indigo-400 border-indigo-500/40',
      icone: Layers
    },
    {
      id: 'climatizacao',
      nome: 'Equipe de Climatização & VRF',
      efetivo: '2 Técnicos HVAC + 2 Ajudantes (SUB-08)',
      cor: 'border-sky-500 bg-sky-950/40 text-sky-300',
      tagCor: 'bg-sky-500/20 text-sky-400 border-sky-500/40',
      icone: Wind
    },
    {
      id: 'pintura',
      nome: 'Equipe de Pintura Acrílica & Acabamento',
      efetivo: '4 Pintores + 2 Ajudantes (SUB-06)',
      cor: 'border-teal-500 bg-teal-950/40 text-teal-300',
      tagCor: 'bg-teal-500/20 text-teal-400 border-teal-500/40',
      icone: Paintbrush
    }
  ];

  // Lista de Zonas Takt (Etapas Construtivas)
  const zonasTakt = [
    {
      id: 'Etapa 1',
      nome: 'Etapa 1 (Zona 1 — Recepção & Diretoria)',
      descricao: 'Sapatas S1-12 → Baldrames VB1-6 → Pilares P1-8 → Laje Z1',
      corBadge: 'bg-blue-500/20 text-blue-400 border-blue-500/40'
    },
    {
      id: 'Etapa 2',
      nome: 'Etapa 2 (Zona 2 — Salas Técnicas & CPD)',
      descricao: 'Sapatas S13-24 → Baldrames VB7-12 → Pilares P9-16 → Laje Z2',
      corBadge: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
    },
    {
      id: 'Etapa 3',
      nome: 'Etapa 3 (Zona 3 — Sanitários, Copa & Apoio)',
      descricao: 'Sapatas S25-32 → Baldrames VB13-19 → Pilares P17-24 → Laje Z3 Global',
      corBadge: 'bg-amber-500/20 text-amber-400 border-amber-500/40'
    }
  ];

  // Função auxiliar para encontrar lote da semana e ciclo (amarração determinística e por período)
  const encontrarLote = (cicloNome: string, semana: string, diasCiclo: string) => {
    // 1. Busca direta por código determinístico do lote (ex: Ciclo 01 -> LOTE-001)
    const cicloNum = parseInt(cicloNome.replace(/\D/g, ''), 10);
    const codFormatado = `LOTE-${String(cicloNum).padStart(3, '0')}`;
    const lotePorCod = lotes.find(l => l.codLote === codFormatado);
    if (lotePorCod) return lotePorCod;

    // 2. Busca de fallback por semana e intervalo de dias
    const isSegQua = diasCiclo.toLowerCase().includes('seg');
    return lotes.find(l => {
      const matchSemana = l.semana?.trim().toLowerCase() === semana?.trim().toLowerCase();
      const lDias = (l.diasSemana || '').toLowerCase();
      const matchDias = isSegQua 
        ? (lDias.includes('seg') || lDias.includes('01 a 03') || lDias.includes('07 a 09') || lDias.includes('13 a 15') || lDias.includes('19 a 21') || lDias.includes('25 a 27') || lDias.includes('31 a 33') || lDias.includes('37 a 39') || lDias.includes('43 a 45'))
        : (lDias.includes('qui') || lDias.includes('sáb') || lDias.includes('sab') || lDias.includes('04 a 06') || lDias.includes('10 a 12') || lDias.includes('16 a 18') || lDias.includes('22 a 24') || lDias.includes('28 a 30') || lDias.includes('34 a 36') || lDias.includes('40 a 42') || lDias.includes('46 a 48'));
      return matchSemana && matchDias;
    });
  };

  return (
    <div className="space-y-6">
      {/* HEADER DO TREM LEAN */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 pb-6 border-b border-zinc-800">
          <div>
            <div className="flex items-center gap-2.5">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-emerald-500 flex items-center justify-center text-white shadow-lg shadow-blue-500/20">
                <Train className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  Trem de Produção Contínua — Esteira Lean (Takt Time)
                  <span className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 px-2.5 py-0.5 rounded-full text-xs font-semibold">
                    Zero Ociosidade
                  </span>
                </h2>
                <p className="text-xs text-zinc-400 mt-0.5">
                  Visualização em formato de vagões sincronizados ao longo do tempo. As equipes transitam de zona em zona sem interrupções por cura.
                </p>
              </div>
            </div>
          </div>

          {/* CONTROLES: PERSPECTIVA E FILTRO DE FASE */}
          <div className="flex flex-wrap items-center gap-3">
            {/* TOGGLE DE VISÃO */}
            <div className="bg-zinc-950 p-1 rounded-xl border border-zinc-800 flex items-center">
              <button
                onClick={() => setVisaoModo('equipes')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                  visaoModo === 'equipes'
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'text-zinc-400 hover:text-white'
                }`}
              >
                <Users className="w-3.5 h-3.5" />
                Visão por Equipes (Rastreio de Ociosidade)
              </button>
              <button
                onClick={() => setVisaoModo('zonas')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                  visaoModo === 'zonas'
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'text-zinc-400 hover:text-white'
                }`}
              >
                <Layers className="w-3.5 h-3.5" />
                Visão por Zonas Takt (Etapas 1, 2 e 3)
              </button>
            </div>

            {/* FILTRO DE FASE */}
            <div className="flex items-center gap-2 bg-zinc-950 px-3 py-1.5 rounded-xl border border-zinc-800">
              <Filter className="w-3.5 h-3.5 text-zinc-400" />
              <span className="text-xs text-zinc-400 font-medium">Fase:</span>
              <select
                value={faseFiltro}
                onChange={(e) => setFaseFiltro(e.target.value)}
                className="bg-transparent text-xs text-white font-semibold focus:outline-none cursor-pointer"
              >
                <option value="FASE_1" className="bg-zinc-900 text-white">Fase 1: Fundações & Estrutura (Sem 01 a 08)</option>
                <option value="FASE_2" className="bg-zinc-900 text-white">Fase 2: Alvenarias & Cobertura (Sem 09 a 12)</option>
                <option value="FASE_3" className="bg-zinc-900 text-white">Fase 3: Reboco, Impermeabilização & Porcelanatos (Sem 13 a 16)</option>
                <option value="FASE_4" className="bg-zinc-900 text-white">Fase 4: Instalações MEP & Climatização HVAC (Sem 17 a 20)</option>
                <option value="FASE_5" className="bg-zinc-900 text-white">Fase 5: Pintura, Comissionamento & Handover (Sem 21 a 26)</option>
                <option value="TODAS" className="bg-zinc-900 text-white">Todas as 26 Semanas (Linha Completa — 52 Ciclos Takt)</option>
              </select>
            </div>
          </div>
        </div>

        {/* BANNER EXPLICATIVO DO FLUXO CONTÍNUO */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          <div className="bg-zinc-950/70 border border-zinc-800/80 rounded-xl p-3.5 flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0">
              <CheckCircle2 className="w-4 h-4" />
            </div>
            <div>
              <span className="text-xs font-bold text-white block">Equipes 100% Produtivas</span>
              <span className="text-[11px] text-zinc-400">Quando a Zona 1 está curando, a equipe já avança para a Zona 2.</span>
            </div>
          </div>

          <div className="bg-zinc-950/70 border border-zinc-800/80 rounded-xl p-3.5 flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center shrink-0">
              <Clock className="w-4 h-4" />
            </div>
            <div>
              <span className="text-xs font-bold text-white block">Takt Time = 3 Dias Úteis</span>
              <span className="text-[11px] text-zinc-400">Ciclos padronizados (Seg-Qua e Qui-Sáb) com datas de calendário reais.</span>
            </div>
          </div>

          <div className="bg-zinc-950/70 border border-zinc-800/80 rounded-xl p-3.5 flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-purple-500/20 text-purple-400 flex items-center justify-center shrink-0">
              <ShieldCheck className="w-4 h-4" />
            </div>
            <div>
              <span className="text-xs font-bold text-white block">Cura Sem Parada</span>
              <span className="text-[11px] text-zinc-400">O concreto ganha fck tecnológico sem deixar trabalhadores de braços cruzados.</span>
            </div>
          </div>
        </div>
      </div>

      {/* ÁREA DA ESTEIRA / MATRIZ DE TREM */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl overflow-hidden">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-500 animate-pulse"></span>
            {visaoModo === 'equipes' 
              ? 'Esteira Contínua por Equipe de Produção (Comprovação de Zero Ociosidade)'
              : 'Fluxo Sequencial por Zona Construtiva (Etapa 1, 2 e 3)'}
          </h3>
          <span className="text-xs text-zinc-400 font-mono">
            Mostrando {ciclosFiltrados.length} ciclos takt de 3 dias
          </span>
        </div>

        {/* CONTAINER COM SCROLL HORIZONTAL */}
        <div className="overflow-x-auto pb-4">
          <div className="min-w-max">
            {/* CABEÇALHO DO TEMPO (RÉGUA DE CICLOS, SEMANAS E DATAS) */}
            <div 
              className="grid gap-2 mb-3 sticky top-0 bg-zinc-900 z-10 pb-2 border-b border-zinc-800"
              style={{ gridTemplateColumns: `220px repeat(${ciclosFiltrados.length}, minmax(170px, 1fr))` }}
            >
              <div className="bg-zinc-950 p-3 rounded-xl border border-zinc-800 flex flex-col justify-center">
                <span className="text-xs font-bold text-zinc-300">
                  {visaoModo === 'equipes' ? 'EQUIPES / VAGÕES' : 'ZONAS DE TRABALHO'}
                </span>
                <span className="text-[10px] text-zinc-500">Mão de Obra / Frente</span>
              </div>

              {ciclosFiltrados.map((c, i) => {
                const loteCiclo = encontrarLote(c.ciclo, c.semana, c.dias);
                return (
                  <div key={i} className="bg-zinc-950 p-2.5 rounded-xl border border-zinc-800 text-center flex flex-col justify-between hover:border-zinc-700 transition-colors">
                    <div>
                      <span className="text-[11px] font-bold text-blue-400 block">{c.ciclo}</span>
                      <span className="text-[10px] text-zinc-300 font-semibold">{c.semana}</span>
                    </div>
                    <div className="mt-1 pt-1 border-t border-zinc-800/80">
                      <span className="text-[9px] text-amber-400 block font-mono font-medium">{c.dias.split('(')[1]?.replace(')', '') || c.dias}</span>
                      <span className="text-[9px] text-zinc-400 block font-mono font-bold mt-0.5">{c.datas}</span>
                    </div>
                    {/* INDICADOR VISUAL DO VAGÃO ATIVO NESTE CICLO */}
                    {loteCiclo && (
                      <div className="mt-1 pt-1 border-t border-zinc-800/60">
                        <span 
                          className="text-[8px] font-mono font-bold text-emerald-400 bg-emerald-950/60 px-1.5 py-0.5 rounded border border-emerald-800/50 block truncate" 
                          title={loteCiclo.vagaoEsteira || loteCiclo.servico}
                        >
                          {(loteCiclo.vagaoEsteira?.split(':')[1] || loteCiclo.vagaoEsteira || loteCiclo.codLote).trim()}
                        </span>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* CORPO: LINHAS POR EQUIPE (MODO EQUIPES) */}
            {visaoModo === 'equipes' && (
              <div className="space-y-3">
                {equipesLean.map((eq) => {
                  const Icone = eq.icone;
                  return (
                    <div 
                      key={eq.id} 
                      className="grid gap-2 items-stretch"
                      style={{ gridTemplateColumns: `220px repeat(${ciclosFiltrados.length}, minmax(170px, 1fr))` }}
                    >
                      {/* IDENTIFICADOR DA EQUIPE */}
                      <div className="bg-zinc-950 p-3.5 rounded-xl border border-zinc-800 flex flex-col justify-center">
                        <div className="flex items-center gap-2">
                          <Icone className="w-4 h-4 text-zinc-400 shrink-0" />
                          <span className="text-xs font-bold text-white leading-tight">{eq.nome}</span>
                        </div>
                        <span className="text-[10px] text-zinc-400 mt-1 font-mono">{eq.efetivo}</span>
                        <div className="flex items-center gap-1 mt-1.5">
                          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                          <span className="text-[9px] text-emerald-400 font-bold uppercase tracking-wider">Ativação Contínua</span>
                        </div>
                      </div>

                      {/* VAGÕES AO LONGO DOS CICLOS */}
                      {ciclosFiltrados.map((c, i) => {
                        const lote = encontrarLote(c.ciclo, c.semana, c.dias);
                        
                        // Lógica precisa de alocação da equipe no lote deste ciclo
                        let estaNesteLote = false;
                        let etapaTexto = lote?.etapaZona || 'Geral';

                        if (lote) {
                          const eqLower = (lote.equipePrevista || '').toLowerCase();
                          const servLower = (lote.servico || '').toLowerCase();
                          const vagaoLower = (lote.vagaoEsteira || '').toLowerCase();

                          if (eq.id === 'carpintaria') {
                            if (eqLower.includes('carpinteiro') || vagaoLower.includes('carpintaria') || servLower.includes('fôrma') || servLower.includes('forma') || servLower.includes('cimbramento')) {
                              estaNesteLote = true;
                            }
                          } else if (eq.id === 'armacao') {
                            if (eqLower.includes('armador') || vagaoLower.includes('armação') || vagaoLower.includes('armacao') || servLower.includes('armação') || servLower.includes('armacao') || servLower.includes('aço') || servLower.includes('ferrag')) {
                              estaNesteLote = true;
                            }
                          } else if (eq.id === 'concretagem') {
                            if ((eqLower.includes('pedreiro') || eqLower.includes('mestre')) && (servLower.includes('concreto') || servLower.includes('desforma') || vagaoLower.includes('concreto') || servLower.includes('lastro') || servLower.includes('capa'))) {
                              estaNesteLote = true;
                            } else if (servLower.includes('concreto') || servLower.includes('desforma') || vagaoLower.includes('concreto')) {
                              estaNesteLote = true;
                            }
                          } else if (eq.id === 'escavacao') {
                            if (eqLower.includes('operador') || eqLower.includes('topógrafo') || eqLower.includes('topografo') || vagaoLower.includes('escavação') || vagaoLower.includes('canteiro') || servLower.includes('escavação') || servLower.includes('canteiro') || servLower.includes('gabarito')) {
                              estaNesteLote = true;
                            }
                          } else if (eq.id === 'alvenaria') {
                            if (servLower.includes('alvenaria') || eqLower.includes('sub-02') || vagaoLower.includes('alvenaria') || servLower.includes('bloco') || servLower.includes('reboco') || servLower.includes('chapisco') || servLower.includes('emboço')) {
                              estaNesteLote = true;
                            }
                          } else if (eq.id === 'cobertura') {
                            if (servLower.includes('cobertura') || servLower.includes('telha') || eqLower.includes('montador') || vagaoLower.includes('cobertura') || servLower.includes('terça') || servLower.includes('esquadria') || servLower.includes('vidro') || servLower.includes('porta')) {
                              estaNesteLote = true;
                            }
                          } else if (eq.id === 'instalacoes') {
                            if (eqLower.includes('eletricista') || eqLower.includes('encanador') || eqLower.includes('sub-03') || eqLower.includes('sub-04') || vagaoLower.includes('elétrica') || vagaoLower.includes('eletrica') || vagaoLower.includes('hidráulica') || vagaoLower.includes('hidraulica') || servLower.includes('eletroduto') || servLower.includes('cabo') || servLower.includes('quadro') || servLower.includes('louça') || servLower.includes('hidrostático') || servLower.includes('luminária') || servLower.includes('comissionamento')) {
                              estaNesteLote = true;
                            }
                          } else if (eq.id === 'revestimentos') {
                            if (eqLower.includes('ladrilhista') || eqLower.includes('sub-05') || vagaoLower.includes('porcelanato') || vagaoLower.includes('revestimento') || servLower.includes('porcelanato') || servLower.includes('cerâmica') || servLower.includes('rejunte') || servLower.includes('contrapiso') || servLower.includes('impermeabiliz')) {
                              estaNesteLote = true;
                            }
                          } else if (eq.id === 'climatizacao') {
                            if (eqLower.includes('hvac') || eqLower.includes('refrigeração') || eqLower.includes('sub-08') || vagaoLower.includes('climatização') || vagaoLower.includes('frigorígena') || servLower.includes('frigorígena') || servLower.includes('hvac') || servLower.includes('evaporadora')) {
                              estaNesteLote = true;
                            }
                          } else if (eq.id === 'pintura') {
                            if (eqLower.includes('pintor') || eqLower.includes('sub-06') || vagaoLower.includes('pintura') || servLower.includes('pintura') || servLower.includes('massa') || servLower.includes('emassamento') || servLower.includes('limpeza')) {
                              estaNesteLote = true;
                            }
                          }
                        }

                        return (
                          <div 
                            key={i} 
                            onClick={() => lote && setLoteSelecionado(lote)}
                            className={`rounded-xl p-2.5 border transition-all cursor-pointer flex flex-col justify-between relative group ${
                              estaNesteLote && lote
                                ? `${eq.cor} hover:scale-[1.02] shadow-lg`
                                : 'bg-zinc-950/40 border-zinc-900/80 hover:border-zinc-800'
                            }`}
                          >
                            {estaNesteLote && lote ? (
                              <>
                                <div className="flex items-center justify-between gap-1">
                                  <span className="font-mono text-[9px] font-bold px-1.5 py-0.5 rounded bg-black/40 border border-white/10 text-white">
                                    {lote.codLote}
                                  </span>
                                  <span className="text-[8px] font-bold text-emerald-400 bg-emerald-950/80 px-1 rounded border border-emerald-800/40">
                                    0% OCIOSO
                                  </span>
                                </div>

                                <div className="my-1.5">
                                  <span className="text-[9px] font-bold text-white block line-clamp-2 leading-tight" title={lote.servico}>
                                    {lote.servico}
                                  </span>
                                  <span className="text-[8px] text-zinc-300 block mt-0.5 font-medium truncate">
                                    📍 {etapaTexto.split('(')[0]}
                                  </span>
                                </div>

                                <div className="pt-1 border-t border-white/10 flex items-center justify-between text-[8px] text-zinc-300 font-mono">
                                  <span>{lote.headcount} Operários</span>
                                  <span className="text-amber-300">{lote.duracaoDias}d Takt</span>
                                </div>
                              </>
                            ) : (
                              <div className="h-full min-h-[85px] flex flex-col items-center justify-center text-center p-1">
                                <span className="text-[8px] font-mono text-zinc-500 uppercase tracking-wider block font-semibold">
                                  {eq.id === 'carpintaria' || eq.id === 'armacao' || eq.id === 'concretagem' || eq.id === 'escavacao'
                                    ? 'Bancada / Standby'
                                    : eq.id === 'alvenaria' || eq.id === 'cobertura'
                                    ? 'Fase 2'
                                    : eq.id === 'revestimentos'
                                    ? 'Fase 3'
                                    : eq.id === 'instalacoes' || eq.id === 'climatizacao'
                                    ? 'Fase 4'
                                    : 'Fase 5'}
                                </span>
                                <span className="text-[7px] text-zinc-600 block mt-1 leading-tight">
                                  {eq.id === 'carpintaria' 
                                    ? 'Pré-montagem fôrmas' 
                                    : eq.id === 'armacao' 
                                    ? 'Corte e dobra central' 
                                    : eq.id === 'concretagem' 
                                    ? 'Aguardando cura/fôrmas' 
                                    : eq.id === 'escavacao' 
                                    ? 'Manutenção canteiro'
                                    : eq.id === 'alvenaria'
                                    ? 'Frentes a partir da Sem 09'
                                    : eq.id === 'cobertura'
                                    ? 'Frentes a partir da Sem 10'
                                    : eq.id === 'instalacoes'
                                    ? 'Frentes a partir da Sem 11'
                                    : eq.id === 'revestimentos'
                                    ? 'Frentes a partir da Sem 14'
                                    : eq.id === 'climatizacao'
                                    ? 'Frentes a partir da Sem 18'
                                    : 'Frentes a partir da Sem 21'}
                                </span>
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  );
                })}
              </div>
            )}

            {/* CORPO: LINHAS POR ZONA TAKT (MODO ZONAS) */}
            {visaoModo === 'zonas' && (
              <div className="space-y-3">
                {zonasTakt.map((zona) => (
                  <div 
                    key={zona.id} 
                    className="grid gap-2 items-stretch"
                    style={{ gridTemplateColumns: `220px repeat(${ciclosFiltrados.length}, minmax(170px, 1fr))` }}
                  >
                    {/* IDENTIFICADOR DA ZONA */}
                    <div className="bg-zinc-950 p-3.5 rounded-xl border border-zinc-800 flex flex-col justify-center">
                      <span className="text-xs font-bold text-white">{zona.nome}</span>
                      <span className="text-[9px] text-zinc-400 mt-1 leading-tight">{zona.descricao}</span>
                      <div className="mt-2">
                        <span className={`text-[9px] font-mono font-bold px-2 py-0.5 rounded border ${zona.corBadge}`}>
                          {zona.id} Ativa
                        </span>
                      </div>
                    </div>

                    {/* VAGÕES NA ZONA AO LONGO DOS CICLOS */}
                    {ciclosFiltrados.map((c, i) => {
                      const lote = encontrarLote(c.ciclo, c.semana, c.dias);

                      const isZonaDesteLote = lote && (
                        lote.etapaZona?.toLowerCase().includes(zona.id.toLowerCase()) ||
                        lote.setor?.toLowerCase().includes(zona.id.toLowerCase())
                      );

                      // Lógica de tempo tecnológico de cura (quando o lote anterior foi concretagem nesta zona)
                      const isTempoCura = !isZonaDesteLote && (
                        (zona.id === 'Etapa 1' && (c.ciclo === 'Ciclo 04' || c.ciclo === 'Ciclo 10' || c.ciclo === 'Ciclo 12')) ||
                        (zona.id === 'Etapa 2' && (c.ciclo === 'Ciclo 06' || c.ciclo === 'Ciclo 11' || c.ciclo === 'Ciclo 13')) ||
                        (zona.id === 'Etapa 3' && (c.ciclo === 'Ciclo 08' || c.ciclo === 'Ciclo 14'))
                      );

                      return (
                        <div 
                          key={i}
                          onClick={() => lote && setLoteSelecionado(lote)}
                          className={`rounded-xl p-2.5 border transition-all cursor-pointer flex flex-col justify-between ${
                            isZonaDesteLote && lote
                              ? 'bg-gradient-to-br from-blue-950/80 to-zinc-900 border-blue-500/80 text-white shadow-lg hover:scale-[1.02]'
                              : isTempoCura
                              ? 'bg-zinc-950/90 border-amber-500/40 text-zinc-400 border-dashed'
                              : 'bg-zinc-950/30 border-zinc-900/60 opacity-30 hover:opacity-60'
                          }`}
                        >
                          {isZonaDesteLote && lote ? (
                            <>
                              <div className="flex items-center justify-between">
                                <span className="font-mono text-[9px] font-bold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/40">
                                  {lote.codLote}
                                </span>
                                <span className="text-[8px] font-mono text-emerald-400 font-bold">EM EXECUÇÃO</span>
                              </div>

                              <div className="my-1.5">
                                <span className="text-[9px] font-bold text-white block line-clamp-2 leading-tight">
                                  {lote.servico}
                                </span>
                                <span className="text-[8px] text-zinc-300 block mt-0.5 truncate font-mono">
                                  👷 {lote.equipePrevista.split('+')[0]}
                                </span>
                              </div>

                              <div className="pt-1 border-t border-zinc-800 flex items-center justify-between text-[8px] text-zinc-400 font-mono">
                                <span>{lote.headcount} Operários</span>
                                <span className="text-blue-400 font-bold">3d Takt</span>
                              </div>
                            </>
                          ) : isTempoCura ? (
                            <div className="h-full min-h-[85px] flex flex-col items-center justify-center text-center p-1">
                              <ShieldCheck className="w-4 h-4 text-amber-400 mb-1" />
                              <span className="text-[8px] font-bold text-amber-400 uppercase tracking-wider block">Cura Tecnológica</span>
                              <span className="text-[7px] text-zinc-400 block mt-0.5 font-mono">Equipe na outra zona</span>
                            </div>
                          ) : (
                            <div className="h-full min-h-[85px] flex flex-col items-center justify-center text-center p-1 text-[8px] text-zinc-600 font-mono">
                              <span>Aguardando Vagão</span>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* MODAL DETALHE DO LOTE AO CLICAR NO VAGÃO */}
      {loteSelecionado && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-zinc-900 border border-zinc-700 rounded-2xl max-w-xl w-full p-6 shadow-2xl space-y-4 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
              <div className="flex items-center gap-2.5">
                <span className="font-mono text-sm font-bold bg-blue-600 text-white px-2.5 py-1 rounded-lg">
                  {loteSelecionado.codLote}
                </span>
                <div>
                  <h4 className="text-base font-bold text-white">{loteSelecionado.semana} ({loteSelecionado.duracaoDias} dias Takt)</h4>
                  <span className="text-xs text-zinc-400 font-mono">{loteSelecionado.diasSemana}</span>
                </div>
              </div>
              <button
                onClick={() => setLoteSelecionado(null)}
                className="text-xs font-semibold text-zinc-400 hover:text-white px-2.5 py-1.5 rounded-lg hover:bg-zinc-800"
              >
                Fechar
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="bg-zinc-950 p-3 rounded-xl border border-zinc-800">
                <span className="text-[10px] text-zinc-500 uppercase font-semibold block">Serviço Programado</span>
                <span className="text-sm font-bold text-zinc-100 block mt-0.5">{loteSelecionado.servico}</span>
                <span className="text-xs text-emerald-400 font-mono block mt-1">Meta Física: {loteSelecionado.metaFisica}</span>
                <span className="text-[11px] text-zinc-500 font-mono block">RUP Meta: {loteSelecionado.rupMeta}</span>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="bg-zinc-950 p-3 rounded-xl border border-zinc-800">
                  <span className="text-[10px] text-zinc-500 uppercase font-semibold block">Recursos Humanos</span>
                  <span className="text-xs font-bold text-white block mt-0.5">{loteSelecionado.equipePrevista}</span>
                  <span className="text-[11px] text-emerald-400 font-mono block mt-1">{loteSelecionado.headcount} operários alocados</span>
                </div>

                <div className="bg-zinc-950 p-3 rounded-xl border border-zinc-800">
                  <span className="text-[10px] text-zinc-500 uppercase font-semibold block">Equipamentos Previstos</span>
                  <span className="text-xs text-zinc-300 block mt-0.5">{loteSelecionado.equipamentos}</span>
                </div>
              </div>

              <div className="bg-zinc-950 p-3 rounded-xl border border-zinc-800">
                <span className="text-[10px] text-zinc-500 uppercase font-semibold block">Insumos UCC Requisitados</span>
                <span className="text-xs text-zinc-300 block mt-0.5">{loteSelecionado.materiaisUcc}</span>
              </div>

              <div className="bg-emerald-950/30 border border-emerald-800/40 p-3 rounded-xl flex items-center justify-between">
                <div>
                  <span className="text-[10px] text-emerald-400 font-bold uppercase block">Status de Nivelamento Lean</span>
                  <span className="text-xs text-zinc-300">100% Sincronizado na Esteira Takt (Zero Ociosidade)</span>
                </div>
                <span className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 px-2 py-1 rounded text-xs font-bold">
                  {loteSelecionado.status}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
