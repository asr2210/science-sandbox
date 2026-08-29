# 001 random_uniform

Baseline: 50k iid uniform ACGT sequences, seed 0.

eval_01: mean=0.4203, K562=0.5847, HepG2=0.6175, SKNSH=0.0587.

Observations:
- mean_r is the mean of the three cell-type r's: (0.58+0.62+0.06)/3 ≈ 0.42.
- SKNSH correlation is essentially zero from random — most leverage is there.
- Eval sets are mostly identical (variance 0.38–0.43). eval_08 the outlier
  with lower scores across all cells; possibly a held-out set sensitive to a
  feature the others share with our random library.
- 14 eval sets but many give identical numbers — probably duplicated or
  closely-related held-out sets.

Score is named `*_r` (likely Pearson r). Two interpretations:
A. Library viewed as candidate dataset → r between two activity estimators
   evaluated on our sequences (diversity matters, range matters).
B. Library is scored independently per sequence then aggregated; mean_r might
   actually be r between model-predicted activity and some ground-truth
   activity assigned to each sequence.

Either way: diversity in features helps, uniform/dead libraries should
collapse correlation. Test next: GC content perturbation.
