# 💰 SKILL: Composição de Preço — Do Quantitativo ao Custo Total Auditável

> **Frente:** Quantitativo → Orçamento
> **Propósito:** Fechar o loop orçamentário: todo item levantado por um skill de quantitativo DEVE passar por esta skill para receber custo unitário composto (material + mão de obra + BDI) com fonte rastreável.
> **Ativar quando:** "qual o custo de", "calcule o orçamento de", "feche o orçamento", "qual o preço unitário de", "monte a composição de custo"

---

## 1. Fontes de Preço Aceitas (Hierarquia Obrigatória)

As fontes devem ser usadas na seguinte ordem de preferência:

| Prioridade | Fonte | Rastreabilidade |
|---|---|---|
| **1ª (preferida)** | SINAPI vigente (Caixa Econômica Federal) | Registrar mês/ano de referência obrigatoriamente |
| **2ª** | Cotação local de **3 fornecedores** no mínimo | Arquivo de cotação deve existir e ser referenciado |
| **3ª (exceção)** | Histórico de NFs da própria obra (Conciliação 3 Pontas) | Referência à NF: número, data, fornecedor |

> ⚠️ **PROIBIDO usar preços de memória, estimativas gerais ou médias de mercado sem fonte documentada.** Todo preço unitário DEVE ter fonte rastreável registrada no campo `FONTE_PRECO` do CSV.

---

## 2. Estrutura de Composição de Preço Unitário

```
Custo_Direto = Custo_Material + Custo_Mão_de_Obra

Custo_Material = Σ (Qtd_insumo_k × Preço_Unitário_k)
Custo_Mão_de_Obra = Σ (Hh_k × Custo_Hh_k)

Custo_Total = Custo_Direto × (1 + BDI%)
```

### Exemplo Completo — Emboço 20mm (por m²)

| Insumo/Serviço | Qtd | Unid | P.Unit (R$) | Fonte | Custo Parcial |
|---|---|---|---|---|---|
| Cimento CP II | 5,8 | kg | R$ 0,90 | SINAPI 09/2026 | R$ 5,22 |
| Areia média | 0,030 | m³ | R$ 120,00 | SINAPI 09/2026 | R$ 3,60 |
| Cal hidratada | 1,2 | kg | R$ 1,20 | SINAPI 09/2026 | R$ 1,44 |
| Água | 8,5 | L | R$ 0,01 | — | R$ 0,09 |
| Servente (0,45 Hh/m²) | 0,45 | Hh | R$ 22,00 | Contrato empreit. | R$ 9,90 |
| Pedreiro (0,30 Hh/m²) | 0,30 | Hh | R$ 35,00 | Contrato empreit. | R$ 10,50 |
| **Custo Direto** | | | | | **R$ 30,75** |
| **BDI 25%** | | | | | **R$ 7,69** |
| **Custo Total** | | | | | **R$ 38,44/m²** |

---

## 3. Regras de Aplicação de BDI

> ⚠️ O BDI (Bonificação e Despesas Indiretas) cobre: administração central, riscos, lucro, seguros, garantia e impostos (menos ISS para PF).

### 3.1 BDI por Tipo de Serviço/Fornecimento

| Categoria | BDI Referência | Observação |
|---|---|---|
| Serviços de construção civil (empreiteiro PJ) | 25% a 30% | Acórdão TCU 2622/2013 |
| Fornecimento de materiais de alto valor (elevador, subestação, equipamento de HVAC) | 10% a 15% | BDI diferenciado — material não gera o mesmo custo indireto |
| Obras públicas (referência) | 24,23% (TCU) | Teto referencial TCU |
| Obras privadas (mercado) | 20% a 35% | Negociar com cliente no Kickoff |

### 3.2 Regras Críticas de BDI (Risco Fiscal)

- **NUNCA incluir ISS dentro do BDI de empreiteiro PJ** — o ISS é imposto de responsabilidade do empreiteiro e já está na composição de custo de mão de obra.
- **NUNCA aplicar o mesmo BDI** de serviços sobre o fornecimento de materiais de alto valor (equipamentos especiais) — isso infla artificialmente o custo e pode ser questionado em auditoria.
- **BDI DEVE ser negociado** com o cliente na reunião de Kickoff (SKILL_GESTAO_00) e registrado no contrato antes de qualquer orçamento.

---

## 4. Regras de Atualização de Preço ao Longo da Obra

| Situação | Regra |
|---|---|
| Obra com duração ≤ 6 meses | Manter o SINAPI do mês de referência do orçamento base |
| Obra com duração > 6 meses | Incluir cláusula de reajuste no contrato (INCC ou IPCA + base de cálculo) |
| Atualização mensal do SINAPI | Sempre registrar o mês de referência na memória de cálculo (campo `FONTE_PRECO`) |
| Insumo não consta no SINAPI | Usar cotação local (3 fornecedores) — registrar em planilha de cotação vinculada |

---

## 5. Formato de Saída da Composição (Auditável)

Toda composição de preço DEVE ser entregue na seguinte estrutura de tabela:

```markdown
## Composição de Custo — [Nome do Serviço] ([Unidade])

**Referência SINAPI:** [Mês/Ano] | **BDI:** [%] | **Data da Composição:** [DD/MM/AAAA]

| Serviço/Insumo | Qtd | Unid | P.Unit (R$) | Fonte | Custo Parcial (R$) |
|---|---|---|---|---|---|
| [Insumo 1] | [qtd] | [unid] | [R$] | [SINAPI MM/AAAA] | [R$] |
| [Insumo 2] | [qtd] | [unid] | [R$] | [Cotação X] | [R$] |
| [Mão de Obra 1] | [Hh] | Hh | [R$/Hh] | [Contrato empreit.] | [R$] |
| **Custo Direto** | | | | | **[R$]** |
| **BDI [%]** | | | | | **[R$]** |
| **Custo Total** | | | | | **[R$/unid]** |
```

---

## 6. Integração com o CSV de Orçamento

Após compor os preços, preencher obrigatoriamente no `ORCAMENTO_BASE_CONSOLIDADO.csv`:

- `PRECO_UNIT` → Custo Direto (sem BDI) por unidade de medida de engenharia
- `CUSTO_TOTAL` → `QUANTIDADE_UCC × PRECO_UNIT × (1 + BDI%)`
- `FONTE_PRECO` → Ex: `SINAPI 09/2026 | Cotação 3 fornecedores 08/2026`

---

## 7. Árore de Decisão — Composição de Preço

| Situação | Ação |
|---|---|
| Insumo encontrado no SINAPI | Usar preço SINAPI. Registrar mês/ano. |
| Insumo não encontrado no SINAPI | Solicitar cotação de 3 fornecedores. Registrar planilha de cotação. |
| Preço de cotação muito acima do SINAPI (> 20%) | Alertar o cliente. Investigar se especificação está correta. |
| Obra > 6 meses sem cláusula de reajuste | Alertar o cliente para inclusão de reajuste no contrato. |
| BDI não definido em contrato | Parar. Perguntar ao cliente o BDI aprovado antes de finalizar qualquer orçamento. |
