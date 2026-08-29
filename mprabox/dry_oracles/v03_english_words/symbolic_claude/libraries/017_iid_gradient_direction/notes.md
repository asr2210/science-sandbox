# 017 — gradient-direction tuning

p = (0.30, 0.245, 0.235, 0.22). Mild '0' boost + mild '3' reduce.

## Result
- eval_01: mean_r = **0.4272** (identical to exp 011!)
- a = 0.5977, b = 0.6295, c = 0.0545

## Conclusion
Adding mild '3' reduction on top of mild '0' boost gave NO additional improvement.
Suggests the '0' boost effect saturates, or these effects don't add linearly.

The eval seems to plateau around 0.4272 for any "mild perturbation toward more '0'".
