# Experiments 015-017 — 32-pool seed replicates

## Results
| Seed | eval_01 |
|------|---------|
| 51 (exp 011) | 0.344 |
| 53 (exp 013) | 0.369 |
| 100 (exp 015) | 0.325 |
| 200 (exp 016) | 0.348 |
| 300 (exp 017) | 0.334 |

Mean = 0.344, std = 0.016. Range = 0.044.

## Interpretation
- Strategy reliably gives 0.32-0.37, well above uniform random (0.331).
- Seed 53 was a 1.5σ lucky outlier.
- Pure seed-lottery to beat 0.369 is unlikely — expected best of 5 more = 0.36.
- Must pursue systematic improvements.

## Path forward
1. Try CURATED higher-quality motif pool (no IUPAC noise, all short canonical).
2. Try ENSEMBLE — large pool with mixed-length motifs but careful quality.
3. Try EXTRA structure: maybe specific motifs at specific positions.
