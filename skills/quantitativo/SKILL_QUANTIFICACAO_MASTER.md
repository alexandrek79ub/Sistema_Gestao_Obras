# 📐 SKILL MASTER: Sistema de Quantificação de Engenharia

Este é o **arquivo núcleo** do sistema de quantificação. Ele define os protocolos universais que se aplicam a **todas as disciplinas** (Fundações, Estrutura, Arquitetura, Elétrica, Hidráulica).

> 🚨 **REGRA ABSOLUTA DO SISTEMA (INVIOLÁVEL — BLINDAGEM CONTRA QUANTITATIVOS ESTIMADOS):**  
> 1. **JAMAIS ESTIMAR QUANTIDADES:** As quantidades são o fiel da balança de uma obra e definem seu sucesso ou fracasso. Portanto, precisam ser informações 100% extraídas e comprovadas em desenhos e pranchas executivas, **JAMAIS ESTIMADAS**. É expressamente PROIBIDO inferir, supor, adotar médias ou chutar dimensões, comprimentos, áreas ou volumes.  
> 2. **DEVER FORMAL QUANDO FALTAR INFORMAÇÃO NO DESENHO:** Caso alguma informação, cota, elevação, espessura ou especificação técnica **NÃO CONSTE NO DESENHO**, é **DEVER OBRIGATÓRIO E INEGOCIÁVEL** do orçamentista:  
>    - **NÃO quantificar o item** baseado em estimativa ou suposição.  
>    - **Registrar obrigatoriamente uma observação formal na Memória de Cálculo e na Planilha de Orçamento:**  
>      `⚠️ [ITEM NÃO LEVANTADO POR FALTA DE INFORMAÇÃO NO DESENHO - Prancha: [Ref] / Ambiente: [CIA] / Elemento: [Nome] - Aberta RFI nº XX].`  
>    - **Emitir RFI / Solicitação de Esclarecimento** ao projetista ou usuário para definição formal da cota.  
> 3. **RIGOR TÉCNICO E AUDITORIA:** Toda memória de cálculo é um documento jurídico-auditável. A presença de itens estimados sem respaldo no desenho resultará em REPROVAÇÃO IMEDIATA pela auditoria de qualidade.

---

## 📂 Módulos Disponíveis

| Arquivo | Disciplina | Conteúdo |
|---|---|---|
| [SKILL_QUANT_01_FUNDACOES.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANT_01_FUNDACOES.md) | Fundações | Sapatas, blocos 3 estacas, estacas/brocas, radier, baldrame, lastros, 10 serviços integrados |
| [SKILL_QUANT_02_ESTRUTURA.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANT_02_ESTRUTURA.md) | Estrutura | Pilares (nasce/morre), vigas (fundo/lados), lajes (escoramento PD), escadas, fôrmas, armadura CA-50/CA-60 |
| [SKILL_QUANT_03_ARQUITETURA.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANT_03_ARQUITETURA.md) | Arquitetura & Acabamentos | Alvenaria Paginada/Paramétrica, Room-by-Room, Panos de Fachada, Esquadrias, Louças, **Muros de Divisa, Portões & Pavimentação** |
| [SKILL_QUANT_04_ELETRICA.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANT_04_ELETRICA.md) | Elétrica, Lógica & SPDA | Eletrodutos, Cabos, QDC, Dutos Enterrados, SPDA, Entrada/Poste, Subestação, **Telefonia, Dados, Fibra, CFTV & Interfonia** |
| [SKILL_QUANT_05_HIDRAULICA.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANT_05_HIDRAULICA.md) | Hidráulica, Incêndio & Gás | Tubulações PVC/PEAD, Caixas Enterradas, Rede de Incêndio Aço, Gás, **Cavalete, Cisternas & Castelo D'Água Elevado** |
| [SKILL_QUANT_06_SERVICOS_ESPECIAIS.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANT_06_SERVICOS_ESPECIAIS.md) | Serviços Especiais & Canteiro | Preliminares, Terraplenagem/Contenções, HVAC, Elevadores/Bombas, SDAI/Extintores, **Comunicação Visual, Paisagismo, Piscinas & Áreas de Lazer** |
| [SKILL_QUANTIFICACAO_AUDITORIA_E_CORRECAO.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANTIFICACAO_AUDITORIA_E_CORRECAO.md) | Auditoria e Verificação | Loop de QA anti-erro de leitura, checklists de cotas, desmembramento de cantos e validação UCC |

