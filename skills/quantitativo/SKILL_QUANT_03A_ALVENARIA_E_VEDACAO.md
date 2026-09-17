# SKILL QUANT 03A — ALVENARIA E VEDAÇÃO

Parte do módulo de Arquitetura. Esta skill define somente o levantamento físico líquido de serviços comprovados nas pranchas.

## Limites obrigatórios

- Não aplicar perdas, empolamento, arredondamento comercial ou coeficientes de consumo.
- Não calcular blocos comerciais, cimento, cal, areia, graute, telas, arames, PU, embalagens ou UCC.
- Esses dados pertencem à composição/BOM posterior e não podem gerar linhas em `itens_quantitativo`.
- Se faltar dimensão, paginação, especificação ou revisão de projeto, registrar `PENDENTE_RFI`; nunca estimar.

## 1. Alvenaria de vedação

Para cada parede identificada na prancha:

```text
A_bruta = comprimento_do_trecho × altura_do_trecho
A_descontos = Σ descontos de vãos conforme critério do projeto
A_líquida = A_bruta − A_descontos
```

Registrar separadamente corpo de parede, platibanda, mureta, boneca, verga, contraverga e encunhamento quando forem serviços explicitamente desenhados ou especificados.

O desconto de vãos deve seguir a regra indicada no projeto e na NBR 12721 adotada para a obra. Sem regra aplicável ou com conflito entre pranchas, abrir RFI.

## 2. Revestimentos de parede

```text
A_revestida = Σ áreas de faces efetivamente revestidas
A_líquida = A_revestida − Σ vãos e áreas não revestidas
```

Quantificar separadamente chapisco, emboço, reboco, revestimento cerâmico, pintura ou outro serviço quando cada camada estiver especificada na documentação.

## 3. Pisos e áreas horizontais

```text
A_piso = área geométrica do ambiente
A_líquida = A_piso − áreas sem revestimento indicadas na prancha
```

Medir contrapiso, impermeabilização, revestimento e rodapé como serviços distintos. Não converter a área líquida em caixas, peças comerciais ou consumo de argamassa.

## 4. Tetos, forros e drywall

```text
A_teto = comprimento × largura (ou decomposição geométrica da planta)
A_líquida = A_teto − aberturas e áreas não executadas indicadas no projeto
```

Para paredes ou forros de drywall, quantificar a área executiva líquida e separar cada serviço especificado. Chapas, perfis, parafusos, fitas, massa e perdas ficam fora do quantitativo físico.

## 5. Evidência mínima por item

Cada resultado deve preservar:

- obra, prancha, revisão e página;
- ambiente ou elemento;
- dimensões transcritas da evidência;
- expressão literal do cálculo;
- unidade física (`m²`, `m`, `m³` ou `un`);
- status `VALIDADO`, `PENDENTE_RFI` ou `BLOQUEADO`.

## 6. Checklist de encerramento

- [ ] Todas as paredes e revestimentos foram confrontados com plantas, cortes e elevações.
- [ ] Vãos, shafts, nichos e áreas não revestidas foram tratados conforme projeto.
- [ ] Nenhuma perda, SKU, consumo, embalagem ou UCC foi aplicada.
- [ ] Cada linha possui memória de cálculo e evidência rastreável.
- [ ] Ausências ou conflitos foram convertidos em RFI.
