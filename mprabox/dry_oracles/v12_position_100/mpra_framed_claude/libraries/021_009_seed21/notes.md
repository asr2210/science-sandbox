# Experiment 021: Replicate 009 with SEED=21

## Design
009 exact composition (20K cCRE + 25K DNase + 5K random), SEED=21.

## Result — 3rd replicate of 009
eval_01 = **0.0732** (K562=0.0772, HepG2=0.0772, SKNSH=0.0651)

## 009 across 3 seeds
| Seed | eval_01 | K562 | HepG2 | SKNSH |
|---|---|---|---|---|
| 9  | 0.0772 | 0.0799 | 0.0812 | 0.0705 |
| 13 | 0.0734 | 0.0761 | 0.0774 | 0.0667 |
| 21 | 0.0732 | 0.0772 | 0.0772 | 0.0651 |
| **Mean** | **0.0746** | 0.0777 | 0.0786 | 0.0674 |
| **Std**  | 0.0023 | 0.0019 | 0.0023 | 0.0029 |

**009's true performance: 0.0746 ± 0.0023.** The original 0.0772 was a
+1σ lucky run. Per-cell stats: K562 0.0777±0.002, HepG2 0.0786±0.002,
SKNSH 0.0674±0.003.

## Implication
019 (kitchen sink) at single-seed 0.0765 may actually beat 009's true
mean. Need to replicate 019 to confirm.
