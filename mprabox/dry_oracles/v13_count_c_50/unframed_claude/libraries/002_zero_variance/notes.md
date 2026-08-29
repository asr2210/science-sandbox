# 002_zero_variance

## What
50,000 identical copies of one random 200bp sequence.

## Why
Diagnostic: confirm Pearson-r-over-library hypothesis. Zero variance → r undefined.

## Results
All NaN. Harness emitted `ConstantInputWarning`. Confirms metric is Pearson r computed over the library — variance is mandatory.

## Implication
- The scoring function: runs my 50K sequences through a hidden ground-truth model → vector A; through 14 eval models → vectors B_i; reports Pearson(A, B_i) (and per-cell-line).
- To raise r: need (i) variance in my library, (ii) features that both models recognize the same way.
- Random already gives r=0.16. Designed variance along biologically meaningful axes should push higher.
