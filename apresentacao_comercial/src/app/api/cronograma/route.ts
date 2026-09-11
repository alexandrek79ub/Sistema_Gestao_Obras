import { NextResponse } from 'next/server';
import { parseCSV } from '@/lib/csvParser';
import path from 'path';
import fs from 'fs';
import { execSync } from 'child_process';

export const dynamic = 'force-dynamic';

function parseDateRobust(dateStr: string): Date | null {
  if (!dateStr) return null;
  const clean = dateStr.trim().replace(/^"|"$/g, '');
  
  if (clean.includes('/')) {
    const parts = clean.split('/');
    if (parts.length === 3) {
      const [d, m, y] = parts;
      const fullYear = y.length === 2 ? `20${y}` : y;
      return new Date(parseInt(fullYear, 10), parseInt(m, 10) - 1, parseInt(d, 10));
    }
  } else if (clean.includes('-')) {
    const parts = clean.split('-');
    if (parts.length === 3) {
      const [y, m, d] = parts;
      return new Date(parseInt(y, 10), parseInt(m, 10) - 1, parseInt(d, 10));
    }
  }
  return null;
}

function formatDateBR(d: Date): string {
  const day = String(d.getDate()).padStart(2, '0');
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const year = d.getFullYear();
  return `${day}/${month}/${year}`;
}

function addWorkingDays(date: Date, days: number): Date {
  const current = new Date(date);
  if (days === 0) return current;
  let added = 0;
  const step = days >= 0 ? 1 : -1;
  const absDays = Math.abs(days);
  while (added < absDays) {
    current.setDate(current.getDate() + step);
    if (current.getDay() !== 0) { // Pula Domingos
      added++;
    }
  }
  return current;
}

function calculateWorkingEndDate(startDate: Date, durationDays: number): Date {
  if (durationDays <= 1) return new Date(startDate);
  return addWorkingDays(startDate, durationDays - 1);
}

function countWorkingDaysBetween(startDate: Date, endDate: Date): number {
  const d1 = new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate());
  const d2 = new Date(endDate.getFullYear(), endDate.getMonth(), endDate.getDate());
  if (d1.getTime() === d2.getTime()) return 0;
  
  const isForward = d2 > d1;
  const step = isForward ? 1 : -1;
  const current = new Date(d1);
  let count = 0;
  
  while (
    (isForward && current < d2) ||
    (!isForward && current > d2)
  ) {
    current.setDate(current.getDate() + step);
    if (current.getDay() !== 0) {
      count += step;
    }
  }
  return count;
}

function getVagaoMacroIndex(vagaoNome: string): number {
  const v = (vagaoNome || '').trim();
  const num = parseInt(v.slice(0, 2), 10);
  if (!isNaN(num)) return num;
  if (v.includes('Topografia') || v.includes('Canteiro')) return 1;
  if (v.includes('Fundaç') || v.includes('Sapata')) return 2;
  if (v.includes('Baldrame')) return 3;
  if (v.includes('Pilar')) return 4;
  if (v.includes('Laje') || v.includes('Viga')) return 5;
  if (v.includes('Alvenaria') || v.includes('Vedação')) return 6;
  if (v.includes('Cobertura') || v.includes('Metálica')) return 7;
  if (v.includes('Instalaç') || v.includes('Embutida')) return 8;
  if (v.includes('Reboco') || v.includes('Chapisco') || v.includes('Emboço')) return 9;
  if (v.includes('Piso') || v.includes('Porcelanato')) return 10;
  if (v.includes('Esquadria') || v.includes('Caixilh')) return 11;
  if (v.includes('Climatiza') || v.includes('HVAC')) return 12;
  if (v.includes('Acabamento') || v.includes('Luminária')) return 13;
  if (v.includes('Pintura')) return 14;
  if (v.includes('Comissionamento') || v.includes('Entrega')) return 15;
  return 99;
}

function getDisciplineColor(tipo: string, pav: string = ''): string {
  const t = (tipo || '').toLowerCase();
  const p = (pav || '').toLowerCase();
  
  if (p.includes('cobertura') || t.includes('cobertura') || t.includes('telha') || t.includes('metálic') || t.includes('calha') || t.includes('rufo')) {
    return 'bg-cyan-600';
  }
  if (t.includes('estrutur') || t.includes('fund') || t.includes('baldrame') || t.includes('pilar') || t.includes('concreto')) {
    return 'bg-blue-600';
  }
  if (t.includes('alvenaria') || t.includes('vedação')) {
    return 'bg-amber-600';
  }
  if (t.includes('elétric') || t.includes('lógica') || t.includes('cabo')) {
    return 'bg-yellow-600';
  }
  if (t.includes('hidrául') || t.includes('esgoto') || t.includes('água') || t.includes('impermeabiliz')) {
    return 'bg-emerald-600';
  }
  if (t.includes('reboco') || t.includes('emboço') || t.includes('chapisco')) {
    return 'bg-orange-600';
  }
  if (t.includes('porcelanato') || t.includes('revestimento') || t.includes('piso') || t.includes('cerâmica')) {
    return 'bg-indigo-600';
  }
  if (t.includes('pintura') || t.includes('esquadria') || t.includes('vidro')) {
    return 'bg-purple-600';
  }
  return 'bg-zinc-600';
}

/**
 * Constrói o Grafo de Precedências da Linha de Balanço (LOB).
 * Combina duas dimensões fundamentais do Lean Construction:
 * 1. Dependência Espacial: Na mesma Zona/Pavimento, a disciplina K só inicia após a liberação da K-1.
 * 2. Dependência de Equipe: No mesmo Vagão, a equipe se desloca sequencialmente entre as zonas (Zona 1 -> 2 -> 3 -> 4).
 * 3. Portões Especiais de Bloqueio da EAP:
 *    - Portão 3: Teste Hidrostático (Vagão 08) bloqueia Reboco (Vagão 09).
 *    - Alvenaria (Vagão 06) libera Cobertura (Vagão 07 na Zona 4).
 *    - Cobertura (Vagão 07) libera acabamentos finos de piso e pintura.
 *    - Comissionamento (Vagão 15) sucede todas as atividades.
 */
