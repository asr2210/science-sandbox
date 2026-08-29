# Exp 027 — per-row Dirichlet noise direction (BREAKTHROUGH)

## Result
eval_01 = 0.1628 (vs 0.1550 baseline). +0.0078 lift.
condition_c = 0.4258 (vs 0.4107). c ceiling BROKEN.
condition_a/b = 0.0314 (essentially unchanged).

All evals lifted (eval_06 jumped to 0.2109 from 0.1955).

## Interpretation
Per-row variation in noise direction LIFTS condition_c despite same
library-wide per-cell freqs. This means condition_c is NOT purely
per-cell freq Pearson — it also captures PER-ROW structure.

The Dirichlet-sampled per-row noise weights create rows that are
INTERNALLY consistent (a row's noise leans one direction) but library
diverse. This matches what the eval reference captures.

## Next
PUSH further: try Dirichlet(0.3) for MORE skewed per-row distributions.
If lift continues, the optimum may be at extreme per-row concentration.
