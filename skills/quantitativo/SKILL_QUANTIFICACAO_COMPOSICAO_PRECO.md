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

## 2. O Link com o Quantitativo — Código CIA como Chave Única e Tabela CCU

Transforma a **quantidade** apurada pelas skills técnicas de quantitativo (`SKILL_QUANT_01` a `06` e `SKILL_QUANTIFICACAO_MASTER`) em **valor (R$)** através da chave unívoca do **Código CIA**:

```text
Quantitativo (SKILL_QUANT_XX / MASTER)        Tabela de Custo Unitário (CCU)
┌─────────┬──────────────────┬───────────┐     ┌─────────┬──────────────────────┐
│ CIA     │ Descrição        │ Quantidade│ ──► │ CIA     │ Custo Direto Unit R$ │
│ 02.01.03│ Emboço Paulista  │ 145 m²    │match│ 02.01.03│ R$ 30,75             │
└─────────┴──────────────────┴───────────┘     └─────────┴──────────────────────┘
```

### Regras de Match e Integridade CIA-CCU:
1. **Correspondência Exata por CIA:** Nenhuma quantidade é orçada sem que exista correspondência direta de código CIA na CCU (Tabela de Custos Unitários) ou composição SINAPI/TCPO. Se não houver match, o Agente sinaliza formalmente como 🔴 **CUSTO NÃO DEFINIDO PARA ESTE CIA**, sendo terminantemente proibido inventar valores "de cabeça" para tapar lacunas.
2. **Harmonização de Granularidade:** Se o CIA do quantitativo estiver detalhado por ambiente ou pavimento (ex: `02.01.03.T01`) e a tabela de CCU for agregada por serviço (`02.01.03`), o Agente deve consolidar a quantidade ao nível suportado pela CCU antes de aplicar o custo unitário — nunca aplicar custo unitário incorreto por descuido de hierarquia.
3. **Decomposição do Custo Unitário (Material + Mão de Obra + Equipamento):** Cada custo unitário na CCU deve apresentar separadamente o insumo material (com perdas conforme `SKILL_GESTAO_08`), mão de obra (Hh × RUP) e equipamentos, permitindo auditoria futura e análise de desvios.

---

## 3. Estrutura de Composição de Preço Unitário

```
Custo_Direto = Custo_Material + Custo_Mão_de_Obra + Custo_Equipamentos

Custo_Material = Σ (Qtd_insumo_k × Preço_Unitário_k)
Custo_Mão_de_Obra = Σ (Hh_k × Custo_Hh_k)
Custo_Equipamentos = Σ (H_maq_k × Custo_Horário_k)

Custo_Total = Custo_Direto × (1 + BDI%)
```

### Exemplo Completo — Emboço 20mm (por m²) [CIA 02.01.03]

| Insumo/Serviço | Qtd | Unid | P.Unit (R$) | Fonte | Custo Parcial |
|---|---|---|---|---|---|
| Cimento CP II | 5,8 | kg | R$ 0,90 | SINAPI 09/2026 | R$ 5,22 |
| Areia média | 0,030 | m³ | R$ 120,00 | SINAPI 09/2026 | R$ 3,60 |
| Cal hidratada | 1,2 | kg | R$ 1,20 | SINAPI 09/2026 | R$ 1,44 |
| Água | 8,5 | L | R$ 0,01 | — | R$ 0,09 |
| Servente (0,45 Hh/m²) | 0,45 | Hh | R$ 22,00 | Contrato empreit. | R$ 9,90 |
| Pedreiro (0,30 Hh/m²) | 0,30 | Hh | R$ 35,00 | Contrato empreit. | R$ 10,50 |
| **Custo Direto (CCU)** | | | | | **R$ 30,75** |
| **BDI 25%** | | | | | **R$ 7,69** |
| **Custo Total** | | | | | **R$ 38,44/m²** |

---

## 4. Custos Indiretos da Obra vs. Composição Analítica do BDI

A governança do sistema adota a melhor prática de engenharia de custos (Acórdão 2622/2013 - TCU, IBEC e CBIC): **segregação absoluta entre Custos Indiretos de Canteiro (Administração Local) e BDI Central**.

