import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';

export const dynamic = 'force-dynamic';

export interface PastaDataBook {
  numero: string;
  nome: string;
  descricao: string;
  totalDocumentos: number;
  documentosConcluidos: number;
  status: 'CONCLUIDO' | 'EM_ANDAMENTO' | 'PENDENTE';
  arquivos: { nome: string; status: 'VALIDADO' | 'MINUTA' | 'PENDENTE'; tipo: string }[];
}

export interface GarantiaItem {
  subsistema: string;
  componente: string;
  garantiaLegal: string;
  garantiaRecomendada: string;
  manutencaoPreventiva: string;
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const obra = searchParams.get('obra') || 'OBRA_TMULT';

  const basePath = process.env.OBRA_PATH
    ? process.env.OBRA_PATH.replace(/OBRA$/, obra)
    : path.resolve(process.cwd(), `../projetos/${obra}`);

  const databookDir = path.join(basePath, '07_DATABOOK_E_ASBUILT');

  // Mapeamento das 5 pastas canônicas de Closeout
  const pastas: PastaDataBook[] = [
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
        { nome: 'TERMO_RECEBIMENTO_DEFINITIVO.md', status: 'PENDENTE', tipo: 'Marco D+15 (Libera Retenção)' },
      ],
    },
  ];

  // Matriz de Prazos de Garantia NBR 15575
  const garantiasNbr15575: GarantiaItem[] = [
    {
      subsistema: 'Fundações e Estrutura',
      componente: 'Sapatas, estacas, vigas, pilares e lajes de concreto armado',
      garantiaLegal: '5 anos',
      garantiaRecomendada: '5 anos',
      manutencaoPreventiva: 'Inspeção visual semestral de fissuras e integridade estrutural',
    },
    {
      subsistema: 'Impermeabilização',
      componente: 'Mantas asfálticas, poliuretanos, reservatórios e calhas',
      garantiaLegal: '5 anos',
      garantiaRecomendada: '5 anos',
      manutencaoPreventiva: 'Limpeza trimestral de ralos e desobstrução de calhas; não perfurar',
    },
    {
      subsistema: 'Instalações Hidráulicas',
      componente: 'Tubulações de PVC/PPR embutidas em alvenaria e solo',
      garantiaLegal: '5 anos',
      garantiaRecomendada: '5 anos',
      manutencaoPreventiva: 'Manter pressão dentro dos limites de projeto (pressão máx 40 mca)',
    },
    {
      subsistema: 'Instalações Hidráulicas',
      componente: 'Louças, metais sanitários, sifões e torneiras',
      garantiaLegal: '1 ano',
      garantiaRecomendada: '1 a 2 anos',
      manutencaoPreventiva: 'Limpeza periódica de arejadores; troca de vedações anuais',
    },
    {
      subsistema: 'Instalações Elétricas',
      componente: 'Fiação, barramentos e tubulações embutidas',
      garantiaLegal: '3 anos',
      garantiaRecomendada: '3 anos',
      manutencaoPreventiva: 'Reaperto semestral dos parafusos dos disjuntores no Quadro',
    },
    {
      subsistema: 'Instalações Elétricas',
      componente: 'Disjuntores, interruptores, tomadas e sensores',
      garantiaLegal: '1 ano',
      garantiaRecomendada: '1 ano',
      manutencaoPreventiva: 'Testar botão de teste do IDR mensalmente',
    },
    {
      subsistema: 'Esquadrias de Alumínio',
      componente: 'Perfis de alumínio, anodização e fixações perimetrais',
      garantiaLegal: '5 anos',
      garantiaRecomendada: '5 anos',
      manutencaoPreventiva: 'Limpeza semestral com detergente neutro; nunca usar abrasivos',
    },
    {
      subsistema: 'Esquadrias de Alumínio',
      componente: 'Roldanas, fechos, borrachas de vedação e escovas',
      garantiaLegal: '1 ano',
      garantiaRecomendada: '1 ano',
      manutencaoPreventiva: 'Lubrificação semestral com spray de silicone neutro',
    },
    {
      subsistema: 'Revestimentos Cerâmicos',
      componente: 'Aderência de pisos e azulejos (descolamento)',
      garantiaLegal: '5 anos',
      garantiaRecomendada: '5 anos',
      manutencaoPreventiva: 'Reposição imediata de rejuntes danificados contra umidade',
    },
    {
      subsistema: 'Pintura e Fachadas',
      componente: 'Pintura externa com textura acrílica hidro-repelente',
      garantiaLegal: '2 anos',
      garantiaRecomendada: '3 anos',
      manutencaoPreventiva: 'Lavagem suave anual; repintura a cada 3 anos em ambiente marinho',
    },
    {
      subsistema: 'Pintura Interna',
      componente: 'Látex acrílico/PVA sobre massa corrida',
      garantiaLegal: '1 ano',
      garantiaRecomendada: '1 ano',
      manutencaoPreventiva: 'Não lavar com excesso de água; retoques pontuais pós-impacto',
    },
    {
      subsistema: 'Cobertura e Telhado',
      componente: 'Telhas termoacústicas trapezoidais PIR/EPS e fixações',
      garantiaLegal: '5 anos',
      garantiaRecomendada: '5 anos',
      manutencaoPreventiva: 'Inspeção e limpeza semestral de parafusos autobrocantes e arruelas',
    },
  ];

  const totalDocs = pastas.reduce((acc, p) => acc + p.totalDocumentos, 0);
  const concluidosDocs = pastas.reduce((acc, p) => acc + p.documentosConcluidos, 0);
  const progressoPercent = Math.round((concluidosDocs / totalDocs) * 100);

  return NextResponse.json({
    success: true,
    obra,
    kpis: {
      totalPastas: pastas.length,
      pastasConcluidas: pastas.filter((p) => p.status === 'CONCLUIDO').length,
      totalDocumentos: totalDocs,
      documentosValidados: concluidosDocs,
      progressoCloseout: progressoPercent,
      statusTrp: 'Em Elaboração (D-0)',
      statusTrd: 'Condicionado ao DataBook 100%',
    },
    pastas,
    garantiasNbr15575,
  });
}
