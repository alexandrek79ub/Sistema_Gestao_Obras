# 📊 SKILL GESTÃO 08: Produtividade, Efetivo, Desperdício e Melhoria Contínua

Cobre quatro dores interligadas de gestão de obra que a `SKILL_GESTAO_06` (EVM/relatórios) e a
`SKILL_GESTAO_07` (ciência de dados) não resolvem sozinhas: **quanto cada equipe realmente produz
por dia**, **quem está na obra e onde**, **quanto está sendo desperdiçado**, e **como transformar
isso num ciclo de melhoria, não só num relatório**.

> Este módulo usa a Hierarquia de Afirmações e o Portão de Qualidade de Dado da `SKILL_GESTAO_07`
> como pré-requisito. Nenhuma métrica de produtividade aqui deve ser calculada sem passar por eles.

---

## ⚠️ PRÉ-REQUISITO OBRIGATÓRIO — PORTÃO DE QUALIDADE DE DADO
Antes de apresentar **qualquer número, projeção ou recomendação** desta skill, o agente DEVE verificar o nível de confiança de cada dado de entrada consultando a `SKILL_GESTAO_07_CIENCIA_DE_DADOS.md` (Seção 1: Hierarquia de Confiança) ou rodando o script `scripts/calculadoras/portao_qualidade_dado.py`.

Formato obrigatório de declaração antes de qualquer análise:
| Dado | Fonte | Confiança | Observação |
|---|---|---|---|
| [dado usado] | [arquivo/CSV] | 🟢/🟡/🔴 | [caveats] |

**NÃO prosseguir com análise se qualquer dado crítico for 🔴.**

---

## 1. Produtividade — RUP (Razão Unitária de Produção)

RUP é a métrica padrão do setor pra medir produtividade de mão de obra:

```
RUP = Homens-hora consumidos ÷ Quantidade de serviço executada
(ex.: Hh / m² de alvenaria, Hh / m³ de concreto lançado)
```

Quanto **menor** o RUP, melhor a produtividade (menos hora-homem por unidade de serviço).

### 1.1 Duas versões do RUP — usar as duas, nunca só uma

| Versão | Fórmula | Serve pra |
|---|---|---|
| **RUP Cíclica (diária/semanal)** | Hh do período ÷ quantidade executada no período | Detectar problema **rápido** — reage no mesmo dia/semana |
| **RUP Cumulativa** | Hh acumulado do serviço ÷ quantidade acumulada executada | Ver a tendência **real** do serviço inteiro — menos sujeita a ruído de um dia ruim isolado |

**Regra de ouro**: RUP cíclica ruim em 1 dia isolado é ruído (chuva, falta de material, feriado —
ver protocolo de correlação×causa da `SKILL_GESTAO_07`, Seção 3). RUP cíclica ruim em **3 ou mais
períodos consecutivos** é sinal real de problema — só aí vira alerta.

### 1.2 De onde vem a meta de RUP

Em ordem de prioridade (a mais confiável primeiro):

1. **RUP histórico da própria obra/empresa** em serviço equivalente (se existir) — mais confiável,
   já reflete a realidade local de equipe e método.
2. **RUP de referência de mercado** (TCPO ou base própria calibrada) — usar quando não há
   histórico próprio, mas **sempre ajustar** pelas condições locais (verticalização, clima,
   experiência da equipe) e declarar esse ajuste como premissa.
3. **Nunca usar meta "no chute"** — se não há nenhuma referência, a IA deve dizer isso
   explicitamente e sugerir medir as primeiras 2 semanas pra estabelecer a linha de base antes de
   cobrar meta.

### 1.3 Cálculo diário

Fonte de dado: RDO (efetivo do dia × horas trabalhadas) + medição do serviço executado no dia
(vem da mesma lógica de medição da `SKILL_QUANTIFICACAO_MASTER`, nunca estimativa visual).

```
RUP do dia = (Nº de trabalhadores da frente × horas trabalhadas) ÷ quantidade medida executada no dia
```

Se a quantidade executada no dia não foi medida (só "avanço visual"), aplica-se a **Regra da
Trena** já existente — não se calcula RUP em cima de estimativa não medida, marca como 🔴 no
Portão de Qualidade de Dado.

---

## 2. Controle de Efetivo

Tabela mínima a manter, atualizada diariamente a partir do RDO:

| Campo | Descrição |
|---|---|
| Data | |
| Frente/Serviço | A qual CIA/atividade do cronograma essa equipe está alocada |
| Empreiteiro/Equipe | Quem é o responsável por essa mão de obra |
| Função | Pedreiro, servente, armador, etc. |
| Nº de trabalhadores presentes | Vem do RDO, não de estimativa |
| Horas trabalhadas | |