### 4.1 Por que NÃO usar o "BDI Gordo" (35% a 48%)?
No mercado tradicional, algumas construtoras embutem custos de canteiro, equipe indireta e alimentação dentro de uma taxa de BDI inflada (chamada de "BDI Gordo"). Essa prática é **rejeitada** pela nossa governança pelas seguintes razões:
1. **Falta de Rastreabilidade e Transparência:** Impede o cliente de auditar quanto da taxa é custo real de obra e quanto é margem/sede.
2. **Risco em Pleitos de Prazo (Claims):** Se a obra for prorrogada por chuvas extraordinárias ou atrasos de projeto pelo cliente, é impossível calcular com exatidão o custo mensal da equipe e canteiro parado se estiverem embutidos em percentual de serviço.
3. **Risco Fiscal e Previdenciário:** Mistura custos dedutíveis de canteiro com tributos de faturamento.

---

### 4.2 Matriz de Segregação: O que vai na Planilha (EAP) vs. O que vai no BDI

| Natureza do Custo | Classificação | Onde é Orçado? | Unidade de Medida | Exemplo no Sistema |
|---|---|---|---|---|
| **Engenheiro Residente / Coordenador** | Custo Indireto da Obra | Planilha Orçamentária (EAP 1.1) | mês / Hh | 10 meses × Salário + Encargos |
| **Mestre de Obras / Encarregados Gerais** | Custo Indireto da Obra | Planilha Orçamentária (EAP 1.1) | mês / Hh | 10 meses × Salário + Encargos |
| **Técnico de Segurança do Trabalho (TST)** | Custo Indireto da Obra | Planilha Orçamentária (EAP 1.1) | mês / Hh | Conforme exigência NR-4 / NR-18 |
| **Almoxarife, Apontador e Vigia / Portaria** | Custo Indireto da Obra | Planilha Orçamentária (EAP 1.1) | mês / Hh | Dimensionado por turno |
| **Containers (escritório, refeitório, vestiário)** | Custo Indireto da Obra | Planilha Orçamentária (EAP 1.1) | mês | Locação mensal de módulos habitáveis |
| **Sanitários Químicos e Limpeza Periódica** | Custo Indireto da Obra | Planilha Orçamentária (EAP 1.1) | unid / mês | Conforme NR-18 (1 para cada 20 operários) |
| **Água, Energia e Internet Provisórias** | Custo Indireto da Obra | Planilha Orçamentária (EAP 1.1) | mês | Consumo estimado + taxas de concessionária |
| **Alimentação (Café da manhã, Almoço, VR/VA)** | Custo Indireto da Obra | Planilha Orçamentária (EAP 1.1) | homem-mês / ref | Fornecimento por operário ativo |
| **Transporte de Pessoal (VT / Fretamento / Vans)** | Custo Indireto da Obra | Planilha Orçamentária (EAP 1.1) | mês / pase | Logística de deslocamento da equipe |
| **Alojamentos / Repúblicas de Mão de Obra** | Custo Indireto da Obra | Planilha Orçamentária (EAP 1.1) | mês | Aluguel de imóvel, mobília e manutenção |
| **EPIs, Fardamento e Exames (PGR/PCMSO/ASO)** | Custo Indireto da Obra | Planilha Orçamentária (EAP 1.1 / UCC) | cj / homem-ano | Kit inicial + reposição mensal |
| **Equipamentos de Apoio (Grua, Cremalheira, Gerador)**| Custo Indireto da Obra | Planilha Orçamentária (EAP 1.1) | mês | Locação mensal + combustível/energia + operador |
| **Diretoria, Jurídico, RH Corporativo e TI da Sede** | Administração Central (AC) | Taxa de BDI | % sobre Custo Direto | Rateio da estrutura central da empresa |
| **Seguro de Risco de Engenharia / Performance Bond**| Seguros e Garantias (S) | Taxa de BDI | % sobre Custo Direto | Apólices contratuais da construtora |
| **Riscos, Imprevistos e Contingências Globais** | Riscos (R) | Taxa de BDI | % sobre Custo Direto | Flutuações pontuais e intempéries leves |
| **Custo de Capital de Giro e Defasagem de Caixa** | Despesas Financeiras (DF) | Taxa de BDI | % sobre Custo Direto | Intervalo entre medição e recebimento |
| **Remuneração da Construtora pelo Empreendimento** | Lucro Operacional (L) | Taxa de BDI | % sobre Custo Direto | Margem bruta operacional da empresa |
| **Tributos Fiscais (PIS, COFINS, ISS, CPRB)** | Impostos (I) | Taxa de BDI | % sobre Faturamento | Carga tributária incidente sobre a nota |
| **IRPJ e CSLL** | Impostos Diretos | ❌ PROIBIDO NO BDI | — | Incide sobre o lucro líquido (Acórdão TCU 2622) |

