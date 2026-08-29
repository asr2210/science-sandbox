# 011 — PWM-sampled 17 TFs, 6 motifs/seq

## Hypothesis
Doubling motif density (3 → 6 per seq) might further improve over exp 010.

## Results
eval_01 = 0.2847 (exp 010 was 0.3644). **DROP of 0.08.**
eval_07 dropped sharply (0.40 → 0.24).

## Update to theory v9
Density curve has a clear inverted-U:
- 0 motifs (pure random):  0.32
- 3 motifs (exp 010):      0.36  ← peak so far
- 6 motifs (exp 011):      0.28
- ~20 motifs (exp 004):    0.17

3 motifs per 200bp is the sweet spot for this TF set. More motifs shift the
sequence too far off uniform-random distribution.

## Next
- Exp 012: all 720 JASPAR human CORE PWMs, 3/seq → test TF diversity.
- If that helps, push more on diversity. If not, try 2/seq or 1/seq.
