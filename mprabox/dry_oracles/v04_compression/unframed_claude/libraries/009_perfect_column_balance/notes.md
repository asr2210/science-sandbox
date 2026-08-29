# Experiment 009 — Perfect per-column nucleotide balance

## Result
eval_01: 0.331 → 0.290 (-0.041). Most evals dropped.
eval_07: 0.420 → 0.424 (essentially flat).

## Interpretation
Removing per-column binomial noise HURT. This is counter-intuitive but real (4× noise level). The natural ±100 variation per column around 12500 each base is doing useful work somehow.

Best interpretation: the scorer's Pearson r benefits from per-column variance because both the model's predictions and the target depend on per-column nucleotide variation. With perfect balance, that joint signal vanishes.

## Theory update → T6
Random uniform i.i.d. is a sweet spot. Both:
- LESS column variance (perfect balance, exp 009): hurts
- MORE column variance (GC tiers, exp 003): hurts
- Replacing column variance with fixed motif structure (exp 002/008): hurts
- Adding diverse-pool motifs at varied positions (exp 006): roughly flat

The scorer appears optimized around the statistical signature of binomial-variance uniform DNA. Hard to beat this with simple perturbations.

## Path forward
1. Try a 50/50 mix of uniform random + motif-loaded. Maybe creates beneficial variance in *predicted activity space* across the library while preserving per-column uniformity.
2. PWM-based motif insertion (soft motifs) — keeps per-column distribution close to uniform while injecting weak motif signal.
3. Bigger motif pools (e.g., 50 motifs, each in 1000 seqs) — extreme diversity.

Next: exp 010 = 50/50 mix.
