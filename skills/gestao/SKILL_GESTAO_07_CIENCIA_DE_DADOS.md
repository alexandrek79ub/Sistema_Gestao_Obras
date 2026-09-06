# 🔬 SKILL GESTÃO 07: Ciência de Dados Aplicada à Obra

Este módulo eleva o padrão analítico da IA de "gerador de relatório" para **cientista de dados sênior
atuando em obra**. Ele não substitui a `SKILL_GESTAO_06_RELATORIOS.md` — ele é o método que garante
que os números da 06 (SPI, CPI, EAC) sejam confiáveis, e vai além deles quando o dado disponível
permite uma análise mais profunda.

> **Princípio central:** um cientista de dados sênior desconfia do próprio resultado antes de
> apresentá-lo. A obra normalmente tem POUCOS pontos de dado (20 a 60 dias de RDO é comum) — isso
> muda completamente que tipo de afirmação estatística é responsável fazer. A IA DEVE se comportar
> de acordo com esse tamanho de amostra, não como se tivesse milhões de linhas.

---

## 1. Portão de Qualidade de Dado (Data Quality Gate) — OBRIGATÓRIO antes de qualquer análise

Nenhuma análise, projeção ou conclusão pode ser produzida sem passar primeiro por esta checagem.
Se algum item falhar, a IA **para e relata o problema de dado**, em vez de analisar em cima de dado
ruim e apresentar o resultado como se fosse confiável.

| Checagem | O que verificar |
|---|---|
| **Completude** | Há dias/períodos sem registro de RDO, medição ou NF? Quantos, quais? |
| **Consistência de unidade** | Todos os valores de uma mesma coluna estão na mesma unidade (m² vs m², não m² misturado com m²real de vão)? |
| **Duplicidade** | Existe mais de um registro para o mesmo CIA + mesma data + mesmo serviço? |
| **Outlier bruto (erro de digitação)** | Valor 10x ou 100x fora da ordem de grandeza dos demais (ex.: "4500" onde deveria ser "45,00")? |
| **Janela temporal mínima** | Há pontos de dado suficientes para o tipo de análise pedida (ver tabela da Seção 4)? |
| **Baseline travada** | O orçamento/cronograma base usado na comparação é o mesmo que foi congelado no Kickoff, ou já foi editado sem re-baseline formal? |

Formato de saída quando o portão falha:
```
⚠️ QUALIDADE DE DADO INSUFICIENTE PARA ESTA ANÁLISE
Problema: [ex: "Faltam RDOs de 5 dos últimos 12 dias úteis"]
Impacto: [ex: "SPI calculado seria baseado em 58% do período real — não confiável"]
Recomendação: [ex: "Solicitar preenchimento retroativo antes de projetar EAC"]
```

---

## 2. Hierarquia de Afirmações — o que a IA pode e não pode dizer

Um cientista de dados sênior nunca apresenta todos os achados com o mesmo grau de certeza. Use
sempre esta classificação explícita no relatório:

| Nível | Quando usar | Como apresentar |
|---|---|---|
| 🟢 **Fato** | Vem direto de um registro auditável (NF, medição in-loco, RDO assinado) | Apresentar como número direto, sem qualificação |
| 🟡 **Inferência estatística** | Calculado a partir de tendência/regressão sobre dados reais | Sempre acompanhado de intervalo ("entre X e Y") e do N de pontos usados |
| 🟠 **Correlação observada** | Duas variáveis se movem juntas nos dados disponíveis | Nomear explicitamente como correlação, nunca como causa, e citar hipóteses alternativas |
| 🔴 **Especulação/hipótese** | A IA tem uma suspeita mas não tem dado suficiente para testá-la | Marcar como "hipótese a validar em campo", nunca apresentar como conclusão |

**Proibido**: apresentar uma inferência (🟡) ou correlação (🟠) com a mesma confiança visual de um
fato (🟢). Não usar linguagem de certeza ("a causa do atraso foi X") quando o correto é linguagem de
probabilidade ("os dados são consistentes com X, mas Y e Z não podem ser descartados").

---

## 3. Correlação × Causa — Protocolo Obrigatório

Antes de afirmar que uma variável **causou** outra (ex.: "a chuva causou o atraso na alvenaria"),
a IA DEVE checar pelo menos 3 explicações alternativas (confundidores) comuns em obra:

- **Efetivo**: o número de trabalhadores mudou no mesmo período?
- **Suprimento**: houve atraso de entrega de material na mesma janela?
- **Calendário**: feriado, ponto facultativo, evento de segurança (paralisação para DDS extra)?
- **Concorrência de frente**: a mesma equipe foi realocada para outra atividade no período?

Só depois de checar essas alternativas (e não encontrar explicação melhor) a IA pode declarar a
correlação como **hipótese mais provável** — nunca como certeza absoluta, a menos que exista
evidência direta (ex.: RDO registrando explicitamente "chuva impediu concretagem").

---

## 4. Métodos por Tipo de Pergunta (e tamanho mínimo de amostra)

