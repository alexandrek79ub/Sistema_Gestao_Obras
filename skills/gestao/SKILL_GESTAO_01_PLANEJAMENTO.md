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

### 1.3 Gestão em 3 Níveis & Esteira Lean de Curto Prazo (Takt Time Planning)

O ecossistema opera o cronograma em **3 níveis de maturidade 5D**:
1. **Longo Prazo (Linha de Balanço - LOB & CPM):**
   - Define o prazo global contratual (ex: 180 dias / 26 semanas), o caminho crítico determinístico e os ritmos de avanço vertical/setorial em fluxo ascendente.
2. **Médio Prazo (Lookahead 4 a 6 Semanas):**
   - Identificação e remoção ativa de restrições (projetos, compras, contratações de empreiteiros, liberações de FVS).
3. **Curto Prazo (Plano Semanal / Lotes em Esteira Lean - WWP):**
   - **Regra de Ouro da Esteira de Produção Construtiva:**
     A mão de obra nunca deve ser alocada de forma caótica ou agrupada sem sequência temporal. Para evitar ociosidade e picos irreais, **toda obra deve ser dividida em 2 a 3 Etapas Construtivas (Zonas Takt) de volumes de serviço equalizados**.
   - **Mecanismo da Linha de Montagem (Parade of Trades / Vagões Especializados):**
     * Cada disciplina atua como um "vagão" que se desloca de zona em zona em ritmo fixo (Takt Time padrão = 3 dias úteis: Seg-Qua e Qui-Sáb).
     * **Eliminação da Espera Tecnológica de Cura:** Enquanto a Zona 1 está concretando e cumprindo o período de cura (ganho de fck e resistência), as equipes especializadas de carpintaria e armação **NUNCA ficam ociosas**: elas avançam imediatamente para montar as fôrmas da Zona 2! Quando a Zona 2 está curando, a carpintaria avança para a Zona 3 ou retorna para montar vigas e pilares da Zona 1 que já desformaram.
   - **Nivelamento Rigoroso de Recursos (Resource Leveling):**
     * O efetivo real diário de campo deve ser rigorosamente constante ao longo de cada semana, calibrado com o teto mensal orçado no **Histograma de Mão de Obra (EAP 1.0 e RH)**.
     * **É PROIBIDO** gerar cronogramas com anomalias de picos fictícios (ex: somar linhas de atividades independentes resultando em 36 operários simultâneos) ou vales de abandono (ex: 6 operários em 1 dia deixando os outros 5 dias úteis sem trabalho).
   - **Padrão de Arquivo:** Todo cronograma de curto prazo deve ser gerado no arquivo `projetos/[OBRA]/03_PLANEJAMENTO_E_CRONOGRAMA/PROGRAMACAO_CURTO_PRAZO_[OBRA].csv` contendo:
     `COD_LOTE`, `SEMANA`, `DIAS_SEMANA`, `ETAPA_ZONA`, `VAGAO_ESTEIRA`, `SERVICO_LOTE`, `META_FISICA`, `DURACAO_DIAS`, `EQUIPE_PREVISTA`, `HEADCOUNT_PREVISTO`, `EQUIPAMENTOS_PREVISTOS`, `MATERIAIS_UCC`, `RUP_META_HH_UNID`, `STATUS_EXECUCAO`, `RDO_VINCULADO`.

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
