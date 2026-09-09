import os
import csv

def main():
    base_dir = r"c:\Users\Alexandre\Workspace\A11_SISTEMA_DE_GESTAO_OBRAS\projetos\OBRA_TMULT\02_ORCAMENTO_BASE_E_CONTRATOS"
    os.makedirs(base_dir, exist_ok=True)

    csv_path = os.path.join(base_dir, "QUANTITATIVO_ARQUITETURA.csv")
    md_path = os.path.join(base_dir, "MEMORIA_CALCULO_ARQUITETURA.md")

    # CSV Data
    rows = [
        ["Código EAP", "Item / Descricao", "Disciplina", "Qtd Projeto", "Unidade Proj", "Perda (%)", "Qtd Comercial UCC", "Unidade UCC", "Prancha Referencia"],
        
        # Alvenaria e Revestimentos de Parede
        ["2.1.1", "Alvenaria de Vedação Bloco Concreto 14x19x39cm", "Arquitetura", "1061.44", "m²", "5.0", "13931", "blocos (1114.5 m²)", "AÇU-3.DES-2.3100-15-EGS-015/018"],
        ["2.1.2", "Chapisco Traço 1:3 e=5mm em Paredes", "Arquitetura", "2122.88", "m²", "5.0", "2229.02", "m² (75 sacos cimento)", "AÇU-3.DES-2.3100-15-EGS-015/016"],
        ["2.1.3", "Emboço/Reboco Paulista e=20mm", "Arquitetura", "2122.88", "m²", "5.0", "2229.02", "m² (446 sacos argamassa)", "AÇU-3.DES-2.3100-15-EGS-015/016"],
        ["2.1.4", "Contrapiso de Regularização e=3cm", "Arquitetura", "368.40", "m²", "5.0", "386.82", "m² (11.6 m³ argamassa)", "AÇU-3.DES-2.3100-15-EGS-015/018"],
        ["2.1.5", "Piso Porcelanato 60x60cm Retificado", "Arquitetura", "368.40", "m²", "10.0", "281", "caixas (405.2 m²)", "AÇU-3.DES-2.3100-15-EGS-015/016"],
        ["2.1.6", "Rodapé Porcelanato h=10cm", "Arquitetura", "384.20", "m", "10.0", "422.62", "m", "AÇU-3.DES-2.3100-15-EGS-015/018"],
        ["2.1.7", "Pintura Látex Acrílica 3 Demãos (Paredes + Tetos)", "Arquitetura", "2491.28", "m²", "5.0", "36", "latas 18L (2615.8 m²)", "AÇU-3.DES-2.3100-15-EGS-015/019"],
        ["2.1.8", "Esquadrias de Madeira/Alumínio (Portas P1-P5)", "Arquitetura", "24.0", "unid", "0.0", "24", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-018"],
        ["2.1.9", "Esquadrias de Alumínio Vidro (Janelas J1-J4)", "Arquitetura", "18.0", "unid", "0.0", "18", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-018"],
        ["2.1.10", "Impermeabilização Polimérica Sanitários/Copa", "Arquitetura", "84.20", "m²", "10.0", "92.62", "m² (19 caixas 18kg)", "AÇU-3.DES-2.3100-15-EGS-015/016"],
        
        # COBERTURA E PLATIBANDA DETALHADA
        ["2.2.1", "Telha Termoacústica Trapezoidal (Sandwich 30mm EPS)", "Cobertura", "381.29", "m²", "10.0", "419.42", "m² (70 telhas de 6m)", "AÇU-3.DES-2.3100-15-EGS-017"],
        ["2.2.2", "Terças Metálicas Perfil U Enrijecido 100x40x2,25mm", "Cobertura", "156.00", "m", "5.0", "28", "barras de 6m (573.3 kg)", "AÇU-3.DES-2.3100-15-EGS-017"],
        ["2.2.3", "Muretas Escalonadas de Apoio no Entreforro (Bloco 9x19x39cm)", "Cobertura", "45.24", "m²", "5.0", "594", "blocos 9x19x39cm", "AÇU-3.DES-2.3100-15-EGS-017"],
        ["2.2.4", "Calha em Chapa Galvanizada nº 24 (Dev 80cm)", "Cobertura", "52.00", "m", "5.0", "54.60", "m (19 peças de 3m)", "AÇU-3.DES-2.3100-15-EGS-017"],
        ["2.2.5", "Rufo e Pingadeira Metálica de Platibanda (Dev 40cm)", "Cobertura", "82.00", "m", "5.0", "86.10", "m (29 peças de 3m)", "AÇU-3.DES-2.3100-15-EGS-017"],
        ["2.2.6", "Impermeabilização Manta Asfáltica 4mm em Calhas", "Cobertura", "62.00", "m²", "15.0", "8", "rolos de 10m² (71.3 m²)", "AÇU-3.DES-2.3100-15-EGS-017/019"],
        ["2.2.7", "Ralo Hemisférico Tipo Abacaxi Inox Ø150mm para Calhas", "Cobertura", "8.0", "unid", "0.0", "8", "unidades", "AÇU-3.DES-2.3100-15-EGS-015/017"],
        
        # PLATIBANDA - ALVENARIA E REVESTIMENTO INTERNO/EXTERNO
        ["2.2.8", "Alvenaria de Platibanda Bloco Concreto 14x19x39cm (h=0,39m sobre viga invertida)", "Cobertura", "31.98", "m²", "5.0", "420", "blocos 14x19x39cm", "AÇU-3.DES-2.3100-15-EGS-017"],
        ["2.2.9", "Chapisco e Emboço/Reboco e=20mm Face Interna da Platibanda", "Cobertura", "74.62", "m²", "5.0", "78.35", "m² (16 sacos argamassa)", "AÇU-3.DES-2.3100-15-EGS-017"],
        ["2.2.10", "Pintura Acrílica Impermeável 3 Demãos Face Interna da Platibanda", "Cobertura", "74.62", "m²", "5.0", "2", "latas 18L (78.35 m²)", "AÇU-3.DES-2.3100-15-EGS-017/019"]
    ]

    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(rows)

    # Markdown Content
    md_content = """# 🏛️ Memória de Cálculo Auditável: Arquitetura, Vedações, Cobertura & Platibanda

**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo  
**Disciplina:** Engenharia de Custos / Arquitetura, Cobertura, Platibanda & Drenagem Pluvial  
**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-15-EGS-015`, `EGS-016`, `EGS-017` (Detalhe da Platibanda/Viga Invertida), `EGS-018` e `EGS-019`  
**Data da Auditoria:** 08/09/2026  

---

## 🧮 1. Fórmulas Matemáticas e Regras de Engenharia Utilizadas

### 1.1 Área Bruta e Líquida de Alvenaria de Vedação
> **Fórmula:** `A_liquida = (Perímetro_total × H_livre) - Σ A_esquadrias - Σ (b_pilar × H_livre)`
- **Perímetro Acumulado de Paredes:** `418,00 m`.
- **Pé-direito livre (H_livre):** `2,98 m`.
- **Desconto de Vãos e Pilares:** `184,20 m²`.
- **Área Líquida de Alvenaria:** `1.061,44 m²` ➔ **13.931 blocos 14x19x39cm**.

### 1.2 Platibanda em Alvenaria e Revestimentos (Regra da Viga Invertida)
> **Fórmula Alvenaria Platibanda:** `H_alvenaria = H_platibanda_total (0,91m) - h_viga_invertida (0,52m) = 0,39 m` (2 fiadas)  
> **Área Alvenaria:** `82,00 m × 0,39 m = 31,98 m²` ➔ **420 blocos 14x19x39cm**  
> **Fórmula Revestimento/Pintura Interna:** `A_revest_int = P_perímetro (82,00m) × H_total (0,91m) = 74,62 m²`
- **Chapisco + Emboço/Reboco e=20mm (Face Interna Platibanda):** `74,62 m²` (Com perda 5%: **78,35 m²** ➔ **16 sacos de argamassa 20kg**).
- **Pintura Acrílica Impermeável (Face Interna Platibanda):** `74,62 m²` (Com perda 5%: **78,35 m²** ➔ **2 latas de 18L**).
- **Face Externa da Platibanda:** Quantificada integradamente no revestimento/pintura da fachada geral.

---

## 📐 2. Detalhamento por Elemento de Arquitetura, Cobertura e Platibanda

### 2.1 Alvenaria e Revestimentos (Pranchas EGS-015 e EGS-018)
- **Área Bruta de Paredes:** `418,00 m × 2,98 m = 1.245,64 m²`
- **Desconto de Portas/Janelas (112,60 m²) + Pilares embutidos (71,60 m²):** `184,20 m²`
- **Área Líquida de Alvenaria:** `1.061,44 m²` ➔ **13.931 blocos**

### 2.2 Platibanda e Estrutura de Cobertura (Prancha EGS-017)
- **Alvenaria de Platibanda (Complemento 2 fiadas h=0,39m):** `31,98 m²` ➔ **420 blocos 14x19x39cm**.
- **Emboço e Pintura Acrílica Interna da Platibanda:** `74,62 m²`.
- **Telhado Termoacústico:** `381,29 m²` de cobertura inclinada 15° (70 telhas termoacústicas de 6,00m x 1,00m).
- **Terças Metálicas U 100x40x2,25mm:** `156 m` de perfis (28 barras de 6m).
- **Muretas de Apoio no Entreforro:** `45,24 m²` de alvenaria em bloco 9x19x39cm (594 blocos).
- **Drenagem e Impermeabilização de Calhas:** `52m` de calha galvanizada dev 80cm, `86,1m` de rufos/pingadeiras dev 40cm, `62m²` de manta asfáltica 4mm, `8 ralos abacaxi Ø150mm` e `110m` de condutores PVC Pluvial Ø150mm.

---

## 📊 3. Tabela Consolidada para EAP e Pedido de Compras (UCC)

| Código EAP | Descrição do Insumo / Serviço | Qtd Projeto | Perda (%) | Qtd Comercial UCC | Unidade UCC | Prancha Ref |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **2.1.1** | Alvenaria de Vedação Bloco 14x19x39cm | 1061,44 m² | 5,0% | **13.931** | `blocos` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **2.1.2** | Chapisco Traço 1:3 e=5mm | 2122,88 m² | 5,0% | **2.229,02** | `m² (75 sacos)` | `AÇU-3.DES-2.3100-15-EGS-016` |
| **2.1.3** | Emboço/Reboco Paulista e=20mm | 2122,88 m² | 5,0% | **2.229,02** | `m² (446 sacos)` | `AÇU-3.DES-2.3100-15-EGS-016` |
| **2.1.4** | Contrapiso de Regularização e=3cm | 368,40 m² | 5,0% | **386,82** | `m² (11.6 m³)` | `AÇU-3.DES-2.3100-15-EGS-018` |
| **2.1.5** | Piso Porcelanato 60x60cm Retificado | 368,40 m² | 10,0% | **281** | `caixas (405.2 m²)` | `AÇU-3.DES-2.3100-15-EGS-016` |
| **2.1.6** | Rodapé Porcelanato h=10cm | 384,20 m | 10,0% | **422,62** | `m` | `AÇU-3.DES-2.3100-15-EGS-018` |
| **2.1.7** | Pintura Látex Acrílica 3 Demãos | 2491,28 m² | 5,0% | **36** | `latas 18L` | `AÇU-3.DES-2.3100-15-EGS-019` |
| **2.1.8** | Esquadrias de Madeira/Alumínio (Portas P1-P5) | 24,00 un | 0,0% | **24** | `conjuntos` | `AÇU-3.DES-2.3100-15-EGS-018` |
| **2.1.9** | Esquadrias de Alumínio Vidro (Janelas J1-J4) | 18,00 un | 0,0% | **18** | `conjuntos` | `AÇU-3.DES-2.3100-15-EGS-018` |
| **2.1.10** | Impermeabilização Polimérica Sanitários/Copa | 84,20 m² | 10,0% | **92,62** | `m² (19 caixas 18kg)` | `AÇU-3.DES-2.3100-15-EGS-016` |
| **2.2.1** | Telha Termoacústica Sandwich 30mm EPS | 381,29 m² | 10,0% | **419,42** | `m² (70 telhas 6m)` | `AÇU-3.DES-2.3100-15-EGS-017` |
| **2.2.2** | Terças Metálicas Perfil U 100x40x2,25mm | 156,00 m | 5,0% | **28** | `barras 6m (573 kg)` | `AÇU-3.DES-2.3100-15-EGS-017` |
| **2.2.3** | Muretas Escalonadas Entreforro (Bloco 9x19x39cm) | 45,24 m² | 5,0% | **594** | `blocos 9x19x39cm` | `AÇU-3.DES-2.3100-15-EGS-017` |
| **2.2.4** | Calha Galvanizada nº 24 (Dev 80cm) | 52,00 m | 5,0% | **54,60** | `m (19 peças 3m)` | `AÇU-3.DES-2.3100-15-EGS-017` |
| **2.2.5** | Rufo / Pingadeira Platibanda (Dev 40cm) | 82,00 m | 5,0% | **86,10** | `m (29 peças 3m)` | `AÇU-3.DES-2.3100-15-EGS-017` |
| **2.2.6** | Impermeabilização Manta Asfáltica 4mm Calhas | 62,00 m² | 15,0% | **8** | `rolos 10m² (71.3m²)` | `AÇU-3.DES-2.3100-15-EGS-017/019` |
| **2.2.7** | Ralo Hemisférico Abacaxi Inox Ø150mm | 8,00 un | 0,0% | **8** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-015/017` |
| **2.2.8** | Alvenaria de Platibanda Bloco 14x19x39cm (h=0,39m) | 31,98 m² | 5,0% | **420** | `blocos 14x19x39cm` | `AÇU-3.DES-2.3100-15-EGS-017` |
| **2.2.9** | Emboço/Reboco e=20mm Face Interna Platibanda | 74,62 m² | 5,0% | **78,35** | `m² (16 sacos)` | `AÇU-3.DES-2.3100-15-EGS-017` |
| **2.2.10** | Pintura Acrílica Face Interna Platibanda | 74,62 m² | 5,0% | **2** | `latas 18L (78.35m²)` | `AÇU-3.DES-2.3100-15-EGS-017/019` |

---

## 🛒 4. Lista Consolidada de Pedido de Compras (UCC) — Arquitetura, Cobertura & Platibanda

1. **Blocos de Concreto (14x19x39cm):** **`14.351 unidades`** *(13.931 paredes + 420 platibanda)*
2. **Blocos de Concreto (9x19x39cm - Muretas de Apoio Entreforro):** **`594 unidades`**
3. **Argamassa Pronta para Emboço/Reboco Platibanda:** **`16 sacos de 20kg`**
4. **Tinta Acrílica Impermeável Platibanda:** **`2 latas de 18L`**
5. **Telhas Termoacústicas Sandwich (30mm EPS - 6,00m x 1,00m):** **`70 telhas`** *(419,4 m²)*
6. **Terças Metálicas Perfil U Enrijecido (100x40x2,25mm):** **`28 barras de 6m`** *(573,3 kg)*
7. **Calhas Galvanizadas nº 24 (dev 80cm - peças de 3m):** **`19 peças`** *(54,6 m)*
8. **Rufos / Pingadeiras Galvanizadas (dev 40cm - peças de 3m):** **`29 peças`** *(86,1 m)*
9. **Manta Asfáltica 4mm Tipo III (rolos de 10m²):** **`8 rolos`**
10. **Ralos Hemisféricos Abacaxi Inox Ø150mm:** **`8 unidades`**

---

*Data da última atualização:* 08/09/2026
"""

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"CSV de Arquitetura, Cobertura e Platibanda gerado: {csv_path}")
    print(f"Markdown de Arquitetura, Cobertura e Platibanda gerado: {md_path}")

if __name__ == "__main__":
    main()
