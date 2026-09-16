# 🌐 MANUAL DO ECOSSISTEMA: A11 Sistema de Gestão de Obras Residenciais

Bem-vindo ao **PMO Virtual de Alta Precisão**. Este documento é o mapa de navegação obrigatório para Gestores, Engenheiros, Orçamentistas e para os Próprios Agentes de Inteligência Artificial que operam este sistema.

Aqui você entende **O QUE** nós temos, **PARA QUE** serve e **COMO** ligar os motores para o "Take-off" (Início) de uma obra.

---

## 🧭 1. A ARQUITETURA DO SISTEMA (O que nós temos)

O nosso ecossistema está dividido em **5 Grandes Pilares**. A IA (ou o humano) nunca deve tentar resolver um problema sem acionar o arquivo correto de sua respectiva área.

### 🧠 Pilar 1: A Mente Central (Roteamento)
- `agents.md`: O arquivo mestre que dá a persona para a Inteligência Artificial. Ele sabe para onde direcionar a dúvida do usuário (se é para custos ou se é para campo).
- `skills/gestao/agents_gestor_obras.md`: O "Cérebro" do Gerente de Projetos. Ele puxa as skills de gestão e obriga a comparação de tudo com a Bíblia da Obra (Orçamento).
- `governanca/INDICE_MESTRE_SKILLS.md`: O mapa de consulta completo que resolve sobreposições de Skills e regras de autonomia.

### 📐 Pilar 2: Engenharia de Custos (Quantitativo e Orçamento)
*Regra: o quantitativo preserva a quantidade física líquida nominal; composições CCU, BDI, perdas e UCC pertencem ao orçamento e compras.*
- `SKILL_QUANTIFICACAO_MASTER.md`: A regra mãe de cálculo. Define os modelos de tabela e as regras matemáticas universais.
- `SKILL_QUANT_01_FUNDACOES.md`: Estacas, Sapatas, Radiers.
- `SKILL_QUANT_02_ESTRUTURA.md`: Pilares, Lajes, Aço (CA-50/60) e Fôrmas.
- `SKILL_QUANT_03_ARQUITETURA.md`: Alvenaria, Reboco, Pisos, Gesso, Pintura.
- `SKILL_QUANT_04_ELETRICA.md` & `SKILL_QUANT_05_HIDRAULICA.md`: Módulos de instalações.
- `SKILL_QUANTIFICACAO_COMPOSICAO_PRECO.md`, `SKILL_QUANTIFICACAO_PEDIDO_DE_COMPRA.md` e `SKILL_QUANTIFICACAO_CONCILIACAO_3_PONTAS.md`: composição, compras e conciliação.
- `SKILL_QUANTIFICACAO_AUDITORIA_E_CORRECAO.md`: Filtro anti-erro e emissão do certificado de auditoria.

### 📊 Pilar 3: A Gestão de Obra (O Backoffice)
*Onde a IA cruza dinheiro, prazo e segurança.*
- `SKILL_GESTAO_00_KICKOFF.md`: A Implantação inicial, matriz de riscos e EAP.
- `SKILL_GESTAO_01_PLANEJAMENTO.md`: Controle da Curva S e Caminho Crítico.
- `SKILL_GESTAO_02_PRODUCAO.md`: Produtividade diária e Relatórios (RDO).
- `SKILL_GESTAO_03_ADMINISTRATIVO.md`: Pedidos, Medições e Fluxo de Caixa.
- `SKILL_GESTAO_04_SEGURANCA.md`: Normas da NR-18.
- `SKILL_GESTAO_05_QUALIDADE.md`: Controle de PBQP-H e rastreabilidade.
- `SKILL_GESTAO_06_RELATORIOS.md`: Dashboard, cruzamento EVM (SPI/CPI) e Planos de Ação autônomos.
- `SKILL_GESTAO_07` a `17`: Gestão avançada, abrangendo Ciência de Dados, Fluxo de Caixa, Contratos, Riscos, Encerramento e Reprogramação (consulte o Índice Mestre).

