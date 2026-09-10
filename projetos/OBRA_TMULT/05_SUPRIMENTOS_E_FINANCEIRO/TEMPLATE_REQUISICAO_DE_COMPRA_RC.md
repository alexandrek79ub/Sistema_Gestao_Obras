# 📋 MODELO PADRÃO: REQUISIÇÃO DE COMPRA (RC)
> **Origem:** Engenharia de Obra (Campo) ➔ **Destino:** Setor de Suprimentos (Compras)  
> **Referência Normativa:** POP 05, Diretrizes de Governança A11 e Plano de Centros de Custo

---

### 1. DADOS DE CABEÇALHO & CONTROLE

| Campo | Preenchimento Obrigatório |
| :--- | :--- |
| **Número da RC:** | `RC-___ / 2026` |
| **Obra / Contrato:** | `OBRA_TMULT — Edifício Administrativo (Porto do Açu)` |
| **Data de Emissão (Obra):** | `DD/MM/AAAA` |
| **Data Necessária no Canteiro:** | **`DD/MM/AAAA`** *(Respeitar Lead Time mínimo do POP 05)* |
| **Disciplina / EAP Vinculada:** | `Ex: Infraestrutura — EAP 1.1.4 e 1.1.8` |
| **Centro de Custo (CC):** | **`Ex: CC-200 (Infraestrutura) / Analítico: CC-203 e CC-206`** |
| **Local Exato de Aplicação (CIA):**| `Ex: Fundações — Sapatas Isoladas S1 a S24` |
| **Engenheiro Solicitante:** | `Nome e CREA` |

---

### 2. ESPECIFICAÇÃO TÉCNICA E QUANTIDADES EM UCC (Unidade Comercial de Compra)

> ⚠️ **Regra Inviolável:** A Engenharia levanta em unidade de projeto, mas converte obrigatoriamente para a embalagem comercial da indústria (barras de 12m, sacos de 50kg, chapas inteiras, m³ dosado em central). Toda linha carrega o Centro de Custo analítico para apropriação contábil.

| Item | Centro de Custo (CC) | Descrição Técnica Completa e Normativa | Qtd Projeto | Und Proj | % Perda | Qtd Compra | Und UCC | Prancha Executiva / Ref. |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 01 | `CC-___` | [Especificação exata: marca de ref., bitola, classe] | | | | | | |
| 02 | `CC-___` | | | | | | | |
| 03 | `CC-___` | | | | | | | |

---

### 3. REQUISITOS TÉCNICOS DE RECEBIMENTO NO CANTEIRO (POP 06)
- **Ensaios Obrigatórios na Entrega:** (Ex: Slump test para concreto / Laudo de ensaio de tração para aço / Selo FSC para madeira);
- **Condição de Frete Exigida:** CIF Canteiro com descarga mecânica/manual por conta do fornecedor;
- **Horário Permitido para Descarga:** Segunda a Sexta, das 07h30 às 16h30 (Portão Portuário TMULT).

---

### 4. CARIMBOS DE DESPACHO E PROTOCOLO

| Instância | Responsável | Data | Parecer / Assinatura |
| :--- | :--- | :---: | :--- |
| **Emissão de Campo:** | Eng. Residente | DD/MM/AAAA | [ ] Aprovado para Cotação |
| **Recebimento Suprimentos:** | Comprador | DD/MM/AAAA | [ ] Aberto no Pipeline de Compras |
| **Status Atual no Tracker:** | `[ ] 1. PENDENTE` `[ ] 2. EM COTAÇÃO` `[ ] 3. PROPOSTAS RECEBIDAS` |
