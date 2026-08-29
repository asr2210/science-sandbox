# Experiment 021 — 32-pool + reverse-complement augmentation

## Result
eval_01 = 0.3475 (seed=53). Worse than baseline 32-pool seed=53 (0.369).

## Interpretation
RC augmentation reorganizes the random number stream so the "seed 53 magic" is
gone. Result is consistent with the 32-pool population mean (~0.344) rather
than the seed-53 outlier. RC therefore doesn't intrinsically help; the
inserted motif statistics on the forward strand are already enough.
