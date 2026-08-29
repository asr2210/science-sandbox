# 003 — Top 50k most-active Gosai sequences

## What
Took 50k sequences with highest max(|K562|, |HepG2|, |SKNSH|) log2FC from Gosai.
Activity range: [2.99, 12.89] (all >3 std above mean).

## Result
- eval_01 mean_r = 0.1350 (vs 002's 0.1439; **worse by 0.009**)
- k562_r = 0.044 (worse than 002's 0.054)

## Theory update
Selecting high-activity tails HURT performance. The scorer rewards
distributional match with the eval set, not extremity. The eval set
likely contains a representative mix of activities, and our library
matching that distribution is what r measures.

This argues against "library as training data" simple narrative and
more for "library distribution must match eval distribution".

## Next
Test the distribution-match hypothesis: try MANY random real samples,
or restrict to specific data_project (GTEx is biggest, 56% of data),
or use ALL real data with N replicated to 50k.
