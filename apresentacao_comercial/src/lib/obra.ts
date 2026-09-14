import fs from 'fs';
import path from 'path';

const OBRA_ID = /^[A-Z0-9_]+$/;

export class ErroObra extends Error {}

export function resolverDiretorioProjetos(): string {
  return path.resolve(process.cwd(), '..', 'projetos');
}

export function resolverDiretorioObra(obra: string): string {
  if (!OBRA_ID.test(obra)) throw new ErroObra('Identificador de obra inválido.');
  const projetosDir = resolverDiretorioProjetos();
  const obraDir = path.resolve(projetosDir, obra);
  if (path.dirname(obraDir) !== projetosDir || !fs.statSync(obraDir, { throwIfNoEntry: false })?.isDirectory()) {
    throw new ErroObra('Obra não encontrada.');
  }
  return obraDir;
}

export function obterObraObrigatoria(request: Request): { obra: string; diretorio: string } {
  const obra = new URL(request.url).searchParams.get('obra');
  if (!obra) throw new ErroObra('O parâmetro obra é obrigatório.');
  return { obra, diretorio: resolverDiretorioObra(obra) };
}
