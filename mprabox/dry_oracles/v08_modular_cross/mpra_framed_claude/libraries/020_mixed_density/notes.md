# Experiment 020 — Mixed-density motifs + 15k pELS

## What I tested
17.5k motifs @ 15-25 inserts + 17.5k motifs @ 35-50 inserts + 15k
pELS. Tested whether the eval_07 grammar (high density) and eval_08
grammar (low density) could COEXIST in one library.

## Result — got the worst of both
- eval_07: -0.0003 (lost 018's 0.0109)
- eval_08: 0.0016 (lost 012's 0.0117)
- eval_13: 0.0045 balanced (kept partly)
- eval_10: -0.0083 (worse than either)
- eval_04/09: -0.0044 (worse than either)
- Mean across 14 ≈ -0.0007

## What this tells me
**Density signals don't combine additively.** Even though motifs at
both densities share vocabulary, the model couldn't extract distinct
grammars from a mixed library. It averaged out.

This is the same pattern as mixing cCRE classes (014/015): mixing
distinct training distributions DILUTES per-distribution signal.

**Hard finding:** the 50k library can only learn ONE grammar well.
Multiple grammars need either bigger libraries or per-grammar
fine-tuning, neither available here.

## Updates to theory
**v3.11 → v3.12:** Library composition is a HARD-CONSTRAINED single-
choice problem at 50k size. Pick ONE recipe optimal for the most
evals you can. Mixing is almost always net-negative.

## Next
Test pure high-density motifs (no cCRE) at 50k. If 018's eval_07
win came from motifs alone (not pELS), then pure dense motifs may
push the records further. If pELS was contributing, this will lose.
