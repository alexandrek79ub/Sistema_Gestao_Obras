import { NextResponse } from 'next/server';
import { parseCSV } from '@/lib/csvParser';
import path from 'path';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const obra = searchParams.get('obra') || 'OBRA';
  
  const basePath = process.env.OBRA_PATH 
    ? process.env.OBRA_PATH.replace(/OBRA$/, obra)
    : path.resolve(process.cwd(), `../projetos/${obra}`);
    
  const filePath = path.join(basePath, '03_PLANEJAMENTO_E_CRONOGRAMA', 'TEMPLATE_LINHA_DE_BALANCO.csv');
  
  try {
    const rawData = parseCSV(filePath);
    
    const pavimentosSet = new Set<string>();
    const tarefas = rawData.map((item: any, index: number) => {
      const pav = item['LOCAL_PAVIMENTO'];
      if (pav) pavimentosSet.add(pav);
      
      const tipo = item['ATIVIDADE'];
      let color = 'bg-blue-500';
      if (tipo && tipo.toLowerCase().includes('alvenaria')) color = 'bg-amber-500';
      if (tipo && tipo.toLowerCase().includes('hidráulica')) color = 'bg-emerald-500';

      // Conversão simples de data para dia corrido (diferença em dias a partir da menor data)
      // Como o csv usa formato DD/MM/AAAA, precisamos parsear
      const [d1, m1, y1] = (item['DATA_INICIO'] || '').split('/');
      const [d2, m2, y2] = (item['DATA_FIM'] || '').split('/');
      
      const startDate = new Date(`${y1}-${m1}-${d1}`);
      const endDate = new Date(`${y2}-${m2}-${d2}`);
      
      return {
        id: index + 1,
        pav,
        tipo,
        color,
        _startDate: startDate,
        _endDate: endDate,
        equipe: item['EQUIPE_RESPONSAVEL'],
        durationOriginal: parseInt(item['RITMO_DIAS_POR_LOCAL'] || '1', 10)
      };
    }).filter((t: any) => t.pav && !isNaN(t._startDate.getTime()) && !isNaN(t._endDate.getTime()));
    
    if (tarefas.length === 0) {
      return NextResponse.json({ tarefas: [], pavimentos: [] });
    }

    const minDate = new Date(Math.min(...tarefas.map((t: any) => t._startDate.getTime())));

    const finalTarefas = tarefas.map((t: any) => {
      const startDay = Math.floor((t._startDate.getTime() - minDate.getTime()) / (1000 * 60 * 60 * 24)) + 1;
      const duration = Math.floor((t._endDate.getTime() - t._startDate.getTime()) / (1000 * 60 * 60 * 24)) + 1;
      
      return {
        id: t.id,
        pav: t.pav,
        tipo: t.tipo,
        color: t.color,
        start: startDay,
        duration: duration || t.durationOriginal || 1,
        equipe: t.equipe
      };
    });

    // Ordenar pavimentos decrescente (ex: 03, 02, 01)
    const pavimentos = Array.from(pavimentosSet).sort((a, b) => b.localeCompare(a));

    return NextResponse.json({ tarefas: finalTarefas, pavimentos });
  } catch (error) {
    return NextResponse.json({ error: 'Falha ao ler cronograma LOB', details: error }, { status: 500 });
  }
}
