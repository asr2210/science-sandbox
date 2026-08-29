# 007 — Uniform random seed=42 (noise diagnostic)

## Setup
Same as exp 001 but seed=42 (different random draw, same distribution).

## Results
- eval_01 = 0.0410 (exp 001 was 0.0420 — diff 0.001)
- eval_08 = 0.1224 (exp 001 was 0.1242 — diff 0.0018)
- Per-cell-line diffs ≤ 0.005 in magnitude

## Inference
Score across same-distribution different random draws varies by ~0.001–0.005.
This is consistent with finite-sample Monte Carlo noise (~1/sqrt(50K) ≈ 0.0045).

So **any improvement larger than ~0.01 is real**, and small movements
(< 0.005) could be noise. Uniform random is highly reproducible at ~0.041.

This also means "best-of-multiple-seeds" lottery is ineffective: variance is too
small to gain much.
