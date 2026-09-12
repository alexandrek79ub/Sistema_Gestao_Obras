# 📅 SKILL GESTÃO 01: Planejamento & Controle

> **Dependência:** Acionado pelo Gestor de Obras (`agents_gestor_obras.md`).
> **Domínio:** Prazos, caminho crítico, sequenciamento de atividades, linha de balanço.

## 🎯 Objetivo
Analisar cronogramas, identificar dependências lógicas entre serviços, medir impactos de atrasos e propor soluções de aceleração para garantir que a obra termine no prazo estabelecido.

---

## 🧭 1. Princípios de Planejamento (Regras Básicas)
1. **Lógica de Precedência:** Nenhum serviço posterior pode iniciar antes da liberação do serviço anterior obrigatório (ex: alvenaria depende de estrutura; pintura depende de emboço curado).
2. **Caminho Crítico (CPM):** Identifique sempre as atividades que não possuem folga. Um atraso no caminho crítico atrasa o prazo final da obra. **Cálculo de CPM sempre via script `calcular_cpm.py`** — nunca estimado visualmente.
3. **Folgas:** Se uma atividade tem folga e atrasa dentro desse limite, o impacto é absorvido.
4. **Linha de Balanço:** Em residenciais com repetição (ex: pavimentos tipo), o ritmo de produção deve ser contínuo e sincronizado (mesma velocidade entre equipes). **Detecção de colisão de ritmo via script `detectar_colisao_linha_balanco.py`**.

### 1.1 Limiar de Alerta e Escalonamento

| SPI (actual) | Duração | Ação obrigatória |
|---|---|---|
| SPI ≥ 0,95 | Qualquer | Monitoramento padrão |
| 0,90 ≤ SPI < 0,95 | 1 período | **Alerta amarelo** — alertar gestor e investigar causa |
| SPI < 0,90 | 1 período | **Alerta laranja** — acionar `SKILL_GESTAO_07` (Portão de Qualidade de Dado) |
| SPI < 0,90 | **2+ períodos consecutivos** | **Alerta vermelho** — acionar `SKILL_GESTAO_16_CRONOGRAMA_E_REPROGRAMACAO.md` para reprogramação formal |

> **Regra:** Não reprogramar cronograma com base em 1 período ruim isolado. Esperar a confirmação de tendência (SPI abaixo do limiar por 2+ períodos consecutivos) antes de emitir nova baseline.

### 1.2 Integração com Outras Skills
- **SPI calculado:** Sempre via `SKILL_GESTAO_06_RELATORIOS.md` (EVM).
- **Duração das atividades:** Baseada no RUP real de `SKILL_GESTAO_08_PRODUTIVIDADE_E_RECURSOS.md` (não estimativa sentida).
- **Reprogramação formal:** Delegada para `SKILL_GESTAO_16_CRONOGRAMA_E_REPROGRAMACAO.md`.

### 1.3 Metodologia Sistêmica Obrigatória: Inversão Lean (Esteira Takt ➔ Linha de Balanço ➔ CPM)

Nas obras do ecossistema, **o cronograma mestre não nasce de um diagrama de barras teórico abstrato**. A engenharia de planejamento deve executar obrigatoriamente a seguinte sequência em 4 passos:

```
[Passo 1: Curto Prazo com Performance]
Modelar Zonas Takt + Vagões Especializados + Bancada de Pré-Fabricação (Zero Ociosidade)
                                      ↓
[Passo 2: Calibração da Linha de Balanço (LOB)]
Mapear os Setores Físicos herdando os ritmos da esteira (Cobertura logo pós-desforma)
                                      ↓
[Passo 3: Caminho Crítico Determinístico (CPM)]
Processar via `calcular_cpm.py` fixando folgas, marcos e prazo contratual global
                                      ↓
[Passo 4: Geração Automatizada dos Artefatos]
Executar `gerar_cronograma.py` gerando CSV, Excel Executivo, MS Project XML e Plotly HTML
```

