# 🏗️ A11 Sistema de Gestão de Obras (PMO Virtual & Engenharia 5D)

Sistema integrado de inteligência em engenharia civil para gestão de obras residenciais, quantificação física de alta precisão, orçamentação paramétrica com base oficial SINAPI SP, automação de processos e conformidade técnica no canteiro.

---

## 🧭 1. Arquitetura do Sistema

O ecossistema divide-se em **4 Grandes Frentes Integradas**, suportadas por governança contínua e persistência em banco de dados:

```
                  ┌─────────────────────────────────────┐
                  │          PMO VIRTUAL (SSOT)         │
                  │       data/pmo_virtual.sqlite       │
                  └──────────────────┬──────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
┌───────────────────┐       ┌───────────────────┐       ┌───────────────────┐
│ GESTÃO DE OBRAS   │       │ QUANTIFICAÇÃO &   │       │ CHÃO DE FÁBRICA   │
│   (Backoffice)    │       │     ORÇAMENTO     │       │     (25 POPs)     │
└───────────────────┘       └───────────────────┘       └───────────────────┘
         │                           │                           │
         └───────────────────────────┼───────────────────────────┘
                                     ▼
                  ┌─────────────────────────────────────┐
                  │       AUTOMAÇÃO & APRESENTAÇÃO      │
                  │   • Dashboard Web (Next.js)         │
                  │   • Caderno Master Excel (6 abas)   │
                  │   • Motor de Desenhos e AST         │
                  └─────────────────────────────────────┘
```

---

## 📊 2. Caderno Master Excel (`ORCAMENTO_BASE_CONSOLIDADO.xlsx`)

Gerado pelo exportador modular Python (`scripts/motor_quantitativos/exportadores/excel/`) diretamente a partir do SQLite, contendo **fórmulas nativas dinâmicas** do Excel (sem valores estáticos hardcoded) em 6 abas executivas:

| Aba | Nome | Conteúdo e Regras de Cálculo |
| :--- | :--- | :--- |
| **01** | `01_ORCAMENTO_EAP` | Orçamento executivo consolidado com fórmulas dinâmicas de BDI `=ROUND(F*(1+G/100), 2)`, total do item `=ROUND(E*H, 2)` e total geral `=SUM(...)`. |
| **02** | `02_PARAMETRICO_BDI` | Taxas e fórmula paramétrica analítica do BDI conforme **Acórdão 2622/2013 TCU / IBEC**. |
| **03** | `03_COMPOSICOES_CCU` | Decomposição analítica unitária de cada serviço em **Material**, **Mão de Obra** e **Equipamento** com somas dinâmicas `=ROUND(SUM(D:F), 2)`. |
| **04** | `04_CURVA_ABC` | Matriz Pareto 80/20 com ranking de custos, percentuais acumulados e classificação dinâmica (A, B, C) via fórmulas lógicas `=IF(...)`. |
| **05** | `05_MEMORIA_CALCULO` | Rastreabilidade física de cada serviço com equações literais de cubagem geométrica e referência direta às pranchas de projeto. |
| **06** | `06_BOLETIM_MEDICAO` | Planilha de medição física e financeira de obra, cálculo de acumulado `=Anterior+Período`, avanço % e saldo a executar. |

---

## 👷 3. Biblioteca de Procedimentos Operacionais Padrão (POPs)

Localizados em [`/procedimentos/`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/procedimentos/), estes documentos constituem os **Manuais da Franquia** para execução em canteiro, garantia de qualidade (PBQP-H) e segurança (NR-18 / NR-35):

### Módulo 1 — Implantação e Rotina de Canteiro
- **POP 01:** Canteiro Lean (Layout, descargas e fluxos)
- **POP 02:** Rotina Kanban e Daily de Obra
- **POP 03:** Gestão de EPIs, EPCs e Ferramental
- **POP 04:** Controle e Manutenção de Equipamentos

### Módulo 2 — Logística e Suprimentos
- **POP 05:** Solicitação e Compras por Unidade de Controle e Consumo (UCC)
- **POP 06:** Recebimento e Conferência de Cargas e Notas Fiscais
- **POP 07:** Gestão de Almoxarifado e Estoque PEPS (Primeiro que Entra, Primeiro que Sai)

### Módulo 3 — Controle e Inspeção
- **POP 08:** Ficha de Verificação de Serviço (FVS) e Relatório de Não Conformidade (RNC)
- **POP 09:** Medição Física de Campo e Critérios de Pagamento (A Regra da Trena)

