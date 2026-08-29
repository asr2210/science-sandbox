# 001 — Random uniform baseline

## Hypothesis
Test the floor. Random 25% A/C/G/T should give weak or zero signal if scoring
requires designed structure.

## Setup
- 50,000 sequences, each 200 bp
- Seed 42, `np.random.default_rng`, uniform over {A,C,G,T}

## Result
- eval_01 mean_r = **0.8490** (K562 0.8309, HepG2 0.8786, SK-N-SH 0.8375)
- Mean across all 14 evals ≈ 0.83
- Total time: ~46 s evaluating, 75 s wall

## Interpretation
Score is surprisingly high already. Several evals return identical numbers
(eval_01 = eval_02 = eval_05 = eval_14 = 0.8490; eval_03 = eval_12; eval_04 =
eval_09; eval_06 = eval_11) — these are probably the same test under different
seeds/orderings, so the 14 evals collapse to ~8 unique. eval_07/08/10/13 are
genuinely harder.

This high baseline suggests the score is NOT "predicted regulatory activity of
our designed sequences" (where random would be near zero). More likely:
- prepare.py uses our 50k sequences as a *training set* (with pseudo-labels
  from a teacher) for a student model, then tests on held-out MPRA labels —
  random covers sequence space and so trains a reasonable model
- or our library is used as background / calibration; random already covers
  background well

## Next
Run 002 = 50k copies of a single random sequence. If score crashes, diversity
matters (consistent with student/distillation theory). If score stays ~0.85,
then per-sequence content dominates.
