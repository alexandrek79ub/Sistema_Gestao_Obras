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

## 🐍 2. Motores em Python (`scripts/`)

Todo script localizado na pasta [`scripts/`](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/scripts/) é considerado um **Motor Universal de Produção**. Ele deve atender rigorosamente aos padrões abaixo:

### 2.1. Interface CLI Padrão com `argparse`
É terminantemente proibido criar scripts sem parametrização de linha de comando. Todo motor deve aceitar a obra alvo e caminho customizado:
```python
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Descrição do Motor Universal")
    parser.add_argument("--obra", default="OBRA_TMULT", help="Nome da pasta da obra em /projetos/ (default: OBRA_TMULT)")
    parser.add_argument("--dir", help="Caminho direto para a pasta da obra")
    args = parser.parse_args()
```

### 2.2. Resolução Agnóstica de Caminhos
Nunca utilize caminhos absolutos locais do seu computador (`C:\Users\...`). Sempre resolva os diretórios a partir da localização do próprio script:
```python
import os

# Raiz do repositório
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Resolução do diretório da obra
if custom_dir:
    proj_dir = os.path.abspath(custom_dir)
elif obra_nome:
    proj_dir = os.path.join(BASE_DIR, "projetos", obra_nome)
else:
    proj_dir = os.path.join(BASE_DIR, "projetos", "OBRA_TMULT")
```

### 2.3. Blindagem de Encoding UTF-8 no Windows
O console do Windows (PowerShell/CMD) frequentemente adota `cp1252`, gerando exceções ao imprimir emojis ou caracteres acentuados. Adicione sempre no início de todo script:
```python
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
```

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

### 2.6. Planilhas Excel com OpenPyXL
- Use paletas corporativas sóbrias (Azul Marinho `#1B365D`, Dourado `#D99B26`, Cinza Claro `#F8FAFC`).
- Todas as fórmulas de planilha devem estar em inglês e maiúsculas (`SUM`, `SUMPRODUCT`, `VLOOKUP`, `IF`).
- Congele sempre os cabeçalhos (`ws.freeze_panes = "A2"` ou correspondente).

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
| **1** | O script Python aceita `--obra` e `--dir` via `argparse`? | [ ] APROVADO |
| **2** | Há algum caminho fixo (`C:\...`) ou nome de obra chumbado no código? | [ ] ZERO HARDCODING |
| **3** | Os CSVs gerados usam `utf-8-sig` e delimitador `;`? | [ ] APROVADO |
| **4** | O relatório Markdown está livre de expressões KaTeX (`$$` ou `\text{}`)? | [ ] 100% LIMPO |
| **5** | O teste de fumaça executou com código de retorno 0 na `OBRA_TMULT`? | [ ] 100% OK |
| **6** | O teste de fumaça executou em outra obra (`RESIDENCIAL_ALPHA`) sem contaminação? | [ ] 100% ISOLADO |
| **7** | O modelo `_TEMPLATE_OBRA_NOVA` foi atualizado caso haja novo tipo de dado? | [ ] ATUALIZADO |