/**
 * Constrói o Grafo Canônico de Precedências da Linha de Balanço (DAG Acíclico).
 * Regras estritas do Lean Construction:
 * 1. Dependência Espacial: Na mesma Zona/Pavimento, a sequência executiva segue estritamente
 *    a ordem natural física das linhas do CSV (evita inversões de fases como Climatização 1 e 2).
 * 2. Dependência de Equipe (Esteira Takt): No mesmo Vagão, a equipe avança de uma zona para a seguinte,
 *    exceto quando o baseline original previa execução em paralelo simultâneo (mesma data).
 * 3. Marco de Cobertura: Cobertura Metálica (Zona 4) só inicia após conclusão da Alvenaria (Zona 3).
 * 4. Marco de Entrega: Comissionamento & Entrega (Vagão 15) sucede todas as frentes.
 */
function buildLOBGraph(rawRows: any[]): { 
  adj: Map<number, number[]>; 
  revAdj: Map<number, number[]>;
  topoOrder: number[];
} {
  const adj = new Map<number, number[]>();
  const revAdj = new Map<number, number[]>();

  for (let i = 0; i < rawRows.length; i++) {
    adj.set(i, []);
    revAdj.set(i, []);
  }

  const addEdge = (u: number, v: number) => {
    if (u === v || u < 0 || v < 0 || u >= rawRows.length || v >= rawRows.length) return;
    const sucs = adj.get(u)!;
    if (!sucs.includes(v)) sucs.push(v);
    const preds = revAdj.get(v)!;
    if (!preds.includes(u)) preds.push(u);
  };

  // 1. Dependência Espacial na Mesma Zona (Sequência Executiva Natural do CSV)
  const zonasMap = new Map<string, number[]>();
  rawRows.forEach((r, idx) => {
    const pav = (r['LOCAL_PAVIMENTO'] || '').trim();
    if (!zonasMap.has(pav)) zonasMap.set(pav, []);
    zonasMap.get(pav)!.push(idx);
  });

  zonasMap.forEach((indices) => {
    indices.sort((a, b) => a - b);
    for (let k = 0; k < indices.length - 1; k++) {
      addEdge(indices[k], indices[k + 1]);
    }
  });

  // 2. Dependência de Equipe no Mesmo Vagão entre Zonas (Esteira Takt)
  const vagoesMap = new Map<string, number[]>();
  rawRows.forEach((r, idx) => {
    const vagao = (r['VAGAO'] || '').trim();
    if (!vagoesMap.has(vagao)) vagoesMap.set(vagao, []);
    vagoesMap.get(vagao)!.push(idx);
  });

  vagoesMap.forEach((indices) => {
    indices.sort((a, b) => a - b);
    for (let k = 0; k < indices.length - 1; k++) {
      const u = indices[k];
      const v = indices[k + 1];
      const dFimU = parseDateRobust(rawRows[u]['DATA_FIM']);
      const dIniV = parseDateRobust(rawRows[v]['DATA_INICIO']);
      // Só vincula se no baseline a tarefa seguinte não foi planejada simultaneamente (em paralelo)
      if (dFimU && dIniV && dIniV.getTime() >= dFimU.getTime()) {
        addEdge(u, v);
      }
    }
  });

  // 3. Marco Técnico: Alvenaria na Zona 3 libera Cobertura Metálica na Zona 4
  const idxAlvenariaZ3 = rawRows.findIndex(r => (r['VAGAO'] || '').includes('06.') && (r['LOCAL_PAVIMENTO'] || '').includes('Zona 03'));
  if (idxAlvenariaZ3 !== -1) {
    rawRows.forEach((r, idx) => {
      if ((r['VAGAO'] || '').includes('07.') && (r['LOCAL_PAVIMENTO'] || '').includes('Zona 04')) {
        addEdge(idxAlvenariaZ3, idx);
      }
    });
  }

  // 4. Marco Técnico: Comissionamento & Entrega (Vagão 15) sucede todas as atividades anteriores
  const indicesComissionamento: number[] = [];
  rawRows.forEach((r, idx) => {
    if ((r['VAGAO'] || '').includes('15.')) {
      indicesComissionamento.push(idx);
    }
  });

  // Ordenação Topológica Canônica (Kahn Algorithm para DAG garantido)
  const inDegree = new Map<number, number>();
  for (let i = 0; i < rawRows.length; i++) {
    inDegree.set(i, revAdj.get(i)!.length);
  }

  const queue: number[] = [];
  for (let i = 0; i < rawRows.length; i++) {
    if (inDegree.get(i) === 0) queue.push(i);
  }

  const topoOrder: number[] = [];
  while (queue.length > 0) {
    const u = queue.shift()!;
    topoOrder.push(u);
    for (const v of adj.get(u) || []) {
      const deg = inDegree.get(v)! - 1;
      inDegree.set(v, deg);
      if (deg === 0) {
        queue.push(v);
      }
    }
  }

  // Se por algum motivo restar algum nó fora da ordenação topológica, adiciona ao final
  if (topoOrder.length < rawRows.length) {
    for (let i = 0; i < rawRows.length; i++) {
      if (!topoOrder.includes(i)) topoOrder.push(i);
    }
  }

  return { adj, revAdj, topoOrder };
}

/**
 * Propagação em Cascata para Sucessoras (Forward Pass).
 * Utiliza a Ordenação Topológica do DAG para recalcular as datas em cadeia com precisão matemática,
 * garantindo zero ciclos, zero sobreposições e fluxo contínuo perfeito.
 */
