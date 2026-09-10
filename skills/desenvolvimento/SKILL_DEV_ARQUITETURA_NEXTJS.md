# 🏗️ SKILL: Arquitetura Next.js e Padrões do Dashboard

> **Frente:** Desenvolvimento ([`SKILL_DEV_SENIOR.md`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/desenvolvimento/SKILL_DEV_SENIOR.md))
> **Propósito:** Mapear a arquitetura real do projeto `apresentacao_comercial/`, documentar convenções de naming, padrões de fetch de dados e passo a passo para adicionar novas funcionalidades sem sair dos trilhos.

---

## 1. Mapa de Pastas do Projeto

```
apresentacao_comercial/
├── src/
│   ├── app/                          # Next.js App Router
│   │   ├── layout.tsx                # Root layout (metadata, providers globais)
│   │   ├── page.tsx                  # Landing/home page (apresentação comercial)
│   │   ├── globals.css               # Estilos globais
│   │   ├── dashboard/                # Área logada de gestão
│   │   │   ├── layout.tsx            # Layout do dashboard (sidebar, header)
│   │   │   ├── page.tsx              # Dashboard principal (KPIs, EVM, Curva S)
│   │   │   ├── orcamento/            # Página de orçamento detalhado
│   │   │   ├── cronograma/           # Página de cronograma e Linha de Balanço
│   │   │   └── rdo/                  # Página de Relatório Diário de Obra
│   │   └── api/                      # API Routes (Server-side)
│   │       └── obras/                # Endpoint: lista as obras disponíveis
│   ├── components/                   # Componentes React reutilizáveis
│   │   ├── TabelaOrcamento.tsx       # Tabela de orçamento detalhada
│   │   ├── LinhaDeBalanco.tsx        # Gráfico de Linha de Balanço
│   │   └── ProjectSelector.tsx       # Seletor de obra ativa
│   ├── context/
│   │   └── ObraContext.tsx           # Contexto global: obra selecionada e lista de obras
│   └── lib/
│       └── csvParser.ts              # Utilitário de leitura de CSV (separador: `;`)
└── package.json
```

---

## 2. Padrões de Naming

| Elemento | Padrão | Exemplo |
|---|---|---|
| **Componente React** | PascalCase | `TabelaOrcamento`, `ProjectSelector` |
| **Hook customizado** | `use` + PascalCase | `useObra`, `useEVM`, `useCronograma` |
| **Função utilitária** | camelCase | `parseCSV`, `calcularSPI`, `formatarMoeda` |
| **Arquivo de componente** | PascalCase + `.tsx` | `TabelaOrcamento.tsx` |
| **Arquivo de página (App Router)** | `page.tsx` (obrigatório) | `app/dashboard/page.tsx` |
| **Arquivo de layout** | `layout.tsx` (obrigatório) | `app/dashboard/layout.tsx` |
| **Variável CSS** | `--kebab-case` | `--color-primary`, `--spacing-md` |

---

## 3. Contextos React — O que cada um provê

### `ObraContext` ([`ObraContext.tsx`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/apresentacao_comercial/src/context/ObraContext.tsx))

```typescript
interface ObraContextType {
  obraAtiva: string;           // Nome da pasta da obra ativa (ex: "OBRA_TMULT")
  setObraAtiva: (obra: string) => void;
  listaObras: string[];        // Lista de obras disponíveis em /projetos/
}
```

**Como usar em um componente:**
```typescript
import { useObra } from '@/context/ObraContext';
const { obraAtiva } = useObra();
```

**Fonte de dados:** Endpoint `/api/obras` que lê as subpastas de `/projetos/`.

---

## 4. Padrão de Fetch de Dados (CSV → Componente)

### Regra geral
- **Server Components** leem os CSVs diretamente via `parseCSV` e passam os dados como props.
- **Client Components** (marcados com `"use client"`) NUNCA leem arquivos diretamente — recebem dados via props ou via contexto/API Route.
- **Lógica de negócio** (cálculo de SPI, CPI, RUP) pertence a `/lib/` ou hooks, NUNCA dentro do JSX.

### Exemplo — Adicionar uma nova página ao dashboard:

```typescript
// app/dashboard/nova-pagina/page.tsx (Server Component)
import { parseCSV } from '@/lib/csvParser';
import path from 'path';

// Tipagem dos dados do CSV (SEMPRE tipar explicitamente)
interface LinhaOrcamento {
  CIA: string;
  SERVICO: string;
  QUANTIDADE_UCC: string;
  PRECO_UNIT: string;
  // ... outras colunas do schema
}

export default async function NovaPaginaPage() {
  const obraAtiva = 'OBRA_TMULT'; // Em produção: vem de params ou cookie
  const csvPath = path.join(
    process.cwd(),
    '..',
    'projetos',
    obraAtiva,
    '02_ORCAMENTO_BASE_E_CONTRATOS',
    'ORCAMENTO_BASE_CONSOLIDADO.csv'
  );

  const dados = parseCSV<LinhaOrcamento>(csvPath);

  return <ComponenteNovaPagina dados={dados} />;
}
```

---

## 5. Como Adicionar um Novo Relatório ao Dashboard

Checklist passo a passo — **não pule etapas**:

- [ ] **1. Definir o schema** do CSV de entrada em `SKILL_DEV_SCHEMA_CSV.md` (se não existir)
- [ ] **2. Criar a pasta** da página: `app/dashboard/[nome-relatorio]/`
- [ ] **3. Criar `page.tsx`** como Server Component que lê o CSV
- [ ] **4. Criar o componente** em `components/[NomeComponente].tsx` como Client Component se precisar de interatividade
- [ ] **5. Tipar explicitamente** a interface dos dados do CSV
- [ ] **6. Tratar edge cases:** CSV vazio (`dados.length === 0`), campo numérico como string vazia (`parseFloat(val) || 0`)
- [ ] **7. Adicionar link** no layout do dashboard (`app/dashboard/layout.tsx`)
- [ ] **8. Rodar verificação:** `npx tsc --noEmit` e testar no browser (`npm run dev`)
- [ ] **9. Executar checklist** do Loop do Tech Lead (SKILL_DEV_SENIOR, Etapa 4)

---

## 6. Integração com o Motor Python

O fluxo completo de dados:

```
1. IA extrai cotas → monta JSON (template_dados_orcamento.json)
                     ↓
2. python scripts/gerador_orcamento_mestre.py [json_path]
                     ↓
3. Gera: ORCAMENTO_BASE_CONSOLIDADO.csv + MEMORIA_CALCULO_[DISC].md
                     ↓
4. Dashboard Next.js lê o CSV via Server Component
                     ↓
5. Componentes exibem os dados ao usuário
```

**Regra:** O Dashboard é READ-ONLY em relação aos CSVs — ele lê mas nunca escreve. Toda escrita de dado passa pelo motor Python ou por entrada manual no CSV.

---

## 7. Anti-Padrões (Nunca faça isso)

| Anti-padrão | Por quê é problema | Alternativa correta |
|---|---|---|
| Ler CSV em Client Component | Não funciona — `fs` não existe no browser | Ler em Server Component e passar como prop |
| Usar `any` em TypeScript | Esconde erros de tipo que surgem com dados reais | Criar interface tipada para o CSV |
| Calcular SPI/CPI dentro do JSX | Mistura lógica de negócio com UI | Mover para `/lib/calculos.ts` |
| `console.log` em produção | Vaza dados e polui o console | Usar variável de ambiente para debug |
| Adicionar dependência sem verificar `package.json` | Pode quebrar o build ou criar conflito | Verificar se a lib já existe ou se pode usar nativa |
