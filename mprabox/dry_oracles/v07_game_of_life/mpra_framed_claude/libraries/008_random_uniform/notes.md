# Experiment 008 — pure random uniform DNA (40% GC)

## Design
50K i.i.d. random 200bp sequences with P(A)=P(T)=0.30, P(C)=P(G)=0.20.

## Result
- eval_01: 0.369 (Δ -0.019 vs exp 001 natural at 0.388)
- K562: 0.573, HepG2: 0.404, SK-N-SH: 0.129
- Note: SK-N-SH dropped most (0.143 → 0.129, -0.014)

## Major calibration finding
v07 floor (random uniform) = 0.369, NOT 0.31 like v04. The total
"library design dynamic range" in v07 is only 0.369 → 0.394 = 0.025.

Comparison to v04 (priors copy):
- v04 random uniform: 0.31
- v04 natural: 0.48
- v04 best (4-way mix): 0.50
- v04 dynamic range: 0.19

vs v07:
- v07 random uniform: 0.369
- v07 natural: 0.388
- v07 best so far: 0.394
- v07 dynamic range: 0.025

So **v07 has ~8x less library design leverage than v04.** Either the
v07 model is much more robust to training data quality, or the eval
distribution overlaps with random sequences much more, or both.

## Revised T6
**In v07, the model has strong inductive biases that achieve ~0.37
eval even with random uniform DNA training. Library design can lift
that to ~0.394 (+0.025). Any 50K library of natural-like distribution
will land near 0.39. The 0.40 ceiling is intrinsic to model+eval, not
library.**

## Strategic implication
Library design contributes at most +0.025 to mean_r. Most "good
library" choices buy +0.020 (over random). The remaining +0.005 of
improvement available from regulatory enrichment is at the noise
floor of the eval. Reasonable strategies cluster around 0.39.

## Sequence-design space refresh
Updated breakdown:
- random uniform → dinuc-shuffled natural: +0.004 (dinuc composition)
- dinuc-shuffled → natural: +0.015 (motif/syntax)
- natural → 4-way mix: +0.006 (regulatory enrichment)
- Total: +0.025
