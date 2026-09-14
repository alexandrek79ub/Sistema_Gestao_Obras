import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const appDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ler = (...partes) => fs.readFileSync(path.join(appDir, ...partes), 'utf-8');

test('cronograma bloqueia POST antes da implementação legada', () => {
  const rota = ler('src', 'app', 'api', 'cronograma', 'route.ts');
  assert.match(rota, /export async function POST\(\) \{\s+return NextResponse\.json\([\s\S]*?status: 405/s);
  assert.doesNotMatch(rota, /projetos\/OBRA_TMULT\/03_PLANEJAMENTO_E_CRONOGRAMA\/LINHA_DE_BALANCO\.csv/);
});

test('coleta de campo só grava submissão em staging, sem shell ou motor', () => {
  const rota = ler('src', 'app', 'api', 'apontamento-campo', 'route.ts');
  const staging = ler('src', 'lib', 'campoStaging.ts');
  assert.doesNotMatch(rota, /child_process|processar_coleta_campo|execAsync/);
  assert.match(staging, /STAGING_CAMPO/);
  assert.match(staging, /flag: 'wx'/);
  assert.match(staging, /status: 'SUBMETIDA'/);
});

test('FVS submetida não é promovida pelo dashboard nem pelo processador', () => {
  const qualidade = ler('src', 'app', 'api', 'qualidade', 'route.ts');
  const processador = ler('..', 'scripts', 'processar_coleta_campo.py');
  assert.doesNotMatch(qualidade, /fvsMatch\.status\s*=\s*'APROVADO'/);
  assert.match(processador, /"status": "SUBMETIDA"/);
  assert.match(processador, /"parecer": "PENDENTE_ANALISE_GOVERNADA"/);
});
