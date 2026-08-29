# 002_gc_rich

50,000 sequences, biased to ~60% GC (P(C)=P(G)=0.30, P(A)=P(T)=0.20).

## Result
eval_01: -0.2388 (vs +0.4637 baseline). Sign FLIPPED.
eval_07: -0.5879 (vs +0.5069 baseline). Huge magnitude swing.
eval_04/09 dropped less but still positive: +0.14.
eval_08 went near zero.

## Interpretation
GC content is a major signal in the scoring function. High GC anti-correlates
with the target on most evals. This implies one of:
- The target (held-out activity) is GC-content-dependent and the predictor
  flips sign because high GC saturates somewhere
- The predictor and target functions both use GC, but with different sign

Sign flip strongly suggests GC is one of the *primary* features the scorer
keys off of. Need to test AT-rich (low GC) to confirm direction.
