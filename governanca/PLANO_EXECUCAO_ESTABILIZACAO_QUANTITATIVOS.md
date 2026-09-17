# Plano de Execucao — Estabilizacao do Motor de Quantitativos

## Objetivo

Transformar o módulo de quantitativos em uma arquitetura multiobra, auditável e determinística. Dados e resultados pertencem exclusivamente ao SQLite da obra; skills e código guardam somente regras, contratos e lógica reutilizável.

## Regra de condução

Somente uma fase fica ativa por vez. Ao encerrá-la, é obrigatório registrar: escopo executado, decisões, arquivos modificados, testes, riscos e pré-requisitos da fase seguinte. Não iniciar a fase seguinte sem o portão da anterior.

## Fase 0 — Baseline e inventário

**Escopo**

- Inventariar skills quantitativas, código do motor, schema, API, exportadores e testes.
- Registrar hashes dos arquivos em escopo e o comportamento atual comprovado pelos testes.
- Identificar contratos implícitos e dados específicos de obra embutidos no sistema.

**Saídas**

- Registro de baseline e relatório de riscos.
- Conjunto mínimo de testes de regressão preservado.

**Portão**

- Nenhuma mudança funcional; baseline revisado.

## Fase 1 — Auditoria e saneamento das skills

**Escopo**

- Revisar Master, Skills 01–06, auditoria, composição, compras e conciliação.
- Classificar cada conteúdo como regra técnica, template, exemplo fictício, preço externo ou dado contaminante.
- Remover ou neutralizar dados específicos de obra, resultados reais, preços apresentados como regra e exemplos reutilizáveis.
- Separar estritamente quantitativo físico de perdas, UCC, insumos e composição de preço.
- Registrar ambiguidades técnicas para decisão do engenheiro responsável.

**Saídas**

- Matriz `skill × regra × fórmula × dado obrigatório × unidade × RFI × EAP`.
- Skills saneadas e changelog de decisão.

**Portão**

- Cada exemplo numérico é marcado como fictício ou removido; nenhuma regra operacional contém dado de obra.

## Fase 2 — Contrato de dados de engenharia

**Escopo**

- Definir modelos normalizados de elemento, dimensão, unidade, CIA, EAP, evidência, confiança e RFI.
- Definir entrada e saída obrigatórias para cada disciplina.

**Portão**

- Toda variável de uma fórmula possui origem, unidade e regra de validação.

## Fase 3 — Catálogo de regras executáveis

**Escopo**

- Centralizar fórmulas em catálogo versionado, referenciado pelas skills e EAP.
- Manter parsers restritos à leitura, associação e normalização de evidências.

**Portão**

- Parser não contém fórmula de quantitativo, preço, dimensão padrão ou fallback de obra.

## Fase 4 — Motor de cálculo e validações

**Escopo**

- Gerar expressões literais a partir de regras e dados normalizados.
- Fazer o avaliador AST falhar de modo explícito; dado inválido vira RFI, nunca zero silencioso.
- Preservar expressão, versão de regra e resultado.

**Portão**

- Testes unitários de regra aprovados e sem valores implícitos.

## Fase 5 — Extração de PDF com evidência

**Escopo**

- Leitura multipágina de texto, tabelas, blocos, coordenadas e OCR controlado.
- Cobertura de detalhes/callouts e relacionamento explícito de pranchas.

**Portão**

- Nenhum campo usado em cálculo é aceito sem evidência verificável.

## Fase 6 — Fundação piloto

**Escopo**

- Aplicar as fases 2–5 a sapatas, blocos, estacas, baldrames, radier e movimento de terra.
- Validar EAP 1.3, portões de qualidade e memórias completas.

**Portão**

- Casos aprovados por engenharia: PDF → evidência → elemento → expressão → SQLite → artefatos.

## Fase 7 — SQLite, API e artefatos derivados

**Escopo**

- Evoluir schema e API para evidência, regra, revisão e controle multiobra.
- Gerar Excel, CSV e Markdown exclusivamente do SQLite.

**Portão**

- Reimportação não é destrutiva sem autorização; nenhum resultado é persistido no código.

## Fase 8 — Escala por disciplina

Ordem: Estrutura → Arquitetura/Vedação → Acabamentos/Esquadrias → Fachadas/Externos → Elétrica → Hidráulica → Serviços Especiais.

Cada disciplina repete: auditoria da skill, contrato, regras, parser, testes e homologação.

## Fase 9 — Homologação final

**Escopo**

- Testes unitários, integração, regressão e cenários de RFI.
- Cobertura de prancha, auditoria de trilha e revisão humana das memórias.

**Portão**

- Liberação apenas com expressão, regra, evidência, status e versão em todo item quantitativo.