#### A) Passo 1: Esteira Lean de Curto Prazo (Takt Time Planning — WWP)
1. **Divisão em Zonas Takt Equalizadas:** Toda obra deve ser subdividida em 2 a 4 Zonas/Etapas de volumes de serviço equivalentes.
2. **Ciclos Takt Padronizados:** Ciclos fixos de 3 dias úteis (Seg-Qua e Qui-Sáb), totalizando 2 lotes por semana.
3. **Parade of Trades (Vagões Especializados):** Cada disciplina atua em cadeia contínua (ex: Fundações ➔ Estrutura ➔ Alvenaria ➔ Instalações ➔ Reboco ➔ Acabamentos/Pisos ➔ Pintura ➔ Esquadrias/HVAC ➔ Comissionamento).
4. **Regra de Ouro contra Ociosidade (Bancada de Pré-Fabricação / Pulmão Lean):**
   * Enquanto a frente de serviço principal estiver executando serviços mecanizados ou de concretagem direta (ex: retroescavadeira abrindo cavas, caminhão betoneira lançando concreto magro ou de sapatas), os profissionais especializados que não atuam diretamente no lançamento (especialmente **Armadores**) **NUNCA ficam parados no canteiro**.
   * Eles são obrigatoriamente alocados na **Central de Corte e Dobra na Bancada (sob tenda protegida)** pré-fabricando as gaiolas, vigas e estribos do lote subsequente. Isso gera um estoque pulmão puxado (Kanban físico) que garante velocidade máxima na montagem seguinte.
5. **Nivelamento Rigoroso de Recursos (Resource Leveling):**
   * O efetivo diário deve ser rigorosamente constante e respeitar o **Histograma Orçado (EAP 1.0 e RH)** (ex: 7 a 9 operários no início; 14 a 15 no pico estrutural; 10 a 12 nos acabamentos).
   * **PROIBIDO:** Picos artificiais de somatório ingênuo (ex: 30 operários num dia) ou vales de abandono com 4 a 6 operários.
6. **Formato Padrão:** Arquivo `projetos/[OBRA]/03_PLANEJAMENTO_E_CRONOGRAMA/PROGRAMACAO_CURTO_PRAZO_[OBRA].csv`.

#### B) Passo 2: Calibração da Linha de Balanço (LOB / Fluxo Ascendente & Sincronização Bidirecional)
* A Linha de Balanço herda as durações e sequências da Esteira de Produção de forma automatizada via `scripts/sincronizar_esteira_e_lob.py`.
* **Ritmo Takt Construtivo:** O ritmo de avanço é rigorosamente o Takt Time da esteira (`RITMO_DIAS_POR_LOCAL = 3`).
* **Sincronização Bidirecional:**
  - `esteira_para_lob`: Converte os lotes semanais da esteira nas barras contínuas da Linha de Balanço com datas exatas.
  - `lob_para_esteira`: Se o gestor alterar prazos ou setores na Linha de Balanço, a esteira de curto prazo é sincronizada.
* **Detector Inteligente de Sobreposições & Alerta de Efetivo:**
  - O sistema varre automaticamente conflitos espaciais no mesmo setor e sobreposições de frentes da mesma disciplina.
  - Se uma reprogramação acelerar atividades concorrentes, o sistema calcula o salto de headcount diário e emite um alerta com **bloqueio de segurança**:
    `"ALERTA: Sobreposição detectada! Efetivo aumenta de X para Y operários (+Z). Confirma o aumento de efetivo?"`
  - A aplicação de sobreposição exige autorização formal via flag `--permitir-sobreposicao`. Sem essa autorização, o sistema mantém o fluxo em série nivelado (Heijunka).
* **Momento Tecnológico da Cobertura (Regra Crítica de Engenharia):**
  A estrutura metálica de terças e o telhamento termoacústico sandwich **devem ser posicionados imediatamente após a cura e desforma da laje/supraestrutura**. O edifício DEVE ser 100% estancado contra chuva antes do início do reboco mecanizado, impermeabilizações internas e assentamento de porcelanatos.
