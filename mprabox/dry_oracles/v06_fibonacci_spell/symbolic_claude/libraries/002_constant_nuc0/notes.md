# 002 — Constant nucleotide 0

## Setup
50,000 identical "0"*200 sequences.

## Result
NaN across all evals with ConstantInputWarning.

## Interpretation
The score is **Pearson r**, not mean activity. Identical sequences
→ constant predictions → undefined correlation. Strategy must shift
toward DIVERSE sequences spanning a wide activity range.
