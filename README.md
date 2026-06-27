# Glyph-it

A cross-platform mobile app (React Native + Expo) that accompanies the **Glyph-it** physical board game. Players sit together in groups; the app assigns random words to 6 block glyphs plus 1 shared glyph, and reveals only the words relevant to each group (its own 4 plus the shared word).

## How it works

- **No backend, no internet, no accounts, no persistence.** Everything runs locally.
- A game is identified by a **4-digit session code** (`0000`–`9999`).
- The code is the **seed** for a deterministic shuffle (seeded Fisher-Yates on top of a `mulberry32` PRNG). The same code always produces the identical word→bookmark assignment on every device — no data is transmitted.
- The organizer taps **New Game** to generate a code; everyone else taps **Join** and enters it.

### Group → block mapping

There are 6 block glyphs split into 3 color blocks (2 each): `yellow`, `red`, `blue`. Each group sees the 4 words from its two blocks. A 7th **shared glyph** (`block: "shared"`, id `99`) is known to **every** group, so each group sees **5** words in total (its 4 + the shared word). The shared glyph also drives the 6 central "shared" cards (the shared glyph paired with each block glyph).

| Group  | Blocks         | Also sees      | Does NOT see |
|--------|----------------|----------------|--------------|
| Orange | yellow + red   | shared glyph   | blue words   |
| Green  | yellow + blue  | shared glyph   | red words    |
| Purple | red + blue     | shared glyph   | yellow words |

## Screens

1. **Home** — New Game (generates code) / Join Game (enter code). Shows the current code.
2. **Group Selection** — pick Orange, Green, or Purple. Includes Reshuffle (new code).
3. **My Words** — the group's 5 glyphs (image thumbnail + word): its 4 block glyphs ordered by block then id, followed by the shared glyph (highlighted). Back preserves the session.

## Project structure

```
assets/
  bookmark*.png                    # 6 block glyph images (ids 1,2,6,7,11,12)
  bookmark_shared.png              # the shared glyph, known to all teams (id 99)
  bookmarks.json                   # id, image, block (color) for each glyph (incl. shared)
  words.json                       # full word bank
src/
  game/rng.js                      # mulberry32 PRNG + seeded Fisher-Yates + code generator
  game/assignment.js               # group mapping + deterministic word assignment
  data/images.js                   # static require() map for bundled images
  screens/                         # Home, Group, Words
  theme.js
App.js                             # root + simple state-based navigation
```

## Run it

```bash
npm install
npm start          # then press a (Android), i (iOS), or scan the QR with Expo Go
```

Requires [Node.js](https://nodejs.org/) and the [Expo](https://docs.expo.dev/) tooling (`npm start` uses the bundled `expo` CLI). Test on a device with the **Expo Go** app or an emulator.

## Customizing the game data

- Edit `assets/words.json` to change the word bank (any length ≥ number of bookmarks).
- Edit `assets/bookmarks.json` to reassign which glyph belongs to which color block. Keep an equal number per block (`yellow`, `red`, `blue`) — currently 2 each — plus the single `shared` glyph (id `99`), which is sorted last so adding it never changes the words the six block glyphs receive for a given code.
- Replace the `bookmarkN.png` images to use your own glyph art (keep the filenames or update both `bookmarks.json` and `src/data/images.js`).


## Printable materials (`tools/`)

- `generate_cards.py` → `cards/` : 12 team cards (orange/green/purple frames) + 6 shared centre cards (gold frame: the shared glyph paired with each block glyph) = **18 cards**, laid out on A4.
- `generate_meaning_sheet.py` → `sheets/` : per-player worksheet listing every glyph (shared glyph first) with columns for tracking guessed meanings.