function propagarCascataForward(
  rawRows: any[], 
  startIndices: number[], 
  adj: Map<number, number[]>,
  topoOrder: number[]
): Set<number> {
  const modificados = new Set<number>();
  
  // 1. Determina todos os nós atingíveis (sucessores diretos e indiretos) a partir dos startIndices
  const reachable = new Set<number>(startIndices);
  const q = [...startIndices];
  while (q.length > 0) {
    const curr = q.shift()!;
    for (const nxt of adj.get(curr) || []) {
      if (!reachable.has(nxt)) {
        reachable.add(nxt);
        q.push(nxt);
      }
    }
  }

  // 2. Processa os nós atingíveis exatamente na ordem topológica do DAG
  const activeTopo = topoOrder.filter(node => reachable.has(node));

  for (const u of activeTopo) {
    const rowU = rawRows[u];
    const dFimU = parseDateRobust(rowU['DATA_FIM']);
    if (!dFimU) continue;

    const sucs = adj.get(u) || [];
    for (const v of sucs) {
      const rowV = rawRows[v];
      const dIniV = parseDateRobust(rowV['DATA_INICIO']);
      const durV = parseInt(rowV['RITMO_DIAS_POR_LOCAL'] || '3', 10);
      if (!dIniV) continue;

      // Sucessora deve iniciar no próximo dia útil após o término da predecessora
      const minInicioV = addWorkingDays(dFimU, 1);

      if (dIniV.getTime() < minInicioV.getTime()) {
        rowV['DATA_INICIO'] = formatDateBR(minInicioV);
        const novoFimV = calculateWorkingEndDate(minInicioV, durV);
        rowV['DATA_FIM'] = formatDateBR(novoFimV);
        modificados.add(v);
      }
    }
  }

  return modificados;
}

/**
 * Propagação em Cascata para Predecessoras (Backward Pass).
 * Percorre na Ordem Topológica Reversa antecipando tarefas predecessoras que entrariam em conflito.
 */
function propagarCascataBackward(
  rawRows: any[], 
  startIndices: number[], 
  revAdj: Map<number, number[]>,
  topoOrder: number[]
): Set<number> {
  const modificados = new Set<number>();
  
  // 1. Determina todos os nós antecessores diretos e indiretos
  const reachable = new Set<number>(startIndices);
  const q = [...startIndices];
  while (q.length > 0) {
    const curr = q.shift()!;
    for (const prv of revAdj.get(curr) || []) {
      if (!reachable.has(prv)) {
        reachable.add(prv);
        q.push(prv);
      }
    }
  }

  // 2. Processa na ordem topológica inversa
  const activeRevTopo = [...topoOrder].reverse().filter(node => reachable.has(node));

  for (const v of activeRevTopo) {
    const rowV = rawRows[v];
    const dIniV = parseDateRobust(rowV['DATA_INICIO']);
    if (!dIniV) continue;

    const preds = revAdj.get(v) || [];
    for (const u of preds) {
      const rowU = rawRows[u];
      const dFimU = parseDateRobust(rowU['DATA_FIM']);
      const durU = parseInt(rowU['RITMO_DIAS_POR_LOCAL'] || '3', 10);
      if (!dFimU) continue;

      // Predecessora deve terminar pelo menos 1 dia útil antes do início da sucessora
      const maxFimU = addWorkingDays(dIniV, -1);

      if (dFimU.getTime() > maxFimU.getTime()) {
        rowU['DATA_FIM'] = formatDateBR(maxFimU);
        const novoIniU = addWorkingDays(maxFimU, -(durU - 1));
        rowU['DATA_INICIO'] = formatDateBR(novoIniU);
        modificados.add(u);
      }
    }
  }

  return modificados;
}

/**
 * Sincronização Bidirecional com a Programação de Curto Prazo (Lotes Semanais).
 * Atualiza o lote correspondente no arquivo CSV de curto prazo com a nova duração e o novo headcount via RUP.
 */
