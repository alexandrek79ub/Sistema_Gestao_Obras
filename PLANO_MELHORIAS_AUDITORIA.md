# Plano de Melhorias da Auditoria Técnica

> Documento de transição para implementação segura dos achados da auditoria concluída em 14/09/2026. Este plano consolida exclusivamente o contexto e as evidências já levantados; ele não representa uma nova auditoria.

## 1. Objetivo e limites

Este documento permite que outro agente, em uma sessão sem o contexto da auditoria, implemente as correções de forma incremental, rastreável e compatível com a governança do repositório.

Escopo deste plano:

- registrar os 14 achados validados na auditoria;
- ordenar as correções por impacto, risco, esforço e dependências;
- definir testes e critérios objetivos de aceite;
- impedir que correções críticas sejam misturadas com refatorações oportunistas.

Fora do escopo:

- realizar nova auditoria global;
- implementar qualquer correção neste documento;
- alterar regras de negócio sem validação explícita das fontes de verdade do repositório;
- modificar dados oficiais de uma obra, baselines ou documentos emitidos sem a autorização exigida pelo `AGENTS.md` e pelo adendo de autonomia.
- introduzir, nesta etapa, infraestrutura SaaS de login, cadastro de usuários, sessões, banco de identidades ou RBAC.

### 1.1 Premissa arquitetural vinculante

Este plano deve ser interpretado segundo o modelo operacional confirmado após a auditoria:

- **agente de IA = operador principal:** Gemini/Codex, no Antigravity, interpreta o pedido, consulta a governança e executa os motores/scripts;
- **motores Python = caminho canônico de escrita:** alterações nos dados das obras devem ocorrer pelos motores universais, sob as regras de autonomia e com trilha no Git;
- **dashboard Next.js = leitura por padrão:** as rotas e telas do cockpit devem visualizar os artefatos produzidos pelos agentes, sem oferecer mutações genéricas dos arquivos da obra;
- **interfaces de campo = exceção explícita:** `/campo` e o PWA podem precisar receber RDO/FVS, mas essa escrita deve ser mínima, segregada e analisada como fluxo próprio;
- **governança = controle de autorização:** ações laranja/vermelhas são autorizadas pela confirmação explícita do usuário na interação com o agente e registradas no Git; não exigem, por si, login ou RBAC no dashboard;
- **segurança local continua obrigatória:** o modelo não SaaS reduz a necessidade de gestão de identidades web, mas não justifica travessia de diretórios, interpolação em shell, escrita fora da obra selecionada ou promoção silenciosa de dados.

Matriz arquitetural alvo:

| Superfície | Papel | Escrita permitida | Controle necessário nesta etapa |
|---|---|---|---|
| `/dashboard` e APIs do cockpit | Visualização | Não, por padrão | Métodos somente leitura, seleção explícita da obra e ausência de fallback cruzado |
| Agentes + CLI Python | Operação principal | Sim | `AGENTS.md`, adendo de autonomia, validação dos motores, confirmação humana quando exigida e commit Git auditável |
| `/campo` e PWA | Coleta operacional | Apenas apontamentos de campo necessários | Payload estrito, obra confinada, staging/fila, idempotência e validação antes de virar registro oficial |
| Baseline oficial | Artefato governado | Somente pelo agente após autorização explícita | Diff/proposta, pausa obrigatória, execução pelo motor e registro no Git |

Consequência prática: nenhum achado deve ser usado para criar preventivamente uma plataforma de autenticação. Se no futuro o sistema for publicado para usuários não confiáveis, essa decisão deverá gerar um plano de segurança próprio.

## 2. Convenções de execução

### 2.1 Prioridades

| Prioridade | Interpretação | Tratamento esperado |
|---|---|---|
| P0 | Integridade, segurança ou governança crítica; pode aprovar, gravar ou exibir informação indevida | Conter imediatamente e corrigir antes de ampliar funcionalidades |
| P1 | Falha funcional relevante, isolamento multiobra, confiabilidade ou perda de dados | Corrigir na sequência das dependências técnicas |
| P2 | Dívida técnica com efeito relevante sobre manutenção e risco de regressão | Executar após proteger o comportamento com testes |

### 2.2 Natureza dos achados

- **Bug confirmado:** o comportamento observado contradiz diretamente a regra esperada.
- **Risco confirmado:** a exposição ou fragilidade existe no código; a ocorrência do dano depende de uso ou exploração.
- **Dívida técnica:** a estrutura atual amplia custo de mudança e probabilidade de regressão.
- **Melhoria:** oportunidade concreta, não tratada isoladamente como defeito.

### 2.3 Status permitidos

Cada item começa como `PENDENTE`. O próximo agente deve usar somente estes estados:

- `PENDENTE` — ainda não iniciado;
- `EM_EXECUCAO` — item autorizado e em implementação;
- `BLOQUEADO` — depende de decisão, dado ou autorização, com motivo registrado;
- `IMPLEMENTADO` — código concluído, ainda sem toda a validação;
- `VALIDADO` — critérios de aceite e testes cumpridos;
- `CANCELADO` — somente por decisão explícita do responsável, registrada no item.

## 3. Ordem recomendada e dependências

Todos os itens exigem testes proporcionais na própria entrega. O item `AUD-014` não deve ser interpretado como autorização para criar antecipadamente uma grande infraestrutura de testes; ele consolida os gates mínimos e é concluído progressivamente.

| Fase | Objetivo | Itens e ordem recomendada | Dependências principais |
|---|---|---|---|
| 0 — Limite leitura/escrita | Retirar mutações genéricas do dashboard e conter promoções automáticas | `AUD-002` → `AUD-006` → contenção de `AUD-001` | Nenhuma; não criar login/RBAC; priorizar remoção ou bloqueio de escrita desnecessária |
| 1 — Contratos de dados e persistência | Criar base segura para isolamento multiobra e para as escritas que permanecerem | `AUD-011` → `AUD-005` → `AUD-012` | A classificação de superfícies definida em `AUD-002` determina onde escrita ainda existe |
| 2 — Regras centrais de planejamento | Corrigir a fonte de verdade da EAP e a confiabilidade dos motores | `AUD-003` → `AUD-007` → `AUD-008` → `AUD-009` | Parser/validação de `AUD-011`; persistência segura de `AUD-012` para mutações |
| 3 — Governança de campo | Corrigir coleta, aprovação de qualidade e emissão de RDO | conclusão de `AUD-001` → `AUD-010` | Fronteira específica de campo (`AUD-002`) e escrita atômica (`AUD-012`) |
| 4 — Veracidade dos painéis | Remover dados plausíveis não derivados das fontes oficiais | `AUD-004` | Contratos explícitos de ausência/erro (`AUD-011`) e seleção multiobra (`AUD-005`) |
| 5 — Sustentação | Reduzir acoplamento e tornar os gates obrigatórios | `AUD-013` → conclusão de `AUD-014` | Comportamentos críticos já cobertos por testes das fases anteriores |

Regra de precedência: se uma correção depender de regra de negócio ainda ambígua, o item deve ficar `BLOQUEADO`; não se deve preencher a lacuna com inferência. Se uma vulnerabilidade impedir testes seguros, a contenção mínima de `AUD-002` precede qualquer trabalho dependente.

## 4. Registro resumido dos achados

