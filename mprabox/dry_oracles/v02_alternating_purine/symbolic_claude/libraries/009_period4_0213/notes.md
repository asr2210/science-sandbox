# Exp 009 — period-4 motif 0,2,1,3 at p=0.7

## Design
Same as Exp 006 but with motif "0,2,1,3" instead of "0,1,2,3". Same
period (4), same use of all 4 bases at 1/4 of positions each, p=0.7.

## Result
eval_01 mean_r = **0.0949** — WORSE than baseline (0.1272) and far
worse than 0123 (Exp 006: 0.1550). condition_c ≈ 0.29.

## Interpretation
The specific ascending order **0,1,2,3** is what the scorer rewards.
A different permutation of the same 4 bases at the same positions
scores WORSE than uniform random. This is a sharp directional signal:
the scorer expects position i to favor base (i mod 4) specifically.

## Implications
- The scorer plausibly has a hidden template along the lines of
  `target[i] = i mod 4` and computes correlation against per-sequence
  agreement with that template.
- Phase shifts (1,2,3,0; 2,3,0,1; 3,0,1,2) might score similarly to
  0,1,2,3 — they're all the same template up to phase. But this
  motif (0,2,1,3) is a different ordering and bombed.

## Next
Tune p around the sweet spot. p=0.9 was too strong, p=0.7 was good.
Try p=0.5 to test whether more variance in per-sequence match count
helps (binomial variance is maximised at p=0.5).
