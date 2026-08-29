# 🚀 ROADMAP: Automações da Engenharia 4.0

Este documento mapeia todas as automações sistêmicas que podem ser implementadas no ecossistema para eliminar trabalhos manuais, reduzir erros de digitação e acelerar o fluxo de informações entre o canteiro de obras e o backoffice. 

O objetivo é transformar a construtora em uma verdadeira **Engenharia 4.0**, onde a Inteligência Artificial e scripts de automação fazem o trabalho repetitivo, permitindo que os engenheiros foquem na estratégia.

---

## 🏗️ 1. Planejamento e Avanço Físico
*   **O Trabalho Manual:** O estagiário ou mestre vai para a obra com uma prancheta, anota o percentual de cada ambiente e depois digita tudo em uma planilha de Excel no escritório.
*   **A Automação 4.0:** 
    *   **Coleta via App/Form:** O apontamento é feito no celular (via Google Forms ou AppSheet).
    *   **Processamento Inteligente:** Ao enviar os dados, um webhook aciona um script que atualiza automaticamente o Cronograma Mestre.
    *   **Geração de Relatórios:** A Curva S (Avanço Físico x Financeiro) é recalculada em tempo real e um dashboard é atualizado no PowerBI/Data Studio.

## 💰 2. Gestão de Medições e Pagamentos (A Regra da Trena)
*   **O Trabalho Manual:** Preencher uma planilha de medição na mão, imprimir, assinar, escanear e enviar para o financeiro validar e liberar o pagamento.
*   **A Automação 4.0:**
    *   **OCR de Medições (Visão Computacional):** O engenheiro escaneia a planilha de medição preenchida à mão (ou FVS de medição).
    *   **Auditoria de IA:** A Inteligência Artificial (Visão) lê os números escritos à mão, cruza com o Orçamento Base para checar se o volume cobrado não excede o contratado, e valida se há assinaturas.
    *   **Liberação Automática:** Se aprovado, a IA envia um alerta ao setor Financeiro com o valor exato a ser pago, já com os impostos retidos.

## 🧾 3. Processamento de Notas Fiscais (Suprimentos/Financeiro)
*   **O Trabalho Manual:** Digitar os dados das notas fiscais no sistema ERP, categorizando item a item para o centro de custo correto.
*   **A Automação 4.0:**
    *   **Caixa de Entrada Automatizada:** A NF (PDF ou XML) é enviada para um e-mail ou pasta específica.
    *   **Classificação Automática:** A IA lê a nota, extrai os itens (ex: "Cimento CP-II") e compara com a Tabela de Insumos da obra.
    *   **Lançamento no Fluxo de Caixa:** A IA atribui o Centro de Custo correto e já lança a despesa na planilha de Fluxo de Caixa, pronta para aprovação do Gestor.

## 📦 4. Controle de Estoque e Gatilhos de Compra (Lead Time)
*   **O Trabalho Manual:** Contagem manual periódica de estoque e checagem visual do cronograma para lembrar quando pedir mais material.
*   **A Automação 4.0:**
    *   **Estoque Virtual Integrado:** Cada NF recebida soma no estoque, cada medição de serviço deduz do estoque.
    *   **Gatilho Preditivo:** Um script diário lê o Cronograma (próximas 3 semanas) e verifica a necessidade de material. Se a previsão de uso for maior que o estoque atual, a automação dispara um **Alerta de Compra** (E-mail/WhatsApp) para o setor de Suprimentos, respeitando os *Lead Times* (ex: 20 dias para aço).

## 📋 5. Fichas de Verificação de Serviços (FVS) e Qualidade
*   **O Trabalho Manual:** Arquivar montanhas de papel (FVS) em pastas físicas e atualizar planilhas de controle de qualidade.
*   **A Automação 4.0:**
    *   **Processamento em Lote:** O estagiário escaneia dezenas de FVS de uma vez para uma pasta na nuvem.
    *   **Triagem Inteligente:** A IA identifica o tipo de serviço, reconhece as assinaturas e renomeia o arquivo automaticamente (Ex: `FVS_ALVENARIA_PAV_02.pdf`). Em seguida, move para o DataBook da obra e atualiza o sistema afirmando que o serviço foi validado.

## 👷 6. Controle de Efetivo e Headcount (RDO)
*   **O Trabalho Manual:** Contar quantas pessoas de cada empreiteiro estão na obra e lançar no Relatório Diário de Obra (RDO).
*   **A Automação 4.0:**
    *   **Ponto Digital / Reconhecimento Facial:** Uso de catraca simples ou app de reconhecimento facial na portaria.
    *   **Integração com RDO:** Os dados de entrada populam automaticamente a seção de Efetivo (Headcount) do RDO daquele dia.
    *   **Alerta de Produtividade:** O sistema cruza o número de funcionários com o avanço físico. Se houver 10 pedreiros e nenhum avanço em alvenaria for reportado, um alerta de "Baixa Produtividade" é gerado para o Gestor.

