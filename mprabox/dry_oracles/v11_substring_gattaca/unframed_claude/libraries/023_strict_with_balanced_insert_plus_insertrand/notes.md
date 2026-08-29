# 023 — Strict with balanced 8-mer insert + random with insert

## Hypothesis
Inserting BALANCED (2A2C2G2T) 8-mers into strict preserves K562 ceiling
while adding cluster structure to strict.

## Result
- eval_01 mean=**0.8696** (K562 0.8497, HepG2 0.9041, SKNSH 0.8551)
- vs 017: mean -0.012. K562 -0.012.

## Interpretation
Even balanced inserts in strict damage K562/HepG2. The strict's K562
ceiling is fragile to ANY structural perturbation — even composition-
preserving ones. Strict needs to remain pure shuffled balanced.

## Lesson
Strict half is sacrosanct. Don't modify.

## Next
024: try 2 random-position inserts in random half (vs 020's fixed pos).
