# Motor de Quantitativos

O SQLite central em `data/pmo_virtual.sqlite` é a fonte oficial do quantitativo e do orçamento.
CSV e Markdown são somente exportações derivadas e nunca devem ser editados como fonte de dados.

## Importação inicial para o banco

```text
python scripts/gerador_orcamento_mestre.py scripts/template_dados_orcamento.json --db data/pmo_virtual.sqlite
```

O comando calcula as expressões, importa o quantitativo e o orçamento e exporta os arquivos da
obra. Se já houver itens no SQLite, a reimportação exige `--substituir`, pois ela substitui
alterações posteriores feitas diretamente na fonte oficial.

## API local

```text
python scripts/api_pmo.py --db data/pmo_virtual.sqlite --port 8787 --api-key "chave-local" --usuario "engenheiro-web"
```

- `GET /api/quantitativos?obra_id={obra_id}`
- `PATCH /api/quantitativo/{obra_id}/{item_id}`

Todas as rotas exigem o header `X-PMO-API-Key`. O PATCH exige `justificativa`, `alteracoes` e
`versao_esperada`. A operação registra auditoria, recalcula o orçamento e atualiza as exportações
derivadas; antes de editar, cria um snapshot SQLite em `data/backups/` (ou em `--backup-dir`).
Esta API é local (`127.0.0.1`), não um serviço exposto à internet.
