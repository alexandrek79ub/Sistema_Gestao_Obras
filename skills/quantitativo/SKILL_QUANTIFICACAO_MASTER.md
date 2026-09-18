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
| [SKILL_QUANTIFICACAO_AUDITORIA_E_CORRECAO.md](file:///c:/Users/Alexandre/Workspace/A11_SISTEMA_DE_GESTAO_OBRAS/skills/quantitativo/SKILL_QUANTIFICACAO_AUDITORIA_E_CORRECAO.md) | Auditoria e Verificação | Loop de QA anti-erro de leitura, checklists de cotas e geometria líquida |

> **Protocolo de uso:** Carregar este MASTER + a skill da disciplina necessária. A skill de auditoria é complementar e deve ser usada quando houver revisão, conferência ou suspeita de inconsistência; não é uma etapa obrigatória em todo levantamento.

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

## 🤖 1.1. Arquitetura Universal de Quantificação

O fluxo oficial de todas as disciplinas é simples e obrigatório. A navegação começa sempre pela lista de desenhos existente da obra:

```text
LISTA_DE_DESENHOS.csv
↓
selecionar pela própria lista usando disciplina_desenho + tipo_desenho
↓
ler disciplinas_levantadas / servicos_levantados / qtd_itens_quantitativo
↓
abrir somente o que ainda falta
↓
PDF
↓
Skill da disciplina
↓
LLM multimodal
├─ lê a prancha
├─ interpreta tecnicamente
├─ aplica os critérios de medição definidos na skill
├─ resolve descontos, apoios e interseções que dependem da leitura visual
└─ produz JSON estruturado com os inputs líquidos e suas evidências
↓
Python
├─ valida estrutura, tipos, unidades e evidências
├─ rejeita campos ausentes, incoerentes ou regras desconhecidas
├─ executa somente a matemática determinística
└─ grava no SQLite
↓
SQLite (fonte oficial)
↓
CSV / Markdown / Excel derivados
```

### Responsabilidade da Skill

A skill da disciplina define:
- o que procurar na prancha;
- como interpretar os elementos;
- os critérios de medição;
- como tratar apoios, encontros, vãos, interseções e descontos;
- quais dados são obrigatórios;
- quais regras Python podem ser acionadas;
- quando interromper e abrir RFI.

A skill não deve transferir fórmulas aritméticas simples para a LLM quando elas puderem ser executadas deterministicamente pelo Python.

### Responsabilidade da LLM multimodal

A LLM é responsável pela interpretação visual e técnica do projeto. Ela deve:
- identificar elementos e dimensões;
- entender relações espaciais visíveis na prancha;
- aplicar os critérios de medição da skill;
- fornecer comprimentos, áreas e demais inputs já líquidos quando o critério depender da leitura gráfica;
- registrar a evidência de cada input;
- indicar pendência quando a informação não estiver comprovada.

A LLM não deve enviar resultado final calculado, preço, BDI, custo ou expressão matemática como autoridade do sistema.

### Entrada obrigatória: Lista de Desenhos

Para qualquer levantamento, leia primeiro `projetos/[OBRA]/01_ENGENHARIA_E_PROJETOS/LISTA_DE_DESENHOS.csv`. Essa lista é o mapa oficial para localizar as pranchas; não faça varredura de pastas para descobrir PDFs quando a lista existir.

Selecione apenas as pranchas potencialmente necessárias à disciplina solicitada usando os próprios campos da lista:
- `disciplina_desenho`;
- `tipo_desenho`;
- `disciplinas_levantadas`;
- `servicos_levantados`;
- `qtd_itens_quantitativo`.

A decisão de abrir ou não uma prancha deve ser feita diretamente por esses campos. Não executar consulta SQLite adicional apenas para descobrir se o levantamento já existe.

No Fast Path é proibido usar `_carimbos_extraidos/`, `carimbos_metadados.json`, varredura de diretórios, `glob`, `os.walk`, scripts temporários ou inspeção em massa de PDFs para descobrir qual prancha usar. Se uma linha estiver classificada como `INDEFINIDA/INDEFINIDO`, ela deve permanecer pendente de classificação ou ser verificada isoladamente; isso não autoriza explorar todas as pranchas.

Depois disso, carregue apenas este MASTER + a skill específica necessária. Não coletar contexto geral da obra, RFI, RDO, cronograma, compras, orçamento ou outras disciplinas antes do levantamento. Buscar contexto adicional somente quando uma lacuna concreta da prancha impedir a medição.

### Responsabilidade do Python

O Python não interpreta o PDF. Ele recebe somente o JSON produzido pela LLM e:
- valida o contrato de dados;
- verifica campos obrigatórios;
- verifica tipos e unidades;
- rejeita valores inválidos;
- executa a fórmula cadastrada;
- gera a expressão auditável;
- grava a quantidade calculada no SQLite;
- gera artefatos derivados.

Erro de validação ou cálculo deve bloquear o item. Nunca converter erro em quantidade zero.

### Regra de simplicidade

- Não criar camadas intermediárias como `EvidenceRecord → ElementRecord → CalculationRequest` sem necessidade comprovada.
- Não explorar o repositório inteiro para um levantamento específico.
- Não carregar skills não relacionadas ao pedido.
- Não abrir todas as pranchas da obra; usar a lista e abrir somente as necessárias.
- Expandir contexto somente quando faltar um dado concreto para concluir a medição.

O contrato oficial entre IA e código é o JSON de extração da disciplina.

### Regra de evidência

Todo input usado em cálculo deve possuir evidência identificável no projeto. Sem evidência, o item não é calculado e deve ser tratado como `PENDENTE_RFI`.

---

## 📋 2. Modelos Universais de Memória de Cálculo

> Todos os números exibidos nos modelos desta seção são fictícios e servem somente como marcadores de preenchimento. Devem ser substituídos por evidências da prancha; nunca podem ser reutilizados como dados de uma obra. O resultado persistido é sempre a quantidade física líquida, sem perdas, UCC ou insumos derivados.

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
║  ✅ RESULTADO FÍSICO LÍQUIDO: XX,XX m²                           ║
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
║  ✅ RESULTADO FÍSICO LÍQUIDO: XX,XX m² de piso                  ║
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
║  ARMADURA (detalhamento executivo obrigatório):                 ║
║    Peso líquido conforme quadro de ferro: XXX,XX kg             ║
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
║  SUBTOTAL LÍQUIDO = 18,49 + 5,68 + 4,41 = 28,58 kg              ║
║                                                                  ║
║  ✅ AÇO TOTAL LÍQUIDO: 28,58 kg                                 ║
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
║  A_arremate = Perímetro × altura_especificada = XX,XX m²        ║
║  A_box (se houver) = Perím_box × altura_especificada = X,XX m²  ║
║  ÁREA TOTAL = XX,XX + X,XX + X,XX = XX,XX m²                    ║
║  ✅ RESULTADO FÍSICO LÍQUIDO: XX,XX m² impermeabilizados        ║
╚══════════════════════════════════════════════════════════════════╝
```

---

---

## 🔍 4. Protocolo de cobertura das pranchas selecionadas

> ⚠️ **REGRA ANTI-OMISSÃO:** esta seção vale somente para as pranchas previamente selecionadas pela `LISTA_DE_DESENHOS.csv`. Ela não autoriza varrer o acervo inteiro.
> 1. **Varredura completa somente da prancha selecionada:** depois que a lista indicar que uma prancha é necessária, leia nela plantas, cortes, elevações, notas, quadros e detalhes relevantes ao serviço solicitado. Não abrir outras pranchas sem uma lacuna concreta.  
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
| [PRANCHA] | [DETALHE / CORTE] | [DESCRIÇÃO] | [LEVANTADO / PENDENTE_RFI] |

#### Etapa 2 — Varredura Tridimensional por Matriz de Integridade

> A matriz abaixo é de cobertura de elementos e serviços executivos. Insumos secundários, consumíveis, perdas e embalagens são verificados apenas como exclusões e permanecem na BOM/CPU.
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
1. [DETALHE / PRANCHA]:
   - Opção A: [critério técnico confirmado em projeto].
   - Opção B: Quantificar como Calha-Rufo moldada in loco.

2. [ELEMENTO / CORTE]:
   - Opção A: [critério técnico confirmado em projeto].
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

### 3.3 Tabela de Insumos para Compra (FORA DO QUANTITATIVO FISICO)

> Interface posterior de BOM/CPU e compras. Esta tabela nao pertence a EAP fisica, nao e persistida em `itens_quantitativo` e nao pode alterar quantidades liquidas. Perdas, coeficientes, embalagens e precos entram somente nas etapas posteriores autorizadas.

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

1. **Gerar quantidades sem rastreabilidade** — todo resultado deve possuir inputs, evidências, regra aplicada e memória auditável gerada pelo motor.
2. **Resumir, agrupar ou omitir insumos/acessórios** — O levantamento DEVE ser 100% granular e detalhado peça-a-peça em todas as disciplinas (caixas, conexões, ferragens, suportes, aterramentos, calhas, rufos, etc.).
3. **Misturar serviços de disciplinas diferentes na mesma memória** — Estrutura e Arquitetura são sempre separadas.
4. **Ignorar a Regra de Desconto de Apoios / Interseções** — Em cruzamentos de elementos (ex: vigas x pilares/pilaretes), é obrigatório medir apenas a geometria líquida conforme a skill da disciplina. A LLM, por enxergar a prancha, aplica o critério visual de face a face, encontros e interseções antes de gerar o JSON. O Python apenas calcula sobre esses inputs líquidos. Jamais gerar duplicidade de concreto, fôrma, escavação, lastro, impermeabilização ou reaterro no mesmo nó.
5. **Omitir o Código CIA** em qualquer resultado.
6. **Assumir dimensões sem evidência** — dado ausente ou ambíguo gera `PENDENTE_RFI`; não estimar nem completar por suposição.
7. **Aplicar taxas de perda no levantamento de projeto** — É expressamente PROIBIDO aplicar perdas de material (concreto, aço, argamassa, madeira) ou empolamentos no levantamento físico. As perdas pertencem estritamente às Composições de Preço Unitário (CPUs/SINAPI) e compras.
8. **Gerar totais globais sem os subtotais por ambiente** — totais são soma auditável dos ambientes.
9. **Arredondar artificialmente números no projeto** — manter a precisão nominal geométrica de 2 casas decimais.
10. **Misturar área de teto com área de parede** — serviços separados, memórias separadas.
11. **Somar paredes irregulares como 2×C+2×L** — medir cada trecho individualmente (P1, P2...).
12. **Apresentar resultado sem unidade de medida** — m², m³, kg, m, unid são obrigatórios.
13. **Estimar preços ou quantitativos** — o agente apura o quantitativo físico das pranchas, o engenheiro orça com SINAPI/cotações.
14. **Inserir insumos miúdos, consumíveis ou embalagens comerciais (arames, pregos, espaçadores, fitas, tintas avulsas)** — É expressamente PROIBIDO explodir insumos secundários no levantamento físico. Esses insumos já estão inclusos nas composições de serviço.
15. **Emitir quantitativo sem a Tabela de Serviços / EAP correspondente** — todo levantamento deve estar vinculado aos serviços executivos e pacotes de trabalho da EAP para alimentar o cronograma e o avanço físico.
16. **Apresentar uma linha na Tabela de Quantitativos sem memória auditável** — a expressão final deve ser gerada pelo Python a partir dos inputs validados.
17. **Omitir cotas ou inventar dimensões ausentes em prancha** — se faltar cota ou detalhe, abrir RFI formal imediatamente.

---

## 📏 6. Regras de Precisão e Geometria Líquida Nominal

| Grandeza | Casas Decimais | Regra de Medição no Projeto |
|---|---|---|
| Dimensões lineares (m) | 2 decimais | Usar valor exato do projeto |
| Áreas de fôrma, alvenaria, revestimento (m²) | 2 decimais | Valor geométrico líquido nominal |
| Volumes de concreto, escavação, lastro (m³) | 2 decimais | Volume geométrico líquido nominal |
| Peso de armadura CA-50 / CA-60 (kg) | 2 decimais | Peso líquido conforme tabelas de ferro das pranchas |
| Peças pré-moldadas, portas, louças (unid) | Inteiro | Contagem exata de projeto |

> **Nota de Engenharia:** O levantamento de projeto deve preservar a fidelidade matemática absoluta da prancha. Conversões para embalagens comerciais de fornecedores (UCC) e coeficientes de perda de canteiro pertencem às composições de custo e às solicitações de compra, nunca ao quantitativo físico de projeto.

---

## ✅ 7. Checklist Universal de Entrega

Antes de encerrar qualquer levantamento de quantitativo:

- [ ] Hierarquia completa preenchida (Obra > Pavimento > Unidade > Ambiente > Disciplina > Serviço)
- [ ] Código CIA atribuído a cada ambiente
- [ ] Quadro de Esquadrias gerado (se houver serviços de alvenaria e acabamentos)
- [ ] Cada serviço possui inputs líquidos, evidências e regra aplicada; a expressão literal auditável é gerada pelo Python
- [ ] **Cada linha da Tabela de Serviços rastreada para sua memória de cálculo** (sem linha órfã)
- [ ] Revestimento de PAREDE separado de TETO
- [ ] Desconto de vãos aplicado (NBR 12721 — tabela de 3 faixas)
- [ ] **Zero perdas aplicadas** (quantitativo reflete 100% a geometria nominal das pranchas)
- [ ] **Zero insumos miúdos explodidos** (sem arames, pregos, desmoldantes, fitas poluindo o quantitativo)
- [ ] Pavimento Tipo com multiplicador aplicado (se houver)
- [ ] Tabela Resumo por Disciplina gerada com subtotais
- [ ] Tabela Oficial de Serviços para EAP gerada (mapeamento serviço → pacote de trabalho → cronograma)
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
