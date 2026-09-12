# 📘 Manual de Sincronização & Orquestração de Cronogramas Lean (Gantt CPM, LOB e Takt)

Este manual é o guia definitivo de engenharia para inicialização, acompanhamento, reprogramação e garantia de **100% de sincronização em tempo real** entre os 3 níveis de planejamento do sistema:
1. **Longo Prazo:** Caminho Crítico CPM e Gráfico de Gantt (`dados_cpm.json`);
2. **Médio Prazo:** Linha de Balanço / LOB com Ritmo Heijunka (`LINHA_DE_BALANCO.csv`);
3. **Curto Prazo:** Esteira Lean Takt / WWP em Lotes de Produção (`PROGRAMACAO_CURTO_PRAZO_[OBRA].csv`).

---

## 1. O Triângulo da Verdade Única

Em qualquer empreendimento gerenciado pelo sistema, nenhuma ferramenta de planejamento opera de forma isolada:

```
                           [ GANTT / CPM ]
                      Rede de Caminho Crítico
                     (178 dias úteis de projeto)
                               ▲     ▲
                      Cascata  │     │  Término
                      Avanço   │     │  Global
                               ▼     ▼
                [ LINHA DE BALANÇO (LOB) ]
              Ritmo de Produção por Zona e Vagão
             (Fluxo Contínuo Nivelado - Heijunka)
                               ▲     ▲
                      Alocação │     │  Avanço
                      Frentes  │     │  de Campo
                               ▼     ▼
               [ ESTEIRA TAKT / CURTO PRAZO ]
              Lotes Semanais, Equipes e UCCs
                (Colunas DATA_INICIO e DATA_FIM)
                               ▲
                               │ Apontamentos Diários
                               ▼
                   [ RDO / MEDIÇÃO DE CAMPO ]
```

---

## 2. Inicialização de Nova Obra (Pipeline Ponta a Ponta)

Para gerar do zero todos os cronogramas de uma obra nova sem rodar scripts isolados:

```bash
python scripts/orquestrar_cronogramas.py --obra NOME_DA_OBRA --gerar-tudo --takt-dias 3
```

### O que o motor executa em cadeia automática:
1. **Orçamento e EAP:** Compila a base física e curva S físico-financeira preliminar.
2. **Curto Prazo Takt:** Modela os lotes com base no Takt Time informado (1 a 6 dias úteis) e associa equipes, insumos UCC e metas físicas.
3. **Linha de Balanço:** Aloca as frentes em cada zona física, valida o fluxo contínuo Heijunka e zera conflitos espaciais.
4. **Reconciliação Físico-Financeira:** Vincula os desembolsos mensais aos marcos de entrega da LOB.
5. **Auditoria Multi-Eixo:** Executa o validador de 5 eixos. Se houver 1 dia sequer de descompasso, emite auto-reconciliação.

---

## 3. Flexibilidade do Takt Time (1 a 6 Dias Úteis)

O Takt Time **não é fixo em 3 dias** e pode ser customizado para o perfil construtivo de cada obra:

| Takt Time | Característica Construtiva | Ciclos por Semana (Seg-Sáb) |
| :--- | :--- | :--- |
| **1 Dia Útil** | Obras rápidas de fit-out corporativo, reformas comerciais e montagem modular. | 6 ciclos semanais (1 por dia) |
| **2 Dias Úteis** | Ciclos curtos com alta rotatividade de frentes (Seg-Ter, Qua-Qui, Sex-Sáb). | 3 lotes por semana |
| **3 Dias Úteis** | **Padrão TMULT:** Divisão simétrica da semana (Seg-Qua e Qui-Sáb). | 2 lotes por semana |
| **4 ou 5 Dias** | Ciclos intermediários de cura tecnológica, alvenarias extensas e montagens pesadas. | 1 a 2 lotes por semana |
| **6 Dias Úteis** | **Takt Semanal Puro:** A equipe entra na segunda-feira e entrega a zona no sábado. | 1 lote por semana |

> **Comando:** Use `--takt-dias N` (ex: `--takt-dias 4` ou `--takt-dias 5`).

---

## 4. Reprogramação & Aceleração de Prazo por Aumento de Equipe (Crashing via RUP)

Quando uma atividade atrasar ou o cliente solicitar a antecipação de um marco, a engenharia aplica a fórmula da **Razão Unitária de Produção (RUP)**:

$$\text{Duração (dias úteis)} = \frac{\text{Volume de Serviço} \times \text{RUP}}{\text{Efetivo (Homens)} \times 8\text{ h/dia}}$$

### Cenário A: Aumentar o efetivo para reduzir o prazo (Crashing)
Se você quer dobrar a equipe de ladrilhistas (ex: de 6 para 12 operários) na atividade de Porcelanato (ID 29):
```bash
python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --reprogramar --tarefa-id 29 --novo-headcount 12
```
* **O que acontece automaticamente:**
  1. A duração da atividade cai pela metade via RUP (ex: de 6 para 3 dias).
  2. O grafo topológico (DAG) propaga a antecipação para todas as frentes sucessoras.
  3. A `LINHA_DE_BALANCO.csv` antecipa o término e libera a pintura mais cedo.
  4. A `PROGRAMACAO_CURTO_PRAZO_*.csv` atualiza o lote correspondente com a nova duração, novo headcount (12 op.) e novas datas (`DATA_INICIO` e `DATA_FIM`).
  5. O `dados_cpm.json` atualiza o CPM determinístico, recalculando o caminho crítico e antecipando o término global da obra.
  6. A Curva S físico-financeira acomoda o novo pico no Histograma de mão de obra.

