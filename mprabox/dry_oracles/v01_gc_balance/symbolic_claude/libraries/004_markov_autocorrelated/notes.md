# Exp 004 — Autocorrelated Markov sequences

## Design
50K Markov-1 sequences. P(c_t = c_{t-1}) = 0.5; P(other) = 1/6 each.
Stationary marginals uniform 25/25/25/25, so per-position composition
matches baseline exactly. Only the dinucleotide distribution changed.

## Result vs baseline
| eval    | baseline | exp004 | delta  |
|---------|----------|--------|--------|
| eval_01 | 0.4848   | 0.2871 | -0.198 |
| eval_07 | 0.5200   | 0.3483 | -0.172 |
| eval_08 | 0.1613   | 0.1317 | -0.030 |
| eval_13 | 0.4992   | 0.3287 | -0.171 |

**ALL evals dropped sharply.** Much bigger effect than composition bias
(exp 003).

## Interpretation
The score strongly rewards local entropy / de-correlation. Repeated
characters at adjacent positions are penalized. This is a bigger lever
than composition.

Next: test the opposite direction (anti-correlation: P(same)=0). If
anti-correlation beats baseline, we have a way to score above 0.485.
If it also drops, uniform-random dinucleotide is the optimum and we
need to find other structure to optimize.
