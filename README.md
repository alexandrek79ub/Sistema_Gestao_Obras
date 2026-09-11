# 🌐 A11 — Sistema Integrado de Gestão de Obras e Engenharia (PMO Virtual)

> **Plataforma Completa de Gestão Técnica, Orçamentação Paramétrica, Produção de Campo e Encerramento (BIM 5D & Engenharia 4.0)**  
> *Base Oficial SINAPI SP 07/2026 | BDI Analítico (27,17% / 15,00%) | 16 Motores Universais Python | Coleta Mobile 4.0*

---

## 🧭 1. Visão Geral da Plataforma

O **A11 Sistema de Gestão de Obras** é um ecossistema operacional de alta precisão projetado para atuar como o **cérebro central e PMO Virtual** de empreendimentos de construção civil. 

O sistema substitui planilhas soltas e controles manuais por uma **arquitetura híbrida e orientada a dados**:
- **Banco de Dados Agnóstico:** Arquivos estruturados em Markdown e CSV com codificação limpa (`UTF-8` e `utf-8-sig`);
- **Trilha de Auditoria Contínua:** Commits do Git atuam como registro inalterável de conformidade (Compliance);
- **Motores Universais em Python:** 16 motores analíticos em `scripts/` que operam via CLI (`--obra` e `--dir`), sem código hardcoded;
- **Chão de Fábrica Conectado:** Aplicativo móvel responsivo ([`/campo`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/apresentacao_comercial/src/app/campo/page.tsx) e PWA offline) conectando Mestre e Encarregados ao escritório;
- **Apresentação Executiva:** Dashboard em Next.js para visualização em tempo real de Curva S (EVM), SPI e medições.

---

## 🏛️ 2. A Arquitetura do Sistema (Os 5 Grandes Pilares)

```
                                  ┌────────────────────────────────┐
                                  │       🤖 MENTE CENTRAL         │
                                  │           agents.md            │
                                  └───────────────┬────────────────┘
                                                  │
         ┌───────────────────┬────────────────────┼───────────────────┬───────────────────┐
         ▼                   ▼                    ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  PILAR 1: CUSTOS │ │ PILAR 2: GESTÃO │ │ PILAR 3: CHÃO   │ │ PILAR 4: MOTORES│ │ PILAR 5: APPS   │
│   E ORÇAMENTO   │ │   BACKOFFICE    │ │    DE FÁBRICA   │ │  UNIVERSAIS CLI │ │    MOBILE 4.0   │
│                 │ │                 │ │                 │ │                 │ │                 │
│ • SINAPI SP     │ │ • Linha de Base │ │ • 25 POPs       │ │ • 16 Scripts    │ │ • Web /campo    │
│ • BDI Analítico │ │ • Fluxo Caixa   │ │ • PBQP-H        │ │ • CSV / XLSX    │ │ • PWA Offline   │
│ • Regra UCC     │ │ • 8 Subcontratos│ │ • Trena e FVS   │ │ • MS Project    │ │ • Bot WhatsApp  │
└─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘
```

