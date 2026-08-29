# 004 gradient_3s_shuffled

Exact same 50,000 sequences as 003, but rows randomly shuffled (seed 1234).

## Result
**IDENTICAL to 003 down to 4 decimals across all 14 evals.**
eval_01 = -0.0049 (matches 003 exactly).

## CRITICAL CONCLUSION
**Order of sequences in the file is irrelevant.** Only the multiset of sequences matters.
The scorer:
1. For each sequence, compute model_a(seq), model_b(seq), model_c(seq) (or some equivalent).
2. Compute another value per sequence (target/oracle), perhaps another model's output.
3. Pearson r is between these two vectors of length 50k, both functions of sequence content.
4. mean_r = mean(r_a, r_b, r_c).

## Next
- The set of sequences must produce model outputs that correlate with some hidden target.
- Need to identify which content features matter.
- Try sequences with diverse compositions (Dirichlet) and see if any composition correlates.
