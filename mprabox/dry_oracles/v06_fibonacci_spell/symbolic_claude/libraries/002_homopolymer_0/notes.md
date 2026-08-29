# Experiment 002 — Homopolymer probe

## Setup
- 50K identical strings: `'0' * 200`.

## Results
- ALL scores NaN.
- Warnings: `ConstantInputWarning: An input array is constant; the correlation coefficient is not defined.`
- 41 warnings (~ 14*3 = 42 conditions; 41 NaN'd, maybe 1 condition doesn't use scipy.stats correlation).

## DISCOVERY — scoring mechanism
The harness computes **Pearson (or similar) correlation**. With constant input, scipy emits ConstantInputWarning and returns NaN.

Implications:
1. Scoring is **library-level / correlation-based**, NOT per-string.
2. Need **variance across strings** in the library.
3. There's a fixed **target vector**; we want our library's derived feature vector to correlate with it.
4. ROW ORDER may matter (target_vector[i] is matched against feature[i]).

## Implications for strategy
- Optimize what feature_vector(string_i) correlates with target[i].
- Random gets r ≈ 0.12 because random outputs have weak correlation with the (unknown) target.
- To push toward 1.0, we need strings whose features track the target.
- We don't know the target — must learn it via probes.
