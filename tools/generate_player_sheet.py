"""Generate the Glyph-it player board (knowledge-tracking sheet).

Each team uses one board to record glyph meanings and track which team knows
which glyph. The board lists every glyph (the shared glyph first, then the
block glyphs grouped/tinted by block), a write-in "Meaning" line, a
knows-matrix for the three teams (Orange / Purple / Green), and a ROUNDS log.

The shared glyph is known to ALL teams, so its row is ticked for all three.

Outputs (in ./sheets):
    glyph_it_player_sheet_A6.pdf        one A6 board (+ .png preview)
    glyph_it_player_sheet_A4_4up.pdf    four A6 boards tiled on A4 (with cut guides)
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DPI = 300
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT_DIR = ROOT / "sheets"

SHARED_ID = 99
SHARED_IMAGE = "bookmark_shared.png"

# Colours -------------------------------------------------------------------
HEADER_BG = (60, 57, 112)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GREY = (130, 130, 130)
DASH = (175, 175, 175)
GRID = (205, 205, 205)

TEAM_COLORS = {
    "orange": (232, 115, 28),
    "purple": (112, 72, 232),
    "green": (47, 158, 68),
}

# Per-block: row tint + meaning-underline colour.
BLOCK_TINT = {
    "shared": (245, 232, 199),
    "blue": (219, 234, 255),
    "yellow": (255, 247, 205),
    "red": (255, 224, 224),
}
LINE_COLOR = {
    "shared": (171, 140, 48),
    "blue": (70, 120, 190),
    "yellow": (176, 140, 40),
    "red": (200, 70, 70),
}

# Knowledge matrix: which team knows a glyph of each block.
KNOWS = {
    "shared": {"orange": True, "purple": True, "green": True},
    "yellow": {"orange": True, "purple": False, "green": True},
    "red": {"orange": True, "purple": True, "green": False},
    "blue": {"orange": False, "purple": True, "green": True},
}

# Row order: shared first, then blue, yellow, red (block ids from bookmarks).
ROWS = [
    ("shared", SHARED_ID),
    ("blue", 11), ("blue", 12),
    ("yellow", 1), ("yellow", 2),
    ("red", 6), ("red", 7),
]

FONT_BOLD = ["C:/Windows/Fonts/arialbd.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]
FONT_REG = ["C:/Windows/Fonts/arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]


def _font(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def mm(v):
    return round(v / 25.4 * DPI)


def glyph_filename(gid):
    return SHARED_IMAGE if gid == SHARED_ID else f"bookmark{gid}.png"


def fit(img, max_w, max_h):
    r = min(max_w / img.width, max_h / img.height)
    return img.resize((max(1, round(img.width * r)), max(1, round(img.height * r))),
                      Image.LANCZOS)


def draw_check(draw, cx, cy, color):
    w = mm(0.8)
    draw.line([(cx - mm(1.7), cy + mm(0.1)), (cx - mm(0.5), cy + mm(1.4))],
              fill=color, width=w)
    draw.line([(cx - mm(0.5), cy + mm(1.4)), (cx + mm(1.9), cy - mm(1.5))],
              fill=color, width=w)


def draw_dash(draw, cx, cy):
    draw.line([(cx - mm(1.6), cy), (cx + mm(1.6), cy)], fill=DASH, width=mm(0.8))


def render_board():
    """Render one A6 player board and return it as an RGB image."""
    W, H = mm(105), mm(148)
    board = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(board)

    f_title = _font(FONT_BOLD, mm(6.5))
    f_team_lbl = _font(FONT_REG, mm(3.0))
    f_colhead = _font(FONT_BOLD, mm(2.7))
    f_letter = _font(FONT_BOLD, mm(3.4))
    f_rounds = _font(FONT_BOLD, mm(3.6))
    f_small = _font(FONT_REG, mm(2.6))

    # --- header band ---
    draw.rectangle([0, 0, W, mm(13)], fill=HEADER_BG)
    draw.text((mm(5), mm(6.5)), "GLYPH-IT", font=f_title, fill=WHITE, anchor="lm")
    draw.text((W - mm(33), mm(6.5)), "my team:", font=f_team_lbl, fill=WHITE, anchor="lm")
    draw.line([(W - mm(18), mm(8.2)), (W - mm(5), mm(8.2))], fill=WHITE, width=mm(0.4))

    # --- column geometry ---
    ml, mr = mm(4), mm(4)
    letter_cx = mm(6)
    glyph_x0, glyph_x1 = mm(9), mm(26)
    meaning_x0, meaning_x1 = mm(29), mm(62)
    team_cx = {"orange": mm(71), "purple": mm(85), "green": mm(98)}

    # --- column header row ---
    chy = mm(16.5)
    draw.text(((glyph_x0 + glyph_x1) // 2, chy), "Glyph", font=f_small, fill=GREY, anchor="mm")
    draw.text((meaning_x0, chy), "Meaning", font=f_small, fill=GREY, anchor="lm")
    for team in ("orange", "purple", "green"):
        draw.text((team_cx[team], chy), team.upper(), font=f_colhead,
                  fill=TEAM_COLORS[team], anchor="mm")

    # --- glyph rows ---
    rows_top, rows_bottom = mm(19), mm(104)
    n = len(ROWS)
    row_h = (rows_bottom - rows_top) / n
    letters = "abcdefg"
    for i, (block, gid) in enumerate(ROWS):
        y0 = round(rows_top + i * row_h)
        y1 = round(rows_top + (i + 1) * row_h)
        cy = (y0 + y1) // 2
        draw.rectangle([0, y0, W, y1], fill=BLOCK_TINT[block])

        draw.text((letter_cx, cy), letters[i], font=f_letter, fill=BLACK, anchor="mm")

        glyph = Image.open(ASSETS / glyph_filename(gid)).convert("RGBA")
        glyph = fit(glyph, glyph_x1 - glyph_x0, (y1 - y0) - mm(1.5))
        gx = (glyph_x0 + glyph_x1) // 2 - glyph.width // 2
        gy = cy - glyph.height // 2
        board.paste(glyph, (gx, gy), glyph)

        draw.line([(meaning_x0, cy + mm(2.2)), (meaning_x1, cy + mm(2.2))],
                  fill=LINE_COLOR[block], width=mm(0.45))

        for team in ("orange", "purple", "green"):
            if KNOWS[block][team]:
                draw_check(draw, team_cx[team], cy, TEAM_COLORS[team])
            else:
                draw_dash(draw, team_cx[team], cy)

    # --- ROUNDS log ---
    ry = mm(107)
    draw.text((ml, ry), "ROUNDS", font=f_rounds, fill=BLACK, anchor="lm")
    sub_y = ry + mm(5)
    team_col_x, notes_col_x = ml, mm(34)
    draw.text((team_col_x, sub_y), "Team", font=f_small, fill=GREY, anchor="lm")
    draw.text((notes_col_x, sub_y), "Notes", font=f_small, fill=GREY, anchor="lm")
    first_line = ry + mm(9)
    n_lines = 6
    gap = mm(5)
    for k in range(n_lines + 1):
        y = first_line + k * gap
        draw.line([(ml, y), (W - mr, y)], fill=GRID, width=mm(0.3))
    draw.line([(notes_col_x - mm(2), first_line - mm(4)),
               (notes_col_x - mm(2), first_line + n_lines * gap)],
              fill=GRID, width=mm(0.3))

    return board


def dashed_line(draw, p0, p1, color, width, dash=14, gap=10):
    import math
    x0, y0 = p0
    x1, y1 = p1
    length = math.hypot(x1 - x0, y1 - y0)
    if length == 0:
        return
    ux, uy = (x1 - x0) / length, (y1 - y0) / length
    pos = 0.0
    while pos < length:
        a = (x0 + ux * pos, y0 + uy * pos)
        b = (x0 + ux * min(pos + dash, length), y0 + uy * min(pos + dash, length))
        draw.line([a, b], fill=color, width=width)
        pos += dash + gap


def main():
    OUT_DIR.mkdir(exist_ok=True)
    board = render_board()

    # A6 outputs
    a6_png = OUT_DIR / "glyph_it_player_sheet_A6.png"
    a6_pdf = OUT_DIR / "glyph_it_player_sheet_A6.pdf"
    board.save(a6_png, dpi=(DPI, DPI))
    board.save(a6_pdf, resolution=DPI)

    # A4 4-up: tile four boards (2x2) centred, with dashed cut guides.
    a4 = Image.new("RGB", (mm(210), mm(297)), WHITE)
    bw, bh = board.size
    off_x = (mm(210) - 2 * bw) // 2
    off_y = (mm(297) - 2 * bh) // 2
    for r in range(2):
        for c in range(2):
            a4.paste(board, (off_x + c * bw, off_y + r * bh))
    d = ImageDraw.Draw(a4)
    dashed_line(d, (off_x + bw, off_y), (off_x + bw, off_y + 2 * bh), GREY, mm(0.3))
    dashed_line(d, (off_x, off_y + bh), (off_x + 2 * bw, off_y + bh), GREY, mm(0.3))
    a4_pdf = OUT_DIR / "glyph_it_player_sheet_A4_4up.pdf"
    a4.save(a4_pdf, resolution=DPI)

    print(f"Player board: {len(ROWS)} glyphs (incl. shared).")
    print("Saved glyph_it_player_sheet_A6.pdf/.png and "
          "glyph_it_player_sheet_A4_4up.pdf in sheets/")


if __name__ == "__main__":
    main()
