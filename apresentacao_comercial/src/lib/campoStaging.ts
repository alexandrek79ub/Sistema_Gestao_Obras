import crypto from 'crypto';
import fs from 'fs';
import path from 'path';

const TIPOS_COLETA = new Set(['rdo', 'fvs']);
const CHAVES_COMUNS = new Set(['obra', 'tipo', 'idempotencyKey']);
const CHAVES_RDO = new Set([
  'data',
  'clima_m',
  'clima_t',
  'h_paral',
  'ef_prop',
  'ef_terc',
  'hh',
  'eap',
  'fvs',
  'fvs_status',
  'obs',
  'responsavel',
  'assinatura',
  'engenheiro',
  'mestre',
]);
const CHAVES_FVS = new Set([
  'codigo',
  'data',
  'status',
  'responsavel',
  'medicao_tolerancia',
  'itens_conferidos',
  'observacoes',
  'assinatura',
]);

export type TipoColeta = 'rdo' | 'fvs';

export interface SubmissaoCampo {
  id: string;
  status: 'SUBMETIDA';
  obra: string;
  tipo: TipoColeta;
  recebidaEm: string;
  dados: Record<string, unknown>;
}

function garantirObjeto(valor: unknown): asserts valor is Record<string, unknown> {
  if (!valor || typeof valor !== 'object' || Array.isArray(valor)) throw new Error('Payload de coleta inválido.');
}

function resolverDiretorioObra(obra: unknown): string {
  if (typeof obra !== 'string' || !/^[A-Z0-9_]+$/.test(obra)) throw new Error('Identificador de obra inválido.');
  const projetosDir = path.resolve(process.cwd(), '..', 'projetos');
  const obraDir = path.resolve(projetosDir, obra);
  if (path.dirname(obraDir) !== projetosDir || !fs.statSync(obraDir, { throwIfNoEntry: false })?.isDirectory()) {
    throw new Error('Obra não encontrada.');
  }
  return obraDir;
}

function validarPayload(payload: Record<string, unknown>): { obra: string; tipo: TipoColeta; chave: string } {
  const tipo = payload.tipo;
  if (typeof tipo !== 'string' || !TIPOS_COLETA.has(tipo)) throw new Error('Tipo de coleta inválido.');
  const chave = payload.idempotencyKey;
  if (typeof chave !== 'string' || !/^[a-f0-9-]{36}$/i.test(chave)) throw new Error('Chave de submissão inválida.');

  const permitidas = tipo === 'rdo' ? CHAVES_RDO : CHAVES_FVS;
  for (const [chavePayload, valor] of Object.entries(payload)) {
    if (!CHAVES_COMUNS.has(chavePayload) && !permitidas.has(chavePayload)) throw new Error(`Campo não permitido na coleta: ${chavePayload}.`);
    if (typeof valor === 'object' && !Array.isArray(valor) && valor !== null) throw new Error(`Formato inválido para o campo: ${chavePayload}.`);
  }

  // Validações de campos obrigatórios mínimos de integridade (Fase 3 / AUD-001 e AUD-010)
  if (tipo === 'fvs') {
    if (!payload.codigo || typeof payload.codigo !== 'string' || !/^FVS-0[1-8]$/i.test(payload.codigo.trim())) {
      throw new Error('Código de FVS inválido. Permitidos: FVS-01 a FVS-08.');
    }
    if (!payload.responsavel || typeof payload.responsavel !== 'string' || !payload.responsavel.trim()) {
      throw new Error('Responsável técnico pela inspeção FVS é obrigatório.');
    }
    if (!payload.medicao_tolerancia || typeof payload.medicao_tolerancia !== 'string' || !payload.medicao_tolerancia.trim()) {
      throw new Error('Medição quantitativa de tolerância em campo é obrigatória.');
    }
    if (!payload.assinatura || typeof payload.assinatura !== 'string' || payload.assinatura.trim().toLowerCase() === 'pendente') {
      throw new Error('Evidência de assinatura é obrigatória para submissão de FVS.');
    }
  } else if (tipo === 'rdo') {
    if (!payload.data || typeof payload.data !== 'string' || !payload.data.trim()) {
      throw new Error('Data do apontamento RDO é obrigatória.');
    }
    if (payload.ef_prop === undefined || payload.ef_prop === null || typeof payload.ef_prop !== 'number') {
      throw new Error('Efetivo próprio (ef_prop) deve ser informado numericamente.');
    }
    if (payload.ef_terc === undefined || payload.ef_terc === null || typeof payload.ef_terc !== 'number') {
      throw new Error('Efetivo terceirizado (ef_terc) deve ser informado numericamente.');
    }
    if (!payload.eap || typeof payload.eap !== 'string' || !payload.eap.trim()) {
      throw new Error('Frentes EAP executadas são obrigatórias no RDO.');
    }
    const resp = payload.responsavel || payload.engenheiro;
    if (!resp || typeof resp !== 'string' || !resp.trim()) {
      throw new Error('Responsável pelo apontamento de RDO é obrigatório.');
    }
  }

  return { obra: String(payload.obra), tipo: tipo as TipoColeta, chave };
}

export function registrarSubmissaoCampo(payloadBruto: unknown): { submissao: SubmissaoCampo; duplicada: boolean } {
  garantirObjeto(payloadBruto);
  const { obra, tipo, chave } = validarPayload(payloadBruto);
  const obraDir = resolverDiretorioObra(obra);
  const stagingDir = path.join(obraDir, '04_PRODUCAO_E_AVANCO', 'STAGING_CAMPO');
  fs.mkdirSync(stagingDir, { recursive: true });
  const caminho = path.join(stagingDir, `${chave}.json`);

  if (fs.existsSync(caminho)) return { submissao: JSON.parse(fs.readFileSync(caminho, 'utf-8')) as SubmissaoCampo, duplicada: true };

  const dados = Object.fromEntries(
    Object.entries(payloadBruto).filter(([chavePayload]) => !CHAVES_COMUNS.has(chavePayload)),
  );
  const submissao: SubmissaoCampo = { id: crypto.randomUUID(), status: 'SUBMETIDA', obra, tipo, recebidaEm: new Date().toISOString(), dados };
  try {
    fs.writeFileSync(caminho, JSON.stringify(submissao, null, 2), { encoding: 'utf-8', flag: 'wx' });
    return { submissao, duplicada: false };
  } catch (erro: unknown) {
    if ((erro as NodeJS.ErrnoException).code === 'EEXIST') {
      return { submissao: JSON.parse(fs.readFileSync(caminho, 'utf-8')) as SubmissaoCampo, duplicada: true };
    }
    throw erro;
  }
}
