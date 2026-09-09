import os
import sys
import glob
import argparse
import pymupdf

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def extrair_carimbos(dir_path, output_dir=None, crop_x_pct=0.35, crop_y_pct=0.35, dpi=150):
    """
    Recorta o carimbo (canto inferior direito) de todas as pranchas em PDF de um diretório.
    Reduz significativamente o tempo de processamento e consumo de tokens em IA.
    """
    if not os.path.exists(dir_path):
        print(f"[ERRO] Diretório não encontrado: {dir_path}")
        return []

    if output_dir is None:
        output_dir = os.path.join(dir_path, "_carimbos_extraidos")
    os.makedirs(output_dir, exist_ok=True)

    pdf_files = glob.glob(os.path.join(dir_path, "*.pdf"))
    if not pdf_files:
        print(f"[AVISO] Nenhum arquivo PDF encontrado em: {dir_path}")
        return []

    resultados = []
    print(f"[INFO] Processando {len(pdf_files)} arquivos em '{dir_path}'...")

    for path in sorted(pdf_files):
        filename = os.path.basename(path)
        try:
            doc = pymupdf.open(path)
            page = doc[0]
            r = page.rect

            # Define retângulo do carimbo no canto inferior direito
            # x0: (1 - crop_x_pct) * largura, y0: (1 - crop_y_pct) * altura
            x0 = r.width * (1.0 - crop_x_pct)
            y0 = r.height * (1.0 - crop_y_pct)
            x1 = r.width
            y1 = r.height

            clip_rect = pymupdf.Rect(x0, y0, x1, y1)

            # Extrai imagem recortada do carimbo
            pix = page.get_pixmap(clip=clip_rect, dpi=dpi)
            out_fname = os.path.splitext(filename)[0] + "_carimbo.png"
            out_path = os.path.join(output_dir, out_fname)
            pix.save(out_path)

            # Tenta extrair texto existente na região do carimbo
            texto_carimbo = page.get_text("text", clip=clip_rect).strip()

            resultados.append({
                "pdf": filename,
                "carimbo_img": out_path,
                "texto": texto_carimbo
            })
            print(f"  [OK] {filename:<45} -> {out_fname}")
        except Exception as e:
            print(f"  [ERRO] {filename}: Erro ao processar ({e})")

    print(f"\n[SUCESSO] Concluído! {len(resultados)} carimbos salvos em: {output_dir}\n")
    return resultados

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recorta o carimbo (canto inferior direito) de desenhos PDF.")
    parser.add_argument("dir_path", help="Caminho do diretório contendo os PDFs")
    parser.add_argument("--output-dir", help="Diretório de saída para as imagens (opcional)")
    parser.add_argument("--crop-x", type=float, default=0.35, help="Porcentagem de corte na largura a partir da direita (padrão: 0.35)")
    parser.add_argument("--crop-y", type=float, default=0.35, help="Porcentagem de corte na altura a partir do fundo (padrão: 0.35)")
    parser.add_argument("--dpi", type=int, default=150, help="Resolução DPI da imagem gerada (padrão: 150)")

    args = parser.parse_args()
    extrair_carimbos(args.dir_path, args.output_dir, args.crop_x, args.crop_y, args.dpi)
