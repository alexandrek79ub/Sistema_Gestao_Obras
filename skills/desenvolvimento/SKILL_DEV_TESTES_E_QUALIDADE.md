# 🧪 SKILL: Testes e Qualidade de Código (Dashboard Next.js)

> **Frente:** Desenvolvimento ([`SKILL_DEV_SENIOR.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/desenvolvimento/SKILL_DEV_SENIOR.md))
> **Propósito:** Definir a estratégia de testes e o checklist de qualidade que DEVE ser executado antes de qualquer deploy ou entrega de funcionalidade ao cliente.

---

## 1. Verificações Obrigatórias (Antes de Qualquer Entrega)

Estas verificações NUNCA podem ser puladas, independente do tamanho da mudança:

```bash
# 1. Verificação de tipos TypeScript (sem erros de compilação)
npx tsc --noEmit

# 2. Build de produção (garante que o app compila)
npm run build

# 3. Lint (qualidade de código)
npm run lint
```

> **Regra de ouro:** Se qualquer um desses três comandos falhar, **a entrega está bloqueada**. Não existe "vou corrigir depois" para falhas de compilação em TypeScript.

---

## 2. Casos de Teste Críticos por Tipo de Componente

### 2.1 Leitura de CSV (`csvParser.ts`)

| Cenário | Resultado esperado |
|---|---|
| CSV vazio (0 linhas de dado, só cabeçalho) | Retorna `[]` sem lançar exceção |
| CSV não encontrado (path errado) | Retorna `[]` com log de erro no servidor |
| Campo numérico como string vazia `""` | Não quebra — o componente trata com `parseFloat(val) \|\| 0` |
| Campo com valor `"N/A"` | Não quebra — componente trata como inválido |
| CSV com encoding diferente de UTF-8 | Retorna `[]` com log de erro (comportamento atual do parser) |
| CSV com separador `,` em vez de `;` | Todas as colunas colapsam na primeira — DETECTAR e alertar |
| Linha com menos colunas que o cabeçalho | O parser preenche os campos ausentes com `""` |

### 2.2 Componentes de Tabela (`TabelaOrcamento.tsx`)

| Cenário | Resultado esperado |
|---|---|
| `dados = []` (array vazio) | Exibir estado vazio: "Sem dados para esta obra" |
| Valor `PRECO_UNIT` vazio `""` | Exibir `—` ou `R$ 0,00` — nunca `NaN` |
| `QUANTIDADE_UCC` com valor `0` | Exibir normalmente (não filtrar zeros) |
| Texto longo em `SERVICO` | Truncar com `...` ou permitir quebra — nunca quebrar o layout |

### 2.3 Componentes de Gráfico (`LinhaDeBalanco.tsx`)

| Cenário | Resultado esperado |
|---|---|
| Série de dados vazia | Exibir mensagem "Sem dados de planejamento" |
| Datas fora de ordem | Ordenar internamente antes de plotar |
| `AVANCO_REAL_PCT > 100` | Truncar em 100 ou exibir alerta de dado inconsistente |
| `AVANCO_PLAN_PCT = AVANCO_REAL_PCT` para todos os pontos | Gráfico válido — sobreposição de linhas é esperada |

### 2.4 Contexto `ObraContext`

| Cenário | Resultado esperado |
|---|---|
| API `/api/obras` retorna `[]` | Estado padrão com `obraAtiva = 'OBRA'` (fallback atual) |
| API `/api/obras` falha (erro 500) | `catch` no `useEffect` — manter estado padrão sem quebrar |
| `obraAtiva` não existe em `listaObras` | Usar a primeira obra da lista como fallback |

---

## 3. Fluxo Completo de Teste de Integração

Antes de cada entrega de nova funcionalidade, executar o fluxo do início ao fim:

```
[1] Preparar dados de teste no CSV correspondente
    (incluir casos de borda: campos vazios, zeros, valores longos)
         ↓
[2] Rodar o motor Python (se aplicável):
    python scripts/gerador_orcamento_mestre.py [json_path]
         ↓
[3] Verificar o CSV gerado:
    - Schema correto?
    - Separador `;`?
    - Encoding UTF-8?
    - Campos numéricos como string numérica (não `""`)
         ↓
[4] Subir o dev server:
    npm run dev
         ↓
[5] Abrir o Dashboard e verificar:
    - Dados aparecem corretamente?
    - Nenhum `NaN` visível na UI?
    - Layout não quebrou com dados longos?
    - Estado vazio funciona ao apontar para obra sem CSV?
         ↓
[6] Rodar as 3 verificações obrigatórias (§1)
         ↓
[7] Entregar / fazer commit
```

---

## 4. Convenções de Commits

Usar prefixo descritivo para rastreabilidade:

| Prefixo | Uso |
|---|---|
| `feat:` | Nova funcionalidade (novo relatório, nova página) |
| `fix:` | Correção de bug |
| `refactor:` | Refatoração sem mudança de comportamento |
| `style:` | Ajuste visual (CSS, layout) |
| `chore:` | Atualização de dependências, config, scripts |
| `docs:` | Atualização de documentação / skills |

**Exemplos:**
```
feat: adicionar página de RDO ao dashboard
fix: tratar NaN em PRECO_UNIT vazio na TabelaOrcamento
refactor: mover cálculo de SPI para lib/calculos.ts
docs: atualizar SKILL_DEV_SCHEMA_CSV com campo STATUS
```

---

## 5. Checklist Final Antes de Mostrar ao Cliente

```
Checklist Pré-Entrega de Feature — Dashboard
============================================================
[ ] tsc --noEmit passou sem erros
[ ] npm run build concluiu sem erros
[ ] npm run lint passou (0 warnings críticos)
[ ] Testado com CSV vazio → exibe estado vazio corretamente
[ ] Testado com campo numérico vazio → sem NaN visível
[ ] Testado com obra sem nenhum CSV → não crasha
[ ] Layout testado com texto longo em campos de descrição
[ ] ObraContext: seletor de obra muda os dados corretamente
[ ] Nenhum console.log de debug vazando para produção
[ ] Nenhum dado hardcoded (nomes de obra, paths) — tudo dinâmico
```
