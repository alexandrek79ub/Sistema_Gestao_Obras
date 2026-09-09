import json
import os

gerador_file = r"c:\Users\Alexandre\Workspace\A11_SISTEMA_DE_GESTAO_OBRAS\scripts\gerador_orcamento_mestre.py"

with open(gerador_file, "r", encoding="utf-8") as f:
    content = f.read()

old_imperm = """- **Arranques de Pilares (24 un h=0,35m enterrados):** `24 × 1,20m × 0,35m = 10,29 m²`
- **Área Total de Impermeabilização:** `35,11 + 112,35 + 25,61 + 10,29 =` **`183,36 m²`**
- **Quantidade Comercial UCC (Com Perda 10% de porosidade):** `183,36 m² × 1,10 = 201,70 m²` → **12 galões de 18L** (`216,00 m²`)."""

new_imperm = """- **Arranques de Pilares P1-P24 (Geometria Líquida c/ Desconto de Nós):**
  - Área bruta lateral (24 un h=0,65m): `24 × (4 × 0,30m) × 0,65m = 18,72 m²`
  - Desconto das faces de conexão com as vigas: `44 vãos livres × 2 extremidades = 88 conexões`.
  - Área descontada: `88 × (0,25m larg × 0,40m alt) = 8,80 m²`
  - Área Líquida dos Arranques = `18,72 - 8,80 = 9,92 m²`
- **Área Total de Impermeabilização:** `35,11 (Topo VB) + 112,35 (Lat VB) + 25,61 (Topo Sap) + 9,92 (Arranques) =` **`182,99 m²`**
- **Quantidade Comercial UCC (Com Perda 10% de porosidade):** `182,99 m² × 1,10 = 201,29 m²` → **12 galões de 18L** (`216,00 m²`)."""

content = content.replace(old_imperm, new_imperm)

with open(gerador_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Patch arranques concluded successfully.")
