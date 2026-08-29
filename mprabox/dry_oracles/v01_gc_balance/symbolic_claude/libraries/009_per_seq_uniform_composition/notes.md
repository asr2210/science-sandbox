# Exp 009 — Forced per-sequence uniform composition

## Design
50K sequences, each a uniformly random permutation of "0"*50 + "1"*50
+ "2"*50 + "3"*50. Per-position marginals uniform. Per-sequence
composition EXACTLY 50/50/50/50.

## Result
All NaN, with ~41 `ConstantInputWarning` from scipy.stats.pearsonr.

## Two major insights
1. **`prepare.py` rewrites sequences_0.txt.** It converts our digits
   to DNA letters and writes them back. Mapping:
       0 → A,  1 → C,  2 → G,  3 → T
   (Alphabetical.) This was verified by inspecting exp 001's
   `sequences_0.txt` after prepare.py ran — what we wrote was digits,
   but the saved file contains ACGT.

2. **Forced-identical per-sequence composition triggers NaN.** Even
   though all 50K sequences are distinct permutations, the score
   pipeline cannot compute pearson r when per-sequence composition is
   constant across the library. The TARGET vector for the correlation
   likely depends on per-sequence composition (or another aggregate
   feature), and constant target → undefined r.

## Theory refinement
Most likely scoring mechanism:
- For each condition (a, b, c) within each eval:
  - The model produces a per-sequence predicted-activity scalar (or
    vector) for our 50K sequences.
  - The TARGET is also a per-sequence value, derived from each sequence
    (probably depends on composition or similar simple features).
  - Pearson r is computed ACROSS the 50K sequences between predicted
    and target.
- Mean across (a, b, c) → mean_r per eval.

This explains:
- Monochromatic (exp 002): predicted is constant within sub-library
  but varies across; target similarly constant within → some
  computation per-condition becomes constant → NaN.
- Forced-uniform-comp (exp 009): every sequence has identical
  composition → target depends on composition → constant target →
  pearsonr NaN.
- Random uniform (exp 001): wide variation in both → r ~ 0.485.

## Practical rules
- ALWAYS ensure per-sequence composition VARIES across the library.
- Per-sequence variation is needed in whatever feature the target tracks.
- Don't force exact uniformity per sequence.
