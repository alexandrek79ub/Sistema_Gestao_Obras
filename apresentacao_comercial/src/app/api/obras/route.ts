import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    const projetosPath = process.env.OBRA_PATH 
      ? path.resolve(process.env.OBRA_PATH, '..')
      : path.resolve(process.cwd(), '../projetos');
      
    if (!fs.existsSync(projetosPath)) {
      return NextResponse.json({ obras: ['OBRA_TMULT'] });
    }

    const itens = fs.readdirSync(projetosPath);
    const pastas = itens.filter(item => {
      try {
        return fs.statSync(path.join(projetosPath, item)).isDirectory();
      } catch {
        return false;
      }
    });

    const obrasValidas = pastas.filter(pasta => {
      const testPath = path.join(projetosPath, pasta, '02_ORCAMENTO_BASE_E_CONTRATOS');
      return fs.existsSync(testPath);
    });

    if (obrasValidas.length === 0) {
      return NextResponse.json({ obras: ['OBRA_TMULT'] });
    }

    return NextResponse.json({ obras: obrasValidas });
  } catch (error) {
    console.error('Erro ao listar obras', error);
    return NextResponse.json({ obras: ['OBRA_TMULT'] });
  }
}