### 🧠 Pilar 1: A Mente Central (IA & Governança)
- [`agents.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/agents.md): As instruções centrais de persona, limites éticos, precedência absoluta e protocolos de inicialização da IA.
- [`governanca/INDICE_MESTRE_SKILLS.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/governanca/INDICE_MESTRE_SKILLS.md): O mapa de navegação das Skills e resolução de sobreposições interdisciplinares da EAP (1.1 a 5.1).
- [`governanca/ADENDO_AGENTS_REGRAS_DE_AUTONOMIA.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/governanca/ADENDO_AGENTS_REGRAS_DE_AUTONOMIA.md): Níveis de autonomia operacional (🟢 Verde: Executar / 🟠 Laranja: Propor / 🔴 Vermelho: Travar e Escalar).

### 📐 Pilar 2: Engenharia de Custos (Quantitativo & Orçamento)
- **Base Oficial SINAPI SP 07/2026:** Todo insumo ou serviço possui código CIA unívoco auditável. Busca via `python scripts/consultar_sinapi.py "termo"`.
- **BDI Analítico Segregado:** Custo de Canteiro e Equipe alocados como Custo Direto na EAP 1.0 (Administração Local). Taxa de BDI cobre exclusivamente despesas centrais:
  - **27,17%** para serviços civis e canteiro;
  - **15,00%** para equipamentos nobres e climatização HVAC (Súmula 253 TCU).
- **Regra UCC (Unidade Comercial de Compra):** Proibido comprar quantidade fracionada. Arredondamento estritamente para cima (`math.ceil`) para barras de aço, sacos, telhas, blocos e caixas.

### 📊 Pilar 3: Gestão de Obra e Backoffice (Módulos 01 a 07)
A pasta de cada obra (`projetos/[OBRA]/`) é padronizada rigorosamente em 7 pastas funcionais:
- 📂 `01_ENGENHARIA_E_PROJETOS/` ➔ Pranchas PDF/DWG, Lista de Desenhos e `RFI_CONTROL.csv` (sem respostas presumidas).
- 📂 `02_ORCAMENTO_BASE_E_CONTRATOS/` ➔ Orçamento com 158 itens, Proposta Comercial Turnkey, 8 Contratos de Empreiteiros (`SUB-01` a `SUB-08`), 6 Contratos de Locação (`LOC-01` a `LOC-06`) e Planilha Master de Medição Quinzenal Contínua (com retenção de 5%).
- 📂 `03_PLANEJAMENTO_E_CRONOGRAMA/` ➔ Linha de Base 01, Caminho Crítico (CPM), Curva S financeira, MS Project XML e Dashboard HTML interativo.
- 📂 `04_PRODUCAO_E_AVANCO/` ➔ RDOs diários, Painel multi-abas de produção, 8 FVSs bloqueantes e Acompanhamento de Avanço Físico (Curva S Real vs. Planejada e SPI).
- 📂 `05_SUPRIMENTOS_E_FINANCEIRO/` ➔ Fluxo de Caixa em 3 cenários, Curva de Desembolso, 24 RCs de materiais, 17 REs de máquinas e Procurement Tracker.
- 📂 `06_SST_E_RH/` ➔ Histograma de Mão de Obra, Organograma funcional (PNG/SVG) com Matriz RACI, Painel de Compliance SST com semáforo de ASOs e matriz de NRs (18, 35, 10, 12).
- 📂 `07_DATABOOK_E_ASBUILT/` ➔ Laudos laboratoriais (concreto 28d NBR 5739, estanqueidade 72h NBR 9575 e SPDA NBR 5419), Catálogo As-Built, Matriz de Garantias NBR 15575 e Termos de Recebimento Provisório e Definitivo.

### 👷 Pilar 4: Chão de Fábrica (Biblioteca dos 25 POPs)
A pasta `procedimentos/` contém os manuais inegociáveis de campo:
- **Implantação e Logística:** POP 01 (Canteiro Lean), 02 (Rotina Kanban), 03 (EPIs/Ferramentas), 04 (Equipamentos), 05 (Compras UCC), 06 (Recebimento NF), 07 (Estoque PEPS).
- **Controle de Qualidade e Medição:** POP 08 (FVS/RNC), POP 09 (Medição Física / Regra da Trena).
- **Engenharia de Execução:** POP 10 (Fundações), 11 (Concretagem), 12 (Alvenaria), 13 (Revestimentos), 14 (Impermeabilização), 15 (Hidráulica), 16 (Elétrica).
- **Compliance e Closeout:** POP 17 (Onboarding Terceiros), POP 18 (DataBook e As-Built).
- **Canteiro Pesado e SESMT:** POP 19 (Fôrmas e Cimbramento), POP 20 (Andaimes Fachadeiros), POP 21 (Topografia a Laser), POP 22 (Controle Tecnológico de Concreto), POP 23 (SESMT e Treinamentos).
- **Acabamentos Externos:** POP 24 (Cobertura Metálica/Telhados), POP 25 (Esquadrias de Alumínio e Vidros).

### 🤖 Pilar 5: Engenharia 4.0 e Coleta Digital Mobile
- **App de Campo Responsivo ([`/campo`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/apresentacao_comercial/src/app/campo/page.tsx)):** Interface escura de alto contraste com contadores rápidos de efetivo, botões de clima, seleção de serviços EAP, canvas de assinatura digital no dedo para FVS e gerador de mensagem instantânea de WhatsApp.
- **PWA Standalone ([`campo.html`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/apresentacao_comercial/public/campo.html)):** Funciona 100% offline em qualquer smartphone salvando os apontamentos em LocalStorage.
- **Ingestão Inteligente via WhatsApp:** Mensagens enviadas pelo Mestre no WhatsApp são lidas e interpretadas pelo motor Python `processar_coleta_campo.py`.

---

## ⚙️ 3. A Suíte dos 16 Motores Universais em Python (`scripts/`)

Todos os motores implementam interface de linha de comando (`argparse`) com parâmetros `--obra [NOME]` e `--dir [CAMINHO]`, com isolamento total anti-contaminação:

| # | Script | Função Principal | Saídas Geradas |
| :---: | :--- | :--- | :--- |
| **01** | `precificar_obra.py` | Motor Universal de Orçamento Base Turnkey | `ORCAMENTO_BASE.csv/xlsx`, Curvas ABC |
| **02** | `gerar_plano_centros_custo.py` | Amarração EAP x Centros de Custo CC-100 a CC-900 | `PLANO_DE_CONTAS.md`, estrutura JSON |
| **03** | `gerar_cronograma.py` | Cronograma Físico-Financeiro, Curva S e CPM | `CRONOGRAMA.xlsx`, XML MS Project, HTML |
| **04** | `gerar_cronograma_suprimentos.py` | Matriz de Compras e Lead Times (D-30/D-15/D-7/D-0) | RCs de materiais e REs de locações |
| **05** | `gerar_tracker_suprimentos.py` | Pipeline de Procurement com semáforos de entrega | `TRACKER_SUPRIMENTOS.xlsx/md` |
| **06** | `gerar_fluxo_caixa.py` | Projeção financeira em 3 cenários e Capital de Giro | `FLUXO_DE_CAIXA.xlsx/csv/md` |
| **07** | `gerar_contratos_empreiteiros.py` | Minutas contratuais de 8 pacotes (SUB-01 a SUB-08) | `CONTRATOS_EMPREITEIROS/` com cadernos |
| **08** | `gerar_contratos_locacao.py` | Contratos de locação de máquinas (LOC-01 a LOC-06) | Minutas e planilha de controle de frotas |
| **09** | `gerar_planilha_medicao.py` | Planilha Master evolutiva de 12 quinzenas | `PLANILHA_MEDICAO_QUINZENAL.xlsx` (ret. 5%) |
| **10** | `gerar_dossie_contratacao.py` | Dossiê de contratação e histogramas de recursos | Histogramas de MO (HH) e Equipamentos |
| **11** | `gerar_rdo.py` | Sistema diário de RDO e painel de produção | `PAINEL_RDOS_OBRA.xlsx` e `RDOS/RDO-XXX.md` |
| **12** | `gerar_fvs_bloqueantes.py` | Caderno de 8 FVSs com bloqueio de medições | `CADERNO_FVS_BLOQUEANTES.md` e planilha |
| **13** | `gerar_tracker_avanco_fisico.py` | Acompanhamento de avanço físico e SPI (EVM) | `ACOMPANHAMENTO_AVANCO_FISICO.xlsx/md` |
| **14** | `gerar_compliance_sst.py` | Painel SST, controle de ASOs e matriz de NRs | `PAINEL_COMPLIANCE_SST.xlsx/md` |
| **16** | `processar_coleta_campo.py` | Ingestão de apontamentos via Mobile e WhatsApp | Atualização atômica de RDOs e FVSs |

#### 🛠️ Motores Auxiliares e Utilitários:
- `consultar_sinapi.py` ➔ Busca instantânea na base SINAPI SP 07/2026 por termo ou código (`python scripts/consultar_sinapi.py "termo"`);
- `gerar_organograma_visual.py` ➔ Geração do organograma funcional em vetor SVG nativo e imagem PNG alta resolução em `06_SST_E_RH/`;
- `gerar_lista_desenhos.py` ➔ Catalogação automática de pranchas PDF e geração de `LISTA_DE_DESENHOS.csv/md` em `01_ENGENHARIA_E_PROJETOS/`;
- `gerar_certificado_auditoria.py` ➔ Auditoria estrutural e QA dos 6 checklists em Markdown puro em `02_ORCAMENTO_BASE_E_CONTRATOS/`.

---

## 🚀 4. Guia Rápido: Como Navegar no Ecossistema

Dependendo do seu perfil, utilize a porta de entrada adequada:

- 👷 **Sou Engenheiro de Obra e quero criar/rodar uma obra nova:**
  ➔ Siga o checklist do [`projetos/_TEMPLATE_OBRA_NOVA/README_COMO_CRIAR_NOVA_OBRA.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/projetos/_TEMPLATE_OBRA_NOVA/README_COMO_CRIAR_NOVA_OBRA.md).
