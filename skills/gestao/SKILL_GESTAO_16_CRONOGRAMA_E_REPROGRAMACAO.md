# 📅 SKILL GESTÃO 16: Cronograma, Reprogramação e Plano de Ataque

Cobre como o cronograma nasce, como é medido no seu próprio ritmo (não só via SPI agregado),
quando e como é reprogramado, e como um atraso vira plano de recuperação com lastro em dado real,
não em "vamos colocar mais gente e torcer".

---

## ⚠️ PRÉ-REQUISITO OBRIGATÓRIO — PORTÃO DE QUALIDADE DE DADO
Antes de apresentar **qualquer número, projeção ou recomendação** desta skill, o agente DEVE verificar o nível de confiança de cada dado de entrada consultando a `SKILL_GESTAO_07_CIENCIA_DE_DADOS.md` (Seção 1: Hierarquia de Confiança) ou rodando o script `scripts/calculadoras/portao_qualidade_dado.py`.

Formato obrigatório de declaração antes de qualquer análise:
| Dado | Fonte | Confiança | Observação |
|---|---|---|---|
| [dado usado] | [arquivo/CSV] | 🟢/🟡/🔴 | [caveats] |

**NÃO prosseguir com análise se qualquer dado crítico for 🔴.**

---

## 1. Duração das Atividades Nasce do RUP, Não de Achismo

```
Duração estimada (dias) = (Quantidade do serviço × RUP meta) ÷ (Efetivo alocado × Horas/dia)
```

- Usa a mesma meta de RUP definida na `SKILL_GESTAO_08`, Seção 1.2 — nunca uma duração
  "sentida" independente da produtividade que a própria obra já documentou ou referenciou.
- Ao longo da execução, se o RUP real diverge da meta (`SKILL_GESTAO_08`, alerta de 3+ períodos),
  a duração **restante** das atividades subsequentes do mesmo tipo deve ser recalculada com o RUP
  real, não mantida na estimativa original — cronograma que ignora produtividade real vivida vira
  ficção rapidamente.

---

## 2. Gantt (CPM) × Linha de Balanço — Ferramentas Diferentes, Não Substitutas

| Ferramenta | Quando usar | O que revela que a outra esconde |
|---|---|---|
| **Gantt / Caminho Crítico (CPM)** | Atividades não repetitivas, dependências complexas (fundação, instalações especiais, marcos contratuais) | Folga de cada atividade, qual atraso realmente compromete o prazo final |
| **Linha de Balanço** | Atividades repetitivas verticalizadas (alvenaria, reboco, pintura subindo por pavimento) | Ritmo (velocidade) de cada frente — se uma equipe mais rápida vai "alcançar" e colidir com a equipe da atividade predecessora, o Gantt não mostra isso |

**Regra**: obra com repetição vertical relevante (prédio de vários pavimentos) deveria manter as
duas ferramentas simultaneamente, cada uma vendo o que a outra não vê.

---

## 3. Reprogramação — Regras, Não Impulso

- **Baseline nunca é sobrescrita** — toda reprogramação gera uma **nova versão** do cronograma,
  a original permanece visível para comparação (mesma disciplina da `SKILL_GESTAO_14`).
- **Gatilho objetivo de reprogramação** (não é "quando alguém achar que deu"):
  - SPI abaixo de um limiar definido (referência: 0,90) sustentado por **2 ou mais períodos**
    consecutivos — mesma lógica de sequência mínima usada no RUP (`SKILL_GESTAO_08`).
  - Marco contratual com risco real identificado (`SKILL_GESTAO_13`, matriz de risco).
- Reprogramação recalcula a duração das atividades **restantes** usando o RUP real observado
  (Seção 1), nunca reaplicando a meta original que já provou não se sustentar.

---

## 4. Plano de Ataque — Táticas com Limite Conhecido, Não "Empurrar Mais Gente"

| Tática | Descrição | Limite/risco a checar antes de aplicar |
|---|---|---|
| **Fast-tracking** | Rodar em paralelo atividades originalmente sequenciais | Aumenta risco de retrabalho/conflito de frente — cruzar com `SKILL_GESTAO_11` |
| **Crashing (reforçar efetivo)** | Aumentar mão de obra na mesma frente | RUP tende a piorar com efetivo excessivo em espaço apertado — checar RUP histórico da própria obra em situação de efetivo elevado antes de assumir ganho linear |
| **Hora extra / turno adicional** | Mais horas, mesmo efetivo | Produtividade por hora cai com fadiga além de certo ponto — não tratar como ganho proporcional às horas extras |
| **Resequenciar atividades com folga** | Liberar recurso de atividade não crítica para reforçar o caminho crítico | Só é seguro com o caminho crítico corretamente calculado (Seção 5) — sem isso, não se sabe o que realmente tem folga |

**Regra de ouro**: nenhuma tática de recuperação de prazo é recomendada sem checar o histórico de
RUP real daquela frente/empreiteiro — "colocar mais gente" só é aconselhável se o dado mostrar que
a frente ainda tem espaço de rendimento, não está saturada.

---

## 5. Cálculo de Caminho Crítico e Folga — Sempre por Script

Cálculo de CPM (forward pass, backward pass, folga) é **algoritmo determinístico clássico** — não
deve ser estimado pela LLM. Usar `calcular_cpm.py` (script determinístico) sempre que precisar
determinar caminho crítico e folga de cada atividade.

---

## 6. Detecção de Colisão na Linha de Balanço — Também por Script

Verificar se uma frente mais rápida "alcança" a frente predecessora (colisão de ritmo) é geometria
de retas (posição × tempo) — cálculo determinístico. Usar `detectar_colisao_linha_balanco.py`.

---

