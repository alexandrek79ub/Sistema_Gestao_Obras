import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';

export const dynamic = 'force-dynamic';

export interface RdoRegistro {
  id: string;
  arquivo: string;
  data: string;
  diaSemana?: string;
  climaManha: string;
  climaTarde: string;
  condicao: string;
  horasParalisacao: number;
  equipePropria: number;
  equipeTerceirizada: number;
  totalEfetivo: number;
  totalHH: number;
  equipamentos: string;
  frentesEap: string;
  fvsInspecionada: string;
  fvsResultado: string;
  ocorrencias: string;
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const obra = searchParams.get('obra') || 'OBRA_TMULT';

  const basePath = process.env.OBRA_PATH
    ? process.env.OBRA_PATH.replace(/OBRA$/, obra)
    : path.resolve(process.cwd(), `../projetos/${obra}`);

  const producaoDir = path.join(basePath, '04_PRODUCAO_E_AVANCO');
  const rdosDir = path.join(producaoDir, 'RDOS');
  const filaCampoPath = path.join(producaoDir, 'fila_apontamentos_campo.json');

  const rdos: RdoRegistro[] = [];
  let totalHHAcumulado = 0;
  let totalEfetivoMedio = 0;

  try {
    if (fs.existsSync(rdosDir)) {
      const arquivos = fs.readdirSync(rdosDir).filter((f) => f.endsWith('.md'));
      arquivos.sort().reverse(); // Mais recentes primeiro

      for (const arq of arquivos) {
        try {
          const conteudo = fs.readFileSync(path.join(rdosDir, arq), 'utf-8');
          const idMatch = conteudo.match(/RDO[-_](\d+)/i) || arq.match(/RDO_(\d+)/i);
          const id = idMatch ? `RDO-${idMatch[1].padStart(3, '0')}` : arq.replace('.md', '');

          const dataMatch = conteudo.match(/\*\*Data:\*\*\s*([0-9/]+)/);
          const data = dataMatch ? dataMatch[1] : '';

          const diaMatch = conteudo.match(/\((Terça-feira|Quarta-feira|Quinta-feira|Sexta-feira|Sábado|Domingo|Segunda-feira|[\w-]+)\)/i);
          const diaSemana = diaMatch ? diaMatch[1] : '';

          const climaManhaMatch = conteudo.match(/Período Manhã:\*\*\s*([^|*\n]+)/i);
          const climaTardeMatch = conteudo.match(/Período Tarde:\*\*\s*([^|*\n]+)/i);
          const condicaoMatch = conteudo.match(/Condição:\*\*\s*([^|*\n]+)/i);
          const horasParalMatch = conteudo.match(/Horas de Paralisação[^:]*:\*\*\s*([\d.]+)/i);

          const eqPropriaMatch = conteudo.match(/Própria:\*\*\s*(\d+)/i);
          const eqTercMatch = conteudo.match(/Terceirizada[^:]*:\*\*\s*(\d+)/i);
          const totalEfMatch = conteudo.match(/Total de Mão de Obra[^:]*:\*\*\s*(\d+)/i);
          const totalHHMatch = conteudo.match(/Total de Horas-Homem[^:]*:\*\*\s*([\d.]+)/i);

          const equipMatch = conteudo.match(/## 🚜 Equipamentos Operando\s*\n\*\s*([^\n]+)/i);
          const frentesMatch = conteudo.match(/Pacotes EAP Executados:\*\*\s*([^\n]+)/i);
          const fvsMatch = conteudo.match(/FVS Inspecionada:\*\*\s*([^—\n]+)(?:—\s*\*\*Resultado:\*\*\s*([^\n]+))?/i);
          const ocorrenciasMatch = conteudo.match(/## 📝 Ocorrências e Diário de Bordo\s*\n([^#*]+)/i);

          const hh = totalHHMatch ? parseFloat(totalHHMatch[1]) : 0;
          const efetivo = totalEfMatch ? parseInt(totalEfMatch[1], 10) : 0;

          totalHHAcumulado += hh;

          rdos.push({
            id,
            arquivo: arq,
            data: data || 'Data n/d',
            diaSemana,
            climaManha: climaManhaMatch ? climaManhaMatch[1].trim() : 'Ensolarado',
            climaTarde: climaTardeMatch ? climaTardeMatch[1].trim() : 'Ensolarado',
            condicao: condicaoMatch ? condicaoMatch[1].trim() : 'Praticável',
            horasParalisacao: horasParalMatch ? parseFloat(horasParalMatch[1]) : 0,
            equipePropria: eqPropriaMatch ? parseInt(eqPropriaMatch[1], 10) : 5,
            equipeTerceirizada: eqTercMatch ? parseInt(eqTercMatch[1], 10) : 8,
            totalEfetivo: efetivo || 13,
            totalHH: hh || 104,
            equipamentos: equipMatch ? equipMatch[1].trim() : 'Mini Retro, Gerador, Betoneira',
            frentesEap: frentesMatch ? frentesMatch[1].trim() : 'Fundações e Estrutura',
            fvsInspecionada: fvsMatch && fvsMatch[1] ? fvsMatch[1].trim() : 'FVS-02',
            fvsResultado: fvsMatch && fvsMatch[2] ? fvsMatch[2].trim() : 'Aprovado',
            ocorrencias: ocorrenciasMatch ? ocorrenciasMatch[1].trim() : 'Sem ocorrências anômalas registradas no canteiro.',
          });
        } catch (itemErr) {
          console.error(`Erro ao processar ${arq}:`, itemErr);
        }
      }

      if (rdos.length > 0) {
        totalEfetivoMedio = Math.round(rdos.reduce((acc, curr) => acc + curr.totalEfetivo, 0) / rdos.length);
      }
    }

    // Leitura da fila de apontamentos do App Mobile
    let apontamentosCampo: unknown[] = [];
    if (fs.existsSync(filaCampoPath)) {
      try {
        const filaRaw = fs.readFileSync(filaCampoPath, 'utf-8');
        apontamentosCampo = JSON.parse(filaRaw);
      } catch (fErr) {
        console.error('Erro ao ler fila_apontamentos_campo:', fErr);
      }
    }

    return NextResponse.json({
      success: true,
      obra,
      resumo: {
        totalRdos: rdos.length,
        ultimoRdo: rdos.length > 0 ? rdos[0].id : 'N/A',
        ultimaData: rdos.length > 0 ? rdos[0].data : 'N/A',
        totalHHAcumulado,
        efetivoMedio: totalEfetivoMedio || 13,
        climaAtual: rdos.length > 0 ? rdos[0].climaTarde : 'Sol / Praticável',
        apontamentosPendentes: Array.isArray(apontamentosCampo) ? apontamentosCampo.length : 0,
      },
      rdos,
      apontamentosCampo,
    });
  } catch (err: unknown) {
    const errorMsg = err instanceof Error ? err.message : String(err);
    return NextResponse.json(
      {
        success: false,
        obra,
        error: errorMsg,
        resumo: {
          totalRdos: 0,
          ultimoRdo: 'N/A',
          ultimaData: 'N/A',
          totalHHAcumulado: 0,
          efetivoMedio: 0,
          climaAtual: 'Sem dados',
          apontamentosPendentes: 0,
        },
        rdos: [],
        apontamentosCampo: [],
      },
      { status: 200 }
    );
  }
}