| ID | Prioridade | Natureza | Resumo | Status |
|---|---|---|---|---|
| AUD-001 | P0 | Bug confirmado | Fluxo de FVS permite aprovação e desbloqueio sem validação técnica e assinatura válida | IMPLEMENTADO |
| AUD-002 | P0 | Risco confirmado / desalinhamento arquitetural | Dashboard expõe mutações genéricas e execução insegura apesar de ser leitura por padrão | IMPLEMENTADO |
| AUD-003 | P0 | Bug confirmado | Mapeamento de EAP do cronograma está incompatível com a governança oficial | PENDENTE |
| AUD-004 | P0 | Bug confirmado | Painéis operacionais apresentam dados fixos ou demonstrativos como se fossem dados reais | PENDENTE |
| AUD-005 | P1 | Bug confirmado | Seleção da obra não é propagada para EVM e orçamento | PENDENTE |
| AUD-006 | P1 | Bug confirmado / governança | API pode reescrever baseline sem fluxo formal de aprovação e versionamento | IMPLEMENTADO |
| AUD-007 | P1 | Bug confirmado | Orquestrador pode terminar com código zero após falha de etapa obrigatória | PENDENTE |
| AUD-008 | P1 | Bug confirmado | Sincronização dita bidirecional usa a mesma direção e aceita fallback de outra obra | PENDENTE |
| AUD-009 | P1 | Bug confirmado | Exportação MS Project não representa corretamente o CPM calculado | PENDENTE |
| AUD-010 | P1 | Bug confirmado | RDO pode ser emitido com valores presumidos, numeração incorreta e assinatura sem evidência | PENDENTE |
| AUD-011 | P1 | Bug confirmado | Parser CSV simplista mascara erros e não trata CSV válido de forma robusta | PENDENTE |
| AUD-012 | P1 | Risco confirmado | Escritas concorrentes não são atômicas nem protegidas contra perda de atualização | PENDENTE |
| AUD-013 | P2 | Dívida técnica | Módulos gigantes concentram UI, regras, persistência e execução de processos | PENDENTE |
| AUD-014 | P1 | Dívida técnica / qualidade | Não há suíte/CI observada; lint falha e dependências Python não estão declaradas de forma reproduzível | PENDENTE |

## 5. Plano detalhado por achado

### AUD-001 — Aprovação indevida de FVS

- **Prioridade:** P0.
- **Natureza:** bug confirmado.
- **Status:** `IMPLEMENTADO` (contenção da Fase 0; fluxo completo de aprovação permanece para a Fase 3).
- **Problema confirmado:** a interface e o processador aceitam valores padrão capazes de registrar uma FVS como aprovada e liberar medição sem comprovar checklist completo, tolerância medida, responsável identificado e assinatura válida.
- **Evidências e arquivos envolvidos:**
  - `apresentacao_comercial/src/app/campo/page.tsx:79` inicializa o resultado como `Aprovado`;
  - `apresentacao_comercial/src/app/campo/page.tsx:231-236` envia o estado de aprovação, usa responsável fixo e apenas rotula a assinatura como pendente;
  - `apresentacao_comercial/src/app/campo/page.tsx:715-718` bloqueia o envio apenas durante `enviando`;
  - `scripts/processar_coleta_campo.py:330-335` fornece padrões para código, status, responsável, tolerância e observação;
  - `scripts/processar_coleta_campo.py:348-349` libera medição pela presença textual de `Aprovad` no status;
  - `apresentacao_comercial/src/app/api/qualidade/route.ts:201-205` transforma FVS enfileirada em `APROVADO` sem respeitar integralmente o resultado informado.
- **Comportamento atual:** omissões no payload são completadas com valores favoráveis e o status textual pode acionar a liberação de medição.
- **Comportamento esperado:** `/campo` coleta e coloca a FVS em staging como `SUBMETIDA`; somente uma aprovação tecnicamente validada, com código permitido, checklist completo, valores medidos obrigatórios, resultado coerente, responsável explicitamente identificado e assinatura/evidência verificável, pode virar registro oficial e liberar medição. O dashboard de qualidade apenas lê o resultado oficial. Reprovação ou pendência nunca pode ser convertida em aprovação por valor padrão.
- **Estratégia de correção:** definir um contrato de FVS versionado; remover defaults decisórios; validar enumerações e campos obrigatórios na fronteira de campo; separar `RASCUNHO`, `SUBMETIDA`, `REPROVADA` e `APROVADA`; registrar o responsável por campo confirmado/configuração controlada e a evidência correspondente, sem exigir sessão web; fazer o agente/motor validar e promover a submissão conforme governança; tornar o desbloqueio consequência dessa promoção, não de busca textual. Na Fase 0, conter a liberação automática até que o fluxo completo exista.
- **Arquivos que provavelmente precisarão ser alterados:** os três arquivos citados; tipos/validadores compartilhados a serem definidos na arquitetura existente; testes do fluxo de campo e qualidade.
- **Dependências:** `AUD-002` para delimitar a exceção de escrita de `/campo`; `AUD-012` para staging e promoção seguros; `AUD-011` caso o registro final seja consumido de CSV.
- **Riscos de regressão:** bloquear FVS históricas válidas; quebrar compatibilidade com payloads offline; duplicar submissões durante sincronização; alterar indevidamente as regras de medição contratual.
- **Testes necessários:** contrato do payload; campos ausentes; código inválido; tolerância vazia/não numérica; checklist incompleto; identificação ausente; assinatura ausente/inválida; reprovada e pendente; reenvio idempotente; tentativa offline; submissão permanece em staging; integração comprovando que só `APROVADA` promovida pelo fluxo governado libera medição.
- **Critérios objetivos de aceite:**
  1. nenhum campo decisório recebe valor padrão no cliente ou servidor;
  2. submissão incompleta retorna erro explícito e não grava aprovação; submissão válida não nasce aprovada;
  3. `REPROVADA`, `PENDENTE` e `RASCUNHO` não liberam medição;
  4. a aprovação registra ator, obra, data/hora, versão do checklist e evidência de assinatura;
  5. testes automatizados cobrem todas as transições permitidas e proibidas.

### AUD-002 — Superfície de escrita incompatível com dashboard de leitura

- **Prioridade:** P0.
- **Natureza:** risco confirmado de segurança.
- **Status:** `IMPLEMENTADO` (contenção da Fase 0; persistência completa permanece para `AUD-012`).
- **Problema confirmado:** foram observados endpoints de escrita genérica no Next.js, embora o papel principal do dashboard seja leitura. Um deles recebe o nome da obra do cliente, compõe caminhos e executa comando por string. A ausência de login/RBAC não é, por si, o defeito neste modelo; o defeito é manter uma superfície de mutação desnecessária e insegura fora do operador-agente.
- **Evidências e arquivos envolvidos:**
  - `apresentacao_comercial/src/app/api/apontamento-campo/route.ts:12-16` recebe e utiliza `payload.obra`;
  - `apresentacao_comercial/src/app/api/apontamento-campo/route.ts:26-38` deriva caminho, grava temporário e executa comando composto por string;
  - `apresentacao_comercial/src/app/api/cronograma/route.ts:942` inicia endpoint de mutação sem controle de acesso identificado na auditoria;
