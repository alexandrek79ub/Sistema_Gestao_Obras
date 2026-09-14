import { NextResponse } from 'next/server';
import { ErroObra, obterObraObrigatoria } from '@/lib/obra';
import { obterDadosCronograma } from '@/lib/cronogramaService';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  let obra: string;
  let basePath: string;
  try {
    const res = obterObraObrigatoria(request);
    obra = res.obra;
    basePath = res.diretorio;
  } catch (err) {
    if (err instanceof ErroObra) {
      return NextResponse.json({ error: err.message, status: 'invalid_obra' }, { status: 400 });
    }
    throw err;
  }

  try {
    const resultado = obterDadosCronograma(basePath, obra);
    if (!resultado.ok) {
      return NextResponse.json(
        {
          error: resultado.error,
          status: resultado.status,
          obra,
          tarefas: [],
          pavimentos: [],
        },
        { status: resultado.httpStatus }
      );
    }
    return NextResponse.json(resultado.data);
  } catch (error) {
    console.error('Falha geral no cronograma', error);
    return NextResponse.json(
      {
        error: 'Falha ao processar dados do cronograma',
        details: String(error),
        obra,
        tarefas: [],
        pavimentos: [],
      },
      { status: 500 }
    );
  }
}

export async function POST() {
  return NextResponse.json(
    {
      error: 'Mutações de cronograma não são permitidas pela API do dashboard.',
      detalhe: 'Gere uma proposta pelo agente e execute o motor canônico após a confirmação exigida pela governança.',
    },
    { status: 405 },
  );
}
