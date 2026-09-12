# 📊 SKILL: Schema dos CSVs e Estrutura de Dados do Sistema

> **Frente:** Desenvolvimento ([`SKILL_DEV_SENIOR.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/desenvolvimento/SKILL_DEV_SENIOR.md))
> **Propósito:** Documentar os schemas de todos os CSVs consumidos pelo Dashboard Next.js e gerados pelo motor Python. É a **fonte da verdade dos dados** — qualquer componente React que leia um CSV DEVE respeitar estes schemas.

---

## 1. Arquitetura de Dados

O sistema usa **arquivos CSV como banco de dados**, organizados por obra dentro de `/projetos/[NOME_OBRA]/`. O Dashboard Next.js lê esses arquivos via Server Components usando o `csvParser.ts` em `/src/lib/`.

```
/projetos/
  └── [NOME_OBRA]/
       ├── 02_ORCAMENTO_BASE_E_CONTRATOS/
       │    └── ORCAMENTO_BASE_CONSOLIDADO.csv
       ├── 03_PLANEJAMENTO_E_CRONOGRAMA/
       │    ├── TEMPLATE_CRONOGRAMA_MASTER.csv
       │    └── TEMPLATE_LINHA_DE_BALANCO.csv
       ├── 04_PRODUCAO_E_AVANCO/
       │    └── RDO_[NOME_OBRA].csv
       └── 05_SUPRIMENTOS_E_FINANCEIRO/
            └── FLUXO_CAIXA_[NOME_OBRA].csv
```

---

## 2. Convenção de Nomenclatura de Arquivos

| Padrão | Exemplo | Criado por |
|---|---|---|
| `ORCAMENTO_BASE_CONSOLIDADO.csv` | — | Motor Python (`gerador_orcamento_mestre.py`) |
| `QUANTITATIVO_[DISC].csv` | `QUANTITATIVO_ARQ.csv` | Motor Python |
| `MEMORIA_CALCULO_[DISC].md` | `MEMORIA_CALCULO_ARQUITETURA.md` | Motor Python |
| `RDO_[NOME_OBRA].csv` | `RDO_TMULT.csv` | Alimentado manualmente |
| `FLUXO_CAIXA_[NOME_OBRA].csv` | `FLUXO_CAIXA_TMULT.csv` | Alimentado manualmente |

**Regra:** Nomes em MAIÚSCULAS com underscores. Nunca usar espaços. Nunca usar acentos em nomes de arquivo.

---

## 3. Schemas dos CSVs

> **Separador:** `;` (ponto e vírgula) — padrão ABNT/Brasil  
> **Encoding:** UTF-8  
> **Primeira linha:** Cabeçalho com os nomes das colunas  
> **Valores vazios:** String vazia `""` — nunca `null` ou `N/A` nos CSVs de produção

### 3.1 `ORCAMENTO_BASE_CONSOLIDADO.csv`

Consumido por: `TabelaOrcamento.tsx`, dashboard de orçamento.

| Coluna | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `CIA` | string | ✅ | Código de Identificação de Ambiente (ex: `T-101-SAL`) |
| `PAVIMENTO` | string | ✅ | Ex: `Térreo`, `Tipo 01`, `Cobertura` |
| `UNIDADE` | string | ✅ | Ex: `Ap 101`, `Área Comum` |
| `AMBIENTE` | string | ✅ | Ex: `Sala de Estar`, `Banheiro Social` |
| `DISCIPLINA` | string | ✅ | `Fundações`, `Estrutura`, `Arquitetura`, `Elétrica`, `Hidráulica` |
| `SERVICO` | string | ✅ | Ex: `Emboço de Paredes`, `Piso Porcelanato 60×60` |
| `INSUMO` | string | ✅ | Nome do material ou serviço |
| `QUANTIDADE` | number | ✅ | Quantidade calculada (2 casas decimais) |
| `UNIDADE_MEDIDA` | string | ✅ | `m²`, `m³`, `kg`, `m`, `unid`, `sc`, `lata`, `rolo` |
| `QUANTIDADE_UCC` | number | ✅ | Quantidade arredondada para cima na UCC comercial |
| `UNIDADE_UCC` | string | ✅ | Ex: `saco 50kg`, `caixa`, `barra 12m` |
| `PRECO_UNIT` | number | ❌ | Preço unitário (preenchido pelo engenheiro com SINAPI/cotação) |
| `CUSTO_TOTAL` | number | ❌ | `QUANTIDADE_UCC × PRECO_UNIT` |
| `TAXA_PERDA` | string | ✅ | Ex: `10%`, `5%` |
| `FONTE_PRECO` | string | ❌ | Ex: `SINAPI 09/2026`, `Cotação Fornecedor X` |

**Valores de STATUS válidos:** `LEVANTADO`, `PENDENTE_RFI`, `NAO_LEVANTADO`

---

### 3.2 `RDO_[NOME_OBRA].csv`

Consumido por: página `/dashboard/rdo`.

| Coluna | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `DATA` | string | ✅ | Formato `YYYY-MM-DD` |
| `CLIMA` | string | ✅ | `Sol`, `Nublado`, `Chuva_Parcial`, `Chuva_Total` |
| `CIA` | string | ✅ | Código do ambiente onde o serviço foi executado |
| `SERVICO` | string | ✅ | Descrição do serviço executado |
| `QUANTIDADE_MEDIDA` | number | ✅ | Quantidade fisicamente medida no dia (Regra da Trena) |
| `UNIDADE_MEDIDA` | string | ✅ | `m²`, `m³`, etc. |
| `EFETIVO_FRENTE` | number | ✅ | Número de trabalhadores alocados nesta frente |
| `HORAS_TRABALHADAS` | number | ✅ | Horas de trabalho da frente no dia |
| `RUP_DIA` | number | ❌ | Calculado: `(EFETIVO × HORAS) / QUANTIDADE_MEDIDA` |
| `EMPREITEIRO` | string | ✅ | Nome da empresa/equipe responsável |
| `IMPEDIMENTO` | string | ❌ | Descrição do impedimento (se houver) |

**Regra crítica:** `QUANTIDADE_MEDIDA` NUNCA pode ser estimativa visual — deve ser medição física. Se não medido, deixar `0` e registrar no campo `IMPEDIMENTO`.

---

### 3.3 `TEMPLATE_CRONOGRAMA_MASTER.csv`

Consumido por: Curva S e dashboard de planejamento.

| Coluna | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `ID_ATIVIDADE` | string | ✅ | Ex: `A001`, `A002` |
| `DESCRICAO` | string | ✅ | Nome da atividade |
| `DISCIPLINA` | string | ✅ | `Estrutura`, `Arquitetura`, etc. |
| `PREDECESSORA` | string | ❌ | ID da atividade predecessora |
| `DATA_INICIO_PLAN` | string | ✅ | Formato `YYYY-MM-DD` |
| `DATA_FIM_PLAN` | string | ✅ | Formato `YYYY-MM-DD` |
| `DATA_INICIO_REAL` | string | ❌ | Real — pode ser vazio se não iniciado |
| `DATA_FIM_REAL` | string | ❌ | Real — pode ser vazio se não concluído |
| `DURACAO_PLAN_DIAS` | number | ✅ | Dias úteis planejados |
| `AVANCO_PLAN_PCT` | number | ✅ | Avanço físico planejado acumulado (0 a 100) |
| `AVANCO_REAL_PCT` | number | ✅ | Avanço físico real medido (0 a 100) |
| `PESO_PCT` | number | ✅ | Peso relativo da atividade no total da obra (0 a 100, soma = 100) |
| `CAMINHO_CRITICO` | string | ✅ | `SIM` ou `NÃO` |

---

### 3.4 `FLUXO_CAIXA_[NOME_OBRA].csv`

Consumido por: dashboard financeiro.

| Coluna | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `DATA` | string | ✅ | Formato `YYYY-MM-DD` |
| `TIPO` | string | ✅ | `RECEITA` ou `DESPESA` |
| `CATEGORIA` | string | ✅ | Ex: `Material`, `Mão de Obra`, `Serviço Terceiro`, `Honorário PMO` |
| `DESCRICAO` | string | ✅ | Descrição do lançamento |
| `VALOR` | number | ✅ | Valor em reais (positivo para receita, positivo para despesa — o TIPO separa) |
| `STATUS` | string | ✅ | `PREVISTO`, `REALIZADO`, `CANCELADO` |
| `NF_NUMERO` | string | ❌ | Número da Nota Fiscal vinculada |
| `FORNECEDOR` | string | ❌ | Nome do fornecedor/empreiteiro |

---

### 3.5 `PROGRAMACAO_CURTO_PRAZO_[OBRA].csv`

Consumido por: `TremDeProducaoLean.tsx`, `page.tsx` (aba Curto Prazo / Lotes), API `/api/cronograma`.  
Localização: `projetos/[NOME_OBRA]/03_PLANEJAMENTO_E_CRONOGRAMA/`.

| Coluna | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `COD_LOTE` | string | ✅ | Identificador determinístico do lote (ex: `LOTE-001` a `LOTE-052`) |
| `SEMANA` | string | ✅ | Semana de produção (ex: `Semana 01` a `Semana 26`) |
| `DIAS_SEMANA` | string | ✅ | Numeração de dias CPM e dias da semana (ex: `Dias 125 a 127 (Ter-Qui)`) |
| `DATA_INICIO` | string | ✅ | Data de início de calendário no formato `DD/MM/AAAA` |
| `DATA_FIM` | string | ✅ | Data de conclusão de calendário no formato `DD/MM/AAAA` |
| `ETAPA_ZONA` | string | ✅ | Zona física ou etapa construtiva (ex: `Etapa 1 (Zona 1 - Recepção/Diretoria)`) |
| `VAGAO_ESTEIRA` | string | ✅ | Nome do vagão Lean (ex: `Vagão 10: Pisos & Porcelanato`) |
| `SERVICO_LOTE` | string | ✅ | Descrição técnica da meta de serviço |
| `META_FISICA` | string | ✅ | Meta quantitativa mensurável (ex: `90 m² porcelanato 60x60 com dupla colagem`) |
| `DURACAO_DIAS` | number | ✅ | Duração da frente no ciclo takt em dias úteis (ex: `3`, `5`) |
| `EQUIPE_PREVISTA` | string | ✅ | Composição da equipe (ex: `3 Ladrilhistas + 3 Ajudantes (SUB-05)`) |
| `HEADCOUNT_PREVISTO` | number | ✅ | Número absoluto de operários alocados na frente |
| `EQUIPAMENTOS_PREVISTOS` | string | ❌ | Maquinários necessários (ex: `Cortadora elétrica + Ventosas`) |
| `MATERIAIS_UCC` | string | ✅ | Insumos principais e embalagem UCC (ex: `Porcelanato 60x60 + AC-III`) |
| `RUP_META_HH_UNID` | string | ✅ | Meta de produtividade RUP (ex: `0,70 HH/m²`) |
| `STATUS_EXECUCAO` | string | ✅ | `PROGRAMADO`, `EM_ANDAMENTO`, `CONCLUIDO`, `ATRASADO` |
| `RDO_VINCULADO` | string | ❌ | Código do RDO que apontou a execução |

---

### 3.6 `LINHA_DE_BALANCO.csv`

Consumido por: `LinhaDeBalanco.tsx`, `TremDeProducaoLean.tsx`, API `/api/cronograma`.  
Localização: `projetos/[NOME_OBRA]/03_PLANEJAMENTO_E_CRONOGRAMA/`.

| Coluna | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `LOCAL_PAVIMENTO` | string | ✅ | Setor físico / zona no eixo Y (ex: `Zona 01 - Recepção/Diretoria`, `Zona 04 - Cobertura`) |
| `SEQUENCIA` | number | ✅ | Ordem sequencial de execução (1 a N) |
| `VAGAO` | string | ✅ | Nome canônico do vagão (ex: `10. Pisos & Porcelanato`) |
| `ATIVIDADE` | string | ✅ | Descrição da atividade executiva |
| `EQUIPE_RESPONSAVEL` | string | ✅ | Equipe ou subempreiteiro responsável (ex: `3 Ladrilhistas + 3 Ajudantes (SUB-05)`) |
| `RITMO_DIAS_POR_LOCAL` | number | ✅ | Ritmo de avanço / Takt Time por setor em dias úteis |
| `DATA_INICIO` | string | ✅ | Data de início no setor (`DD/MM/AAAA`) |
| `DATA_FIM` | string | ✅ | Data de término no setor (`DD/MM/AAAA`) |

---

## 4. Regras de Migração de Schema

Quando um schema de CSV muda (nova coluna adicionada, coluna renomeada):

1. **Nunca renomear uma coluna em uso** sem atualizar todos os componentes React que a consomem.
2. **Novas colunas** devem ser adicionadas no final do CSV, nunca no meio — o `csvParser.ts` mapeia por cabeçalho (nome), não por posição, então é seguro adicionar no fim.
3. **Colunas removidas** devem ser marcadas como `DEPRECATED_[nome]` por pelo menos 1 sprint antes de serem excluídas.
4. **Registrar a mudança** no histórico desta skill com: data, coluna alterada e motivo.

---

## 5. Edge Cases e Tratamento de Erro no Dashboard

O `csvParser.ts` atual retorna `[]` em caso de erro de leitura. Os componentes React DEVEM:

| Situação | Comportamento esperado |
|---|---|
| CSV vazio (0 linhas de dado) | Exibir estado vazio com mensagem "Sem dados para esta obra" |
| Coluna ausente no CSV | Não quebrar — usar valor `""` (padrão do parser) e tratar como vazio |
| Valor numérico como string `""` | Converter com `parseFloat(val) || 0` — nunca deixar `NaN` vazar para a UI |
| CSV com encoding diferente de UTF-8 | Exibir erro amigável "Arquivo com encoding inválido" |
| Arquivo CSV não encontrado | `csvParser` retorna `[]` — componente exibe estado vazio |
