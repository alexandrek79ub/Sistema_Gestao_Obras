# 📋 SKILL: Gestão de RFI (Request for Information)

> **Propósito:** Gerenciar o ciclo de vida completo de uma RFI — da abertura formal até a incorporação da resposta ao quantitativo. Toda informação faltante de projeto que bloqueia levantamento ou execução DEVE ser registrada como RFI antes de qualquer estimativa.
> **Ativar quando:** "falta informação no desenho", "precisa de RFI", "emitir RFI", "resposta do projetista", "acompanhar RFIs abertas"

---

## 1. Estrutura de uma RFI

Uma RFI válida contém obrigatoriamente:

| Campo | Descrição | Exemplo |
|---|---|---|
| **Número** | `RFI-[OBRA]-[NNN]` (sequencial) | `RFI-TMULT-001` |
| **Prancha de referência** | Código da prancha onde a dúvida está | `ARQ-3.DES-A100 Rev 01` |
| **Pergunta objetiva** | Dúvida específica e mensurável | `"Qual a espessura da laje no vão V3 (entre eixos 5 e 6)?"` |
| **Motivo (bloqueio)** | Quais itens do quantitativo estão bloqueados | `"Itens: laje alveolar vão V3, carga de pilar P-12"` |
| **Data de abertura** | `DD/MM/AAAA` | `09/09/2026` |
| **Prazo de resposta** | Em dias úteis | `5 dias úteis` |
| **Status** | Ver Seção 3 | `ABERTA` |

### 1.1 O que NÃO é uma pergunta válida de RFI

| ❌ Pergunta vaga | ✅ Pergunta válida |
|---|---|
| "Falta a cota desta laje" | "Qual a espessura da laje nervurada no vão V3 (eixos 5-6, bloco B)?" |
| "Precisa de mais informação" | "O memorial de acabamentos não especifica o tipo de revestimento do corredor (CIA T-005-COR). Qual o revestimento de piso e parede?" |
| "O projeto está incompleto" | "A prancha ARQ-A100 não indica a cota do peitoril da janela JA02 (quartos). Qual a altura do peitoril?" |

---

## 2. Arquivo de Controle de RFIs

Cada obra DEVE ter um arquivo `RFI_CONTROL.csv` em:
```
/projetos/[NOME_OBRA]/01_ENGENHARIA_E_PROJETOS/RFI_CONTROL.csv
```

### Schema do `RFI_CONTROL.csv`

| Coluna | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `ID` | string | ✅ | `RFI-[OBRA]-[NNN]` |
| `DATA_ABERTURA` | string | ✅ | `YYYY-MM-DD` |
| `PRANCHA` | string | ✅ | Código da prancha de referência |
| `PERGUNTA` | string | ✅ | Pergunta objetiva e mensurável |
| `CIA_BLOQUEADOS` | string | ✅ | Códigos de CIA separados por vírgula |
| `ITENS_BLOQUEADOS` | string | ✅ | Descrição dos itens bloqueados |
| `PRAZO_DIAS_UTEIS` | number | ✅ | Prazo esperado de resposta em dias úteis |
| `STATUS` | string | ✅ | `ABERTA`, `AGUARDANDO`, `RESPONDIDA`, `INCORPORADA`, `CANCELADA` |
| `DATA_RESPOSTA` | string | ❌ | `YYYY-MM-DD` — quando foi respondida |
| `RESPOSTA` | string | ❌ | Texto ou referência à prancha revisada |
| `REVISAO_PRANCHA` | string | ❌ | Ex: `ARQ-A100 Rev 02` — nova prancha emitida |
| `DATA_INCORPORACAO` | string | ❌ | `YYYY-MM-DD` — quando o item voltou ao quantitativo |

---

## 3. Fluxo de Vida de uma RFI

```
[ABERTA] → Emitida pela IA ou pelo consultora ao detectar falta de informação
     ↓
[AGUARDANDO] → Enviada formalmente ao projetista / cliente
     ↓
     ├── Respondida no prazo? → [RESPONDIDA] → Incorporar ao quantitativo → [INCORPORADA]
     │
     └── Sem resposta no prazo? → Escalonamento (ver Seção 4)
```

### Regra de atualização de STATUS no CSV:
- Ao abrir: `ABERTA`
- Ao enviar ao projetista: `AGUARDANDO`
- Ao receber resposta: `RESPONDIDA`
- Após relançar o cálculo do item: `INCORPORADA`
- Se a dúvida foi sanada por outra fonte (outra prancha): `CANCELADA`

---

## 4. Escalonamento por Prazo Vencido

| Prazo desde abertura | Ação de escalonamento |
|---|---|
| **5 dias úteis** sem resposta | Enviar lembrete formal ao projetista (registrar no log da RFI) |
| **10 dias úteis** sem resposta | Comunicar ao cliente via `SKILL_GESTAO_15_COMUNICACAO_CLIENTE.md` — nota formal de impacto no cronograma/orçamento |
| **15 dias úteis** sem resposta | Registrar como risco no `SKILL_GESTAO_13_MATRIZ_DE_RISCO.md` — categoria: Projeto |

---

## 5. Integração com o Quantitativo

### Quando uma RFI é aberta:
1. O item no CSV de quantitativo recebe `STATUS = "PENDENTE_RFI"` e `QUANTIDADE = 0`.
2. A memória de cálculo recebe a observação padrão:
```
> ⚠️ OBSERVAÇÃO DE AUDITORIA — ITEM NÃO LEVANTADO POR FALTA DE INFORMAÇÃO NO DESENHO:
> - RFI nº: RFI-[OBRA]-[NNN]
> - Prancha: [código]
> - Motivo: [descrição objetiva da informação faltante]
> - Ação: Aguardando resposta do projetista.
```

### Quando a RFI é respondida e incorporada:
1. Atualizar a prancha de referência no levantamento.
2. Relançar o cálculo do item bloqueado (retornar ao submódulo de skill correspondente).
3. Atualizar o CSV de quantitativo: `STATUS = "LEVANTADO"` e `QUANTIDADE = [valor calculado]`.
4. Atualizar o `RFI_CONTROL.csv`: `STATUS = "INCORPORADA"` + `DATA_INCORPORACAO`.
5. **Não alterar a memória de cálculo original** — apenas adicionar nota de encerramento:
```
> ✅ RFI-[OBRA]-[NNN] INCORPORADA em [DD/MM/AAAA]: [resumo da resposta]
```

---

## 6. Dashboard de RFIs Abertas

O agente DEVE gerar um relatório de RFIs ao iniciar qualquer sessão de obra que tenha `RFI_CONTROL.csv`:

```markdown
## 📋 Status de RFIs — [Nome da Obra] — [Data]

| RFI | Prancha | Dias em aberto | Status | CIA Bloqueados |
|---|---|---|---|---|
| RFI-TMULT-001 | ARQ-A100 | **12 dias** ⚠️ | AGUARDANDO | T-001-SAL, T-001-QRT |
| RFI-TMULT-002 | EST-E200 | 3 dias | ABERTA | T-001-COZ |

⚠️ **1 RFI acima do prazo de escalonamento (10 dias úteis) — ação requerida.**
```

> **Regra:** RFIs abertas há mais de 10 dias úteis sem resposta DEVEM ser reportadas ao cliente na próxima comunicação — nunca silenciosamente.