- **Comportamento atual:** um chamador capaz de alcançar a API pode tentar selecionar obra arbitrária, inclusive com segmentos de travessia, enviar payload e disparar processamento; a composição textual do comando amplia a superfície de injeção. A rota de cronograma também oferece mutação que deveria pertencer ao fluxo agente/CLI.
- **Comportamento esperado:** APIs do dashboard são somente leitura. Mutações de cronograma/baseline são removidas ou desabilitadas e executadas pelo agente via motores. A única exceção web prevista é a coleta estritamente necessária de `/campo`, limitada a staging/fila: identificador de obra validado, caminho canônico confinado a `projetos/`, payload limitado, operação idempotente e sem shell interpolado. Não se exige login, sessão, banco de usuários ou RBAC nesta etapa.
- **Estratégia de correção:** classificar cada rota existente como `LEITURA`, `COLETA_CAMPO` ou `MUTACAO_AGENTE`; eliminar/desabilitar métodos web da terceira categoria; manter apenas a ingestão mínima de campo; centralizar validação de obra e confirmar que o caminho resolvido permanece sob a raiz; substituir execução via shell por chamada segura com argumentos ou, preferencialmente, fazer a rota apenas enfileirar e deixar o agente/motor processar; padronizar erros. Documentar que eventual exposição futura a ambiente não confiável exige revisão própria de autenticação e rede.
- **Arquivos que provavelmente precisarão ser alterados:** rotas citadas; utilitário central de resolução de obra; fronteira de staging da coleta; serviço seguro de execução caso ainda seja indispensável; documentação arquitetural e testes de segurança. Não incluir middleware de login/RBAC sem nova decisão explícita.
- **Dependências:** nenhuma para contenção. Deve anteceder `AUD-001`, `AUD-006`, `AUD-010` e `AUD-012` em produção.
- **Riscos de regressão:** interromper o modo PWA/offline; negar acesso legítimo por configuração incompleta; introduzir incompatibilidade Windows na execução sem shell; vazar dados sensíveis em logs.
- **Testes necessários:** métodos de escrita recusados nas APIs do dashboard; `/campo` aceita somente o contrato de coleta; `..`, caminhos absolutos, separadores alternativos e codificados; obra inexistente; payload grande; repetição idempotente; argumentos com metacaracteres; resposta sem stack trace; confirmação de que a coleta não promove diretamente baseline, FVS ou RDO oficial.
- **Critérios objetivos de aceite:**
  1. APIs do dashboard não expõem mutações de dados de obra;
  2. todo caminho de obra é resolvido por função central e provado contido em `projetos/`;
  3. não há shell construído com entrada do usuário;
  4. testes de travessia e injeção falham de modo seguro, sem criar arquivos nem processos indevidos;
  5. a exceção `/campo` grava somente staging/fila e toda promoção oficial posterior fica registrada pelo agente/motor no Git;
  6. nenhuma infraestrutura de login, sessão, banco de usuários ou RBAC é adicionada por este item.

### AUD-003 — Mapeamento de EAP incompatível com a governança

- **Prioridade:** P0.
- **Natureza:** bug confirmado.
- **Status:** `PENDENTE`.
- **Problema confirmado:** o gerador de cronograma interpreta prefixos da EAP segundo uma taxonomia antiga, divergente da cadeia oficial e enviando códigos oficiais relevantes para uma distribuição genérica.
- **Evidências e arquivos envolvidos:**
  - `governanca/INDICE_MESTRE_SKILLS.md:50-57` define, entre outros, 1.1 preliminares, 1.2 terraplenagem, 1.3 fundações, 1.4 estrutura e 2.2 acabamentos;
  - `scripts/gerar_cronograma.py:81-87` trata 1.1 como infraestrutura e 1.2 como superestrutura;
  - `scripts/gerar_cronograma.py:121-123` trata 2.2 como cobertura;
  - `scripts/gerar_cronograma.py:148-150` envia códigos não reconhecidos ao período intermediário;
  - o parâmetro `regras_custom` declarado no fluxo não estava efetivamente aplicado no comportamento auditado.
- **Comportamento atual:** códigos oficiais como 1.3 e 1.4 podem cair na regra genérica, enquanto códigos reconhecidos recebem disciplina/período incorretos.
- **Comportamento esperado:** uma única fonte versionada da EAP deve definir disciplina, hierarquia, predecessoras, portões e regra de distribuição para todos os motores e consumidores.
- **Estratégia de correção:** modelar catálogo canônico da EAP conforme o Índice Mestre; fazer os motores consumirem esse catálogo; rejeitar ou sinalizar código desconhecido, nunca posicioná-lo silenciosamente; implementar explicitamente os quatro portões interdisciplinares; remover regras obsoletas somente após teste de migração.
- **Arquivos que provavelmente precisarão ser alterados:** `scripts/gerar_cronograma.py`; módulo compartilhado novo ou existente para EAP; motores de cronograma que duplicarem o mapa; schemas/configurações de obra; testes.
- **Dependências:** `AUD-011` para leitura validada de fontes tabulares; precede `AUD-007`, `AUD-008` e `AUD-009`.
- **Riscos de regressão:** reclassificar itens históricos; alterar datas e curvas existentes; quebrar obras com códigos legados; introduzir ciclos em precedências.
- **Testes necessários:** códigos 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 3.1 e 3.2; código desconhecido; compatibilidade/migração de obra existente; DAG acíclico; quatro portões oficiais; comparação controlada das saídas antes/depois.
- **Critérios objetivos de aceite:**
  1. há uma única fonte de verdade programática para a EAP;
  2. todos os códigos oficiais testados são classificados conforme o Índice Mestre;
  3. código desconhecido gera diagnóstico explícito;
  4. os quatro portões oficiais possuem testes automatizados;
  5. nenhuma regra obsoleta de prefixo permanece ativa em paralelo.

### AUD-004 — Dados demonstrativos apresentados como operação real

- **Prioridade:** P0.
- **Natureza:** bug confirmado.
- **Status:** `PENDENTE`.
- **Problema confirmado:** APIs e geradores retornam indicadores plausíveis fixos ou derivados de premissas específicas da OBRA_TMULT sem distinguir demonstração, ausência de dados e informação oficial da obra selecionada.
- **Evidências e arquivos envolvidos:**
  - `apresentacao_comercial/src/app/api/evm/route.ts:40-48` monta percentuais EVM fixos;
  - `apresentacao_comercial/src/app/api/financeiro/route.ts:122` mantém 12 medições pré-definidas e, em `:141`, KPIs fixos da TMULT;
  - `apresentacao_comercial/src/app/api/qualidade/route.ts:42` define coleção fixa, incluindo estados aprovados em `:51` e `:71`;
  - `apresentacao_comercial/src/app/api/sst/route.ts:60` fornece pessoas, datas e conformidades fixas;
  - `apresentacao_comercial/src/app/api/databook/route.ts:33-36` resolve diretório, mas retorna estrutura/progresso fixos;
  - `scripts/gerar_fluxo_caixa.py:70-75`, `:89-92` e `:128-134` contém caso específico da TMULT e fallback de custos/partição 35%–65%; uma obra sem parâmetros correspondentes pode herdar essas premissas.
