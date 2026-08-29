# 026_explicit_chr_diversity

022's recipe with 7 chrs explicit (4 gene-dense + chr1/11/16) replacing whole_genome.

## Result
eval_01: 0.6924 — within noise of 022 (0.6930)
GC mean=0.496

## Interpretation
Explicit gene-dense-biased chr sampling roughly equivalent to length-
weighted whole_genome. Either is fine; the 022 recipe is robust to
chromosome-source perturbations.

022 remains best at 0.6930.

## Next
- 027: Reproduce 022 with different seeds to measure noise floor.
  If 0.6930 is real, then we have a winner. If it's noise, ceiling
  around 0.69 for this recipe class.
