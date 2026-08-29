# Exp 004 — exactly balanced composition + random ordering

## Design
50,000 sequences, each containing exactly 50 of each base (0,1,2,3),
ordered by independent random permutation per sequence.

## Result
eval_01 mean_r = 0.1243 (vs random baseline 0.1272). condition_c = 0.3685.
Effectively identical to uniform random.

## Interpretation
Composition variance (the small binomial wiggle in random uniform) is
NOT the lever — clamping composition to exactly balanced gives the same
score. The active scorer (condition_c) is reading something *positional*
or *motif-level*, not per-base counts.

## What changed vs baseline
- eval_07 dropped from 0.1514 → 0.1276 (notable shift).
- eval_06/11 roughly preserved.
- Suggests eval_07 reads something composition-variance-sensitive that
  the others don't.

## Next
Probe **subset-restricted bases** — e.g., sequences using only bases
{0, 2}. If much different from baseline, we have a directional lever
on base preferences. The "v02/alternating-purine" directory naming
elsewhere on disk hints that purine-like (pair) structures may be
rewarded.
