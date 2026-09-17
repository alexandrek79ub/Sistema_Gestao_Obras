# ⚙️ Motor de Quantitativos, Orçamento e Exportação Executiva

O banco central SQLite em `data/pmo_virtual.sqlite` é a **ÚNICA Fonte da Verdade (SSOT)** do sistema de engenharia.
Planilhas Excel (`.xlsx`), arquivos CSV e Memórias de Cálculo em Markdown são **exclusivamente produtos derivados de exportação**, gerados automaticamente pelo motor para consumo externo, auditoria e apresentações executivas.

---

## 🏛️ 1. Arquitetura de Dados

```
JSON Entrada (Literais) ──► AST Python (CPU) ──► SQLite (data/pmo_virtual.sqlite)
                                                    │
       ┌────────────────────────────────────────────┴────────────────────────────────────────────┐
       ▼                                                                                         ▼
API Routes Next.js                                                                 Camada de Exportação
(node:sqlite direto ao banco)                                                      (scripts/motor_quantitativos/exportadores/)
       │                                                                                         │
       ▼                                                                                         ├─► Master Book Excel (.xlsx com 6 abas & fórmulas)
Dashboard Comercial                                                                              ├─► CSVs de Integração (ORCAMENTO_BASE, QUANTITATIVO)
(Curva S, EVM, LOB, Orçamento)                                                                   └─► Memórias de Cálculo em Markdown (.md)
```

- **`itens_quantitativo`**: Armazena a geometria física líquida nominal apurada das pranchas (sem perdas, UCC ou empolamento).
- **`itens_orcamento`**: Persiste a composição analítica de preço unitário (material, mão de obra, equipamento), fonte de preço (SINAPI SP / cotações), taxa de BDI, centro de custo e totais orçados.
- **`revisoes` & `snapshots`**: Trilha de auditoria rastreando autor, data, justificativa e integridade SHA-256.

---

## 📊 2. Caderno Master Excel com Fórmulas Vivas (`.xlsx`)

O subpacote modular `scripts/motor_quantitativos/exportadores/excel/` gera a planilha `ORCAMENTO_BASE_CONSOLIDADO.xlsx` com formatação executiva corporativa (paleta Navy/Slate, cabeçalhos estilizados, larguras automáticas e formatação de moeda brasileira). **Nenhuma fórmula é estática ou hardcoded.**

### Estrutura das 6 Abas Integradas:

1. **`01_ORCAMENTO_EAP`**:
   - Orçamento executivo estruturado por nível de EAP e disciplina.
   - Colunas: Código EAP, Descrição, Disciplina, Unidade, Quantidade, Custo Direto Unitário, BDI (%), Preço Unitário com BDI, Custo Total, Empreiteiro, Prancha, Fonte.
   - **Fórmulas dinâmicas:**
     - Preço Unitário com BDI: `=ROUND(F5*(1+G5/100), 2)`
     - Custo Total do Item: `=ROUND(E5*H5, 2)`
     - Total Geral do Orçamento: `=SUM(I5:I[N])`

2. **`02_PARAMETRICO_BDI`**:
   - Composição analítica de BDI paramétrico conforme fórmula oficial do Acórdão 2622/2013 TCU / IBEC.
   - Exibe parâmetros: Administração Central (AC), Seguro e Garantia (S), Risco (R), Despesas Financeiras (DF), Lucro (L), Tributos (PIS, COFINS, ISS, CPRB) e taxa resultante.

3. **`03_COMPOSICOES_CCU`**:
   - Tabela de Custos Unitários (CCU) analítica por serviço.
   - Decomposição transparente: Custo de Material (R$), Custo de Mão de Obra (R$) e Custo de Equipamento (R$).
   - **Fórmulas dinâmicas:**
     - Custo Direto Unitário: `=ROUND(SUM(D5:F5), 2)`

4. **`04_CURVA_ABC`**:
   - Matriz Pareto 80/20 com ordenação decrescente por relevância financeira.
   - Colunas: Ranking, Código EAP, Descrição, Custo Total, % do Orçamento, % Acumulado, Classe (A, B, C).
   - **Fórmulas dinâmicas:**
     - Percentual do Item: `=ROUND((D5/$D$[Total])*100, 2)`
     - Percentual Acumulado: `=ROUND(SUM($E$5:E5), 2)`
     - Classificação Pareto: `=IF(F5<=80, "A", IF(F5<=95, "B", "C"))`

5. **`05_MEMORIA_CALCULO`**:
   - Rastreabilidade física e geométrica integral das medições.
   - Colunas: Código EAP, Descrição, Unidade, Quantidade Calculada, Expressão Literal do Cálculo (ex: `11 * 1.4 * 1.4 * 0.7`), Prancha de Referência.

6. **`06_BOLETIM_MEDICAO`**:
   - Boletim de Medição Físico-Financeiro para gestão de avanço e pagamentos a empreiteiros.
   - Colunas: EAP, Descrição, Unidade, Preço Unitário, Qtd Contratada, Qtd Medida Anterior, Qtd Medida Período, Qtd Acumulada, Saldo a Executar, Valor Período (R$), Valor Acumulado (R$), Avanço Físico (%).
   - **Fórmulas dinâmicas:**
     - Quantidade Acumulada: `=F5+G5`
     - Saldo a Executar: `=E5-H5`
     - Valor do Período: `=ROUND(G5*D5, 2)`
     - Valor Acumulado: `=ROUND(H5*D5, 2)`
     - Avanço %: `=ROUND((H5/E5)*100, 2)`

---

## 🚀 3. Comandos Principais

### Importação Inicial e Compilação dos Artefatos

```bash
python scripts/motor_quantitativos/cli.py scripts/template_dados_orcamento.json --db data/pmo_virtual.sqlite
```

Calcula expressões na CPU via AST segura, persiste os dados no SQLite e exporta automaticamente:
- `projetos/[OBRA]/02_ORCAMENTO_BASE_E_CONTRATOS/ORCAMENTO_BASE_CONSOLIDADO.xlsx` (6 abas com fórmulas)
- `projetos/[OBRA]/02_ORCAMENTO_BASE_E_CONTRATOS/ORCAMENTO_BASE_CONSOLIDADO.csv`
- `projetos/[OBRA]/02_ORCAMENTO_BASE_E_CONTRATOS/QUANTITATIVO_MESTRE.csv`
- `projetos/[OBRA]/01_ENGENHARIA_E_PROJETOS/MEMORIA_CALCULO_[DISC].md`

*Nota: Se a obra já possuir dados no SQLite, a reimportação exige `--substituir` para evitar sobrescritas acidentais.*

### API Local para Edições Controladas e Auditadas

```bash
python scripts/api_pmo.py --db data/pmo_virtual.sqlite --port 8787 --api-key "sua-chave-local" --usuario "engenheiro-responsavel"
```

- `GET /api/quantitativos?obra_id={obra_id}`
- `PATCH /api/quantitativo/{obra_id}/{item_id}`

Toda edição via API exige:
1. Header `X-PMO-API-Key`
2. Campo `justificativa`
3. Campo `versao_esperada` (controle de concorrência otimista)
4. Gera snapshot de backup em `data/backups/` antes de aplicar a alteração
5. Recalcula o orçamento automaticamente
6. Regenera as exportações derivadas (Excel Master Book, CSVs e MDs) com novo SHA-256
