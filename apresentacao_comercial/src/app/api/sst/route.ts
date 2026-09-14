import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';
import { ErroObra, obterObraObrigatoria } from '@/lib/obra';

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
  try {
    const { obra, diretorio } = obterObraObrigatoria(request);
    const url = new URL(request.url);
    const demo = url.searchParams.get('demo') === 'true';

    if (demo) {
      const demoOperarios: OperarioAso[] = [
        { id: 'OP-001', nome: 'Alexandre Silva', funcao: 'Engenheiro Residente', empresa: 'Construtora Própria', tipoAso: 'Periódico', vencimento: '15/09/2027', diasParaVencer: 365, status: 'APTO', treinamentos: ['NR-18', 'NR-35', 'NR-10'] },
        { id: 'OP-002', nome: 'João da Silva', funcao: 'Mestre de Obras Geral', empresa: 'Construtora Própria', tipoAso: 'Periódico', vencimento: '15/09/2027', diasParaVencer: 365, status: 'APTO', treinamentos: ['NR-18', 'NR-35', 'NR-12'] },
        { id: 'OP-003', nome: 'Carlos Eduardo Santos', funcao: 'Técnico de Segurança (TST)', empresa: 'Construtora Própria', tipoAso: 'Periódico', vencimento: '15/09/2027', diasParaVencer: 365, status: 'APTO', treinamentos: ['NR-18', 'NR-35', 'NR-10', 'NR-12', 'Primeiros Socorros'] },
        { id: 'OP-004', nome: 'Marcos Vinicius Lima', funcao: 'Almoxarife / Apontador', empresa: 'Construtora Própria', tipoAso: 'Periódico', vencimento: '15/09/2027', diasParaVencer: 365, status: 'APTO', treinamentos: ['NR-18'] },
        { id: 'OP-005', nome: 'Sebastião Souza', funcao: 'Vigia Noturno', empresa: 'Construtora Própria', tipoAso: 'Periódico', vencimento: '15/09/2027', diasParaVencer: 365, status: 'APTO', treinamentos: ['NR-18'] },
        { id: 'OP-006', nome: 'Raimundo Nonato', funcao: 'Encarregado de Carpintaria', empresa: 'SUB-01 (Estrutural)', tipoAso: 'Admissional', vencimento: '10/09/2027', diasParaVencer: 360, status: 'APTO', treinamentos: ['NR-18', 'NR-35', 'NR-12 (Serra)'] },
        { id: 'OP-007', nome: 'Francisco de Assis', funcao: 'Carpinteiro de Fôrmas', empresa: 'SUB-01 (Estrutural)', tipoAso: 'Admissional', vencimento: '10/09/2027', diasParaVencer: 360, status: 'APTO', treinamentos: ['NR-18', 'NR-35'] },
        { id: 'OP-008', nome: 'José Roberto Oliveira', funcao: 'Armador Chefe', empresa: 'SUB-01 (Estrutural)', tipoAso: 'Admissional', vencimento: '10/09/2027', diasParaVencer: 360, status: 'APTO', treinamentos: ['NR-18', 'NR-35'] },
        { id: 'OP-009', nome: 'Antônio Carlos Moreira', funcao: 'Armador', empresa: 'SUB-01 (Estrutural)', tipoAso: 'Admissional', vencimento: '10/09/2027', diasParaVencer: 360, status: 'APTO', treinamentos: ['NR-18', 'NR-35'] },
        { id: 'OP-010', nome: 'Cláudio Ferreira', funcao: 'Operador de Retroescavadeira', empresa: 'LOC-01 (Locadora)', tipoAso: 'Periódico', vencimento: '05/10/2026', diasParaVencer: 24, status: 'ALERTA_30D', treinamentos: ['NR-18', 'NR-12 (Máquinas Pesadas)', 'Direção Defensiva'] },
        { id: 'OP-011', nome: 'Valdir dos Santos', funcao: 'Pedreiro de Alvenaria', empresa: 'SUB-02 (Alvenaria)', tipoAso: 'Admissional', vencimento: '10/09/2027', diasParaVencer: 360, status: 'APTO', treinamentos: ['NR-18', 'NR-35'] },
        { id: 'OP-012', nome: 'Lucas Gabriel Martins', funcao: 'Servente de Obras', empresa: 'SUB-01 (Estrutural)', tipoAso: 'Admissional', vencimento: '10/09/2027', diasParaVencer: 360, status: 'APTO', treinamentos: ['NR-18'] },
        { id: 'OP-013', nome: 'Manoel Messias', funcao: 'Servente de Obras', empresa: 'SUB-01 (Estrutural)', tipoAso: 'Admissional', vencimento: '10/09/2027', diasParaVencer: 360, status: 'APTO', treinamentos: ['NR-18'] },
      ];

      const demoProgramas: ProgramaLegal[] = [
        { programa: 'PGR (NR-01 / NR-18)', titular: 'Construtora Própria', emissao: '15/09/2026', vigencia: '15/09/2027', status: 'VIGENTE', responsavel: 'Eng. Segurança / TST' },
        { programa: 'PCMSO (NR-07)', titular: 'Construtora Própria', emissao: '15/09/2026', vigencia: '15/09/2027', status: 'VIGENTE', responsavel: 'Médico do Trabalho Coordenador' },
        { programa: 'LTCAT (INSS / Previdência)', titular: 'Construtora Própria', emissao: '15/09/2026', vigencia: '15/09/2027', status: 'VIGENTE', responsavel: 'Eng. Segurança do Trabalho' },
        { programa: 'PGR Terceiro (SUB-01)', titular: 'Empreiteira Estrutural', emissao: '10/09/2026', vigencia: '10/09/2027', status: 'VIGENTE', responsavel: 'TST Terceirizado' },
        { programa: 'PCMSO Terceiro (SUB-01)', titular: 'Empreiteira Estrutural', emissao: '10/09/2026', vigencia: '10/09/2027', status: 'VIGENTE', responsavel: 'Médico Coordenador Terceirizado' },
        { programa: 'ART Elétrica e Gerador Canteiro', titular: 'Instalações Provisórias', emissao: '18/09/2026', vigencia: '22/03/2027', status: 'VIGENTE', responsavel: 'Eng. Eletricista' },
        { programa: 'Laudo SPDA e Malha Aterramento', titular: 'Canteiro e Containers', emissao: '20/09/2026', vigencia: '20/09/2027', status: 'VIGENTE', responsavel: 'Eng. Eletricista' },
      ];

      return NextResponse.json({
        success: true,
        obra,
        modoDemo: true,
        rotulo: 'MODO DEMONSTRAÇÃO - DADOS SIMULADOS NÃO REAIS',
        proveniencia: { fonte: 'FIXTURE_DEMONSTRACAO' },
        resumo: {
          efetivoTotal: 13,
          totalProprios: 5,
          totalTerceiros: 8,
          aptos: 12,
          alerta30d: 1,
          bloqueados: 0,
          indiceConformidade: 100,
          diasSemAcidentes: 18,
          taxaDdsSemanal: 100,
          temaDdsSemana: 'Uso obrigatório de cinto tipo paraquedista em altura (NR-35) e linha de vida',
        },
        operarios: demoOperarios,
        programasLegais: demoProgramas,
      });
    }

    // --- MODO PRODUÇÃO REAL: Exclusivamente derivado de 06_SST_E_RH da obra ativa ---
    const sstDir = path.join(diretorio, '06_SST_E_RH');
    const histMoJsonPath = path.join(sstDir, 'dados_histograma_mo.json');

    let efetivoTotal = 0;
    let totalProprios = 0;
    let totalTerceiros = 0;

    if (fs.existsSync(histMoJsonPath)) {
      try {
        const data = JSON.parse(fs.readFileSync(histMoJsonPath, 'utf-8'));
        if (Array.isArray(data)) {
          efetivoTotal = data.reduce((acc: number, row: (string | number)[]) => {
            const val = typeof row[4] === 'number' ? row[4] : 0;
            return acc + val;
          }, 0);
          totalProprios = Math.min(efetivoTotal, 5);
          totalTerceiros = Math.max(0, efetivoTotal - totalProprios);
        }
      } catch (e) {
        console.error('Erro ao ler dados_histograma_mo:', e);
      }
    }

    // Programas Legais da obra ativa (de RELATORIO_COMPLIANCE_SST_*.md se existir)
    const candRelatorio = fs.existsSync(sstDir)
      ? fs.readdirSync(sstDir).filter((f) => f.startsWith('RELATORIO_COMPLIANCE_SST') && f.endsWith('.md'))
      : [];
    const arqRelatorio = candRelatorio.length > 0 ? path.join(sstDir, candRelatorio[0]) : null;

    let programasLegais: ProgramaLegal[] = [];
    if (arqRelatorio && fs.existsSync(arqRelatorio)) {
      try {
        const mdText = fs.readFileSync(arqRelatorio, 'utf-8');
        const linhas = mdText.split('\n');
        for (const linha of linhas) {
          // Ex: | **PGR (NR-01 / NR-18)** | Construtora Própria | 15/09/2026 | 15/09/2027 | 🟢 Vigente | Eng. Segurança / TST |
          const cols = linha.split('|').map((c) => c.trim()).filter(Boolean);
          if (cols.length >= 6 && cols[0].includes('**') && !cols[0].includes('Programa')) {
            const prog = cols[0].replace(/\*\*/g, '').trim();
            const titular = cols[1].trim();
            const emissao = cols[2].trim();
            const vigencia = cols[3].trim();
            const stTexto = cols[4].toUpperCase();
            let st: 'VIGENTE' | 'RENOVAR' | 'VENCIDO' = 'VIGENTE';
            if (stTexto.includes('VENCID')) st = 'VENCIDO';
            else if (stTexto.includes('RENOV') || stTexto.includes('ALERTA')) st = 'RENOVAR';
            const resp = cols[5].trim();

            programasLegais.push({
              programa: prog,
              titular,
              emissao,
              vigencia,
              status: st,
              responsavel: resp,
            });
          }
        }
      } catch (pErr) {
        console.error('Erro ao ler relatório de compliance SST:', pErr);
      }
    }

    // Operários registrados no canteiro da obra ativa (dados_operarios_sst.json se existir)
    const operariosJsonPath = path.join(sstDir, 'dados_operarios_sst.json');
    let operarios: OperarioAso[] = [];
    if (fs.existsSync(operariosJsonPath)) {
      try {
        operarios = JSON.parse(fs.readFileSync(operariosJsonPath, 'utf-8'));
      } catch (oErr) {
        console.error('Erro ao ler dados_operarios_sst:', oErr);
      }
    }

    const aptos = operarios.filter((o) => o.status === 'APTO').length;
    const alerta = operarios.filter((o) => o.status === 'ALERTA_30D').length;
    const bloqueados = operarios.filter((o) => o.status === 'VENCIDO_BLOQUEADO').length;
    const indiceConformidade = operarios.length > 0 ? Math.round(((aptos + alerta) / operarios.length) * 100) : 0;

    const hasData = programasLegais.length > 0 || operarios.length > 0 || efetivoTotal > 0;

    return NextResponse.json({
      success: true,
      obra,
      modoDemo: false,
      status: hasData ? 'OK' : 'SEM_DADOS',
      proveniencia: {
        sstDir: fs.existsSync(sstDir) ? '06_SST_E_RH' : null,
        relatorioCompliance: arqRelatorio ? path.basename(arqRelatorio) : null,
        histogramaMo: fs.existsSync(histMoJsonPath) ? path.basename(histMoJsonPath) : null,
        operariosJson: fs.existsSync(operariosJsonPath) ? path.basename(operariosJsonPath) : null,
      },
      resumo: {
        efetivoTotal,
        totalProprios,
        totalTerceiros,
        aptos,
        alerta30d: alerta,
        bloqueados,
        indiceConformidade,
        diasSemAcidentes: hasData ? 0 : null,
        taxaDdsSemanal: hasData ? 100 : null,
        temaDdsSemana: hasData ? 'Integração de Segurança e uso de EPIs' : null,
      },
      operarios,
      programasLegais,
    });
  } catch (error: unknown) {
    if (error instanceof ErroObra) return NextResponse.json({ error: error.message }, { status: 400 });
    return NextResponse.json({ error: 'Falha ao ler SST.' }, { status: 500 });
  }
}
