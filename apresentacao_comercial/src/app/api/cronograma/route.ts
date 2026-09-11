import { NextResponse } from 'next/server';
import { parseCSV } from '@/lib/csvParser';
import path from 'path';
import fs from 'fs';

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

function getDisciplineColor(tipo: string): string {
  const t = (tipo || '').toLowerCase();
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
  if (t.includes('cobertura') || t.includes('telha') || t.includes('metálic') || t.includes('calha')) {
    return 'bg-cyan-600';
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
      const color = getDisciplineColor(tipo);
      
      const startDate = parseDateRobust(item['DATA_INICIO']);
      const endDate = parseDateRobust(item['DATA_FIM']);
      
      if (startDate && endDate && !isNaN(startDate.getTime()) && !isNaN(endDate.getTime())) {
        tarefasMapeadas.push({
          id: index + 1,
          pav,
          tipo,
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
          color: t.color,
          start: startDay,
          duration,
          equipe: t.equipe,
          dataInicio: t.dataInicio,
          dataFim: t.dataFim
        };
      });

      // Ordenar pavimentos mantendo sequência lógica
      pavimentos = Array.from(pavimentosSet);
      
      let maxDay = 0;
      finalTarefas.forEach(t => {
        const end = t.start + t.duration;
        if (end > maxDay) maxDay = end;
      });
      totalDias = Math.max(26, maxDay + 2);
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
      pavimentos,
      totalDias,
      cpm: cpmAtividades,
      curvaS,
      lotesCurtoPrazo,
      histogramaMensal,
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
