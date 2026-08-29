# condition_a/b/c sub-evaluations

## What they are
Each eval reports `mean_r` plus 3 condition sub-scores `condition_a/b/c`.
`mean_r` is the average of the three condition scores.

## Diagnostic
- For uniform random: all three are defined; consistently cond_b > cond_a > cond_c.
- For very biased compositions (P=0.05 for some chars): cond_a goes NaN
  for all evals while b/c stay defined. → cond_a requires diversity in
  characters that become rare.
- Going more extreme triggers more NaNs.

## Practical rule
- Keep every character at probability ≥ ~0.1 across the library to avoid
  cond_a NaN.
- mean_r = (cond_a + cond_b + cond_c) / 3 (probably) — if any is NaN, mean
  is NaN.
- Track condition_b and condition_c independently when mean is NaN to still
  glean signal.
