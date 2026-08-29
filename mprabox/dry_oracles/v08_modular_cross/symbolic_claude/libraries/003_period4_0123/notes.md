# 003 — 50,000 identical period-4 sequences

All 50,000 strings = "0123" * 50. Length 200.

## Results
ALL values NaN (mean, a, b, c) for all 14 evals.

## Interpretation
50,000 identical strings → all per-string predicted values identical
→ across-string variance is zero → correlation undefined → NaN.
This confirms scoring uses ACROSS-STRING correlation.

Even conditions b/c are NaN here, which differs from exp 002 (where b/c gave
real values for 4 distinct strings). So even b/c likely require some
across-string variance.

## Conclusion
We MUST submit a diverse set of strings. Identical or near-identical
submissions give NaN.
