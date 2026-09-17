# SKILL QUANT 03B — ACABAMENTOS, IMPERMEABILIZAÇÃO E ESQUADRIAS

> Parte de: `SKILL_QUANT_03_ARQUITETURA.md`
> Dependência: `SKILL_QUANTIFICACAO_MASTER.md`

Esta skill mede somente quantidades físicas líquidas comprovadas no projeto. Perdas, recortes comerciais, sobreposições de compra, consumo de produto, kits, ferragens de consumo e embalagens pertencem à CPU/BOM posterior.

## 1. Impermeabilização

### 1.1 Áreas molhadas, sacadas e varandas

```text
A_piso = comprimento × largura
A_arremates = Σ (extensão_do_arremate × altura_especificada)
A_impermeabilização = A_piso + A_arremates + faces especificadas
```

### 1.2 Box, laje exposta, terraço e reservatório

```text
A_box = área_de_piso + Σ áreas de paredes impermeabilizadas
A_laje_exposta = área_horizontal + Σ arremates especificados
A_reservatório = Σ faces internas especificadas em projeto
```

Medir somente as faces, alturas de rodapé e arremates indicados no detalhe. Não adicionar sobreposição de manta, perdas ou área de compra.

## 2. Esquadrias, vidros, vergas e contravergas

### 2.1 Quadro mestre e alocação

Cada código de esquadria deve ter um registro de tipo, material, abertura, largura, altura, acabamento, ambiente e quantidade de ocorrências. O quadro mestre deve ser confrontado com plantas, cortes e elevações.

```text
Qtd_total = Σ ocorrências confirmadas do código
A_vão = largura × altura × Qtd_total
A_pintura = área_da_face × número_de_faces_especificadas × Qtd_total
```

### 2.2 Verga, contraverga, peitoril e soleira

```text
L_verga = Σ (largura_do_vão + extensões_de_apoio_especificadas)
L_contraverga = Σ (largura_da_janela + extensões_de_apoio_especificadas)
L_peitoril = Σ larguras de janelas especificadas
L_soleira = Σ larguras de portas especificadas
```

Verga e contraverga só devem ser levantadas quando forem elementos ou serviços explicitamente desenhados/contratados; não derivar dimensão padrão.

## 3. Rodapés, baguetes e arremates lineares

```text
L_rodapé = perímetro_revestido − Σ vãos sem rodapé
L_baguete_box = extensão indicada no detalhe do box
L_arremate = Σ trechos especificados
```

## 4. Louças, metais, cubas e acessórios especificados

Contar cada conjunto pela legenda e pelo ambiente: bacias, lavatórios, tanques, cubas, torneiras, misturadores, duchas, válvulas, sifões e acabamentos. Registrar código de especificação, unidade e local. Não derivar acessórios que não estejam na legenda ou memorial.

```text
Qtd_total_item = Σ ocorrências confirmadas por ambiente e pavimento
```

## 5. Bancadas, tampos, peitoris e divisórias em pedra

```text
A_peça = comprimento × largura
A_total_por_código = Σ áreas das peças confirmadas
L_borda = Σ comprimentos de bordas especificadas
```

Para cada peça registrar código, material, espessura, acabamento, recortes e apoios somente se estiverem indicados na documentação técnica. Recorte de cuba não reduz área sem critério contratual explícito.

## 6. Evidência e decisão

| Pedido | Método |
|---|---|
| Impermeabilização de banheiro | Piso + arremates + paredes indicadas no detalhe |
| Esquadrias | Quadro mestre + alocação por ambiente + conferência em cortes |
| Rodapé/soleira | Trechos executados menos vãos sem acabamento |
| Louças e metais | Contagem por legenda e ambiente |
| Bancadas | Peça a peça, por código de especificação |

Checklist:

- [ ] Áreas de impermeabilização não incluem perdas ou sobreposição comercial.
- [ ] Esquadrias foram confrontadas com quadro, planta, corte e elevação.
- [ ] Vergas, contravergas e arremates têm detalhe ou especificação.
- [ ] Louças, metais e bancadas possuem contagem por ambiente.
- [ ] Cada item possui prancha, revisão, expressão, unidade e status.
- [ ] Nenhuma linha contém consumo, UCC, embalagem ou insumo avulso.