function sincronizarCurtoPrazo(
  basePath: string, 
  obra: string, 
  vagaoNome: string, 
  pavimento: string, 
  novaDuracao: number, 
  novoHeadcount?: number,
  novaEquipe?: string
) {
  const obraClean = obra.replace(/^OBRA_/, '');
  const candidateFiles = Array.from(new Set([
    path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', `PROGRAMACAO_CURTO_PRAZO_${obra}.csv`),
    path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', `PROGRAMACAO_CURTO_PRAZO_${obraClean}.csv`),
    path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'PROGRAMACAO_CURTO_PRAZO_OBRA_TMULT.csv'),
    path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'PROGRAMACAO_CURTO_PRAZO_TMULT.csv'),
    path.resolve(process.cwd(), `../projetos/${obra}/03_PLANEJAMENTO_E_CRONOGRAMA/PROGRAMACAO_CURTO_PRAZO_${obra}.csv`),
    path.resolve(process.cwd(), `../projetos/${obra}/03_PLANEJAMENTO_E_CRONOGRAMA/PROGRAMACAO_CURTO_PRAZO_${obraClean}.csv`),
    path.resolve(process.cwd(), `projetos/${obra}/03_PLANEJAMENTO_E_CRONOGRAMA/PROGRAMACAO_CURTO_PRAZO_${obra}.csv`),
    path.resolve(process.cwd(), `projetos/${obra}/03_PLANEJAMENTO_E_CRONOGRAMA/PROGRAMACAO_CURTO_PRAZO_${obraClean}.csv`),
  ])).filter(p => fs.existsSync(p));
  
  if (candidateFiles.length === 0) return;

  const vagaoPrefix = (vagaoNome || '').slice(0, 2);
  const pavLower = (pavimento || '').toLowerCase();

  for (const progFile of candidateFiles) {
    try {
      const rawContent = fs.readFileSync(progFile, 'utf-8');
      const lines = rawContent.split(/\r?\n/).filter(l => l.trim().length > 0);
      if (lines.length < 2) continue;

      const headers = lines[0].split(';').map(h => h.replace(/^"|"$/g, '').trim());
      const durIdx = headers.indexOf('DURACAO_DIAS');
      const hcIdx = headers.indexOf('HEADCOUNT_PREVISTO');
      const eqIdx = headers.indexOf('EQUIPE_PREVISTA');
      const vagaoIdx = headers.indexOf('VAGAO_ESTEIRA');
      const zonaIdx = headers.indexOf('ETAPA_ZONA');

      if (durIdx === -1 || hcIdx === -1) continue;

      let modified = false;
      const newLines = [lines[0]];

      for (let i = 1; i < lines.length; i++) {
        const parts = lines[i].split(';').map(p => p.replace(/^"|"$/g, '').trim());
        const loteVagao = vagaoIdx !== -1 ? parts[vagaoIdx] : '';
        const loteZona = zonaIdx !== -1 ? parts[zonaIdx].toLowerCase() : '';

        const matchVagao = loteVagao.includes(vagaoPrefix) || 
                           (vagaoNome && loteVagao.toLowerCase().includes(vagaoNome.toLowerCase().slice(3, 10)));
        
        const matchZona = !pavimento ||
                          (pavLower.includes('zona 01') && (loteZona.includes('zona 1') || loteZona.includes('etapa 1'))) ||
                          (pavLower.includes('zona 02') && (loteZona.includes('zona 2') || loteZona.includes('etapa 2'))) ||
                          (pavLower.includes('zona 03') && (loteZona.includes('zona 3') || loteZona.includes('etapa 3'))) ||
                          (pavLower.includes('zona 04') && (loteZona.includes('cobertura') || loteZona.includes('platibanda')));

        if (matchVagao && matchZona) {
          const oldDur = parseInt(parts[durIdx] || '3', 10);
          const oldHc = parseInt(parts[hcIdx] || '8', 10);

          parts[durIdx] = String(novaDuracao);

          // Dimensionamento Dinâmico RUP: Headcount = ceil(HeadcountBase * (DuracaoBase / NovaDuracao))
          let calcHc = novoHeadcount;
          if (!calcHc || calcHc <= 0) {
            if (oldDur > 0 && novaDuracao > 0 && oldDur !== novaDuracao) {
              calcHc = Math.max(1, Math.ceil(oldHc * (oldDur / novaDuracao)));
            } else {
              calcHc = oldHc;
            }
          }
          parts[hcIdx] = String(calcHc);

          if (novaEquipe && eqIdx !== -1) {
            parts[eqIdx] = novaEquipe;
          }

          modified = true;
        }

        newLines.push(parts.map(p => `"${p}"`).join(';'));
      }

      if (modified) {
        fs.writeFileSync(progFile, newLines.join('\n') + '\n', 'utf-8');
      }
    } catch (err) {
      console.warn(`Aviso: Erro ao sincronizar curto prazo no arquivo ${progFile}:`, err);
    }
  }
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const obra = searchParams.get('obra') || 'OBRA_TMULT';
  
  const basePath = process.env.OBRA_PATH 
    ? process.env.OBRA_PATH.replace(/OBRA.*$/, obra)
    : path.resolve(process.cwd(), `../projetos/${obra}`);
    
  const possiblePaths = [
    path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'LINHA_DE_BALANCO.csv'),
    path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'TEMPLATE_LINHA_DE_BALANCO.csv'),
    path.resolve(process.cwd(), '../projetos/OBRA_TMULT/03_PLANEJAMENTO_E_CRONOGRAMA/LINHA_DE_BALANCO.csv'),
    path.resolve(process.cwd(), '../projetos/_TEMPLATE_OBRA_NOVA/03_PLANEJAMENTO_E_CRONOGRAMA/TEMPLATE_LINHA_DE_BALANCO.csv')
  ];

  let filePath = possiblePaths.find(p => fs.existsSync(p)) || possiblePaths[0];

  try {
    const rawData = parseCSV(filePath);
    const { adj, revAdj } = buildLOBGraph(rawData);
    
    const pavimentosSet = new Set<string>();
    const tarefasMapeadas: any[] = [];

    rawData.forEach((item: any, index: number) => {
      const pav = item['LOCAL_PAVIMENTO'] || item['PAVIMENTO'] || item['SETOR'];
      if (!pav) return;
      pavimentosSet.add(pav);
      
      const tipo = item['ATIVIDADE'] || item['SERVICO'] || 'Serviço';
      const vagao = item['VAGAO'] || tipo;
      const color = getDisciplineColor(vagao || tipo, pav);
      
      const startDate = parseDateRobust(item['DATA_INICIO']);
      const endDate = parseDateRobust(item['DATA_FIM']);
      
      const predsIndices = revAdj.get(index) || [];
      const sucsIndices = adj.get(index) || [];

      const predecessoresNomes = predsIndices.map(i => `${rawData[i]['VAGAO'] || rawData[i]['ATIVIDADE']} (${rawData[i]['LOCAL_PAVIMENTO']})`);
      const sucessoresNomes = sucsIndices.map(i => `${rawData[i]['VAGAO'] || rawData[i]['ATIVIDADE']} (${rawData[i]['LOCAL_PAVIMENTO']})`);

      if (startDate && endDate && !isNaN(startDate.getTime()) && !isNaN(endDate.getTime())) {
        tarefasMapeadas.push({
          id: index + 1,
          pav,
          tipo,
          vagao,
          color,
          _startDate: startDate,
          _endDate: endDate,
          dataInicio: item['DATA_INICIO'],
          dataFim: item['DATA_FIM'],
          equipe: item['EQUIPE_RESPONSAVEL'] || 'Equipe Própria',
          durationOriginal: parseInt(item['RITMO_DIAS_POR_LOCAL'] || '1', 10),
          predecessores: predsIndices.map(i => i + 1),
          sucessores: sucsIndices.map(i => i + 1),
          predecessoresNomes,
          sucessoresNomes
        });
      }
    });

    let finalTarefas: any[] = [];
    let pavimentos: string[] = [];
    let vagoesFluxo: any[] = [];
    let totalDias = 35;

    if (tarefasMapeadas.length > 0) {
      const minTimestamp = Math.min(...tarefasMapeadas.map(t => t._startDate.getTime()));
      
      finalTarefas = tarefasMapeadas.map(t => {
        const startDay = Math.max(1, Math.floor((t._startDate.getTime() - minTimestamp) / (1000 * 60 * 60 * 24)) + 1);
        const calcDuration = Math.max(1, Math.floor((t._endDate.getTime() - t._startDate.getTime()) / (1000 * 60 * 60 * 24)) + 1);
        const duration = t.durationOriginal > 0 ? t.durationOriginal : calcDuration;
        
        return {
          id: t.id,
          pav: t.pav,
          tipo: t.tipo,
          vagao: t.vagao,
          color: t.color,
          start: startDay,
          duration,
          equipe: t.equipe,
          dataInicio: t.dataInicio,
          dataFim: t.dataFim,
          predecessores: t.predecessores,
          sucessores: t.sucessores,
          predecessoresNomes: t.predecessoresNomes,
          sucessoresNomes: t.sucessoresNomes
        };
      });

      const ordemHierarquica = [
        'Zona 01 - Recepção/Diretoria',
        'Zona 02 - Salas Técnicas/CPD',
        'Zona 03 - Sanitários e Apoio',
        'Zona 04 - Cobertura e Platibanda'
      ];
      pavimentos = Array.from(pavimentosSet)
        .filter(p => !p.toLowerCase().includes('geral'))
        .sort((a, b) => {
          const idxA = ordemHierarquica.indexOf(a);
          const idxB = ordemHierarquica.indexOf(b);
          if (idxA !== -1 && idxB !== -1) return idxA - idxB;
          return a.localeCompare(b);
        });

      if (pavimentos.length === 0) {
        pavimentos = ordemHierarquica;
      }
      
      let maxDay = 0;
      finalTarefas.forEach(t => {
        const end = t.start + t.duration;
        if (end > maxDay) maxDay = end;
      });
      totalDias = Math.max(26, maxDay + 2);

      const vagoesMap = new Map<string, any>();
      finalTarefas.forEach(t => {
        const vagaoNome = t.vagao || t.tipo;
        if (!vagoesMap.has(vagaoNome)) {
          vagoesMap.set(vagaoNome, {
            id: vagaoNome.toLowerCase().replace(/[^a-z0-9]/g, '-'),
            nome: vagaoNome,
            equipe: t.equipe,
            color: t.color,
            pontos: [],
            startMin: t.start,
            endMax: t.start + t.duration,
            dataInicioGlobal: t.dataInicio,
            dataFimGlobal: t.dataFim,
            predecessoresNomes: new Set<string>(),
            sucessoresNomes: new Set<string>()
          });
        }
        
        const v = vagoesMap.get(vagaoNome);
        if (pavimentos.includes(t.pav)) {
          v.pontos.push({
            id: t.id,
            pav: t.pav,
            start: t.start,
            duration: t.duration,
            dataInicio: t.dataInicio,
            dataFim: t.dataFim
          });
        }
        
        (t.predecessoresNomes || []).forEach((pn: string) => v.predecessoresNomes.add(pn));
        (t.sucessoresNomes || []).forEach((sn: string) => v.sucessoresNomes.add(sn));

        if (t.start < v.startMin) {
          v.startMin = t.start;
          v.dataInicioGlobal = t.dataInicio;
        }
        if (t.start + t.duration > v.endMax) {
          v.endMax = t.start + t.duration;
          v.dataFimGlobal = t.dataFim;
        }
      });

      vagoesFluxo = Array.from(vagoesMap.values())
        .filter(v => v.pontos.length > 0)
        .map(v => ({
          ...v,
          predecessoresNomes: Array.from(v.predecessoresNomes),
          sucessoresNomes: Array.from(v.sucessoresNomes)
        }))
        .sort((a, b) => a.startMin - b.startMin);
    }

    const sobreposicaoPath = path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'RELATORIO_SOBREPOSICAO_LOB.json');
    let relatorioSobreposicao: any = null;
    if (fs.existsSync(sobreposicaoPath)) {
      try {
        relatorioSobreposicao = JSON.parse(fs.readFileSync(sobreposicaoPath, 'utf-8'));
      } catch (err) {
        console.error('Erro ao ler RELATORIO_SOBREPOSICAO_LOB.json', err);
      }
    }

    const cpmPath = path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'dados_cpm.json');
    let cpmAtividades: any[] = [];
    if (fs.existsSync(cpmPath)) {
      try {
        const cpmRaw = JSON.parse(fs.readFileSync(cpmPath, 'utf-8'));
        cpmAtividades = cpmRaw.atividades || [];
      } catch (err) {
        console.error('Erro ao ler dados_cpm.json', err);
      }
    }

    const curvaS = [
      { mes: 'Mês 1', fisicoPlan: 12.05, financeiroPlan: 9.84, valorMes: 163442.02 },
      { mes: 'Mês 2', fisicoPlan: 30.20, financeiroPlan: 26.57, valorMes: 277895.85 },
      { mes: 'Mês 3', fisicoPlan: 54.10, financeiroPlan: 48.63, valorMes: 366373.12 },
      { mes: 'Mês 4', fisicoPlan: 69.85, financeiroPlan: 63.43, valorMes: 245681.39 },
      { mes: 'Mês 5', fisicoPlan: 88.40, financeiroPlan: 82.72, valorMes: 320416.90 },
      { mes: 'Mês 6', fisicoPlan: 100.0, financeiroPlan: 100.0, valorMes: 286953.00 },
    ];

    const progPaths = [
      path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', `PROGRAMACAO_CURTO_PRAZO_${obra}.csv`),
      path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'PROGRAMACAO_CURTO_PRAZO_OBRA_TMULT.csv'),
      path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'PROGRAMACAO_CURTO_PRAZO_TMULT.csv'),
      path.resolve(process.cwd(), '../projetos/OBRA_TMULT/03_PLANEJAMENTO_E_CRONOGRAMA/PROGRAMACAO_CURTO_PRAZO_TMULT.csv')
    ];
    let lotesCurtoPrazo: any[] = [];
    const progFile = progPaths.find(p => fs.existsSync(p));
    if (progFile) {
      const rawProg = parseCSV(progFile);
      lotesCurtoPrazo = rawProg.map(row => ({
        codLote: row['COD_LOTE'],
        semana: row['SEMANA'],
        diasSemana: row['DIAS_SEMANA'] || '',
        etapaZona: row['ETAPA_ZONA'] || row['SETOR'] || 'Geral',
        vagaoEsteira: row['VAGAO_ESTEIRA'] || 'Geral',
        setor: row['ETAPA_ZONA'] || row['SETOR'] || 'Geral',
        servico: row['SERVICO_LOTE'],
        metaFisica: row['META_FISICA'],
        duracaoDias: parseInt(row['DURACAO_DIAS'] || '3', 10),
        equipePrevista: row['EQUIPE_PREVISTA'],
        headcount: parseInt(row['HEADCOUNT_PREVISTO'] || '4', 10),
        equipamentos: row['EQUIPAMENTOS_PREVISTOS'],
        materiaisUcc: row['MATERIAIS_UCC'],
        rupMeta: row['RUP_META_HH_UNID'],
        status: row['STATUS_EXECUCAO'],
        rdoVinculado: row['RDO_VINCULADO']
      }));
    }

    const histogramaMensal = [
      { mes: 'Mês 1 (Sem 01-04)', producao: 9, gestaoApoio: 5, total: 14, foco: 'Topografia, Canteiro, Escavações e Sapatas S1 a S32' },
      { mes: 'Mês 2 (Sem 05-08)', producao: 14, gestaoApoio: 5, total: 19, foco: 'Baldrames VB1-VB19, Pilares P1-P24 e Laje H12' },
      { mes: 'Mês 3 (Sem 09-12)', producao: 15, gestaoApoio: 5, total: 20, foco: 'Alvenaria de Vedação, Cobertura Metálica e Embutidos' },
      { mes: 'Mês 4 (Sem 13-16)', producao: 12, gestaoApoio: 5, total: 17, foco: 'Reboco Mecanizado, Contrapisos e Impermeabilização' },
      { mes: 'Mês 5 (Sem 17-20)', producao: 11, gestaoApoio: 5, total: 16, foco: 'Porcelanatos, Esquadrias Alumínio e Tubulações HVAC' },
      { mes: 'Mês 6 (Sem 21-26)', producao: 11, gestaoApoio: 5, total: 16, foco: 'Pintura Acrílica, Aparelhos HVAC, Comissionamento e Limpeza' },
    ];

    return NextResponse.json({
      obra,
      tarefas: finalTarefas,
      vagoesFluxo,
      pavimentos,
      totalDias,
      cpm: cpmAtividades,
      curvaS,
      lotesCurtoPrazo,
      histogramaMensal,
      relatorioSobreposicao,
      metaGlobal: {
        prazoMeses: 6,
        diasCorridos: 180,
        semanas: 26,
        valorTurnkey: 1660762.28,
        caminhoCriticoDias: 178
      }
    });
  } catch (error) {
    console.error('Falha geral no cronograma', error);
    return NextResponse.json({ 
      error: 'Falha ao processar dados do cronograma', 
      details: String(error),
      obra,
      tarefas: [], 
      pavimentos: [] 
    }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { 
      obra = 'OBRA_TMULT', 
      acao = 'atualizar_tarefa', 
      tarefa, 
      tarefas, 
      id, 
      vagaoNome,
      dias, 
      deslocarSucessores = true,
      deslocarPredecessores = false,
      empurrarSucessores,
      aplicarEmTodoVagao = false,
      permitirSobreposicao = false
    } = body;
    
    const basePath = process.env.OBRA_PATH 
      ? process.env.OBRA_PATH.replace(/OBRA.*$/, obra)
      : path.resolve(process.cwd(), `../projetos/${obra}`);
      
    const possiblePaths = [
      path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'LINHA_DE_BALANCO.csv'),
      path.resolve(process.cwd(), `../projetos/${obra}/03_PLANEJAMENTO_E_CRONOGRAMA/LINHA_DE_BALANCO.csv`),
      path.resolve(process.cwd(), `projetos/${obra}/03_PLANEJAMENTO_E_CRONOGRAMA/LINHA_DE_BALANCO.csv`),
    ];
    const filePath = possiblePaths.find(p => fs.existsSync(p));
    if (!filePath) {
      return NextResponse.json({ error: `Arquivo LINHA_DE_BALANCO.csv não encontrado para ${obra}` }, { status: 404 });
    }

    const rawRows = parseCSV(filePath);
    if (rawRows.length === 0) {
      return NextResponse.json({ error: 'Arquivo CSV vazio' }, { status: 400 });
    }

    // Constrói grafo de precedências canônico
    const { adj, revAdj, topoOrder } = buildLOBGraph(rawRows);
    let tarefasModificadasSet = new Set<number>();
    let feedbackMsg = '';

    // =========================================================================
    // 1. Ação: Atualizar uma tarefa individual (ou todo o vagão) com grafo
    // =========================================================================
    if (acao === 'atualizar_tarefa' && tarefa && tarefa.id) {
      const targetIdx = Number(tarefa.id) - 1;
      if (targetIdx >= 0 && targetIdx < rawRows.length) {
        const row = rawRows[targetIdx];
        const oldIni = parseDateRobust(row['DATA_INICIO']);
        const oldFim = parseDateRobust(row['DATA_FIM']);
        const oldDuration = parseInt(row['RITMO_DIAS_POR_LOCAL'] || '3', 10);

        let newIni = tarefa.dataInicio ? parseDateRobust(tarefa.dataInicio) : oldIni;
        const newDuration = tarefa.duration ? parseInt(String(tarefa.duration), 10) : oldDuration;

        // Se veio data fim explícita ou recalcula com a nova duração
        let newFim = tarefa.dataFim ? parseDateRobust(tarefa.dataFim) : null;
        if (newIni && newDuration > 0) {
          const autoFim = calculateWorkingEndDate(newIni, newDuration);
          if (!newFim || (oldFim && newFim.getTime() === oldFim.getTime() && newDuration !== oldDuration)) {
            newFim = autoFim;
          }
        }

        // Validação ou propagação para Predecessoras (Backward)
        const predsIndices = revAdj.get(targetIdx) || [];
        if (newIni && predsIndices.length > 0) {
          let maxFimPred: Date | null = null;
          let nomePredBloqueante = '';

          predsIndices.forEach(pIdx => {
            const fPred = parseDateRobust(rawRows[pIdx]['DATA_FIM']);
            if (fPred && (!maxFimPred || fPred.getTime() > maxFimPred.getTime())) {
              maxFimPred = fPred;
              nomePredBloqueante = rawRows[pIdx]['VAGAO'] || rawRows[pIdx]['ATIVIDADE'];
            }
          });

          if (maxFimPred) {
            const minInicioPermitido = addWorkingDays(maxFimPred, 1);
            if (newIni.getTime() < minInicioPermitido.getTime()) {
              if (deslocarPredecessores) {
                // Modo Cascata Reverso: antecipa predecessoras
                row['DATA_INICIO'] = formatDateBR(newIni);
                if (newFim) row['DATA_FIM'] = formatDateBR(newFim);
                const recMod = propagarCascataBackward(rawRows, [targetIdx], revAdj, topoOrder);
                recMod.forEach(id => tarefasModificadasSet.add(id));
              } else {
                // Modo Validação Restritiva: respeita a predecessora
                newIni = minInicioPermitido;
                newFim = calculateWorkingEndDate(newIni, newDuration);
                feedbackMsg += `Início ajustado para ${formatDateBR(newIni)} respeitando o término de '${nomePredBloqueante}'. `;
              }
            }
          }
        }

        if (newIni) row['DATA_INICIO'] = formatDateBR(newIni);
        if (newFim) row['DATA_FIM'] = formatDateBR(newFim);
        if (tarefa.equipe) row['EQUIPE_RESPONSAVEL'] = tarefa.equipe;
        row['RITMO_DIAS_POR_LOCAL'] = String(newDuration);
        if (tarefa.pav) row['LOCAL_PAVIMENTO'] = tarefa.pav;

        tarefasModificadasSet.add(targetIdx);

        // Se solicitado aplicar em todo o vagão (em todas as zonas)
        if (aplicarEmTodoVagao) {
          const vagaoAlvo = row['VAGAO'];
          rawRows.forEach((r, idx) => {
            if (r['VAGAO'] === vagaoAlvo && idx !== targetIdx) {
              r['RITMO_DIAS_POR_LOCAL'] = String(newDuration);
              if (tarefa.equipe) r['EQUIPE_RESPONSAVEL'] = tarefa.equipe;
              const rIni = parseDateRobust(r['DATA_INICIO']);
              if (rIni) {
                r['DATA_FIM'] = formatDateBR(calculateWorkingEndDate(rIni, newDuration));
              }
              tarefasModificadasSet.add(idx);
            }
          });
        }

        // Propagação em Cascata para Sucessoras (Forward Pass)
        const shouldEmpurrar = empurrarSucessores !== undefined ? Boolean(empurrarSucessores) : (deslocarSucessores ?? true);
        if (shouldEmpurrar) {
          const modSucs = propagarCascataForward(rawRows, Array.from(tarefasModificadasSet), adj, topoOrder);
          modSucs.forEach(id => tarefasModificadasSet.add(id));
        }

        // Sincronização com o Curto Prazo e Redimensionamento RUP
        sincronizarCurtoPrazo(
          basePath, 
          obra, 
          row['VAGAO'], 
          row['LOCAL_PAVIMENTO'], 
          newDuration, 
          tarefa.headcount,
          tarefa.equipe
        );
      }
    }
    // =========================================================================
    // 2. Ação: Deslocar Tarefa Única por N dias
    // =========================================================================
    else if (acao === 'deslocar') {
      const numId = Number(id);
      const numDias = Number(dias);
      if (!isNaN(numId) && !isNaN(numDias) && numDias !== 0) {
        const targetIdx = numId - 1;
        if (targetIdx >= 0 && targetIdx < rawRows.length) {
          const targetRow = rawRows[targetIdx];
          const dIni = parseDateRobust(targetRow['DATA_INICIO']);
          const dFim = parseDateRobust(targetRow['DATA_FIM']);
          if (dIni && dFim) {
            targetRow['DATA_INICIO'] = formatDateBR(addWorkingDays(dIni, numDias));
            targetRow['DATA_FIM'] = formatDateBR(addWorkingDays(dFim, numDias));
            tarefasModificadasSet.add(targetIdx);

            if (numDias < 0 && deslocarPredecessores) {
              const modPreds = propagarCascataBackward(rawRows, [targetIdx], revAdj, topoOrder);
              modPreds.forEach(idx => tarefasModificadasSet.add(idx));
            }

            if (deslocarSucessores) {
              const modSucs = propagarCascataForward(rawRows, [targetIdx], adj, topoOrder);
              modSucs.forEach(idx => tarefasModificadasSet.add(idx));
            }

            sincronizarCurtoPrazo(
              basePath,
              obra,
              targetRow['VAGAO'],
              targetRow['LOCAL_PAVIMENTO'],
              parseInt(targetRow['RITMO_DIAS_POR_LOCAL'] || '3', 10)
            );
          }
        }
      }
    }
    // =========================================================================
    // 3. Ação: Deslocar Vagão Inteiro (Todas as Zonas em Bloco)
    // =========================================================================
    else if (acao === 'deslocar_vagao') {
      const numDias = Number(dias);
      const vNome = String(vagaoNome || '').trim();
      if (vNome && !isNaN(numDias) && numDias !== 0) {
        const indicesDoVagao: number[] = [];
        rawRows.forEach((r, idx) => {
          if ((r['VAGAO'] || '').trim() === vNome) {
            indicesDoVagao.push(idx);
          }
        });

        indicesDoVagao.forEach(targetIdx => {
          const targetRow = rawRows[targetIdx];
          const dIni = parseDateRobust(targetRow['DATA_INICIO']);
          const dFim = parseDateRobust(targetRow['DATA_FIM']);
          if (dIni && dFim) {
            targetRow['DATA_INICIO'] = formatDateBR(addWorkingDays(dIni, numDias));
            targetRow['DATA_FIM'] = formatDateBR(addWorkingDays(dFim, numDias));
            tarefasModificadasSet.add(targetIdx);
          }
        });

        if (numDias < 0 && deslocarPredecessores) {
          const modPreds = propagarCascataBackward(rawRows, indicesDoVagao, revAdj, topoOrder);
          modPreds.forEach(idx => tarefasModificadasSet.add(idx));
        }

        if (deslocarSucessores) {
          const modSucs = propagarCascataForward(rawRows, indicesDoVagao, adj, topoOrder);
          modSucs.forEach(idx => tarefasModificadasSet.add(idx));
        }

        sincronizarCurtoPrazo(
          basePath,
          obra,
          vNome,
          '',
          3
        );
      }
    }
    // =========================================================================
    // 4. Ação: Salvar Todas as Tarefas
    // =========================================================================
    else if (acao === 'salvar_todas' && Array.isArray(tarefas)) {
      const updatedMap = new Map<number, any>();
      tarefas.forEach((t: any) => {
        if (t.id) updatedMap.set(Number(t.id), t);
      });
      rawRows.forEach((row: any, idx: number) => {
        const rowId = idx + 1;
        const up = updatedMap.get(rowId);
        if (up) {
          if (up.dataInicio) row['DATA_INICIO'] = up.dataInicio;
          if (up.dataFim) row['DATA_FIM'] = up.dataFim;
          if (up.equipe) row['EQUIPE_RESPONSAVEL'] = up.equipe;
          if (up.duration) row['RITMO_DIAS_POR_LOCAL'] = String(up.duration);
          if (up.pav) row['LOCAL_PAVIMENTO'] = up.pav;
          tarefasModificadasSet.add(idx);
        }
      });
    }

    // Regravar o CSV com formatação limpa e rigorosa
    const headers = ['LOCAL_PAVIMENTO', 'SEQUENCIA', 'VAGAO', 'ATIVIDADE', 'EQUIPE_RESPONSAVEL', 'RITMO_DIAS_POR_LOCAL', 'DATA_INICIO', 'DATA_FIM'];
    const lines = [headers.join(';')];
    rawRows.forEach((r: any, idx: number) => {
      const seq = r['SEQUENCIA'] || String(idx + 1);
      const line = [
        r['LOCAL_PAVIMENTO'] || '',
        seq,
        r['VAGAO'] || '',
        r['ATIVIDADE'] || '',
        r['EQUIPE_RESPONSAVEL'] || '',
        r['RITMO_DIAS_POR_LOCAL'] || '3',
        r['DATA_INICIO'] || '',
        r['DATA_FIM'] || ''
      ].join(';');
      lines.push(line);
    });

    fs.writeFileSync(filePath, lines.join('\n') + '\n', 'utf-8');

    // Executar análise de sobreposição e sincronização rápida em background
    let relatorioSobreposicao = null;
    try {
      const possibleScriptPaths = [
        path.resolve(process.cwd(), 'scripts', 'sincronizar_esteira_e_lob.py'),
        path.resolve(process.cwd(), '..', 'scripts', 'sincronizar_esteira_e_lob.py')
      ];
      const scriptSync = possibleScriptPaths.find(p => fs.existsSync(p));
      if (scriptSync) {
        const rootDir = path.dirname(path.dirname(scriptSync));
        const cmd = `python "${scriptSync}" --obra "${obra}" --analisar-sobreposicao ${permitirSobreposicao ? '--permitir-sobreposicao' : ''}`;
        execSync(cmd, {
          cwd: rootDir,
          timeout: 8000,
          encoding: 'utf-8'
        });
      }
    } catch (scriptErr) {
      console.warn('Aviso: Execução do script de sincronização:', scriptErr);
    }

    try {
      const actualBasePath = path.dirname(path.dirname(filePath));
      const sobreposicaoPath = path.join(actualBasePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'RELATORIO_SOBREPOSICAO_LOB.json');
      if (fs.existsSync(sobreposicaoPath)) {
        relatorioSobreposicao = JSON.parse(fs.readFileSync(sobreposicaoPath, 'utf-8'));
      }
    } catch (readErr) {
      console.warn('Aviso ao carregar relatório de sobreposição:', readErr);
    }

    return NextResponse.json({
      success: true,
      message: feedbackMsg 
        ? feedbackMsg 
        : `Linha de Balanço salva e recalculada com sucesso! (${tarefasModificadasSet.size} tarefas sincronizadas)`,
      totalModificados: tarefasModificadasSet.size,
      totalTarefas: rawRows.length,
      relatorioSobreposicao
    });
  } catch (error) {
    console.error('Erro ao salvar cronograma:', error);
    return NextResponse.json({
      error: 'Erro ao salvar alterações no cronograma',
      details: String(error)
    }, { status: 500 });
  }
}
