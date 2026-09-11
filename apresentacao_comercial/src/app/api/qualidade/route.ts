import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';

export const dynamic = 'force-dynamic';

export interface FvsItem {
  id: string;
  codigo: string;
  titulo: string;
  norma: string;
  pop: string;
  contratoBloqueado: string;
  servicoLiberado: string;
  status: 'APROVADO' | 'EM_INSPECAO' | 'BLOQUEADO' | 'PENDENTE';
  dataUltimaInspecao?: string;
  responsavel?: string;
  toleranciaCritica: string;
  checklist: string[];
}

export interface SubcontratoStatus {
  codigo: string;
  nome: string;
  fvsCondicionante: string;
  statusMedicao: 'LIBERADO' | 'RETENCAO_QUALIDADE' | 'BLOQUEADO';
  retencaoTecnicaPercent: number;
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const obra = searchParams.get('obra') || 'OBRA_TMULT';

  const basePath = process.env.OBRA_PATH
    ? process.env.OBRA_PATH.replace(/OBRA$/, obra)
    : path.resolve(process.cwd(), `../projetos/${obra}`);

  const producaoDir = path.join(basePath, '04_PRODUCAO_E_AVANCO');
  const filaCampoPath = path.join(producaoDir, 'fila_apontamentos_campo.json');

