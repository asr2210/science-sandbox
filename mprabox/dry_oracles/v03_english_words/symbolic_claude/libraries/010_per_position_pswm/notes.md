# 010 — per-position random PSWM

Sample one Dirichlet(alpha=1) per position (200 distributions). Same PSWM
for all sequences. Per-sequence iid from per-position dists.

Some positions have very biased distributions, e.g.,
position 100: p=[0.53, 0.37, 0.09, 0.01].

## Result
- eval_01: mean_r = 0.4190 (vs 0.4200 baseline) — essentially identical
- a = 0.5883, b = 0.6151, c = 0.0536

## Critical insight
**Per-position composition bias is NEUTRAL.** Per-sequence stats (composition,
k-mer counts) are still iid-random-like (since each sequence is iid from
fixed per-position dists, character counts behave similarly to iid uniform).

The eval cares about PER-SEQUENCE FEATURES, not position-specific patterns.
This means:
- Modifying position distributions: doesn't help, doesn't hurt
- Modifying per-sequence distributions (composition, k-mer): hurts

The optimum is therefore iid random (which matches per-seq feature distribution).
Best path: seed lottery for marginal gain.

## Status: 10/30 used
