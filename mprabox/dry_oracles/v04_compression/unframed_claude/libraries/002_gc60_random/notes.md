# 002 — GC60% random

## Hypothesis
Many regulatory elements are GC-rich (CpG islands). If composition alone matters,
pushing GC from 50% → 60% should improve scores.

## Setup
50k x 200bp, i.i.d. with P(A)=P(T)=0.20, P(C)=P(G)=0.30. Seed 20260603.

## Results
eval_01 = 0.1215 (random was 0.3157; **drop of 0.20**)
eval_07 = -0.0163 (random was 0.4481; **drop of 0.46, went NEGATIVE**)
All evals dropped substantially.

## Key observations
1. **Scores can be negative.** This strongly supports the "r = correlation"
   interpretation — but then random shouldn't score 0.32. So r is more likely
   a normalized score that can sit anywhere on the real line.
2. Pure GC bias does NOT help; it hurts a lot. Real enhancers are GC-rich but
   uniform-GC random sequences are not enhancer-like.
3. The drop is proportional to the random baseline value across evals — every
   eval got "worse by similar fraction." Suggests the homogeneity itself (low
   per-position diversity) is what's hurting, not GC specifically.

## Update to theory v2
The scorer rewards sequence DIVERSITY (sequences that look biologically
varied) — not arbitrary nucleotide bias. Pushing composition globally hurts.
What likely matters: localized regulatory MOTIFS embedded in a diverse
background, not a globally shifted composition.

## Next
Experiment 003: random uniform scaffold + multiple universal TFBSs sprinkled
in. If motifs add signal on top of uniform random, we know the lever.