## 🚜 7. Manutenção de Equipamentos (Betoneiras, Elevadores)
*   **O Trabalho Manual:** Controle de horas de uso na prancheta ou esquecimento das manutenções preventivas (gerando quebra no meio da obra).
*   **A Automação 4.0:**
    *   **QR Code e Horímetro Digital:** Cada equipamento ganha um QR Code. O operador bipa ao iniciar e terminar o uso (ou usa um sensor IoT simples).
    *   **Gatilho de Manutenção:** Ao atingir as horas de uso limite (ex: troca de óleo do gerador a cada 200h), o sistema cria automaticamente uma Ordem de Serviço e notifica o mecânico/locadora.

## 🛡️ 8. Gestão de EPIs e Segurança do Trabalho
*   **O Trabalho Manual:** Assinatura em ficha de papel toda vez que um peão retira uma luva ou botina, que se perde ou rasga.
*   **A Automação 4.0:**
    *   **Retirada Digital:** O almoxarife registra a entrega do EPI via tablet com assinatura digital (ou biometria) do colaborador.
    *   **Controle de Validade:** O sistema calcula o tempo de vida útil do EPI (ex: capacete = 5 anos, luva = 15 dias). Quando a luva de um funcionário "vence", a catraca ou o sistema alerta o SESMT que ele precisa de substituição imediata, garantindo 100% de compliance.

## 🔄 9. Rotinas Administrativas (Check-in Lean e DDS)
*   **O Trabalho Manual:** Lembrar de fazer as reuniões e documentar no WhatsApp.
*   **A Automação 4.0:**
    *   **Robô Assistente (WhatsApp):** Um bot manda mensagem todo dia às 07:00 para o Mestre de Obras: *"Mestre, já realizou o DDS hoje? Envie uma foto e o tema"*. 
    *   **Registro Automático:** Quando o Mestre envia a foto e o áudio, a IA transcreve o áudio, salva a foto e anexa tudo no RDO de forma automática.

---

## 📊 10. Dashboard Gerencial Preditivo (A Mente Analítica)
*   **O Trabalho Manual:** Fazer reuniões longas no fim do mês para compilar planilhas e descobrir, tarde demais, que a obra vai atrasar.
*   **A Automação 4.0:**
    *   **Interface em Tempo Real (PowerBI / Web App):** Um painel visual que consolida todas as automações anteriores (Avanço Físico, Financeiro, Estoque).
    *   **Indicadores EVM (Valor Agregado):** O sistema calcula automaticamente o **SPI** (Índice de Prazo) e o **CPI** (Índice de Custo).
    *   **Previsão de Atraso (Machine Learning):** Se a obra avança 2% por semana, mas precisava avançar 3%, a IA projeta a linha de tendência e alerta: *"Projeção de 23 dias de atraso no término da obra"*.
    *   **Planos de Ação Autônomos:** A IA identifica o "Gargalo" (ex: Alvenaria no Caminho Crítico) e sugere soluções instantâneas: *"Sugestão: Contratar +3 pedreiros por 15 dias ou autorizar horas extras aos sábados, custo estimado R$ 4.500, para recuperar a linha de base"*.

---

## 📱 11. Despacho Diário via WhatsApp (Evolution API + Next.js)
*   **O Trabalho Manual:** O mestre de obras precisar correr atrás de cada empreiteiro (gato) no canteiro todo dia de manhã para lembrar o que eles têm que fazer, gerando o famoso "eu não sabia que era pra fazer isso hoje".
*   **A Automação 4.0 (Arquitetura Proprietária):**
    *   **Backend Customizado:** Em vez de depender de ferramentas de terceiros (como n8n ou Make), o ecossistema utiliza uma aplicação construída em **Next.js**.
    *   **Gatilho e Processamento (Cron/Webhook Universal):** O servidor em Next.js possui um *CRON Job* ou *Webhook Universal* que lê o banco de dados do cronograma diariamente às 06:00. Ele filtra as metas do dia por Empreiteiro.
    *   **Disparo (Evolution API):** O backend Next.js dispara um POST direto para a Evolution API, que roteia as mensagens via WhatsApp.
    *   **Exemplo de Mensagem:** *"Bom dia, João! Suas metas para hoje (29/08) na Obra Lumina são: 1. Levantar Alvenaria Pav. 3. 2. Chapiscar Muro dos fundos. Lembre-se de não iniciar o reboco sem a FVS assinada. Bom trabalho!"*

---
*Status do Documento: Roadmap de Inovação traçado. Aguardando priorização técnica.*
