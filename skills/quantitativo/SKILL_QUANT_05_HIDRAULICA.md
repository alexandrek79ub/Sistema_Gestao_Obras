# 💧 SKILL 05: Instalações Hidráulicas (MEP)

**Disciplina:** Água Fria, Água Quente, Esgoto e Pluvial.
**Dependência:** `SKILL_QUANTIFICACAO_MASTER.md`

## 1. Escopo de Levantamento
- **Tubos:** PVC Soldável (Água Fria), PPR/CPVC (Água Quente), PVC Série Normal/Reforçada (Esgoto).
- **Conexões:** Joelhos (Cotovelos), Tês, Luvas, Caps, Reduções.
- **Registros e Válvulas:** Registros de Gaveta (Geral), Pressão (Chuveiro), Válvulas de Retenção.
- **Louças e Metais:** Bacias, Cubas, Torneiras, Sifões, Engates flexíveis.

## 2. Regras Matemáticas e Tolerâncias

### 2.1 Tubulações (Tubos)
- Medir a extensão linear em planta (X, Y) e somar os prumadas/descidas (Z).
- **Taxa de Perda:** Adicionar **10%** no total medido.
- **Regra UCC:** 
  - Tubos Soldáveis (Água): Barras de **3 metros** ou **6 metros** (arredondar CIMA).
  - Tubos de Esgoto: Barras de **6 metros**.

### 2.2 Conexões Hidráulicas (A "Regra da Taxa")
A contagem visual peça-por-peça é suscetível a erros de projeto (isométricos falhos). Para orçamentos, o Gestor adotará a regra mista:
- **Diâmetros Grandes (Esgoto/Pluvial >= 75mm):** Contagem *exata* (peça por peça). O valor financeiro é alto.
- **Diâmetros Pequenos (Água Fria/Quente <= 32mm):** O Agente de IA aplicará a "Taxa de Conexões", que consiste em adicionar **20%** sobre o valor financeiro do tubo para cobrir as dezenas de joelhos/luvas, ou fará a extração quantitativa caso o usuário forneça a tabela de peças (BOM) do projeto BIM.

## 3. Modelo de Memória de Cálculo (Hidráulica)
```text
╔══════════════════════════════════════════════════════════════════╗
║        MEMÓRIA DE CÁLCULO — INSTALAÇÕES HIDRÁULICAS             ║
╠══════════════════════════════════════════════════════════════════╣
║  AMBIENTE: [T-101-BAN]   SISTEMA: [Esgoto Sanitário]            ║
╠══════════════════════════════════════════════════════════════════╣
║  TUBULAÇÃO (PVC Esgoto Série Normal DN 100mm):                  ║
║    Trecho horizontal: X,XX m | Prumada: X,XX m                  ║
║    Subtotal: X,XX m + Perda 10% = X,XX m                        ║
║                                                                  ║
║  CONEXÕES E ACESSÓRIOS:                                          ║
║    Joelho 90º DN 100mm: 2 unid                                   ║
║    Junção Y 100x50mm: 1 unid                                     ║
║    Ralo Sifonado 150x150x50mm: 1 unid                            ║
║    Vaso Sanitário com Caixa Acoplada: 1 conjunto                 ║
╚══════════════════════════════════════════════════════════════════╝
```

## 4. Tabela Final de Compra (UCC)
O relatório final deve somar o total em metros e transformar em barras inteiras.
Exemplo: Se a obra precisa de 21 metros de Tubo Soldável 25mm, e a barra fornecida pela Tigre/Amanco é de 6 metros, a solicitação de compra final será de **4 Barras** (24m).
