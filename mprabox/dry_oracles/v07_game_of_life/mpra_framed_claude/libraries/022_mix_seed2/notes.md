# Experiment 022 — 4-way mix seed=2 (third noise sample)

## Design
Exact copy of exp 002's 4-way mix design with SEED=2.

## Result
- eval_01: 0.3954
- K562: 0.6084, HepG2: 0.4299, SK-N-SH: 0.1478

## Noise floor — 3-sample estimate
Three runs of identical 4-way mix design:
- seed=0 (002): 0.3937
- seed=1 (010): 0.3961
- seed=2 (022): **0.3954**

Mean: **0.3951**, sample std: **0.0012**.

Per-eval std (avg across 14 evals): ~0.0014.

**The library design ceiling is 0.395 ± 0.002 (95% CI).**

## Implications
- The 0.396 from seed=1 was the upper tail of normal seed variance,
  not a real lift.
- Differences below |Δ|=0.0025 between two libraries are noise.
- The natural→mix lift (+0.0075) is real (>5σ above noise).
- All "tied at ceiling" designs are in the [0.392, 0.398] band.

## Per-eval interpretation
Even at the ceiling, evals vary widely:
- eval_13: 0.41 (highest, all designs)
- eval_01/14: ~0.395 (the primary)
- eval_03/12: ~0.39
- eval_10: ~0.367
- eval_08: ~0.265 (way below — different eval entirely)

The bottom line for library design: **the achievable mean_r on the
primary eval (eval_01) is 0.395 ± 0.002, achievable via any
broadly composition-balanced library.**