> **Protocolo de uso:** Sempre carregar este MASTER + o módulo da disciplina necessária + **SKILL_QUANTIFICACAO_AUDITORIA_E_CORRECAO.md** para validação final.

---

## 🧭 1. Hierarquia Obrigatória de Rastreabilidade

Toda quantidade gerada deve estar vinculada à seguinte cadeia hierárquica, **sem exceções**:

```
OBRA
 └── PAVIMENTO  (ex: Subsolo, Térreo, Mezzanino, Tipo 01..N, Cobertura, Ático)
      └── UNIDADE / SETOR  (ex: Ap 101, Área Comum, Loja 01, Bloco A)
           └── AMBIENTE  (ex: Sala de Estar, Banheiro Social, Varanda)
                └── DISCIPLINA  (Fundações | Estrutura | Arquitetura | Elétrica | Hidráulica)
                     └── SERVIÇO / ELEMENTO  (ex: Emboço de Paredes, Pilar P1, Sapata F3)
                          └── MEMÓRIA DE CÁLCULO  ← Transcrição auditável obrigatória
```

### Código de Identificação de Ambiente (CIA)
Cada ambiente recebe um código único no formato: `[Pav]-[Unidade]-[Abrev]`

| Exemplo | Significado |
|---|---|
| `T-101-SAL` | Térreo, Ap 101, Sala de Estar |
| `T-101-BAN` | Térreo, Ap 101, Banheiro Social |
| `T-101-COZ` | Térreo, Ap 101, Cozinha |
| `TP-201-DOR` | Tipo, Ap 201, Dormitório |
| `COB-AC-PIS` | Cobertura, Área Comum, Piscina |
| `SUB-GAR-PI1` | Subsolo, Garagem, Pilar 1 |
| `FUN-GER-S01` | Fundação, Geral, Sapata 01 |

---

## 🤖 1.1. Arquitetura Híbrida de Quantitativo (Tool Use & Motor Python)

Para garantir **zero alucinação matemática e precisão contábil absoluta**, o processo de levantamento quantitativo adota uma arquitetura híbrida em 2 etapas:

1. **O Agente de IA (Extração e Regras):**  
   - Lê as pranchas executivas em PDF ou imagem.
   - Aplica as regras normativas desta Skill Master e dos Módulos Específicos.
   - **NUNCA calcula o valor numérico final de cabeça.**
   - Extrai as cotas e monta as expressões matemáticas no formato literal puro em um arquivo `.json` estruturado conforme o [template_dados_orcamento.json](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/scripts/template_dados_orcamento.json).
   - *Exemplo de expressão no JSON:* `"12 * pi * (0.30/2)**2 * 6.00"` ou `"11 * 1.4 * 1.4 * 0.7"`.

2. **O Motor Python na CPU ([gerador_orcamento_mestre.py](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/scripts/gerador_orcamento_mestre.py)):**  
   - O Agente aciona a execução no terminal:
     ```bash
     python scripts/gerador_orcamento_mestre.py [caminho_do_json]
     ```
   - O script resolve a matemática na CPU via AST segura, aplica perdas percentuais, converte para Unidade Comercial de Compra (UCC) aplicando teto (`math.ceil`) em itens inteiros, e gera automaticamente:
     - As Memórias de Cálculo em Markdown nativo (`MEMORIA_CALCULO_[DISC].md`);
     - Os quantitativos em CSV por disciplina (`QUANTITATIVO_[DISC].csv`);
     - O orçamento consolidado unificado (`ORCAMENTO_BASE_CONSOLIDADO.csv`), diretamente consumível pelo Dashboard Next.js.

---

## 📋 2. Modelos Universais de Memória de Cálculo

O Agente DEVE usar um destes modelos para **cada serviço, em cada ambiente**. Não omitir etapas.

> 🛑 **Padrão Obrigatório de Formatação Visual (Markdown Nativo Anti-Erro):**  
> Para garantir que as memórias de cálculo sejam renderizadas de forma limpa, elegante e 100% livre de erros visuais em qualquer editor ou visualizador (incluindo o VS Code nativo sem plugins de LaTeX):  
> 1. **Fórmulas e Equações:** Devem ser formatadas usando blocos de código nativos (ex: `V = N × (B × L × H)`) ou citações (`>`).  
> 2. **Zero Dependência de KaTeX/LaTeX:** É **PROIBIDO** usar blocos `$$` ou comandos `\text{}` que geram mensagens vermelhas de *ParseError* em visualizadores padrão.  
> 3. **Demonstrativo Auditável:** Exibir as substituições numéricas reais com unidades de forma legível e organizada.  
> 4. **Registro Mandatório de Falta de Informação em Desenho:** Caso falte qualquer cota, nível, detalhe ou especificação no projeto, é expressamente **PROIBIDO ESTIMAR OU INFERIR**. Deve constar obrigatoriamente a observação: `⚠️ [ITEM NÃO LEVANTADO POR FALTA DE INFORMAÇÃO NO DESENHO - Prancha: XX / Detalhe ausente: YY]` e abertura imediata de RFI.

