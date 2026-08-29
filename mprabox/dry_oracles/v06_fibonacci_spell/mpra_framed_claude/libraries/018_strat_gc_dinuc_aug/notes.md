# 018 — GC-strat chr22 + dinuc-shuffle augmentation

## What I tested
25,000 unique chr22 windows (5 GC bins × 5,000 each), each written
TWICE: once as natural sequence and once as Altschul-Erickson
dinucleotide-shuffled. Total = 50,000. Random orientation. Seed=42.

## Result — matches 012 on eval_01, lifts a couple evals
- eval_01 = 0.1367 (012: 0.1367 — tied exactly)
- mean of evals = 0.1296 (012: 0.1308, -0.001)
- eval_13 = **0.1371** (012: 0.1317, +0.005 — biggest improvement)
- eval_06 = 0.1380 (012: 0.1374, +0.001)
- K562 in eval_13: 0.052 (012: ~0.041, big jump)

## Interpretation
Dinuc-shuffle augmentation gives the model 2× sequence variety at
the same compositional content per bin. It doesn't lift the primary
(eval_01) above its plateau, but adds variety to specific evals (eval_13
in particular, which seems sensitive to sequence diversity at fixed
dinuc composition).

This is consistent with T16: the model learns compositional statistics
and is largely insensitive to higher-order structure. Adding shuffled
versions doesn't break this; it just doubles the available training
patterns at each composition.

## Theory update
Dinuc-shuffle augmentation is a "free" technique: not hurting,
slightly helping per-eval variability. May be worth keeping as a
component in future designs.

The eval_01 plateau at 0.137 is robust to multiple chr22-stratified
strategies. Likely the model capacity/training is the bottleneck,
not the library, at this regime.

## What to try next
019: Tail-weighted GC stratification. Instead of uniform 10k per bin,
push 15k into the extreme bins (0 and 4) and 7.5k into bins 1 and 3
and 5k into bin 2. Tests if EXTRA tail coverage extracts more benefit.
