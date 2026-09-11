import glob
import os
import csv
import re

def processar_obra(base_dir, pdf_subdir, nome_projeto, titulos_map):
    pdf_dir = os.path.join(base_dir, pdf_subdir)
    carimbo_dir = os.path.join(pdf_dir, '_carimbos_extraidos')
    os.makedirs(carimbo_dir, exist_ok=True)
    pdfs = sorted(glob.glob(os.path.join(pdf_dir, '*.pdf')))
    
    if not pdfs:
        print(f"Nenhum PDF em: {pdf_dir}")
        return

    desenhos = []

    for i, p in enumerate(pdfs, 1):
        fname = os.path.basename(p)
        
        match = re.search(r'([A-Za-z0-9\._\-]+)\s+rev\.?([A-Za-z0-9]+)', fname, re.IGNORECASE)
        if match:
            codigo = match.group(1)
            rev = match.group(2)
        else:
            match2 = re.search(r'([A-Za-z0-9\._\-]+)_([0-9]+)\.pdf', fname)
            if match2:
                codigo = match2.group(1)
                rev = match2.group(2)
            else:
                codigo = os.path.splitext(fname)[0]
                rev = '0'
            
        titulo = titulos_map.get(fname, f"Prancha {codigo}")
        img_name = os.path.splitext(fname)[0] + '_carimbo.png'
        carimbo_path = os.path.join(pdf_subdir, '_carimbos_extraidos', img_name)
        
        desenhos.append({
            'item': i,
            'codigo': codigo,
            'titulo': titulo,
            'revisao': rev,
            'arquivo_pdf': f"{pdf_subdir}/{fname}",
            'carimbo_img': carimbo_path
        })

    # CSV
    csv_path = os.path.join(base_dir, 'LISTA_DE_DESENHOS.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['item', 'codigo', 'titulo', 'revisao', 'arquivo_pdf', 'carimbo_img'], delimiter=';')
        writer.writeheader()
        writer.writerows(desenhos)
    print(f"CSV gerado: {csv_path}")

    # MD
    md_path = os.path.join(base_dir, 'LISTA_DE_DESENHOS.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f'# 📋 Lista Mestra de Desenhos - {nome_projeto}\n\n')
        f.write(f'**Projeto:** {nome_projeto}\n')
        f.write(f'**Localização dos Arquivos:** `01_ENGENHARIA_E_PROJETOS/{pdf_subdir}/`\n')
        f.write(f'**Total de Pranchas Indexadas:** {len(desenhos)}\n\n')
        f.write('---\n\n')
        f.write('## 📐 Tabela Mestra de Pranchas\n\n')
        f.write('| Item | Código do Desenho | Título / Descrição da Prancha | Rev | Arquivo PDF |\n')
        f.write('| :---: | :--- | :--- | :---: | :--- |\n')
        for d in desenhos:
            pdf_full_path = os.path.join(base_dir, d['arquivo_pdf']).replace(os.sep, '/')
            pdf_filename = os.path.basename(d['arquivo_pdf'])
            f.write(f"| {d['item']} | `{d['codigo']}` | {d['titulo']} | **{d['revisao']}** | [{pdf_filename}](file:///{pdf_full_path}) |\n")
        f.write('\n---\n\n')
        f.write('## 🖼️ Imagens dos Carimbos Extraídos\n\n')
        f.write('Os carimbos foram recortados para consulta rápida e auditoria:\n\n')
        f.write(f'```text\n01_ENGENHARIA_E_PROJETOS/{pdf_subdir}/_carimbos_extraidos/\n```\n\n')
        f.write('*Data da última atualização:* 08/09/2026\n')
    print(f"Markdown gerado: {md_path}")

# TMULT
processar_obra(
    r'c:\Users\Alexandre\Workspace\A11_SISTEMA_DE_GESTAO_OBRAS\projetos\OBRA_TMULT\01_ENGENHARIA_E_PROJETOS',
    'EDIFICIO_ADMINISTRATIVO',
    'TMULT - Edifício Administrativo',
    {
        'AÇU-3.DES-2.3100-11-EGS-051 rev.A.pdf': 'Estrutura - Fôrmas e Armação de Sapatas e Baldrames (Prancha 01)',
        'AÇU-3.DES-2.3100-11-EGS-052 rev.A.pdf': 'Estrutura - Planta e Cortes de Detalhamento de Sapatas (Prancha 02)',
        'AÇU-3.DES-2.3100-11-EGS-053 rev.A.pdf': 'Estrutura - Detalhamento de Armação de Vigas VB1 a VB6',
        'AÇU-3.DES-2.3100-11-EGS-054 rev.A.pdf': 'Estrutura - Detalhamento de Armação de Vigas VB11 a VB18',
        'AÇU-3.DES-2.3100-11-EGS-055 rev.A.pdf': 'Estrutura - Fôrma e Detalhes das Nervuras das Lajes',
        'AÇU-3.DES-2.3100-11-EGS-056 rev.A.pdf': 'Estrutura - Planta de Cobertura e Laje L2',
        'AÇU-3.DES-2.3100-11-EGS-057 rev.A.pdf': 'Estrutura - Tabela de Dobramento de Aço e Relação de Armações',
        'AÇU-3.DES-2.3100-11-EGS-059 rev.A.pdf': 'Estrutura - Quadro Geral de Resumo de Aço e Concreto',
        'AÇU-3.DES-2.3100-11-EGS-060 rev.A.pdf': 'Estrutura - Locação de Pilares V114 e Cobertura',
        'AÇU-3.DES-2.3100-15-EGS-015 rev.A.pdf': 'Arquitetura - Layout de Pavimento e Legenda de Acabamentos (01)',
        'AÇU-3.DES-2.3100-15-EGS-016 rev.A.pdf': 'Arquitetura - Legenda e Tabela Geral de Acabamentos (02)',
        'AÇU-3.DES-2.3100-15-EGS-017 rev.A.pdf': 'Arquitetura - Cortes Gerais e Acessos do Edifício',
        'AÇU-3.DES-2.3100-15-EGS-018 rev.A.pdf': 'Arquitetura - Planta Baixa de Modulação de Ambientes',
        'AÇU-3.DES-2.3100-15-EGS-019 rev.A.pdf': 'Arquitetura - Elevações e Fachadas Principais',
        'AÇU-3.DES-2.3100-16-EGS-013 rev.0.pdf': 'Instalações - Esquema Unifilar e Diagrama Elétrico',
        'AÇU-3.DES-2.3100-16-EGS-015 rev.0.pdf': 'Instalações - Esqueletos Hidráulicos e Prumadas de Água/Esgoto',
        'AÇU-3.DES-2.3100-64-EGS-008 rev.A.pdf': 'HVAC - Distribuição de Dutos e Climatização Edifício Administrativo'
    }
)

# PETROBRAS PORTARIA
processar_obra(
    r'c:\Users\Alexandre\Workspace\A11_SISTEMA_DE_GESTAO_OBRAS\projetos\OBRA_PETROBRAS_PORTARIA\01_ENGENHARIA_E_PROJETOS',
    'LOCACAO_E_ESTACAS',
    'Petrobrás - Portaria (Locação e Estacas)',
    {
        'P70069-406-DW-1430-002_1.pdf': 'Fundações - Planta Geral de Locação de Estacas (Rev 1)',
        'P70069-406-DW-1711-121_4.pdf': 'Estrutura - Forma e Armação do Bloco de Coroamento (Rev 4)',
        'P70069-406-DW-2054-101_3.pdf': 'Arquitetura - Planta Baixa da Portaria Principal (Rev 3)',
        'P70069-406-DW-2054-102_3.pdf': 'Arquitetura - Elevações e Cortes da Portaria (Rev 3)'
    }
)
