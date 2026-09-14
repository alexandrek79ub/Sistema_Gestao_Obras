import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';
import { ErroObra, obterObraObrigatoria } from '@/lib/obra';

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

const CATALOGO_PADRAO_FVS = [
  {
    codigo: 'FVS-01',
    titulo: 'Topografia, Locação de Eixos e Terraplenagem',
    norma: 'ABNT NBR 13133',
    pop: 'POP 21 / POP 01',
    contratoBloqueado: 'SUB-01 (Estrutura e Fundações)',
    servicoLiberado: 'Escavação mecanizada profunda e concretagem de lastro de fundação',
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
    codigo: 'FVS-02',
    titulo: 'Fundações Isoladas, Estacas e Vigas Baldrames',
    norma: 'ABNT NBR 6122 / NBR 9575',
    pop: 'POP 10 / POP 14',
    contratoBloqueado: 'SUB-01 (Medições 01 e 02)',
    servicoLiberado: 'Lançamento de concreto estrutural usinado e reaterro de valas',
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
    codigo: 'FVS-03',
    titulo: 'Estrutura de Concreto Armado (Pilares, Vigas e Lajes)',
    norma: 'ABNT NBR 6118 / NBR 14931',
    pop: 'POP 11 / POP 19 / POP 22',
    contratoBloqueado: 'SUB-01 (Medições 03 e 04)',
    servicoLiberado: 'Desforma de fundo de vigas/lajes e alvenaria de vedação',
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
    codigo: 'FVS-04',
    titulo: 'Alvenaria Estrutural e Vedação',
    norma: 'ABNT NBR 8545 / NBR 6136',
    pop: 'POP 12',
    contratoBloqueado: 'SUB-02 (Alvenaria e Vedações)',
    servicoLiberado: 'Aplicação de chapisco, emboço e reboco nas paredes',
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
    codigo: 'FVS-05',
    titulo: 'Impermeabilização e Teste de Estanqueidade (72 Horas)',
    norma: 'ABNT NBR 9575 / NBR 9574',
    pop: 'POP 14',
    contratoBloqueado: 'SUB-07 (Impermeabilização)',
    servicoLiberado: 'Instalação de revestimentos cerâmicos, pisos vinílicos e reaterro',
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
    codigo: 'FVS-06',
    titulo: 'Instalações Hidráulicas e Teste Hidrostático sob Pressão',
    norma: 'ABNT NBR 5626 / NBR 8160',
    pop: 'POP 15',
    contratoBloqueado: 'SUB-05 (Instalações Hidráulicas)',
    servicoLiberado: 'Chapisco e emboço de alvenarias com tubulações e fechamento de shafts',
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
    codigo: 'FVS-07',
    titulo: 'Instalações Elétricas, Cabeamento e Malha SPDA',
    norma: 'ABNT NBR 5410 / NBR 5419',
    pop: 'POP 16 / POP 23',
    contratoBloqueado: 'SUB-06 (Instalações Elétricas e SPDA)',
    servicoLiberado: 'Fechamento de forro de gesso, colocação de espelhos e energização final',
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
    codigo: 'FVS-08',
    titulo: 'Cobertura Termoacústica, Calhas e Esquadrias de Alumínio',
    norma: 'ABNT NBR 10821 / NBR 14718',
    pop: 'POP 24 / POP 25',
    contratoBloqueado: 'SUB-03 (Cobertura) e SUB-04 (Esquadrias)',
    servicoLiberado: 'Execução de forros internos de gesso e pintura fina de acabamento',
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

export async function GET(request: Request) {
  try {
    const { obra, diretorio } = obterObraObrigatoria(request);
    const url = new URL(request.url);
    const demo = url.searchParams.get('demo') === 'true';

    if (demo) {
      const demoFvss: FvsItem[] = CATALOGO_PADRAO_FVS.map((item, idx) => ({
        id: `fvs-0${idx + 1}`,
        codigo: item.codigo,
        titulo: item.titulo,
        norma: item.norma,
        pop: item.pop,
        contratoBloqueado: item.contratoBloqueado,
        servicoLiberado: item.servicoLiberado,
        status: idx === 0 || idx === 1 ? 'APROVADO' : idx === 2 ? 'EM_INSPECAO' : 'PENDENTE',
        dataUltimaInspecao: idx === 0 ? '22/09/2026' : idx === 1 ? '29/09/2026' : undefined,
        responsavel: idx < 2 ? 'Eng. Residente' : undefined,
        toleranciaCritica: item.toleranciaCritica,
        checklist: item.checklist,
      }));

      const demoSubcontratos: SubcontratoStatus[] = [
        { codigo: 'SUB-01', nome: 'Estrutura e Fundações', fvsCondicionante: 'FVS-01 (OK), FVS-02 (OK), FVS-03 (Inspeção)', statusMedicao: 'RETENCAO_QUALIDADE', retencaoTecnicaPercent: 5.0 },
        { codigo: 'SUB-02', nome: 'Alvenaria e Vedações', fvsCondicionante: 'FVS-04', statusMedicao: 'BLOQUEADO', retencaoTecnicaPercent: 5.0 },
        { codigo: 'SUB-03', nome: 'Cobertura e Estrutura Metálica', fvsCondicionante: 'FVS-08', statusMedicao: 'BLOQUEADO', retencaoTecnicaPercent: 5.0 },
        { codigo: 'SUB-04', nome: 'Esquadrias de Alumínio e Vidros', fvsCondicionante: 'FVS-08', statusMedicao: 'BLOQUEADO', retencaoTecnicaPercent: 5.0 },
        { codigo: 'SUB-05', nome: 'Instalações Hidráulicas e Combate a Incêndio', fvsCondicionante: 'FVS-06', statusMedicao: 'BLOQUEADO', retencaoTecnicaPercent: 5.0 },
        { codigo: 'SUB-06', nome: 'Instalações Elétricas e SPDA', fvsCondicionante: 'FVS-07', statusMedicao: 'BLOQUEADO', retencaoTecnicaPercent: 5.0 },
        { codigo: 'SUB-07', nome: 'Impermeabilização e Tratamentos', fvsCondicionante: 'FVS-05', statusMedicao: 'BLOQUEADO', retencaoTecnicaPercent: 5.0 },
        { codigo: 'SUB-08', nome: 'Pintura, Revestimentos e Acabamentos', fvsCondicionante: 'FVS-04, FVS-05, FVS-08', statusMedicao: 'BLOQUEADO', retencaoTecnicaPercent: 5.0 },
      ];

      return NextResponse.json({
        success: true,
        obra,
        modoDemo: true,
        rotulo: 'MODO DEMONSTRAÇÃO - DADOS SIMULADOS NÃO REAIS',
        proveniencia: { fonte: 'FIXTURE_DEMONSTRACAO' },
        resumo: {
          totalFvss: demoFvss.length,
          aprovadas: 2,
          emInspecao: 1,
          pendentes: 5,
          taxaConformidade: 25,
          contratosBloqueados: 7,
        },
        fvss: demoFvss,
        subcontratos: demoSubcontratos,
      });
    }

    // --- MODO PRODUÇÃO REAL: Inspecionar registros oficiais de campo da obra ativa ---
    const producaoDir = path.join(diretorio, '04_PRODUCAO_E_AVANCO');
    const regCampoPath = path.join(producaoDir, 'REGISTRO_INSPECOES_CAMPO.md');
    const filaCampoPath = path.join(producaoDir, 'fila_apontamentos_campo.json');

    // Mapeamento de inspeções reais registradas
    const inspecoesRegistradas: Record<string, { status: 'APROVADO' | 'EM_INSPECAO' | 'BLOQUEADO' | 'PENDENTE'; data?: string; resp?: string }> = {};

    if (fs.existsSync(regCampoPath)) {
      try {
        const mdText = fs.readFileSync(regCampoPath, 'utf-8');
        const linhas = mdText.split('\n');
        for (const linha of linhas) {
          // Ex: | FVS-01 | Topografia... | APROVADA | 22/09/2026 | Eng. Alexandre |
          const colunas = linha.split('|').map((c) => c.trim()).filter(Boolean);
          if (colunas.length >= 4 && /^FVS-\d+/i.test(colunas[0])) {
            const cod = colunas[0].toUpperCase();
            const stTexto = colunas[2].toUpperCase();
            let st: 'APROVADO' | 'EM_INSPECAO' | 'BLOQUEADO' | 'PENDENTE' = 'PENDENTE';
            if (stTexto.includes('APROVAD')) st = 'APROVADO';
            else if (stTexto.includes('REPROVAD')) st = 'BLOQUEADO';
            else if (stTexto.includes('INSPE')) st = 'EM_INSPECAO';

            inspecoesRegistradas[cod] = {
              status: st,
              data: colunas[3] || undefined,
              resp: colunas[4] || undefined,
            };
          }
        }
      } catch (regErr) {
        console.error('Erro ao ler REGISTRO_INSPECOES_CAMPO.md:', regErr);
      }
    }

    // Se houver submissões na fila aguardando promoção
    if (fs.existsSync(filaCampoPath)) {
      try {
        const filaRaw = JSON.parse(fs.readFileSync(filaCampoPath, 'utf-8'));
        if (Array.isArray(filaRaw)) {
          for (const item of filaRaw) {
            const cod = String(item?.dados_entrada?.codigo || item?.codigo || '').trim().toUpperCase();
            if (cod && !inspecoesRegistradas[cod]) {
              const res = item.resultado;
              if (res?.status === 'APROVADA') {
                inspecoesRegistradas[cod] = { status: 'APROVADO', resp: res.responsavel };
              } else if (res?.status === 'REPROVADA') {
                inspecoesRegistradas[cod] = { status: 'BLOQUEADO', resp: res.responsavel };
              } else {
                inspecoesRegistradas[cod] = { status: 'EM_INSPECAO' };
              }
            }
          }
        }
      } catch (fErr) {
        console.error('Erro ao ler fila_apontamentos_campo.json:', fErr);
      }
    }

    // Construir FVSs da obra: nenhuma é dada como aprovada sem registro real comprovado
    const fvss: FvsItem[] = CATALOGO_PADRAO_FVS.map((cat, idx) => {
      const registro = inspecoesRegistradas[cat.codigo];
      return {
        id: `fvs-0${idx + 1}`,
        codigo: cat.codigo,
        titulo: cat.titulo,
        norma: cat.norma,
        pop: cat.pop,
        contratoBloqueado: cat.contratoBloqueado,
        servicoLiberado: cat.servicoLiberado,
        status: registro ? registro.status : 'PENDENTE',
        dataUltimaInspecao: registro?.data,
        responsavel: registro?.resp,
        toleranciaCritica: cat.toleranciaCritica,
        checklist: cat.checklist,
      };
    });

    // Definir condicionantes de subcontratos baseados estritamente nas FVSs da obra
    const fvsStatusMap = new Map(fvss.map((f) => [f.codigo, f.status]));

    const checkContrato = (requisitos: string[]): 'LIBERADO' | 'RETENCAO_QUALIDADE' | 'BLOQUEADO' => {
      const statuses = requisitos.map((r) => fvsStatusMap.get(r) || 'PENDENTE');
      if (statuses.every((s) => s === 'APROVADO')) return 'LIBERADO';
      if (statuses.some((s) => s === 'EM_INSPECAO' || s === 'APROVADO')) return 'RETENCAO_QUALIDADE';
      return 'BLOQUEADO';
    };

    const subcontratos: SubcontratoStatus[] = [
      {
        codigo: 'SUB-01',
        nome: 'Estrutura e Fundações',
        fvsCondicionante: 'FVS-01, FVS-02, FVS-03',
        statusMedicao: checkContrato(['FVS-01', 'FVS-02', 'FVS-03']),
        retencaoTecnicaPercent: 5.0,
      },
      {
        codigo: 'SUB-02',
        nome: 'Alvenaria e Vedações',
        fvsCondicionante: 'FVS-04',
        statusMedicao: checkContrato(['FVS-04']),
        retencaoTecnicaPercent: 5.0,
      },
      {
        codigo: 'SUB-03',
        nome: 'Cobertura e Estrutura Metálica',
        fvsCondicionante: 'FVS-08',
        statusMedicao: checkContrato(['FVS-08']),
        retencaoTecnicaPercent: 5.0,
      },
      {
        codigo: 'SUB-04',
        nome: 'Esquadrias de Alumínio e Vidros',
        fvsCondicionante: 'FVS-08',
        statusMedicao: checkContrato(['FVS-08']),
        retencaoTecnicaPercent: 5.0,
      },
      {
        codigo: 'SUB-05',
        nome: 'Instalações Hidráulicas e Combate a Incêndio',
        fvsCondicionante: 'FVS-06',
        statusMedicao: checkContrato(['FVS-06']),
        retencaoTecnicaPercent: 5.0,
      },
      {
        codigo: 'SUB-06',
        nome: 'Instalações Elétricas e SPDA',
        fvsCondicionante: 'FVS-07',
        statusMedicao: checkContrato(['FVS-07']),
        retencaoTecnicaPercent: 5.0,
      },
      {
        codigo: 'SUB-07',
        nome: 'Impermeabilização e Tratamentos',
        fvsCondicionante: 'FVS-05',
        statusMedicao: checkContrato(['FVS-05']),
        retencaoTecnicaPercent: 5.0,
      },
      {
        codigo: 'SUB-08',
        nome: 'Pintura, Revestimentos e Acabamentos',
        fvsCondicionante: 'FVS-04, FVS-05, FVS-08',
        statusMedicao: checkContrato(['FVS-04', 'FVS-05', 'FVS-08']),
        retencaoTecnicaPercent: 5.0,
      },
    ];

    const totalAprovadas = fvss.filter((f) => f.status === 'APROVADO').length;
    const totalEmInspecao = fvss.filter((f) => f.status === 'EM_INSPECAO').length;
    const totalPendentes = fvss.filter((f) => f.status === 'PENDENTE' || f.status === 'BLOQUEADO').length;

    return NextResponse.json({
      success: true,
      obra,
      modoDemo: false,
      status: totalAprovadas > 0 || totalEmInspecao > 0 ? 'OK' : 'SEM_INSPECOES_CONCLUIDAS',
      proveniencia: {
        catalogo: 'apoio/catalogo_fvs.json',
        registroCampo: fs.existsSync(regCampoPath) ? path.basename(regCampoPath) : null,
        filaCampo: fs.existsSync(filaCampoPath) ? path.basename(filaCampoPath) : null,
      },
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
  } catch (error: unknown) {
    if (error instanceof ErroObra) return NextResponse.json({ error: error.message }, { status: 400 });
    return NextResponse.json({ error: 'Falha ao ler qualidade.' }, { status: 500 });
  }
}
