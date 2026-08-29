# 014 — combo: fixed-center motif + narrow GC

## Design
Background: per-seq target GC ~ Normal(0.5, 0.02). Insertion: 1 JASPAR consensus motif at fixed center. Combines 012 + 013.

## Result
- eval_01 mean_r = **0.5196**
- K562 r = 0.9932
- HepG2 r = 0.5695
- SK-N-SH r = -0.004

## Reading
Gains did NOT stack. Below 013 (0.5206) and barely above 012 (0.5191). This suggests both individual gains were noise or that they actively interfere.

Strong evidence that we're in the noise band: random uniform variance ±0.001-0.003 absorbs everything we've tried.

## Implication
Pivot. Stop combining tiny improvements. Look at very different design ideas: extreme variants, sequence-length cassettes, real K562/HepG2/SK-N-SH ChIP-seq, etc.
