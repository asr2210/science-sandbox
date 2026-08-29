# 022_no_mouse — notes

## Design
3-way human-only: 25K natural + 15K cCRE off-center + 10K DHS = 50K.
Removes 5K mouse from exp 011, replaces with 5K more natural human.

## Result
- eval_01 = 0.4945 (vs exp 011 = 0.5012, Δ = -0.007, ~1.7σ)
- eval_07 = **0.6016** (highest in any library; vs 011's 0.5946, +0.007)
- eval_13 = 0.5881 vs 011's 0.5946 (Δ = -0.007)
- Time: 13s (no mouse FASTA scan)

## Interpretation
Mouse 5K has divergent effects:
- Helps eval_01, eval_10, eval_13, eval_04 by ~0.005-0.010
- Hurts eval_07 by ~0.007

Net on primary metric (eval_01): mouse is slightly positive (+0.007),
right at the noise edge.

## Implication
Mouse 5K is a borderline-useful component. The cross-species signal it
provides for eval_01 is real but small. eval_07 has different preferences
(human-specific bias).

## Lesson
Different evals prefer different library compositions. A multi-objective
view of the experiments would have to weigh evals. Since eval_01 is
primary, keep mouse at 5K (small positive).

## Next test
Variant-perturbed natural: 12.5K natural + 12.5K natural with 5-SNP
random point mutations each. Plus 10K cCRE + 5K cCRE-with-5-SNPs +
5K DHS + 5K mouse. Gives the model PAIRED data (similar sequences with
slightly different activity) to teach motif sensitivity.
