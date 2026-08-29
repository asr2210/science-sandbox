# Experiment 001 — uniform random baseline

## What I did
50,000 uniform random 200bp sequences over {A,C,G,T}, seed=0.

## Result (eval_01)
- mean_r = **0.5187**
- k562_r = 0.9947
- hepg2_r = 0.5669
- sknsh_r = -0.0054

## Interpretation
- K562 is essentially saturated (r≈0.99) — almost no headroom there
- HepG2 has moderate r, plausibly improvable
- SK-N-SH has zero correlation — large headroom
- mean is dominated by K562 (drags average up), so to lift mean_r meaningfully
  we need to lift SK-N-SH and HepG2

mean_r ≈ (k562 + hepg2 + sknsh)/3 confirmed.

## Cross-eval variation
mean_r across eval_01..14 spans 0.47..0.53. eval_08 is the outlier (lowest).
K562 stable at ~0.994 everywhere; HepG2 varies 0.42..0.58; SK-N-SH ~0.

Time: 35s of evaluator work; ~2 min wall.
