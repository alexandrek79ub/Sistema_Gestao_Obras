import assert from 'node:assert/strict';
import fs from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const appDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const rootDir = path.resolve(appDir, '..');
const ler = (...partes) => fs.readFileSync(path.join(appDir, ...partes), 'utf8');
const lerRaiz = (...partes) => fs.readFileSync(path.join(rootDir, ...partes), 'utf8');
const require = createRequire(import.meta.url);
const typescript = require('typescript');

function carregarCronogramaService({ parseCSV, existsSync = () => false, readFileSync = () => '' }) {
  const fonte = ler('src/lib/cronogramaService.ts');
  const compilado = typescript.transpileModule(fonte, {
    compilerOptions: {
      module: typescript.ModuleKind.CommonJS,
      target: typescript.ScriptTarget.ES2022,
    },
  }).outputText;
  const moduloCompilado = { exports: {} };
  const carregarModulo = (nome) => {
    if (nome === 'path') return { default: path };
    if (nome === 'fs') return { default: { existsSync, readFileSync } };
    if (nome === '@/lib/csvParser') return { parseCSV };
    throw new Error(`Módulo inesperado: ${nome}`);
  };

  vm.runInNewContext(compilado, { module: moduloCompilado, exports: moduloCompilado.exports, require: carregarModulo, console });
  return moduloCompilado.exports;
}

