# Scoring is Pearson correlation across the 50k library

## What we know (confirmed by Exp 002)
The harness emits `ConstantInputWarning` from scipy when a homopolymer
library is submitted. This means it computes Pearson r over a 50,000-
element vector, and at least one of the two arrays in the correlation
becomes constant when sequences lack diversity.

## Implication for library design
1. **Never submit a low-diversity library** — sequences must vary enough
   that the model's per-sequence output is not constant. With 4 distinct
   sequences across 50,000, the predictions collapse to NaN.
2. **The score reflects how well structure in *my* sequences aligns with
   structure the hidden reference cares about.** Random uniform gives
   mean_r ≈ 0.13. To do better, sequences must vary in features the
   hidden scorer is sensitive to AND in a pattern that correlates with
   the reference.
3. Three conditions are averaged: `mean_r = (a + b + c) / 3`. On random,
   a == b ≈ 0 and c ≈ 0.4. Condition c is where the lift lives.

## Practical pattern
- Generate libraries with **per-sequence variation** in whatever feature
  you're probing (e.g., sample composition profiles per sequence rather
  than constant composition across the library).
- Mixing N distinct repeating patterns each repeated 50000/N times
  reduces effective N → degenerate correlation. Avoid.
- **All 4 bases must appear across the library at most positions.**
  Restricting to a 2-base or 1-base alphabet — even with 2^200 distinct
  sequences — also produces NaN. The scorer's internal feature
  representation probably has a zero-variance column for absent bases.
  This is a library-wide constraint, not a per-sequence one.

## Recipe for valid libraries
- All 50,000 sequences should be ~unique (no mass repetition of identical
  strings).
- Composition can be biased but every base 0/1/2/3 should appear at
  every position with at least small probability across the library.
- Per-sequence biases (Dirichlet) reduce the active condition (c) score
  slightly. Library-wide near-uniform composition is the safer default.

## condition_c structure (confirmed by Exp 024)
condition_c = Pearson(library per-cell base frequencies, eval reference
per-cell base frequencies). It's a per-cell-frequency correlation.

**Shape invariance**: Pearson is invariant to linear rescaling. This
explains why p in [0.4, 0.75] all give condition_c ≈ 0.41 for period-4
phase 0 — same shape, different magnitudes.

**To break the c ceiling**: must match the eval's reference SHAPE more
precisely. Adding asymmetric noise toward "next" base (Exp 017) hurt c
(wrong shape). The eval's reference is approximately period-4 phase 0
with SYMMETRIC noise — but Pearson capped at 0.41 means some extra
structure isn't captured.

**Per-cell constancy → NaN**: deterministic 4-pattern library (only 4
unique sequences) produced uniform per-cell freqs = 0.25 → condition_c
NaN despite many distinct rows. Library NEEDS per-cell freq VARIANCE
across cells (not just across rows). This is a frequency-shape requirement.

## Per-row variance breaks the c ceiling (confirmed by Exp 027-030)
condition_c is NOT purely a per-cell-freq Pearson. While shape match
matters (Exp 017/025/026 showed wrong shape hurts c), per-ROW
structure also affects c.

Recipe to break the 0.41 ceiling:
- Use per-row Dirichlet sampled noise direction/distribution.
- The library-wide per-cell freqs stay (0.7, 0.1, 0.1, 0.1), but rows
  individually have biased noise — one prefers (+1) noise, another
  prefers (+3) noise, etc.
- This lifts c from 0.41 → 0.43.

Adding per-row p variance (4-way Dirichlet over all 4 offsets) also
lifts condition_a/b from ~0.031 → 0.041.

Best design (Exp 030):
- α = (0.7, 0.1, 0.1, 0.1) over offsets {0, 1, 2, 3} per row
- Mean per-row p on template = 0.7, std = 0.32
- eval_01 = 0.1710 (vs deterministic-p baseline 0.1550)
