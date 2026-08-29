# 024_six_way_max_atlas — notes

## Design
20K natural + 8K cCRE + 7K DHS + 7K ChIP + 3K FANTOM + 5K mouse = 50K.
6-way maximal atlas diversity (4 distinct regulatory atlases at moderate
fractions + natural + mouse).

## Result
- eval_01 = **0.5025** — NEW HIGHEST eval_01 (vs exp 011 = 0.5012)
- Δ = +0.0013 (within noise but the best realization yet)
- eval_04/09: 0.5211 (best yet, +0.003 over 011)
- eval_10: 0.5419 (lower than 011's 0.5451, -0.003)
- eval_13: 0.5898 (lower, -0.005)
- Time: 14s

## Interpretation
6-way mix with 4 atlases at moderate fractions ties exp 011 within
noise but EDGES IT on eval_01 specifically. This is the first
realization above 0.5020.

Possible explanation: spreading regulatory content across 4 atlases
exposes the model to slightly more motif/context variety per training
step than concentrating in 2 atlases — at the cost of redundancy.
The net effect is small (within ±0.005 noise).

Could be noise; could be marginal real signal. Worth multi-seed
verification.

## Implication
This design is now the BEST single-realization. Lock in via multi-seed.
If the average across 3+ seeds remains ≥ 0.500, it's a real (if tiny)
improvement over exp 011.

## Next test
Re-run exp 024 design with seed=1 to verify the +0.001 advantage is
not seed luck. If 025 ≥ 0.500, 6-way is competitive with 4-way at
the level of the plateau.
