# Exp 030 — per-row 4-way Dirichlet EXTREME (FINAL)

## Result
eval_01 = 0.1710 — BEST.
condition_a/b = 0.0413, condition_c = 0.4304. Both at peak.
eval_06 hit 0.2278.

## Interpretation
Per-row variance is THE LEVER. The more per-row variation in
(p, noise direction), the higher the score — both a/b and c lift.

Trajectory:
- 006 (deterministic p=0.7):       0.1550 (a=0.0316, c=0.4107)
- 027 (3-way Dirichlet noise):     0.1628 (a=0.0314, c=0.4258)
- 029 (4-way alpha=2.1/0.3...):    0.1658 (a=0.0362, c=0.4251)
- 030 (4-way alpha=0.7/0.1...):    0.1710 (a=0.0413, c=0.4304)

## Conclusion
Eval reward = per-row consistency of period-4 phase 0 template AND
per-row variance in alignment strength. Library-wide per-cell freqs
average to the same shape, but per-row STRUCTURE matters significantly.
