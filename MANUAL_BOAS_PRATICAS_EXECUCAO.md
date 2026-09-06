# 📖 MANUAL DE BOAS PRÁTICAS DE EXECUÇÃO

Mapa por fase de obra, indexando os 25 POPs, com os pontos de maior risco de retrabalho de cada
etapa e os **checkpoints topográficos obrigatórios** — o momento em que a obra não deveria avançar
para a próxima fase sem uma conferência de precisão (POP_21), porque um erro geométrico não
corrigido agora se multiplica (e fica muito mais caro de corrigir) nas fases seguintes.

> Este manual não substitui os POPs — é a camada de navegação e sequenciamento entre eles, no
> mesmo espírito do `INDICE_MESTRE_SKILLS.md` para as skills de gestão.

---

## 1. Por Que o Checkpoint Topográfico Vem Antes de Avançar de Fase

Um erro de locação na fundação não desaparece — ele **se propaga e piora** em cada fase seguinte:
um eixo fora de posição na fundação gera pilar fora de prumo na estrutura, que gera parede fora de
esquadro na alvenaria, que gera **espessura de reboco desigual e cara** para disfarçar o erro
(o próprio POP_21 já nomeia isso: "desperdício massivo de revestimento para consertar o erro de
quem levantou a parede"). Corrigir na origem custa uma fração do que custa disfarçar depois.

**Regra geral do manual**: nenhuma fase é liberada para a próxima sem o checkpoint topográfico
correspondente assinado/registrado — isso é responsabilidade de quem fiscaliza a obra, não uma
sugestão opcional.

---

## 2. Mapa por Fase

### Fase 1 — Fundação
**POPs**: `POP_10_FUNDACOES`, `POP_11_CONCRETAGEM`, `POP_22_CONTROLE_CONCRETO`
**Prática crítica**: locação de eixos X/Y com Estação Total, gabarito travado rigorosamente
(POP_21, Seção 2).
**✅ Checkpoint topográfico antes de avançar**: conferência dos eixos principais e cotas de nível
das estacas/blocos **antes de concretar a próxima etapa (baldrame/estrutura)** — erro na fundação é
o mais caro de todos para corrigir depois de coberto por concreto.

### Fase 2 — Estrutura
**POPs**: `POP_19_FORMAS_CIMBRAMENTO`, `POP_11_CONCRETAGEM`, `POP_22_CONTROLE_CONCRETO`
**Prática crítica**: prumo de forma antes da concretagem — forma fora de prumo gera pilar fora de
prumo, irreversível depois de curado.
**✅ Checkpoint topográfico**: prumo e nível de cada pavimento conferidos com nível a laser
(POP_21, Seção 1) **antes da desforma ser liberada para a próxima etapa**, e aferição semanal do
aparelho contra prumo físico.

### Fase 3 — Alvenaria
**POPs**: `POP_12_ALVENARIA`
**Prática crítica**: prumo de face com régua de 2m + nível de bolha, tolerância máxima de 3mm a
cada 2 metros (POP_21, Seção 2).
**✅ Checkpoint topográfico**: conferência de esquadro e prumo de **todas as paredes** antes de
liberar o início do chapisco/reboco — é o último ponto em que corrigir uma parede é barato;
depois do reboco aplicado, corrigir esquadro significa demolir revestimento pronto.

### Fase 4 — Instalações (embutidas)
**POPs**: `POP_15_INSTALACOES_HIDROS`, `POP_16_INSTALACOES_ELETRICAS`
**Prática crítica**: conferência de posicionamento de pontos contra o projeto antes do fechamento
com reboco/contrapiso — ponto embutido errado só é descoberto (caro) depois de acabamento pronto.
**✅ Checkpoint**: teste de estanqueidade hidráulica (pressão) e continuidade elétrica antes do
fechamento — não é topográfico, mas segue a mesma lógica de "testar antes de esconder".

### Fase 5 — Revestimentos
**POPs**: `POP_13_REVESTIMENTOS`, `POP_14_IMPERMEABILIZACAO`
**Prática crítica**: espessura de reboco controlada por taliscamento (1,5-2,5cm ideal, POP_13),
tempo de cura do chapisco (mínimo 3 dias) respeitado antes do emboço.
**✅ Checkpoint**: se o checkpoint da Fase 3 foi bem-feito, a espessura de reboco aqui deveria ser
uniforme — espessura muito irregular nesta fase é sinal de que o checkpoint anterior falhou ou foi
pulado, vale investigar antes de simplesmente aplicar mais argamassa para compensar.

### Fase 6 — Cobertura
**POPs**: `POP_24_COBERTURA`
**Prática crítica**: caimento mínimo por tipo de telha, fixação na crista (nunca no vale), rufos e
calhas como ponto de maior risco de infiltração.
**✅ Checkpoint**: teste de estanqueidade com água **antes** de liberar o forro/acabamento interno
abaixo — nunca fechar o forro sem confirmar ausência de infiltração primeiro.

### Fase 7 — Esquadrias
**POPs**: `POP_25_ESQUADRIAS`
**Prática crítica**: conferência de esquadro do vão antes da instalação, argamassamento completo
do contramarco (nunca deixar vazio), pingadeira no peitoril.
**✅ Checkpoint**: teste de funcionamento (abertura/fechamento) e estanqueidade antes da entrega —
mesma lógica de nunca entregar por inspeção visual isolada.

### Fase 8 — Entrega
**POPs**: `POP_18_ENTREGA_DATABOOK`, `SKILL_GESTAO_12_ENCERRAMENTO_DE_OBRA`
**Prática crítica**: checklist de encerramento com evidência documental, nunca por suposição
(já coberto em detalhe na skill de encerramento).

---

## 3. Tolerâncias de Referência — Consolidado em Um Só Lugar

| Item | Tolerância | Fonte |
|---|---|---|
| Desaprumo de face de alvenaria | Máx. 3mm a cada 2m | POP_21 |
| Espessura de reboco | 1,5cm a 2,5cm (acima de 3cm, risco de desplacamento) | POP_13 |
| Cura de chapisco antes do emboço | Mín. 3 dias | POP_13 |
| Cura de reboco antes de pintura | 21-28 dias | POP_13 |
| Cura de reboco antes de cerâmica | Mín. 14 dias | POP_13 |
| Aferição de nível a laser | Semanal, contra prumo físico | POP_21 |

---

## ⚠️ 4. Regra de Ouro do Manual

**Nenhuma fase avança sem o checkpoint da fase anterior registrado.** Se um checkpoint foi pulado
e um problema aparece 2-3 fases depois (ex.: reboco irregular na Fase 5 por erro de prumo não
pego na Fase 3), a causa raiz deve ser investigada retroativamente — aplicando o protocolo de
correlação×causa da `SKILL_GESTAO_07` — antes de simplesmente corrigir o sintoma visível.

---
*Este manual referencia os POPs 10 a 25 e trabalha junto com `SKILL_GESTAO_11_QUALIDADE_NAO_CONFORMIDADE.md`
(registro formal quando um checkpoint revela desvio) e `SKILL_GESTAO_07_CIENCIA_DE_DADOS.md`
(investigação de causa raiz quando o problema só aparece fases depois).*
