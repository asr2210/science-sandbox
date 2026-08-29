# 027_022_seedvar

Re-run 022's exact recipe with different RNG seed (220 -> 271).
Tests reproducibility / noise floor.

## Result
eval_01: 0.6934 (vs 022's 0.6930 — basically identical)
Noise floor of this recipe: ±0.0004

## Interpretation
022 = 027 within noise. The 0.693 score is a real, reproducible
characteristic of this recipe class. We're at a stable local optimum
for "mixed real DNA + 30% high-GC cCRE."

To push further, need a qualitatively different ingredient.

## Next
- 028: expand high-GC pool to PLS+DNase-H3K4me3+pELS (add pELS).
- 029: alternative regulatory sources.
- 030: combine all learnings into final best recipe.
