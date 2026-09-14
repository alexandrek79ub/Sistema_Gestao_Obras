import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const appDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

test('Fase 2 / AUD-008: API de cronograma exige obra ativa e não usa fallback para TMULT ou template', () => {
  const cronogramaRoute = fs.readFileSync(path.join(appDir, 'src/app/api/cronograma/route.ts'), 'utf8');

  // Exige obra ativa e trata erro de validação
  assert.match(cronogramaRoute, /obterObraObrigatoria\(request\)/);

  // Não contém fallback de leitura para template de linha de balanço
  assert.doesNotMatch(cronogramaRoute, /TEMPLATE_LINHA_DE_BALANCO\.csv/);

  // Não contém fallbacks cruzados para PROGRAMACAO_CURTO_PRAZO_OBRA_TMULT ou PROGRAMACAO_CURTO_PRAZO_TMULT
  assert.doesNotMatch(cronogramaRoute, /PROGRAMACAO_CURTO_PRAZO_OBRA_TMULT/);
  assert.doesNotMatch(cronogramaRoute, /PROGRAMACAO_CURTO_PRAZO_TMULT/);
  assert.doesNotMatch(cronogramaRoute, /\.\.\/projetos\/OBRA_TMULT\/03_PLANEJAMENTO_E_CRONOGRAMA/);
});

test('Fase 2 / AUD-003: Governança do Índice Mestre e agentes adota 2.1.8 para acabamento e segrega EAP de serviço', () => {
  const rootDir = path.resolve(appDir, '..');
  const indiceMestre = fs.readFileSync(path.join(rootDir, 'governanca/INDICE_MESTRE_SKILLS.md'), 'utf8');
  const agentsMd = fs.readFileSync(path.join(rootDir, 'agents.md'), 'utf8');

  // Portão 4 deve referenciar 2.1.8 (Pintura interna 1ª demão)
  assert.match(indiceMestre, /2\.1\.8 → 3\.1\.9/);
  assert.match(agentsMd, /2\.1\.8 \(1ª Demão de Pintura\)/);

  // Segregação clara de CODIGO_EAP_SERVICO
  assert.match(indiceMestre, /CODIGO_EAP_SERVICO/);
  assert.match(agentsMd, /CODIGO_EAP_SERVICO/);
});
