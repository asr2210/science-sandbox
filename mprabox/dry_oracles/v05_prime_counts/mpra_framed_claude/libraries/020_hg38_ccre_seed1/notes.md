# Exp 020 — 013 design (40K rand + 10K cCRE) with seed=1

## Design
Variance check on the best eval_01 library. Same as 013 except seed=1.

## Result
**eval_01 = 0.0487; HepG2 = 0.0534.** Very close to seed=0.

| metric | 013 (seed=0) | 020 (seed=1) | avg |
|--------|--------------|--------------|-----|
| eval_01 | 0.0493 | 0.0487 | **0.0490** |
| HepG2 | 0.0535 | 0.0534 | **0.0535** |
| eval_13 | 0.0363 | 0.0347 | 0.0355 |

## Interpretation
013 design is robust across seeds. Per-seed variance is ~0.001 on eval_01
and HepG2 mean — much smaller than gene-desert's variance (±0.005).

So 013 is the robust best:
- eval_01 = 0.049 (above 010 random's 0.048 and gene-desert's 0.045 avg)
- HepG2 = 0.054 (essentially tied with gene-desert avg 0.053)

## Theory update
- The 013 sweet-spot design (80% rand hg38 + 20% cCRE) is genuinely
  the best natural-DNA library design tested.
- Different libraries have different variance: 013 is low-variance,
  gene-desert is high-variance. Possibly because cCRE-centered sampling
  has small N_eff (1M cCREs, no resampling within), while gene-desert
  picks from a much larger genomic pool where sample-to-sample
  composition can drift.

## Next step
Explore designs with explicit ACTIVITY CONTRAST: combine putative-active
(cCRE) + putative-silent (gene-desert) + mid-activity (random). The
model may benefit from explicit dynamic-range labels.

## Time
42s wall, 12s evaluator.
