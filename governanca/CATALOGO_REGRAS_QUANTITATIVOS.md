# Catálogo de Regras Executáveis

O catálogo computável está em `scripts/motor_quantitativos/regras/`. Cada regra possui ID, versão, disciplina, EAP, unidade, campos obrigatórios, expressão-modelo e referência da skill.

Na Fase 3 foram cadastradas as primeiras regras de Fundações: escavação, apiloamento, lastro, concreto e fôrma de sapata, concreto de estaca e concreto de radier.

O catálogo não calcula, não lê PDF e não acessa SQLite. Ele será consumido pelo gerador de expressões da Fase 4. Valores de obra entram somente pelos `ElementRecord` com evidência.

Critérios de expansão:

- nova regra exige referência a uma seção da skill e código EAP;
- mudança de fórmula cria nova versão, sem sobrescrever a anterior;
- regra não pode conter dimensão, preço, perda, UCC ou identificador de obra;
- toda regra precisa declarar unidade e campos obrigatórios;
- regra sem dados comprovados bloqueia o cálculo e gera RFI.
