import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';
import { ErroObra, obterObraObrigatoria } from '@/lib/obra';

export const dynamic = 'force-dynamic';

export interface ArquivoItem {
  nome: string;
  status: 'VALIDADO' | 'MINUTA' | 'PENDENTE';
  tipo: string;
}

export interface PastaDataBook {
  numero: string;
  nome: string;
  descricao: string;
  totalDocumentos: number;
  documentosConcluidos: number;
  status: 'CONCLUIDO' | 'EM_ANDAMENTO' | 'PENDENTE';
  arquivos: ArquivoItem[];
}

export interface GarantiaItem {
  subsistema: string;
  componente: string;
  garantiaLegal: string;
  garantiaRecomendada: string;
  manutencaoPreventiva: string;
}

const PASTAS_CANONICAS = [
  {
    numero: '01',
    dirName: '01_LAUDOS_E_CONTROLE_TECNOLOGICO',
    nome: 'Laudos e Controle Tecnológico',
    descricao: 'Corpos de prova de concreto (NBR 5739), estanqueidade de impermeabilização e laudos de SPDA',
  },
  {
    numero: '02',
    dirName: '02_PROJETOS_ASBUILT',
    nome: 'Projetos As-Built',
    descricao: 'Desenhos técnicos finais com todas as alterações de canteiro homologadas pelos projetistas',
  },
  {
    numero: '03',
    dirName: '03_TERMOS_DE_GARANTIA_E_MANUAIS',
    nome: 'Termos de Garantia e Manuais',
    descricao: 'Manual do Usuário (NBR 14037) e Matriz Oficial de Prazos de Garantia da Norma NBR 15575',
  },
  {
    numero: '04',
    dirName: '04_COMPLIANCE_LEGAL_E_HABITESE',
    nome: 'Compliance Legal e Habite-se',
    descricao: 'Alvarás, Habite-se municipal, AVCB do Corpo de Bombeiros e CND/SERO da Receita Federal',
  },
  {
    numero: '05',
    dirName: '05_TERMOS_DE_RECEBIMENTO_E_ENTREGA',
    nome: 'Termos de Recebimento e Entrega',
    descricao: 'Termo Provisório (TRP), Punch List com vistorias de entrega de chaves e Termo Definitivo (TRD)',
  },
];

const GARANTIAS_NBR15575_PADRAO: GarantiaItem[] = [
  { subsistema: 'Estrutura e Fundações', componente: 'Concreto armado, sapatas e vigas baldrames', garantiaLegal: '5 anos', garantiaRecomendada: '5 anos', manutencaoPreventiva: 'Inspeção visual semestral de fissuras e recalques' },
  { subsistema: 'Impermeabilização', componente: 'Manta asfáltica, argamassa polimérica e caixilhos', garantiaLegal: '5 anos', garantiaRecomendada: '5 anos', manutencaoPreventiva: 'Limpeza anual de ralos e calhas; teste de estanqueidade em reformas' },
  { subsistema: 'Esquadrias de Alumínio', componente: 'Perfis de alumínio anodizado e vidros laminados', garantiaLegal: '5 anos', garantiaRecomendada: '5 anos', manutencaoPreventiva: 'Limpeza semestral com detergente neutro e lubrificação de roldanas' },
  { subsistema: 'Instalações Hidráulicas', componente: 'Tubulações de água fria soldáveis e esgoto sanitário', garantiaLegal: '3 anos', garantiaRecomendada: '5 anos', manutencaoPreventiva: 'Verificação periódica de registros, válvulas e caixa de gordura (3 meses)' },
  { subsistema: 'Instalações Elétricas', componente: 'Cabos antichama, disjuntores DIN e quadros QGBT', garantiaLegal: '3 anos', garantiaRecomendada: '5 anos', manutencaoPreventiva: 'Reaperto anual de conexões elétricas e teste semestral de IDR' },
  { subsistema: 'Revestimentos e Pintura', componente: 'Porcelanatos, argamassas colantes AC-III e pintura acrílica', garantiaLegal: '2 anos', garantiaRecomendada: '3 anos', manutencaoPreventiva: 'Repintura externa a cada 3 anos; lavagem suave sem ácidos' },
  { subsistema: 'Cobertura e Telhado', componente: 'Telhas termoacústicas trapezoidais e calhas metálicas', garantiaLegal: '5 anos', garantiaRecomendada: '5 anos', manutencaoPreventiva: 'Inspeção antes do período de chuvas e reaperto de fixadores' },
];

