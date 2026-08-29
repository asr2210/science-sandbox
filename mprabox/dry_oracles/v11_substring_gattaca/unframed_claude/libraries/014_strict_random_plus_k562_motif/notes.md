# 014 — 25k strict + 25k (random + 1 K562 motif each)

## Result
- eval_01 mean=**0.8811** (K562 0.8525, HepG2 0.9112, SKNSH 0.8795)
- vs 012 (SKNSH motif): K562 0.852 = same, HepG2 0.907 → 0.911 (+0.004),
  SKNSH 0.878 → 0.880 (+0.002). Generic, not K562-specific lift.
- vs 007 (no motif): mean +0.003.

## Interpretation
Surprisingly, the "K562 motif" basket (AGATAAG/CCACGCCC/TGACTCAG) does NOT
specifically lift K562 — instead it gives a slight all-cell-line boost.
This suggests the lift mechanism is not cell-line-specific TF binding
recognition; rather, the inserted motif acts as a generic structured
perturbation of the random background. K562 motifs are GC-rich short
sequences; possibly any such structured insert at low dose gives this
generic lift.

## Next
- 015: insert 1 motif drawn from a diverse 9-pool (K562+SKNSH+universal),
  random per seq. Tests if motif diversity adds beyond cell-line uniformity.
- 016: try a single universal motif (e.g., CACGTG MYC E-box) per seq. Tests
  if motif identity matters.
- 017: combine best motif config + something on the strict half.
