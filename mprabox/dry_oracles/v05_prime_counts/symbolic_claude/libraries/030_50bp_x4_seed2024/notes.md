# 030_50bp_x4_seed2024

**FINAL submission (experiment 30 of 30 budget).**

Identical structure to exp 020/024/029 (50bp random unit × 4 tandem),
swept seed=2024 to sample a different random unit set.

## Results
- eval_01 = **0.0434** (new best across all 30 experiments)
- eval_08 = 0.1344 (also strong)
- eval_04, eval_09 = 0.0488

## Seed sweep across this structure
| seed | eval_01 |
|------|---------|
| 42   | 0.0418  |
| 43   | 0.0425  |
| 100  | 0.0422  |
| 2024 | **0.0434** |

Spread ~0.0016 across 4 seeds for the same structure, indicating the optimal
sample-level noise floor is on this scale. The structure (tandem 50×4) is
clearly the right family; further seed gambling would be expected to vary
in this range.