  // Base normativa das 8 FVSs do Caderno Mestre
  const fvss: FvsItem[] = [
    {
      id: 'fvs-01',
      codigo: 'FVS-01',
      titulo: 'Topografia, Locação de Eixos e Terraplenagem',
      norma: 'ABNT NBR 13133',
      pop: 'POP 21 / POP 01',
      contratoBloqueado: 'SUB-01 (Estrutura e Fundações)',
      servicoLiberado: 'Escavação mecanizada profunda e concretagem de lastro de fundação',
      status: 'APROVADO',
      dataUltimaInspecao: '22/09/2026',
      responsavel: 'Eng. Alexandre / Mestre João Silva',
      toleranciaCritica: 'Erro angular máx. ±10"; Desvio linear máx. ±3mm; Nível de cota máx. ±10mm',
      checklist: [
        'Locação do gabarito perimetral de tábua corrida travado e pintado',
        'Conferência de esquadro via triangulação 3-4-5 com estação total',
        'Cotas de nível amarradas ao marco georreferenciado RN oficial',
        'Alinhamento dos eixos de sapatas e arranques de pilares com fio de nylon',
        'Compactação e nivelamento da praça de trabalho e valas',
      ],
    },
    {
      id: 'fvs-02',
      codigo: 'FVS-02',
      titulo: 'Fundações Isoladas, Estacas e Vigas Baldrames',
      norma: 'ABNT NBR 6122 / NBR 9575',
      pop: 'POP 10 / POP 14',
      contratoBloqueado: 'SUB-01 (Medições 01 e 02)',
      servicoLiberado: 'Lançamento de concreto estrutural usinado e reaterro de valas',
      status: 'APROVADO',
      dataUltimaInspecao: '29/09/2026',
      responsavel: 'Eng. Alexandre / Mestre João Silva',
      toleranciaCritica: 'Lastro concreto magro ≥50mm; Cobrimento armadura solo ≥50mm; Desaprumo máx. 5mm',
      checklist: [
        'Limpeza e remoção total de terra solta do fundo de cava antes do lastro',
        'Aplicação de concreto magro e=5cm em 100% da área de contato das sapatas',
        'Montagem e estroncamento de fôrmas compensadas de sapatas e baldrames',
        'Espaçadores plásticos tipo pastilha de concreto (proibido toco de madeira)',
        'Amarração de arranques de pilares (P1 a P24) com transpasse normativo',
      ],
    },
    {
      id: 'fvs-03',
      codigo: 'FVS-03',
      titulo: 'Estrutura de Concreto Armado (Pilares, Vigas e Lajes)',
      norma: 'ABNT NBR 6118 / NBR 14931',
      pop: 'POP 11 / POP 19 / POP 22',
      contratoBloqueado: 'SUB-01 (Medições 03 e 04)',
      servicoLiberado: 'Desforma de fundo de vigas/lajes e alvenaria de vedação',
      status: 'EM_INSPECAO',
      dataUltimaInspecao: '30/09/2026',
      responsavel: 'Eng. Residente',
      toleranciaCritica: 'Slump test 12±2cm; fck ≥ 30 MPa aos 28d; Flecha máx. L/350; Desaprumo máx. H/500',
      checklist: [
        'Inspeção do cimbramento metálico e escoramento com cálculo de contra-flecha',
        'Conferência das armaduras positivas, negativas e estribos contra pranchas estruturais',
        'Slump test na caçamba do caminhão betoneira antes da descarga de concreto usinado',
        'Moldagem de 4 corpos de prova cilíndricos por caminhão betoneira (NBR 5738)',
        'Cura úmida contínua por aspersão de água ou membrana química por no mínimo 7 dias',
      ],
    },
    {
      id: 'fvs-04',
      codigo: 'FVS-04',
      titulo: 'Alvenaria Estrutural e Vedação',
      norma: 'ABNT NBR 8545 / NBR 6136',
      pop: 'POP 12',
      contratoBloqueado: 'SUB-02 (Alvenaria e Vedações)',
      servicoLiberado: 'Aplicação de chapisco, emboço e reboco nas paredes',
      status: 'PENDENTE',
      toleranciaCritica: 'Desaprumo máx. 5mm por pé-direito; Espessura de junta 10 a 15mm; Nivelamento máx. 3mm/m',
      checklist: [
        'Impermeabilização da fiada de arranque sobre o baldrame c/ argamassa polimérica',
        'Amortecimento e amarração de pilares com tela galvanizada soldada ou ferros-cabelo',
        'Preenchimento de 100% das juntas verticais e horizontais sem vazios',
        'Vergas e contravergas armadas em 100% dos vãos de portas e janelas (engaste ≥ 20cm)',
        'Encunhamento superior da alvenaria sob as vigas com argamassa expansiva resiliente',
      ],
    },
    {
      id: 'fvs-05',
      codigo: 'FVS-05',
      titulo: 'Impermeabilização e Teste de Estanqueidade (72 Horas)',
      norma: 'ABNT NBR 9575 / NBR 9574',
      pop: 'POP 14',
      contratoBloqueado: 'SUB-07 (Impermeabilização)',
      servicoLiberado: 'Instalação de revestimentos cerâmicos, pisos vinílicos e reaterro',
      status: 'PENDENTE',
      toleranciaCritica: 'Queda para ralos mín. 1,0%; Subida em rodapés mín. 20cm; Lâmina d água 72h sem perda',
      checklist: [
        'Regularização de base com caimento mínimo de 1% em direção aos ralos sem empoçamento',
        'Execução de meia-cana arredondada nos encontros entre piso e alvenaria (r=5cm)',
        'Aplicação de primer e manta asfáltica polimérica com transpasse mín. de 10cm',
        'Enchimento de água com lâmina mínima de 5cm e permanência estanque por 72 horas',
        'Camada separadora de filme plástico e proteção mecânica c/ argamassa de cimento e areia',
      ],
    },
    {
      id: 'fvs-06',
      codigo: 'FVS-06',
      titulo: 'Instalações Hidráulicas e Teste Hidrostático sob Pressão',
      norma: 'ABNT NBR 5626 / NBR 8160',
      pop: 'POP 15',
      contratoBloqueado: 'SUB-05 (Instalações Hidráulicas)',
      servicoLiberado: 'Chapisco e emboço de alvenarias com tubulações e fechamento de shafts',
      status: 'PENDENTE',
      toleranciaCritica: 'Pressão de ensaio: 1,5x pressão estática de trabalho (mín. 6 kgf/cm² por 1h sem queda)',
      checklist: [
        'Conferência de prumadas e alinhamentos de tubulações de água fria com braçadeiras',
        'Aplicação de pressão estática via bomba hidrostática manual aferida por manômetro',
        'Inspeção visual direta em 100% das conexões soldáveis e roscáveis sob pressão',
        'Declividade mínima de 1% para ramais de esgoto Ø 100mm e 2% para Ø 50mm e 75mm',
        'Amarração e vedação com anel de borracha lubrificado em 100% das bolsas de esgoto',
      ],
    },
    {
      id: 'fvs-07',
      codigo: 'FVS-07',
      titulo: 'Instalações Elétricas, Cabeamento e Malha SPDA',
      norma: 'ABNT NBR 5410 / NBR 5419',
      pop: 'POP 16 / POP 23',
      contratoBloqueado: 'SUB-06 (Instalações Elétricas e SPDA)',
      servicoLiberado: 'Fechamento de forro de gesso, colocação de espelhos e energização final',
      status: 'PENDENTE',
      toleranciaCritica: 'Resistência de aterramento SPDA ≤ 10 Ohms; Ocupação máx. eletroduto: 40%',
      checklist: [
        'Conferência de bitolas mínimas: 1,5mm² para iluminação e 2,5mm² para tomadas (TUG)',
        'Separação física de condutores de força, sinal e dados em eletrodutos independentes',
        'Instalação e teste individual do dispositivo IDR e DPS em todos os quadros (QGBT/QDL)',
        'Medição de resistência ôhmica da malha de aterramento através de terrômetro aferido',
        'Identificação e anilhamento de 100% dos circuitos no quadro de distribuição',
      ],
    },
    {
      id: 'fvs-08',
      codigo: 'FVS-08',
      titulo: 'Cobertura Termoacústica, Calhas e Esquadrias de Alumínio',
      norma: 'ABNT NBR 10821 / NBR 14718',
      pop: 'POP 24 / POP 25',
      contratoBloqueado: 'SUB-03 (Cobertura) e SUB-04 (Esquadrias)',
      servicoLiberado: 'Execução de forros internos de gesso e pintura fina de acabamento',
      status: 'PENDENTE',
      toleranciaCritica: 'Desaprumo de marcos de esquadrias máx. 2mm; Estanqueidade da cobertura sob jato de água',
      checklist: [
        'Conferência da fixação das telhas termoacústicas trapezoidais com parafusos autobrocantes',
        'Vedação e caimento de calhas e rufos metálicos com poliuretano estrutural (PU)',
        'Chumbamento e fixação de contramarcos de alumínio perfeitamente aprumados e nivelados',
        'Vedação perimetral externa de esquadrias com silicone neutro contra infiltração pluvial',
        'Teste de funcionamento de roldanas, fechos cremona, travas e maçanetas de portas e janelas',
      ],
    },
  ];

