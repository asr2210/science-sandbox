# 023_more_regions_wider

## Design
10K cCREs × 5 wider-offset tiles (±400bp) = 50K. Doubles region
count vs 020/021/022 while keeping per-region tile count low.

## Result
                eval_01  K562    HepG2   SKNSH   eval_07  eval_13
014 narrow:     0.3181   0.144   0.188   0.623   0.337    0.328
020 wider:      0.3216   0.144   0.200   0.621   0.338    0.331
021 wider+RC:   0.3222   0.145   0.200   0.622   0.340    0.330
022 wider 800:  0.3221   0.143   0.202   0.621   0.338    0.333
023 wider 10K:  0.3215   0.144   0.200   0.621   0.340    0.331

Parity with 020. The saturation point under wider tiling is the
SAME as under narrow tiling (~5K diverse regions). More regions
do not help; per-region context breadth is the binding lever.

## Interpretation
The wider-tile lever (020) and the region-count lever (008/014)
are NOT interacting. Wider tiles don't open up additional region
capacity. The model has a fixed "regulatory grammar capacity" of
~5K regions × N tiles regardless of context breadth.

This suggests the wider-tile lift is NOT about "richer per-region
information enabling more regions to fit" but about teaching a
NEW SKILL (context inference) that lifts every example.

## Theory T15
The ceiling moves only when we add SKILLS, not when we add data.
Two skill axes found:
- Context breadth (±400 wider) — +0.004
- Strand invariance (RC alone) — +0.001 (subsumed when wider)
The next ceiling-lifting intervention must teach a NEW SKILL.

## Open hypothesis for the wider-tile lift mechanism
Wider tiles may work because they create NATURAL POS/NEG pairing
within each cCRE: some tiles hit the core, others hit flank +
non-functional DNA. The model implicitly contrasts and learns
"what makes the core different from the flank."

## Next
Experiment 024: explicit POS/NEG pairing from real genome.
5K cCREs × 5 narrow tiles (positives) + 5K random non-cCRE
genomic windows × 5 tiles (paired negatives, far from any cCRE)
= 50K. Tests whether explicit positive/negative pairing matches
or beats the wider-tile lift (which may be implicit pairing).
