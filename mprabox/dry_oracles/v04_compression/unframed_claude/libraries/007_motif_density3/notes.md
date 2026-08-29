# Experiment 007 — 3 motifs at random positions

## Result
eval_01: 0.328 → 0.320 (-0.008, ~noise but consistent direction).
eval_07: 0.447 → 0.447 (saturated).
eval_13: 0.429 → 0.423 (slight drop).
Most other evals slightly dropped.

## Interpretation
More motif density (1 → 3) did NOT continue helping. eval_07 plateaued; eval_01 trended down. Diminishing returns set in fast: at 3 motifs per seq (15-30bp of fixed motif structure), the cumulative structure starts to cost on all the "structure-averse" evals.

The motif-rewarding evals (07, 13) have a saturation: a single random motif appears to be enough to put us in the regime they reward. Adding more doesn't increase that signal further.

## Theory update → T4'
For eval_01 (primary metric) random uniform i.i.d. is still the local optimum. Adding even small structured content hurts it slightly. The motif benefit is real but limited to eval_07/13.

## Next
Exp 008: AP-1 at random position (vs fixed pos in exp 002). Cleanest test of position-vs-identity: if AP-1 random matches the random-pool random-pos result (0.328), then position is the dominant factor; if it matches exp 002 (0.278), motif identity matters.
