import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';

export const dynamic = 'force-dynamic';

export interface OperarioAso {
  id: string;
  nome: string;
  funcao: string;
  empresa: string;
  tipoAso: string;
  vencimento: string;
  diasParaVencer: number;
  status: 'APTO' | 'ALERTA_30D' | 'VENCIDO_BLOQUEADO';
  treinamentos: string[];
}

export interface ProgramaLegal {
  programa: string;
  titular: string;
  emissao: string;
  vigencia: string;
  status: 'VIGENTE' | 'RENOVAR' | 'VENCIDO';
  responsavel: string;
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const obra = searchParams.get('obra') || 'OBRA_TMULT';

  const basePath = process.env.OBRA_PATH
    ? process.env.OBRA_PATH.replace(/OBRA$/, obra)
    : path.resolve(process.cwd(), `../projetos/${obra}`);

  const sstDir = path.join(basePath, '06_SST_E_RH');
  const histMoJsonPath = path.join(sstDir, 'dados_histograma_mo.json');

  let totalProprios = 5;
  let totalTerceiros = 8;
  let efetivoTotal = 13;

  if (fs.existsSync(histMoJsonPath)) {
    try {
      const data = JSON.parse(fs.readFileSync(histMoJsonPath, 'utf-8'));
      if (Array.isArray(data)) {
        // soma mês 1
        const mes1 = data.reduce((acc: number, row: (string | number)[]) => {
          const val = typeof row[4] === 'number' ? row[4] : 0;
          return acc + val;
        }, 0);
        if (mes1 > 0) efetivoTotal = mes1;
      }
    } catch (e) {
      console.error('Erro ao ler dados_histograma_mo:', e);
    }
  }

  // Lista controlada de operários no canteiro para o Semáforo de ASO
  const operarios: OperarioAso[] = [
    {
      id: 'OP-001',
      nome: 'Alexandre Silva',
      funcao: 'Engenheiro Residente',
      empresa: 'Construtora Própria',
      tipoAso: 'Periódico',
      vencimento: '15/09/2027',
      diasParaVencer: 365,
      status: 'APTO',
      treinamentos: ['NR-18', 'NR-35', 'NR-10'],
    },
    {
      id: 'OP-002',
      nome: 'João da Silva',
      funcao: 'Mestre de Obras Geral',
      empresa: 'Construtora Própria',
      tipoAso: 'Periódico',
      vencimento: '15/09/2027',
      diasParaVencer: 365,
      status: 'APTO',
      treinamentos: ['NR-18', 'NR-35', 'NR-12'],
    },
    {
      id: 'OP-003',
      nome: 'Carlos Eduardo Santos',
      funcao: 'Técnico de Segurança (TST)',
      empresa: 'Construtora Própria',
      tipoAso: 'Periódico',
      vencimento: '15/09/2027',
      diasParaVencer: 365,
      status: 'APTO',
      treinamentos: ['NR-18', 'NR-35', 'NR-10', 'NR-12', 'Primeiros Socorros'],
    },
    {
      id: 'OP-004',
      nome: 'Marcos Vinicius Lima',
      funcao: 'Almoxarife / Apontador',
      empresa: 'Construtora Própria',
      tipoAso: 'Periódico',
      vencimento: '15/09/2027',
      diasParaVencer: 365,
      status: 'APTO',
      treinamentos: ['NR-18'],
    },
    {
      id: 'OP-005',
      nome: 'Sebastião Souza',
      funcao: 'Vigia Noturno',
      empresa: 'Construtora Própria',
      tipoAso: 'Periódico',
      vencimento: '15/09/2027',
      diasParaVencer: 365,
      status: 'APTO',
      treinamentos: ['NR-18'],
    },
    {
      id: 'OP-006',
      nome: 'Raimundo Nonato',
      funcao: 'Encarregado de Carpintaria',
      empresa: 'SUB-01 (Estrutural)',
      tipoAso: 'Admissional',
      vencimento: '10/09/2027',
      diasParaVencer: 360,
      status: 'APTO',
      treinamentos: ['NR-18', 'NR-35', 'NR-12 (Serra)'],
    },
    {
      id: 'OP-007',
      nome: 'Francisco de Assis',
      funcao: 'Carpinteiro de Fôrmas',
      empresa: 'SUB-01 (Estrutural)',
      tipoAso: 'Admissional',
      vencimento: '10/09/2027',
      diasParaVencer: 360,
      status: 'APTO',
      treinamentos: ['NR-18', 'NR-35'],
    },
    {
      id: 'OP-008',
      nome: 'José Roberto Oliveira',
      funcao: 'Armador Chefe',
      empresa: 'SUB-01 (Estrutural)',
      tipoAso: 'Admissional',
      vencimento: '10/09/2027',
      diasParaVencer: 360,
      status: 'APTO',
      treinamentos: ['NR-18', 'NR-35'],
    },
    {
      id: 'OP-009',
      nome: 'Antônio Carlos Moreira',
      funcao: 'Armador',
      empresa: 'SUB-01 (Estrutural)',
      tipoAso: 'Admissional',
      vencimento: '10/09/2027',
      diasParaVencer: 360,
      status: 'APTO',
      treinamentos: ['NR-18', 'NR-35'],
    },
    {
      id: 'OP-010',
      nome: 'Cláudio Ferreira',
      funcao: 'Operador de Retroescavadeira',
      empresa: 'LOC-01 (Locadora)',
      tipoAso: 'Periódico',
      vencimento: '05/10/2026',
      diasParaVencer: 24,
      status: 'ALERTA_30D',
      treinamentos: ['NR-18', 'NR-12 (Máquinas Pesadas)', 'Direção Defensiva'],
    },
    {
      id: 'OP-011',
      nome: 'Valdir dos Santos',
      funcao: 'Pedreiro de Alvenaria',
      empresa: 'SUB-02 (Alvenaria)',
      tipoAso: 'Admissional',
      vencimento: '10/09/2027',
      diasParaVencer: 360,
      status: 'APTO',
      treinamentos: ['NR-18', 'NR-35'],
    },
    {
      id: 'OP-012',
      nome: 'Lucas Gabriel Martins',
      funcao: 'Servente de Obras',
      empresa: 'SUB-01 (Estrutural)',
      tipoAso: 'Admissional',
      vencimento: '10/09/2027',
      diasParaVencer: 360,
      status: 'APTO',
      treinamentos: ['NR-18'],
    },
    {
      id: 'OP-013',
      nome: 'Manoel Messias',
      funcao: 'Servente de Obras',
      empresa: 'SUB-01 (Estrutural)',
      tipoAso: 'Admissional',
      vencimento: '10/09/2027',
      diasParaVencer: 360,
      status: 'APTO',
      treinamentos: ['NR-18'],
    },
  ];

