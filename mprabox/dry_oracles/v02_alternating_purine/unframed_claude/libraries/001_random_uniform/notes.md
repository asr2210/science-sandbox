# 001 random_uniform

50,000 uniformly random A/C/G/T 200bp sequences, seed=42.

## Results
- mean_r averaged across evals ≈ 0.135
- eval_01: mean=0.1342, K562=0.0104, HepG2=0.0104, SKNSH=0.3817
- SKNSH already at 0.38 from random sequences
- K562 ≈ HepG2 ≈ 0.01 (near zero, but identical)
- mean_r = (K562 + HepG2 + SKNSH) / 3 confirmed

## Key observations
- **K562 and HepG2 are identical to 4 decimal places in every eval.**
  Either: the model outputs the same head for both, or the targets are
  shared. Effectively 2 signals: {K562==HepG2} and SKNSH.
- Eval pairs: (01,14), (02,05), (03,12), (04,09), (06,11) match exactly.
  Plus singletons: 07, 08 (outlier low), 10, 13. → 9 unique groups.
- eval_08 is much lower (mean=0.06) — likely a different/harder eval.
- Runtime: ~1 min per experiment.

## Implication
SKNSH dominates the baseline. To improve mean_r, the biggest leverage is
raising K562==HepG2 since SKNSH is already 0.38 from chance.
