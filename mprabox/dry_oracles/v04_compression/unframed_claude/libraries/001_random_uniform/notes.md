# Experiment 001 — Random uniform baseline

## What I tested
50,000 random 200bp sequences, each base uniform i.i.d. from {A,C,G,T}, seed=42.

## Result
mean_r per eval: 0.33, 0.33, 0.36, 0.30, 0.33, 0.35, **0.42** (best), 0.11 (worst), 0.30, 0.38, 0.35, 0.36, 0.40, 0.33

Per-cell-line: K562_r === HepG2_r in every single eval. SKNSH_r usually slightly higher than the other two.

## Interpretation
- Random uniform DNA is already at r ≈ 0.30-0.42, not at zero. So we're far from a "noise floor" — the scorer measures something that's correlated with bulk properties of any DNA sequence (e.g., GC content, k-mer distribution overlap with training data, or a model's baseline prediction).
- eval_07 is unusually high, eval_08 unusually low. These two are outliers and may use different scoring conventions.
- K562_r == HepG2_r is consistent across all 14 evals. This is a structural property of prepare.py — these two cell-line breakdowns are computed from the same numerator. SKNSH is genuinely different.
- 50K seqs scored in ~40s of actual eval time; prepare.py overhead is ~2 min total.

## Next
Experiment 2: insert a single strong AP-1 motif (TGAGTCA) at the center of each otherwise-random sequence. If T0 (motifs help) is right, scores rise; if flat, motifs may not be it (or that specific motif isn't relevant).
