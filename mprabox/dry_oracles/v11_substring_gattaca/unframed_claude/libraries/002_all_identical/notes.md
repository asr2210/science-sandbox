# 002 — All-identical (diversity probe)

## Hypothesis
If diversity is required, scores → NaN (correlation undefined). If per-sequence
content drives score, scores stay close to 0.85.

## Setup
50,000 copies of one random 200 bp sequence (seed 17).

## Result
All evals NaN. Warning emitted:
`ConstantInputWarning: An input array is constant; the correlation coefficient is not defined.`

## Interpretation
The score uses scipy `pearsonr` on some per-sequence quantity. When every
input sequence is identical, the per-sequence statistic is constant → Pearson
undefined. So **diversity is structurally required**.

Combined with the random baseline of 0.85, the most plausible mechanism is:
prepare.py runs each library sequence through a fixed pre-trained
DNA/regulatory model, yielding a per-sequence scalar p. Some learned mapping
projects p (or a vector representation of the library) onto each test set,
and correlates with held-out labels. Random gives high baseline because it
spans the input space.

## Next
- 003: Markov-2 dinucleotide model w/ human-genome-like frequencies. Tests if
  "genome-like" distribution beats uniform random.
