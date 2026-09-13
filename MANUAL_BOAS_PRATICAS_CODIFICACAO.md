# 📘 Manual de Boas Práticas de Codificação & Engenharia de Software
### Ecossistema Integrado de Gestão de Obras & PMO Virtual (BIM 5D)

---

## 🧭 1. Princípios Gerais da Arquitetura

O sistema opera sobre um ecossistema híbrido de alta performance:
- **Engenharia de Dados e Motores de Cálculo:** Python 3.10+ (`scripts/`).
- **Apresentação e Dashboards Interativos:** TypeScript, React e Next.js 14+ (`apresentacao_comercial/`).
- **Banco de Dados Descentralizado (Flat-File DB):** Arquivos CSV (`utf-8-sig`), JSON estruturado e planilhas Excel (`projetos/[NOME_DA_OBRA]/`).
- **Memórias Técnicas e Contratos:** Markdown puro nativo (`.md`).

> **Lema do Tech Lead:** *"O código não é escrito apenas para funcionar hoje; é escrito para durar, ser auditado a qualquer momento e escalar para centenas de obras independentes sem contaminação cruzada."*

---

## 🐍 2. Motores em Python (`scripts/`) — Arquitetura Modular v2.0 Lean

Todo script localizado na pasta [`scripts/`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/scripts/) é considerado um **Motor Universal de Produção**. Ele deve atender rigorosamente aos padrões da **Arquitetura Modular v2.0 Lean**, mantendo o código conciso (idealmente entre 150 e 300 linhas):

### 2.1. Camada de Infraestrutura Compartilhada (`scripts/common/`)
É terminantemente proibido reimplementar rotinas de CLI, resolução de pastas, leitura de configuração, manipulação de dias úteis ou estilização de planilhas Excel. Utilize sempre os módulos utilitários canônicos:

```python
import sys
import os

# Adiciona o diretório scripts/ ao sys.path caso necessário
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# I/O, CLI padronizada e persistência segura:
from scripts.common.obra_io import (
    parse_obra_args,           # Parser com --obra e --dir padronizados
    resolver_obra_dir,         # Resolução dinâmica sem hardcoding
    carregar_config_obra,      # Leitura resiliente de config_obra.json
    salvar_csv_utf8_sig,       # CSV com encoding utf-8-sig e separador ';'
    salvar_json                # JSON estruturado formatado (indent=2)
)

# Estilização visual única de planilhas OpenPyXL:
from scripts.common.excel_theme import (
    NAVY, BLUE_DARK, BLUE_LIGHT, GOLD_ACCENT, GREEN_FILL, RED_FILL,  # Paleta
    FONT_TITLE, FONT_HEADER, FONT_BOLD, FONT_REGULAR,                # Tipografia
    THIN_BORDER, ALIGN_CENTER, ALIGN_LEFT, ALIGN_RIGHT,              # Geometria
    aplicar_cabecalho_tabela, auto_ajustar_colunas, zebrar_linhas     # Utilitários
)

# Cálculos de calendário e dias úteis:
from scripts.common.calendario import (
    parse_date_br, dias_uteis_entre, adicionar_dias_uteis, janelas_mensais_obra
)
```

### 2.2. Desacoplamento de Templates de Relatórios (`scripts/templates/`)
- **Regra de Ouro:** Scripts Python **NÃO** devem conter centenas de linhas de blocos literais de texto Markdown (`f"""# LAUDO..."""`).
- Laudos técnicos, termos contratuais, minutas, manuais, RDOs e cadernos de FVS devem residir em arquivos `.md` dedicados dentro de [`scripts/templates/`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/scripts/templates/) (ex: `templates/databook/`, `templates/rdo/`, `templates/qualidade/`, `templates/avanco/`).
- O script Python apenas lê o arquivo de template e realiza a substituição limpa de placeholders:
```python
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates", "databook")

def carregar_template(nome_arquivo, config):
    caminho = os.path.join(TEMPLATES_DIR, nome_arquivo)
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
    return (
        conteudo
        .replace("{{NOME_OBRA}}", config.get("nome_obra", "Obra"))
        .replace("{{SIGLA_OBRA}}", config.get("sigla_obra", "OBRA"))
    )
```

