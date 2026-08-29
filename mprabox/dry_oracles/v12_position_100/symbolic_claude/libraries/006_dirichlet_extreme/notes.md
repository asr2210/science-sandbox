# Exp 006: Dirichlet(0.3) extreme compositions

## Setup
Each seq draws character weights from Dir(0.3,0.3,0.3,0.3), then draws 200 chars.

## Results vs Random (Exp 002)
- eval_01: 0.0648 → 0.0774 (+19%)
- eval_04: 0.0813 → 0.0900 (+11%)
- eval_07: 0.1310 → 0.1479 (+13%)
- eval_08: 0.0563 → 0.0719 (+28%)
- eval_10: 0.1194 → 0.1286 (+8%)
- eval_13: 0.1186 → 0.1445 (+22%)

All evals improved!

## Theory
Correlation is scale-invariant, so more variance in predictions doesn't automatically help. But if the model has nonlinear thresholding/saturation, random compositions (near uniform 25%) sit in the flat region where output is noise-dominated. Extreme compositions push predictions into informative regimes.

## Next
Exp 007: Dirichlet(0.1) — even more extreme
Exp 008: structured composition coverage (4-simplex grid)