### Modelo A — Revestimento de Parede / Teto:
```
╔══════════════════════════════════════════════════════════════════╗
║           MEMÓRIA DE CÁLCULO — [NOME DO SERVIÇO]                ║
╠══════════════════════════════════════════════════════════════════╣
║  OBRA:         [Nome da Obra]                                    ║
║  PAVIMENTO:    [Térreo / Tipo / Cobertura / etc.]                ║
║  UNIDADE:      [Ap 101 / Área Comum / Bloco A / etc.]            ║
║  AMBIENTE:     [Nome do Ambiente]       CIA: [T-101-COZ]         ║
║  DISCIPLINA:   Arquitetura                                       ║
║  SERVIÇO:      [Ex: Emboço de Paredes — espessura 20mm]          ║
╠══════════════════════════════════════════════════════════════════╣
║  DIMENSÕES DO AMBIENTE:                                          ║
║    Comprimento (A):  X,XX m                                      ║
║    Largura (B):      X,XX m                                      ║
║    Pé-direito (H):   X,XX m                                      ║
║                                                                  ║
║  FÓRMULA:                                                        ║
║    A_bruta = (2A + 2B) × H                                       ║
║    A_bruta = (2 × X,XX + 2 × X,XX) × X,XX                       ║
║    A_bruta = (X,XX + X,XX) × X,XX = XX,XX m²                    ║
║                                                                  ║
║  DESCONTO DE VÃOS (NBR 12721):                                   ║
║    [Tag]  [Tipo]  [L×H] = [A_vão] m²  → [Critério] → [Desconto] ║
║    Ex: PA-01  Porta  0,90×2,10 = 1,89 m² < 2,00 → NÃO desconta  ║
║    Ex: JA-02  Janela 1,50×1,80 = 2,70 m² → desconta (2,70-2,00) = 0,70 m² ║
║    Σ Descontos = X,XX m²                                         ║
║                                                                  ║
║  ÁREA LÍQUIDA = XX,XX − X,XX = XX,XX m²                         ║
║  TAXA DE PERDA (X%) = XX,XX × 1,0X = XX,XX m²                   ║
║                                                                  ║
║  ✅ RESULTADO FINAL: XX,XX m²                                    ║
╚══════════════════════════════════════════════════════════════════╝
```

### Modelo B — Revestimento de Piso:
```
╔══════════════════════════════════════════════════════════════════╗
║           MEMÓRIA DE CÁLCULO — REVESTIMENTO DE PISO             ║
╠══════════════════════════════════════════════════════════════════╣
║  OBRA/PAV/UNIDADE/AMBIENTE/CIA: [conforme hierarquia]           ║
║  SERVIÇO:  Piso [Tipo] [Formato] — assentamento [alinhado/diag] ║
╠══════════════════════════════════════════════════════════════════╣
║  A_piso = Comp × Larg = X,XX × X,XX = XX,XX m²                  ║
║  Descontos: pilares embutidos, ralos = X,XX m²                  ║
║  ÁREA LÍQUIDA = XX,XX m²                                        ║
║  TAXA DE PERDA (10%/15%) = XX,XX × 1,1X = XX,XX m²             ║
║                                                                  ║
║  INSUMOS (TCPO §9.10–§9.14 do módulo Arquitetura):             ║
║    Argamassa colante AC-[I/II/III]: XX,XX m² × 5,0 = XX,XX kg  ║
║    Rejunte (junta Xmm): XX,XX m² × X,XX = XX,XX kg             ║
║    Espaçadores: XX,XX m² × 6 = XX unid                         ║
║                                                                  ║
║  ✅ RESULTADO FINAL: XX,XX m² de piso                           ║
╚══════════════════════════════════════════════════════════════════╝
```