* **Orientação Canônica:** Zona 01 na base e Zona Superior/Geral no topo, com fluxo ascendente (↗) ao longo do tempo.

#### C) Passo 3: Rede Determinística de Caminho Crítico (CPM)
* Cálculo algorítmico via Teoria dos Grafos usando o script determinístico `scripts/calculadoras/calcular_cpm.py`.
* Verificação de folgas zero e garantia do fechamento dentro da data contratual com margem de segurança de 2 a 3 dias para entrega definitiva das chaves.

#### D) Passo 4: Orquestração Unificada e Geração de Artefatos
* Execução do motor mestre `python scripts/orquestrar_cronogramas.py --obra [OBRA] --gerar-tudo [--takt-dias N]` para compilar e harmonizar simultaneamente:
  - CPM / Gantt determinístico (`dados_cpm.json`);
  - Linha de Balanço e Heijunka (`LINHA_DE_BALANCO.csv`);
  - Curto Prazo em Lotes Takt (`PROGRAMACAO_CURTO_PRAZO_[OBRA].csv`);
  - Histograma Oficial de Mão de Obra e Headcount (`06_SST_E_RH/dados_histograma_mo.json`, `.csv` e `.xlsx`);
  - Físico-Financeiro, Curva S e Auditoria Multi-Eixo de 6 Eixos com tolerância zero para descompassos.
* Para recalcular apenas o Histograma de Mão de Obra: `python scripts/orquestrar_cronogramas.py --obra [OBRA] --histograma`.
* Para reprogramações e crashing de equipe (RUP), acione `python scripts/orquestrar_cronogramas.py --obra [OBRA] --reprogramar --tarefa-id ID [--novo-headcount H]`.
* Para manter a sincronização contínua durante edições de campo ou escritório, utilize o sentinela reativo `python scripts/orquestrar_cronogramas.py --obra [OBRA] --watch`.

---

## 📥 2. Inputs Necessários (O que você deve pedir ao Gestor)
Para agir, você precisa receber:
- **Baseline (Linha de Base):** Qual era a data prevista de início e fim da atividade?
- **Status Real:** Qual a data real de início e a %. de avanço atual?
- **Restrições:** O que está impedindo o avanço (chuva, falta de material, falta de projeto, falta de frente)?

---

## 🛠️ 3. Ações e Entregáveis

Ao ser acionado pelo Gestor devido a um atraso ou reprogramação, você deve:

### A) Calcular o Impacto
- Verificar se a atividade atrasada está no **Caminho Crítico**.
- Estimar quantos dias úteis foram perdidos.
- Projetar a nova data de término.

### B) Propor Soluções (Aceleração)
- **Crashing:** Recomendar aumento de recursos (mais mão de obra, horas extras, turnos adicionais) na atividade atrasada.
- **Fast-Tracking:** Sugerir atividades que poderiam ser feitas em paralelo, que originalmente estavam em sequência.

### C) Relatório de Retorno
Você devolve ao Gestor a seguinte análise:
1. Impacto no Prazo Final (X dias).
2. Atividades Subsequentes Afetadas (Lista).
3. Sugestão de Recuperação do Cronograma.

### D) Critérios de Escalonação
- **Atividade com folga:** Informar ao Gestor; nenhuma ação imediata necessária.
- **Atividade crítica atrasada 1–2 dias:** Propor Crashing ou Fast-Tracking dentro da skill.
- **Atividade crítica atrasada > 3 dias OU SPI < 0,90 por 2 períodos:** Escalonar para `SKILL_GESTAO_16_CRONOGRAMA_E_REPROGRAMACAO.md` para reprogramação formal com nova baseline.
- **Marco contratual em risco:** Escalonar para `SKILL_GESTAO_13_MATRIZ_DE_RISCO.md` + notificação ao cliente via `SKILL_GESTAO_15_COMUNICACAO_CLIENTE.md`.

---
*Fim do Módulo Planejamento. Para reprogramação formal consulte [`SKILL_GESTAO_16`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/gestao/SKILL_GESTAO_16_CRONOGRAMA_E_REPROGRAMACAO.md).*
