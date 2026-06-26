"""Generate printable cards for the Glyph-it board game.

Produces every valid picture pair (one glyph from each of the two blocks of a
group) as a 5 cm x 8 cm card with one picture on top and one on the bottom,
then lays the cards out on A4 pages (max cards per page) for printing.

Blocks (by bookmark id), 2 glyphs each:
    yellow = 1,2   red = 6,7   blue = 11,12
Groups (two blocks each):
    Orange = yellow x red, Green = yellow x blue, Purple = red x blue
=> 4 pairs per group, 12 cards total.

Output (in ./cards):
    page_1.png .. page_N.png   one A4 page each (300 DPI)
    cards.pdf                  all pages combined for printing
"""

from itertools import product
from pathlib import Path
from PIL import Image, ImageDraw

# ---- configuration ----------------------------------------------------------
DPI = 300
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT_DIR = ROOT / "cards"

CARD_W_MM = 50      # 5 cm wide
CARD_H_MM = 80      # 8 cm tall
A4_W_MM = 210
A4_H_MM = 297
INNER_PAD_MM = 4    # padding between picture and card edge
GAP_MM = 2          # gap between the two pictures on a card

BLOCKS = {
    "yellow": [1, 2],
    "red": [6, 7],
    "blue": [11, 12],
}
GROUPS = {
    "orange": ("yellow", "red"),
    "green": ("yellow", "blue"),
    "purple": ("red", "blue"),
}

# Border colour per group, so each card shows which group it belongs to.
GROUP_COLORS = {
    "orange": (232, 115, 28),
    "green": (47, 158, 68),
    "purple": (112, 72, 232),
}

BORDER_MM = 2          # thickness of the coloured group frame
BG_COLOR = (255, 255, 255)


def mm(value_mm: float) -> int:
    """Millimetres -> pixels at the configured DPI."""
    return round(value_mm / 25.4 * DPI)


def load_glyph(bookmark_id: int) -> Image.Image:
    img = Image.open(ASSETS / f"bookmark{bookmark_id}.png").convert("RGBA")
    return img


def fit(img: Image.Image, max_w: int, max_h: int) -> Image.Image:
    ratio = min(max_w / img.width, max_h / img.height)
    size = (max(1, round(img.width * ratio)), max(1, round(img.height * ratio)))
    return img.resize(size, Image.LANCZOS)


def build_pairs():
    """Return list of (top_id, bottom_id, group) for all 48 cards."""
    pairs = []
    for group, (block_a, block_b) in GROUPS.items():
        for top_id, bottom_id in product(BLOCKS[block_a], BLOCKS[block_b]):
            pairs.append((top_id, bottom_id, group))
    return pairs


def render_card(top_id: int, bottom_id: int, group: str, glyphs: dict) -> Image.Image:
    card_w, card_h = mm(CARD_W_MM), mm(CARD_H_MM)
    pad = mm(INNER_PAD_MM)
    gap = mm(GAP_MM)
    border_w = max(1, mm(BORDER_MM))
    border_color = GROUP_COLORS[group]

    card = Image.new("RGBA", (card_w, card_h), BG_COLOR + (255,))

    # Two equal picture regions stacked vertically (top / bottom).
    region_h = (card_h - 2 * pad - gap) // 2
    region_w = card_w - 2 * pad

    for index, glyph_id in enumerate((top_id, bottom_id)):
        glyph = fit(glyphs[glyph_id], region_w, region_h)
        region_top = pad + index * (region_h + gap)
        x = (card_w - glyph.width) // 2
        y = region_top + (region_h - glyph.height) // 2
        card.alpha_composite(glyph, (x, y))

    # Coloured frame indicating the card's group (also a cutting guide).
    draw = ImageDraw.Draw(card)
    draw.rectangle([0, 0, card_w - 1, card_h - 1],
                   outline=border_color, width=border_w)
    return card


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    glyphs = {gid: load_glyph(gid) for ids in BLOCKS.values() for gid in ids}
    pairs = build_pairs()

    card_w, card_h = mm(CARD_W_MM), mm(CARD_H_MM)
    page_w, page_h = mm(A4_W_MM), mm(A4_H_MM)

    cols = page_w // card_w
    rows = page_h // card_h
    per_page = cols * rows
    margin_x = (page_w - cols * card_w) // 2
    margin_y = (page_h - rows * card_h) // 2

    pages = []
    for start in range(0, len(pairs), per_page):
        page = Image.new("RGB", (page_w, page_h), BG_COLOR)
        for slot, (top_id, bottom_id, group) in enumerate(pairs[start:start + per_page]):
            card = render_card(top_id, bottom_id, group, glyphs)
            col = slot % cols
            row = slot // cols
            x = margin_x + col * card_w
            y = margin_y + row * card_h
            page.paste(card, (x, y), card)
        pages.append(page)

    for i, page in enumerate(pages, start=1):
        page.save(OUT_DIR / f"page_{i}.png", dpi=(DPI, DPI))

    pages[0].save(
        OUT_DIR / "cards.pdf",
        save_all=True,
        append_images=pages[1:],
        resolution=DPI,
    )

    print(f"Cards: {len(pairs)}  |  per A4 page: {per_page} ({cols} x {rows})  "
          f"|  pages: {len(pages)}")
    print(f"Output written to: {OUT_DIR}")


if __name__ == "__main__":
    main()