### Cenário B: Reduzir a duração explicitamente
```bash
python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --reprogramar --tarefa-id 29 --nova-duracao 3
```
* O sistema calcula o novo efetivo necessário via RUP e propaga para os 3 cronogramas.

### Cenário C: Deslocar um vagão inteiro (Todas as zonas)
```bash
python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --reprogramar --vagao 10 --deslocar-dias -3 --aplicar-todo-vagao
```

---

## 5. O Sentinela / File Watcher em Tempo Real (`--watch`)

Para trabalhar com planilhas Excel ou no VS Code sem precisar rodar comandos a cada salvamento:

```bash
python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --watch
```

* O processo fica rodando em segundo plano monitorando `LINHA_DE_BALANCO.csv`, `PROGRAMACAO_CURTO_PRAZO_*.csv`, `dados_cpm.json` e `config_obra.json`.
* Assim que você editar uma célula no Excel e pressionar `Ctrl + S`:
  1. O sentinela detecta a alteração no disco em milissegundos.
  2. Aplica um debounce de 1.5s para conclusão da escrita.
  3. Dispara a sincronização em cascata para os outros 2 cronogramas.
  4. Executa a auditoria multi-eixo.
  5. Imprime no console: `"[SUCESSO] Sincronização executada com sucesso! 0 divergências entre CPM, LOB e Curto Prazo."`

---

## 6. Sincronização e Geração Automática do Histograma de Mão de Obra (Headcount & HH)

O **Histograma de Mão de Obra** reflete o efetivo físico necessário em campo a cada mês e é a base para o dimensionamento do canteiro de obras (NR-18: vivência, vestiários, refeitório, alojamento, transporte e EPIs).

### Como o Motor Mantém a Sincronização Contínua:
1. **Extração Automática dos Lotes Takt:** Cada lote de `PROGRAMACAO_CURTO_PRAZO_*.csv` define a equipe alocada (ex: `3 Ladrilhistas + 3 Ajudantes`) e as datas de execução (`DATA_INICIO` e `DATA_FIM`).
2. **Equipe Fixa de Gestão & SST (5 profissionais):** Engenheiro Residente, Mestre de Obras Geral, TST, Almoxarife e Vigia Patrimonial permanecem estáveis (1 por mês) ao longo de todo o contrato.
3. **Nivelamento Heijunka da Produção:** Para as especialidades operacionais (Pedreiros, Ladrilhistas, Armadores, Pintores, Eletricistas, etc.), o motor calcula o pico simultâneo da disciplina ativa naquele mês.
4. **Crashing com Aumento de Efetivo:** Se o engenheiro dobrar a equipe de um lote (ex: `--novo-headcount 12`), o motor:
   - Aloca 6 oficiais + 6 serventes no lote;
   - Atualiza o mês correspondente no Histograma para absorver o novo pico;
   - Recalcula automaticamente as **Horas-Homem (HH)** mensais ($\text{HH} = \text{Headcount} \times 220\text{ h/mês}$);
   - Regera simultaneamente `06_SST_E_RH/dados_histograma_mo.json`, `HISTOGRAMA_MAO_DE_OBRA_[SIGLA].csv` e `HISTOGRAMA_MAO_DE_OBRA_[SIGLA].xlsx`;
   - Atualiza a rota `/api/cronograma` e reflete imediatamente no modal do Dashboard Comercial.

```bash
# Recalcular exclusivamente o Histograma de Mão de Obra:
python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --histograma
# ou diretamente:
python scripts/gerar_histograma_sincronizado.py --obra OBRA_TMULT
```

---

## 7. Tabela de Referência Rápida (Cheat Sheet do Engenheiro)

| Necessidade | Comando Recomendado |
| :--- | :--- |
| **Criar cronogramas de obra nova do zero** | `python scripts/orquestrar_cronogramas.py --obra NOVA_OBRA --gerar-tudo --takt-dias 3` |
| **Sincronizar e auditar cronogramas existentes** | `python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --sincronizar` |
| **Recalcular apenas o Histograma de Mão de Obra** | `python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --histograma` |
| **Acelerar atividade dobrando a equipe (Crashing)** | `python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --reprogramar --tarefa-id 29 --novo-headcount 12` |
| **Alterar duração de uma frente específica** | `python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --reprogramar --tarefa-id 15 --nova-duracao 4` |
| **Deslocar um vagão inteiro em +2 dias** | `python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --reprogramar --vagao 06 --deslocar-dias 2 --aplicar-todo-vagao` |
| **Simular sem alterar arquivos (Dry-Run)** | `python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --reprogramar --tarefa-id 29 --novo-headcount 12 --dry-run` |
| **Ativar Sentinela em segundo plano** | `python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --watch` |
| **Auditar conformidade rigorosa (6 Eixos)** | `python scripts/orquestrar_cronogramas.py --obra OBRA_TMULT --auditar` |
