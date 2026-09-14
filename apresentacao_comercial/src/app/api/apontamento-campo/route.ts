import { NextRequest, NextResponse } from 'next/server';
import { registrarSubmissaoCampo } from '@/lib/campoStaging';

export async function POST(request: NextRequest) {
  try {
    const resultado = registrarSubmissaoCampo(await request.json());
    return NextResponse.json({
      success: true,
      status: 'SUBMETIDA',
      duplicate: resultado.duplicada,
      message: 'Apontamento recebido para análise. Nenhum registro oficial foi alterado.',
      submissao: resultado.submissao,
    });
  } catch (error: unknown) {
    const errorMsg = error instanceof Error ? error.message : 'Erro interno ao receber apontamento';
    return NextResponse.json(
      { success: false, error: errorMsg },
      { status: errorMsg.includes('Obra não encontrada') ? 404 : 400 },
    );
  }
}

export async function GET() {
  return NextResponse.json({
    status: 'online',
    service: 'Coleta Digital de Campo 4.0 API',
    endpoints: { POST: 'Recebe apontamento de RDO ou FVS em staging' },
  });
}