### Modelo C — Elemento Estrutural (Concreto + Fôrma + Aço):
```
╔══════════════════════════════════════════════════════════════════╗
║        MEMÓRIA DE CÁLCULO — ELEMENTO ESTRUTURAL                 ║
╠══════════════════════════════════════════════════════════════════╣
║  OBRA:     [Nome]   PAV: [Térreo]   CIA: [SUB-GER-P01]          ║
║  ELEMENTO: [Pilar P1 / Viga V3 / Laje L2 / Sapata F1]           ║
║  DIMENSÕES: b = X,XX m | h = X,XX m | H/L = X,XX m              ║
║  RESISTÊNCIA: Fck = XX MPa  | TIPO AÇO: CA-50 / CA-60           ║
╠══════════════════════════════════════════════════════════════════╣
║  CONCRETO:                                                       ║
║    V = b × h × H = X,XX × X,XX × X,XX = X,XX m³                ║
╠══════════════════════════════════════════════════════════════════╣
║  FÔRMA:                                                          ║
║    A_forma = (2b + 2h) × H = XX,XX m²                           ║
╠══════════════════════════════════════════════════════════════════╣
║  ARMADURA (taxa estimada ou detalhamento):                       ║
║    Taxa: XXX kg/m³ → Peso = X,XX × XXX = XXX,XX kg              ║
║    Arame recozido (1,5%): X,XX kg                                ║
║                                                                  ║
║  ✅ CONCRETO: X,XX m³ | FÔRMA: XX,XX m² | AÇO: XXX,XX kg        ║
╚══════════════════════════════════════════════════════════════════╝
```

### Modelo D — Armadura Detalhada por Bitola:
```
╔══════════════════════════════════════════════════════════════════╗
║        MEMÓRIA DE CÁLCULO — ARMADURA DETALHADA                  ║
╠══════════════════════════════════════════════════════════════════╣
║  ELEMENTO: [Viga V-01]   Pav: [Térreo]   CIA: [T-AC-V01]        ║
╠══════════════════════════════════════════════════════════════════╣
║  ARMADURA LONGITUDINAL:                                          ║
║    Ø 12,5mm (CA-50): 4 barras × (3,80m + 2×0,50m) = 4 × 4,80m  ║
║      → 19,20m × 0,963 kg/m = 18,49 kg                           ║
║    Ø 10,0mm (CA-50): 2 barras × (3,80m + 2×0,40m) = 2 × 4,60m  ║
║      → 9,20m × 0,617 kg/m = 5,68 kg                             ║
║                                                                  ║
║  ARMADURA TRANSVERSAL (Estribos):                                ║
║    Ø 6,3mm (CA-60): 20 estribos × 0,90m = 18,00m                ║
║      → 18,00m × 0,245 kg/m = 4,41 kg                            ║
║                                                                  ║
║  SUBTOTAL = 18,49 + 5,68 + 4,41 = 28,58 kg                      ║
║  TAXA DE PERDA (5%) = 28,58 × 1,05 = 30,01 kg                   ║
║  ARAME RECOZIDO (1,5%) = 30,01 × 0,015 = 0,45 kg                ║
║                                                                  ║
║  ✅ AÇO TOTAL: 30,01 kg + 0,45 kg arame = 30,46 kg              ║
╚══════════════════════════════════════════════════════════════════╝
```

### Modelo E — Impermeabilização:
```
╔══════════════════════════════════════════════════════════════════╗
║           MEMÓRIA DE CÁLCULO — IMPERMEABILIZAÇÃO                ║
╠══════════════════════════════════════════════════════════════════╣
║  OBRA/PAV/UNIDADE/CIA: [conforme hierarquia]                    ║
║  SERVIÇO: Impermeabilização — [Tipo: Manta Asfáltica / Polimérica] ║
╠══════════════════════════════════════════════════════════════════╣
║  A_piso = Comp × Larg = X,XX × X,XX = XX,XX m²                  ║
║  A_arremate (30cm) = Perímetro × 0,30 = XX,XX m²               ║
║  A_box (1,80m, se houver) = Perím_box × 1,80 = X,XX m²          ║
║  ÁREA TOTAL = XX,XX + X,XX + X,XX = XX,XX m²                    ║
║  TAXA DE PERDA (15%) = XX,XX × 1,15 = XX,XX m²                  ║
║                                                                  ║
║  INSUMOS (TCPO §9.14 do módulo Arquitetura):                    ║
║    Manta 3mm: XX,XX × 1,20 = XX,XX m²                           ║
║    Primer: XX,XX × 0,40 = XX,XX L                               ║
║                                                                  ║
║  ✅ RESULTADO FINAL: XX,XX m² impermeabilizados                 ║
╚══════════════════════════════════════════════════════════════════╝
```

---

---

## 🔍 4. Protocolo de Varredura Exaustiva de Projetos e Interrogatório Técnico (Varredura 360° — Regra Universal)

