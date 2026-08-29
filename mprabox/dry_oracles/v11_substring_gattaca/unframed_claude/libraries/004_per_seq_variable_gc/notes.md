# 004 — per-sequence variable GC (U[0.20, 0.80])

## Hypothesis
Spreading per-sequence GC across [20%, 80%] keeps the library *mean*
composition at 25% each base while widening coverage. Predict: at least
neutral, possibly helpful for some cell line.

## Setup
Per-seq target GC uniform on [0.20, 0.80]. Within seq, sample bases according
to that composition. Library-mean composition: 25.0%, 25.0%, 25.0%, 25.0%.

## Result
- eval_01: mean=**0.7512** (K562 0.7640, HepG2 0.7633, SKNSH 0.7262)
- All three cell lines DOWN vs random uniform 001 (K562 -0.067,
  HepG2 -0.116, SKNSH -0.112).

## Interpretation
Adding inter-sequence composition variance hurt EVERY cell line. So the
metric rewards uniform per-sequence composition, not library-mean uniformity.
This rules out the kNN/library-coverage theory in its naive form, and is
consistent with: each library sequence is independently scored against
something that expects ~25% per-base, and outliers drag the per-sequence
score down.

## Next
- 005: every sequence has EXACTLY 50 of each base (zero per-seq composition
  variance) — does pinning composition help or hurt vs random's small Poisson
  variance?
