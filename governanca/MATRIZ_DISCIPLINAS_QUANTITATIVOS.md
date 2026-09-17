# Matriz de Escala por Disciplina

Cada disciplina usa o mesmo contrato: evidência → elemento normalizado → regra versionada → resultado líquido → SQLite. Nenhuma disciplina pode aplicar perdas, UCC, preço ou dimensão padrão no parser.

| Disciplina | Parser atual | Catálogo inicial | Próximo adaptador |
|---|---|---|---|
| Fundação | legado + `ParserFundacoesContrato` | 7 regras | ampliar blocos, estacas, baldrames e radier |
| Estrutura | `parser_estrutura.py` | pilares e vigas | converter saída para `ElementRecord` |
| Arquitetura | `parser_arquitetura.py` | parede e piso líquidos | separar vedação, acabamento e esquadrias |
| Elétrica | `parser_instalacoes.py` | eletroduto líquido | circuitos, cabos e pontos com evidência |
| Hidráulica | `parser_instalacoes.py` | tubulação líquida | prumadas, conexões e testes |
| Serviços especiais | sem adaptador dedicado | serviço por área | criar parser específico por sistema |

## Critério de prontidão disciplinar

- pelo menos um `ElementRecord` real de teste;
- regras referenciadas à skill e EAP;
- ausência de valores padrão no parser;
- erro de campo ausente gera RFI/bloqueio;
- expressão, unidade e evidência preservadas;
- teste unitário e teste de integração aprovados.