## 8. Sincronização Obrigatória: O Triângulo da Verdade Única (CPM ↔ LOB ↔ Takt Curto Prazo)

Toda revisão de cronograma (ou elaboração de nova baseline) deve ser **orquestrada de forma atômica e simultânea nos 3 níveis**:

1. **A Esteira Define a Realidade:** A duração dos ciclos Takt (flexível de 1 a 6 dias úteis via `--takt-dias N`), os lotes semanais e as equipes dimensionadas com suas metas de RUP formam a base concreta do planejamento.
2. **A Linha de Balanço Reflete a Esteira:** As datas de início e término de cada setor físico na Linha de Balanço (LOB) devem herdar rigorosamente o encadeamento dos lotes da esteira.
3. **Momento Crítico da Cobertura:** A montagem de estruturas metálicas de cobertura e telhas termoacústicas deve ser posicionada **imediatamente após a desforma da laje**. É terminantemente proibido projetar cronogramas com alvenaria e reboco avançando por semanas sem telhado estanque.
4. **Alocação Sem Ociosidade (Bancada Pulmão):** Em períodos de concretagem ou escavação direta, equipes auxiliares/especialistas (ex: armadores) operam na central de corte e dobra na bancada, acumulando peças pré-montadas para os lotes futuros.
5. **Detector de Sobreposição e Alerta de Efetivo:** O sistema varre conflitos espaciais no mesmo setor e duplicação de frentes. Para manter o fluxo nivelado Heijunka (status `CONFORME_FLUXO_NIVELADO`), o efetivo se mantém dentro do teto orçado.
6. **Aceleração por Aumento de Equipe (Crashing via RUP):** Ao acelerar frentes com `--novo-headcount H`, a duração cai proporcionalmente à RUP ($\text{Nova Duração} = \text{Duração Antiga} \times \frac{\text{Headcount Base}}{\text{Novo Headcount}}$) e o grafo topológico (DAG) propaga a antecipação para o CPM, LOB e lotes de curto prazo.
7. **Sincronização Contínua do Histograma de Mão de Obra (`scripts/gerar_histograma_sincronizado.py`):**
   - Toda alteração de prazo ou aumento de equipe no curto prazo recalcula instantaneamente o Histograma de Mão de Obra (Headcount & HH).
   - O mês correspondente absorve o novo pico da disciplina e atualiza as Horas-Homem ($\text{Headcount} \times 220\text{ h/mês}$).
   - Regera simultaneamente `06_SST_E_RH/dados_histograma_mo.json`, `HISTOGRAMA_MAO_DE_OBRA_[SIGLA].csv` e `.xlsx`.
8. **Orquestrador Central e File Watcher (`scripts/orquestrar_cronogramas.py`):**
   - Criação de nova obra: `python scripts/orquestrar_cronogramas.py --obra NOVA_OBRA --gerar-tudo --takt-dias 3`
   - Reprogramação atômica: `python scripts/orquestrar_cronogramas.py --obra [OBRA] --reprogramar --tarefa-id ID [--novo-headcount H]`
   - Recalcular apenas o Histograma: `python scripts/orquestrar_cronogramas.py --obra [OBRA] --histograma`
   - Sincronização total: `python scripts/orquestrar_cronogramas.py --obra [OBRA] --sincronizar`
   - Sentinela em tempo real: `python scripts/orquestrar_cronogramas.py --obra [OBRA] --watch` (detecta edições no Excel/IDE e auto-harmoniza em < 2s).

---

## ⚠️ 7. Regras de Ouro

1. Duração de atividade nasce do RUP meta, nunca de estimativa "sentida" sem lastro em produtividade (histórico próprio ou referência).
2. Obra com repetição vertical relevante mantém Gantt E Linha de Balanço — nunca só um dos dois.
3. Reprogramação nunca sobrescreve a baseline — sempre gera versão nova, mantendo a anterior visível.
4. Gatilho de reprogramação é objetivo (SPI sustentado abaixo do limiar, ou risco real identificado) — nunca decisão de humor do momento.
5. Nenhum plano de recuperação de prazo é proposto sem checar o RUP histórico da frente específica — "aumentar efetivo" sem essa checagem é aposta, não plano.
6. Caminho crítico e colisão de linha de balanço são sempre calculados por script, nunca estimados visualmente pelo agente.
7. **O cronograma mestre (LOB e CPM) deve ser sempre calibrado em cima da Esteira Lean:** frentes de curto prazo niveladas, zero ociosidade com central de bancada, e cobertura montada logo após a desforma estrutural.
8. **Sincronização Atômica Obrigatória via Orquestrador:** Toda alteração de prazo ou efetivo deve atualizar simultaneamente `dados_cpm.json`, `LINHA_DE_BALANCO.csv`, `PROGRAMACAO_CURTO_PRAZO_*.csv` e o Histograma de Mão de Obra em `06_SST_E_RH/` via `scripts/orquestrar_cronogramas.py`.
9. **Auditoria de Conformidade Multi-Eixo (6 Eixos):** Antes de oficializar qualquer baseline ou revisão, é mandatório rodar `python scripts/auditar_cronogramas.py --obra [OBRA]`, assegurando que CPM, Linha de Balanço, Esteira Takt, Orçamento Físico-Financeiro e Histograma de Mão de Obra estejam 100% harmonizados e com 0 divergências.

---
*Trabalha junto com `SKILL_GESTAO_01_PLANEJAMENTO.md` (arquitetura do plano), `SKILL_GESTAO_08_PRODUTIVIDADE_E_RECURSOS.md` (fonte do RUP e nivelamento de recursos), `SKILL_GESTAO_14_CONTROLE_DE_REVISAO.md` (versionamento) e `SKILL_GESTAO_13_MATRIZ_DE_RISCO.md` (gatilho de risco para reprogramação).*
