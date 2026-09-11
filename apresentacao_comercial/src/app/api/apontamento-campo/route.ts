import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
  try {
    const payload = await request.json();
    const obra = payload.obra || 'OBRA_TMULT';

    // Caminho da raiz do workspace
    const workspaceRoot = path.resolve(process.cwd(), '..');
    const obraDir = path.join(workspaceRoot, 'projetos', obra);

    if (!fs.existsSync(obraDir)) {
      return NextResponse.json(
        { success: false, error: `Diretório da obra ${obra} não encontrado.` },
        { status: 404 }
      );
    }

    // Criar arquivo temporário de apontamento
    const tempDir = path.join(obraDir, '04_PRODUCAO_E_AVANCO');
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }

    const tempFile = path.join(tempDir, `temp_apontamento_${Date.now()}.json`);
    fs.writeFileSync(tempFile, JSON.stringify(payload, null, 2), 'utf-8');

    // Executar o motor universal em Python
    const scriptPath = path.join(workspaceRoot, 'scripts', 'processar_coleta_campo.py');
    const cmd = `python "${scriptPath}" --obra "${obra}" --arquivo "${tempFile}"`;

    const { stdout } = await execAsync(cmd, { cwd: workspaceRoot });

    // Remover arquivo temporário após processamento
    try {
      if (fs.existsSync(tempFile)) {
        fs.unlinkSync(tempFile);
      }
    } catch {
      // ignore
    }

    return NextResponse.json({
      success: true,
      message: 'Apontamento de campo processado com sucesso!',
      stdout: stdout.trim(),
      tipo: payload.tipo || 'rdo'
    });
  } catch (error: unknown) {
    const errorMsg = error instanceof Error ? error.message : 'Erro interno ao processar apontamento';
    console.error('Erro ao processar apontamento de campo:', error);
    return NextResponse.json(
      {
        success: false,
        error: errorMsg
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    status: 'online',
    service: 'Coleta Digital de Campo 4.0 API',
    endpoints: {
      POST: 'Envia apontamento de RDO ou FVS de campo'
    }
  });
}
