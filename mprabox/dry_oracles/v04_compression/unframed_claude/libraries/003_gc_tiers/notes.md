# Experiment 003 — GC tiered library

## What I tested
50,000 seqs split equally across GC = 0.30, 0.45, 0.55, 0.70 (i.i.d. bases at the tier's marginal frequencies).

## Result
eval_01: 0.331 → **0.267** (drop -0.064). Most evals dropped substantially.
Exception: eval_07 stayed nearly flat (0.420 → 0.414).
eval_08 halved: 0.109 → 0.048.

## Interpretation
T1 is also REJECTED. Adding cross-library variance in GC did NOT help. Random uniform DNA at GC=0.5 is a *better* operating point than a multi-tier mixture.

The pattern across all 3 experiments so far:
- exp1 (uniform random): 0.331 — best
- exp2 (uniform random + AP-1): 0.278 — worse
- exp3 (4 GC tiers): 0.267 — worst on eval_01

Differential eval sensitivity is informative:
- eval_07 is INSENSITIVE to GC tiers but sensitive to motif insertion (likely cares about positional/local structure, not global composition)
- eval_08 is HIGHLY sensitive to GC composition (likely a global k-mer / nt-frequency model)
- Most other evals respond to both perturbations

This is consistent with there being multiple independent scoring models with different feature dependencies.

## Theory update → T2
Random uniform DNA at GC=50% may be CLOSE to a target distribution the scorers expect. Both biased GC and inserted motifs move us away from that distribution.

T2: The scoring is some Pearson r where matching the *natural* training distribution of the scorers gets us higher r. Random uniform DNA is a surprisingly good first guess because i.i.d. uniform is the maximum-entropy choice that doesn't favor any particular hypothesis.

## Next
Exp 004: pure noise-level control — random uniform with a different seed. This tells me how reproducible the baseline is and whether the AP-1 / GC-tier drops are real signal.
