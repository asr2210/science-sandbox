# 019 — Insert in both halves (strict and random)

## Result
- eval_01 mean=**0.8771** (K562 0.849, HepG2 0.910, SKNSH 0.873)
- vs 017 (insert only in random): mean -0.005. K562 -0.013.

## Interpretation
Inserting into strict half damages strict's composition strength on K562
(strict's K562 ceiling came partly from EXACT 50/50/50/50). Insert in random
only is still the optimum recipe.

## Next
- 020: two inserts at FIXED positions in random half (50-bank each). Creates
  2500 sub-clusters instead of 50.
