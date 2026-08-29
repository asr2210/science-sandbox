# 015 — Joint GC stratification across chr19+chr22

## What I tested
50k 200bp windows from chr19+chr22 sliding stride=50, sorted into 5
equal-quantile GC bins of the combined pool, 10k per bin. Random
orientation. Seed=42.

Bin makeup: roughly 40% chr22 + 60% chr19 in each bin (chr19 is
1.5× more abundant in candidates).

## Result — adding chr19 HURTS
- eval_01 = 0.1347 (012: 0.1367, -0.002)
- mean of evals = 0.1283 (012: 0.1308, -0.0025)
- eval_13 = 0.1360 (012: 0.1317, +0.004 — only winner)
- K562 in eval_13: 0.045 (012: ~0.041)

Most evals dropped. chr19 inclusion was net-negative even with
stratification preserving GC coverage.

## Why this may have happened
- chr19 is gene-dense and has very different sequence composition
  in non-coding regions (high CpG islands, low-complexity coding-
  adjacent regions)
- Training is small (~50k), and chr19 sequences may not match the
  eval distribution as well as chr22
- The eval test set likely uses sequences not on chr19/22, but their
  STATISTICS may be closer to chr22-style than chr19-style

This echoes 005 (random chr19+22, eval_01=0.1325 < 003's 0.1341).
Adding chr19 hurts regardless of stratification.

## Theory update
The "right" compositional reference is chr22-like, not pan-genomic.
Adding chr19 (more GC-rich, more gene-dense) shifts the training
distribution away from where the eval lives.

This is a useful negative result: **the BEST library is composed of
chr22 windows, stratified to expose GC tails, NOT a multi-chromosome
mix.**

## What to try next
016: Hybrid of 012 (GC-strat chr22) + 014 (CpG-strat chr22), 25k
each = 50k. Tests if hybrid stratification captures both per-eval
emphases without leaving chr22.
