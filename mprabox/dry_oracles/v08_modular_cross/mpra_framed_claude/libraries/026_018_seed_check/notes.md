# Experiment 026 — 018 recipe stability (seed=180)

## What I tested
Identical to 018 (35-50 motif density + 15k pELS) with SEED=180.
Tests whether eval_07's 0.0109 was lucky.

## Result — CONFIRMED, eval_07 was lucky
- **eval_07: -0.0001** (was 018's 0.0109 — COLLAPSED with new seed)
- eval_08: mean=0.0087, HepG2=0.0195 (HepG2 record on eval_08)
- eval_10: mean=0.0089, SKNSH=0.0128 (SKNSH record on eval_10)
- Broad evals (01-06, 11, 14): all NEGATIVE around -0.0025
- Mean across 14 ≈ -0.0002

## What this tells me
018 recipe is MORE volatile than 012 recipe:
- 018 seed=18: mean=0.0008
- 018 seed=180: mean=-0.0002 (negative!)
- Per-eval magnitudes shuffle wildly

Compare 012 recipe:
- 012 seed=12: mean=0.0029
- 012 seed=125: mean=0.0034

**012 (low-density) is both higher-mean AND more seed-stable.**

The high-density 018 recipe creates a more chaotic per-eval
distribution. Some seeds hit gold (eval_07 in 018, eval_10/08
HepG2 in 026), some hit nothing.

## Updates to theory
**v3.17 → v3.18:** Recipe choice = balance of mean and variance.
- 012-style (15-25 motif density + pELS) = stable ~0.003-0.004 mean
- 018-style (35-50 motif density + pELS) = volatile -0.0002 to 0.001 mean

For a FINAL deployed library, choose 012-style. Lower variance, more
likely to give reproducible performance in a model-training pipeline.

## Next
Run 012 recipe with one MORE different seed (027) to get 3 data
points and a more confident estimate of the stable mean.
