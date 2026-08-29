# Exp 006 — noisy periodic 0123 (p_template = 0.7)

## Design
Each sequence: position i has base (i mod 4) with prob 0.7, else
uniformly random among the other 3 bases (0.1 each). All bases at
every position library-wide. 50k unique sequences.

## Result
eval_01 mean_r = **0.1550** vs baseline 0.1272. **+0.028 absolute,
+22% relative.** Most evals up; condition_c up to 0.41-0.45 range
(baseline c ≈ 0.39).
- Biggest wins: eval_06/11 jumped to 0.1973 (+30%).
- Losses: eval_07 (-0.016), eval_13 (-0.020), eval_08 small drop.
- Suggests different evals reward this period-4 structure to varying
  degrees.

## Interpretation
Positional periodic structure is a real lever. The active scorer
rewards a pattern where each position prefers a specific base, in a
period-4 cycle (0,1,2,3,0,1,2,3,...). Worth scaling up.

## Next
- Exp 007: push template adherence higher (p=0.9) — test if stronger
  positional bias scores better, while keeping all 4 bases at every
  position.
- Later experiments: try alternative period-4 permutations and other
  periods to triangulate the *kind* of positional structure the scorer
  prefers.
