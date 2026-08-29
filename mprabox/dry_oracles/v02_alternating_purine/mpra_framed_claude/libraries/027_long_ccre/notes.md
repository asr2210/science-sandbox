# Experiment 027 — long cCREs only (≥300bp)

## Design
- 013 ratio: 15K uniform + 5K CTCF + 5K DNH3 + 25K paired far flanks
- ONLY change: uniform sampled from 488K long cCREs (≥300bp) instead
  of all 1.06M. CTCF/DNH3 unchanged.

## Result — mean_r 0.144 (worse than 013's 0.166)
- eval_06/11 = 0.187 (down from 013's 0.218)
- eval_10 = 0.155 (close to 013)
- eval_07 = 0.147 (down from 0.177)
- eval_04/09 = 0.127 (down from 0.169)

## Interpretation
Length-filtering positives hurt. The 488K long cCREs probably skew
toward dELS (which tend to be longer) and under-represent pELS/PLS
(typically shorter promoter elements). The PLS/pELS classes contribute
to eval_04/09 signal that gets lost.

Also disappointing for the "long = stronger element" hypothesis —
length doesn't correlate with model-detectable signal strength.

## Next
028 = combine 013 base with 020-style jitter, but at a different
magnitude (±25bp instead of ±50). Tests if small jitter avoids
the slight K562 loss seen at ±50bp.
