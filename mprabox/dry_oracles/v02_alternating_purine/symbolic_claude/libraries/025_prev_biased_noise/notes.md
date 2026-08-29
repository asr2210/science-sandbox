# Exp 025 — period-4 with PREV-in-cycle biased noise

## Result
eval_01 = 0.1178; condition_c = 0.3195. Worse than baseline (c=0.41).

## Interpretation
Both directions of asymmetric noise (Exp 017 next-biased: c=0.32,
Exp 025 prev-biased: c=0.32) hurt similarly. Eval expects symmetric
noise shape. No directional preference.

## Next
Try GRADIENT peak shape: template at 0.5, ADJACENT bases (both prev
and next in cycle) at 0.2 each, antipodal at 0.1. This is a "soft peak"
shape — different from "1 sharp peak, 3 flat" shape we've used.
Tests if eval has gradient-shaped per-cell preferences.