---

### 4.3 Fórmula Analítica Oficial do BDI (IBEC / TCU Acórdão 2622/2013)

Com todos os custos de canteiro planilhados na EAP 1.1, a taxa de BDI é calculada estritamente pela fórmula:

```text
BDI = [ ((1 + AC + S + R) * (1 + DF) * (1 + L)) / (1 - I) ] - 1
```

Onde todos os parâmetros entram em formato decimal:
- **AC:** Taxa de rateio da Administração Central da construtora (sede)
- **S:** Taxa de Seguros e Garantias contratuais
- **R:** Taxa de Riscos, contingências e imprevistos
- **DF:** Taxa de Despesas Financeiras (custo do capital de giro)
- **L:** Taxa de Lucro Operacional bruto pretendido
- **I:** Somatório dos tributos diretos incidentes sobre o faturamento (PIS + COFINS + ISS + CPRB eventual)

---

### 4.4 Tabela Referencial de Parâmetros e Composição Padrão

| Componente do BDI | Sigla | Faixa TCU / Mercado | Valor Adotado Padrão | Justificativa Técnica |
|---|:---:|:---:|:---:|---|
| **Administração Central** | AC | 3,00% a 5,50% | **4,00%** | Cobertura da estrutura corporativa e governança |
| **Seguro e Garantia** | S | 0,80% a 1,50% | **1,00%** | Seguro de riscos de engenharia e apólice garantia |
| **Risco e Imprevisto** | R | 0,97% a 2,00% | **1,50%** | Cobertura de oscilações menores não contratuais |
| **Despesa Financeira** | DF | 0,59% a 1,39% | **1,00%** | Defasagem média de 30 a 45 dias entre gasto e medição |
| **Lucro Operacional** | L | 6,16% a 9,96% | **8,00%** | Remuneração justa pelo risco e capacidade técnica |
| **Tributos (Faturamento)** | I | 5,65% a 13,15% | **8,65%** | PIS (0,65%) + COFINS (3,00%) + ISS médio SP (5,00%) |
| **BDI Resultante (Serviços)** | **BDI** | **20,00% a 28,00%** | **27,17%** | **Cálculo exato pela fórmula analítica IBEC/TCU** |

#### Memorial de Cálculo Passo a Passo (BDI Serviços):
1. **Fator de Custos Centrais e Riscos:** `(1 + AC + S + R) = (1 + 0,0400 + 0,0100 + 0,0150) = 1,0650`
2. **Fator Financeiro:** `(1 + DF) = (1 + 0,0100) = 1,0100`
3. **Fator de Lucro:** `(1 + L) = (1 + 0,0800) = 1,0800`
4. **Numerador Composto:** `1,0650 * 1,0100 * 1,0800 = 1,161738`
5. **Denominador Fiscal:** `(1 - I) = (1 - 0,0865) = 0,9135`
6. **Multiplicador de Preço de Venda:** `1,161738 / 0,9135 = 1,271744`
7. **Taxa de BDI Final:** `1,271744 - 1 = 0,271744 = 27,17%` (arredondamento comercial para **25,00% a 27,00%** dependendo do ISS municipal efetivo).

