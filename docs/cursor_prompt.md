# Cursor App Prompt: Bookmark Word Game

## Context

Build a cross-platform mobile app (React Native / Expo) to support a physical board game. Players sit together in groups; the app assigns random words to visual bookmarks and reveals only the relevant words to each group.

---

## Data Files

Place all files in `/assets/`.

| File | Description |
|------|-------------|
| `bookmarks.json` | 12 bookmark objects: `id`, `image`, `block` ("yellow"/"red"/"blue") |
| `words.json` | Array of all available words (strings) |
| `bookmark1.png` … `bookmark12.png` | Bookmark images |

### `bookmarks.json` example

```json
[
  { "id": 1,  "image": "bookmark1.png",  "block": "yellow" },
  { "id": 2,  "image": "bookmark2.png",  "block": "red"    },
  { "id": 3,  "image": "bookmark3.png",  "block": "blue"   }
]
```

---

## Group → Block Mapping (hardcoded)

```
Orange = yellow + red    → sees 8 words (NOT the 4 blue words)
Green  = yellow + blue   → sees 8 words (NOT the 4 red words)
Purple = red   + blue    → sees 8 words (NOT the 4 yellow words)
```

Each group sees **exactly 8 words** — the words assigned to their two blocks only.

---

## Session Code & Word Assignment Logic

On every app launch and on "Reshuffle": randomly pick **12 unique words** from `words.json`, shuffle, and assign one word per bookmark (by bookmark id).

### Shared session — no backend required

- The organizer presses **"New Game"** → the app generates a random 4-digit code (0000–9999) and uses it as a **seed for a deterministic shuffle algorithm** (seeded Fisher-Yates).
- The seed alone is sufficient to fully reproduce the identical word assignment on any device — no data is transmitted.
- Other players enter the same 4-digit code → their app runs the identical seeded shuffle on the same `words.json` → they see the exact same assignment.
- The code space (10,000 values) is sufficient for casual game use.

### Implementation requirement

Implement a simple seeded pseudo-random number generator (e.g. `mulberry32` or `sfc32`) so that the same seed always produces the same sequence.

> ⚠️ Do **not** use `Math.random()` for the shuffle — it is not seedable.

---

## Screens

### Screen 1 — Home

- **"New Game"** button (organizer): generates a random 4-digit code, runs the seeded shuffle, displays the code prominently
- **"Join Game"** input field (other players): enter the 4-digit code, runs the same seeded shuffle
- Current session code is displayed once generated

### Screen 2 — Group Selection

- Title: "Choose your group"
- Three large colored buttons:
  - 🟠 Orange
  - 🟢 Green
  - 🟣 Purple

### Screen 3 — My Words

- Shows group name and color
- Lists the **8 bookmarks belonging to this group's two blocks**
- Each row: bookmark image (thumbnail) + assigned word
- Sorted: first block's 4 bookmarks, then second block's 4 bookmarks (by bookmark id within each block)
- **Back button** → returns to Group Selection (session code and assignment are preserved)

---

## Technical Requirements

| Requirement | Value |
|-------------|-------|
| Framework | React Native + Expo (managed workflow) |
| Platforms | iOS + Android |
| Backend | None — no internet required |
| Auth | None — no login, no accounts |
| Persistence | None — fresh state on every launch |
| Language | English UI |
| RTL | Not needed |

---

## Files to Prepare Before Starting

| File | Action |
|------|--------|
| `bookmarks.json` | ✍️ Write this yourself (12 entries: id, image filename, block) |
| `words.json` | ✍️ Provide your full word bank |
| `bookmark1.png` … `bookmark12.png` | 🖼️ Your 12 bookmark images |
