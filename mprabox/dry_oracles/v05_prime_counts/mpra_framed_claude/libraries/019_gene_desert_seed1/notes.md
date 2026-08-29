# Exp 019 — Gene-desert seed=1 (variance check)

## Design
Same generative process as 016 with seed=1 instead of seed=0. Variance check
on the gene-desert HepG2 lift.

## Result
**eval_01 = 0.0428; HepG2 = 0.0493.** Both DOWN from seed=0.

| metric | 016 (seed=0) | 019 (seed=1) | avg |
|--------|--------------|--------------|-----|
| eval_01 | 0.0479 | 0.0428 | 0.0454 |
| HepG2 | 0.0556 | 0.0493 | 0.0525 |
| eval_13 | 0.0384 | 0.0343 | 0.0364 |

## Interpretation — humbling
Per-seed variance is LARGER than I'd estimated. The "HepG2 lift from
gene-desert" disappears when averaged. Gene-desert HepG2 avg = 0.052 is
within noise of random hg38 HepG2 avg = 0.054 (from 003/007).

I'd been treating ~0.003 differences as signal but the per-seed variance
on per-cell-type means is at least ±0.005.

## Theory update (major correction)
- **Noise floor on per-experiment eval_01 ≈ ±0.005**, not the ±0.003 I
  estimated from 003/007 (which happened to be a low-variance pair).
- Noise on HepG2 mean ≈ ±0.005–0.007.
- Most of my "directional findings" (cCRE-fraction sweep, gene-desert
  helps HepG2) are at or below this floor.
- The robust findings remain:
  1. Real DNA > synthetic-matched (012 confirmed dramatic anti-prediction)
  2. Real DNA > sparse-motif synthetic
  3. Real DNA > dense-motif synthetic
  4. Real DNA in random/cCRE/desert form all sit in 0.04-0.05 eval_01
  5. Saturation mutagenesis HURTS (sequence diversity matters)
- Within natural DNA, the ceiling is robust.

## Next step
Variance-check the best eval_01 candidate (013, 20% cCRE) with seed=1
before declaring it the best library. If 013 holds at ≈0.049, that's
the real best. If it drops to ≈0.044, the cCRE+ "lift" is also noise.

## Time
43s wall, 12s evaluator.