  // Checa se há apontamentos recentes do mobile para atualizar status
  if (fs.existsSync(filaCampoPath)) {
    try {
      const fila = JSON.parse(fs.readFileSync(filaCampoPath, 'utf-8'));
      if (Array.isArray(fila)) {
        for (const item of fila) {
          if (item?.dados?.tipo === 'fvs' && item.dados.codigo) {
            const fvsMatch = fvss.find((f) => f.codigo === item.dados.codigo);
            if (fvsMatch) {
              fvsMatch.status = 'APROVADO';
              fvsMatch.dataUltimaInspecao = item.dados.data || fvsMatch.dataUltimaInspecao;
              fvsMatch.responsavel = item.dados.responsavel || fvsMatch.responsavel;
            }
          }
        }
      }
    } catch (e) {
      console.error('Erro ao ler apontamentos de FVS:', e);
    }
  }

  // Matriz de Governança dos Subcontratos SUB-01 a SUB-08
  const subcontratos: SubcontratoStatus[] = [
    {
      codigo: 'SUB-01',
      nome: 'Estrutura e Fundações',
      fvsCondicionante: 'FVS-01 (OK), FVS-02 (OK), FVS-03 (Inspeção)',
      statusMedicao: 'RETENCAO_QUALIDADE',
      retencaoTecnicaPercent: 5.0,
    },
    {
      codigo: 'SUB-02',
      nome: 'Alvenaria e Vedações',
      fvsCondicionante: 'FVS-04',
      statusMedicao: 'BLOQUEADO',
      retencaoTecnicaPercent: 5.0,
    },
    {
      codigo: 'SUB-03',
      nome: 'Cobertura e Estrutura Metálica',
      fvsCondicionante: 'FVS-08',
      statusMedicao: 'BLOQUEADO',
      retencaoTecnicaPercent: 5.0,
    },
    {
      codigo: 'SUB-04',
      nome: 'Esquadrias de Alumínio e Vidros',
      fvsCondicionante: 'FVS-08',
      statusMedicao: 'BLOQUEADO',
      retencaoTecnicaPercent: 5.0,
    },
    {
      codigo: 'SUB-05',
      nome: 'Instalações Hidráulicas e Combate a Incêndio',
      fvsCondicionante: 'FVS-06',
      statusMedicao: 'BLOQUEADO',
      retencaoTecnicaPercent: 5.0,
    },
    {
      codigo: 'SUB-06',
      nome: 'Instalações Elétricas e SPDA',
      fvsCondicionante: 'FVS-07',
      statusMedicao: 'BLOQUEADO',
      retencaoTecnicaPercent: 5.0,
    },
    {
      codigo: 'SUB-07',
      nome: 'Impermeabilização e Tratamentos',
      fvsCondicionante: 'FVS-05',
      statusMedicao: 'BLOQUEADO',
      retencaoTecnicaPercent: 5.0,
    },
    {
      codigo: 'SUB-08',
      nome: 'Pintura, Revestimentos e Acabamentos',
      fvsCondicionante: 'FVS-04, FVS-05, FVS-08',
      statusMedicao: 'BLOQUEADO',
      retencaoTecnicaPercent: 5.0,
    },
  ];

  const totalAprovadas = fvss.filter((f) => f.status === 'APROVADO').length;
  const totalEmInspecao = fvss.filter((f) => f.status === 'EM_INSPECAO').length;
  const totalPendentes = fvss.filter((f) => f.status === 'PENDENTE' || f.status === 'BLOQUEADO').length;

  return NextResponse.json({
    success: true,
    obra,
    resumo: {
      totalFvss: fvss.length,
      aprovadas: totalAprovadas,
      emInspecao: totalEmInspecao,
      pendentes: totalPendentes,
      taxaConformidade: Math.round((totalAprovadas / fvss.length) * 100),
      contratosBloqueados: subcontratos.filter((s) => s.statusMedicao === 'BLOQUEADO').length,
    },
    fvss,
    subcontratos,
  });
}
