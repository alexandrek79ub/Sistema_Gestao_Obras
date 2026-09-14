import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const appDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const rootDir = path.resolve(appDir, '..');
const ler = (...partes) => fs.readFileSync(path.join(appDir, ...partes), 'utf8');
const lerRaiz = (...partes) => fs.readFileSync(path.join(rootDir, ...partes), 'utf8');

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