> ⚠️ **REGRA OBRIGATÓRIA E UNIVERSAL ANTI-OMISSÃO (APLICA-SE A TODAS AS DISCIPLINAS):**  
> 1. **Varredura 100% da Prancha:** Toda prancha de desenho deve ser varrida de ponta a ponta. É **ESTRITAMENTE PROIBIDO** olhar apenas para a Planta Baixa principal! O levantamento deve incluir obrigatoriamente: Plantas, Cortes, Elevações, Quadros de Legenda/Notas Técnicas, Prumadas, Esquemas Unifilares/Isométricos e **todos os Callouts de Detalhes Construtivos (Detalhes 01 a N)**. Nenhum detalhe pode ser esquecido ou ignorado.  
> 2. **Consulta Obrigatória ao Usuário:** Caso exista algum detalhe ou especificação no desenho que **NÃO possua instruções diretas ou regras claras nas Skills**, o Agente é **PROIBIDO de omitir ou assumir premissas por conta própria**. O Agente **DEVE OBRIGATORIAMENTE PARAR E PERGUNTAR AO USUÁRIO** (formulando o Interrogatório Técnico de Alinhamento) antes de prosseguir.

### 4.1 As 4 Etapas da Varredura Exaustiva

```
 [1. Mapeamento de Pranchas & Detalhes] ──► [2. Varredura 360° por Disciplina]
                                                    │
                                                    ▼
 [4. Matriz de Cobertura 100%] ◄── [3. Interrogatório Técnico se Houver Dúvida/Lacuna]
```

#### Etapa 1 — Mapeamento de Pranchas e Chamadas de Detalhes (Callout Scanning)
Antes de emitir o orçamento, o agente DEVE listar explicitamente todas as chamadas de detalhe encontradas nas pranchas:

| Prancha | Círculo / Chamada no Desenho | Descrição do Detalhe | Status no Levantamento |
|---|---|---|---|
| DW-2054-101 | Detalhe 01 / Corte AA | Impermeabilização da Calha e Platibanda | [X] Quantificado |
| DW-2054-102 | Detalhe 02 / 08 | Mureta de Apoio e Terça Metálica | [X] Quantificado (3x apoios) |
| DW-2054-102 | Detalhe 04 | Pingadeira Pré-moldada no topo da Platibanda | [X] Quantificado |
| DW-2054-102 | Detalhe 06 | Rufo Metálico de Encontro Telha/Platibanda | [X] Quantificado |

#### Etapa 2 — Varredura Tridimensional por Matriz de Integridade
Para cada disciplina, o agente deve verificar a **Cadeia Completa de Insumos Secundários**:

- **Fundações:** Estaca + Bloco + Lastro + Armadura + Fôrmas + Escavação + Reaterro.
- **Estrutura:** Pilares + Vigas + Lajes + Vigas Invertidas + Fôrmas + Armadura + Escoramento + Arame.
- **Alvenarias:** Alvenaria do Corpo + Alvenaria da Platibanda + Muretas de Apoio no Entreforro + Vergas/Contravergas + Bonecas.
- **Cobertura:** Telha + Terças Metálicas + Muretas de Apoio + Calha + Ralo Hemisférico + Tubo Queda AP + Pingadeiras + Rufos + Manta Asfáltica + Proteção Mecânica.
- **Impermeabilização:** Manta Asfáltica (Calhas) + Proteção Mecânica + Argamassa Polimérica (Piso Sanitário + Rodapé h=20cm) + Primer.

#### Etapa 3 — Protocolo de Interrogatório Técnico (Dúvidas ou Faltas de Instrução na Skill)
Se o agente identificar um detalhe construtivo ou elemento desenhado nas pranchas (ex: *"Detalhe de junta de dilatação"*, *"Peça especial de pingadeira"*, *"Mureta de apoio sem espessura"*), mas:
1. Faltar a especificação exata do material nas notas, OU
2. Não houver regra ou instrução direta de cálculo registrada nas Skills:

> 🛑 **PROIBIDO CHUTAR OU OMITIR O ITEM!**  
> O agente DEVE parar imediatamente o levantamento e formular o **Interrogatório Técnico de Alinhamento**, apresentando as opções ao usuário:

