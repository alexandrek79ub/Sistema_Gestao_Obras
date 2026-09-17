# Extração de Evidências de Pranchas

O `LeitorPDFBase` agora percorre todas as páginas e expõe:

- `obter_texto_todas_paginas()` para leitura integral;
- `iterar_blocos()` com página e coordenadas;
- `extrair_evidencias()` produzindo `EvidenceRecord` conforme o contrato de dados.

Esta camada somente lê e registra evidências. Ela não calcula quantidades, não aplica perdas e não decide dimensões ausentes. OCR, tabelas estruturadas e validação geométrica permanecem etapas posteriores; blocos ambíguos devem receber revisão/RFI antes de alimentar o parser.
