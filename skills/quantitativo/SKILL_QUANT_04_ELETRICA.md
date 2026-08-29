# ⚡ SKILL 04: Instalações Elétricas (MEP)

**Disciplina:** Elétrica e Lógica
**Dependência:** `SKILL_QUANTIFICACAO_MASTER.md`

## 1. Escopo de Levantamento
O Agente deve extrair quantidades dos projetos unifilares elétricos, separando-os por:
- **Eletrodutos:** Conduítes corrugados (embutidos) e tubos rígidos (aparentes).
- **Condutores:** Fios e Cabos (seção em mm² e cores - Fase, Neutro, Terra, Retorno).
- **Caixas:** Passagem, tomadas e interruptores (4x2, 4x4, octogonais).
- **Quadros:** Quadros de Distribuição (QDC) e Disjuntores (DPS, DR, Termomagnéticos).

## 2. Regras Matemáticas e Tolerâncias

### 2.1 Eletrodutos
- Medir a extensão linear em planta e somar as descidas/subidas de parede (Pé-direito).
- **Taxa de Perda:** Adicionar **10%** sobre o comprimento total calculado.
- **Regra UCC:** Comprar eletrodutos flexíveis sempre em múltiplos de **50 metros** (Rolo padrão). Tubos rígidos em múltiplos de **3 metros**.

### 2.2 Fios e Cabos
- A metragem de fios não é apenas a metragem do eletroduto multiplicada pelos circuitos.
- **Regra de Pontas (Sobra Obrigatória):** Adicionar +0,50m para cada caixa de passagem/tomada que o fio acessar, e +1,00m dentro do Quadro de Distribuição.
- **Taxa de Perda:** Adicionar **5%** sobre o cálculo total.
- **Regra UCC:** Cabos até 10mm² são comprados em Rolos de **100 metros**. Cabos de bitolas maiores podem ser comprados por metro linear fracionado em bobinas.

## 3. Modelo de Memória de Cálculo (Elétrica)
```text
╔══════════════════════════════════════════════════════════════════╗
║        MEMÓRIA DE CÁLCULO — INSTALAÇÕES ELÉTRICAS               ║
╠══════════════════════════════════════════════════════════════════╣
║  AMBIENTE: [T-101-SAL]   CIRCUITO: [Circuito 03 - Tomadas]      ║
╠══════════════════════════════════════════════════════════════════╣
║  ELETRODUTO (PVC Flexível 25mm - 3/4"):                         ║
║    Teto: X,XX m | Descidas (3x): X,XX m                         ║
║    Subtotal: X,XX m + Perda 10% = X,XX m                        ║
║                                                                  ║
║  CONDUTORES (Cabo Flex 2,5mm² - Fase/Neutro/Terra):             ║
║    Trecho embutido: X,XX m × 3 = XX,XX m                        ║
║    Pontas (4 caixas × 0,5m × 3 cabos): 6,00 m                   ║
║    Ponta QDC (1,0m × 3 cabos): 3,00 m                           ║
║    Subtotal: XX,XX m + Perda 5% = XX,XX m (Por Cor)             ║
║                                                                  ║
║  CAIXAS E MÓDULOS:                                               ║
║    Caixa 4x2 PVC: 4 unid                                         ║
║    Tomada Dupla 10A: 4 unid                                      ║
╚══════════════════════════════════════════════════════════════════╝
```

## 4. Tabela Final de Compra (UCC)
O relatório final deve arredondar para cima usando a UCC. Se a soma do projeto exigir 112 metros de cabo flexível azul 2,5mm², a SC (Solicitação de Compra) final será de **2 Rolos de 100m** (200m).
