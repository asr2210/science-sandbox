# 008 — Uniform random, different seed

## Hypothesis
If uniform random is the ceiling for "composition + insertion" strategies,
re-seeding should give nearly the same score. Differences > ~0.01 on eval_01
would suggest seed-luck is significant.

## Results
eval_01 = 0.3183 (vs 0.3157 in 001). Diff 0.003 — noise.
eval_04: +0.044 between seeds (seed-sensitive).
eval_07: -0.056 between seeds (seed-sensitive).
eval_08: +0.003 (very stable).

## Implication
eval_01 noise floor ≈ ±0.005. Improvements smaller than 0.01 on eval_01 are
unreliable. Some other evals (04, 07) are noisy enough to benefit from
seed selection, but eval_01 is mostly indifferent to RNG seed.

## Next
Test whether tighter per-sequence composition (exactly 50 of each base)
helps. Then escalate to real-biology downloads.