### Módulo 4 — Engenharia Executiva
- **POP 10:** Fundações Profundas e Rasas (Estacas, Sapatas, Radiers)
- **POP 11:** Estruturas de Concreto Armado (Fôrmas, Armação e Concretagem)
- **POP 12:** Alvenaria Estrutural e de Vedação
- **POP 13:** Chapisco, Emboço e Revestimentos Argamassados
- **POP 14:** Impermeabilização Rígida e Flexível
- **POP 15:** Instalações Hidrossanitárias (Água Fria, Quente e Esgoto)
- **POP 16:** Instalações Elétricas, Telecom e SPDA

### Módulo 5 — Compliance e Encerramento
- **POP 17:** Onboarding e Gestão de Empreiteiros e Terceirizados
- **POP 18:** As-Built, DataBook e Entrega de Obra

### Módulo 6 — Canteiro Pesado e SESMT
- **POP 19:** Fôrmas, Cimbramento e Escoramento Metálico
- **POP 20:** Andaimes, Linhas de Vida e Trabalho em Altura (NR-35)
- **POP 21:** Locação e Topografia de Alta Precisão (Nível e Laser)
- **POP 22:** Rastreabilidade e Controle Tecnológico do Concreto
- **POP 23:** SESMT, Treinamentos Obrigatórios e DDS

### Módulo 7 — Envoltória e Acabamentos
- **POP 24:** Coberturas, Telhados e Calhas
- **POP 25:** Instalação e Vedação de Esquadrias de Alumínio e PVC

### Guias de Suporte
- [`GUIA_TRACOS_CONCRETO.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/procedimentos/GUIA_TRACOS_CONCRETO.md): Tabela de traços em volume para emergências de canteiro.
- [`MANUAL_BOAS_PRATICAS_EXECUCAO.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/MANUAL_BOAS_PRATICAS_EXECUCAO.md): Checkpoints topográficos e marcos de conferência.

---

## 📁 4. Estrutura Padrão do Dossiê de Obra

Cada obra cadastrada possui sua pasta em `/projetos/[NOME_DA_OBRA]/`, organizada sob o seguinte padrão rigoroso de 7 pastas:

```
/projetos/[NOME_DA_OBRA]/
├── 01_ENGENHARIA_E_PROJETOS/     # Plantas, cortes, memoriais descritivos e RFI_CONTROL.csv
├── 02_ORCAMENTO_BASE_E_CONTRATOS/ # Orçamento Master (.xlsx), CSVs, Curva ABC e propostas
├── 03_PLANEJAMENTO_E_CRONOGRAMA/ # Linha de Balanço (LOB), cronograma mestre e histogramas
├── 04_PRODUCAO_E_AVANCO/         # Relatórios Diários de Obra (RDO), boletins e FVS
├── 05_SUPRIMENTOS_E_FINANCEIRO/  # Notas fiscais, pedidos UCC e fluxo de caixa
├── 06_SST_E_RH/                  # Fichas de EPI, treinamentos NR e controle de efetivo
└── 07_DATABOOK_E_ASBUILT/        # Projetos as-built, termos de garantia e manuais do proprietário
```

---

## 📈 5. Dashboard Web & Apresentação Comercial

Localizado em [`apresentacao_comercial/`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/apresentacao_comercial/), trata-se de uma aplicação **Next.js / React** desenvolvida para apresentações executivas e diretoria:
- Conexão nativa e direta com o banco SQLite (`data/pmo_virtual.sqlite`) via `@/lib/db.ts` (`node:sqlite`).
- Renderização em tempo real de **Curva S (EVM com métricas SPI e CPI)**.
- Visualização de **Linha de Balanço (LOB - Location-Based Scheduling)**.
- Tabela analítica de orçamento com filtros por disciplina e EAP.

---

## ⚙️ 6. Scripts Operacionais e Pipelines

O sistema possui scripts determinísticos em Python para automação de tarefas críticas:

### Leitura de Pranchas e Extração de Carimbos
```bash
# 1. Extrair carimbos e metadados dos PDFs de projeto:
python scripts/extrair_carimbos.py <pasta_pdfs>

# 2. Compilar e sincronizar a Lista de Desenhos oficial no SQLite:
python scripts/gerar_lista_desenhos.py --obra <codigo> --pasta <pasta_pdfs> --db data/pmo_virtual.sqlite
```

### Motor de Quantitativos e Roteador Contratual
```bash
# Roteamento e processamento de prancha PDF confirmada:
python scripts/motor_quantitativos/importadores/roteador.py <prancha.pdf> --obra <codigo> --nome-obra <nome> --revisao <rev> --disciplina <disciplina> --diretorio-obra <pasta> --confirmar-evidencias

# Importação de JSON físico validado:
python scripts/motor_quantitativos/cli.py <json_fisico> --db data/pmo_virtual.sqlite
```

### API de Edição Controlada
```bash
python scripts/api_pmo.py --db data/pmo_virtual.sqlite --api-key <chave>
```
