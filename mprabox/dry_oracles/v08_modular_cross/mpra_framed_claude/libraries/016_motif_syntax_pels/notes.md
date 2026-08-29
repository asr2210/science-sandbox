# Experiment 016 — Structured-syntax motifs + 15k pELS

## What I tested
Replaced the random-placement motif scaffold with structured syntax:
12k homotypic clusters + 12k cooperative TF pairs + 11k mixed
(original recipe as control). Plus 15k pELS as in 012.

## Hypothesis
Real enhancers depend on TF cooperativity (homotypic clusters, TF
pairs at specific spacings). A model trained on syntax should learn
features that transfer better.

## Result — worse than expected
- eval_07: **-0.0088** (vs 012's +0.0024) — major loss
- eval_10: -0.0077 (vs 013's +0.0085)
- eval_08: 0.0037 balanced (vs 012's 0.0117)
- eval_13: K562=0.0084 (positive, but mean only 0.0015)
- HepG2 slightly elevated on several evals
- K562 mostly NEGATIVE
- Mean across 14 ≈ 0.0001 (worse than 012's 0.0029)

## What this tells me
**Structured syntax HURT.** Two possible reasons:
1. K562 specifically thrives on RANDOM motif density, not concentrated
   clusters. The shuffled, high-entropy backbone may be what the
   model needs.
2. Reducing the "broad mixed" fraction from 35k to 11k removed too
   much of the broad-spectrum signal that was holding K562 positive.

In retrospect, the 007/012 "15-25 random motifs" recipe wasn't
*missing* syntax — it was BENEFITING from the breadth.

## Updates to theory
**v3.8 → v3.9:** For training a sequence-to-activity model from
50k examples on small architectures, BROAD random motif co-occurrence
beats biologically-realistic concentrated clusters. Diversity of TF
combinations per sequence matters more than realism of individual
combinations.

This is consistent with the idea that the model is learning a
"motif co-occurrence statistic" rather than syntax-aware predictions.

## Next
Step back to the 012 baseline and try a different angle: **expand
the motif vocabulary** from 35 to ~70 motifs. Adding more cell-type-
specific TFs (more hematopoietic, more neural, more housekeeping,
more pioneer factors) should give the model more grammar to learn,
especially for evals that respond to TFs not in the current pool.
