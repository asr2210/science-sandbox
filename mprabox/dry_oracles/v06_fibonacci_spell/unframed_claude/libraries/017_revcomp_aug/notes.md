# Experiment 017: Reverse-complement augmentation (50%)

## Plan
50,000 hg38 random windows (seed=17), with each window randomly
reverse-complemented with p=0.5 before submission. Tests whether scorer
is strand-aware (DNA is double-stranded; both strands carry information).

## Result
- eval_01 mean_r = **0.1379** (K562=0.0433, HepG2=0.1729, SKNSH=0.1976)
- Beats exp 014 random (0.1350) by +0.003; ~same as exp 006 (0.1387)
- K562 r = 0.0433 is among the best yet (exp 006 = 0.049, exp 014 = 0.038)
- Within seed-noise band of best (006); not a clear win on aggregate

## Implication
Revcomp augmentation is at most a noise-level effect. The scorer either
(a) already augments internally with both strands or (b) is approximately
strand-invariant for this prediction task. Cannot reject "no-op" from a
single seed run.

## Next
Theory T14: with diminishing returns on sampling strategy, try richer
inputs. Two candidate directions:
- 018: multi-seed pooled hg38 random (4 seeds, 12.5k each) to test whether
  diversity beyond a single 50k draw helps.
- 019: combine multi-seed + revcomp augmentation.
