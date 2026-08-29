# 026_six_way_seed2 — notes

## Design
Identical to exp 024 (6-way) but SEED=2.

## Result
- eval_01 = 0.4959 — well below 024 (0.5025) and 025 (0.5027)
- 3-seed mean for 6-way: 0.5004 (vs 011 design 2-seed mean 0.4992)
- Δ between designs shrunk: +0.001 from +0.003

## Interpretation
The +0.003 between seeds 0/1 was lucky. Seed 2 hit a -1σ realization.
The TRUE 6-way mean is closer to 0.500, indistinguishable from 4-way
within standard error.

The 6-way design is NOT significantly better than 4-way.

## Lesson
Multi-seed verification matters. n=2 was not enough to distinguish
designs at the +0.003 level. Need n=4+ for confidence.

## Implication
The plateau is robust. Both 4-way (exp 011 family) and 6-way (exp 024
family) average ~0.500 ± 0.003. The "best single realization" (0.5027
from exp 025) is just the lucky tail.

## Strategic decision
Stop chasing tiny improvements within the plateau. Use remaining
experiments for:
1. 1 more seed of exp 011 design (lock in 4-way mean)
2. Try one more genuinely-different design
3. Final submission via best-of-best

## Next test
exp 011 design with SEED=2. Third realization of 4-way for matched
3-seed comparison.
