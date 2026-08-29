# 030 — 017 recipe, seed 314159 (final)

## Result
- eval_01 mean=**0.8783** (K562 0.8558, HepG2 0.9115, SKNSH 0.8674)
- Best across 4 seeds tested:
  - 88888 (017):    **0.8820**  ← BEST
  - 314159 (030):    0.8783
  - 11111 (029):     0.8771
  - 999999 (028):    0.8738
  - mean ± std: 0.8778 ± 0.0030

## Interpretation
017's seed 88888 remains the best in our search. Variance ±0.003 (std)
across 4 seeds — narrower than initial 028 estimate suggested.

## Final library
**017_strict_random_50_8mer_bank** is the best submission. Recipe:
- 25k strict (perfect 50/50/50/50 ACGT, shuffled per seq)
- 25k uniform random + 1 random 8-mer insert from 50-bank at random pos

## End of 30 experiments.