  const programasLegais: ProgramaLegal[] = [
    {
      programa: 'PGR (NR-01 / NR-18)',
      titular: 'Construtora Própria',
      emissao: '15/09/2026',
      vigencia: '15/09/2027',
      status: 'VIGENTE',
      responsavel: 'Eng. Segurança / TST',
    },
    {
      programa: 'PCMSO (NR-07)',
      titular: 'Construtora Própria',
      emissao: '15/09/2026',
      vigencia: '15/09/2027',
      status: 'VIGENTE',
      responsavel: 'Médico do Trabalho Coordenador',
    },
    {
      programa: 'LTCAT (INSS / Previdência)',
      titular: 'Construtora Própria',
      emissao: '15/09/2026',
      vigencia: '15/09/2027',
      status: 'VIGENTE',
      responsavel: 'Eng. Segurança do Trabalho',
    },
    {
      programa: 'PGR Terceiro (SUB-01)',
      titular: 'Empreiteira Estrutural',
      emissao: '10/09/2026',
      vigencia: '10/09/2027',
      status: 'VIGENTE',
      responsavel: 'TST Terceirizado',
    },
    {
      programa: 'PCMSO Terceiro (SUB-01)',
      titular: 'Empreiteira Estrutural',
      emissao: '10/09/2026',
      vigencia: '10/09/2027',
      status: 'VIGENTE',
      responsavel: 'Médico Coordenador Terceirizado',
    },
    {
      programa: 'ART Elétrica e Gerador Canteiro',
      titular: 'Instalações Provisórias',
      emissao: '18/09/2026',
      vigencia: '22/03/2027',
      status: 'VIGENTE',
      responsavel: 'Eng. Eletricista',
    },
    {
      programa: 'Laudo SPDA e Malha Aterramento',
      titular: 'Canteiro e Containers',
      emissao: '20/09/2026',
      vigencia: '20/09/2027',
      status: 'VIGENTE',
      responsavel: 'Eng. Eletricista',
    },
  ];

  const aptos = operarios.filter((o) => o.status === 'APTO').length;
  const alerta = operarios.filter((o) => o.status === 'ALERTA_30D').length;
  const bloqueados = operarios.filter((o) => o.status === 'VENCIDO_BLOQUEADO').length;

  return NextResponse.json({
    success: true,
    obra,
    resumo: {
      efetivoTotal,
      totalProprios,
      totalTerceiros,
      aptos,
      alerta30d: alerta,
      bloqueados,
      indiceConformidade: Math.round(((aptos + alerta) / operarios.length) * 100),
      diasSemAcidentes: 18,
      taxaDdsSemanal: 100,
      temaDdsSemana: 'Uso obrigatório de cinto tipo paraquedista em altura (NR-35) e linha de vida',
    },
    operarios,
    programasLegais,
  });
}
