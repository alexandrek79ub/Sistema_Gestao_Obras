import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const appDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

function carregarParser() {
  const diretorio = fs.mkdtempSync(path.join(os.tmpdir(), 'a11-csv-parser-'));
  try {
    execFileSync(process.execPath, [path.join(appDir, 'node_modules', 'typescript', 'lib', 'tsc.js'),
      'src/lib/csvParser.ts', '--target', 'es2022', '--module', 'commonjs', '--esModuleInterop', '--skipLibCheck', '--outDir', diretorio,
    ], { cwd: appDir, stdio: 'pipe' });
    return createRequire(import.meta.url)(path.join(diretorio, 'csvParser.js'));
  } finally {
    // O módulo já foi carregado; a remoção evita reter artefatos de teste.
    setImmediate(() => fs.rmSync(diretorio, { recursive: true, force: true }));
  }
}

test('parser CSV preserva campos citados, aspas e quebras internas', () => {
  const { parseCSV } = carregarParser();
  const diretorio = fs.mkdtempSync(path.join(os.tmpdir(), 'a11-csv-fixture-'));
  const arquivo = path.join(diretorio, 'complexo.csv');
  fs.writeFileSync(arquivo, '\uFEFFCIA;SERVICO;CUSTO_TOTAL\nA-01;"Serviço; com ""aspas""\ne quebra";12,50\n', 'utf8');
  const resultado = parseCSV(arquivo, { requiredHeaders: ['CIA', 'SERVICO', 'CUSTO_TOTAL'] });
  assert.equal(resultado.status, 'ok');
  assert.equal(resultado.data[0].SERVICO, 'Serviço; com "aspas"\ne quebra');
  fs.rmSync(diretorio, { recursive: true, force: true });
});

test('parser CSV distingue ausência, vazio, encoding inválido e schema inválido', () => {
  const { parseCSV } = carregarParser();
  const diretorio = fs.mkdtempSync(path.join(os.tmpdir(), 'a11-csv-status-'));
  const vazio = path.join(diretorio, 'vazio.csv');
  const invalido = path.join(diretorio, 'invalido.csv');
  const schema = path.join(diretorio, 'schema.csv');
  fs.writeFileSync(vazio, 'CIA;SERVICO\n', 'utf8');
  fs.writeFileSync(invalido, Buffer.from([0xff, 0xfe]));
  fs.writeFileSync(schema, 'CIA;SERVICO\nA;Teste\n', 'utf8');
  assert.equal(parseCSV(path.join(diretorio, 'ausente.csv')).status, 'not_found');
  assert.equal(parseCSV(vazio).status, 'empty');
  assert.equal(parseCSV(invalido).status, 'invalid_encoding');
  assert.equal(parseCSV(schema, { requiredHeaders: ['CUSTO_TOTAL'] }).status, 'invalid_schema');
  fs.rmSync(diretorio, { recursive: true, force: true });
});

test('Fase 1 exige obra na API e não usa fallback cruzado em EVM e orçamento', () => {
  const ler = (arquivo) => fs.readFileSync(path.join(appDir, arquivo), 'utf8');
  const orcamento = ler('src/app/api/orcamento/route.ts');
  const evm = ler('src/app/api/evm/route.ts');
  const contexto = ler('src/context/ObraContext.tsx');
  assert.match(orcamento, /obterObraObrigatoria\(request\)/);
  assert.match(evm, /obterObraObrigatoria\(request\)/);
  assert.doesNotMatch(evm, /searchParams\.get\('obra'\) \|\|/);
  assert.doesNotMatch(contexto, /OBRA_TMULT|RESIDENCIAL_ALPHA/);
});