- **Comportamento atual:** a ausência de fonte pode produzir números e estados que parecem oficiais, criando risco de decisão gerencial incorreta.
- **Comportamento esperado:** indicadores operacionais devem ser calculados exclusivamente das fontes da obra ativa. Ausência, inconsistência ou indisponibilidade deve aparecer como estado explícito (`SEM_DADOS`, `INCOMPLETO` ou erro); modo demonstração deve ser separado e visualmente identificado.
- **Estratégia de correção:** inventariar por endpoint a fonte oficial já definida no repositório; criar contrato comum de proveniência e estado; remover fallbacks específicos de outra obra; parametrizar premissas legítimas em `config_obra.json` com validação; separar fixtures de demonstração do caminho produtivo; mostrar data/fonte no painel.
- **Arquivos que provavelmente precisarão ser alterados:** cinco rotas citadas; `scripts/gerar_fluxo_caixa.py`; componentes consumidores; schemas/configurações; fixtures e testes.
- **Dependências:** `AUD-005` para selecionar a obra correta; `AUD-011` para distinguir dado ausente de inválido; `AUD-003` quando indicadores dependerem da EAP.
- **Riscos de regressão:** painéis ficarem vazios onde antes exibiam demo; mudança de contrato de API; resultados históricos divergirem por remoção de premissas ocultas; confundir dado zero com ausência.
- **Testes necessários:** obra completa; obra nova/vazia; arquivo ausente; schema inválido; duas obras com dados divergentes; modo demo explicitamente habilitado; ausência de vazamento TMULT; proveniência e data de atualização.
- **Critérios objetivos de aceite:**
  1. nenhuma rota produtiva retorna fixture ou valor específico de outra obra como dado real;
  2. ausência e erro são distinguíveis de zero;
  3. cada indicador expõe fonte/proveniência suficiente para auditoria;
  4. modo demo, se mantido, exige ativação explícita e rótulo visível;
  5. testes com duas obras provam isolamento e resultados distintos.

### AUD-005 — Obra ativa não propagada para EVM e orçamento

- **Prioridade:** P1.
- **Natureza:** bug confirmado.
- **Status:** `PENDENTE`.
- **Problema confirmado:** consumidores relevantes não enviam a obra ativa nas consultas, embora exista `ObraContext` e outras telas já adotem esse padrão.
- **Evidências e arquivos envolvidos:**
  - `apresentacao_comercial/src/components/TabelaOrcamento.tsx:12` consulta `/api/orcamento` sem `obra`;
  - `apresentacao_comercial/src/app/dashboard/page.tsx:15` consulta `/api/evm` sem `obra`;
  - o contexto `useObra()` já existe e é utilizado em outras páginas auditadas.
- **Comportamento atual:** trocar a obra no seletor pode manter orçamento/EVM obtidos de um default implícito ou de contexto divergente.
- **Comportamento esperado:** toda consulta dependente de obra recebe um identificador validado, recarrega ao trocar a seleção e nunca usa silenciosamente outra obra.
- **Estratégia de correção:** centralizar cliente/hook de API por obra; incluir `encodeURIComponent(obraAtiva)` ou mecanismo equivalente; usar a obra na chave de cache; cancelar/ignorar resposta obsoleta após troca; exigir o parâmetro também no servidor.
- **Arquivos que provavelmente precisarão ser alterados:** os dois consumidores citados; contexto/hook compartilhado; rotas `/api/orcamento` e `/api/evm`; testes de interface e API.
- **Dependências:** `AUD-002` para consolidar o dashboard como leitura e validar a obra solicitada; `AUD-011` para contrato de erro/ausência. Precede `AUD-004`.
- **Riscos de regressão:** loops de fetch; corrida em troca rápida; cache cruzado; nomes com espaços/caracteres especiais; tela inicial sem obra carregada.
- **Testes necessários:** troca A→B; retorno tardio de A após selecionar B; obra inexistente; caracteres especiais; ausência de seleção; cache isolado; rejeição servidor sem parâmetro.
- **Critérios objetivos de aceite:**
  1. EVM e orçamento sempre incluem a obra ativa na requisição;
  2. o servidor rejeita obra ausente/inválida, sem fallback cruzado;
  3. trocar a obra atualiza os dois painéis e não reutiliza resposta da obra anterior;
  4. teste automatizado com duas obras comprova isolamento.

### AUD-006 — Mutação direta da baseline sem aprovação formal

- **Prioridade:** P1, com contenção na Fase 0.
- **Natureza:** bug confirmado de governança.
- **Status:** `IMPLEMENTADO` (método web bloqueado; proposta, promoção versionada e trilha Git continuam pendentes das fases dependentes).
- **Problema confirmado:** a API de cronograma reescreve a Linha de Balanço e aciona o orquestrador, mas a governança classifica alteração de baseline como ação vermelha, nunca autônoma.
- **Evidências e arquivos envolvidos:**
  - `apresentacao_comercial/src/app/api/cronograma/route.ts:942` expõe a mutação;
  - `apresentacao_comercial/src/app/api/cronograma/route.ts:1187-1205` regrava a LOB;
  - `apresentacao_comercial/src/app/api/cronograma/route.ts:1207-1222` chama o orquestrador após a escrita;
  - `governanca/ADENDO_AGENTS_REGRAS_DE_AUTONOMIA.md:24` classifica alteração de baseline como não autônoma.
- **Comportamento atual:** uma ação na API pode sobrescrever o artefato tratado como oficial antes de registrar aprovação, motivo e versão anterior.
- **Comportamento esperado:** o dashboard apenas visualiza cronograma e baseline. O agente gera uma proposta/diff por CLI, pausa conforme o adendo e só promove nova baseline depois da confirmação explícita do usuário na conversa. O commit Git registra motivo, versão e vínculo com a anterior. Não é necessário construir tela de aprovação, sessão ou serviço de identidade.
- **Estratégia de correção:** remover/desabilitar a escrita direta da rota; manter `proposta` separada da baseline; fazer o agente executar `proposta` → validação técnica → pausa para confirmação → promoção pelo motor → commit auditável. Versionar ou preservar o artefato anterior de modo compatível com a governança existente. A confirmação conversacional e o Git são os mecanismos de autorização e trilha nesta arquitetura.
- **Arquivos que provavelmente precisarão ser alterados:** rota de cronograma; motores/serviços de orquestração e persistência; convenção de proposta/metadados de baseline; instruções do agente se necessário; testes. Não criar UI de aprovação ou cadastro de usuários.
- **Dependências:** `AUD-002` para retirar a mutação do dashboard; `AUD-012` para promoção atômica; `AUD-007` para resultado confiável do orquestrador.
- **Riscos de regressão:** quebrar fluxo de edição operacional; duplicar versões; promover conjunto parcial; incompatibilidade com arquivos legados sem metadados.
- **Testes necessários:** POST/mutação recusada no dashboard; criação de proposta sem alterar baseline; diff; ausência de confirmação impede promoção; confirmação explícita seguida de promoção pelo motor; promoção única/idempotente; falha no meio com rollback; commit/trilha completa.
- **Critérios objetivos de aceite:**
  1. nenhuma chamada comum da API sobrescreve a baseline oficial;
  2. toda promoção exige confirmação humana explícita registrada no contexto do agente e commit Git correspondente;
  3. versão anterior permanece recuperável;
  4. falha de validação/orquestração impede promoção;
  5. teste confirma que proposta rejeitada não altera qualquer arquivo oficial.

### AUD-007 — Orquestrador retorna sucesso após falha

