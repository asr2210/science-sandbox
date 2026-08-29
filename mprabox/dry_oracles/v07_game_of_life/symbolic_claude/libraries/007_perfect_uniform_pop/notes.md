# 007 — Perfectly uniform per-position distribution

50k sequences with exactly 12,500 of each char {0,1,2,3} at every position.

## Result
- eval_01: 0.3938 (vs random 0.3943)
- Essentially identical to uniform random across all evals.

## Interpretation
Poisson noise in uniform random doesn't matter — the score is invariant to it.
So the "0.39 ceiling" for unstructured uniform sequences is robust.

## Conjunction with earlier results
- exp 001 (random uniform): 0.3943
- exp 003 (4 blocks 70% biased, pop_mean = uniform): 0.3296
- exp 007 (per-pos perfect uniform): 0.3938

Both 001 and 007 have ≈ uniform per-position population (with/without Poisson noise),
yet 003 also has uniform per-position population but scores lower. This means:
**the score does NOT depend only on per-position population mean.**

It must depend on either:
- Per-sequence composition (each sequence's individual bias)
- Higher-order population statistics (covariance across positions, etc.)

## Next probe
Try a template-following library: 50k sequences each 90% matching a fixed random base
template, 10% noise. Per-position pop is 90% base char + 10% other. Tests if matching
a fixed (random) template across all sequences helps.
