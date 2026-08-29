# 016 — iid reduce '3' to 0.10

p = (0.30, 0.30, 0.30, 0.10). Boost '0','1','2' equally, slash '3'.

## Result
- eval_01: mean_r = **0.3857** (vs 0.4200 baseline) — **-0.0343 (very bad)**
- a = 0.5388, b = 0.5579, c = 0.0604

## Conclusion
Even reducing the WORST char (with others boosted) tanks score. The eval prefers ALL chars present in roughly even proportions.

Combined with 015 (heavy '0' bias hurts): **only TINY perturbations near uniform help**. Optimum is mild '0' bias from exp 011.
