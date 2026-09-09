import os
import csv

def main():
    base_dir = r"c:\Users\Alexandre\Workspace\A11_SISTEMA_DE_GESTAO_OBRAS\projetos\OBRA_TMULT\02_ORCAMENTO_BASE_E_CONTRATOS"
    os.makedirs(base_dir, exist_ok=True)

    csv_path = os.path.join(base_dir, "QUANTITATIVO_INSTALACOES_HVAC.csv")
    md_path = os.path.join(base_dir, "MEMORIA_CALCULO_INSTALACOES_HVAC.md")

    # CSV Data
    rows = [
        ["Código EAP", "Item / Descricao", "Disciplina", "Qtd Projeto", "Unidade Proj", "Perda (%)", "Qtd Comercial UCC", "Unidade UCC", "Prancha Referencia"],
        
        # 3.1 INSTALAÇÕES ELÉTRICAS
        ["3.1.1", "Cabo Cobre Flexível 750V 2,5mm² (Iluminação/TUG)", "Elétrica", "1850.0", "m", "10.0", "21", "rolos de 100m (2035m)", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.2", "Cabo Cobre Flexível 750V 4,0mm² (Tomadas TUG/TUE)", "Elétrica", "640.0", "m", "10.0", "8", "rolos de 100m (704m)", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.3", "Cabo Cobre Flexível 750V 6,0mm² (Ar Condicionado)", "Elétrica", "420.0", "m", "10.0", "5", "rolos de 100m (462m)", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.4", "Cabo Cobre Sintenax 0,6/1kV 35mm² (Alimentador)", "Elétrica", "120.0", "m", "5.0", "126.0", "m", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.5", "Eletroduto Rígido PVC Ø3/4\" (25mm) c/ Conexões", "Elétrica", "480.0", "m", "10.0", "176", "varas de 3m (528m)", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.6", "Eletroduto Rígido PVC Ø1\" (32mm) c/ Conexões", "Elétrica", "210.0", "m", "10.0", "77", "varas de 3m (231m)", "AÇU-3.DES-2.3100-15-EGS-013"],
        
        # Caixas de Embutir, Placas e Módulos Elétricos
        ["3.1.7", "Caixa de Embutir 4x2\" PVC Amarela para Parede", "Elétrica", "184.0", "unid", "5.0", "194", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.8", "Caixa de Embutir 4x4\" PVC Amarela para Parede", "Elétrica", "24.0", "unid", "5.0", "26", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.9", "Caixa Octogonal 3x3\" PVC para Teto", "Elétrica", "68.0", "unid", "5.0", "72", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.10", "Conjunto Suporte + Placa 4x2\" c/ Parafusos", "Elétrica", "184.0", "unid", "5.0", "194", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.11", "Módulo de Tomada 2P+T 10A / 250V (Branca)", "Elétrica", "110.0", "unid", "5.0", "116", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.12", "Módulo de Tomada 2P+T 20A / 250V (Vermelha TUE)", "Elétrica", "24.0", "unid", "5.0", "26", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.13", "Módulo Interruptor Simples 10A", "Elétrica", "22.0", "unid", "5.0", "24", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.14", "Módulo Interruptor Paralelo (Three-Way) 10A", "Elétrica", "8.0", "unid", "5.0", "9", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],

        # Cabeamento de Dados, Voz e Telecomunicações
        ["3.1.15", "Cabo UTP Cat6 LSZH 4 Pares (Dados/Voz)", "Telecom", "1450.0", "m", "10.0", "16", "rolos de 100m (1600m)", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.16", "Módulo Tomada RJ45 Cat6 Keystone", "Telecom", "36.0", "unid", "5.0", "38", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.17", "Rack Metalico Telecom 19\" 12U de Parede", "Telecom", "1.0", "unid", "0.0", "1", "unidade", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.18", "Patch Panel 24 Portas Cat6 19\"", "Telecom", "2.0", "unid", "0.0", "2", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.19", "Switch Gigabit Ethernet 24 Portas PoE", "Telecom", "1.0", "unid", "0.0", "1", "unidade", "AÇU-3.DES-2.3100-15-EGS-013"],

        # Quadros e Proteção Elétrica
        ["3.1.20", "Quadro Geral de Distribuição QDG 150A Trifásico", "Elétrica", "1.0", "unid", "0.0", "1", "unidade", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.21", "Quadro de Distribuição de Luz QDF 24 Elementos embutir", "Elétrica", "2.0", "unid", "0.0", "2", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.22", "Disjuntor Geral Caixa Moldada 150A Trifásico", "Elétrica", "1.0", "unid", "0.0", "1", "unidade", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.23", "Disjuntor Termomagnético DIN Monopolar 10A/16A/20A", "Elétrica", "28.0", "unid", "5.0", "30", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.24", "Disjuntor Termomagnético DIN Bipolar/Tripolar 25A/32A", "Elétrica", "18.0", "unid", "5.0", "19", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.25", "Interruptor Diferencial Residual DR Tetrapolar 40A 30mA", "Elétrica", "4.0", "unid", "0.0", "4", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.26", "Dispositivo de Proteção contra Surtos DPS 20kA 275V", "Elétrica", "8.0", "unid", "0.0", "8", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.27", "Painel LED Embutir 60x60cm 40W 4000K", "Elétrica", "68.0", "unid", "5.0", "72", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.28", "Luminária Hermética LED 2x18W IP65 (Áreas Técnicas)", "Elétrica", "16.0", "unid", "5.0", "17", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.29", "Bloco Iluminação de Emergência LED 2x8W c/ Bateria", "Elétrica", "14.0", "unid", "0.0", "14", "unidades", "AÇU-3.DES-2.3100-15-EGS-013"],
        ["3.1.30", "Haste de Aterramento Copperweld 3/4\" x 3,00m + Malha", "Elétrica", "6.0", "unid", "0.0", "6", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-013"],

        # 3.2 INSTALAÇÕES HIDROSSANITÁRIAS E PLUVIAIS (Detalhamento Completo)
        ["3.2.1", "Tubo PVC Soldável Água Fria Ø25mm (3/4\")", "Hidráulica", "180.0", "m", "10.0", "33", "varas de 6m (198m)", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.2", "Tubo PVC Soldável Água Fria Ø50mm (1.1/2\")", "Hidráulica", "95.0", "m", "10.0", "18", "varas de 6m (108m)", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.3", "Tubo PVC Esgoto Série Normal Ø40mm", "Hidráulica", "64.0", "m", "10.0", "12", "varas de 6m (72m)", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.4", "Tubo PVC Esgoto Série Normal Ø75mm", "Hidráulica", "42.0", "m", "10.0", "8", "varas de 6m (48m)", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.5", "Tubo PVC Esgoto Série Normal Ø100mm", "Hidráulica", "140.0", "m", "10.0", "26", "varas de 6m (156m)", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.6", "Tubo PVC Pluvial Série Reforçada Ø150mm", "Hidráulica", "110.0", "m", "10.0", "21", "varas de 6m (126m)", "AÇU-3.DES-2.3100-15-EGS-015"],

        # Conexões Hidráulicas e Esgoto
        ["3.2.7", "Joelho 90º PVC Soldável Ø25mm", "Hidráulica", "86.0", "unid", "5.0", "91", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.8", "Joelho 90º c/ Bucha de Latão Ø25mm x 1/2\"", "Hidráulica", "32.0", "unid", "5.0", "34", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.9", "Joelho 90º PVC Soldável Ø50mm", "Hidráulica", "24.0", "unid", "5.0", "26", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.10", "Tê 90º PVC Soldável Ø25mm", "Hidráulica", "48.0", "unid", "5.0", "51", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.11", "Tê 90º Redução PVC Soldável Ø50x25mm", "Hidráulica", "18.0", "unid", "5.0", "19", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.12", "Curva de Transposição PVC Soldável Ø25mm", "Hidráulica", "14.0", "unid", "5.0", "15", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.13", "Joelho 90º PVC Esgoto Ø100mm", "Hidráulica", "36.0", "unid", "5.0", "38", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.14", "Joelho 45º PVC Esgoto Ø100mm", "Hidráulica", "22.0", "unid", "5.0", "24", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.15", "Junção 45º Y PVC Esgoto Ø100x50mm", "Hidráulica", "18.0", "unid", "5.0", "19", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.16", "Tê Sanitário 90º PVC Esgoto Ø100x100mm", "Hidráulica", "12.0", "unid", "5.0", "13", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],

        # Registros, Válvulas e Reservatórios
        ["3.2.17", "Registro de Gaveta Bruto c/ Canopla Cromada Ø25mm (3/4\")", "Hidráulica", "12.0", "unid", "0.0", "12", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.18", "Registro de Gaveta Bruto c/ Canopla Cromada Ø50mm (1.1/2\")", "Hidráulica", "4.0", "unid", "0.0", "4", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.19", "Registro de Pressão c/ Canopla Cromada Ø20mm (Chuveiros)", "Hidráulica", "6.0", "unid", "0.0", "6", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.20", "Válvula de Retenção Vertical Ø50mm", "Hidráulica", "2.0", "unid", "0.0", "2", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.21", "Reservatório de Água Potável Polietileno 5.000 L c/ Tampa", "Hidráulica", "2.0", "unid", "0.0", "2", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.22", "Ralo Sifonado PVC 150x150x50mm Grelha Inox", "Hidráulica", "14.0", "unid", "0.0", "14", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.23", "Caixa de Gordura Pré-moldada Concreto 100L", "Hidráulica", "2.0", "unid", "0.0", "2", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.24", "Caixa de Inspeção Esgoto Concreto 60x60x60cm c/ Tampa", "Hidráulica", "6.0", "unid", "0.0", "6", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],

        # Louças, Metais e Kits Sanitários
        ["3.2.25", "Bacia Sanitária c/ Caixa Acoplada 3/6L e Assento", "Hidráulica", "10.0", "unid", "0.0", "10", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.26", "Lavatório Louça Branca c/ Torneira Automática de Mesa", "Hidráulica", "12.0", "unid", "0.0", "12", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.27", "Sifão Sanfonado Universal PVC c/ Adaptador", "Hidráulica", "14.0", "unid", "5.0", "15", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.28", "Engate Flexível Inox 1/2\" 40cm", "Hidráulica", "22.0", "unid", "5.0", "24", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.29", "Válvula de Escoamento Inox 7/8\" para Lavatório", "Hidráulica", "12.0", "unid", "5.0", "13", "unidades", "AÇU-3.DES-2.3100-15-EGS-015"],
        ["3.2.30", "Fita Veda-Rosca PTFE 18mm x 50m", "Hidráulica", "12.0", "rolo", "0.0", "12", "rolos", "AÇU-3.DES-2.3100-15-EGS-015"],

        # 3.3 HVAC - CLIMATIZAÇÃO E EXAUSTÃO
        ["3.3.1", "Aparelho Split Cassete 36.000 BTU/h Inverter R410A", "HVAC", "4.0", "unid", "0.0", "4", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-008"],
        ["3.3.2", "Aparelho Split Hi-Wall 18.000 BTU/h Inverter R410A", "HVAC", "6.0", "unid", "0.0", "6", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-008"],
        ["3.3.3", "Aparelho Split Hi-Wall 12.000 BTU/h Inverter R410A", "HVAC", "6.0", "unid", "0.0", "6", "conjuntos", "AÇU-3.DES-2.3100-15-EGS-008"],
        ["3.3.4", "Tubulação Cobre Flexível Ø3/8\"+Ø5/8\" c/ Isolamento", "HVAC", "180.0", "m", "10.0", "198.0", "m", "AÇU-3.DES-2.3100-15-EGS-008"],
        ["3.3.5", "Tubo PVC Condensado Ø25mm c/ Isolamento", "HVAC", "120.0", "m", "10.0", "22", "varas de 6m (132m)", "AÇU-3.DES-2.3100-15-EGS-008"],
        ["3.3.6", "Exaustor Axial de Parede/Teto 150 m³/h", "HVAC", "6.0", "unid", "0.0", "6", "unidades", "AÇU-3.DES-2.3100-15-EGS-008"]
    ]

    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(rows)

    # Markdown Content
    md_content = """# ⚡💧❄️ Memória de Cálculo Auditável: Instalações Elétricas, Telecom, Hidrossanitárias e HVAC

**Projeto:** TMULT - Terminal Multiuso (Porto do Açu) — Edifício Administrativo  
**Disciplina:** Engenharia de Custos / Instalações Elétricas, Lógica/Telecom, Hidrossanitárias & HVAC  
**Documentos de Referência:** Pranchas `AÇU-3.DES-2.3100-15-EGS-013` (Elétrica/Telecom), `EGS-015` (Hidrosanitária/Louças) e `EGS-008` (HVAC)  
**Data da Auditoria:** 08/09/2026  

---

## 🧮 1. Fórmulas Matemáticas e Regras de Engenharia Utilizadas

### 1.1 Instalações Elétricas e Telecomunicações
> **Fórmula Metragem de Cabos:** `L_cabo = Σ (L_trajeto × N_condutores) + Pontas (0,5m/caixa + 1,0m/QDC)`  
> **Eletrodutos:** `L_eletroduto = (L_horizontal + ΔZ_descidas) × (1 + Perda 10%)`
- **Caixas de Embutir 4x2" e 4x4":** Mapeadas trecho a trecho para todos os pontos de tomadas (117 un), interruptores (30 un) e pontos de dados (36 un) $\rightarrow$ **194 caixas 4x2"** e **26 caixas 4x4"**.
- **Caixas Octogonais de Teto:** 68 pontos de iluminação LED $\rightarrow$ **72 caixas octogonais**.
- **Telecom & Dados (Cat6):** `1.450 m` de Cabo UTP Cat6 LSZH $\rightarrow$ **16 rolos de 100m**, 38 Keystone RJ45, 1 Rack 19" 12U, 2 Patch Panels 24p e 1 Switch PoE.
- **Quadros & Disjuntores:** 1 QDG 150A, 2 QDF 24e, 1 Disjuntor Moldado 150A, 49 Disjuntores DIN, 4 DRs 40A 30mA e 8 DPS 20kA.

### 1.2 Instalações Hidrossanitárias, Louças e Conexões
> **Fórmula Tubulações:** `L_comercial = CEIL( L_projeto × (1 + Perda 10%) / 6,00m ) × 6,00m`  
> **Conexões Detalhadas:** Rastreamento unifilar/isométrico peça a peça.
- **Tubulações PVC Água Fria e Esgoto:** 661m lineares no projeto $\rightarrow$ **126 varas de 6m**.
- **Conexões Derivadas:** 86 joelhos Ø25mm, 32 joelhos c/ bucha latão, 24 joelhos Ø50mm, 48 tês Ø25mm, 18 tês redução Ø50x25mm, 14 curvas transposição, 36 joelhos esgoto Ø100mm, 22 joelhos 45° Ø100mm, 18 junções Y 45° e 12 tês sanitários.
- **Registros e Válvulas:** 12 Registros de Gaveta Ø25mm c/ Canopla, 4 Registros de Gaveta Ø50mm, 6 Registros de Pressão Ø20mm cromados, 2 Válvulas Retenção Ø50mm.
- **Reservatórios & Caixas:** 2 Reservatórios Polietileno 5.000L, 14 Ralos Sifonados 150x150mm, 2 Caixas de Gordura 100L e 6 Caixas de Inspeção 60x60x60cm.
- **Louças, Metais & Acessórios:** 10 Bacias Sanitárias C/ CA, 12 Lavatórios c/ Torneira Automática, 15 Sifões Sanfonados, 24 Engates Inox 40cm, 13 Válvulas Escoamento e 12 rolos Fita Veda-Rosca.

---

## 📊 2. Tabela Consolidada para EAP e Pedido de Compras (UCC)

| Código EAP | Descrição do Insumo / Serviço | Qtd Projeto | Perda (%) | Qtd Comercial UCC | Unidade UCC | Prancha Ref |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **3.1.1** | Cabo Cobre Flex 2,5mm² | 1850.0 m | 10.0% | **21** | `rolos 100m (2035m)` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.2** | Cabo Cobre Flex 4,0mm² | 640.0 m | 10.0% | **8** | `rolos 100m (704m)` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.3** | Cabo Cobre Flex 6,0mm² | 420.0 m | 10.0% | **5** | `rolos 100m (462m)` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.4** | Cabo Sintenax 35mm² | 120.0 m | 5.0% | **126,0** | `m` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.5** | Eletroduto PVC Ø3/4" (25mm) | 480.0 m | 10.0% | **176** | `varas 3m (528m)` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.7** | Caixa Embutir 4x2" PVC Parede | 184.0 un | 5.0% | **194** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.8** | Caixa Embutir 4x4" PVC Parede | 24.0 un | 5.0% | **26** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.9** | Caixa Octogonal 3x3" PVC Teto | 68.0 un | 5.0% | **72** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.11** | Módulo Tomada 2P+T 10A Branca | 110.0 un | 5.0% | **116** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.12** | Módulo Tomada 2P+T 20A Vermelha | 24.0 un | 5.0% | **26** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.13** | Módulo Interruptor Simples 10A | 22.0 un | 5.0% | **24** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.14** | Módulo Interruptor Paralelo 10A | 8.0 un | 5.0% | **9** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.15** | Cabo UTP Cat6 LSZH Dados/Voz | 1450.0 m | 10.0% | **16** | `rolos 100m (1600m)` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.16** | Módulo Tomada RJ45 Cat6 Keystone | 36.0 un | 5.0% | **38** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.17** | Rack Telecom 19" 12U Parede | 1.0 un | 0.0% | **1** | `unidade` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.20** | Quadro General QDG 150A Trifásico | 1.0 un | 0.0% | **1** | `unidade` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.21** | Quadro Distribuição QDF 24e Embutir | 2.0 un | 0.0% | **2** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.23** | Disjuntor DIN Monopolar 10A-20A | 28.0 un | 5.0% | **30** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.1.25** | Interruptor DR Tetrapolar 40A 30mA | 4.0 un | 0.0% | **4** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-013` |
| **3.2.1** | Tubo PVC Soldável Ø25mm | 180.0 m | 10.0% | **33** | `varas 6m (198m)` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **3.2.5** | Tubo PVC Esgoto Ø100mm | 140.0 m | 10.0% | **26** | `varas 6m (156m)` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **3.2.7** | Joelho 90º PVC Soldável Ø25mm | 86.0 un | 5.0% | **91** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **3.2.8** | Joelho 90º c/ Bucha Latão Ø25x1/2" | 32.0 un | 5.0% | **34** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **3.2.10** | Tê 90º PVC Soldável Ø25mm | 48.0 un | 5.0% | **51** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **3.2.17** | Registro Gaveta c/ Canopla Ø25mm | 12.0 un | 0.0% | **12** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **3.2.19** | Registro Pressão c/ Canopla Ø20mm | 6.0 un | 0.0% | **6** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **3.2.21** | Reservatório Polietileno 5.000L | 2.0 un | 0.0% | **2** | `unidades` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **3.2.25** | Bacia Sanitária C/ CA | 10.0 un | 0.0% | **10** | `conjuntos` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **3.2.26** | Lavatório c/ Torneira Automática | 12.0 un | 0.0% | **12** | `conjuntos` | `AÇU-3.DES-2.3100-15-EGS-015` |
| **3.2.30** | Fita Veda-Rosca PTFE 18mmx50m | 12.0 rolo | 0.0% | **12** | `rolos` | `AÇU-3.DES-2.3100-15-EGS-015` |

---

## 🛒 3. Lista Consolidada de Pedido de Compras (UCC) — Instalações & Telecom

1. **Caixas de Embutir 4x2" PVC Amarela (Parede):** **`194 unidades`**
2. **Caixas de Embutir 4x4" PVC Amarela (Parede):** **`26 unidades`**
3. **Caixas Octogonais 3x3" PVC (Teto):** **`72 unidades`**
4. **Conjuntos Placa + Suporte 4x2":** **`194 conjuntos`**
5. **Módulos de Tomada 2P+T (116 un 10A + 26 un 20A):** **`142 unidades`**
6. **Módulos de Interruptor (24 Simples + 9 Paralelos):** **`33 unidades`**
7. **Cabo UTP Cat6 LSZH (Dados/Voz):** **`16 rolos de 100m`** *(1.600m)*
8. **Módulos Keystone RJ45 Cat6:** **`38 unidades`**
9. **Rack Telecom 19" 12U Parede + 2 Patch Panels 24p + Switch 24p PoE:** **`1 Kit Telecom`**
10. **Quadros Elétricos (1 QDG 150A + 2 QDF 24e):** **`3 quadros`**
11. **Disjuntores DIN (30 Monopolares + 19 Bipolares/Tripolares + 4 DRs + 8 DPS):** **`61 dispositivos`**
12. **Conexões Hidráulicas PVC Soldável (Joelhos, Tês, Luvas, Transposição):** **`217 unidades`**
13. **Conexões Esgoto PVC (Joelhos 90°/45°, Junções Y 45°, Tês Sanitários):** **`94 unidades`**
14. **Registros c/ Canopla Cromada (12 Gaveta 3/4" + 4 Gaveta 1.1/2" + 6 Pressão):** **`22 registros`**
15. **Reservatórios Polietileno 5.000 Litros c/ Tampa:** **`2 unidades`**
16. **Kits Sanitários (10 Bacias C/ CA + 12 Lavatórios + 15 Sifões + 24 Engates Inox):** **`61 itens`**

---

*Data da última atualização:* 08/09/2026
"""

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"CSV Completo de Instalações gerado: {csv_path}")
    print(f"Markdown Completo de Instalações gerado: {md_path}")

if __name__ == "__main__":
    main()