test('Fase 5 / AUD-013: API de cronograma é thin layer desacoplada delegando para cronogramaService', () => {
  const rotaConteudo = ler('src/app/api/cronograma/route.ts');
  assert.match(
    rotaConteudo,
    /from\s+['"]@\/lib\/cronogramaService['"]/,
    'Rota de cronograma deve importar a lógica de negócio do cronogramaService'
  );
  assert.match(
    rotaConteudo,
    /obterDadosCronograma\(/,
    'Rota de cronograma deve delegar a extração para obterDadosCronograma'
  );
  // Garante que a rota não é mais monolítica (tinha 1254 linhas antes)
  const linhas = rotaConteudo.split('\n').length;
  assert.ok(linhas < 150, `Rota de cronograma deve ser fina (< 150 linhas), atual: ${linhas}`);
});

test('Fase 5 / AUD-013: Tipos de cronograma estão centralizados em types/cronograma.ts', () => {
  const typesConteudo = ler('src/types/cronograma.ts');
  const tiposEsperados = ['TarefaLOB', 'VagaoFluxo', 'PontoVagao', 'CronogramaDados', 'AtividadeCPM'];
  for (const tipo of tiposEsperados) {
    assert.match(
      typesConteudo,
      new RegExp(`export\\s+interface\\s+${tipo}`),
      `types/cronograma.ts deve declarar e exportar a interface ${tipo}`
    );
  }
});

test('Fase 5 / AUD-014: requirements.txt declara as dependências Python dos motores e relatórios', () => {
  const reqConteudo = lerRaiz('requirements.txt');
  const dependenciasEsperadas = ['openpyxl', 'Pillow', 'plotly', 'numpy', 'pandas', 'pymupdf'];
  for (const dep of dependenciasEsperadas) {
    assert.match(
      reqConteudo,
      new RegExp(`^${dep}>=`, 'm'),
      `requirements.txt deve declarar a dependência pinada ${dep}`
    );
  }
});

test('Fase 5 / AUD-014: CI workflow define gates para testes e validações de Python e Frontend', () => {
  const ciConteudo = lerRaiz('.github/workflows/ci.yml');
  assert.match(ciConteudo, /name:\s*CI/, 'Workflow de CI deve estar nomeado');
  assert.match(ciConteudo, /python -m unittest discover -s scripts\/tests/, 'CI deve rodar suite unificada Python');
  assert.match(ciConteudo, /npm run lint/, 'CI deve executar gate de ESLint');
  assert.match(ciConteudo, /npm test/, 'CI deve executar testes automatizados do frontend');
});

test('Fase 5 / regressão: LOB preserva as dependências do commit 141402c', () => {
  const { buildLOBGraph } = carregarCronogramaService({ parseCSV: () => { throw new Error('não utilizado'); } });

  const sobrepostas = buildLOBGraph([
    { LOCAL_PAVIMENTO: 'Zona 01', VAGAO: '01. Fundação', DATA_INICIO: '01/10/2026', DATA_FIM: '03/10/2026' },
    { LOCAL_PAVIMENTO: 'Zona 02', VAGAO: '01. Fundação', DATA_INICIO: '02/10/2026', DATA_FIM: '04/10/2026' },
  ]);
  assert.deepEqual(Array.from(sobrepostas.adj.get(0)), [], 'tarefas sobrepostas do mesmo vagão permanecem em paralelo');

  const comissionamento = buildLOBGraph([
    { LOCAL_PAVIMENTO: 'Zona 01', VAGAO: '01. Fundação', DATA_INICIO: '01/10/2026', DATA_FIM: '03/10/2026' },
    { LOCAL_PAVIMENTO: 'Zona 02', VAGAO: '15. Comissionamento', DATA_INICIO: '04/10/2026', DATA_FIM: '05/10/2026' },
  ]);
  assert.deepEqual(Array.from(comissionamento.adj.get(0)), [], 'comissionamento não recebe dependências implícitas');

  const sequenciais = buildLOBGraph([
    { LOCAL_PAVIMENTO: 'Zona 01', VAGAO: '01. Fundação', DATA_INICIO: '01/10/2026', DATA_FIM: '03/10/2026' },
    { LOCAL_PAVIMENTO: 'Zona 02', VAGAO: '01. Fundação', DATA_INICIO: '03/10/2026', DATA_FIM: '05/10/2026' },
  ]);
  assert.deepEqual(Array.from(sequenciais.adj.get(0)), [1], 'sequência não paralela do mesmo vagão mantém precedência');
});

test('Fase 5 / regressão: erro de parsing do takt é propagado pela API', () => {
  const { obterDadosCronograma } = carregarCronogramaService({
    existsSync: (arquivo) => String(arquivo).includes('LINHA_DE_BALANCO') || String(arquivo).includes('PROGRAMACAO_CURTO_PRAZO_OBRA_TESTE.csv'),
    parseCSV: (arquivo) => String(arquivo).includes('LINHA_DE_BALANCO')
      ? { status: 'empty', data: [], headers: [] }
      : { status: 'invalid_schema', data: [], headers: [], error: 'Cabeçalho inválido' },
  });

  const resultado = obterDadosCronograma('/obras/OBRA_TESTE', 'OBRA_TESTE');
  assert.equal(resultado.ok, false);
  assert.equal(resultado.error, 'Cabeçalho inválido');
  assert.equal(resultado.status, 'invalid_schema');
  assert.equal(resultado.httpStatus, 422);
});

test('Fase 5 / regressão: campos ausentes mantêm o contrato anterior sem defaults novos', () => {
  const { obterDadosCronograma } = carregarCronogramaService({
    existsSync: (arquivo) => String(arquivo).includes('LINHA_DE_BALANCO') || String(arquivo).includes('PROGRAMACAO_CURTO_PRAZO_OBRA_TESTE.csv') || String(arquivo).includes('dados_cpm.json'),
    readFileSync: () => JSON.stringify({ atividades: [{ id: 'A1' }] }),
    parseCSV: (arquivo) => String(arquivo).includes('LINHA_DE_BALANCO')
      ? { status: 'empty', data: [], headers: [] }
      : { status: 'ok', data: [{ DURACAO_DIAS: '2', HEADCOUNT_PREVISTO: '3' }], headers: [] },
  });
  const resultado = obterDadosCronograma('/obras/OBRA_TESTE', 'OBRA_TESTE');

  assert.equal(resultado.ok, true);
  assert.equal(resultado.data.lotesCurtoPrazo[0].codLote, undefined);
  assert.equal(resultado.data.lotesCurtoPrazo[0].semana, undefined);
  assert.equal(resultado.data.lotesCurtoPrazo[0].servico, undefined);
  assert.equal(resultado.data.lotesCurtoPrazo[0].metaFisica, undefined);
  assert.equal(resultado.data.lotesCurtoPrazo[0].equipePrevista, undefined);
  assert.equal(resultado.data.cpm[0].duracao_dias, undefined);
});
