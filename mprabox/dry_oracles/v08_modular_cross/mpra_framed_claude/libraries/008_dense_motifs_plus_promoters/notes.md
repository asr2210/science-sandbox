# Experiment 008 — 50/50 dense motifs + TSS promoters

## What I tested
25,000 dense motif scaffolds (same as exp 007) + 25,000 TSS-centered
RefSeq promoters. Halving each subset to test additivity.

## Hypothesis
The HepG2 boost from promoters + the K562/SKNSH lift from dense
motifs should add up to a larger mean than either alone.

## Result — additivity failed
- mean_r best eval = 0.0027 (eval_04/09)
- Worse than exp 007 (0.0061 on eval_07).
- K562 turned mostly NEGATIVE (-0.002 to -0.008) on most evals — the
  prior K562 signal from dense motifs collapsed.
- HepG2 improved on certain evals (eval_03/12: 0.0103 vs 007's 0.0059).
- SKNSH: small consistent positive (~0.002) on most evals, no eval_07
  spike anymore.

## What this tells me
**Mixing different sequence types does NOT simply add their signals.**
It seems to either:
1. Reduce training data per type below what the model needs.
2. Force the model to learn distinct sub-models, weakening each.
3. Or: dense motif scaffolds need to dominate the training data to
   keep K562 lit up.

The promoter signal lifted HepG2 by ~0.004 on specific evals but cost
K562 ~0.010 broadly. Net: worse mean.

## Updates to theory
**Theory v3.1 → v3.2:** library-type signals are NOT linearly additive
in 50/50 mixes. The dominant type drives the model. Mixing requires
weighting toward the type that helps most cell types broadly.

Dense motif scaffolds help K562 + sometimes SKNSH + sometimes HepG2 —
they're the broadest single library. Promoters help only HepG2 evals.

## Next
Try 70/30: more motif scaffolds, fewer promoters. Hypothesis: K562
signal recovers, HepG2 still gets some boost.
