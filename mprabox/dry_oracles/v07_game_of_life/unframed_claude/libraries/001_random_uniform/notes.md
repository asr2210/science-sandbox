# 001_random_uniform

## Hypothesis
Establish baseline. Uniform i.i.d. random bases tests whether the scoring function rewards any random library at all, or whether biological signal is required.

## Method
- N = 50,000 sequences, L = 200 bp
- Each base sampled i.i.d. from {A,C,G,T} with equal probability
- Seed: 42

## Result
- **eval_01 mean_r = 0.3981** (K562=0.6189, HepG2=0.4355, SKNSH=0.1400)
- All evals cluster around 0.39-0.41 except eval_08 (0.2765 — outlier, harder?).
- Many evals are duplicates (e.g., 01==14, 02==05). Suggests ~9 unique evaluations.
- 116 s reported internal compute; ~20 min wall clock total.

## Interpretation
A high baseline (0.4) on random sequences rules out simple "library used as model training data" interpretation. More likely the `_r` measures agreement between two predictors on our 50k sequences. Random sequences already have enough natural variance (GC, dinuc bias) to drive partial agreement.

## Next
Real human genomic 200bp tiles — does biological signal increase r?
