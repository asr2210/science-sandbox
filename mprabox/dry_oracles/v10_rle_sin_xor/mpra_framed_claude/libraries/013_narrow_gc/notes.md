# 013 — random with per-seq target GC ~ Normal(0.5, 0.02)

## Design
Per-sequence target GC drawn from clipped Normal(0.5, 0.02). Each sequence then sampled with that target (A=T=(1-gc)/2, C=G=gc/2). Realized GC: mean=0.501, std=0.040 (vs ~0.035 for pure binomial).

## Result
- eval_01 mean_r = **0.5206** (vs random uniform 0.5177; **best so far**)
- K562 r = 0.9946 (kept high)
- HepG2 r = 0.5676 (up from 0.557)
- SK-N-SH r = -0.001

## Reading
Slightly above noise — best result so far. The realized GC distribution is barely wider than pure binomial (std 0.040 vs 0.035), so the effective change is small. Yet the gain is consistent across most eval sets.

May suggest that a tiny per-seq GC perturbation helps the model see GC-importance signal explicitly. Or pure noise.

## Implication
Try combining: fixed-center motif (012) + narrow GC (013) as exp 014. If gains stack, we have a real signal. If they don't, we're chasing noise.
