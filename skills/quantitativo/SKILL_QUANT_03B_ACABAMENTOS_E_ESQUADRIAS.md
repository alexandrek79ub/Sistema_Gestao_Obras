# SKILL QUANT 03B — ACABAMENTOS E ESQUADRIAS

Esta skill define somente quantidades físicas líquidas de acabamentos, impermeabilização, esquadrias, louças, metais e bancadas comprovados no projeto.

## Limites obrigatórios

- Não aplicar perdas, recortes, sobreposição, consumo de produto ou arredondamento comercial.
- Não calcular mantas de compra, primer, argamassa, rejunte, tinta, cola, espaçadores, ferragens de consumo ou embalagens.
- Materiais comerciais e composições pertencem à etapa posterior de CPU/BOM.
- Informação ausente ou divergente exige `PENDENTE_RFI`; nunca usar dimensões de exemplo.

## 1. Impermeabilização

```text
A_piso = comprimento × largura
A_arremates = extensão especificada × altura especificada
A_líquida = A_piso + A_arremates + demais faces comprovadas
```

Para boxes, reservatórios, lajes e terraços, medir somente as faces indicadas em detalhe ou memorial do projeto. Não adicionar percentual de sobreposição ou perda.

## 2. Esquadrias e vidros

Para cada código de esquadria da prancha:

```text
Qtd_total = soma das ocorrências identificadas
A_vão = largura × altura × Qtd_total
```

Registrar tipo, material, abertura, dimensões, ambiente e quantidade. Verga, contraverga, peitoril e soleira somente entram quando forem serviços especificados e devem ser medidos separadamente.

## 3. Rodapés, peitoris e soleiras

```text
Rodapé_líquido = perímetro executado − vãos explicitamente não revestidos
Peitoril = Σ larguras de janelas especificadas
Soleira = Σ larguras de portas especificadas
```

## 4. Louças, metais e cubas

Contar cada conjunto conforme legenda, quadro de acabamentos e ambientes da prancha. Registrar a unidade física (`un` ou `cj`) e o código de especificação; não derivar acessórios de compra.

## 5. Bancadas, tampos e divisórias

```text
A_peça = comprimento × largura
A_total = Σ áreas das peças comprovadas
```

Espessura, material, acabamento, recortes e apoios só devem ser registrados quando estiverem explicitamente especificados.

## 6. Evidência e checklist

- [ ] Quadro de esquadrias confrontado com plantas, cortes e elevações.
- [ ] Áreas de impermeabilização e revestimento medidas sem perdas ou sobreposição.
- [ ] Louças, metais, bancadas, rodapés, peitoris e soleiras contados por ambiente.
- [ ] Cada linha possui prancha, revisão, expressão, unidade e status.
- [ ] Nenhuma linha contém insumo, consumo, UCC ou embalagem.
- [ ] Ausências ou conflitos foram convertidos em RFI.