### 2.3. Catálogos e Tabelas de Referência de Engenharia (`apoio/`)
- Tabelas de custos de mão de obra (CUB/SINDUSCON), frentes de esteira Takt, especificações de FVS e composições de engenharia **não devem ficar hardcoded** dentro dos scripts.
- Elas devem residir na pasta [`apoio/`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/apoio/) em formato JSON auditável:
  - `apoio/catalogo_funcoes.json`: Especialidades e custos hora-homem (CUB/SINDUSCON);
  - `apoio/mapa_lotes_cpm.json`: Mapeamento canônico dos 52 lotes Lean com atividades CPM e LOB;
  - `apoio/catalogo_lotes_takt.json`: Especificação completa dos 52 lotes de produção (metas físicas, equipes, equipamentos e RUP);
  - `apoio/catalogo_fvs.json`: Especificação normativa das 8 FVSs bloqueantes (critérios, tolerâncias NBR e travas contratuais).
- O script deve carregar esses catálogos com fallback seguro caso um contrato regional específico deseje sobrescrevê-los via `config_obra.json`.

### 2.4. Regex de Alta Precisão (Fronteiras de Palavra)
Em processamento de strings de engenharia, nunca use `in` para palavras curtas. Use sempre `\b` para evitar falsos positivos graves:
```python
import re

# CORRETO: Só casa com "AÇO" isolado (evita casar com "MAÇO", "BRAÇO", "ESPAÇO")
if re.search(r'\b(ACO|AÇO|ARMADURA|ARMADURAS)\b', texto_normalizado):
    processar_aco()

# ERRADO: Causará falso positivo com "Reaterro com Maço"
if "ACO" in texto_normalizado:
    processar_aco()
```

### 2.5. Prazos e Arrays Dinâmicos Multi-Obra
Nunca assuma que todas as obras duram 6 meses. O prazo deve ser lido de `config_obra.json` (`prazo_meses`) e os fatiamentos de colunas devem ser dinâmicos para não gerar `AssertionError` em bibliotecas como Pandas:
```python
prazo_meses = int(config.get("prazo_meses", 6))
meses_headers = [f"M{m}" for m in range(1, prazo_meses + 1)]

# Fatiamento seguro de dados para bater com o número exato de colunas:
row_ajustada = row[:4] + row[4:4 + prazo_meses]
```

### 2.6. Planilhas Excel com OpenPyXL e Padrão Visual Único
- Use exclusivamente a paleta centralizada de [`excel_theme.py`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/scripts/common/excel_theme.py) (`NAVY`, `BLUE_DARK`, `GOLD_ACCENT`).
- Todas as fórmulas de planilha devem estar em inglês e maiúsculas (`SUM`, `SUMPRODUCT`, `VLOOKUP`, `IF`).
- Congele sempre os painéis (`ws.freeze_panes = "E6"` ou correspondente) e use `auto_ajustar_colunas(ws)` ao finalizar a planilha.

---

## 📊 3. Banco de Dados Flat-File (CSVs e JSONs)

Os dados de cada obra residem dentro de suas respectivas pastas em `projetos/[NOME_DA_OBRA]/`.

### 3.1. Padrão Mandatório de CSV para Excel Brasileiro
- **Codificação:** `utf-8-sig` (inclui o BOM UTF-8, essencial para o Microsoft Excel abrir caracteres acentuados corretamente no Windows).
- **Delimitador:** Ponto e vírgula (`;`). O uso de vírgula simples quebra colunas que contêm descrições técnicas ou valores monetários no Brasil.
```python
import csv

with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Código EAP", "Item / Descricao", "Valor Total (R$)"])
```

### 3.2. Formatação Numérica e Monetária
- **Em Arquivos CSV e Relatórios MD:** Formato brasileiro legível (`R$ 1.660.762,28`).
- **Em Arquivos JSON e Cálculos de CPU:** Float puro (`1660762.28`).
- Função padrão de formatação:
```python
def formatar_moeda(val):
    if val <= 0:
        return "R$ 0,00"
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
```

### 3.3. Regra da Unidade Comercial de Compra (UCC)
Materiais discretos nunca podem ser comprados em quantidades fracionadas:
- Barras de aço, chapas de compensado, sacos de cimento, latas de tinta e caixas de porcelanato devem sofrer arredondamento obrigatório para cima via `math.ceil()`.
- O cálculo deve aplicar a taxa regulamentar de perda contratual (ex: 5% para aço, 10% para fôrmas, 10% para tintas).

---

## ⚛️ 4. Frontend Web BIM 5D (`Next.js / TypeScript`)

O dashboard comercial e executivo opera em Next.js no diretório [`apresentacao_comercial/`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/apresentacao_comercial/).

### 4.1. Arquitetura em Camadas
- **Componentes (`/components`):** Devem ser componentes puros ("burros"), focados unicamente na renderização e experiência visual.
- **Hooks (`/hooks`):** Centralizam o consumo de dados, caching, leitura de CSVs e tratamento de estado.
- **Utilitários (`/lib`):** Funções matemáticas puras de valor agregado (EVM, Curva S, Linha de Balanço).

