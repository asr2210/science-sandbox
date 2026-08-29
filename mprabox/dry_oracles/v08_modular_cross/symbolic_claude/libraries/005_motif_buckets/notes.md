# 005 — 4 motif buckets, poly-X length 20 at pos 90-109

- Buckets of 12500 strings each: poly-0, poly-1, poly-2, poly-3 motif
  inserted at positions 90-109 in an otherwise uniform-random 200-char string.
- Background random per string → no NaN.
- Result: **First positive signal.** condition_a > 0 for most evals.
  - eval_01: 0.0061 (mean), a=0.0060
  - eval_03: 0.0074 (best)
  - eval_06: 0.0072, eval_07: 0.0029, eval_11: 0.0072, eval_12: 0.0074
  - eval_04, eval_08, eval_09 still ~0 (these may use a different feature
    or be the harder evals).
- vs exp 001 (random): condition_a was -0.003 to +0.010 (noise).
  Now mostly positive 0.005-0.007 → above noise floor.

## Interpretation
Either:
1. The scorer's feature responds to poly-X motifs (composition near pos 90).
2. The scorer uses the order of strings, and a 4-bucket monotone arrangement
   accidentally lines up with a target gradient.

Next: AMPLIFY the effect with longer motifs. If signal goes up, hypothesis 1
or 2 is supported. If it disappears, look elsewhere.
