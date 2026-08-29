# Skill: Scorer fingerprinting via 14-eval signature

The scorer returns 14 eval scores. Duplicates revealed in this run:
(eval_01, eval_14), (eval_02, eval_05), (eval_03, eval_12),
(eval_04, eval_09), (eval_06, eval_11). Singletons: 07, 08, 10, 13.

Use this to:
1. Confirm framework is the v08/v10 family (these duplicates persist).
2. Read condition_a/b/c separately — they often differ in sign, telling
   you WHICH feature your design hits.
3. Run baselines first (random uniform seed=42) to see the noise floor
   per eval, then anything outside ±0.002 is signal.

## Per-eval orthogonality
Different evals reward different features. Examples observed:
- eval_07 and eval_13 sometimes reward "uniqueness" / index-encoding.
- eval_10 sometimes rewards local autocorrelation patterns.
- eval_08 sometimes rewards compositional gradient.

Don't optimize a single eval — see how each candidate moves all 14.

## Pearson noise floor
50,000 samples => Pearson noise std ≈ 1/sqrt(50000-2) ≈ 0.0045.
Anything < 2σ ≈ 0.009 is probably noise on a single eval at a single seed.
For mean across (a,b,c) the noise reduces by ~sqrt(3): ~0.0026.
A score of +0.005 is barely 2σ — needs replication to trust.
