# 011 four_corner

12500 sequences per corner, each with composition (0.7 one char, 0.1 each rest).

## Result
- eval_01: **0.2703** — much worse than Dirichlet(2)'s 0.3917

## Interpretation
Structured clusters at compositional corners do MUCH worse than smooth
Dirichlet over the simplex. The predictors apparently like smooth, varied
compositions across the full simplex — not 4-way clustering at extremes.

## Updated theory
- We don't just need composition variance — we need SMOOTH gradient compositions
  over the simplex.
- Smooth Dirichlet works because every region of compositional space is sampled.
- Concentration at corners (whether by hard clustering or Dirichlet(0.1)) hurts.
