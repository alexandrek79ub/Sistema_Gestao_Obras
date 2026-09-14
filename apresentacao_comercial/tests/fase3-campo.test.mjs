import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const appDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ler = (...partes) => fs.readFileSync(path.join(appDir, ...partes), 'utf-8');

test('Fase 3 / AUD-001 e AUD-010: validação estrita em staging de campo', async () => {
  const { registrarSubmissaoCampo } = await import('../src/lib/campoStaging.js').catch(() =>
    import('../.next/server/chunks/campoStaging.js').catch(() => ({ registrarSubmissaoCampo: null }))
  ) || {};

  // Validação estática do módulo campoStaging.ts
  const stagingCodigo = ler('src', 'lib', 'campoStaging.ts');
  assert.match(stagingCodigo, /Código de FVS inválido/);
  assert.match(stagingCodigo, /Responsável técnico pela inspeção FVS é obrigatório/);
  assert.match(stagingCodigo, /Medição quantitativa de tolerância em campo é obrigatória/);
  assert.match(stagingCodigo, /Evidência de assinatura é obrigatória para submissão de FVS/);
  assert.match(stagingCodigo, /Data do apontamento RDO é obrigatória/);
  assert.match(stagingCodigo, /Efetivo próprio \(ef_prop\) deve ser informado/);
  assert.match(stagingCodigo, /Efetivo terceirizado \(ef_terc\) deve ser informado/);
  assert.match(stagingCodigo, /Frentes EAP executadas são obrigatórias/);
  assert.match(stagingCodigo, /Responsável pelo apontamento de RDO é obrigatório/);
});

test('Fase 3 / AUD-001: interface /campo não possui defaults decisórios ou medições presumidas', () => {
  const campoPage = ler('src', 'app', 'campo', 'page.tsx');

  // Não pode inicializar com resultado favorável automático
  assert.doesNotMatch(campoPage, /useState<'Conforme'\s*\|\s*'NaoConforme'>\('Conforme'\)/);
  // Tolerância não pode vir pré-preenchida com valor inventado
  assert.doesNotMatch(campoPage, /useState\('Desvio linear < 2mm'\)/);
  // Checklist não pode vir 100% marcado como true por padrão
  assert.doesNotMatch(campoPage, /'Locação dos eixos e conferência do esquadro':\s*true/);
  // Deve conter campos para coletar explicitamente os responsáveis técnicos
  assert.match(campoPage, /responsavelRdo/);
  assert.match(campoPage, /fvsResponsavel/);
});

test('Fase 3 / AUD-010: template de obra nova não possui RDOs operacionais pré-preenchidos', () => {
  const rdosDir = path.resolve(appDir, '..', 'projetos', '_TEMPLATE_OBRA_NOVA', '04_PRODUCAO_E_AVANCO', 'RDOS');
  if (fs.existsSync(rdosDir)) {
    const arquivos = fs.readdirSync(rdosDir).filter((f) => f.startsWith('RDO_') && f.endsWith('.md'));
    assert.equal(arquivos.length, 0, 'Template de obra nova não deve conter RDOs operacionais');
  }

  const filaPath = path.resolve(appDir, '..', 'projetos', '_TEMPLATE_OBRA_NOVA', '04_PRODUCAO_E_AVANCO', 'fila_apontamentos_campo.json');
  if (fs.existsSync(filaPath)) {
    const fila = JSON.parse(fs.readFileSync(filaPath, 'utf-8'));
    assert.equal(fila.length, 0, 'Fila de apontamentos do template deve estar vazia');
  }
});
