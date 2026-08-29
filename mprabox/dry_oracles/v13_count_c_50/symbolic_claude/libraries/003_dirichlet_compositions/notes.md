# 003 dirichlet_compositions

Per-sequence Dirichlet(0.5) compositions, sequences sampled from those.

## Result vs uniform random
- eval_01: 0.1451 → **0.3604** (+0.21)
- eval_07: -0.1223 → 0.3947 (HUGE +0.52)
- eval_13: -0.1243 → 0.3824 (+0.51)
- eval_08: 0.5795 → 0.2070 (-0.37 — degraded)
- Most other evals jumped 0.20-0.25

## Interpretation
Compositional variance between sequences is a major axis for most evals.
eval_08 is anti-correlated — it likes more uniform compositions (or maybe
specific within-sequence diversity).

## Next
Push composition variance even further (Dirichlet(0.1)) to see if eval_01
keeps climbing or plateaus. eval_08 already paid a price; accept that for
primary metric.
