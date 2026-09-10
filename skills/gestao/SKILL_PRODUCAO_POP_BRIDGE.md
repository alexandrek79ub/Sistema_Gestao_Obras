# 🔗 SKILL: Bridge Gestão de Produção → POPs de Execução

> **Propósito:** Arquivo-roteador leve. Quando a Frente de Produção (`SKILL_GESTAO_02_PRODUCAO.md`) for acionada para um serviço específico, consultar obrigatoriamente o POP correspondente antes de orientar a execução.
> **Regra:** O Gestor de Obras não libera frente de serviço sem verificar se o POP da atividade foi lido e aplicado.

---

## 🔀 Tabela de Roteamento: Serviço → POP

| Serviço / Fase | POP a Acionar | Quando acionar |
|---|---|---|
| **Implantação do canteiro** | `POP_01_CANTEIRO_LEAN.md` | Antes da mobilização de qualquer equipe |
| **Rotina diária / Kanban de obra** | `POP_02_ROTINA_KANBAN.md` | Todo dia útil de obra |
| **Controle de EPIs e ferramentas** | `POP_03_EPI_FERRAMENTAS.md` | Onboarding de trabalhador e troca de EPI |
| **Operação de equipamentos** | `POP_04_EQUIPAMENTOS.md` | Antes de operar guincho, betoneira, grua |
| **Pedido de compra / suprimentos** | `POP_05_COMPRAS_UCC.md` | Qualquer solicitação de material novo |
| **Recebimento de NF e material** | `POP_06_RECEBIMENTO_NF.md` | Chegada de caminhão / entrega de material |
| **Controle de estoque (almoxarifado)** | `POP_07_ESTOQUE_PEPS.md` | Entrada e saída de material do almoxarifado |
| **Inspeção de serviço executado / FVS** | `POP_08_FVS_RNC.md` | Após conclusão de qualquer serviço inspecionável |
| **Medição física de serviço (Regra da Trena)** | `POP_09_MEDICAO_TRENA.md` | Medição de empreiteiro ou avanço físico do RDO |
| **Fundação (escavação, estacas, brocas, sapatas)** | `POP_10_FUNDACAO.md` | Início da fase de infraestrutura |
| **Concretagem (lançamento e cura)** | `POP_11_CONCRETO.md` | Antes de qualquer concretagem de estrutura |
| **Alvenaria de vedação / estrutural** | `POP_12_ALVENARIA.md` | Início de elevação de paredes |
| **Revestimentos (chapisco, emboço, gesso, cerâmica)** | `POP_13_REVESTIMENTO.md` | Início de fase de acabamentos internos |
| **Impermeabilização** | `POP_14_IMPERMEABILIZACAO.md` | Antes de qualquer serviço de impermeabilização |
| **Instalações hidráulicas** | `POP_15_HIDRAULICA.md` | Execução de tubulações de água e esgoto |
| **Instalações elétricas** | `POP_16_ELETRICA.md` | Execução de eletrodutos, fiação e QDC |
| **Onboarding de terceiro / empreiteiro novo** | `POP_17_ONBOARDING_TERCEIROS.md` | Antes de qualquer empresa terceira entrar na obra |
| **As-Built e DataBook final** | `POP_18_ASBUILT_DATABOOK.md` | Fase de encerramento e entrega ao cliente |
| **Fôrmas e cimbramento** | `POP_19_FORMAS.md` | Antes de montar fôrmas para lajes/pilares/vigas |
| **Trabalho em altura (qualquer serviço)** | `POP_20_ANDAIMES_NR35.md` | Todo serviço executado acima de 2,00m |
| **Topografia / verificação de gabarito** | `POP_21_TOPOGRAFIA.md` | Antes de iniciar fase, marco ou controle de nível |
| **Controle tecnológico de concreto** | `POP_22_CONTROLE_CONCRETO.md` | Coleta de CPs aos 7 e 28 dias |
| **SESMT, DDS e treinamentos obrigatórios** | `POP_23_SESMT_TREINAMENTOS.md` | Início de obra e fases de alto risco |
| **Cobertura / telhado** | `POP_24_COBERTURA.md` | Antes de iniciar montagem de telhado |
| **Esquadrias (portas, janelas, caixilhos)** | `POP_25_ESQUADRIAS.md` | Antes de instalar esquadrias externas e internas |

---

## ⚠️ Regras de Uso

1. **Não libere frente sem o POP lido.** O Gestor de Produção deve confirmar que o encarregado ou mestre de obras recebeu as diretrizes do POP antes de iniciar o serviço.
2. **Trabalho em altura (NR-35) sempre aciona `POP_20`**, independentemente do serviço principal — é uma camada de segurança adicional sobre qualquer outro POP.
3. **Se o POP do serviço não existir na lista acima,** o Gestor deve parar e criar um checklist mínimo baseado na `SKILL_GESTAO_04_SEGURANCA.md` e na `SKILL_GESTAO_05_QUALIDADE.md`, e sugerir que o POP seja criado como item de melhoria.
4. **O roteamento não substitui a leitura do POP.** Este arquivo aponta qual POP carregar; o conteúdo técnico está integralmente nos arquivos de POP em `/procedimentos/`.

---

## 🔗 Referências

- **Frente de Produção:** [`SKILL_GESTAO_02_PRODUCAO.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/gestao/SKILL_GESTAO_02_PRODUCAO.md)
- **Segurança (SST):** [`SKILL_GESTAO_04_SEGURANCA.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/gestao/SKILL_GESTAO_04_SEGURANCA.md)
- **Qualidade (FVS):** [`SKILL_GESTAO_05_QUALIDADE.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/gestao/SKILL_GESTAO_05_QUALIDADE.md)
- **Pasta de POPs:** [`/procedimentos/`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/procedimentos/)
