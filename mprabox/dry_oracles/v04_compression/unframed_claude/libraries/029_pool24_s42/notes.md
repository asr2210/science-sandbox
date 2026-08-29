# Experiments 026-030 — 24-pool seed lottery

## Results
| Exp | Seed | eval_01 |
|-----|------|---------|
| 025 | 53  | 0.3681 |
| 026 | 100 | 0.3292 |
| 027 | 200 | 0.3372 |
| 028 | 7   | 0.3547 |
| 029 | 42  | **0.3722** |
| 030 | 999 | 0.3543 |

Mean = 0.3526, std = 0.0156, range = 0.043.

## Best overall
**029_pool24_s42 = 0.3722** — new best across all 30 experiments.

## Interpretation
- 24-pool has same variance profile as 32-pool (~0.016 σ from seed).
- Best of 6 seeds = 0.372 vs 32-pool best of 5 seeds = 0.369.
- Likely 24- and 32-pool draw from very similar distributions.
- Final sweet spot is "pool of ~20-32 short canonical TF motifs, one motif/seq
  at random position in uniform random background".

## Reproducibility caveat
Seed 42 with this exact motif pool is needed to reproduce 0.3722. Per-seed
variance ~σ=0.016 means a fresh draw averages 0.353.