### 4.2. Tipagem Estrita sem Concessões
- Proibido o uso de `any` sem justificativa documentada em comentário.
- Toda entidade do sistema (Item de EAP, Insumo, Contrato, Medição) deve possuir sua `interface` ou `type` TypeScript fortemente tipado em `/types`.

### 4.3. Tratamento de Estados de Borda (Edge Cases)
Todo componente interativo deve tratar explicitamente 4 estados:
1. **Loading State:** Skeleton screen ou spinner suave.
2. **Error State:** Alerta explicativo com botão de tentar novamente (sem tela em branco).
3. **Empty State:** Ilustração ou aviso claro caso a obra não possua registros naquela disciplina.
4. **Data Loaded:** Renderização suave com micro-animações.

---

## 📝 5. Relatórios Técnicos e Memórias (`Markdown`)

O Markdown é a saída oficial para contratos, certificados e memórias de cálculo.

### 5.1. Regra Inviolável da Pureza Markdown (Anti-KaTeX)
> 🚨 **PROIBIÇÃO ABSOLUTA DE BLOCOS LATEX CRUS (`$$` ou `\text{}`):**
> Sintaxes como `$L_{\text{livre}} = 140,44\text{ m}$` ou `$$\text{BDI} = 27,17\%$$` quebram a visualização no GitHub, no VS Code e em conversores de PDF.
> **Escreva sempre em notação limpa nativa:**
> - `L_livre = 140,44 m`
> - `BDI = 27,17%`
> - `Volume = 64,48 m³`
> - `Área = 731,91 m²`

### 5.2. Links Clicáveis Auditáveis
Links para pranchas, planilhas ou relatórios locais devem usar o esquema oficial `file:///`:
- ✅ `[Nome da Prancha](file:///c:/Users/Alexandre/.../prancha.pdf)`
- ❌ `[Nome da Prancha](c:\Users\Alexandre\...\prancha.pdf)`

### 5.3. Tabelas Markdown
- Use alinhamento explícito nas colunas (`:---` para texto, `:---:` para códigos/datas, `---:` para valores monetários).
- Não deixe linhas quebradas no meio de uma tabela.

---

## 🗂️ 6. Gestão de Repositório e Versionamento (Git)

### 6.1. Padrão de Mensagens de Commit (Conventional Commits)
Adote sempre o padrão semântico:
- `feat(modulo):` Nova funcionalidade ou motor criado.
- `fix(modulo):` Correção de bug ou divergência numérica.
- `refactor(modulo):` Desacoplamento ou melhoria de código sem alterar regra de negócio.
- `docs(governança):` Atualização de manuais, checklists ou POPs.
- `test(auditoria):` Testes de fumaça ou verificações de conformidade.

### 6.2. Higiene de Pastas
- A pasta `scripts/` deve conter **apenas motores universais**.
- Scripts legados, históricos ou backups monolíticos devem ser mantidos em `scripts/_legado_tmult/`.
- Dados de obras devem ficar isolados dentro de `projetos/[NOME_DA_OBRA]/`.
- Modelos universais devem ser preservados em `projetos/_TEMPLATE_OBRA_NOVA/`.

---

## 🚦 7. Checklist de QA Pré-Commit do Desenvolvedor

Antes de fazer qualquer commit ou entrega de código, execute o checklist mental:

| # | Check de Qualidade | Status Obrigatório |
| :-: | :--- | :---: |
| **1** | O script reutiliza a camada compartilhada [`scripts/common/`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/scripts/common/) (`obra_io`, `excel_theme`, `calendario`)? | [ ] REUTILIZADO |
| **2** | Textos longos de laudos/termos foram externalizados para [`scripts/templates/`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/scripts/templates/)? | [ ] DESACOPLADO |
| **3** | Dados vivos de engenharia foram externalizados para [`apoio/`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/apoio/)? | [ ] AUDITÁVEL |
| **4** | O script aceita `--obra` e `--dir` com ZERO caminhos absolutos ou fixos (`C:\...`)? | [ ] ZERO HARDCODING |
| **5** | Os CSVs gerados usam estritamente `utf-8-sig` e delimitador `;`? | [ ] APROVADO |
| **6** | O relatório Markdown gerado está limpo e sem expressões KaTeX (`$$` ou `\text{}`)? | [ ] 100% LIMPO |
| **7** | Teste de fumaça executado com sucesso (código 0) na `OBRA_TMULT` e em `_TEMPLATE_OBRA_NOVA`? | [ ] 100% ISOLADO |