- **Prioridade:** P1.
- **Natureza:** bug confirmado.
- **Status:** `PENDENTE`.
- **Problema confirmado:** o fluxo principal não consolida o retorno booleano das etapas em código de saída; a API, por sua vez, pode reduzir falha do subprocesso a aviso e responder sucesso.
- **Evidências e arquivos envolvidos:**
  - `scripts/orquestrar_cronogramas.py:327-342` chama operações sem transformar falha em `sys.exit` não zero;
  - na auditoria, `python scripts/orquestrar_cronogramas.py --obra __AUDIT_OBRA_INEXISTENTE__ --gerar-tudo` registrou falha, mas encerrou com código `0`;
  - `apresentacao_comercial/src/app/api/cronograma/route.ts:1224-1226` trata falha do subprocesso como aviso e, em `:1238`, segue para resposta de sucesso.
- **Comportamento atual:** automação e interface podem considerar concluída uma operação que falhou parcial ou totalmente.
- **Comportamento esperado:** qualquer etapa obrigatória falha com código não zero, resposta HTTP de erro e diagnóstico estruturado; sucesso só ocorre após todas as etapas e auditorias obrigatórias.
- **Estratégia de correção:** definir resultado estruturado por etapa; agregar estados no `main`; usar códigos de saída estáveis; abortar etapas dependentes; na API, mapear falha para status apropriado e nunca confirmar promoção/alteração incompleta.
- **Arquivos que provavelmente precisarão ser alterados:** `scripts/orquestrar_cronogramas.py`; rota de cronograma; possivelmente motores chamados para padronizar contrato; testes CLI/API.
- **Dependências:** `AUD-003` deve estabilizar regras; `AUD-012` para impedir persistência parcial. Precede promoção em `AUD-006`.
- **Riscos de regressão:** scripts existentes dependerem indevidamente de código zero; tratar aviso opcional como erro fatal; perder detalhes úteis do stderr.
- **Testes necessários:** obra inexistente; etapa obrigatória falha; etapa opcional falha; todas passam; exceção; subprocesso interrompido; API reflete código/diagnóstico; nenhuma mensagem de sucesso em falha.
- **Critérios objetivos de aceite:**
  1. o comando de obra inexistente encerra com código diferente de zero;
  2. falha obrigatória impede a continuidade dependente;
  3. API retorna erro e não sinaliza sucesso;
  4. sucesso exige validações finais concluídas;
  5. contrato de códigos de saída está documentado e testado.

### AUD-008 — Sincronização falsa bidirecional e fallback entre obras

- **Prioridade:** P1.
- **Natureza:** bug confirmado.
- **Status:** `PENDENTE`.
- **Problema confirmado:** ambas as opções de origem executam a transformação Esteira→LOB, e a API procura dados da OBRA_TMULT/template quando faltam dados na obra selecionada.
- **Evidências e arquivos envolvidos:**
  - `scripts/orquestrar_cronogramas.py:187-195` chama `esteira_para_lob` nos dois ramos de origem;
  - `apresentacao_comercial/src/app/api/cronograma/route.ts:480-484` usa fallback da OBRA_TMULT e depois template;
  - outros fallbacks específicos foram observados em `apresentacao_comercial/src/app/api/cronograma/route.ts:391-396` e `:775-778`.
- **Comportamento atual:** escolher LOB como origem não inverte o fluxo real; obra sem arquivo pode exibir ou processar dados de outra obra.
- **Comportamento esperado:** cada origem executa sua transformação correspondente e validada; ausência de arquivo na obra ativa resulta em estado explícito, nunca em dados de outra obra.
- **Estratégia de correção:** tornar a direção uma enumeração fechada; separar funções e contratos por direção; criar invariantes/relatório de conflitos; remover fallback cruzado do caminho produtivo; manter templates apenas para criação explícita de obra, não para leitura operacional.
- **Arquivos que provavelmente precisarão ser alterados:** orquestrador; `scripts/sincronizar_esteira_e_lob.py`; rota de cronograma; tipos e testes.
- **Dependências:** `AUD-003` para semântica EAP; `AUD-005` para obra ativa; `AUD-007` para propagar falha; `AUD-011` para validar entradas.
- **Riscos de regressão:** transformação reversa perder campos exclusivos; ciclos de sincronização; arredondamentos causarem drift; obras que dependiam inadvertidamente do fallback ficarem sem dados.
- **Testes necessários:** Esteira→LOB; LOB→Esteira; round-trip com invariantes declarados; conflito; fonte ausente; duas obras divergentes; proibição de TMULT/template em leitura produtiva.
- **Critérios objetivos de aceite:**
  1. os dois modos chamam implementações semanticamente distintas;
  2. cada direção tem fixture e teste de resultado;
  3. nenhuma leitura produtiva acessa diretório de outra obra ou template;
  4. fonte ausente gera erro/estado vazio explícito;
  5. conflitos são relatados sem sobrescrita silenciosa.

### AUD-009 — Exportação MS Project divergente do CPM

- **Prioridade:** P1.
- **Natureza:** bug confirmado.
- **Status:** `PENDENTE`.
- **Problema confirmado:** o XML é montado com sequência artificial, datas explícitas e todas as tarefas críticas, sem refletir ES/EF, folgas, caminho crítico e calendário do CPM.
- **Evidências e arquivos envolvidos:**
  - `scripts/gerar_cronograma.py:370` inicia a exportação;
  - `scripts/gerar_cronograma.py:378-387` cria tarefas sintéticas quando o CPM não está disponível;
  - `scripts/gerar_cronograma.py:389-390` calcula o término global por soma simples;
  - `scripts/gerar_cronograma.py:419-427` avança `current_day` sequencialmente e grava datas;
  - `scripts/gerar_cronograma.py:448` marca tarefas como críticas indiscriminadamente.
- **Comportamento atual:** o arquivo pode abrir no MS Project, mas representa cronograma diferente do calculado e pode induzir leitura incorreta do caminho crítico.
- **Comportamento esperado:** o XML deve ser projeção fiel do cronograma CPM validado, incluindo calendário, predecessoras, ES/EF, folgas e criticidade; ausência de CPM deve interromper a exportação produtiva.
- **Estratégia de correção:** desacoplar cálculo de exportação; definir DTO validado de cronograma; consumir apenas saída do CPM; mapear calendário útil e relações; validar XML contra schema/formato suportado e reimportar em teste. Eliminar fallback sintético silencioso.
- **Arquivos que provavelmente precisarão ser alterados:** `scripts/gerar_cronograma.py`; módulo de CPM/calendário compartilhado; exportador XML; testes/fixtures.
- **Dependências:** `AUD-003`, `AUD-007` e, quando a fonte for CSV, `AUD-011`.
- **Riscos de regressão:** incompatibilidade de versão do MS Project; diferenças de fuso/data inclusiva; duração útil versus corrida; relações não suportadas; mudança em IDs de tarefas.
- **Testes necessários:** rede com paralelismo e folga; caminho crítico conhecido; feriado/fim de semana; predecessoras múltiplas; marco; CPM ausente; XML válido; round-trip ou parser independente comparando datas e criticidade.
- **Critérios objetivos de aceite:**
  1. nenhuma tarefa é marcada crítica sem folga crítica calculada;
  2. datas e predecessoras do XML coincidem com o DTO CPM;
  3. calendário útil está explícito e testado;
  4. CPM ausente impede exportação com erro claro;
  5. fixture de rede conhecida é reimportada sem divergência material.