### 2.1 Cruzamentos que essa tabela habilita (aplicando a Seção 6 da `SKILL_GESTAO_07`)

- **Efetivo planejado × efetivo real por frente** — dimensionamento de equipe estava certo?
- **Efetivo alocado × cronograma** — tem gente sobrando numa frente atrasada e faltando numa
  adiantada? Isso é rebalanceamento óbvio que só aparece se a IA cruzar as duas tabelas.
- **Correlação efetivo × RUP** — confirma ou refuta hipótese de queda de produtividade por
  redução de equipe (sempre seguindo o protocolo de correlação×causa, nunca declarando causa
  direto).

---

## 3. Desperdício (Mão de Obra, Material, Equipamento)

### 3.1 Desperdício de material — a métrica é sempre comparativa, nunca isolada

```
Índice de perda real = (Quantidade comprada − Quantidade efetivamente aplicada, medida pelo
quantitativo) ÷ Quantidade orçada
```

- **Quantidade comprada** vem das notas fiscais/pedidos (já coberto pela conciliação de 3 pontas
  discutida com o usuário).
- **Quantidade efetivamente aplicada** vem da medição do serviço executado (mesma fonte da
  memória de cálculo), nunca de "sobrou pouco, então gastou tudo".
- **Comparar sempre contra um índice de perda de referência do próprio material** (TCPO/histórico
  da obra tem índices de perda padrão por material — ex.: bloco cerâmico tem perda esperada
  diferente de granito). Nunca tratar toda perda acima de zero como anomalia — materiais têm
  perda técnica esperada, o alerta é quando a perda **excede** o índice de referência.

### 3.2 Desperdício de mão de obra

Manifesta-se como RUP pior que a meta sem explicação técnica válida (ver protocolo de
correlação×causa antes de declarar "desperdício de mão de obra" como causa — pode ser
retrabalho, pode ser espera de material, pode ser efetivo mal dimensionado).

### 3.3 Desperdício/ociosidade de equipamento

Rastrear: horas locadas/disponíveis × horas efetivamente em uso (do RDO). Equipamento locado
parado é custo puro sem contrapartida — deveria aparecer no relatório de desvio com a mesma
prioridade que desvio de material.

---

## 4. Ciclo de Melhoria Contínua (PDCA aplicado à obra)

Uma meta sem ciclo de retroalimentação é só um número decorativo. O agente deve estruturar isso
como um loop, não como relatório único:

```
1. META      → RUP alvo definido (Seção 1.2) por serviço/frente
2. MEDIR     → RUP real diário/semanal (Seção 1.3), efetivo (Seção 2), desperdício (Seção 3)
3. COMPARAR  → Real × Meta, segmentado por frente/empreiteiro (nunca só o agregado da obra)
4. DIAGNOSTICAR → Aplicar protocolo de correlação×causa da SKILL_GESTAO_07 antes de apontar motivo
5. AGIR      → Ação corretiva registrada (o quê, quem, prazo)
6. RECALIBRAR → Meta ajustada com base no que foi aprendido, não fica estática pra sempre
```

**Regra de ouro**: a IA nunca fecha o ciclo no passo 3 (comparar) apresentando só o desvio como
"problema do empreiteiro" — precisa passar pelo passo 4 (diagnóstico com rigor estatístico) antes
de qualquer recomendação de ação no passo 5.

---

## ⚠️ 5. Regras de Ouro deste módulo

1. RUP nunca é calculado sobre quantidade "estimada visualmente" — só sobre quantidade medida.
2. Um único dia ruim de RUP não é alerta — só é problema real com 3+ períodos consecutivos fora
   da meta (aplicando o mesmo cuidado de amostra pequena da `SKILL_GESTAO_07`).
3. Meta de produtividade sem fonte (nem histórico, nem referência) deve ser assumida como
   "linha de base ainda não estabelecida", nunca inventada.
4. Desperdício de material só é reportado como anomalia quando excede o índice de perda técnica
   esperado daquele material especificamente — não existe "zero perda" como referência.
5. Toda métrica desta skill deve ser reportada segmentada por frente/empreiteiro, nunca só o
   agregado da obra (mesma regra da Seção 6 da `SKILL_GESTAO_07`).
6. O ciclo de melhoria contínua não termina no diagnóstico — precisa registrar a ação corretiva e
   revisitar a meta depois de aplicada, ou o ciclo fica incompleto.

---
*Este módulo trabalha junto com `SKILL_QUANTIFICACAO_MASTER.md` (fonte da medição de serviço
executado), `SKILL_GESTAO_06_RELATORIOS.md` (KPIs de EVM) e `SKILL_GESTAO_07_CIENCIA_DE_DADOS.md`
(rigor estatístico e protocolo de correlação×causa).*
