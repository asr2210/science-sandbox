# 005 GC-varied random uniform

50k sequences, each with per-sequence GC ~ Uniform[0.2, 0.8], bases sampled
from corresponding (pA,pC,pG,pT) distribution.

## Result
- mean_r = 0.741 (eval_01 = 0.752)
- Worse than fixed-GC random uniform (0.852) by 0.11
- Worse on every eval

## Takeaway
Composition diversity HURTS rather than helps. Likely because:
1. GC=0.2 and GC=0.8 sequences have very different MPRA activity → bimodal label
   distribution that confuses the regression model
2. Eval sequences probably cluster around GC=40–50%, so training on extremes
   wastes capacity
3. Fixed GC=50% gives the model a tight, unimodal label distribution + maximum
   k-mer entropy — a sweet spot

## Implication
The "broaden composition coverage" hypothesis is FALSE. Random uniform at
GC=0.5 is near-optimal for this model architecture. The remaining lever to
beat 0.86 may be richer motif signal that ADDS to k-mer info without
broadening label distribution. Test PWM-sampled motifs next.
