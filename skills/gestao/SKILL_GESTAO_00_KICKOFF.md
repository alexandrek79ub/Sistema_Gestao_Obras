# 🚀 SKILL GESTÃO 00: Implantação e Kickoff da Obra (Fase 0)

> **Dependência:** Acionado pelo Gestor de Obras (`agents_gestor_obras.md`) na fase de inicialização de um novo projeto.
> **Domínio:** Preparação do canteiro, validação de orçamento, planejamento mestre, engenharia de suprimentos inicial e Lean Construction.

## 🎯 Objetivo
Estruturar as bases inquebráveis da obra ANTES da mobilização das equipes. Evitar gargalos logísticos, atrasos de suprimentos críticos e certificar-se de que o "Orçamento Base" (A Bíblia) é matematicamente executável face aos projetos.

---

## 🧭 Fase 1: Aferição da "Bíblia da Obra" (Orçamento vs. Projetos)
O primeiro passo da engenharia não é construir, é conferir se a conta fecha.
1. **Varredura de Projetos (Status Executivo):** Verificar se todos os projetos (Arquit., Estrutural, MEP) estão marcados como "Liberados para Construção" (Revisão 0/As-Built). Projetos preliminares geram "Alerta de Risco de Retrabalho".
2. **Matriz de Colisão Quantitativa:** Extrair quantitativos reais dos projetos usando a *SKILL QUANT* e confrontar com o **Orçamento de Venda**.
3. **Alerta de Overbudget na Largada:** Se a quantidade extraída do projeto superar a verba do Orçamento Base, emitir imediatamente um alerta de "Estouro de Verba". **Regra:** O Gestor não deve autorizar o início dessa frente sem a aprovação explícita da Diretoria (readequação de projeto ou assunção do prejuízo).

---

## 📅 Fase 2: Planejamento Estratégico (O Motor do Tempo)
Transformar prazos contratuais em um sequenciamento lógico de execução.
1. **Estruturação da EAP (WBS):** Dividir a obra em pacotes (Ex: Serviços Preliminares > Infraestrutura > Superestrutura > Vedações > Instalações > Acabamentos).
2. **CPM e Sequenciamento Lógico:** Todo serviço deve ter dependências claras (Predecessoras/Sucessoras). O cálculo do **Caminho Crítico** (atividades sem folga) é a prioridade máxima.
3. **Ritmo (Linha de Balanço / Takt Time):** Para áreas repetitivas (pavimentos tipo), definir um ritmo unificado. A estrutura não pode andar mais rápido que a alvenaria a ponto de criar um vácuo, nem mais devagar a ponto de parar as frentes de vedação.
4. **Histograma de Mão de Obra:** Gerar a Curva "S" de efetivo humano ao longo dos meses para prever os picos de lotação no canteiro.

---

## 💼 Fase 3: Engenharia de Suprimentos (Cronologia de Compras)
Obrigar a equipe a comprar com antecedência matemática, eliminando o "comprar para apagar incêndio".
1. **Identificação da Curva ABC:** Listar os insumos que representam 80% do custo global e colocá-los sob gestão intensiva.
2. **Cálculo de Lead Time Inverso:**
   - A fórmula: `Data de Aplicação (Cronograma) - Tempo de Logística - Tempo de Fabricação - Tempo de Aprovação - Tempo de Cotação = DATA MÁXIMA DE INÍCIO DA COMPRA`.
   - Gerar um cronograma de contratações. Ex: *Se o elevador será montado no mês 8 e leva 4 meses para fabricar, a cotação deve fechar no mês 3.*
3. **Mapeamento de Terceirizações:** Definir de antemão os pacotes de serviços. Quem faz a fôrma? Quem fornece a madeira? Escopos fechados evitam cobranças em duplicidade.

---

## 🚜 Fase 4: Planejamento de Canteiro e Lean Construction
O canteiro deve ser desenhado como uma fábrica de alta eficiência. O layout deve minimizar a movimentação (os "7 Desperdícios do Lean").
1. **Dimensionamento Normativo (NR-18):** Usar o Histograma (Fase 2) para calcular a área exata necessária para refeitórios, vestiários e banheiros no pico da obra.
2. **Layout Físico (Arranjo):**
   - **Almoxarifado:** Na boca da obra, acesso fácil a caminhões, com controle visual total.
   - **Fluxo de Aço:** Área de descarga contígua à bancada de armação, obrigatoriamente dentro do raio de alcance da grua (se houver).
   - **Fluxo de Argamassa:** Betoneiras/Silos colados à torre de elevação (cremalheira ou guincho). Carrinho de mão não faz curva desnecessária.
3. **Logística Just-in-Time:** Criar o protocolo de agendamento de descargas. Material pesado só desce do caminhão quando a frente de serviço estiver pronta, evitando bi-tributação de movimentação na obra.

---

## 🛡️ Fase 5: Setup Inicial de Qualidade e Segurança
Antes de qualquer trabalhador entrar na obra, os processos de auditoria devem estar prontos.
1. **Plano de Inspeção e Ensaios (PIE):** Definir o cronograma do controle tecnológico (Ex: dias de coleta e rompimento de corpos de prova de concreto aos 7 e 28 dias).
2. **Matriz de Risco (APR):** Elaborar as Análises Preliminares de Risco para os serviços da Fase 1 (Demolição, Tapume, Escavação).
3. **Kits de FVS:** Imprimir/Digitalizar as Fichas de Verificação de Serviço (Gabarito, Fundação) para que a Produção saiba os critérios de tolerância (Qualidade) logo no dia 1.

---

> ⚠️ **Output Esperado do Gestor ao finalizar a Fase 0:** 
> Entregar um dossiê contendo: (A) Alertas de divergência de Orçamento, (B) Cronograma Físico com Caminho Crítico, (C) Cronograma de Suprimentos Críticos, (D) Recomendações de Layout Lean e (E) Pacote inicial de APR e FVS.

*Fim do Módulo de Kickoff.*
