import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const appDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ler = (...partes) => fs.readFileSync(path.join(appDir, ...partes), 'utf8');

test('Fase 4 / AUD-004: Todas as rotas de painéis exigem obra ativa via obterObraObrigatoria', () => {
  const rotas = [
    'src/app/api/evm/route.ts',
    'src/app/api/financeiro/route.ts',
    'src/app/api/qualidade/route.ts',
    'src/app/api/sst/route.ts',
    'src/app/api/databook/route.ts',
  ];

  for (const rota of rotas) {
    const conteudo = ler(rota);
    assert.match(
      conteudo,
      /obterObraObrigatoria\(request\)/,
      `Rota ${rota} deve validar obra obrigatória`
    );
    assert.doesNotMatch(
      conteudo,
      /searchParams\.get\('obra'\)\s*\|\|\s*['"]OBRA_TMULT['"]/,
      `Rota ${rota} não pode ter fallback silencioso para OBRA_TMULT`
    );
  }
});

test('Fase 4 / AUD-004: Modo demonstração só é ativado com parâmetro explícito demo=true', () => {
  const rotas = [
    'src/app/api/evm/route.ts',
    'src/app/api/financeiro/route.ts',
    'src/app/api/qualidade/route.ts',
    'src/app/api/sst/route.ts',
    'src/app/api/databook/route.ts',
  ];

  for (const rota of rotas) {
    const conteudo = ler(rota);
    assert.match(
      conteudo,
      /(?:const\s+demo|const\s+modoDemo)\s*=\s*(?:url\.)?searchParams\.get\('demo'\)\s*===\s*'true'/,
      `Rota ${rota} deve checar parâmetro demo=true explicitamente`
    );
    assert.match(
      conteudo,
      /modoDemo/,
      `Rota ${rota} deve retornar a flag modoDemo no payload`
    );
    assert.match(
      conteudo,
      /proveniencia/,
      `Rota ${rota} deve incluir metadados de proveniência dos dados`
    );
  }
});

test('Fase 4 / AUD-004: Rotas de painel não injetam dados fabricados em produção quando obra não possui medições', () => {
  const evm = ler('src/app/api/evm/route.ts');
  const financeiro = ler('src/app/api/financeiro/route.ts');
  const sst = ler('src/app/api/sst/route.ts');
  const qualidade = ler('src/app/api/qualidade/route.ts');
  const databook = ler('src/app/api/databook/route.ts');

  // EVM não deve mais ter array fixo de semanas simuladas (0.08, 0.20, etc.) no fluxo de produção
  assert.doesNotMatch(evm, /const semanas = \[\s*\{\s*semana: 1,\s*planejado: 0\.08/);

  // Financeiro não deve usar fallback fixo para FLUXO_DE_CAIXA_TMULT.csv
  assert.doesNotMatch(financeiro, /'FLUXO_DE_CAIXA_TMULT\.csv'/);

  // SST não deve inventar lista de 13 operários fixos com ASOs fabricados no fluxo de produção
  assert.doesNotMatch(sst, /const operarios = \[\s*\{\s*id:\s*1,\s*nome:\s*'Severino Lima'/);

  // Qualidade não deve forçar itens como APROVADO sem registro de campo
  assert.match(qualidade, /PENDENTE/);

  // Databook deve ler pastas reais de 07_DATABOOK_E_ASBUILT
  assert.match(databook, /07_DATABOOK_E_ASBUILT/);
});

test('Fase 4 / AUD-004: Páginas do dashboard possuem banner de demonstração e tratam ausência de dados com veracidade', () => {
  const paginas = [
    'src/app/dashboard/page.tsx',
    'src/app/dashboard/financeiro/page.tsx',
    'src/app/dashboard/qualidade/page.tsx',
    'src/app/dashboard/sst/page.tsx',
    'src/app/dashboard/databook/page.tsx',
  ];

  for (const pagina of paginas) {
    const conteudo = ler(pagina);
    assert.match(
      conteudo,
      /modoDemo|Modo de Demonstração|MODO DE DEMONSTRAÇÃO/i,
      `Página ${pagina} deve exibir identificação visual clara de modo demonstração`
    );
  }

  // Dashboard principal não exibe SPI/CPI 1.00 falso quando sem medição
  const mainDash = ler('src/app/dashboard/page.tsx');
  assert.doesNotMatch(mainDash, /evm\?\.spi \|\| 1\.0/);
  assert.doesNotMatch(mainDash, /evm\?\.cpi \|\| 1\.0/);

  // Dashboard financeiro não usa fallback hardcoded com valores da TMULT
  const finDash = ler('src/app/dashboard/financeiro/page.tsx');
  assert.doesNotMatch(finDash, /faturamentoTotal:\s*1660762\.28/);
});
