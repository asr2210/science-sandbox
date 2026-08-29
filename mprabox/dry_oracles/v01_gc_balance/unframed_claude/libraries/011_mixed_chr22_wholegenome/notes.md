# 011_mixed_chr22_wholegenome

25k chr22 random + 25k whole-genome random.

## Result
eval_01: 0.6571 (vs 0.6780 chr22 alone, 0.6149 whole genome alone)
eval_07: 0.7599 (best yet, slightly above whole genome)
eval_04: 0.5011 (between the two parents)

## Interpretation
Mixing is just a weighted average; doesn't break the 0.68 plateau.
Confirms that for this scorer, sequence SOURCE is everything — diversity alone
doesn't add signal.

The ceiling for "real DNA" libraries is ~0.68 on eval_01. To break through, need
either:
1. Sequences from the predictor's training distribution (likely MPRA data)
2. Sequences engineered to look like high-confidence regulatory elements
