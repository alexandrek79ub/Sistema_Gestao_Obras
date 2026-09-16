# 📊 SKILL: Schema dos CSVs e Estrutura de Dados do Sistema

> **Frente:** Desenvolvimento (`SKILL_DEV_SENIOR.md`)
> **Propósito:** O SQLite é a fonte única da verdade; os CSVs são exportações consumidas pelo Dashboard Next.js.

## 1. Arquitetura de dados

O banco oficial é `data/pmo_virtual.sqlite`. Os documentos e exportações continuam organizados por obra em `/projetos/[NOME_OBRA]/` e usam `;` como separador e UTF-8.
Valores ausentes são strings vazias; nunca usar `null` ou `N/A` nos arquivos de produção.

## 2. Orçamento base, quantitativo e EAP

`itens_quantitativo` no SQLite é o contrato comum entre EAP, quantitativo físico e Dashboard.
`ORCAMENTO_BASE_CONSOLIDADO.csv` é apenas uma exportação derivada.
Cada linha é um serviço da EAP, com quantidade nominal líquida. Insumos miúdos, perdas,
empolamento e arredondamentos comerciais não pertencem a este arquivo.

| Coluna | Tipo | Obrigatório | Regra |
|---|---|---:|---|
| `COD_EAP` | string | sim | Código hierárquico do serviço, ex.: `1.3.11` |
| `DESCRICAO_DO_SERVICO` | string | sim | Serviço executivo; não material derivado |
| `DISCIPLINA` | string | sim | Fundação, Estrutura, Arquitetura, Elétrica, Hidráulica etc. |
| `UNIDADE` | string | sim | `m²`, `m³`, `kg`, `m`, `un` |
| `QUANTIDADE_TOTAL` | number | sim | Quantidade física líquida da prancha/memória |
| `CUSTO_UNITARIO_BDI` | number/string | não | Custo unitário validado pela composição e fonte de preço |
| `CUSTO_TOTAL` | number/string | não | `QUANTIDADE_TOTAL × CUSTO_UNITARIO_BDI` |
| `EMPREITEIRO_VINCULADO` | string | não | Responsável; padrão `Engenharia` quando não informado |
| `PRANCHA_REFERENCIA` | string | sim | Prancha ou detalhe que fundamenta a quantidade |
| `FONTE_PRECO` | string | não | SINAPI, cotação ou contrato que fundamenta o custo unitário |
| `STATUS` | string | sim | `LEVANTADO`, `PENDENTE_RFI` ou `NAO_LEVANTADO` |
| `CODIGO_SINAPI` | string | não | Composição SINAPI vinculada ao item de orçamento; não pertence ao quantitativo físico |
| `CENTRO_CUSTO` | string | não | Classificação financeira do orçamento; não altera EAP nem quantidade líquida |

O código `COD_EAP` é o identificador do serviço para cronograma, medição e consolidação do
orçamento. `CIA`, ambiente e pavimento podem ser mantidos em arquivos analíticos de origem,
mas não substituem o código EAP no consolidado.

### Separação obrigatória de compras

`QUANTIDADE_UCC`, `UNIDADE_UCC` e `TAXA_PERDA` não fazem parte do quantitativo físico nem da
EAP. Quando necessários, são gerados em BOM/lista de compras separada, após a composição de
custos, sem alterar `QUANTIDADE_TOTAL`.

## 3. RDO

`RDO_[NOME_OBRA].csv` usa as colunas: `DATA`, `CLIMA`, `CIA`, `SERVICO`,
`QUANTIDADE_MEDIDA`, `UNIDADE_MEDIDA`, `EFETIVO_FRENTE`, `HORAS_TRABALHADAS`, `RUP_DIA`,
`EMPREITEIRO`, `IMPEDIMENTO`. `QUANTIDADE_MEDIDA` deve ser física; se não houver medição,
usar `0` e registrar o impedimento.

## 4. Cronograma

`TEMPLATE_CRONOGRAMA_MASTER.csv` usa `ID_ATIVIDADE`, `DESCRICAO`, `DISCIPLINA`,
`PREDECESSORA`, `DATA_INICIO_PLAN`, `DATA_FIM_PLAN`, `DATA_INICIO_REAL`, `DATA_FIM_REAL`,
`DURACAO_PLAN_DIAS`, `AVANCO_PLAN_PCT`, `AVANCO_REAL_PCT`, `PESO_PCT` e `CAMINHO_CRITICO`.

`TEMPLATE_LINHA_DE_BALANCO.csv` usa `LOCAL_PAVIMENTO`, `SEQUENCIA`, `ATIVIDADE`,
`EQUIPE_RESPONSAVEL`, `RITMO_DIAS_POR_LOCAL`, `DATA_INICIO` e `DATA_FIM`.

## 5. Fluxo de caixa

`FLUXO_CAIXA_[NOME_OBRA].csv` usa `DATA`, `TIPO`, `CATEGORIA`, `DESCRICAO`, `VALOR`,
`STATUS`, `NF_NUMERO` e `FORNECEDOR`.

## 6. Regras de compatibilidade

1. O motor Python deve gerar exatamente o cabeçalho do orçamento definido na Seção 2.
2. O Dashboard deve consumir os nomes canônicos, sem depender de cabeçalhos legados.
3. Novas colunas entram no final e devem ser registradas nesta skill antes do uso.
4. Nenhuma coluna de perdas/UCC pode ser usada para alterar a quantidade física do projeto.
5. Alterações de schema exigem atualização do parser, das rotas, dos componentes e dos testes.
6. A API exige versão esperada, justificativa e chave local; uma edição gera backup, auditoria e novas exportações.

## 7. Tolerância a falhas no Dashboard

- CSV ausente ou vazio: exibir estado vazio, sem quebrar a página.
- Coluna opcional ausente: usar string vazia.
- Número vazio ou inválido: converter para `0` e sinalizar dado incompleto quando relevante.
- Erro de leitura/encoding: registrar no servidor e retornar mensagem amigável.
