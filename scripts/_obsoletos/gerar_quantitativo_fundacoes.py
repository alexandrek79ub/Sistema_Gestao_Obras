import os
import csv

dest_dir = r'c:\Users\Alexandre\Workspace\A11_SISTEMA_DE_GESTAO_OBRAS\projetos\OBRA_TMULT\02_ORCAMENTO_BASE_E_CONTRATOS'
os.makedirs(dest_dir, exist_ok=True)

# 1. WRITE CSV
csv_path = os.path.join(dest_dir, 'QUANTITATIVO_INFRAESTRUTURA_FUNDACOES.csv')
items = [
    {'eap': '1.1.1', 'item': 'Escavação Mecanizada/Manual para Cavas de Sapatas e Vigas Baldrames', 'unidade': 'm³', 'qtd_projeto': 86.40, 'perda_pct': 0.0, 'qtd_comercial_ucc': 86.40, 'unidade_ucc': 'm³', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-051/052'},
    {'eap': '1.1.2', 'item': 'Lastro de Concreto Magro e=5cm para Regularização do Fundo das Cavas', 'unidade': 'm²', 'qtd_projeto': 32.60, 'perda_pct': 5.0, 'qtd_comercial_ucc': 1.71, 'unidade_ucc': 'm³ usinado', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-052'},
    {'eap': '1.1.3', 'item': 'Concreto Armado C30 (Sapatas S1 a S24 e Vigas Baldrames VB1 a VB18)', 'unidade': 'm³', 'qtd_projeto': 43.40, 'perda_pct': 4.0, 'qtd_comercial_ucc': 45.00, 'unidade_ucc': 'm³ (caminhão 8m³)', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-051/054/059'},
    {'eap': '1.1.4', 'item': 'Fôrma de Compensado Resinado/Tábua para Sapatas e Vigas Baldrames', 'unidade': 'm²', 'qtd_projeto': 210.60, 'perda_pct': 10.0, 'qtd_comercial_ucc': 231.66, 'unidade_ucc': 'm²', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-051/054'},
    {'eap': '1.1.5.1', 'item': 'Aço CA-50 Ø 6.3mm (Estribos Baldrames)', 'unidade': 'kg', 'qtd_projeto': 114.40, 'perda_pct': 5.0, 'qtd_comercial_ucc': 41.00, 'unidade_ucc': 'barras de 12m (120.1kg)', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-054/057'},
    {'eap': '1.1.5.2', 'item': 'Aço CA-50 Ø 8.0mm (Armação Sapatas e Baldrames)', 'unidade': 'kg', 'qtd_projeto': 413.70, 'perda_pct': 5.0, 'qtd_comercial_ucc': 92.00, 'unidade_ucc': 'barras de 12m (434.4kg)', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-052/054/057'},
    {'eap': '1.1.5.3', 'item': 'Aço CA-50 Ø 12.5mm (Armação Longitudinal Baldrames)', 'unidade': 'kg', 'qtd_projeto': 263.20, 'perda_pct': 5.0, 'qtd_comercial_ucc': 24.00, 'unidade_ucc': 'barras de 12m (276.4kg)', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-054/057'},
    {'eap': '1.1.5.4', 'item': 'Aço CA-50 Ø 16.0mm (Reforços Baldrames VB114/VB115)', 'unidade': 'kg', 'qtd_projeto': 206.20, 'perda_pct': 5.0, 'qtd_comercial_ucc': 12.00, 'unidade_ucc': 'barras de 12m (216.5kg)', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-054/057'},
    {'eap': '1.1.6', 'item': 'Reaterro Mecanizado/Manual Compactado de Valas de Fundação', 'unidade': 'm³', 'qtd_projeto': 43.00, 'perda_pct': 0.0, 'qtd_comercial_ucc': 43.00, 'unidade_ucc': 'm³', 'ref_prancha': 'AÇU-3.DES-2.3100-11-EGS-051/052'}
]

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['eap', 'item', 'unidade', 'qtd_projeto', 'perda_pct', 'qtd_comercial_ucc', 'unidade_ucc', 'ref_prancha'])
    writer.writeheader()
    writer.writerows(items)

print('CSV criado com sucesso:', csv_path)

# 2. WRITE MARKDOWN
md_path = os.path.join(dest_dir, 'MEMORIA_CALCULO_INFRAESTRUTURA_FUNDACOES.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write('# 🏛️ Memória de Cálculo Auditável: Infraestrutura e Fundações\n\n')
    f.write('**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo\n')
    f.write('**Disciplina:** Engenharia de Custos / Estrutura e Infraestrutura\n')
    f.write('**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-11-EGS-051`, `EGS-052`, `EGS-053`, `EGS-054`, `EGS-057` e `EGS-059` (Rev A)\n')
    f.write('**Data da Auditoria:** 08/09/2026\n\n')
    f.write('---\n\n')
    f.write('## 📐 1. Resumo Executivo das Sapatas (32 Unidades)\n\n')
    f.write('| Tipo de Sapata | Quantidade | Dimensões (B x L x H) (cm) | Volume Unit (m³) | Volume Total Concreto (m³) | Área Fôrma (m²) |\n')
    f.write('| :--- | :---: | :---: | :---: | :---: | :---: |\n')
    f.write('| **SE1 a SE7** (Divisa/Esquina) | 6 | 70 x 70 x 50 | 0.245 | 1.47 | 8.40 |\n')
    f.write('| **S7, S8, S12..SE8** | 9 | 90 x 90 x 55 | 0.445 | 4.01 | 17.82 |\n')
    f.write('| **S1, S2, S6, S11..S24** | 11 | 100 x 100 x 60 | 0.600 | 6.60 | 26.40 |\n')
    f.write('| **S3, S4, S5, S9, S10, S23** | 6 | 110 x 110 x 60 | 0.726 | 4.36 | 15.84 |\n')
    f.write('| **TOTAL SAPATAS** | **32** | - | - | **24.80 m³** | **62.40 m²** |\n\n')
    f.write('---\n\n')
    f.write('## 🧱 2. Resumo Executivo das Vigas Baldrames (VB1 a VB18)\n\n')
    f.write('- **Volume Total de Concreto Armado C30:** `18.60 m³`\n')
    f.write('- **Área Total de Fôrma de Madeira:** `148.20 m²`\n\n')
    f.write('---\n\n')
    f.write('## 📊 3. Tabela Consolidada para EAP, Suprimentos (UCC) e Cronograma\n\n')
    f.write('| Código EAP | Descrição do Insumo / Serviço | Qtd Projeto | Perda (%) | Qtd Comercial UCC | Unidade UCC | Prancha Ref |\n')
    f.write('| :---: | :--- | :---: | :---: | :---: | :---: | :--- |\n')
    for it in items:
        f.write(f"| **{it['eap']}** | {it['item']} | {it['qtd_projeto']} {it['unidade']} | {it['perda_pct']}% | **{it['qtd_comercial_ucc']}** | `{it['unidade_ucc']}` | `{it['ref_prancha']}` |\n")
    f.write('\n---\n\n')
    f.write('## 🛒 4. Lista Consolidada de Pedido de Compras (UCC)\n\n')
    f.write('1. **Concreto Usinado C30 (Sapatas + Baldrames):** **`45 m³`** *(Pedir 6 caminhões betoneira de 8 m³ com fck 30 MPa e slump 12±2 cm)*\n')
    f.write('2. **Aço CA-50 Total:** **`1.047,4 kg`** *(1,05 toneladas)*:\n')
    f.write('   - Aço $\\varnothing$ 6.3mm: **41 barras de 12m** (120,1 kg)\n')
    f.write('   - Aço $\\varnothing$ 8.0mm: **92 barras de 12m** (434,4 kg)\n')
    f.write('   - Aço $\\varnothing$ 12.5mm: **24 barras de 12m** (276,4 kg)\n')
    f.write('   - Aço $\\varnothing$ 16.0mm: **12 barras de 12m** (216,5 kg)\n')
    f.write('3. **Fôrmas de Madeira (Compensado Resinado 17mm):** **`232 m²`** *(Pedir 78 chapas de 1,10m x 2,20m)*\n')
    f.write('4. **Arame Recozido Nº 18:** **`25 kg`** *(Consumo médio de 20 a 25g por kg de aço)*\n\n')
    f.write('*Data da última auditoria:* 08/09/2026\n')

print('Markdown criado com sucesso:', md_path)
