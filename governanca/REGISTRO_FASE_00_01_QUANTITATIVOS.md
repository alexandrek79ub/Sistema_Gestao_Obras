# Registro de Execução — Fases 0 e 1

## Estado

- Fase 0: concluída em 2026-09-17.
- Fase 1: concluída em 2026-09-17 após reabertura do escopo.
- Skills de levantamento e documentos de governança foram alterados; nenhum dado de obra foi inserido.

## Baseline

- Skills quantitativas inventariadas: 15 arquivos Markdown.
- Código do motor inventariado: 30 arquivos Python sob `scripts/motor_quantitativos/`.
- Teste de regressão atual: `python -m unittest tests.test_motor_quantitativos -v`, executado a partir de `scripts/`: 5 testes aprovados.
- Compilação Python: `python -m compileall -q motor_quantitativos`: aprovada.
- Último commit no início da fase: `e9e76ef feat: add foundation and structure parsers along with quantitative skill documentation`.

## Achados já confirmados

| Severidade | Local | Achado | Ação da Fase 1 |
|---|---|---|---|
| Crítica | `SKILL_QUANTIFICACAO_MASTER.md` | Exemplos operacionais com pranchas e quantitativos específicos (`DW-2054-*`, 20,36 m, 11,62 m²). | Converter em template neutro ou exemplo explicitamente fictício. |
| Crítica | `SKILL_QUANTIFICACAO_MASTER.md` | Modelos de memória incluem perdas, arame e insumos dentro do quantitativo físico. | Remover do Master; remeter a composição/preço ou compras. |
| Média | `SKILL_QUANT_01_FUNDACOES.md` | Exemplo numérico completo pode ser reutilizado indevidamente como dado de projeto. | Adicionar selo fictício e separar de instruções executáveis. |
| Média | `SKILL_QUANTIFICACAO_COMPOSICAO_PRECO.md` | Preços e BDI datados em exemplo. | Tornar inequivocamente didático ou migrar para base de preço versionada. |
| Baixa | `SKILL_QUANT_03C_FACHADAS_E_EXTERNOS.md` | Referência de prancha `AÇU-3.DES-A100` no template. | Substituir por placeholder neutro. |
| Controlada | `SKILL_QUANT_04_ELETRICA.md` | Exemplo numérico de compra/UCC já está identificado como fictício. | Preservar a proteção e isolar do fluxo de quantitativo líquido. |
| Crítica | `SKILL_QUANT_03A_ALVENARIA_E_VEDACAO.md` | Fórmulas de perdas, SKUs, insumos e coeficientes de compra aparecem no fluxo de levantamento físico. | Segregar para composição/BOM e manter no quantitativo somente serviços líquidos. |
| Crítica | `SKILL_QUANT_05_HIDRAULICA.md` | Instrui adicionar 10% de perda ao total medido, contrariando a segregação obrigatória. | Remover do levantamento e remeter à composição/BOM. |
| Alta | `SKILL_QUANT_02_ESTRUTURA.md` | Admite estimar aço sem projeto por taxa média. | Remover; ausência de quadro de ferro deve gerar RFI. |
| Alta | `SKILL_QUANT_05_HIDRAULICA.md` | Teste hidrostático indica 24h, enquanto a cadeia global define 72h. | Resolver a precedência técnica antes de codificar a regra. |

## Achados de arquitetura que dependem das fases posteriores

- `parser_fundacoes.py` contém dimensões, preços, SINAPI e fallback associados a caso de obra.
- O roteador grava projeto fixo e usa fallback de disciplina para fundações.
- O avaliador de expressões retorna `0.0` em erro, mascarando falhas.
- O leitor PDF atual lê somente a primeira página e correlaciona pranchas por padrão de nome limitado.

## Próximo trabalho

Fase 2 iniciada: contrato de dados em `governanca/CONTRATO_DADOS_QUANTITATIVOS.md`.

## Fase 3 — catálogo de regras

- Concluída em 2026-09-17 como primeira versão do catálogo central.
- Registro computável: `scripts/motor_quantitativos/regras/catalogo.py`.
- Documentação: `governanca/CATALOGO_REGRAS_QUANTITATIVOS.md`.
- Regras iniciais cadastradas: 7 de Fundações.
- Verificação: importação, seleção por disciplina e compilação Python aprovadas.
- O catálogo não lê PDF, não acessa SQLite e não contém valores de obra.

## Fase 4 — motor de cálculo

- Concluída em 2026-09-17 como primeira implementação do motor orientado ao catálogo.
- Código: `scripts/motor_quantitativos/calculo/motor_regras.py`.
- `calcular_expressao()` agora bloqueia expressões inválidas; não retorna zero silenciosamente.
- O motor valida campos obrigatórios, tipos numéricos, valores negativos e resultado negativo.
- Testes direcionados de expressão, bloqueio de campo/tipo e regressão do motor: aprovados.

## Fase 5 — extração de evidências

- Concluída em 2026-09-17.
- `LeitorPDFBase` agora percorre todas as páginas e oferece evidências com página, coordenadas, texto original, revisão e confiança.
- Detecção de disciplina passou a considerar o documento inteiro.
- Teste em prancha PDF existente: 1 página, 8 evidências, página máxima validada.
- OCR/tabelas estruturadas e integração com parsers ficam para a Fase 6, sem assumir dados ausentes.

## Fase 6 — piloto de Fundação

- Concluída em 2026-09-17 no trecho extrator → evidência → parser → elemento → regra → resultado.
- `parser_fundacoes_contrato.py` só reconhece dimensões explicitamente presentes na evidência.
- `pipeline_fundacoes.py` gera itens líquidos com EAP, expressão, regra, elemento e evidência.
- Caso sintético `11x S1 (100x100x30 cm)` produziu `11 * 1 * 1 * 0.3 = 3.3 m³`.
- Persistência no SQLite e exportações ficam deliberadamente na Fase 7, para não misturar contrato de dados com migração de schema.

