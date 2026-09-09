# 🏛️ Memória de Cálculo Auditável: Arquitetura, Vedações, Cobertura e Platibanda

**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo  
**Disciplina:** Arquitetura, Vedações, Cobertura e Platibanda  
**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-15-EGS-015 a EGS-019`  
**Data da Auditoria:** 08/09/2026  

---

## 🧮 1. Demonstração Matemática Detalhada Arquitetura e Platibanda

### 1.1 Alvenaria de Vedação Bloco Concreto 14x19x39cm (Pranchas EGS-015 e EGS-018)
> **Fórmula:** `A_líquida = A_bruta - Σ A_esquadrias - Σ A_pilares`
- **Perímetro de Paredes:** `418,00 m` × **Pé-direito:** `2,98 m` = `1.245,64 m²` (Bruta)
- **Desconto de Esquadrias (24 Portas + 18 Janelas):** `112,60 m²`
- **Desconto de Pilares Embutidos:** `71,60 m²`
- **Área Líquida Alvenaria:** **`1.061,44 m²`** → **13.931 blocos 14x19x39cm** (13,12 blocos/m² c/ perda 5%).

### 1.2 Revestimento Cerâmico dos Sanitários (Prancha EGS-016)
- **Ambientes WCs (Feminino, Masculino, PNE):**
  - Perímetro total de paredes internas dos WCs: `46,78 m`
  - Altura do revestimento conforme Legenda EGS-016: `1,80 m`
  - Área de Cerâmica Eliane 45x45 Plus Gray: `46,78m × 1,80m = 84,20 m²`
  - Quantidade Comercial UCC (Com Perda 10%): `84,20 × 1,10 = 92,62 m²` → **65 caixas**.

---

## 📊 2. Tabela Consolidada de Quantitativos e Pedido de Compras (UCC)

| Código EAP | Descrição do Insumo / Serviço | Qtd Projeto | Perda (%) | Qtd Comercial UCC | Unidade UCC | Prancha Ref |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **2.1.1** | Alvenaria de Vedação Bloco Concreto 14x19x39cm | 1061.44 m² | 5.0% | **13931** | `blocos (1114.5 m²)` | `AÇU-3.DES-2.3100-15-EGS-015/018` |
| **2.1.2** | Chapisco Traço 1:3 e=5mm em Paredes | 2122.88 m² | 5.0% | **2229.02** | `m² (75 sacos cimento)` | `AÇU-3.DES-2.3100-15-EGS-015/016` |
| **2.1.3** | Emboço/Reboco Paulista e=20mm em Paredes | 2122.88 m² | 5.0% | **2229.02** | `m² (446 sacos argamassa)` | `AÇU-3.DES-2.3100-15-EGS-015/016` |
| **2.1.4** | Contrapiso de Regularização e=3cm | 368.40 m² | 5.0% | **386.82** | `m² (11.6 m³ argamassa)` | `AÇU-3.DES-2.3100-15-EGS-015/018` |
| **2.1.5** | Piso Porcelanato 60x60cm Retificado | 368.40 m² | 10.0% | **281** | `caixas (405.2 m²)` | `AÇU-3.DES-2.3100-15-EGS-015/016` |
| **2.1.6** | Revestimento Cerâmico h=1,80m nos WCs (Eliane 45x45 Plus Gray) | 84.20 m² | 10.0% | **65** | `caixas (92.6 m²)` | `AÇU-3.DES-2.3100-15-EGS-018` |
| **2.1.7** | Rodapé Porcelanato h=10cm | 384.20 m | 10.0% | **422.62** | `m` | `AÇU-3.DES-2.3100-15-EGS-015/018` |
| **2.1.8** | Pintura Látex Acrílica 3 Demãos (Paredes + Tetos) | 2491.28 m² | 5.0% | **36** | `latas 18L (2615.8 m²)` | `AÇU-3.DES-2.3100-15-EGS-015/019` |
| **2.1.9** | Esquadrias de Madeira/Alumínio (Portas P1-P5) | 24.0 unid | 0.0% | **24** | `conjuntos` | `AÇU-3.DES-2.3100-15-EGS-018` |
| **2.1.10** | Esquadrias de Alumínio Vidro (Janelas J1-J4) | 18.0 unid | 0.0% | **18** | `conjuntos` | `AÇU-3.DES-2.3100-15-EGS-018` |
| **2.1.11** | Impermeabilização Polimérica Sanitários/Copa | 84.20 m² | 10.0% | **92.62** | `m² (19 caixas 18kg)` | `AÇU-3.DES-2.3100-15-EGS-015/016` |
| **2.2.1** | Telha Termoacústica Trapezoidal (Sandwich 30mm EPS) | 381.29 m² | 10.0% | **419.42** | `m² (70 telhas de 6m)` | `AÇU-3.DES-2.3100-15-EGS-017` |
| **2.2.2** | Terças Metálicas Perfil U Enrijecido 100x40x2,25mm | 156.00 m | 5.0% | **28** | `barras de 6m (573.3 kg)` | `AÇU-3.DES-2.3100-15-EGS-017` |
| **2.2.3** | Muretas Escalonadas de Apoio no Entreforro (Bloco 9x19x39cm) | 45.24 m² | 5.0% | **594** | `blocos 9x19x39cm` | `AÇU-3.DES-2.3100-15-EGS-017` |
| **2.2.4** | Calha em Chapa Galvanizada nº 24 (Dev 80cm) | 52.00 m | 5.0% | **54.60** | `m (19 peças de 3m)` | `AÇU-3.DES-2.3100-15-EGS-017` |
| **2.2.5** | Rufo e Pingadeira Metálica de Platibanda (Dev 40cm) | 82.00 m | 5.0% | **86.10** | `m (29 peças de 3m)` | `AÇU-3.DES-2.3100-15-EGS-017` |
| **2.2.6** | Impermeabilização Manta Asfáltica 4mm em Calhas | 62.00 m² | 15.0% | **8** | `rolos de 10m² (71.3 m²)` | `AÇU-3.DES-2.3100-15-EGS-017/019` |
| **2.2.7** | Ralo Hemisférico Tipo Abacaxi Inox Ø150mm para Calhas | 8.0 unid | 0.0% | **8** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-015/017` |
| **2.2.8** | Alvenaria de Platibanda Bloco Concreto 14x19x39cm (h=0,39m) | 31.98 m² | 5.0% | **420** | `blocos 14x19x39cm` | `AÇU-3.DES-2.3100-15-EGS-017` |
| **2.2.9** | Chapisco e Emboço/Reboco e=20mm Face Interna da Platibanda | 74.62 m² | 5.0% | **78.35** | `m² (16 sacos argamassa)` | `AÇU-3.DES-2.3100-15-EGS-017` |
| **2.2.10** | Pintura Acrílica Impermeável 3 Demãos Face Interna da Platibanda | 74.62 m² | 5.0% | **2** | `latas 18L (78.35 m²)` | `AÇU-3.DES-2.3100-15-EGS-017/019` |

---

*Data da última atualização:* 08/09/2026
