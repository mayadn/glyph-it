# Print material generators

Python scripts that produce the printable game material from the glyph images
in `../assets/`. Outputs are written to `../cards/` and `../sheets/` (both are
git-ignored — they are regenerated from these scripts).

## Requirements

- Python 3
- [Pillow](https://pypi.org/project/Pillow/): `pip install Pillow`

## Scripts

### `generate_cards.py`
Generates 5 cm × 8 cm cards — one glyph on top, one on the bottom — laid out on
A4 pages, max per page. Two kinds of card:
- **12 team cards**: each pairs two glyphs from the two blocks of a group, framed
  in that group's colour (Orange / Green / Purple).
- **6 shared centre cards**: the shared glyph (id 99) paired with each block
  glyph, framed in **gold**.

```bash
python tools/generate_cards.py
```

Output (`cards/`): `page_1.png … page_N.png` (A4, 300 DPI) + `cards.pdf`.

With 2 glyphs per block: 4 pairs per group → 12 team cards + 6 shared = **18 cards**, 12 per A4 page → **2 pages**.

### `generate_meaning_sheet.py`
Generates an A4 worksheet: a table with one row per glyph (the **shared glyph
first**, then the block glyphs grouped and tinted by block: red, yellow, blue)
and columns `Glyph | Optional Meaning ×3 | Final Meaning`. With 6 block glyphs +
1 shared = 7 glyph rows.

```bash
python tools/generate_meaning_sheet.py
```

Output (`sheets/`): `glyph_meanings.png` (A4, 300 DPI) + `glyph_meanings.pdf`.

## Changing the glyph set

Both scripts define the glyphs per colour block near the top of the file
(`BLOCKS` in `generate_cards.py`, `BLOCKS_ORDER` in `generate_meaning_sheet.py`),
using bookmark ids that match `assets/bookmarkN.png`, plus the shared glyph
(`SHARED_ID = 99` → `assets/bookmark_shared.png`). Keep these in sync with
`assets/bookmarks.json` so the app and the printed material agree. The layouts
(cards-per-page, table rows) adjust automatically to the number of glyphs.

## Printing

Print the PDFs at **100% / Actual size** (not "Fit to page") so the cards keep
their exact 5 × 8 cm dimensions.
