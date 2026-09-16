import path from 'path';
import fs from 'fs';
import { parseCSV } from '@/lib/csvParser';
import {
  CronogramaDados,
  TarefaLOB,
  VagaoFluxo,
  AtividadeCPM,
  LoteCurtoPrazo,
  HistogramaItem,
  HistogramaFuncaoItem,
  CurvaSItem,
} from '@/types/cronograma';

export function parseDateRobust(dateStr: string): Date | null {
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

export function formatDateBR(d: Date): string {
  const day = String(d.getDate()).padStart(2, '0');
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const year = d.getFullYear();
  return `${day}/${month}/${year}`;
}

export function addWorkingDays(date: Date, days: number): Date {
  const current = new Date(date);
  if (days === 0) return current;
  let added = 0;
  const step = days >= 0 ? 1 : -1;
  const absDays = Math.abs(days);
  while (added < absDays) {
    current.setDate(current.getDate() + step);
    if (current.getDay() !== 0) {
      added++;
    }
  }
  return current;
}

export function getDisciplineColor(tipo: string, pav: string = ''): string {
  const t = (tipo || '').toLowerCase();
  const p = (pav || '').toLowerCase();

  if (
    p.includes('cobertura') ||
    t.includes('cobertura') ||
    t.includes('telha') ||
    t.includes('metálic') ||
    t.includes('calha') ||
    t.includes('rufo')
  ) {
    return 'bg-cyan-600';
  }
  if (
    t.includes('estrutur') ||
    t.includes('fund') ||
    t.includes('baldrame') ||
    t.includes('pilar') ||
    t.includes('concreto')
  ) {
    return 'bg-blue-600';
  }
  if (t.includes('alvenaria') || t.includes('vedação')) {
    return 'bg-amber-600';
  }
  if (t.includes('elétric') || t.includes('lógica') || t.includes('cabo')) {
    return 'bg-yellow-600';
  }
  if (
    t.includes('hidrául') ||
    t.includes('esgoto') ||
    t.includes('água') ||
    t.includes('impermeabiliz')
  ) {
    return 'bg-emerald-600';
  }
  if (t.includes('reboco') || t.includes('emboço') || t.includes('chapisco')) {
    return 'bg-orange-600';
  }
  if (
    t.includes('porcelanato') ||
    t.includes('revestimento') ||
    t.includes('piso') ||
    t.includes('cerâmica')
  ) {
    return 'bg-indigo-600';
  }
  if (t.includes('pintura') || t.includes('esquadria') || t.includes('vidro')) {
    return 'bg-purple-600';
  }
  return 'bg-zinc-600';
}

export function buildLOBGraph(rawRows: Record<string, string>[]): {
  adj: Map<number, number[]>;
  revAdj: Map<number, number[]>;
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
      const dataFimU = parseDateRobust(rawRows[u]['DATA_FIM']);
      const dataIniV = parseDateRobust(rawRows[v]['DATA_INICIO']);

      if (dataFimU && dataIniV && dataIniV.getTime() >= dataFimU.getTime()) {
        addEdge(u, v);
      }
    }
  });

  // 3. Marco de Cobertura (Alvenaria na Zona 3 libera Cobertura Metálica na Zona 4)
  let idxAlvenariaZ3: number | null = null;
  rawRows.forEach((r, idx) => {
    const vagao = r['VAGAO'] || '';
    const pav = r['LOCAL_PAVIMENTO'] || '';
    if (vagao.includes('06.') && pav.toLowerCase().includes('zona 03')) {
      idxAlvenariaZ3 = idx;
    }
  });

  if (idxAlvenariaZ3 !== null) {
    rawRows.forEach((r, idx) => {
      const vagao = r['VAGAO'] || '';
      const pav = r['LOCAL_PAVIMENTO'] || '';
      if (vagao.includes('07.') && pav.toLowerCase().includes('zona 04')) {
        addEdge(idxAlvenariaZ3!, idx);
      }
    });
  }

  return { adj, revAdj };
}

export type ResultadoCronograma =
  | { ok: true; data: CronogramaDados }
  | { ok: false; error: string; status: string; httpStatus: number };