- 💻 **Sou Desenvolvedor e vou criar scripts ou mexer no Next.js:**
  ➔ Siga rigorosamente o [`MANUAL_BOAS_PRATICAS_CODIFICACAO.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/MANUAL_BOAS_PRATICAS_CODIFICACAO.md).
- 🤖 **Instruções da IA do PMO Virtual:**
  ➔ Consulte as regras de precedência e autonomia em [`agents.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/agents.md).
- 📱 **Acessar o Aplicativo de Coleta Móvel de Campo:**
  ➔ Inicie a aplicação comercial em `apresentacao_comercial/` e acesse a rota [`/campo`](http://localhost:3000/campo) ou abra diretamente no celular o arquivo [`apresentacao_comercial/public/campo.html`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/apresentacao_comercial/public/campo.html).

---

## ⛔ 5. Regras Inegociáveis do Ecossistema (Red Flags)

1. **Tolerância Zero para Estimativas ou Chutes:** Toda dimensão e cota deve vir 100% de prancha aprovada ou confirmação do usuário. Havendo dúvida, é obrigatório parar e perguntar.
2. **A Regra da Trena (POP 09):** Nenhuma medição de empreiteiro é paga por avanço presumido; exige conferência física in-loco.
3. **Portão de Qualidade FVS Bloqueante:** Nenhuma medição quinzenal de empreiteiro pode ser liberada pelo Financeiro se a FVS correspondente não estiver formalmente assinada pelo Engenheiro Residente.
4. **Segregação Rigorosa: EAP é Serviço, UCC é Compra:** Na EAP entram pacotes de serviços; na lista UCC explodem-se 100% das miudezas e consumíveis com arredondamento para cima (`math.ceil`).
5. **Motores Universais Multi-Obras:** Proibido hardcoding de projetos em scripts. Dados residem exclusivamente dentro da pasta da respectiva obra (`projetos/[OBRA]/`).

---
*Ecossistema A11 — Inteligência Artificial, Engenharia de Custos e Gestão de Obras Integradas.*
