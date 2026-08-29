# 004 — Two halves with disjoint alphabets

- First 25k strings: random uniform from {0,1}.
- Second 25k strings: random uniform from {2,3}.
- Result: all evals near zero. condition_a ranges -0.019 to +0.004.
- No NaN → predictions varied across strings.
- Even a stark composition split gives no signal. Strong evidence that
  the scorer's feature is not driven by single-base composition.
- Runtime 10.9s (faster than gradient/random). Maybe simpler input → faster path.