```markdown
❓ INTERROGATÓRIO TÉCNICO DE ALINHAMENTO DE ORÇAMENTO

Identifiquei os seguintes detalhes no projeto que requerem confirmação de critério:
1. DETALHE 06 (Rufo da Platibanda - Prancha DW-2054-102):
   - Opção A (Recomendada): Quantificar como Rufo em Chapa Galvanizada corte 33cm (20,36 m linear).
   - Opção B: Quantificar como Calha-Rufo moldada in loco.

2. MURETAS DE APOIO DA COBERTURA (Corte BB):
   - Opção A (Recomendada): Quantificar as 3 muretas escalonadas em Bloco 9x19x39cm (11,62 m²) SEM revestimento/emboço.
   - Opção B: Quantificar com emboço simples de proteção.
```

#### Etapa 4 — Emissão do Certificado de Cobertura de Detalhes
No final de cada levantamento, o agente DEVE declarar se 100% das pranchas e chamadas de detalhe foram cobertas.

> Preços preenchidos pelo Engenheiro com base no SINAPI vigente ou cotações locais. O agente NÃO estima preços — apenas quantidades.

### 3.2 Tabela de Resumo — Estrutura

| Elemento | Qtd | Und | Concreto (m³) | Fôrma (m²) | Aço (kg) | Fck | Pavimento | Custo (R$) |
|---|---|---|---|---|---|---|---|---|
| Pilar P1 | — | unid | — | — | — | C25 | — | — |
| Viga V1 | — | unid | — | — | — | C25 | — | — |
| Laje L1 | — | unid | — | — | — | C25 | — | — |
| Sapata F1 | — | unid | — | — | — | C30 | Fundação | — |
| Radier | — | m² | — | — | — | C30 | Fundação | — |
| | | | **TOTAL** | **TOTAL** | **TOTAL** | | | **R$ —** |

### 3.3 Tabela de Insumos para Compra

| Insumo | Und | Qtd Calculada | Coef. TCPO | Qtd para Compra | Preço Unit. (R$) | Custo (R$) |
|---|---|---|---|---|---|---|
| Blocos cerâmicos 9×19×19 | unid | — | 25/m² | Σ m² × 25 × 1,05 ↑ | — | — |
| Cimento CP II (sc 50kg) | sc | — | §9 ARQ | Σ kg / 50 ↑ | — | — |
| Areia média | m³ | — | §9 ARQ | Σ m³ | — | — |
| Cal hidratada (sc 20kg) | sc | — | §9.4 ARQ | Σ kg / 20 ↑ | — | — |
| Argamassa colante AC-II (sc 20kg) | sc | — | 5,0 kg/m² | Σ kg / 20 ↑ | — | — |
| Rejunte (sc 5kg) | sc | — | §9.11 ARQ | Σ kg / 5 ↑ | — | — |
| Massa corrida PVA (lt 25kg) | lata | — | 0,90 kg/m² | Σ kg / 25 ↑ | — | — |
| Tinta látex acrílica (lt 18L) | lata | — | 0,26 L/m² | Σ L / 18 ↑ | — | — |
| Selador acrílico (lt 18L) | lata | — | 0,10 L/m² | Σ L / 18 ↑ | — | — |
| Concreto usinado | m³ | — | — | Σ V_concreto | — | — |
| Aço CA-60 Ø 6,3mm | kg | — | §3.3 EST | Σ kg × 1,03 | — | — |
| Aço CA-50 Ø 8,0mm | kg | — | §3.3 EST | Σ kg × 1,05 | — | — |
| Aço CA-50 Ø 10,0mm | kg | — | §3.3 EST | Σ kg × 1,05 | — | — |
| Aço CA-50 Ø 12,5mm | kg | — | §3.3 EST | Σ kg × 1,05 | — | — |
| Aço CA-50 Ø 16,0mm | kg | — | §3.3 EST | Σ kg × 1,05 | — | — |
| Aço CA-50 Ø 20,0mm | kg | — | §3.3 EST | Σ kg × 1,05 | — | — |
| Arame recozido BWG 18 | kg | — | 1,5% aço | Σ aço × 0,015 | — | — |
| Manta asfáltica 3mm | m² | — | 1,20 m²/m² | Σ m² × 1,20 | — | — |
| Primer asfáltico | L | — | 0,40 L/m² | Σ m² × 0,40 | — | — |
| | | | | **TOTAL GERAL** | | **R$ —** |

> O símbolo **↑** indica arredondamento para cima (compra de unidades inteiras).

---

## 🌳 4. Árvore de Decisão — Qual Módulo Carregar

