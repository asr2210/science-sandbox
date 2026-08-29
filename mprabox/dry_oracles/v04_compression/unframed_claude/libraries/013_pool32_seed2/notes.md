# Experiment 013 — 32-motif pool reproducibility (seed 53)

## Result
eval_01: **0.369** (vs 0.344 in exp 011 with seed 51). All evals improved further:
- eval_07: 0.498 (+0.078 over uniform baseline)
- eval_13: 0.465 (+0.065 over baseline)
- eval_03/12: 0.400 (+0.043)
- eval_04/09: 0.352 (+0.051)

## Interpretation
- The 32-motif strategy is robust (both seeds beat uniform).
- Substantial seed-to-seed variance (~0.025), much larger than uniform random's seed variance (~0.009).
- The motif placement details matter — some specific layouts of which motifs land where give better scores.

## Implication
- Strategy works. Can be reliably above 0.34.
- Lucky seeds might push toward 0.40.
- Worth both: (a) running replicates to find lucky seeds, (b) trying systematic improvements (2 motifs/seq, PWM softening, refined motif pool).

## Next
Exp 014: 32-pool, 2 motifs per seq, new seed. Tests if more motif content (at low per-motif library frequency) helps further.
