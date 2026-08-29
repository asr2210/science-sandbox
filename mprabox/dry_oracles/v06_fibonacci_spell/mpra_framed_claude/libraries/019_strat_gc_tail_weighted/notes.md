# 019 — Tail-weighted GC stratification (15/7.5/5/7.5/15)

## What I tested
5-bin chr22 GC quantile stratification with extra weight on extremes:
15k bin0, 7.5k bin1, 5k bin2, 7.5k bin3, 15k bin4. Total = 50k.
Random orientation. Seed=42.

## Result — slightly worse than uniform on eval_01
- eval_01 = 0.1363 (012 uniform: 0.1367, -0.0004; 013: 0.1375)
- mean of evals = 0.1297 (012: 0.1308)
- eval_04 = **0.1387** (new max for eval_04; prev 0.1385 in 014)
- eval_07 = 0.1307 (matches 014)

Per-cell-type: K562 dropped, but for eval_04 specifically K562 lifted
to 0.045 (012: 0.042).

## Interpretation
Tail-weighting doesn't help the primary. Uniform stratification is
optimal — the natural-distribution "balanced quantile bins" approach
already gives each compositional band the right amount of attention.

## Theory refinement (T18)
The right rule is **uniform quantile stratification**, not tail-
weighted. Quantile bins automatically correct for natural-distribution
imbalance (rare tails get equal weight). Pushing further toward
tails over-corrects and shifts the prediction profile.

## What to try next
020: 20-bin GC stratification (2,500 per bin). Continues to test
granularity hypothesis. 5→10 bins was +0.001 on eval_01;
10→20 bins probably won't add much but worth testing the limit.

If 020 ≈ 013 → granularity is exhausted, pivot to a new axis.
If 020 > 013 → continue finer.
