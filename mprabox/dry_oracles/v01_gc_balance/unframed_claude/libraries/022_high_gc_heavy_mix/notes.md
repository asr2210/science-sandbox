# 022_high_gc_heavy_mix

Same 7 sources as 021 but rebalanced — push cCRE high-GC fraction from
~14% to ~30% of library.

Mix: 5k each chr22/19/17/20/whole_genome + 10k cCRE all + 15k cCRE PLS+DNase-H3K4me3.

## Result
eval_01: **0.6930 — NEW BEST** (+0.0022 over 021's 0.6908)
eval_04: 0.6192 (big gain from 021's 0.5968)
eval_03: 0.6992
eval_07: 0.7491 (drop from 021's 0.7571)
eval_13: 0.7411 (drop)
GC mean=0.491 std=0.122

## Interpretation
Adding more high-GC cCREs lifts eval_01-06 but drops eval_07/13.
eval_07/13 prefer broader chromosomal coverage; eval_01-06 prefer
specific regulatory composition (high-GC enriched).

The variance hypothesis was partially right — but it's not just "more
variance" — it's "more sequences with regulatory signal AND wide GC
distribution." High-GC PLS+DNase regions carry both: strong regulatory
activity AND high GC.

## Next
- 023: even more cCRE PLS+DNase (e.g., 20k+) to see if trend continues
  or plateaus.
- Also explore other cCRE subcategories: pELS, dELS, CTCF-only.