### AUD-010 — RDO com valores presumidos e assinatura não comprovada

- **Prioridade:** P1.
- **Natureza:** bug confirmado.
- **Status:** `PENDENTE`.
- **Problema confirmado:** o processador preenche identidade, efetivo, HH, atividade, FVS e status com defaults, inicia a numeração vazia em 006 e declara assinatura digital sem evidência correspondente no payload.
- **Evidências e arquivos envolvidos:**
  - `scripts/processar_coleta_campo.py:161-171` inicia `max_num` em 5;
  - `scripts/processar_coleta_campo.py:181` fixa engenheiro e mestre;
  - `scripts/processar_coleta_campo.py:193-207` fornece valores presumidos para campos operacionais;
  - `scripts/processar_coleta_campo.py:215` afirma assinatura digital sem comprovação equivalente no payload auditado;
  - `_TEMPLATE_OBRA_NOVA/04_PRODUCAO_E_AVANCO/RDOS/RDO_001` a `RDO_006` e `PAINEL_RDOS_OBRA.xlsx` já estão preenchidos no template.
- **Comportamento atual:** obra vazia pode começar no RDO 006 e emitir documento aparentemente oficial com dados não medidos ou não assinados.
- **Comportamento esperado:** template é vazio; numeração inicial é 001; `/campo` envia apontamento para staging; campos técnicos obrigatórios vêm do apontamento validado; responsável é informado e confirmado no fluxo de campo ou por configuração controlada; assinatura possui evidência verificável; o agente/motor promove o apontamento a RDO oficial. Ausência de evidência impede emissão oficial, sem exigir conta ou sessão web.
- **Estratégia de correção:** separar exemplo de template produtivo; definir schema de apontamento/RDO; remover defaults factuais; reservar número sob lock ou usar identidade imutável além do número; modelar coleta, rascunho e emissão como etapas distintas; anexar hash/metadados de assinatura; fazer a promoção pelo motor/agente; migrar templates sem apagar dados reais.
- **Arquivos que provavelmente precisarão ser alterados:** `scripts/processar_coleta_campo.py`; tela/rota de coleta; `_TEMPLATE_OBRA_NOVA/04_PRODUCAO_E_AVANCO/`; gerador de RDO; schemas e testes.
- **Dependências:** `AUD-002` para delimitar `/campo` como coleta em staging; `AUD-011` para dados tabulares; `AUD-012` para numeração e gravação concorrente.
- **Riscos de regressão:** confundir exemplos com documentos reais; colisão de numeração; impedir rascunhos; invalidar RDOs históricos; armazenar evidência sensível de forma insegura.
- **Testes necessários:** primeira emissão; duas emissões concorrentes; campo obrigatório ausente; zero legítimo versus ausência; responsável ausente; assinatura ausente/inválida; coleta não vira documento oficial automaticamente; rascunho; template novo; preservação de histórico.
- **Critérios objetivos de aceite:**
  1. obra nova não contém RDOs operacionais pré-preenchidos e começa em 001;
  2. nenhum valor factual é inventado pelo processador;
  3. documento sem assinatura válida não é marcado como assinado/oficial;
  4. emissões concorrentes não repetem número nem sobrescrevem arquivo;
  5. identidade e evidência de emissão são auditáveis.

### AUD-011 — Parser CSV mascara falhas e não implementa CSV robusto

- **Prioridade:** P1.
- **Natureza:** bug confirmado.
- **Status:** `PENDENTE`.
- **Problema confirmado:** o parser divide texto por linhas e ponto e vírgula, remove aspas superficialmente e converte qualquer exceção em lista vazia, confundindo arquivo vazio, ausente, inválido e erro de schema.
- **Evidências e arquivos envolvidos:**
  - `apresentacao_comercial/src/lib/csvParser.ts:3-30` contém leitura síncrona, `split` manual e `catch` genérico com retorno `[]`;
  - `skills/desenvolvimento/SKILL_DEV_TESTES_E_QUALIDADE.md:37-38` exige detectar separador e encoding incorretos;
  - `skills/desenvolvimento/SKILL_DEV_SCHEMA_CSV.md:201` estabelece validação correspondente no contrato de dados.
- **Comportamento atual:** campos com delimitadores, aspas ou quebras internas podem ser interpretados incorretamente; falhas são apresentadas como ausência de registros.
- **Comportamento esperado:** parser compatível com CSV real, encoding definido e validação de cabeçalho/schema; consumidores recebem resultado discriminado como `ok`, `empty`, `not_found`, `invalid_encoding` ou `invalid_schema`.
- **Estratégia de correção:** escolher biblioteca madura já compatível com o projeto ou implementar via infraestrutura aprovada; detectar BOM/UTF-8 conforme manual; validar cabeçalhos e tipos em runtime; retirar `catch` silencioso; padronizar tradução para respostas API. Planejar migração dos CSVs legados sem regravação automática.
- **Arquivos que provavelmente precisarão ser alterados:** `src/lib/csvParser.ts`; rotas consumidoras; schemas/tipos; dependências Node se necessárias; fixtures/testes.
- **Dependências:** nenhuma. É base para `AUD-003`, `AUD-004`, `AUD-005`, `AUD-008`, `AUD-009` e `AUD-010`.
- **Riscos de regressão:** arquivos legados com encoding ou separador divergente deixarem de carregar; mudança de tipos; perda de compatibilidade com BOM; custo de parsing em arquivos grandes.
- **Testes necessários:** UTF-8 e UTF-8 com BOM; acentos; delimitador em campo citado; aspas escapadas; quebra de linha em campo; arquivo vazio; ausente; header incompleto/extra; encoding inválido; arquivo grande; propagação correta pela API.
- **Critérios objetivos de aceite:**
  1. fixtures CSV válidas complexas são lidas corretamente;
  2. ausência, vazio, encoding inválido e schema inválido geram estados distintos;
  3. nenhum consumidor transforma erro estrutural em lista vazia silenciosa;
  4. headers obrigatórios são validados conforme a skill de schema;
  5. regressão com CSVs oficiais representativos está automatizada.

### AUD-012 — Escritas não atômicas e suscetíveis a concorrência

- **Prioridade:** P1.
- **Natureza:** risco confirmado de integridade de dados.
- **Status:** `PENDENTE`.
- **Problema confirmado:** fluxos fazem leitura-modificação-escrita e numeração por varredura sem lock; a rota de cronograma grava arquivo oficial antes de saber se o processamento posterior será bem-sucedido.
- **Evidências e arquivos envolvidos:**
  - `scripts/processar_coleta_campo.py:161-171` calcula próximo RDO por máximo observado;
  - `scripts/processar_coleta_campo.py:295-314` altera fila JSON por leitura-modificação-escrita;
  - `scripts/processar_coleta_campo.py:403-421` repete o padrão para FVS;
  - `apresentacao_comercial/src/app/api/cronograma/route.ts:1205` grava LOB antes da execução/validação posterior;
  - não foi identificada infraestrutura comum de lock e troca atômica no levantamento realizado.
