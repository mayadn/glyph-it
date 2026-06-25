# Print material generators

Python scripts that produce the printable game material from the glyph images
in `../assets/`. Outputs are written to `../cards/` and `../sheets/` (both are
git-ignored — they are regenerated from these scripts).

## Requirements

- Python 3
- [Pillow](https://pypi.org/project/Pillow/): `pip install Pillow`

## Scripts

### `generate_cards.py`
Generates every valid picture pair (one glyph from each of the two blocks of a
group) as a 5 cm × 8 cm card — one glyph on top, one on the bottom — with a
frame coloured by group (Orange / Green / Purple). Cards are laid out on A4
pages, max per page.

```bash
python tools/generate_cards.py
```

Output (`cards/`): `page_1.png … page_N.png` (A4, 300 DPI) + `cards.pdf`.

With 3 glyphs per block: 3×3 = 9 pairs per group → **27 cards**, 12 per A4 page → **3 pages**.

### `generate_meaning_sheet.py`
Generates an A4 worksheet: a table with one row per glyph (grouped and tinted by
block: red, yellow, blue) and columns `Glyph | Optional Meaning ×3 | Final Meaning`.

```bash
python tools/generate_meaning_sheet.py
```

Output (`sheets/`): `glyph_meanings.png` (A4, 300 DPI) + `glyph_meanings.pdf`.

## Changing the glyph set

Both scripts define the glyphs per colour block near the top of the file
(`BLOCKS` in `generate_cards.py`, `BLOCKS_ORDER` in `generate_meaning_sheet.py`),
using bookmark ids that match `assets/bookmarkN.png`. Keep these in sync with
`assets/bookmarks.json` so the app and the printed material agree. The layouts
(cards-per-page, table rows) adjust automatically to the number of glyphs.

## Printing

Print the PDFs at **100% / Actual size** (not "Fit to page") so the cards keep
their exact 5 × 8 cm dimensions.
