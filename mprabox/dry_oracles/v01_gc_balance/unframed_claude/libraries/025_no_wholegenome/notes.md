# 025_no_wholegenome

022's recipe minus whole_genome; redistribute 5k to cCRE_all (15k total).

## Result
eval_01: 0.6901 — drop from 022's 0.6930
GC mean=0.499 std=0.120

## Interpretation
whole_genome (length-weighted random) DOES add value despite being
"unfocused" — likely contributes low-GC variance (background AT-rich
intergenic) that the cCRE sources don't capture.

022 recipe is genuinely well-balanced: removing any component drops it.

## Next
- 026: try adding more diverse chromosomes (chr1, chr11, chr16) instead of
  pure whole_genome — explicit chr diversity, gene-dense biased.
