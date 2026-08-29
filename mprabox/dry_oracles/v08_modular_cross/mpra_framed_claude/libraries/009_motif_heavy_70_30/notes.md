# Experiment 009 — 70/30 dense motifs + TSS promoters

## What I tested
35,000 dense motif scaffolds (15-25 motifs/seq, 35-motif pool) +
15,000 TSS-centered RefSeq promoters. Tests whether a motif-dominant
mix can keep the K562 motif signal while still gaining HepG2 from
promoters.

## Hypothesis
At 70/30, the K562 signal from motif scaffolds should mostly survive
while picking up the HepG2 lift from promoters.

## Result — best yet
- eval_07: mean = 0.0088, K562 = 0.0129, HepG2 = 0.0098, SKNSH = 0.0037
  (first time all three cell types positive AND large on one eval)
- eval_08: mean = 0.0040, HepG2 = 0.0119
- eval_01/14: mean = 0.0035 (all three cell types positive)
- eval_06/11: mean = 0.0038
- eval_04/09: K562 = 0.0123 (strong K562 signal preserved)
- Across all 14 evals, ~9 are positive, 5 negative/zero

## What this tells me
- 70/30 mix BEATS both pure-motif (007) and 50/50 (008). Confirmed:
  mixing should be weighted toward the broader-acting subset (motifs).
- All three cell types can be lit up simultaneously — eval_07 proves it.
- The eval set is heterogeneous: eval_07 responds best, eval_13 doesn't.

## Updates to theory
**Theory v3.2 → v3.3:**
- Library mixing ratios matter: weight should favor the broadest-
  acting subset (motifs > promoters by breadth of cell-type lift).
- Specific eval correlations differ widely — the library should cover
  multiple sequence "modes" to hit different evals.
- Trying 80/20 next to see if even more motif weight helps further.

## Next
- 80/20 mix (40k motifs + 10k promoters): test the boundary.
- After that: introduce a third sequence type (real cCREs of the
  promoter-like / PLS class, the most active cCRE category) to see
  if a 3-way mix lifts the floor further.
