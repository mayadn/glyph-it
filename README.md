# Glyph-it

A cross-platform mobile app (React Native + Expo) that accompanies the **Glyph-it** physical board game. Players sit together in groups; the app assigns random words to 12 visual bookmarks and reveals only the words relevant to each group.

## How it works

- **No backend, no internet, no accounts, no persistence.** Everything runs locally.
- A game is identified by a **4-digit session code** (`0000`–`9999`).
- The code is the **seed** for a deterministic shuffle (seeded Fisher-Yates on top of a `mulberry32` PRNG). The same code always produces the identical word→bookmark assignment on every device — no data is transmitted.
- The organizer taps **New Game** to generate a code; everyone else taps **Join** and enters it.

### Group → block mapping

There are 12 bookmarks split into 3 color blocks (4 each): `yellow`, `red`, `blue`. Each group sees exactly the 8 words from its two blocks:

| Group  | Blocks         | Does NOT see |
|--------|----------------|--------------|
| Orange | yellow + red   | blue words   |
| Green  | yellow + blue  | red words    |
| Purple | red + blue     | yellow words |

## Screens

1. **Home** — New Game (generates code) / Join Game (enter code). Shows the current code.
2. **Group Selection** — pick Orange, Green, or Purple. Includes Reshuffle (new code).
3. **My Words** — the group's 8 bookmarks (image thumbnail + word), ordered by block then bookmark id. Back preserves the session.

## Project structure

```
assets/
  bookmark1.png … bookmark12.png   # 12 glyph bookmark images
  bookmarks.json                   # id, image, block (color) for each bookmark
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

- Edit `assets/words.json` to change the word bank (any length ≥ 12).
- Edit `assets/bookmarks.json` to reassign which bookmark belongs to which color block. Keep 4 bookmarks per block (`yellow`, `red`, `blue`).
- Replace the `bookmarkN.png` images to use your own glyph art (keep the filenames or update both `bookmarks.json` and `src/data/images.js`).