### 👷 Pilar 4: O Chão de Fábrica (Biblioteca de POPs)
*Os manuais inegociáveis para não ocorrer patologias nem desperdício logístico. Estão na pasta `procedimentos/`.*
- **Módulo 1 (Implantação):** POP 01 (Canteiro Lean), 02 (Rotina Kanban), 03 (EPIs/Ferramentas), 04 (Equipamentos).
- **Módulo 2 (Logística):** POP 05 (Compras UCC), 06 (Recebimento NF), 07 (Estoque PEPS).
- **Módulo 3 (Controle):** POP 08 (FVS/RNC), 09 (Medição/Trena).
- **Módulo 4 (Engenharia):** POP 10 (Fundação), 11 (Concreto), 12 (Alvenaria), 13 (Revestimento), 14 (Impermeabilização), 15 (Instalações Hidráulicas), 16 (Instalações Elétricas).
- **Módulo 5 (Compliance e Closeout):** POP 17 (Onboarding Terceiros), POP 18 (As-Built e DataBook).
- **Módulo 6 (Canteiro Pesado e SESMT):** POP 19 (Fôrmas e Cimbramento), POP 20 (Andaimes e NR-35), POP 21 (Topografia a Laser), POP 22 (Controle de Concreto), POP 23 (SESMT e Treinamentos).
- **Módulo 7 (Acabamentos Externos):** POP 24 (Cobertura), POP 25 (Esquadrias).
- *Extra:* `GUIA_TRACOS_CONCRETO.md` (Emergências no canteiro) e `MANUAL_BOAS_PRATICAS_EXECUCAO.md` (Mapa de fases com checkpoints topográficos).

### 🤖 Pilar 5: Automação e Engenharia 4.0
*Onde a tecnologia potencializa a governança corporativa.*
- **SQLite como ÚNICA Fonte da Verdade (SSOT):** O banco `data/pmo_virtual.sqlite` centraliza quantitativos (`itens_quantitativo`), orçamentos (`itens_orcamento`), revisões e obras. Nunca se edita planilhas ou markdowns diretamente.
- **Exportador Modular Excel com Fórmulas (`ORCAMENTO_BASE_CONSOLIDADO.xlsx`):** Subpacote Python modular (`scripts/motor_quantitativos/exportadores/excel/`) que exporta um Master Book corporativo com 6 abas integradas contendo fórmulas nativas do Excel (`ROUND`, `SUM`, `IF`):
  1. `01_ORCAMENTO_EAP`: EAP e orçamento com fórmulas de BDI e totais dinâmicos;
  2. `02_PARAMETRICO_BDI`: Taxas e fórmula paramétrica analítica do BDI (Acórdão 2622/2013 TCU);
  3. `03_COMPOSICOES_CCU`: Decomposição unitária analítica (Material, Mão de Obra e Equipamento);
  4. `04_CURVA_ABC`: Matriz Pareto 80/20 com ranking dinâmico e classificação automática;
  5. `05_MEMORIA_CALCULO`: Cubagem geométrica com equações literais e pranchas de projeto;
  6. `06_BOLETIM_MEDICAO`: Planilha de medição física e financeira de obra com saldos automáticos.
- **Artefatos Derivados de Exportação:** CSVs (`ORCAMENTO_BASE_CONSOLIDADO.csv`, `QUANTITATIVO_MESTRE.csv`) e memórias em Markdown (`MEMORIA_CALCULO_[DISC].md`) gerados automaticamente pelo motor para portabilidade, transparência e consumo externo.
- **Dashboard PMO (Next.js):** Front-end em React/Next.js conectado **diretamente ao SQLite** via `@/lib/db.ts` (`node:sqlite`), garantindo latência zero para Curva S (EVM com SPI/CPI), Linha de Balanço e Orçamento.
- **Roadmap 4.0:** Automação de despachos aos empreiteiros via WhatsApp (**Evolution API**) e leitura automatizada de pranchas PDF.

---

## 🚀 2. O TAKE-OFF DA OBRA (Guia Passo a Passo)

Acabou de assinar um contrato novo? É assim que você utiliza o sistema para iniciar a obra com controle absoluto:

### Passo 1: Orçamento Cego (O Nascimento da Bíblia)
1. Acione o **Gestor/Orçamentista** e forneça os projetos.
2. A IA lê a `SKILL_QUANTIFICACAO_MASTER.md` + Módulos 01 a 03.
3. Extrai as cotas das pranchas e monta o JSON estruturado com equações matemáticas puras (sem calcular de cabeça).
4. O motor Python (`cli.py`) executa os cálculos na CPU via AST segura, persiste no SQLite (`data/pmo_virtual.sqlite`) e compila as exportações derivadas (Excel com fórmulas, CSVs e Markdowns).
5. O Engenheiro vincula as composições de custo unitário (CCU) via SINAPI SP (`apoio/sinapi_sp/`) ou cotações com BDI paramétrico.

