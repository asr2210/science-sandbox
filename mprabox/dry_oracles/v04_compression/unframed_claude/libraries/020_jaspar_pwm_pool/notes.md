# Experiment 020 — JASPAR PWM pool (814 motifs, len 5-15)

## Result
eval_01 = 0.3243 (worse than 32-pool 0.344, much worse than seed-53 best 0.369).

## Interpretation
- 814 motifs is *way* over the sweet spot. Replicates exp 012 dilution effect: too many motifs => each appears <100 times, signal lost.
- PWM-sampling (per-instance variation) didn't rescue diversity-dilution.
- Confirms pool-SIZE is the dominant lever: ~32 is optimal.

## Next
Try JASPAR with sub-pool of 32 high-IC motifs + PWM sampling.
Or pivot to seed-lottery on the proven 32-pool.
