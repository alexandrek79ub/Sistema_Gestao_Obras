export interface TarefaLOB {
  id: number;
  pav: string;
  tipo: string;
  vagao: string;
  color: string;
  start: number;
  duration: number;
  equipe: string;
  dataInicio: string;
  dataFim: string;
  predecessores: number[];
  sucessores: number[];
  predecessoresNomes: string[];
  sucessoresNomes: string[];
}

export interface PontoVagao {
  id: number;
  pav: string;
  start: number;
  duration: number;
  dataInicio?: string;
  dataFim?: string;
}

export interface VagaoFluxo {
  id: string;
  nome: string;
  equipe: string;
  color: string;
  corHex?: string;
  pontos: PontoVagao[];
  startMin: number;
  endMax: number;
  dataInicioGlobal?: string;
  dataFimGlobal?: string;
  predecessoresNomes: string[];
  sucessoresNomes: string[];
}

export interface MacroFluxoItem {
  id: string;
  nome: string;
  equipe: string;
  color: string;
  corHex?: string;
  pontos: PontoVagao[];
  pontosMap: Map<string, { id: number; pav: string; start: number; duration: number; dataInicio?: string; dataFim?: string }>;
  startMin: number;
  endMax: number;
  dataInicioGlobal?: string;
  dataFimGlobal?: string;
  predecessoresNomes: Set<string>;
  sucessoresNomes: Set<string>;
}

export interface LoteLOBDetalhado {
  id: number;
  vagaoNome: string;
  tipo: string;
  equipe: string;
  color: string;
  start: number;
  end: number;
  duration: number;
  dataInicio: string;
  dataFim: string;
  dataInicioFormatada?: string;
  dataFimFormatada?: string;
}

export interface AtividadeCPM {
  id: string;
  duracao_dias?: number;
  predecessoras: string[];
  es_inicio_mais_cedo: number;
  ef_fim_mais_cedo: number;
  ls_inicio_mais_tarde: number;
  lf_fim_mais_tarde: number;
  folga_dias: number;
  critica: boolean;
  dataInicio: string;
  dataFim: string;
}

export interface LoteCurtoPrazo {
  codLote?: string;
  semana?: string;
  diasSemana: string;
  dataInicio: string;
  dataFim: string;
  etapaZona: string;
  vagaoEsteira: string;
  setor: string;
  servico?: string;
  metaFisica?: string;
  duracaoDias: number;
  equipePrevista?: string;
  headcount: number;
  equipamentos?: string;
  materiaisUcc?: string;
  rupMeta?: string;
  status?: string;
  rdoVinculado?: string;
}

export interface HistogramaItem {
  mes: string;
  producao: number;
  gestaoApoio: number;
  total: number;
  hhTotal: number;
  foco: string;
}

export interface HistogramaFuncaoItem {
  grupo: string;
  cargo: string;
  categoria: string;
  custoBase: number;
  meses: number[];
  totalMeses: number;
  totalHH: number;
}

export interface ResumoHistograma {
  totalGeralHH: number;
  totalHeadcountMeses: number;
  mediaHeadcount: number;
  picoHeadcount: number;
}

export interface CurvaSItem {
  mes: string;
  fisicoPlan: number;
  financeiroPlan: number;
  valorMes: number;
}

export interface MetaGlobal {
  prazoMeses?: number;
  diasCorridos: number;
  semanas: number;
  valorTurnkey: number;
  caminhoCriticoDias: number;
  [key: string]: unknown;
}

export interface CronogramaDados {
  obra: string;
  tarefas: TarefaLOB[];
  vagoesFluxo: VagaoFluxo[];
  pavimentos: string[];
  totalDias: number;
  cpm: AtividadeCPM[];
  curvaS: CurvaSItem[];
  lotesCurtoPrazo: LoteCurtoPrazo[];
  histogramaMensal: HistogramaItem[];
  histogramaPorFuncao: HistogramaFuncaoItem[];
  resumoHistograma: ResumoHistograma;
  relatorioSobreposicao: unknown;
  metaGlobal: MetaGlobal;
}