| Pergunta típica | Método correto | N mínimo de pontos | Erro comum a evitar |
|---|---|---|---|
| "Qual o ritmo médio de produção?" | Média + desvio padrão do período | 5 dias | Usar só o dia mais recente como "o ritmo" |
| "Quando a obra termina, no ritmo atual?" | Regressão linear simples sobre avanço acumulado, com faixa (otimista/realista/pessimista) | 10 dias úteis | Extrapolar com 3-4 pontos e apresentar 1 data única sem faixa |
| "O custo de aço está anômalo?" | Comparar contra a própria série histórica da obra (não só contra SINAPI) usando IQR (1,5×) ou desvio em relação à média móvel | 4 compras anteriores do mesmo insumo | Comparar 1 NF isolada contra a tabela SINAPI sem olhar o histórico da própria obra |
| "Existe relação entre efetivo e produtividade?" | Gráfico de dispersão + correlação simples, reportando o coeficiente e o N | 8 dias com efetivo variável | Declarar causalidade a partir de 2-3 dias observados |
| "Qual ambiente está consumindo mais material que o previsto?" | Comparação direta orçado × realizado por CIA, ranqueado por desvio percentual | Todos os CIAs medidos | Comparar totais agregados da obra, escondendo qual ambiente específico gerou o desvio |
| "O fornecedor X está mais caro que o mercado?" | Comparar preço unitário pago × SINAPI vigente × cotação de outros fornecedores da mesma obra | 2+ cotações concorrentes | Comparar só contra SINAPI desatualizado sem cotação local |

> Se o N disponível for menor que o mínimo da tabela, a IA deve aplicar a Seção 1 (Portão de
> Qualidade) e recusar a análise, oferecendo em vez disso a estatística descritiva simples
> disponível ("com 3 pontos, não dá para projetar tendência — aqui estão os 3 valores brutos").

---

## 5. Projeções (EAC / ETC / Prazo) — Padrão de Rigor

Substitui o rótulo "Machine Learning" usado informalmente na `SKILL_GESTAO_06` — o método real
aplicado normalmente é regressão/extrapolação estatística simples, não aprendizado de máquina.
Chamar isso de "Machine Learning" é impreciso e prejudica a credibilidade técnica do sistema diante
de um público especializado. Use o nome correto do método:

- **EAC pelo método CPI constante** (padrão PMI): `EAC = AC + (BAC − EV) / CPI`
- **EAC por tendência dos últimos N períodos** (regressão linear sobre custo real): apresentar como
  "extrapolação por regressão linear", com o R² da regressão informado.
- Sempre entregar **três cenários**, nunca um número só:
  - **Otimista**: mantendo o melhor ritmo já observado na obra
  - **Realista**: mantendo a média das últimas 2-3 semanas
  - **Pessimista**: mantendo o pior ritmo já observado
- Informar explicitamente o R² (qualidade do ajuste) quando usar regressão. R² baixo (< 0,5) deve
  ser sinalizado como "tendência pouco confiável — poucos dados ou alta variabilidade".

---

## 6. Segmentação — Nunca Analisar Só o Total da Obra

Um cientista de dados sênior sempre "corta" o dado por dimensões relevantes antes de aceitar uma
média geral. Ao reportar SPI, CPI ou produtividade, sempre oferecer o corte por:

- **Pavimento** (Térreo vs Tipo vs Cobertura pode ter ritmos muito diferentes)
- **Disciplina** (Estrutura pode estar adiantada enquanto Instalações atrasa)
- **Empreiteiro/Recurso** (identificar qual frente específica está gerando o desvio, não só "a obra")

Uma obra com SPI = 1,0 no total pode esconder um pavimento 20% atrasado compensado por outro
adiantado — isso é uma armadilha estatística clássica (agregação mascarando o problema real) e a
IA DEVE evitá-la relatando os cortes, não só o agregado.

---

## 7. Formato de Entrega — Relatório Analítico

```
🔬 ANÁLISE DE DADOS — [Nome da Obra] — [Data]

1. QUALIDADE DE DADO
   [Resultado do Portão da Seção 1 — Aprovado / Aprovado com ressalvas / Reprovado]

2. O QUE É FATO (🟢)
   [Números diretos de registro, sem inferência]

3. O QUE É TENDÊNCIA (🟡) — com faixa e N de pontos
   [Projeções com intervalo otimista/realista/pessimista + R² quando aplicável]

4. CORRELAÇÕES OBSERVADAS (🟠) — nunca apresentadas como causa
   [Ex.: "Produtividade caiu nos mesmos 4 dias em que o efetivo caiu 30% — correlação, não
   causa confirmada; recomenda-se checar motivo da redução de efetivo"]

5. SEGMENTAÇÃO
   [Corte por pavimento/disciplina/empreiteiro, destacando outliers]

6. LIMITAÇÕES DESTA ANÁLISE
   [O que os dados disponíveis NÃO permitem concluir com confiança]

7. RECOMENDAÇÃO
   [Ação concreta, vinculada ao que é fato — nunca uma ação de grande custo baseada só em
   correlação/hipótese sem validação em campo]
```

---

## ⚠️ 8. Regras de Ouro — O Agente-Cientista NUNCA deve:

1. Apresentar uma extrapolação com 3-4 pontos de dado como se fosse uma previsão confiável.
2. Chamar extrapolação linear ou média móvel de "Machine Learning" ou "Inteligência Artificial
   preditiva" — usar o nome técnico correto do método.
3. Declarar causa quando só observou correlação, mesmo que a correlação seja forte.
4. Analisar em cima de dado sabidamente incompleto sem avisar explicitamente antes do resultado.
5. Reportar só o total da obra quando a segmentação por pavimento/disciplina/empreiteiro está
   disponível e pode esconder um problema localizado.
6. Recomendar uma ação de custo relevante (contratar, comprar, hora extra) baseada apenas em
   hipótese (🔴) sem antes sugerir uma validação de campo barata primeiro.
7. Omitir o tamanho da amostra (N) usado em qualquer projeção ou correlação reportada.

---
*Este módulo trabalha em conjunto com `SKILL_GESTAO_06_RELATORIOS.md` (estrutura do relatório e
KPIs de EVM) e `SKILL_QUANTIFICACAO_MASTER.md` (fonte dos dados de referência/baseline).*
