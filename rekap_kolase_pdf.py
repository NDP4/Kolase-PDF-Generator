import argparse
from fpdf import FPDF
from PIL import Image
import os
import math
import sys

def create_pdf_collage(input_folder, output_pdf, cols=2, rows=3, margin=10, gap=5):
    # Konfigurasi grid dan ukuran halaman
    PAGE_WIDTH = 210  # mm
    PAGE_HEIGHT = 297  # mm
    
    IMAGE_BOX_WIDTH = (PAGE_WIDTH - 2 * margin - (cols - 1) * gap) / cols
    IMAGE_BOX_HEIGHT = (PAGE_HEIGHT - 2 * margin - (rows - 1) * gap) / rows

    # Validasi folder input
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"Folder tidak ditemukan: {input_folder}")

    images = sorted([
        img for img in os.listdir(input_folder)
        if img.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    if not images:
        raise ValueError(f"Tidak ada file gambar yang ditemukan di {input_folder}")

    pdf = FPDF(unit="mm", format="A4")
    pdf.set_auto_page_break(0)

    # Bagi gambar ke dalam kelompok
    chunks = [images[i:i + rows * cols] for i in range(0, len(images), rows * cols)]

    for chunk in chunks:
        pdf.add_page()

        for index, img_name in enumerate(chunk):
            img_path = os.path.join(input_folder, img_name)
            img = Image.open(img_path)

            col = index % cols
            row = index // cols

            x = margin + col * (IMAGE_BOX_WIDTH + gap)
            y = margin + row * (IMAGE_BOX_HEIGHT + gap)

            # Hitung ukuran gambar yang proporsional
            img_w, img_h = img.size
            aspect = img_h / img_w
            box_aspect = IMAGE_BOX_HEIGHT / IMAGE_BOX_WIDTH

            if aspect > box_aspect:
                display_h = IMAGE_BOX_HEIGHT
                display_w = display_h / aspect
            else:
                display_w = IMAGE_BOX_WIDTH
                display_h = display_w * aspect

            x_offset = x + (IMAGE_BOX_WIDTH - display_w) / 2
            y_offset = y + (IMAGE_BOX_HEIGHT - display_h) / 2

            pdf.image(img_path, x=x_offset, y=y_offset, w=display_w, h=display_h)

    pdf.output(output_pdf)
    print(f"PDF berhasil dibuat: {output_pdf}")

def main():
    parser = argparse.ArgumentParser(description='Membuat kolase PDF dari gambar-gambar')
    parser.add_argument('--input', '-i', type=str, help='Folder input yang berisi gambar-gambar')
    parser.add_argument('--output', '-o', type=str, help='File output PDF')
    parser.add_argument('--cols', type=int, default=2, help='Jumlah kolom (default: 2)')
    parser.add_argument('--rows', type=int, default=3, help='Jumlah baris (default: 3)')
    parser.add_argument('--margin', type=int, default=10, help='Margin halaman dalam mm (default: 10)')
    parser.add_argument('--gap', type=int, default=5, help='Jarak antar gambar dalam mm (default: 5)')

    args = parser.parse_args()

    # Gunakan nilai default jika tidak ada argumen yang diberikan
    input_folder = args.input or "file_gambar"
    output_pdf = args.output or "rekap_bukti_transfer_kolase.pdf"

    try:
        create_pdf_collage(
            input_folder,
            output_pdf,
            cols=args.cols,
            rows=args.rows,
            margin=args.margin,
            gap=args.gap
        )
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    try:
        from rekap_kolase_gui import main as gui_main
        gui_main()  # Run GUI version by default
    except ImportError as e:
        print("GUI dependencies not found, falling back to command line version")
        main()  # Run command line version as fallback
