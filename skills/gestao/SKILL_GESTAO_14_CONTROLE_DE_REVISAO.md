# 📐 SKILL GESTÃO 14: Controle de Revisão de Projeto e Documento

Resolve um risco silencioso: quantitativo, medição e execução sendo feitos em cima de uma **versão
desatualizada** do projeto. É pré-requisito de confiança para tudo que a `SKILL_QUANTIFICACAO_MASTER`
já faz bem — de nada adianta um quantitativo perfeito se foi extraído da revisão errada do PDF.

---

## 1. Registro Mínimo por Documento de Projeto

| Campo | Descrição |
|---|---|
| Documento | Nome/identificação da prancha ou arquivo |
| Revisão atual | Ex.: "Rev. 03" |
| Data da revisão | |
| O que mudou desde a revisão anterior | Resumo objetivo — não é preciso reproduzir o desenho, mas registrar **quais elementos** mudaram |
| Quantitativo/CIA impactado | Se a mudança afeta um item já quantificado, isso precisa ser sinalizado |

---

## 2. Checagem Obrigatória Antes de Quantificar

Antes de rodar a `SKILL_QUANTIFICACAO_MASTER` sobre um PDF/DXF, o agente deve confirmar:

1. **Este é o arquivo da revisão mais recente?** Se o nome do arquivo ou a data não deixam claro,
   perguntar antes de prosseguir — nunca assumir que o arquivo mais recente na pasta é
   necessariamente a revisão vigente.
2. **Já existe um quantitativo anterior feito numa revisão diferente deste mesmo documento?** Se
   sim, a IA deve comparar as duas revisões e apontar **o que mudou no quantitativo**, não
   simplesmente substituir o número antigo pelo novo sem explicar a diferença.

---

## 3. Sinalização de Impacto em Cascata

Quando uma revisão de projeto muda uma quantidade já orçada/comprada:

- Verificar se já existe **pedido de compra** baseado na quantidade antiga
  (`SKILL_QUANTIFICACAO_PEDIDO_DE_COMPRA`) — se sim, sinalizar que o pedido pode precisar de
  ajuste.
- Verificar se a mudança justifica um **aditivo** (`SKILL_GESTAO_10`) — mudança de projeto que
  aumenta escopo é candidata natural a aditivo, e a IA deve apontar isso proativamente, não
  esperar ser perguntada.

---

## ⚠️ 4. Regras de Ouro

1. Nunca quantificar a partir de um arquivo sem confirmar que é a revisão vigente.
2. Mudança de revisão que impacta quantitativo já usado em compra ou medição gera alerta
   obrigatório — nunca é uma atualização silenciosa de número.
3. O histórico de revisões é mantido, não sobrescrito — sempre deve ser possível responder "o que
   mudou entre a Rev. 02 e a Rev. 03, e isso afetou o quê no orçamento".

---
*Trabalha junto com `SKILL_QUANTIFICACAO_MASTER.md` (fonte do quantitativo) e
`SKILL_GESTAO_10_CONTRATOS_EMPREITEIROS.md` (mudança de projeto como gatilho de aditivo).*