## Fase 7 — persistência e artefatos

- Concluída em 2026-09-17.
- Migração SQLite versão 2 adiciona CIA, tipo/ID do elemento, regra/versão, evidências e revisão da prancha.
- `substituir_quantitativos()` preserva esses metadados e mantém compatibilidade com importações antigas.
- Memória Markdown passa a exibir regra, versão, CIA, elemento e evidências.
- API mantém auditoria e controle otimista de versão.
- Regressão: 5 testes aprovados; compilação Python e `git diff --check` aprovados.

## Fase 8 — escala por disciplina

- Concluída em 2026-09-17 no nível de catálogo e contrato.
- Catálogo ampliado para 14 regras em 6 disciplinas: Fundações, Estrutura, Arquitetura, Elétrica, Hidráulica e Serviços Especiais.
- Matriz de escala: `governanca/MATRIZ_DISCIPLINAS_QUANTITATIVOS.md`.
- Regressão, compilação e verificação de registro de regras aprovadas.
- A conversão de cada parser legado para `ElementRecord` permanece como trabalho de integração/homologação da Fase 9.

## Reabertura da Fase 1 — escopo corrigido

- Incluídas formalmente todas as skills do levantamento físico: Master, 01–06 e Auditoria e Correção.
- Composição, orçamentação, compras e conciliação permanecem fora do escopo direto; serão apenas interfaces posteriores.
- Fase 1A, 1B e 1C concluídas: Master, Skills 01–06 e Auditoria e Correção.

### Encerramento da revisão integral da Fase 1 (2026-09-17)

- Escopo confirmado: Master, Skills 01–06 (incluindo 03A, 03B e 03C) e Auditoria e Correção.
- Composição de preço, orçamentação, pedido de compra e conciliação 3 pontas ficaram fora da execução direta; suas interfaces foram verificadas apenas para impedir retorno de perdas, UCC, embalagens e insumos ao quantitativo físico.
- Master: modelos numéricos tratados como fictícios; tabela de compras identificada como interface BOM/CPU; matriz de cobertura limitada a elementos e serviços executivos.
- Skills 01–03C: mantida a exigência de evidência de prancha, RFI quando faltar dado e quantidade líquida sem contaminação.
- Skills 04–06: reforçada a separação entre serviço físico e BOM/UCC; consumíveis e perdas não alimentam `itens_quantitativo`.
- Auditoria e Correção: certificado convertido em modelo não aprovado; o status deve ser preenchido por obra somente após evidências e revisão.
- Portão: `git diff --check` aprovado e regressão `python -m unittest tests.test_motor_quantitativos -q` aprovada (5 testes).
- Correção posterior: as Skills 03A e 03B foram reescritas para remover fórmulas operacionais de perdas, SKUs, consumos, coeficientes, insumos e UCC. Permanecem apenas regras de medição física líquida, evidência e RFI.
- Correção posterior: a Skill 01 Fundações foi reescrita sem resultados, nomes de elementos, pranchas ou dimensões de obra. Permaneceram apenas EAP, regras de evidência e fórmulas simbólicas.

## Fase 9 — início da homologação e bloqueios do legado

- Removido fallback que injetava dimensões fictícias no `parser_estrutura.py`.
- Removido fallback do roteador que classificava disciplina desconhecida como Fundação.
- Criado `parser_contrato.py` para validar identidade, status, evidência e ocorrência de `ElementRecord`.
- Compilação, teste de contrato e regressão atual aprovados.
- Fase ainda não encerrada: faltam converter os parsers legados de Estrutura, Arquitetura e Instalações e ligá-los ao SQLite.

### Fase 9 — conversão disciplinar (subetapa concluída)

- Criados parsers contratuais para Estrutura, Arquitetura e Instalações em `parsers_contrato.py`.
- Criado `quantificador_contrato.py`, que liga tipos de elemento às regras versionadas.
- Teste sintético cobriu pilar, viga, parede, eletroduto e tubulação, com cinco resultados determinísticos.
- Persistência dos itens disciplinares e Serviços Especiais ainda pendente.

### Fase 9C — persistência e artefatos (subetapa concluída)

- `persistir_itens_quantificados()` grava itens contratuais no SQLite com regra, versão, CIA/elemento e evidências.
- Adaptador de Serviços Especiais por área foi adicionado ao parser contratual.
- Homologação sintética gerou itens no SQLite e regenerou CSV, Excel e Markdown.
- Regressão de 5 testes, compilação e verificação de diff aprovadas.

### Fase 9D — homologação real (em andamento)

- Cinco PDFs reais foram lidos sem erro, com evidências multipágina/por bloco.
- A prancha `EGS-051` produziu 73 evidências, mas nenhuma sapata foi reconhecida pelo padrão contratual; nenhum quantitativo foi inventado.
- Pranchas `DW-*` foram classificadas como `GENERICA`, indicando que a detecção precisa de selo/metadado ou disciplina informada explicitamente.
- O próximo ajuste deve tratar blocos CAD fragmentados e classificação por acervo, mantendo o bloqueio quando a evidência não for suficiente.

### Fase 9D — homologação final

- Reconstrução de blocos CAD normaliza espaços e remove duplicação de elementos.
- Prancha real `EGS-051` reconheceu 24 pilares com dimensões explícitas e altura derivada de cotas documentadas.
- Itens não reconhecidos permanecem sem quantitativo, evitando falsos positivos.
- Compilação e regressão aprovadas após o ajuste.
- Fase 9 encerrada; padrões de prancha sem evidência suficiente devem seguir fluxo de RFI, não fallback.
