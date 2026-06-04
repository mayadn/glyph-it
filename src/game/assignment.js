import { seededShuffle } from './rng';
import bookmarks from '../../assets/bookmarks.json';
import words from '../../assets/words.json';

// Group -> the two blocks each group can see (hardcoded mapping).
export const GROUPS = {
  orange: { name: 'Orange', color: '#e8731c', blocks: ['yellow', 'red'] },
  green: { name: 'Green', color: '#2f9e44', blocks: ['yellow', 'blue'] },
  purple: { name: 'Purple', color: '#7048e8', blocks: ['red', 'blue'] },
};

// Given a 4-digit session code, deterministically assign one word to each
// of the 12 bookmarks. The same code always yields the same assignment on
// any device, with no data transmitted.
//
// Returns an array of { id, image, block, word }, ordered by bookmark id.
export function buildAssignment(code) {
  const seed = parseInt(code, 10) || 0;

  // Pick 12 unique words by shuffling the full word bank with the seed
  // and taking the first 12. Bookmark i (sorted by id) gets word i.
  const shuffledWords = seededShuffle(words, seed).slice(0, 12);

  const sortedBookmarks = bookmarks.slice().sort((a, b) => a.id - b.id);

  return sortedBookmarks.map((bookmark, index) => ({
    ...bookmark,
    word: shuffledWords[index],
  }));
}

// Filter a full assignment down to the 8 bookmarks a group can see,
// ordered by the group's first block then second block (by id within each).
export function wordsForGroup(assignment, groupKey) {
  const group = GROUPS[groupKey];
  if (!group) return [];

  return group.blocks.flatMap((block) =>
    assignment
      .filter((item) => item.block === block)
      .sort((a, b) => a.id - b.id)
  );
}
