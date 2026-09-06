# 📅 SKILL GESTÃO 16: Cronograma, Reprogramação e Plano de Ataque

Cobre como o cronograma nasce, como é medido no seu próprio ritmo (não só via SPI agregado),
quando e como é reprogramado, e como um atraso vira plano de recuperação com lastro em dado real,
não em "vamos colocar mais gente e torcer".

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

## ⚠️ 7. Regras de Ouro

1. Duração de atividade nasce do RUP meta, nunca de estimativa "sentida" sem lastro em
   produtividade (histórico próprio ou referência).
2. Obra com repetição vertical relevante mantém Gantt E Linha de Balanço — nunca só um dos dois.
3. Reprogramação nunca sobrescreve a baseline — sempre gera versão nova, mantendo a anterior
   visível.
4. Gatilho de reprogramação é objetivo (SPI sustentado abaixo do limiar, ou risco real
   identificado) — nunca decisão de humor do momento.
5. Nenhum plano de recuperação de prazo é proposto sem checar o RUP histórico da frente
   específica — "aumentar efetivo" sem essa checagem é aposta, não plano.
6. Caminho crítico e colisão de linha de balanço são sempre calculados por script, nunca
   estimados visualmente pelo agente.

---
*Trabalha junto com `SKILL_GESTAO_08_PRODUTIVIDADE_E_RECURSOS.md` (fonte do RUP),
`SKILL_GESTAO_14_CONTROLE_DE_REVISAO.md` (versionamento) e `SKILL_GESTAO_13_MATRIZ_DE_RISCO.md`
(gatilho de risco para reprogramação).*
