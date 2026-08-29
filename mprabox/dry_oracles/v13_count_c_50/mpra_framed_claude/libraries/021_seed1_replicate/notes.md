# 021 — Seed=1 replicate of exp 020 (noise estimation)

**Goal:** Determine if recent fine-tuning gains (+0.0001 to +0.0004
each) are real or seed noise.

**Design:** Identical exp 020 config, only SEED=1 (vs seed=0).

**Results vs exp 020 (seed=0):**
- eval_01:    0.5777 (-0.001)
- eval_04/09: 0.5629 (-0.004) ← biggest gap (after eval_08)
- eval_07:    0.6180 (+0.001)
- eval_08:    0.1691 (-0.005) ← largest variance
- eval_13:    0.5975 (+0.001)
- eval_10:    0.5154 (+0.001)
- Mean:       **0.5456** (-0.001 vs exp 020)

**Findings (CRITICAL):**

Per-eval seed variance:
- Most evals: ±0.001
- eval_04/09: ±0.004
- eval_08:    ±0.005

Mean variance: ±0.001 between seeds.

**Implication:** My fine-tuning differences (0.0001-0.0004) are
WITHIN noise. The "NEW BEST" labels on exp 016/018/019/020 are
statistically meaningless — they're all in a ~0.546 cluster.

Real improvements (likely significant):
- exp 010 (+CpGi) → +0.003 over exp 007: PROBABLY REAL
- exp 013-020 (synthetic, windowing): WITHIN NOISE

The exp 020 library is still the best-of-cluster. But I should look
for changes that give >0.003 mean change to be confident.

**Plan exp 022:** Big swing — random-offset cCRE windowing. 20k
unique cCREs × 1 random offset each (vs exp 019's 4k × 5 fixed).
Tests whether anchor breadth with random positions matches per-anchor
fixed-offset diversity.
