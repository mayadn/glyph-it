// Seeded pseudo-random number generator (mulberry32).
// Deterministic: the same seed always produces the same sequence,
// which lets every device reproduce the identical word assignment
// from just the 4-digit session code. Do NOT use Math.random() here.

export function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Seeded Fisher-Yates shuffle. Returns a new array; does not mutate input.
export function seededShuffle(array, seed) {
  const rng = mulberry32(seed);
  const result = array.slice();
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

// Generate a random 4-digit session code (0000-9999) as a string.
// Uses Math.random here only to pick the seed itself, which is fine —
// the seed is shared explicitly via the code, not the shuffle output.
export function generateSessionCode() {
  const n = Math.floor(Math.random() * 10000);
  return String(n).padStart(4, '0');
}
