import fs from 'fs';

export type CsvStatus = 'ok' | 'empty' | 'not_found' | 'invalid_encoding' | 'invalid_schema';

export interface CsvParseResult<T> {
  status: CsvStatus;
  data: T[];
  headers: string[];
  error?: string;
}

export interface CsvSchema {
  requiredHeaders?: string[];
  requiredHeaderGroups?: string[][];
}

function resultado<T>(status: CsvStatus, data: T[] = [], headers: string[] = [], error?: string): CsvParseResult<T> {
  return { status, data, headers, error };
}

function parseRegistros(conteudo: string): string[][] {
  const registros: string[][] = [];
  let registro: string[] = [];
  let campo = '';
  let entreAspas = false;

  for (let indice = 0; indice < conteudo.length; indice += 1) {
    const caractere = conteudo[indice];
    if (entreAspas) {
      if (caractere === '"' && conteudo[indice + 1] === '"') {
        campo += '"';
        indice += 1;
      } else if (caractere === '"') {
        entreAspas = false;
      } else {
        campo += caractere;
      }
      continue;
    }

    if (caractere === '"') {
      if (campo.length > 0) throw new Error('Aspas fora de posição em campo CSV.');
      entreAspas = true;
    } else if (caractere === ';') {
      registro.push(campo);
      campo = '';
    } else if (caractere === '\n') {
      registro.push(campo.replace(/\r$/, ''));
      registros.push(registro);
      registro = [];
      campo = '';
    } else {
      campo += caractere;
    }
  }

  if (entreAspas) throw new Error('Aspas não encerradas em CSV.');
  if (campo.length > 0 || registro.length > 0) {
    registro.push(campo.replace(/\r$/, ''));
    registros.push(registro);
  }
  return registros.filter((linha) => linha.some((valor) => valor !== ''));
}

export function parseCSV<T = Record<string, string>>(absolutePath: string, schema: CsvSchema = {}): CsvParseResult<T> {
  let buffer: Buffer;
  try {
    buffer = fs.readFileSync(absolutePath);
  } catch (error: unknown) {
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') return resultado('not_found', [], [], 'Arquivo CSV não encontrado.');
    return resultado('invalid_schema', [], [], 'Não foi possível ler o arquivo CSV.');
  }

  let conteudo: string;
  try {
    conteudo = new TextDecoder('utf-8', { fatal: true }).decode(buffer);
  } catch {
    return resultado('invalid_encoding', [], [], 'O arquivo não está codificado em UTF-8 válido.');
  }
  if (conteudo.includes('\u0000')) return resultado('invalid_encoding', [], [], 'O arquivo contém bytes incompatíveis com UTF-8.');

  let registros: string[][];
  try {
    registros = parseRegistros(conteudo);
  } catch (error: unknown) {
    return resultado('invalid_schema', [], [], error instanceof Error ? error.message : 'CSV inválido.');
  }
  if (registros.length === 0) return resultado('empty');

  const headers = registros[0].map((header) => header.trim());
  if (headers.length < 2 || headers.some((header) => header.length === 0) || new Set(headers).size !== headers.length) {
    return resultado('invalid_schema', [], headers, 'Cabeçalho CSV inválido ou separador diferente de ponto e vírgula.');
  }
  if (schema.requiredHeaders?.some((header) => !headers.includes(header))) {
    return resultado('invalid_schema', [], headers, 'Cabeçalho CSV não contém todas as colunas obrigatórias.');
  }
  if (schema.requiredHeaderGroups?.some((grupo) => !grupo.some((header) => headers.includes(header)))) {
    return resultado('invalid_schema', [], headers, 'Cabeçalho CSV não atende ao contrato de dados aceito.');
  }

  const data: T[] = [];
  for (const valores of registros.slice(1)) {
    if (valores.length > headers.length) return resultado('invalid_schema', [], headers, 'Linha CSV contém mais campos que o cabeçalho.');
    const row: Record<string, string> = {};
    headers.forEach((header, indice) => {
      row[header] = valores[indice] ?? '';
    });
    data.push(row as T);
  }
  return resultado(data.length === 0 ? 'empty' : 'ok', data, headers);
}
