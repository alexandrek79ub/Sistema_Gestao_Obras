# 🚀 Guia de Inicialização de Nova Obra (Passo a Passo)

Esta pasta `_TEMPLATE_OBRA_NOVA/` é o modelo padrão, limpo e agnóstico de empreendimento do **PMO Virtual A11**.
Para iniciar o planejamento e gestão de uma nova obra de forma 100% independente e sem contaminação de código, siga o roteiro abaixo:

---

## 1. Criar a Pasta da Nova Obra
Duplique esta pasta inteira atribuindo o nome do seu projeto, por exemplo:
```powershell
Copy-Item -Path "projetos\_TEMPLATE_OBRA_NOVA" -Destination "projetos\OBRA_NOVA" -Recurse
```

---

## 2. Configurar os Parâmetros Gerais
Abra o arquivo `projetos/OBRA_NOVA/config_obra.json` e ajuste os dados básicos:
- **`nome_obra`**: Nome completo do empreendimento.
- **`sigla_obra`**: Sigla identificadora (ex: `ALPHA`, `PETROBRAS`, `GALPAO01`).
- **`area_construida_m2`**: Área total construída.
- **`prazo_meses`**: Prazo contratual em meses (ex: 4, 6, 12, etc.).
- **`bdi_servico_pct`** e **`bdi_equipamento_pct`**: Taxas de BDI aplicáveis.
- **`administracao_local`**: Itens de gestão de canteiro, equipe, vivência e módulos.

---

## 3. Alimentar os Quantitativos e Composições
1. **Engenharia e Projetos (`01_ENGENHARIA_E_PROJETOS/`):**
   - Deposite os memoriais descritivos, pranchas DWG/PDF e caderno de encargos.
2. **Orçamento e Mapeamento (`02_ORCAMENTO_BASE_E_CONTRATOS/`):**
   - Atualize `mapeamento_sinapi.csv` ou gere a planilha base de quantitativos.
   - Ajuste os centros de custo em `estrutura_centros_custo.json`.
3. **Catálogos de Suprimentos (`05_SUPRIMENTOS_E_FINANCEIRO/`):**
   - Ajuste os catálogos de materiais (`catalogo_materiais_rc.json`) e locações (`catalogo_equipamentos_re.json`).

---

## 4. Executar a Suíte Universal de Scripts
Abra o terminal na raiz do workspace e execute a sequência com a flag `--obra OBRA_NOVA`:

```bash
# 1. Precificar o Orçamento Base com BDI e Encargos
python scripts/precificar_obra.py --obra OBRA_NOVA

# 2. Gerar o Plano de Contas e Centros de Custo
python scripts/gerar_plano_centros_custo.py --obra OBRA_NOVA

# 3. Gerar o Cronograma Físico-Financeiro, Baseline, Excel, MS Project XML e Dashboard HTML
python scripts/gerar_cronograma.py --obra OBRA_NOVA

# 3.1 Gerar a Programação de Curto Prazo em Lotes Takt (Esteira Lean em Zonas Equalizadas)
python scripts/gerar_programacao_curto_prazo_takt.py --obra OBRA_NOVA

# 4. Gerar o Pacote Completo de Suprimentos (RCs, REs, Matriz de Subcontratos)
python scripts/gerar_cronograma_suprimentos.py --obra OBRA_NOVA

# 5. Gerar o Procurement Tracker Operacional de Compras
python scripts/gerar_tracker_suprimentos.py --obra OBRA_NOVA

# 6. Gerar a Modelagem de Fluxo de Caixa, Desembolso e Capital de Giro (3 Cenários)
python scripts/gerar_fluxo_caixa.py --obra OBRA_NOVA

# 7. Gerar os Contratos Executivos com Empreiteiros e Índice Mestre
python scripts/gerar_contratos_empreiteiros.py --obra OBRA_NOVA

# 8. Gerar os Contratos de Locação de Equipamentos e Planilha de Gestão
python scripts/gerar_contratos_locacao.py --obra OBRA_NOVA

# 9. Gerar a Planilha Master de Medição Quinzenal de Empreiteiros
python scripts/gerar_planilha_medicao.py --obra OBRA_NOVA

# 10. Gerar o Dossiê Executivo (Histogramas de MO/Equipamentos e Curva ABC Dupla)
python scripts/gerar_dossie_contratacao.py --obra OBRA_NOVA

# 11. Gerar o Sistema de RDO e Painel de Produção Diária (04_PRODUCAO_E_AVANCO)
python scripts/gerar_rdo.py --obra OBRA_NOVA

# 12. Gerar o Caderno de FVSs Bloqueantes e Matriz de Qualidade (04_PRODUCAO_E_AVANCO)
python scripts/gerar_fvs_bloqueantes.py --obra OBRA_NOVA

# 13. Gerar o Acompanhamento de Avanço Físico e Curva S Real EVM/SPI (04_PRODUCAO_E_AVANCO)
python scripts/gerar_tracker_avanco_fisico.py --obra OBRA_NOVA

# 14. Gerar o Painel de Compliance SST, Controle de ASOs e NRs (06_SST_E_RH)
python scripts/gerar_compliance_sst.py --obra OBRA_NOVA

# 15. Gerar a Estrutura de DataBook, As-Built e Encerramento Closeout (07_DATABOOK_E_ASBUILT)
python scripts/gerar_estrutura_databook.py --obra OBRA_NOVA

# 16. Ingerir Coleta Digital de Campo e Mensagens de WhatsApp (04_PRODUCAO_E_AVANCO)
python scripts/processar_coleta_campo.py --obra OBRA_NOVA --texto "RDO 29/09/2026: 8 pedreiros, 4 serventes..."
```

---

## 5. Garantia de Isolamento
- Nenhum script em `scripts/` contém dados fixos ou códigos de obra hardcoded.
- Todas as saídas (CSVs, Excels, XMLs, Dashboards HTML e Relatórios MD) são geradas exclusivamente dentro da pasta da sua obra em `projetos/OBRA_NOVA/`.
- Diferentes obras podem ser executadas em paralelo ou sequencialmente sem contaminação cruzada.

---

## 6. Visualizar no Cockpit Web e Coleta Mobile 4.0
Após rodar os scripts da sua obra, inicie a aplicação web:
```bash
cd apresentacao_comercial
npm run dev
```
1. Acesse [`http://localhost:3000/dashboard`](http://localhost:3000/dashboard) e selecione `OBRA_NOVA` no seletor do cabeçalho.
2. Navegue pelas **8 visões integradas**: EVM, Orçamento Base, Linha de Balanço, RDO Diário, Qualidade e FVS, Fluxo de Caixa, Compliance SST e DataBook/Closeout.
3. Para apontamentos em tempo real de canteiro, acesse [`http://localhost:3000/campo`](http://localhost:3000/campo) do seu smartphone ou emulador.
