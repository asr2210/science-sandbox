# 004 all identical

## Design
50,000 copies of '0' * 200.

## Result
**NaN** for every eval/cell-line. scipy emitted ConstantInputWarning:
"An input array is constant; the correlation coefficient is not defined."

## Interpretation — definitive proof
The scoring function is computing Pearson correlation between two
per-sequence vectors. When all our seqs are identical, both vectors
become constant → r = NaN. This perfectly explains:
- The "_r" suffix.
- Row-order invariance (permuting both vectors identically leaves r
  unchanged).
- Robustness to partially-constant strata (those points have weight but
  don't break the correlation as long as some seqs vary).

## Updated model of the metric
For each (eval, cell_line) tuple, the scoring function:
1. Computes f(seq) for each of our 50k seqs → vector A (length 50k)
2. Computes g(seq) for each of our 50k seqs → vector B (length 50k)
3. Returns Pearson r between A and B
where f, g are sequence functions (likely ML predictors).

To MAXIMIZE r, we need to choose 50k seqs such that f and g values
across the bag are maximally linearly related.
