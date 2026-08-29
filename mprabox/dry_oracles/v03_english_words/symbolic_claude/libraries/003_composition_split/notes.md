# 003 — composition split

50,000 sequences split into 4 chunks of 12500. Each chunk: each char drawn iid with one of {0,1,2,3} at 70% and the others at 10%.

Overall library composition: 25% each. But each sequence is heavily skewed.

## Result
- eval_01: mean_r = 0.3326 (vs 0.4200 baseline) — WORSE
- a = 0.4574 (vs 0.5884), b = 0.4787 (vs 0.6187), c = 0.0617 (vs 0.0530)

## Interpretation
- Conditions a, b strongly prefer balanced within-sequence composition
- Condition c slightly UP (small but consistent across all evals)
- Skewed within-seq composition hurts overall by ~0.09 on eval_01

So **scoring rewards within-sequence balance / entropy** for a, b.
Possibly **rewards within-sequence imbalance** for c (small effect).

Since mean_r = (a + b + c) / 3 and a, b dominate the loss, we should
prioritize within-sequence balance.

## Next probe
Try EXACTLY uniform per-sequence (50 of each char in random order).
If this beats 0.42, balance is the key. If not, there's some other factor.
