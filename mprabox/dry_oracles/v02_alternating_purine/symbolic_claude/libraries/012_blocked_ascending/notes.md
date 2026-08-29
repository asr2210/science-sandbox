# Exp 012 — blocked ascending (50 positions per base)

## Design
Template: positions 0-49 prefer 0, 50-99 prefer 1, 100-149 prefer 2,
150-199 prefer 3. Same monotonic ascending arrangement as the 0,1,2,3
periodic, but stretched to 50 positions per base. p=0.7.

## Result
eval_01 mean_r = 0.0864 (much worse than baseline 0.1272, far worse
than period-4 0,1,2,3 = 0.1550). condition_c ≈ 0.29.

## Interpretation
"Ascending arrangement" alone is NOT the lever. The specific period-4
cycle (0,1,2,3,0,1,2,3,...) is what the scorer rewards. Stretching it
to blocks kills the signal — the scorer's hidden template is almost
certainly literally `template[i] = i mod 4`.

## Next
With the template locked in as period-4 0,1,2,3, push other levers:
- Variable p per sequence — increase variance in per-sequence template
  match count, which (if the scorer is Pearson-on-match-count) should
  lift r substantially.
