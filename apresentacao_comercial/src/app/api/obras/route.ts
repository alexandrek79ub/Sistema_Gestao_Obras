import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
  try {
    const projetosPath = process.env.OBRA_PATH 
      ? path.resolve(process.env.OBRA_PATH, '..')
      : path.resolve(process.cwd(), '../projetos');
      
    if (!fs.existsSync(projetosPath)) {
      return NextResponse.json({ obras: ['OBRA'] });
    }

    const pastas = fs.readdirSync(projetosPath, { withFileTypes: true })
      .filter(dirent => dirent.isDirectory())
      .map(dirent => dirent.name);

    const obrasValidas = pastas.filter(pasta => {
      // Verifica se tem a estrutura básica (ex: 02_ORCAMENTO_BASE_E_CONTRATOS)
      const testPath = path.join(projetosPath, pasta, '02_ORCAMENTO_BASE_E_CONTRATOS');
      return fs.existsSync(testPath);
    });

    if (obrasValidas.length === 0) {
      return NextResponse.json({ obras: ['OBRA'] });
    }

    return NextResponse.json({ obras: obrasValidas });
  } catch (error) {
    console.error('Erro ao listar obras', error);
    return NextResponse.json({ obras: ['OBRA'] });
  }
}
