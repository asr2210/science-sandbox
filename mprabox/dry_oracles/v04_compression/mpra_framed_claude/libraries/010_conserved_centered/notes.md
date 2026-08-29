# 010_conserved_centered

50k 200bp windows centered on phastCons100way conserved elements.
~9.4M conserved elements on autosomes; most are 5-50bp cores.

## Result
eval_01: 0.4606 (vs 008 best: 0.5035; -0.043)
mean across 14: 0.487

## Pattern: curation-as-distribution-shift again
Worse than 002, 005, 007, 008, 009. Conservation-centered sampling
shifts the distribution toward functional cores (which sit in
specific compositional regimes — promoters, exonic enhancers) and
the model loses generalization.

## NEW critical observation: eval_08 likes RANDOM
Reviewing eval_08 across all libraries:
- 001 random uniform:     0.110  ← BEST
- 002 genomic:            0.097
- 003 dinuc-shuffled:     0.099
- 004 cCREs:              0.086
- 005 hybrid:             0.099
- 006 motif-injected:     0.073
- 007 all-autosomes:      0.090
- 008 TSS-25kb:           0.092
- 009 TSS-2.5kb:          0.092
- 010 conserved:          0.093

**Pure random sequences score highest on eval_08.** Genomic-derived
libraries are uniformly worse. Motif injection was worst.

This suggests eval_08 contains sequences that are either truly random
or have composition very unlike natural genome — so training on
natural sequences hurts the model's ability to predict eval_08
activity.

## Implication
A library that includes a substantial chunk of uniform random
sequences (e.g., 10-20k of 50k) should lift eval_08 toward 0.11
without sacrificing too much on other evals. This is the multi-
objective mix strategy.