---

### 4.5 BDI Diferenciado para Aquisição de Equipamentos e Materiais Nobres

Quando o orçamento envolve itens de elevado valor financeiro com pouca intervenção executiva (ex: elevadores de passageiros, grupos geradores a diesel, transformadores de alta tensão, chillers de HVAC, esquadrias importadas), **NÃO se aplica o BDI integral de serviços (27%)**.

Aplica-se o **BDI Reduzido / Diferenciado (10% a 15%)**, pois:
- A administração central demandada é residual (apenas gestão de contrato de compra).
- O risco de mão de obra direta inexiste (garantia assegurada pelo fabricante).
- O lucro bruto e as despesas financeiras operam em escala menor.

| Componente | Equipamento Nobre | Justificativa |
|---|:---:|---|
| **Administração Central (AC)** | 1,50% | Apenas diligenciamento de entrega |
| **Seguro e Garantia (S)** | 0,50% | Seguro de transporte e garantia de fábrica |
| **Risco (R)** | 0,50% | Risco mínimo de instalação direta |
| **Despesa Financeira (DF)** | 0,80% | Cronograma de faturamento direto com sinal |
| **Lucro Operacional (L)** | 4,00% | Margem comercial sobre intermediação |
| **Tributos (I)** | 8,65% | Impostos sobre faturamento |
| **BDI Equipamento Resultante** | **15,00%** | **BDI Diferenciado (Súmula 253 TCU)** |

---

### 4.6 Regras Fiscais e Contratuais Críticas

1. **Vedação de Bitributação:** NUNCA incluir na taxa de BDI custos de mão de obra de fiscalização ou apoio que já constem na Planilha de Administração Local (EAP 1.1).
2. **Vedação de IRPJ e CSLL no BDI:** O Imposto de Renda da Pessoa Jurídica (IRPJ) e a Contribuição Social sobre o Lucro Líquido (CSLL) são impostos diretos devidos sobre o resultado contábil da empresa, e devem ser absorvidos pela margem de lucro (`L`), nunca repassados explicitamente como custo no BDI.
3. **Pactuação no Kickoff:** O percentual exato do BDI (de serviços e de equipamentos) e a planilha de Administração Local devem ser expressamente apresentados e aprovados pelo cliente no Kickoff (`SKILL_GESTAO_00`), integrando o anexo orçamentário do contrato.

---

## 5. Regras de Atualização de Preço ao Longo da Obra

| Situação | Regra |
|---|---|
| Obra com duração ≤ 6 meses | Manter o SINAPI do mês de referência do orçamento base |
| Obra com duração > 6 meses | Incluir cláusula de reajuste no contrato (INCC ou IPCA + base de cálculo) |
| Atualização mensal do SINAPI | Sempre registrar o mês de referência na memória de cálculo (campo `FONTE_PRECO`) |
| Insumo não consta no SINAPI | Usar cotação local (3 fornecedores) — registrar em planilha de cotação vinculada |

---

## 6. Formato de Saída da Composição e Orçamento Vinculado

Toda composição e orçamento vinculado DEVE ser entregue na seguinte estrutura auditável por CIA:

```markdown
### 💵 Orçamento Vinculado — [Código CIA] — [Descrição do Pacote]

- **Código CIA:** [ex: 02.01.03]
- **Quantidade Apurada:** [valor + unid] (Fonte: SKILL_QUANT_XX)
- **Custo Unitário Direto (CCU):** R$ [valor] — Fonte: [SINAPI MM/AAAA / Cotação X]
- **Custo Direto Total:** R$ [Quantidade × Custo Unitário]
- **BDI Aplicado:** [%]
- **Valor Final do Item:** R$ [Custo Direto Total × (1 + BDI%)]

#### Composição Analítica do Custo Unitário (CCU):
| Serviço/Insumo | Qtd | Unid | P.Unit (R$) | Fonte | Custo Parcial (R$) |
|---|---|---|---|---|---|
| [Insumo 1] | [qtd] | [unid] | [R$] | [SINAPI MM/AAAA] | [R$] |
| [Mão de Obra 1] | [Hh] | Hh | [R$/Hh] | [Contrato empreit.] | [R$] |
| **Custo Direto** | | | | | **[R$]** |
| **BDI [%]** | | | | | **[R$]** |
| **Custo Total** | | | | | **[R$/unid]** |

⚠️ **CIAs Pendentes / Sem Custo:** [Lista de códigos CIA sem preço referenciado, se houver]
```

