# Experiment 014: Full-genome random (seed=14)

## Plan
Re-run exp 006 with seed=14 to measure noise floor.

## Result
- eval_01 mean_r = **0.1350** (vs exp 006 with seed=6: 0.1387)
- Δ = 0.004 from changing seed → significant noise from sampling stochasticity

## Important finding
The 0.1387 from exp 006 was at the high end of the noise distribution.
"True" expected score for full-genome random is ~0.135. Many of my
"worse than 006" comparisons (mix, dnase, chr22) were within noise.

## Implication
To meaningfully beat 0.135, I need an intervention that pushes the
expected score, not just a lucky seed. Or I need to BLEND multiple
seeds into a more thoroughly diverse library.