### Passo 2: O Kickoff e o "Dossiê de Take-off" (Fase Zero)
Antes de qualquer tijolo ser assentado, o Gestor/PMO DEVE organizar, travar (baseline) e gravar todos os documentos fundamentais da obra no sistema.
1. **Acione a `SKILL_GESTAO_00_KICKOFF.md`.**
2. **Monte o Dossiê de Take-Off:** Toda nova obra DEVE ser montada na pasta `/projetos/OBRA/`, seguindo estritamente a árvore abaixo. A IA buscará e atualizará os dados com persistência oficial no SQLite e artefatos derivados nas pastas:
   - 📂 `01_ENGENHARIA_E_PROJETOS/` -> Plantas, Cortes e Projetos Complementares.
   - 📂 `02_ORCAMENTO_BASE_E_CONTRATOS/` -> Master Book Excel com fórmulas (`ORCAMENTO_BASE_CONSOLIDADO.xlsx`), CSVs consolidados, Propostas e Curva ABC.
   - 📂 `03_PLANEJAMENTO_E_CRONOGRAMA/` -> Cronograma Mestre, TEMPLATE_LINHA_DE_BALANCO.csv (Location-Based Scheduling) e Histograma.
   - 📂 `04_PRODUCAO_E_AVANCO/` -> Relatório Diário de Obra (TEMPLATE_RDO.md), Medições e FVS (Qualidade).
   - 📂 `05_SUPRIMENTOS_E_FINANCEIRO/` -> Notas Fiscais (NFs), Fluxo de Caixa e Controle de Estoque.
   - 📂 `06_SST_E_RH/` -> Treinamentos, Fichas de EPI e Controle de Efetivo.
   - 📂 `07_DATABOOK_E_ASBUILT/` -> Projetos Executados (As-Built) e Manuais para entrega.
3. **Sincronização Visual:** Os dados gravados no SQLite refletem instantaneamente no Dashboard Next.js para visualização da Diretoria e Engenharia.
4. **Logística Inicial:** Cruze a Tabela de Insumos com as necessidades físicas usando o **POP 01 (Canteiro Lean)** para desenhar o layout de descarga do material pesado (aço, blocos, areia).

### Passo 3: Compras Iniciais (O Motor Liga)
1. Acione o setor Administrativo (`SKILL_GESTAO_03_ADMINISTRATIVO.md`).
2. Dispare os pedidos utilizando as regras do **POP 05 (Solicitação de Compras)**, respeitando o Lead Time (20 dias para estrutura, 7 dias para areia).
3. Entregue o **POP 06 (Recebimento)** na mão do porteiro/almoxarife para ele saber como barrar carga errada.

### Passo 4: Execução Diária (Produção e Planejamento)
1. Comece o dia com o DDS e o Check-in Lean (**POP 02** e **POP 03**).
2. Obras com Terceirizados exigem integração prévia e checagem documental rigorosa (**POP 17**).
3. Libere as concretagens, alvenarias e instalações exigindo do mestre o rigor técnico contido nos **POPs 10 a 16**.
4. Na sexta-feira, o Engenheiro pega a trena e vai para a obra conferir o serviço antes de pagar o empreiteiro, conforme **POP 09 (Medição)**, e checa se a FVS do serviço está assinada (**POP 08**).

### Passo 5: Encerramento e Entrega (Closeout)
1. Concluída a execução, a obra não deve ser desmobilizada antes do "DataBook".
2. **Trava Financeira (As-Built):** Acione o setor Financeiro para reter a última medição dos empreiteiros de instalações até que eles entreguem o As-Built (Projeto como Construído) conforme o **POP 18**.
3. Realize a Limpeza Fina e a entrega do Manual do Proprietário para blindar a construtora contra acionamento indevido de garantias futuras.

---

## ⛔ 3. REGRAS INEGOCIÁVEIS (Red Flags)

Se alguma destas regras for quebrada, a Inteligência Artificial (ou o Gestor) DEVE travar o processo e emitir um ALERTA:

1. **SQLITE É A ÚNICA FONTE DA VERDADE (SSOT):** É expressamente PROIBIDO editar arquivos `.csv`, `.xlsx` ou `.md` manualmente como repositório de dados. Todas as alterações devem ocorrer no SQLite.
2. **PROIBIDO PAGAR POR AVANÇO PRESUMIDO:** Só se paga medição após verificação com trena *in loco* (POP 09).
3. **PROIBIDO COMPRAR "QUEBRADO":** A Engenharia calcula "13,4 metros", o Compras obrigatoriamente compra barra fechada ("18 metros"). (Regra UCC - POP 05).
4. **A REGRA DA TRENA (POP 09):** Nenhuma Nota Fiscal de serviço de empreiteiro pode ser paga sem Medição Física In-Loco. Proibido pagar "porcentagem de avanço" no olho.
5. **O ORÇAMENTO É A LEI SUPREMA:** Nenhuma contratação pode exceder o valor do Orçamento Base. Se estourar, tem que gerar Alerta de "Estouro de Verba" (`SKILL_GESTAO_03`).
6. **NÃO HÁ RESUMO DE SKILL:** A Inteligência Artificial (Agente) nunca deve agir baseada em um resumo. Ela DEVE ler os arquivos `md` na íntegra para dar uma resposta.

---
*Gerado por: Antigravity AI — Engenheiro Chefe.*