| Pedido do Usuário | Módulos a Carregar | Seção Aplicável |
|---|---|---|
| "Quantifique revestimento de paredes / piso / teto" | MASTER + ARQ | §1 (parede), §2 (piso), §3 (teto) ARQ |
| "Quanto de concreto no pilar P1 / viga / laje?" | MASTER + EST | §1 a §3 EST |
| "Calcule o aço da viga V-03" | MASTER + EST | §3 EST |
| "Quantifique as fundações (sapatas / radier / estacas)" | MASTER + FUN | §1 a §3 FUN |
| "Quantificação completa de um apartamento" | MASTER + ARQ + EST | Todos §§ |
| "Quantificação completa da obra" | MASTER + FUN + EST + ARQ | Todos §§ |
| "Preciso quantificar a impermeabilização" | MASTER + ARQ | §7.1 + §9.14 ARQ |
| "Parede de drywall / forro" | MASTER + ARQ | §8 ARQ |
| "Quantifique o pavimento tipo multiplicado por N andares" | MASTER + EST | §3.4 EST |
| "Preciso conferir/revisar um quantitativo" | MASTER + módulo da disciplina | §2 MASTER + módulo pertinente |
| "Tenho uma reforma — demolir e reconstruir" | MASTER + ARQ ± EST ± FUN | Etapas separadas |
| "Leia este PDF e quantifique" | MASTER + todos os módulos pertinentes | Skill completa |

---

## ⚠️ 5. Regras de Ouro — O Agente NUNCA deve:

1. **Gerar quantidades sem transcrever a memória de cálculo** — fórmula, valores e critério de desconto de vão obrigatórios.
2. **Resumir, agrupar ou omitir insumos/acessórios** — O levantamento DEVE ser 100% granular e detalhado peça-a-peça em todas as disciplinas (caixas, conexões, ferragens, suportes, aterramentos, calhas, rufos, etc.).
3. **Misturar serviços de disciplinas diferentes na mesma memória** — Estrutura e Arquitetura são sempre separadas.
4. **Ignorar a Regra de Desconto de Apoios / Interseções** — Em cruzamentos de elementos (ex: vigas x pilares/pilaretes), é obrigatório descontar os apoios na viga para que ela seja levantada apenas nos vãos livres, se os pilaretes já foram ou serão levantados inteiros. Jamais gere duplicidade de concreto, fôrma ou impermeabilização no mesmo nó.
5. **Omitir o Código CIA** em qualquer resultado.
6. **Assumir dimensões sem confirmação** — perguntar explicitamente antes de calcular.
7. **Usar taxas de perda sem registrar qual foi aplicada** — a taxa é parte da memória.
8. **Gerar totais globais sem os subtotais por ambiente** — totais são soma auditável dos ambientes.
9. **Arredondar para baixo** — quantitativos arredondam para CIMA na compra.
10. **Misturar área de teto com área de parede** — serviços separados, memórias separadas.
11. **Somar paredes irregulares como 2×C+2×L** — medir cada trecho individualmente (P1, P2...).
12. **Apresentar resultado sem unidade de medida** — m², m³, kg, m, unid são obrigatórios.
13. **Estimar preços** — o agente quantifica, o engenheiro precifica com SINAPI/cotações.
14. **Fechar a Tabela Consolidada sem antes varrer TODOS os Kits de Miudezas** de cada disciplina presente na obra (Kit Alvenaria §1.6 da SKILL_QUANT_03A, Kit Pintura §5, Kit Esquadrias §2.3 da SKILL_QUANT_03B, Kit Pisos §6, Kit Impermeabilização §1.5). A omissão de miudezas resulta em **REPROVAÇÃO IMEDIATA** pela auditoria.
15. **Emitir Tabela Consolidada sem a Tabela de Serviços / EAP correspondente** — todo levantamento de compras DEVE ser acompanhado do mapeamento de insumos → serviços → pacotes de trabalho EAP para alimentar o cronograma e os contratos de empreitada.
16. **Apresentar uma linha na Tabela Consolidada sem sua memória de cálculo detalhada** — cada insumo na tabela de compras DEVE ter sua expressão algébrica documentada na Seção 1 da Memória de Cálculo. Tabela sem memória correspondente = documento inválido.


---

## 📏 6. Regras de Precisão e Arredondamento

| Grandeza | Casas Decimais | Regra de Arredondamento Final |
|---|---|---|
| Dimensões lineares (m) | 2 decimais | Usar valor exato do projeto |
| Áreas (m²) | 2 decimais | Arredondar para cima na compra |
| Volumes (m³) | 2 decimais | Arredondar para cima na compra |
| Peso de aço (kg) | 2 decimais | Arredondar para cima na compra |
| Quantidade de blocos (unid) | 0 decimais | Arredondar para cima SEMPRE |
| Sacos de cimento / cal (unid) | 0 decimais | Arredondar para cima SEMPRE |
| Latas de tinta / massa (unid) | 0 decimais | Arredondar para cima SEMPRE |

