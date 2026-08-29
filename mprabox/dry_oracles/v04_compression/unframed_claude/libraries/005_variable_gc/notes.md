# 005 — Variable per-sequence GC

## Hypothesis
Per-sequence GC ∈ [0.2, 0.8] gives the library wide between-sequence GC variance.
- If metric likes library diversity → score UP
- If metric demands genome-like composition → score DOWN

## Results
eval_01 = **0.2607** (random=0.3157). Drop.

## Update to theory
Confirmed: metric demands narrow 50% GC composition. ALL deviations from
uniform-random 50%-GC hurt. So our "best library" remains exp 001 (random
uniform). To improve, we need to add structure that the model recognizes
WHILE keeping 50% GC and per-sequence diversity.

## Next
Exp 006: first-order Markov chain mimicking human dinucleotide stats.
Preserves 50% GC but adds genome-like CpG depletion / TpA depletion.
