# 004_gc_gradient

## What
50K sequences. Each sequence's GC% drawn uniformly from [0.20, 0.80] target. Pure A/C/G/T, no motifs. Realized GC range: 0.13–0.92, std 0.177.

## Why
Test smooth, naturally-distributed variance along a single biological axis (GC content).

## Results
**eval_01: 0.392** (vs random 0.156, +150%)
- K562_r: 0.447 (vs 0.314)
- HepG2_r: 0.348 (vs 0.033) — 10x improvement
- SKNSH_r: 0.382 (vs 0.121) — 3x improvement

Other notable:
- eval_07: -0.11 → +0.44 (FLIPPED)
- eval_13: -0.11 → +0.42 (FLIPPED)
- eval_08: 0.58 → 0.20 (DROPPED — eval_08 dislikes GC variance)

## Interpretation
GC content variance is THE dominant signal both models agree on. The "natural" K562_r of 0.31 from random was mostly residual GC-axis noise; widening the GC distribution from std ≈ 0.035 to 0.177 nearly tripled the eval_01 score.

eval_08 appears to be the inverse — it favors libraries with LOW compositional variance (or rewards a different feature). Trade-off: optimizing eval_01 hurts eval_08.

## Next
- Push GC range wider [0.05, 0.95].
- Add CpG dinucleotide variance as an orthogonal axis.
- Try other compositional axes (CG vs AT-only sequences).