### Conversão Obrigatória para Unidade Comercial de Compra (UCC)
O quantitativo de engenharia puro (físico/matemático) quase nunca bate com a embalagem do fornecedor. Para a Tabela de Insumos final, o Agente DEVE converter as quantidades para a Unidade Comercial (UCC):
- **Aço (Vergalhão):** Vendido em barras de **12 metros**. Se a obra precisa de 25 metros, deve-se comprar 3 barras (36m).
- **Tubos de PVC (Hidráulica):** Vendidos em barras de **3 metros** ou **6 metros** (dependendo da bitola). Se o projeto pede 14 metros de tubo esgoto 100mm, comprar 3 barras de 6m (18m).
- **Cimento / Argamassa:** Vendidos em sacos de **50kg** (cimento) ou **20kg** (argamassa). Dividir o total de kg pela capacidade do saco e arredondar o número de sacos para CIMA.
- **Pisos / Revestimentos:** Vendidos em **Caixas fechadas**. O Engenheiro deve fornecer o m²/caixa do modelo escolhido para que a divisão resulte em caixas inteiras.

> Resultados intermediários (por ambiente) mantêm 2 casas decimais. A conversão para UCC e o arredondamento para cima ocorrem somente no TOTAL FINAL de compra.

---

## ✅ 7. Checklist Universal de Entrega

Antes de encerrar qualquer levantamento:

- [ ] Hierarquia completa preenchida (Obra > Pavimento > Unidade > Ambiente > Disciplina > Serviço)
- [ ] Código CIA atribuído a cada ambiente
- [ ] Quadro de Esquadrias gerado (se houver serviços de revestimento)
- [ ] Memória de cálculo transcrita para **cada serviço em cada ambiente** — incluindo expressão algébrica para cada insumo
- [ ] **Cada linha da Tabela Consolidada rastreada para sua memória de cálculo** (sem linha órfã)
- [ ] Revestimento de PAREDE separado de TETO
- [ ] Desconto de vãos aplicado (NBR 12721 — tabela de 3 faixas)
- [ ] Taxas de perda explicitadas na memória
- [ ] Pavimento Tipo com multiplicador aplicado (se houver)
- [ ] Tabela Resumo por Disciplina gerada com subtotais
- [ ] Tabela de Insumos para Compra (BOM) gerada
- [ ] **Kits de Miudezas varridos por disciplina** (verificar cada kit antes de fechar a BOM):
  - [ ] Alvenaria: Kit §1.6 da SKILL_QUANT_03A (telas, pinos, adesivo, espuma de encunhamento)
  - [ ] Pinturas: Kit §5 da SKILL_QUANT_03A (selador, lixas, fita crepe, lona)
  - [ ] Pisos/Cerâmicos: Kit §6 da SKILL_QUANT_03B (cimentcola, rejunte, espaçadores, clips, cunhas)
  - [ ] Esquadrias: Kit §2.3 da SKILL_QUANT_03B (dobradiças, fechaduras, batedores, espuma PU, paraf., pregos, cola, selante)
  - [ ] Impermeabilização: Kit §1.5 da SKILL_QUANT_03B (primer, tela poliéster, fita asfáltica, GLP)
  - [ ] Cobertura: Kit da SKILL_QUANT_03C (parafusos autobrocantes, fita butílica, parabolts, rebites, selante)
- [ ] **Tabela de Serviços / EAP gerada** (mapeamento insumo → serviço → pacote de trabalho → cronograma)
- [ ] Totais auditáveis (soma dos subtotais por ambiente)
- [ ] Unidades de medida em todos os resultados
- [ ] Precisão decimal: 2 casas para m², m³, kg

---

## 🔒 8. Nota de Responsabilidade

> ⚠️ **AVISO OBRIGATÓRIO:** Todo quantitativo gerado por esta Skill é uma **ferramenta de apoio à engenharia** e deve ser conferido pelo Engenheiro/Arquiteto responsável técnico antes de uso para compra, contratação ou propostas.
>
> O Agente de IA:
> - NÃO substitui o julgamento técnico do profissional habilitado (CREA/CAU)
> - NÃO assume responsabilidade por variações de campo ou mudanças de projeto
> - DEVE alertar quando uma taxa ou coeficiente estiver fora do padrão usual
> - DEVE recomendar conferência humana quando houver ambiguidade nos dados
>
> **O engenheiro responsável deve revisar toda memória de cálculo antes de assinar ART/RRT.**