export async function GET(request: Request) {
  try {
    const { obra, diretorio } = obterObraObrigatoria(request);
    const url = new URL(request.url);
    const demo = url.searchParams.get('demo') === 'true';

    if (demo) {
      const demoPastas: PastaDataBook[] = [
        {
          numero: '01',
          nome: 'Laudos e Controle Tecnológico',
          descricao: 'Corpos de prova de concreto (NBR 5739), estanqueidade de impermeabilização e laudos de SPDA',
          totalDocumentos: 3,
          documentosConcluidos: 2,
          status: 'EM_ANDAMENTO',
          arquivos: [
            { nome: 'TEMPLATE_LAUDO_ROMPIMENTO_CONCRETO.md', status: 'VALIDADO', tipo: 'Laudo Laboratorial' },
            { nome: 'TEMPLATE_LAUDO_ESTANQUEIDADE_IMPERMEABILIZACAO.md', status: 'MINUTA', tipo: 'Ensaio 72h' },
            { nome: 'TEMPLATE_LAUDO_SPDA_E_ATERRAMENTO.md', status: 'VALIDADO', tipo: 'Laudo Elétrico c/ ART' },
          ],
        },
        {
          numero: '02',
          nome: 'Projetos As-Built',
          descricao: 'Desenhos técnicos finais com todas as alterações de canteiro homologadas pelos projetistas',
          totalDocumentos: 4,
          documentosConcluidos: 2,
          status: 'EM_ANDAMENTO',
          arquivos: [
            { nome: 'ASBUILT_ARQUITETURA_REV_FINAL.pdf', status: 'VALIDADO', tipo: 'Projeto Arquitetônico' },
            { nome: 'ASBUILT_ESTRUTURAL_FUNDACOES.pdf', status: 'VALIDADO', tipo: 'Projeto Estrutural' },
            { nome: 'ASBUILT_INSTALACOES_HIDRAULICAS.dwg', status: 'MINUTA', tipo: 'Rede Hidrossanitária' },
            { nome: 'ASBUILT_INSTALACOES_ELETRICAS_SPDA.dwg', status: 'MINUTA', tipo: 'Diagrama Unifilar e SPDA' },
          ],
        },
        {
          numero: '03',
          nome: 'Termos de Garantia e Manuais',
          descricao: 'Manual do Usuário (NBR 14037) e Matriz Oficial de Prazos de Garantia da Norma NBR 15575',
          totalDocumentos: 3,
          documentosConcluidos: 3,
          status: 'CONCLUIDO',
          arquivos: [
            { nome: 'MATRIZ_PRAZOS_GARANTIA_NBR15575.md', status: 'VALIDADO', tipo: 'Matriz Normativa' },
            { nome: 'MANUAL_DE_USO_OPERACAO_E_MANUTENCAO.md', status: 'VALIDADO', tipo: 'Manual do Proprietário' },
            { nome: 'CERTIFICADOS_GARANTIA_EQUIPAMENTOS_HVAC.pdf', status: 'VALIDADO', tipo: 'Garantia Fabril' },
          ],
        },
        {
          numero: '04',
          nome: 'Compliance Legal e Habite-se',
          descricao: 'Alvarás, Habite-se municipal, AVCB do Corpo de Bombeiros e CND/SERO da Receita Federal',
          totalDocumentos: 4,
          documentosConcluidos: 1,
          status: 'EM_ANDAMENTO',
          arquivos: [
            { nome: 'ALVARA_DE_CONSTRUCAO_MUNICIPAL.pdf', status: 'VALIDADO', tipo: 'Licença Inicial' },
            { nome: 'AVCB_CORPO_DE_BOMBEIROS.pdf', status: 'PENDENTE', tipo: 'Segurança Contra Pânico' },
            { nome: 'CERTIDAO_DE_HABITE_SE_PREFEITURA.pdf', status: 'PENDENTE', tipo: 'Conclusão Legal' },
            { nome: 'CND_PREVIDENCIARIA_OBRA_SERO.pdf', status: 'PENDENTE', tipo: 'Receita Federal' },
          ],
        },
        {
          numero: '05',
          nome: 'Termos de Recebimento e Entrega',
          descricao: 'Termo Provisório (TRP), Punch List com vistorias de entrega de chaves e Termo Definitivo (TRD)',
          totalDocumentos: 3,
          documentosConcluidos: 1,
          status: 'EM_ANDAMENTO',
          arquivos: [
            { nome: 'CHECKLIST_VISTORIA_DE_ENTREGA_CHAVES.md', status: 'VALIDADO', tipo: 'Punch List de Campo' },
            { nome: 'TERMO_RECEBIMENTO_PROVISORIO.md', status: 'MINUTA', tipo: 'Marco D-0' },
            { nome: 'TERMO_RECEBIMENTO_DEFINITIVO.md', status: 'PENDENTE', tipo: 'Marco D+90' },
          ],
        },
      ];

      return NextResponse.json({
        success: true,
        obra,
        modoDemo: true,
        rotulo: 'MODO DEMONSTRAÇÃO - DADOS SIMULADOS NÃO REAIS',
        proveniencia: { fonte: 'FIXTURE_DEMONSTRACAO' },
        kpis: {
          totalPastas: 5,
          pastasConcluidas: 1,
          totalDocumentos: 17,
          documentosValidados: 9,
          progressoCloseout: 53,
          statusTrp: 'MINUTA (D-0)',
          statusTrd: 'PENDENTE (D+90)',
        },
        pastas: demoPastas,
        garantiasNbr15575: GARANTIAS_NBR15575_PADRAO,
      });
    }

    // --- MODO PRODUÇÃO REAL: Escanear exclusivamente arquivos em 07_DATABOOK_E_ASBUILT ---
    const databookDir = path.join(diretorio, '07_DATABOOK_E_ASBUILT');
    const databookExiste = fs.existsSync(databookDir);

    const pastas: PastaDataBook[] = PASTAS_CANONICAS.map((spec) => {
      const folderPath = path.join(databookDir, spec.dirName);
      if (!databookExiste || !fs.existsSync(folderPath)) {
        return {
          numero: spec.numero,
          nome: spec.nome,
          descricao: spec.descricao,
          totalDocumentos: 0,
          documentosConcluidos: 0,
          status: 'PENDENTE',
          arquivos: [],
        };
      }

      let fileNames: string[] = [];
      try {
        fileNames = fs.readdirSync(folderPath).filter((f) => {
          try {
            return fs.statSync(path.join(folderPath, f)).isFile();
          } catch {
            return false;
          }
        });
      } catch (err) {
        console.error(`Erro ao ler pasta ${spec.dirName}:`, err);
      }

      const arquivos: ArquivoItem[] = fileNames.map((nome) => {
        let st: 'VALIDADO' | 'MINUTA' | 'PENDENTE' = 'VALIDADO';
        if (nome.startsWith('TEMPLATE_') || nome.includes('MINUTA') || nome.includes('RASCUNHO')) {
          st = 'MINUTA';
        }

        let tipo = 'Documento';
        if (nome.endsWith('.pdf')) tipo = 'Documento Final Homologado';
        else if (nome.endsWith('.dwg')) tipo = 'Projeto Executivo CAD';
        else if (nome.endsWith('.xlsx')) tipo = 'Planilha de Controle';
        else if (nome.endsWith('.md')) tipo = 'Laudo / Termo Técnico';

        return { nome, status: st, tipo };
      });

      const totalDocs = arquivos.length;
      const validados = arquivos.filter((a) => a.status === 'VALIDADO').length;
      let statusPasta: 'CONCLUIDO' | 'EM_ANDAMENTO' | 'PENDENTE' = 'PENDENTE';
      if (totalDocs > 0) {
        statusPasta = validados === totalDocs ? 'CONCLUIDO' : 'EM_ANDAMENTO';
      }

      return {
        numero: spec.numero,
        nome: spec.nome,
        descricao: spec.descricao,
        totalDocumentos: totalDocs,
        documentosConcluidos: validados,
        status: statusPasta,
        arquivos,
      };
    });

    const totalDocumentos = pastas.reduce((acc, p) => acc + p.totalDocumentos, 0);
    const documentosValidados = pastas.reduce((acc, p) => acc + p.documentosConcluidos, 0);
    const pastasConcluidas = pastas.filter((p) => p.status === 'CONCLUIDO').length;
    const progresso = totalDocumentos > 0 ? Math.round((documentosValidados / totalDocumentos) * 100) : 0;

    const pasta05 = pastas[4];
    const arqTrp = pasta05?.arquivos.find((a) => a.nome.includes('PROVISORIO'));
    const statusTrp = arqTrp ? (arqTrp.status === 'VALIDADO' ? 'EMITIDO' : 'MINUTA') : 'PENDENTE';

    const arqTrd = pasta05?.arquivos.find((a) => a.nome.includes('DEFINITIVO'));
    const statusTrd = arqTrd ? (arqTrd.status === 'VALIDADO' ? 'EMITIDO' : 'MINUTA') : 'PENDENTE';

    return NextResponse.json({
      success: true,
      obra,
      modoDemo: false,
      status: totalDocumentos > 0 ? 'OK' : 'SEM_DADOS',
      proveniencia: {
        databookDir: databookExiste ? '07_DATABOOK_E_ASBUILT' : null,
        arquivosReaisEncontrados: totalDocumentos,
      },
      kpis: {
        totalPastas: 5,
        pastasConcluidas,
        totalDocumentos,
        documentosValidados,
        progressoCloseout: progresso,
        statusTrp,
        statusTrd,
      },
      pastas,
      garantiasNbr15575: GARANTIAS_NBR15575_PADRAO,
    });
  } catch (error: unknown) {
    if (error instanceof ErroObra) return NextResponse.json({ error: error.message }, { status: 400 });
    return NextResponse.json({ error: 'Falha ao ler databook.' }, { status: 500 });
  }
}