- **Comportamento atual:** requisições concorrentes podem perder atualizações, repetir IDs/números ou deixar conjunto parcial após falha.
- **Comportamento esperado:** mutações são serializadas por obra/recurso ou usam controle otimista; escrevem em staging, validam e promovem por troca atômica; operações multiarquivo têm manifesto/recuperação e idempotência.
- **Estratégia de correção:** criar camada compartilhada de persistência; lock com timeout por obra/recurso; IDs UUID e sequência reservada quando o número humano for necessário; escrita temporária no mesmo volume, `fsync` quando aplicável e replace atômico; versionamento/ETag; manifesto para conjunto; recuperação de temporários órfãos.
- **Arquivos que provavelmente precisarão ser alterados:** processador de campo; rota/serviço de cronograma; `scripts/common/` para utilitário compartilhado; todos os escritores críticos identificados durante a implementação estritamente relacionada; testes de concorrência.
- **Dependências:** `AUD-002` para reduzir e classificar as superfícies de escrita; `AUD-011` para validar antes da promoção; necessário para concluir `AUD-001`, `AUD-006` e `AUD-010`.
- **Riscos de regressão:** deadlock; locks órfãos; comportamento diferente entre Windows e ambiente de implantação; replace entre volumes; queda de throughput; dupla escrita em retry.
- **Testes necessários:** duas e várias escritas paralelas; timeout de lock; processo interrompido entre staging e promoção; retry idempotente; versão obsoleta; rollback de multiarquivo; recuperação pós-falha; compatibilidade Windows.
- **Critérios objetivos de aceite:**
  1. teste concorrente não perde atualização nem duplica identificador;
  2. falha antes da promoção preserva integralmente a versão oficial anterior;
  3. arquivos temporários não são consumidos como oficiais;
  4. retry da mesma operação não duplica efeito;
  5. estratégia de lock, timeout e recuperação está documentada e coberta por testes.

### AUD-013 — Módulos monolíticos e acoplamento elevado

- **Prioridade:** P2.
- **Natureza:** dívida técnica confirmada.
- **Status:** `PENDENTE`.
- **Problema confirmado:** módulos de grande porte concentram responsabilidades de apresentação, parsing, regras, DAG, persistência e execução de processos, aumentando superfície de regressão.
- **Evidências e arquivos envolvidos:** contagens observadas na auditoria:
  - `apresentacao_comercial/src/components/LinhaDeBalanco.tsx`: 2.221 linhas;
  - `apresentacao_comercial/src/app/api/cronograma/route.ts`: 1.254 linhas;
  - `apresentacao_comercial/src/app/dashboard/cronograma/page.tsx`: 985 linhas;
  - `scripts/sincronizar_esteira_e_lob.py`: 861 linhas;
  - `scripts/reprogramar_cronograma.py`: 751 linhas;
  - o lint também apontou atualização de estado em efeito e dependência ausente em `LinhaDeBalanco.tsx:361`.
- **Comportamento atual:** mudanças pequenas exigem navegar por múltiplas responsabilidades no mesmo arquivo e são difíceis de testar isoladamente.
- **Comportamento esperado:** rotas finas; domínio e casos de uso independentes de transporte; repositórios isolam arquivos; componentes separam estado, transformação e visualização; módulos Python reutilizam `scripts/common/` e respeitam o manual.
- **Estratégia de correção:** somente após testes dos comportamentos críticos, extrair por fronteiras reais: tipos/DTOs, parser, domínio CPM/LOB, repositório, executor e UI. Fazer movimentos pequenos, sem mudança funcional simultânea. Não usar meta de linhas como finalidade; usar coesão e testabilidade.
- **Arquivos que provavelmente precisarão ser alterados:** os cinco módulos citados; módulos novos nas estruturas já prescritas pelas skills; testes correspondentes.
- **Dependências:** `AUD-003`, `AUD-007`, `AUD-008`, `AUD-011`, `AUD-012` e cobertura incremental de `AUD-014`.
- **Riscos de regressão:** alterar comportamento junto com movimentação; dependências circulares; duplicar lógica durante transição; piorar renderização/estado; interfaces internas instáveis.
- **Testes necessários:** caracterização antes de cada extração; unidade para domínio; integração de repositório/rota; snapshots somente quando semanticamente úteis; renderização/interação da LOB; paridade de saídas Python.
- **Critérios objetivos de aceite:**
  1. cada extração mantém testes de caracterização verdes;
  2. rota de cronograma delega regras e persistência a serviços testáveis;
  3. UI não mistura parsing de arquivo com renderização;
  4. não há duplicação temporária deixada ao concluir a fase;
  5. nenhuma alteração funcional não autorizada acompanha a refatoração.

### AUD-014 — Gates de qualidade ausentes ou falhando

- **Prioridade:** P1.
- **Natureza:** dívida técnica e risco de qualidade confirmados.
- **Status:** `PENDENTE`.
- **Problema confirmado:** não foi encontrada suíte automatizada nem CI; o lint falha; não há manifesto/lock Python reproduzível, embora existam dependências externas.
- **Evidências e arquivos envolvidos:** resultados da auditoria:
  - `npx.cmd tsc --noEmit --incremental false`: aprovado;
  - `npm run build`: aprovado;
  - análise AST dos 46 arquivos Python produtivos/não legados: aprovada;
  - smoke `--help` de 29 scripts de topo: aprovado;
  - ESLint: reprovado com 104 ocorrências, sendo 53 erros e 51 avisos;
  - testes automatizados encontrados: 0;
  - workflows de CI encontrados: 0;
  - manifesto/lock de dependências Python encontrado: 0;
  - o código importa bibliotecas como pandas, openpyxl, numpy, plotly e pymupdf;
  - `npm audit --json` avaliou 477 dependências e encontrou 0 vulnerabilidades conhecidas naquele momento;
  - `package.json` não oferecia script `test` no estado auditado.
- **Comportamento atual:** build e tipagem capturam apenas parte dos defeitos; regressões de regra/persistência não têm proteção; ambiente Python não é reproduzível; lint não pode atuar como gate.
- **Comportamento esperado:** cada linguagem possui dependências reproduzíveis e testes; CI executa formatação/lint, tipos, testes, build e verificações Python; gates são verdes e bloqueantes.
- **Estratégia de correção:** adicionar primeiro testes mínimos dos P0/P1 ao implementar cada item; escolher framework alinhado ao projeto; declarar e travar dependências Python com versões/ambientes suportados; classificar e corrigir lint por categoria sem mudanças cosméticas massivas; criar CI com cache e comandos idênticos aos locais; manter auditoria de dependências.
- **Arquivos que provavelmente precisarão ser alterados:** `package.json` e lock; configuração de testes/lint; manifesto/lock Python; workflow de CI; pastas de testes; arquivos com violações reais de lint.
- **Dependências:** transversal. Para fechar o item, depende dos testes produzidos em `AUD-001` a `AUD-012`; `AUD-013` depende dessa rede de proteção.
- **Riscos de regressão:** escolher ferramentas incompatíveis; CI divergente do Windows/local; congelar versões incorretas; corrigir lint alterando comportamento; testes frágeis baseados em arquivos oficiais mutáveis.
- **Testes necessários:** execução limpa em checkout novo; testes unitários e integração dos achados; build Next.js; TypeScript; ESLint; compilação/importação Python; smoke CLI; instalação reproduzível; falha proposital comprovando que CI bloqueia.
- **Critérios objetivos de aceite:**
  1. existe comando único documentado para validar frontend e outro para Python;
  2. CI executa em checkout limpo e bloqueia merge quando qualquer gate falha;
  3. ESLint termina sem erros, e avisos remanescentes têm decisão explícita;
  4. dependências Python diretas e versões suportadas estão declaradas e reproduzíveis;
  5. todos os bugs P0/P1 corrigidos possuem teste de regressão;
  6. build, tipagem, testes, lint e smoke CLI ficam verdes.

