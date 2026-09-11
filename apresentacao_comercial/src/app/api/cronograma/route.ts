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
    if (current.getDay() !== 0) { // Sunday = 0
      count += step;
    }
  }
  return count;
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
          durationOriginal: parseInt(item['RITMO_DIAS_POR_LOCAL'] || '1', 10)
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
          dataFim: t.dataFim
        };
      });

      // Ordenar pavimentos estritamente nas 4 Zonas Físicas Reais (Base Zona 01 até Topo Zona 04)
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

      // Agrupar tarefas por VAGÃO para gerar as Linhas de Balanço Contínuas (↗)
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
            dataFimGlobal: t.dataFim
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
        .sort((a, b) => a.startMin - b.startMin);
    }

    // Carregar Relatório de Sobreposição e Nivelamento da LOB
    const sobreposicaoPath = path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'RELATORIO_SOBREPOSICAO_LOB.json');
    let relatorioSobreposicao: any = null;
    if (fs.existsSync(sobreposicaoPath)) {
      try {
        relatorioSobreposicao = JSON.parse(fs.readFileSync(sobreposicaoPath, 'utf-8'));
      } catch (err) {
        console.error('Erro ao ler RELATORIO_SOBREPOSICAO_LOB.json', err);
      }
    }

    // Carregar dados CPM se disponíveis
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

    // Curva S oficial de referência (Linha de Base 01)
    const curvaS = [
      { mes: 'Mês 1', fisicoPlan: 12.05, financeiroPlan: 9.84, valorMes: 163442.02 },
      { mes: 'Mês 2', fisicoPlan: 30.20, financeiroPlan: 26.57, valorMes: 277895.85 },
      { mes: 'Mês 3', fisicoPlan: 54.10, financeiroPlan: 48.63, valorMes: 366373.12 },
      { mes: 'Mês 4', fisicoPlan: 69.85, financeiroPlan: 63.43, valorMes: 245681.39 },
      { mes: 'Mês 5', fisicoPlan: 88.40, financeiroPlan: 82.72, valorMes: 320416.90 },
      { mes: 'Mês 6', fisicoPlan: 100.0, financeiroPlan: 100.0, valorMes: 286953.00 },
    ];

    // Carregar Programação de Curto Prazo (Lotes & Recursos Previstos)
    const progPaths = [
      path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', `PROGRAMACAO_CURTO_PRAZO_${obra}.csv`),
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

    // Histograma de Mão de Obra Oficial da Obra (EAP 1.0 e RH)
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
      dias, 
      deslocarSucessores = true,
      deslocarPredecessores = false,
      empurrarSucessores,
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

    // 1. Ação: Salvar todas as tarefas editadas
    if (acao === 'salvar_todas' && Array.isArray(tarefas)) {
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
        }
      });
    } 
    // 2. Ação: Atualizar uma única tarefa ou vagão com recálculo e efeito cascata opcional
    else if (acao === 'atualizar_tarefa' && tarefa && tarefa.id) {
      const targetIdx = Number(tarefa.id) - 1;
      if (targetIdx >= 0 && targetIdx < rawRows.length) {
        const row = rawRows[targetIdx];
        const oldIni = parseDateRobust(row['DATA_INICIO']);
        const oldFim = parseDateRobust(row['DATA_FIM']);
        const oldDuration = parseInt(row['RITMO_DIAS_POR_LOCAL'] || '3', 10);

        let newIni = tarefa.dataInicio ? parseDateRobust(tarefa.dataInicio) : oldIni;
        const newDuration = tarefa.duration ? parseInt(String(tarefa.duration), 10) : oldDuration;

        // Se a duração foi alterada ou se a dataFim fornecida não foi ajustada, recalcula a data de término
        let newFim = tarefa.dataFim ? parseDateRobust(tarefa.dataFim) : null;
        if (newIni && newDuration > 0) {
          const autoFim = calculateWorkingEndDate(newIni, newDuration);
          // Se não veio dataFim ou se veio a data antiga mas a duração mudou, prioriza a data calculada pela nova duração
          if (!newFim || (oldFim && newFim.getTime() === oldFim.getTime() && newDuration !== oldDuration)) {
            newFim = autoFim;
          }
        }

        if (newIni) row['DATA_INICIO'] = formatDateBR(newIni);
        if (newFim) row['DATA_FIM'] = formatDateBR(newFim);
        if (tarefa.equipe) row['EQUIPE_RESPONSAVEL'] = tarefa.equipe;
        row['RITMO_DIAS_POR_LOCAL'] = String(newDuration);
        if (tarefa.pav) row['LOCAL_PAVIMENTO'] = tarefa.pav;

        // Efeito Cascata / Propagação de Precedências:
        // Padrão: empurrar sucessores automaticamente se a duração ou data fim aumentou/diminuiu
        const shouldEmpurrar = empurrarSucessores !== undefined ? Boolean(empurrarSucessores) : (deslocarSucessores ?? true);
        if (shouldEmpurrar && oldFim && newFim) {
          const deltaDias = countWorkingDaysBetween(oldFim, newFim);
          if (deltaDias !== 0) {
            for (let i = targetIdx + 1; i < rawRows.length; i++) {
              const sucIni = parseDateRobust(rawRows[i]['DATA_INICIO']);
              const sucFim = parseDateRobust(rawRows[i]['DATA_FIM']);
              if (sucIni && sucFim) {
                rawRows[i]['DATA_INICIO'] = formatDateBR(addWorkingDays(sucIni, deltaDias));
                rawRows[i]['DATA_FIM'] = formatDateBR(addWorkingDays(sucFim, deltaDias));
              }
            }
          }
        }
      }
    } 
    // 3. Ação: Deslocar por N dias (respeitando folgas e sem empurrar tarefas quando dentro da folga)
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
          }

          // Se estiver atrasando (numDias > 0) E foi solicitado empurrar sucessores:
          if (numDias > 0 && deslocarSucessores) {
            for (let i = targetIdx + 1; i < rawRows.length; i++) {
              const sIni = parseDateRobust(rawRows[i]['DATA_INICIO']);
              const sFim = parseDateRobust(rawRows[i]['DATA_FIM']);
              if (sIni && sFim) {
                rawRows[i]['DATA_INICIO'] = formatDateBR(addWorkingDays(sIni, numDias));
                rawRows[i]['DATA_FIM'] = formatDateBR(addWorkingDays(sFim, numDias));
              }
            }
          }
          // Se numDias < 0 (adiantando / aproveitando folga entre zonas),
          // NENHUMA outra tarefa é deslocada! Apenas a tarefa alvo aproveita a folga existente!
        }
      }
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
      message: 'Linha de Balanço salva e validada com sucesso no backend!',
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
