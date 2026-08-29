# Exp 005 — Anti-correlated Markov

## Design
50K sequences from Markov-1 with P(c_t = c_{t-1}) = 0; non-same
transitions at P=1/3 each. Marginals uniform.

## Result vs baseline
| eval    | baseline | exp005 | delta  |
|---------|----------|--------|--------|
| eval_01 | 0.4848   | 0.2438 | -0.241 |
| eval_07 | 0.5200   | 0.2335 | -0.286 |
| eval_08 | 0.1613   | 0.0683 | -0.093 |
| eval_13 | 0.4992   | 0.2294 | -0.270 |

ALL evals dropped. Anti-correlation hurts MORE than autocorrelation in
exp 004 for most evals (eval_01: 0.244 vs 0.287; eval_07: 0.234 vs
0.348). Condition a stayed relatively higher (~0.35); conditions b and
c collapsed (~0.18-0.20).

## Interpretation
Uniform random dinucleotide structure is at a peak. Both deviations
(higher P(same) or lower P(same)) hurt the score. The score appears
to reward maximum local entropy, with random uniform sitting at the
optimum along this 1D axis.

Notable: the condition spread widened. Condition a is more robust to
structural changes than b or c. This might mean condition a uses a
simpler / more diffuse predictor.

## Theory update
Score appears to track sequence ENTROPY at the dinucleotide level.
Uniform random gives max entropy and best score along this axis.

To beat baseline, we cannot use simple structural levers — we need to
find sequences that match a specific TARGET DISTRIBUTION. The most
plausible target is "natural-DNA-like" sequences (if the model was
trained on real DNA). Next experiment will test this.