export function obterDadosCronograma(basePath: string, obra: string): ResultadoCronograma {
  const filePath = path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'LINHA_DE_BALANCO.csv');

  const csvLinhaBalanco = parseCSV(filePath);
  if (csvLinhaBalanco.status !== 'ok' && csvLinhaBalanco.status !== 'empty') {
    return {
      ok: false,
      error: csvLinhaBalanco.error || 'Erro ao processar CSV de cronograma',
      status: csvLinhaBalanco.status,
      httpStatus: csvLinhaBalanco.status === 'not_found' ? 404 : 422,
    };
  }

  const rawData = csvLinhaBalanco.data;
  const { adj, revAdj } = buildLOBGraph(rawData);

  const pavimentosSet = new Set<string>();
  interface MapeadaInterna {
    id: number;
    pav: string;
    tipo: string;
    vagao: string;
    color: string;
    _startDate: Date;
    _endDate: Date;
    dataInicio: string;
    dataFim: string;
    equipe: string;
    durationOriginal: number;
    predecessores: number[];
    sucessores: number[];
    predecessoresNomes: string[];
    sucessoresNomes: string[];
  }

  const tarefasMapeadas: MapeadaInterna[] = [];

  rawData.forEach((item: Record<string, string>, index: number) => {
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

    const predecessoresNomes = predsIndices.map(
      (i) => `${rawData[i]['VAGAO'] || rawData[i]['ATIVIDADE']} (${rawData[i]['LOCAL_PAVIMENTO']})`
    );
    const sucessoresNomes = sucsIndices.map(
      (i) => `${rawData[i]['VAGAO'] || rawData[i]['ATIVIDADE']} (${rawData[i]['LOCAL_PAVIMENTO']})`
    );

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
        predecessores: predsIndices.map((i) => i + 1),
        sucessores: sucsIndices.map((i) => i + 1),
        predecessoresNomes,
        sucessoresNomes,
      });
    }
  });

  let finalTarefas: TarefaLOB[] = [];
  let pavimentos: string[] = [];
  let vagoesFluxo: VagaoFluxo[] = [];
  let totalDias = 35;

  if (tarefasMapeadas.length > 0) {
    const minTimestamp = Math.min(...tarefasMapeadas.map((t) => t._startDate.getTime()));

    finalTarefas = tarefasMapeadas.map((t) => {
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
        sucessoresNomes: t.sucessoresNomes,
      };
    });

    const ordemHierarquica = [
      'Zona 01 - Recepção/Diretoria',
      'Zona 02 - Salas Técnicas/CPD',
      'Zona 03 - Sanitários e Apoio',
      'Zona 04 - Cobertura e Platibanda',
    ];
    pavimentos = Array.from(pavimentosSet)
      .filter((p) => !p.toLowerCase().includes('geral'))
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
    finalTarefas.forEach((t) => {
      const end = t.start + t.duration;
      if (end > maxDay) maxDay = end;
    });
    totalDias = Math.max(26, maxDay + 2);

    interface VagaoAcc {
      id: string;
      nome: string;
      equipe: string;
      color: string;
      pontos: { id: number; pav: string; start: number; duration: number; dataInicio?: string; dataFim?: string }[];
      startMin: number;
      endMax: number;
      dataInicioGlobal?: string;
      dataFimGlobal?: string;
      predecessoresNomes: Set<string>;
      sucessoresNomes: Set<string>;
    }

    const vagoesMap = new Map<string, VagaoAcc>();
    finalTarefas.forEach((t) => {
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
          sucessoresNomes: new Set<string>(),
        });
      }

      const v = vagoesMap.get(vagaoNome)!;
      if (pavimentos.includes(t.pav)) {
        v.pontos.push({
          id: t.id,
          pav: t.pav,
          start: t.start,
          duration: t.duration,
          dataInicio: t.dataInicio,
          dataFim: t.dataFim,
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
      .filter((v) => v.pontos.length > 0)
      .map((v) => ({
        id: v.id,
        nome: v.nome,
        equipe: v.equipe,
        color: v.color,
        pontos: v.pontos,
        startMin: v.startMin,
        endMax: v.endMax,
        dataInicioGlobal: v.dataInicioGlobal,
        dataFimGlobal: v.dataFimGlobal,
        predecessoresNomes: Array.from(v.predecessoresNomes),
        sucessoresNomes: Array.from(v.sucessoresNomes),
      }))
      .sort((a, b) => a.startMin - b.startMin);
  }

  const actualBasePath = path.dirname(path.dirname(filePath));
  const sobreposicaoPath = path.join(
    actualBasePath,
    '03_PLANEJAMENTO_E_CRONOGRAMA',
    'RELATORIO_SOBREPOSICAO_LOB.json'
  );
  let relatorioSobreposicao: unknown = null;
  if (fs.existsSync(sobreposicaoPath)) {
    try {
      relatorioSobreposicao = JSON.parse(fs.readFileSync(sobreposicaoPath, 'utf-8'));
    } catch (err) {
      console.error('Erro ao ler RELATORIO_SOBREPOSICAO_LOB.json', err);
    }
  }

  const cpmPath = path.join(actualBasePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'dados_cpm.json');
  let cpmAtividades: AtividadeCPM[] = [];
  let duracaoTotalCpm = 178;
  if (fs.existsSync(cpmPath)) {
    try {
      const cpmRaw = JSON.parse(fs.readFileSync(cpmPath, 'utf-8'));
      interface AtividadeRaw {
        id: string;
        nome?: string;
        servico?: string;
        duracao_dias?: number;
        predecessoras?: string[];
      }
      const rawAtividades: AtividadeRaw[] = cpmRaw.atividades || [];

      // Algoritmo clássico de CPM (Kahn forward/backward pass)
      const mapAtv = new Map<string, AtividadeRaw>();
      rawAtividades.forEach((a) => mapAtv.set(a.id, a));

      const inDegree = new Map<string, number>();
      const successors = new Map<string, string[]>();
      rawAtividades.forEach((a) => {
        inDegree.set(a.id, (a.predecessoras || []).length);
        successors.set(a.id, []);
      });

      rawAtividades.forEach((a) => {
        (a.predecessoras || []).forEach((p) => {
          if (successors.has(p)) successors.get(p)!.push(a.id);
        });
      });

      const queue: string[] = [];
      inDegree.forEach((deg, id) => {
        if (deg === 0) queue.push(id);
      });

      const topoOrder: string[] = [];
      while (queue.length > 0) {
        const u = queue.shift()!;
        topoOrder.push(u);
        (successors.get(u) || []).forEach((v) => {
          const currentDeg = (inDegree.get(v) || 0) - 1;
          inDegree.set(v, currentDeg);
          if (currentDeg === 0) queue.push(v);
        });
      }

      const es = new Map<string, number>();
      const ef = new Map<string, number>();
      topoOrder.forEach((id) => {
        const atv = mapAtv.get(id);
        const preds: string[] = atv?.predecessoras || [];
        let maxEf = 0;
        preds.forEach((p) => {
          const pEf = ef.get(p) || 0;
          if (pEf > maxEf) maxEf = pEf;
        });
        es.set(id, maxEf);
        ef.set(id, maxEf + (atv?.duracao_dias || 1));
      });

      let maxTotal = 0;
      ef.forEach((v) => {
        if (v > maxTotal) maxTotal = v;
      });
      duracaoTotalCpm = maxTotal || 178;

      const ls = new Map<string, number>();
      const lf = new Map<string, number>();
      for (let i = topoOrder.length - 1; i >= 0; i--) {
        const id = topoOrder[i];
        const atv = mapAtv.get(id);
        const sucs = successors.get(id) || [];
        let minLs = sucs.length === 0 ? maxTotal : Infinity;
        sucs.forEach((s) => {
          const sLs = ls.get(s) ?? maxTotal;
          if (sLs < minLs) minLs = sLs;
        });
        lf.set(id, minLs);
        ls.set(id, minLs - (atv?.duracao_dias || 1));
      }

      const baseStartDate = parseDateRobust('01/10/2026') || new Date(2026, 9, 1);

      cpmAtividades = topoOrder.map((id) => {
        const atv = mapAtv.get(id);
        const esVal = es.get(id) || 0;
        const efVal = ef.get(id) || 0;
        const lsVal = ls.get(id) || 0;
        const lfVal = lf.get(id) || 0;
        const folga = Math.max(0, lsVal - esVal);
        const isCritica = folga === 0;

        const dataIni = addWorkingDays(baseStartDate, esVal);
        const dataFim = addWorkingDays(baseStartDate, Math.max(0, efVal - 1));

        return {
          id,
          tipo: atv?.nome || atv?.servico || id,
          duracao_dias: atv?.duracao_dias,
          predecessoras: atv?.predecessoras || [],
          es_inicio_mais_cedo: esVal,
          ef_fim_mais_cedo: efVal,
          ls_inicio_mais_tarde: lsVal,
          lf_fim_mais_tarde: lfVal,
          folga_dias: folga,
          critica: isCritica,
          dataInicio: formatDateBR(dataIni),
          dataFim: formatDateBR(dataFim),
        };
      });
    } catch (err) {
      console.error('Erro ao calcular CPM determinístico em cronogramaService:', err);
    }
  }

  const curvaS: CurvaSItem[] = [
    { mes: 'Mês 1', fisicoPlan: 12.05, financeiroPlan: 9.84, valorMes: 163442.02 },
    { mes: 'Mês 2', fisicoPlan: 30.2, financeiroPlan: 26.57, valorMes: 277895.85 },
    { mes: 'Mês 3', fisicoPlan: 54.1, financeiroPlan: 48.63, valorMes: 366373.12 },
    { mes: 'Mês 4', fisicoPlan: 69.85, financeiroPlan: 63.43, valorMes: 245681.39 },
    { mes: 'Mês 5', fisicoPlan: 88.4, financeiroPlan: 82.72, valorMes: 320416.9 },
    { mes: 'Mês 6', fisicoPlan: 100.0, financeiroPlan: 100.0, valorMes: 286953.0 },
  ];

  const obraClean = obra.replace(/^OBRA_/, '');
  const progPaths = [
    path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', `PROGRAMACAO_CURTO_PRAZO_${obra}.csv`),
    path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', `PROGRAMACAO_CURTO_PRAZO_${obraClean}.csv`),
    path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'PROGRAMACAO_CURTO_PRAZO.csv'),
  ];
  let lotesCurtoPrazo: LoteCurtoPrazo[] = [];
  const progFile = progPaths.find((p) => fs.existsSync(p));
  if (progFile) {
    const csvProgramacao = parseCSV(progFile);
    if (csvProgramacao.status !== 'ok' && csvProgramacao.status !== 'empty') {
      return {
        ok: false,
        error: csvProgramacao.error || 'Erro ao processar CSV de programação de curto prazo',
        status: csvProgramacao.status,
        httpStatus: csvProgramacao.status === 'not_found' ? 404 : 422,
      };
    }
    const rawProg = csvProgramacao.data;
    lotesCurtoPrazo = rawProg.map((row) => ({
      codLote: row['COD_LOTE'],
      semana: row['SEMANA'],
      diasSemana: row['DIAS_SEMANA'] || '',
      dataInicio: row['DATA_INICIO'] || '',
      dataFim: row['DATA_FIM'] || '',
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
      rdoVinculado: row['RDO_VINCULADO'],
    }));
  }

  // Histograma Oficial de Mão de Obra e Headcount Sincronizado
  let histogramaMensal: HistogramaItem[] = [];
  const histogramaPorFuncao: HistogramaFuncaoItem[] = [];
  const histMoPath = path.join(basePath, '06_SST_E_RH', 'dados_histograma_mo.json');

  const focosPadrao = [
    'Topografia, Canteiro, Escavações e Sapatas S1 a S32',
    'Baldrames VB1-VB19, Pilares P1-P24 e Laje H12',
    'Alvenaria de Vedação, Cobertura Metálica e Embutidos',
    'Reboco Mecanizado, Contrapisos e Impermeabilização',
    'Porcelanatos, Esquadrias Alumínio e Tubulações HVAC',
    'Pintura Acrílica, Aparelhos HVAC, Comissionamento e Limpeza',
  ];

  if (fs.existsSync(histMoPath)) {
    try {
      const rawHist = JSON.parse(fs.readFileSync(histMoPath, 'utf-8'));
      if (Array.isArray(rawHist) && rawHist.length > 0) {
        const numMeses = Math.max(0, rawHist[0].length - 4);
        for (let m = 0; m < numMeses; m++) {
          let producao = 0;
          let gestaoApoio = 0;
          for (const row of rawHist) {
            const grupo = row[0];
            const val = typeof row[4 + m] === 'number' ? row[4 + m] : parseInt(row[4 + m] || '0', 10);
            if (grupo === 'Gestão' || grupo === 'SST / Apoio') {
              gestaoApoio += val;
            } else {
              producao += val;
            }
          }
          const mesNum = m + 1;
          const mesNome =
            mesNum <= 5
              ? `Mês ${mesNum} (Sem ${String((mesNum - 1) * 4 + 1).padStart(2, '0')}-${String(mesNum * 4).padStart(2, '0')})`
              : `Mês ${mesNum} (Sem 21-26)`;

          histogramaMensal.push({
            mes: mesNome,
            producao,
            gestaoApoio,
            total: producao + gestaoApoio,
            hhTotal: (producao + gestaoApoio) * 220,
            foco: focosPadrao[m] || `Execução Físico-Operacional - Fase Mês ${mesNum}`,
          });
        }

        for (const row of rawHist) {
          const grupo = row[0];
          const cargo = row[1];
          const categoria = row[2];
          const custoBase = typeof row[3] === 'number' ? row[3] : parseFloat(row[3] || '0');
          const mesesValores: number[] = [];
          for (let m = 0; m < numMeses; m++) {
            const val = typeof row[4 + m] === 'number' ? row[4 + m] : parseInt(row[4 + m] || '0', 10);
            mesesValores.push(val);
          }
          const totalMeses = mesesValores.reduce((a, b) => a + b, 0);
          const totalHH = totalMeses * 220;
          histogramaPorFuncao.push({
            grupo,
            cargo,
            categoria,
            custoBase,
            meses: mesesValores,
            totalMeses,
            totalHH,
          });
        }
      }
    } catch (err) {
      console.warn('Erro ao processar dados_histograma_mo.json:', err);
    }
  }

  // Fallback de segurança calibrado (22.440 HH e 102 headcount-mês)
  if (histogramaMensal.length === 0) {
    histogramaMensal = [
      { mes: 'Mês 1 (Sem 01-04)', producao: 9, gestaoApoio: 5, total: 14, hhTotal: 3080, foco: focosPadrao[0] },
      { mes: 'Mês 2 (Sem 05-08)', producao: 14, gestaoApoio: 5, total: 19, hhTotal: 4180, foco: focosPadrao[1] },
      { mes: 'Mês 3 (Sem 09-12)', producao: 15, gestaoApoio: 5, total: 20, hhTotal: 4400, foco: focosPadrao[2] },
      { mes: 'Mês 4 (Sem 13-16)', producao: 12, gestaoApoio: 5, total: 17, hhTotal: 3740, foco: focosPadrao[3] },
      { mes: 'Mês 5 (Sem 17-20)', producao: 11, gestaoApoio: 5, total: 16, hhTotal: 3520, foco: focosPadrao[4] },
      { mes: 'Mês 6 (Sem 21-26)', producao: 11, gestaoApoio: 5, total: 16, hhTotal: 3520, foco: focosPadrao[5] },
    ];
  }

  const totalGeralHeadcountMeses = histogramaMensal.reduce((acc, cur) => acc + cur.total, 0);
  const totalGeralHH = histogramaMensal.reduce((acc, cur) => acc + (cur.hhTotal || cur.total * 220), 0);
  const picoHeadcount = Math.max(...histogramaMensal.map((h) => h.total), 0);
  const mediaHeadcount = histogramaMensal.length > 0 ? totalGeralHeadcountMeses / histogramaMensal.length : 0;

  const resumoHistograma = {
    totalGeralHH,
    totalHeadcountMeses: totalGeralHeadcountMeses,
    mediaHeadcount: Math.round(mediaHeadcount * 10) / 10,
    picoHeadcount,
  };

  let dataInicioObra = '01/10/2026';
  let dataTerminoObra = '03/03/2027';
  let duracaoDiasUteis = duracaoTotalCpm || 132;
  let lotesConcluidos = 0;
  let lotesEmAndamento = 0;
  let totalLotesCount = lotesCurtoPrazo.length || 52;

  const mestrePath = path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'planejamento_mestre.json');
  if (fs.existsSync(mestrePath)) {
    try {
      const mestreRaw = JSON.parse(fs.readFileSync(mestrePath, 'utf-8'));
      dataInicioObra = mestreRaw.data_inicio_obra || dataInicioObra;
      dataTerminoObra = mestreRaw.data_termino_obra || dataTerminoObra;
      duracaoDiasUteis = mestreRaw.duracao_total_dias_uteis || duracaoDiasUteis;
      if (Array.isArray(mestreRaw.lotes)) {
        totalLotesCount = mestreRaw.lotes.length;
        lotesConcluidos = mestreRaw.lotes.filter((l: { status?: string }) => l.status === 'CONCLUIDO').length;
        lotesEmAndamento = mestreRaw.lotes.filter((l: { status?: string }) => l.status === 'EM_ANDAMENTO').length;
      }
    } catch (e) {
      console.warn('Erro ao ler planejamento_mestre.json em cronogramaService:', e);
    }
  }

  return {
    ok: true,
    data: {
      obra,
      tarefas: finalTarefas,
      vagoesFluxo,
      pavimentos,
      totalDias,
      cpm: cpmAtividades,
      curvaS,
      lotesCurtoPrazo,
      histogramaMensal,
      histogramaPorFuncao,
      resumoHistograma,
      relatorioSobreposicao,
      metaGlobal: {
        prazoMeses: 6,
        diasCorridos: 180,
        semanas: Math.ceil(duracaoDiasUteis / 6),
        valorTurnkey: 1660762.28,
        caminhoCriticoDias: duracaoDiasUteis,
        dataInicioObra,
        dataTerminoObra,
        duracaoDiasUteis,
        totalLotes: totalLotesCount,
        lotesConcluidos,
        lotesEmAndamento,
      },
    },
  };
}
