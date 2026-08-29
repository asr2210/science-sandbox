# 026 — Block-stratified strict (4-bp per-block balanced) + insert-rand

## Hypothesis
Tighter local composition (every 4-bp window has ACGT once each) might
push K562/HepG2 above strict's ceiling.

## Result
- eval_01 mean=**0.8185** (K562 0.8163, HepG2 0.8477, SKNSH 0.7913)
- vs 017: mean -0.064. K562 -0.046, HepG2 -0.064, SKNSH -0.081.

## Interpretation
Disastrous. Block-stratification creates too much local repetition —
every 4-bp window is a permutation of ACGT, which produces high
short-range autocorrelation that crashes all 3 cell lines.

## Lesson
Strict's value comes from GLOBAL balance + LOCAL randomness. Removing
local randomness destroys it.

## Next
027: push bank size to 200 (test K562 trend continuation).
