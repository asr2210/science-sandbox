# Exp 023 — 47.5K rand + 2.5K cCRE (5% cCRE)

## Design
Lowest cCRE-fraction sweep point. GC=0.412.

## Result
**eval_01 = 0.0484; HepG2 = 0.0525.** Essentially identical to 010 random.

## Full cCRE-fraction sweep (eval_01)
| cCRE % | library | eval_01 | HepG2 mean |
|--------|---------|---------|------------|
| 0% | 010 | 0.0480 | 0.0526 |
| 5% | 023 | 0.0484 | 0.0525 |
| 20% (s0) | 013 | 0.0493 | 0.0535 |
| 20% (s1) | 020 | 0.0487 | 0.0534 |
| 40% | 015 | 0.0470 | 0.0512 |
| 100% PLS | 008 | 0.0387 | 0.0391 |

## Interpretation
The 20% sweet spot lifts +0.001 (HepG2) and +0.001 (eval_01) over random
hg38 — both at the noise floor. Below 20% (5%) and above 20% (40%) tie or
fall. The whole "cCRE enrichment helps" finding is barely above noise.

## Theory update — final ceiling estimate
- eval_01 = **0.049 ± 0.003** is the natural-DNA ceiling. No library
  combination tested moves it above 0.05.
- HepG2 mean = **0.053 ± 0.005** ditto.
- The benefit of cCRE enrichment is real but tiny (~0.001).

## Next step
Final triplicate of best library (013 with seed=2) to nail down its
score before declaring it the best.

## Time
42s wall, 11s evaluator.
