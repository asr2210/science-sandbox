# 008 — Anti-autocorrelated Markov chain

## Setup
1st-order Markov, T[i][i] = 0.10, T[i][j≠i] = 0.30. Stationary uniform.
P(next == prev) sampled at 0.10 (vs 0.25 for iid uniform).

## Results
- eval_01 = 0.0372 (vs baseline 0.0420; Δ ≈ −0.005)
- eval_08 = 0.1053 (vs baseline 0.1242; Δ ≈ −0.019)

## Inference
Anti-autocorrelation hurts (modestly, but beyond noise). Suggests iid uniform's
NATURAL repeat rate (25%) is closer to what the score wants.

## Next direction
Test positive autocorrelation (sticky chain, T[i][i]=0.40). If that also hurts,
iid uniform is the local dinucleotide optimum.
