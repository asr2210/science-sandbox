# Experiment 023: Replicate 019 (kitchen sink) with SEED=23

eval_01 = 0.0730. **019 3-seed mean = 0.0748** (vs 009 3-seed mean = 0.0746).
019 and 009 are statistically tied — kitchen sink ≈ simple hybrid.

## 019 across 3 seeds (eval_01)
| Seed | mean | K562 | HepG2 | SKNSH |
|---|---|---|---|---|
| 19 | 0.0765 | 0.0809 | 0.0813 | 0.0674 |
| 22 | 0.0749 | 0.0788 | 0.0792 | 0.0665 |
| 23 | 0.0730 | 0.0766 | 0.0769 | 0.0656 |
| Mean | 0.0748 | 0.0788 | 0.0791 | 0.0665 |
| Std  | 0.0018 | 0.0022 | 0.0022 | 0.0009 |

## 009 vs 019 across replicates
| | 009 (n=3) | 019 (n=3) | Δ |
|---|---|---|---|
| eval_01 mean | 0.0746 | 0.0748 | +0.0002 |
| K562 | 0.0777 | 0.0788 | +0.0011 |
| HepG2 | 0.0786 | 0.0791 | +0.0005 |
| SKNSH | 0.0674 | 0.0665 | -0.0009 |

Both designs ≈ 0.075 mean. 019 wins K562 by 0.001 (within noise); 009 wins
SKNSH by 0.001. Pick either as final library.
