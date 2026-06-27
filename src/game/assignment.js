import { seededShuffle } from './rng';
import bookmarks from '../../assets/bookmarks.json';
import words from '../../assets/words.json';

// Group -> the two blocks each group can see (hardcoded mapping).
export const GROUPS = {
  orange: { name: 'Orange', color: '#e8731c', blocks: ['yellow', 'red'] },
  green: { name: 'Green', color: '#2f9e44', blocks: ['yellow', 'blue'] },
  purple: { name: 'Purple', color: '#7048e8', blocks: ['red', 'blue'] },
};

// The shared glyph is known to EVERY team. It lives in its own "shared" block,
// is paired with each of the six block glyphs on the central cards, and its
// word is shown to all groups (so each team sees 4 block words + 1 shared = 5).
export const SHARED_BLOCK = 'shared';

// Given a 4-digit session code, deterministically assign one word to each glyph
// (the six block glyphs + the shared glyph). The same code always yields the
// same assignment on any device, with no data transmitted. The shared glyph is
// sorted last (highest id), so adding it does not change the words the six
// block glyphs receive for a given code.
//
// Returns an array of { id, image, block, word }, ordered by bookmark id.
export function buildAssignment(code) {
  const seed = parseInt(code, 10) || 0;

  const sortedBookmarks = bookmarks.slice().sort((a, b) => a.id - b.id);

  // Pick one unique word per glyph by shuffling the full word bank with the
  // seed and taking the first N. Bookmark i (sorted by id) gets word i.
  const shuffledWords = seededShuffle(words, seed).slice(0, sortedBookmarks.length);

  return sortedBookmarks.map((bookmark, index) => ({
    ...bookmark,
    word: shuffledWords[index],
  }));
}

// The shared glyph's assignment entry (known to all teams), or null.
export function sharedAssignment(assignment) {
  return assignment.find((item) => item.block === SHARED_BLOCK) || null;
}

// Filter a full assignment down to the glyphs a group can see: its two blocks
// (first block then second block, by id within each), followed by the shared
// glyph that every group knows. The shared entry is flagged with shared: true.
export function wordsForGroup(assignment, groupKey) {
  const group = GROUPS[groupKey];
  if (!group) return [];

  const blockGlyphs = group.blocks.flatMap((block) =>
    assignment
      .filter((item) => item.block === block)
      .sort((a, b) => a.id - b.id)
  );

  const shared = sharedAssignment(assignment);
  return shared ? [...blockGlyphs, { ...shared, shared: true }] : blockGlyphs;
}
