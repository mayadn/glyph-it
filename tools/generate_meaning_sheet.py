"""Generate an A4 worksheet listing all 12 glyphs with meaning columns.

Table: 5 columns x (1 header row + one row per glyph).
  Col 1: "Glyph"           -> the 12 bookmark images, grouped by block
  Col 2: "Optional Meaning"
  Col 3: "Optional Meaning"
  Col 4: "Optional Meaning"
  Col 5: "Final Meaning"

Rows are grouped (and tinted) by block in the order: red, yellow, blue.

Output (in ./sheets):
    glyph_meanings.png   A4 page at 300 DPI
    glyph_meanings.pdf   same, for printing
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DPI = 300
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT_DIR = ROOT / "sheets"

A4_W_MM, A4_H_MM = 210, 297
MARGIN_MM = 12
CELL_PAD_MM = 3

# Block order as requested: red, yellow, blue. 3 glyphs per block.
BLOCKS_ORDER = [
    ("red", [6, 7, 8], (255, 224, 224)),
    ("yellow", [1, 2, 4], (255, 247, 205)),
    ("blue", [9, 11, 12], (219, 234, 255)),
]

HEADERS = ["Glyph", "Optional Meaning", "Optional Meaning",
           "Optional Meaning", "Final Meaning"]

HEADER_BG = (60, 57, 112)
HEADER_FG = (255, 255, 255)
GRID = (120, 120, 120)
BG = (255, 255, 255)

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"


def mm(v: float) -> int:
    return round(v / 25.4 * DPI)


def fit(img: Image.Image, max_w: int, max_h: int) -> Image.Image:
    ratio = min(max_w / img.width, max_h / img.height)
    return img.resize((max(1, round(img.width * ratio)),
                       max(1, round(img.height * ratio))), Image.LANCZOS)


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)

    n_glyphs = sum(len(ids) for _name, ids, _color in BLOCKS_ORDER)

    page_w, page_h = mm(A4_W_MM), mm(A4_H_MM)
    margin = mm(MARGIN_MM)
    pad = mm(CELL_PAD_MM)

    table_w = page_w - 2 * margin
    table_h = page_h - 2 * margin

    # Column widths: glyph column fixed, the four text columns share the rest.
    glyph_col_w = mm(34)
    text_col_w = (table_w - glyph_col_w) // 4
    col_widths = [glyph_col_w, text_col_w, text_col_w, text_col_w,
                  table_w - glyph_col_w - 3 * text_col_w]
    col_x = [margin]
    for w in col_widths:
        col_x.append(col_x[-1] + w)

    # Row heights: header row a bit shorter, then one equal row per glyph.
    header_h = mm(14)
    body_h = table_h - header_h
    row_h = body_h // n_glyphs
    # Recompute table_h so the grid is exact (avoid rounding gap at bottom).
    table_h = header_h + row_h * n_glyphs

    page = Image.new("RGB", (page_w, page_h), BG)
    draw = ImageDraw.Draw(page)

    header_font = ImageFont.truetype(FONT_BOLD, mm(4))

    # Ordered list of (block_color) per row.
    ordered = []
    for _name, ids, color in BLOCKS_ORDER:
        for gid in ids:
            ordered.append((gid, color))

    # --- header row ---
    draw.rectangle([margin, margin, margin + table_w, margin + header_h],
                   fill=HEADER_BG)
    for c in range(5):
        cx = col_x[c] + col_widths[c] // 2
        cy = margin + header_h // 2
        draw.text((cx, cy), HEADERS[c], font=header_font, fill=HEADER_FG,
                  anchor="mm")

    # --- body rows ---
    for r, (gid, color) in enumerate(ordered):
        y0 = margin + header_h + r * row_h
        y1 = y0 + row_h
        # Tint the whole row by its block color.
        draw.rectangle([margin, y0, margin + table_w, y1], fill=color)

        # Glyph image in the first column, centered.
        glyph = Image.open(ASSETS / f"bookmark{gid}.png").convert("RGBA")
        glyph = fit(glyph, glyph_col_w - 2 * pad, row_h - 2 * pad)
        gx = col_x[0] + (glyph_col_w - glyph.width) // 2
        gy = y0 + (row_h - glyph.height) // 2
        page.paste(glyph, (gx, gy), glyph)

    # --- grid lines (drawn last, on top) ---
    bottom = margin + table_h
    right = margin + table_w
    # vertical lines
    for x in col_x:
        draw.line([(x, margin), (x, bottom)], fill=GRID, width=2)
    # horizontal lines
    draw.line([(margin, margin), (right, margin)], fill=GRID, width=2)
    draw.line([(margin, margin + header_h), (right, margin + header_h)],
              fill=GRID, width=2)
    for r in range(1, n_glyphs + 1):
        y = margin + header_h + r * row_h
        draw.line([(margin, y), (right, y)], fill=GRID, width=2)

    png_path = OUT_DIR / "glyph_meanings.png"
    pdf_path = OUT_DIR / "glyph_meanings.pdf"
    page.save(png_path, dpi=(DPI, DPI))
    page.save(pdf_path, resolution=DPI)

    print(f"Table: 5 cols x {n_glyphs + 1} rows | glyphs: {n_glyphs} "
          f"| order: red, yellow, blue")
    print("Saved glyph_meanings.png and glyph_meanings.pdf in sheets/")


if __name__ == "__main__":
    main()