## 6. Marcos de validação por fase

### Marco da Fase 0 — Limite leitura/escrita estabelecido

- APIs do dashboard são somente leitura e mutações genéricas permanecem indisponíveis;
- `/campo` é tratado como exceção de coleta, sem promoção automática para registro oficial;
- baseline não pode ser promovida por fluxo comum;
- FVS não libera medição por default;
- nenhuma contenção altera dados oficiais existentes.

### Marco da Fase 1 — Contratos e persistência confiáveis

- resultado de leitura distingue ausência, vazio e inválido;
- a obra ativa é obrigatória e isolada em cliente e servidor;
- gravações concorrentes e falhas intermediárias não corrompem o estado oficial.

### Marco da Fase 2 — Planejamento consistente

- EAP única e portões oficiais testados;
- falhas de motor propagam código não zero e erro HTTP;
- direções LOB/Esteira funcionam de forma distinta;
- XML representa o CPM validado.

### Marco da Fase 3 — Evidência de campo confiável

- aprovação de FVS e emissão de RDO exigem responsável identificado e evidência válida, sem pressupor sessão web;
- não existem defaults factuais nem documentos oficiais pré-preenchidos;
- transições e emissões são idempotentes e auditáveis.

### Marco da Fase 4 — Painéis verdadeiros

- nenhuma API produtiva apresenta fixture como fato;
- obra sem dados é mostrada como tal;
- toda métrica relevante informa origem e atualização.

### Marco da Fase 5 — Mudança sustentável

- responsabilidades críticas estão isoladas sem mudança funcional colateral;
- lint, tipos, build, testes e verificações Python são executados em CI e estão verdes;
- instalação Python é reproduzível.

## 7. Instruções para o próximo agente

1. Leia integralmente o `AGENTS.md` aplicável e este `PLANO_MELHORIAS_AUDITORIA.md` antes de começar. Em seguida, consulte pelo `INDICE_MESTRE_SKILLS.md` apenas as Skills/Manuais exigidos pelo item autorizado.
2. Execute apenas um item ou uma fase explicitamente autorizada por vez. Não trate a existência deste plano como autorização para executar todos os itens.
3. Antes de alterar qualquer arquivo, valide o estado atual do código relacionado ao item: confirme as evidências, registre divergências desde a auditoria e execute os checks existentes pertinentes. Essa validação deve ser localizada, não uma nova auditoria global.
4. Não repita a auditoria global. Investigue apenas o necessário para implementar e testar o item autorizado e suas dependências diretas.
5. Não faça refatorações fora do escopo. Melhorias adjacentes devem ser registradas para decisão posterior, sem serem incorporadas silenciosamente.
6. Respeite o adendo de autonomia. Alteração de baseline, emissão oficial, promoção de dados e outras ações laranja/vermelhas exigem o fluxo de aprovação correspondente.
7. Preserve a premissa `agente = operador / dashboard = leitura`. Não introduza login, sessões, banco de usuários ou RBAC sem uma nova decisão arquitetural explícita. Trate `/campo` como exceção independente e limitada a coleta/staging.
8. Preserve alterações preexistentes do usuário e nunca use comandos destrutivos para limpar o worktree.
9. Para cada item, crie primeiro o teste que demonstra o defeito ou uma caracterização equivalente; depois implemente a menor correção completa e valide riscos de regressão.
10. Não use arquivos oficiais de obra como fixtures mutáveis. Trabalhe com cópias temporárias e dados mínimos claramente identificados como teste.
11. Atualize este documento após implementação e validação de cada item:
    - troque o **Status** no detalhe e na tabela-resumo;
    - acrescente, no bloco de registro abaixo, data, responsável/agente, commit ou referência, arquivos alterados, testes executados e resultado;
    - se bloqueado, registre a decisão ou informação ausente sem inventá-la;
    - marque `VALIDADO` somente quando todos os critérios objetivos de aceite do item tiverem sido cumpridos.

## 8. Registro de execução

O próximo agente deve adicionar uma linha por mudança de status. Não apagar registros anteriores.

| Data | Item/Fase | Status anterior → novo | Responsável/agente | Commit/referência | Validações executadas | Observações |
|---|---|---|---|---|---|---|
| 14/09/2026 | Plano inicial | — → PENDENTE | Auditoria técnica | `PLANO_MELHORIAS_AUDITORIA.md` | Consolidação documental dos achados já auditados | Nenhuma correção implementada |
| 14/09/2026 | Premissa arquitetural | PENDENTE → PENDENTE | Tech Lead | `PLANO_MELHORIAS_AUDITORIA.md` | Revisão documental localizada; sem nova auditoria | Agente como operador, dashboard somente leitura e `/campo` como exceção; removidos requisitos de login/RBAC |
| 14/09/2026 | Fase 0 / AUD-002 | PENDENTE → IMPLEMENTADO | Codex / Tech Lead | `f040d9b` | `npm run test` (3/3), `tsc --noEmit`, build, lint focado e `py_compile` aprovados | `POST /api/cronograma` bloqueado; fallback cruzado removido apenas da leitura de LOB; `/campo` grava somente `STAGING_CAMPO`, sem shell ou motor web. |
| 14/09/2026 | Fase 0 / AUD-006 | PENDENTE → IMPLEMENTADO | Codex / Tech Lead | `f040d9b` | `npm run test` (3/3), `tsc --noEmit` e build aprovados | Mutação de baseline pelo dashboard bloqueada com HTTP 405. Proposta, confirmação e promoção canônica permanecem para as fases dependentes. |
| 14/09/2026 | Fase 0 / AUD-001 | PENDENTE → IMPLEMENTADO | Codex / Tech Lead | `f040d9b` | `npm run test` (3/3) e `py_compile` aprovados | FVS de campo é apenas submetida; dashboard e processador não promovem para `APROVADO` nem liberam medição. Contrato completo, evidência e promoção governada permanecem para a Fase 3. |

## 9. Top 10 recomendado por benefício

Esta ordem considera impacto, risco e dependências; ela não substitui a autorização por fase.

1. `AUD-002` — tornar o dashboard somente leitura e confinar com segurança a exceção `/campo`.
2. `AUD-001` — impedir aprovação indevida de FVS e desbloqueio de medição.
3. `AUD-006` — retirar mutação de baseline da web e usar confirmação do agente + Git.
4. `AUD-003` — estabelecer a EAP canônica e os portões oficiais.
5. `AUD-004` — eliminar dados demonstrativos apresentados como reais.
6. `AUD-012` — tornar gravações concorrentes, atômicas e recuperáveis.
7. `AUD-011` — validar CSV e tornar erros de dados explícitos.
8. `AUD-007` — propagar falhas reais dos motores e da API.
9. `AUD-010` — garantir RDO medido, numerado e assinado com evidência.
10. `AUD-005` — assegurar isolamento da obra ativa em EVM e orçamento.

Os itens `AUD-008`, `AUD-009`, `AUD-013` e `AUD-014` continuam obrigatórios na ordem de fases, embora fiquem fora do Top 10 por combinação relativa de urgência, dependência e benefício imediato.