---

## 7. Integração com o CSV de Orçamento

Após compor os preços, preencher obrigatoriamente no `ORCAMENTO_BASE_CONSOLIDADO.csv`:

- `CODIGO_CIA` → Código CIA vinculando ao quantitativo e à EAP
- `PRECO_UNIT` → Custo Direto (sem BDI) por unidade de medida de engenharia (CCU)
- `CUSTO_TOTAL` → `QUANTIDADE_UCC × PRECO_UNIT × (1 + BDI%)`
- `FONTE_PRECO` → Ex: `SINAPI 09/2026 | Cotação 3 fornecedores 08/2026`

---

## 8. Árvore de Decisão — Composição de Preço

| Situação | Ação |
|---|---|
| Insumo encontrado no SINAPI | Usar preço SINAPI. Registrar mês/ano. |
| Insumo não encontrado no SINAPI | Solicitar cotação de 3 fornecedores. Registrar planilha de cotação. |
| Preço de cotação muito acima do SINAPI (> 20%) | Alertar o cliente. Investigar se especificação está correta. |
| Obra > 6 meses sem cláusula de reajuste | Alertar o cliente para inclusão de reajuste no contrato. |
| BDI não definido em contrato | Parar. Perguntar ao cliente o BDI aprovado antes de finalizar qualquer orçamento. |

---

## ⚠️ 9. Regras de Ouro da Orçamentação e Composição

1. **Rastreabilidade CIA Obrigatória:** Todo item orçado tem rastreabilidade até a linha exata do quantitativo que gerou a quantidade através do mesmo Código CIA. Orçamento nunca existe desconectado do quantitativo.
2. **Proibição de Estimativa sem Fonte:** Nenhum custo unitário (CCU) é arbitrado sem fonte declarada (SINAPI, cotação formal de 3 fornecedores ou contrato de empreitada). Ausência de fonte gera pendência formal (RFI), não estimativa.
3. **Transparência de BDI:** O percentual de BDI é sempre declarado de forma explícita e justificado por categoria (serviço vs. fornecimento de equipamentos), nunca embutido silenciosamente no preço unitário.
4. **Sincronismo com Revisões (`SKILL_GESTAO_14`):** Qualquer alteração de quantidade decorrente de revisão de projeto deve atualizar imediatamente o orçamento vinculado ao respectivo CIA.

---

## 🤖 10. Automação e Motor Universal de Precificação (`precificar_obra.py`)

O ecossistema dispõe do motor universal em Python (`scripts/precificar_obra.py`) que automatiza a aplicação de preços oficiais SINAPI SP e cotações locais em escala multi-obra:

```bash
# Execução por obra:
python scripts/precificar_obra.py --obra [NOME_DA_OBRA]

# Exemplos:
python scripts/precificar_obra.py --obra OBRA_TMULT
python scripts/precificar_obra.py --obra RESIDENCIAL_ALPHA
```

### Arquitetura de Desacoplamento (Data vs. Engine):
1. **Configuração da Obra (`projetos/[OBRA]/config_obra.json`):** Define prazos, área em m², taxas de BDI (serviços e equipamentos nobres) e o dimensionamento da equipe e canteiro (Administração Local - EAP 1.0).
2. **Tabela De-Para (`projetos/[OBRA]/02_ORCAMENTO_BASE_E_CONTRATOS/mapeamento_sinapi.csv`):** Conecta cada código EAP ao seu código SINAPI correspondente ou cotação homologada.
3. **Idempotência e Blindagem:** O motor pode ser executado sucessivas vezes de forma determinística, sem duplicação de itens de canteiro e com isolamento total entre obras.
