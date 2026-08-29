# 013_intergenic_deserts

50k random 200bp windows from regions >25kb from any RefSeq TSS.
Pure natural human DNA, disjoint complement of 008.

## Result
eval_01: 0.4439 (vs 002=0.4967, 008=0.5035, 001=0.3425)
eval_08: 0.0864
Sits between random (001) and broad-genomic (002).

## Per-eval vs 002 (broad random genomic)
- eval_01: -0.053
- eval_03: -0.053
- eval_04: -0.079
- eval_06: -0.054
- eval_07: -0.009  (closest match)
- eval_08: -0.011
- eval_10: -0.050
- eval_13: -0.023

## What this tells us
Gene-rich regions DO carry incremental signal: removing them from
the sampling pool drops eval_01 by ~0.05. But intergenic alone is
still ~0.10 above pure random — the "natural DNA prior" is partly
universal (composition, repeats, k-mer statistics shared across the
genome) and partly gene-region-specific.

Decomposition of the natural-DNA lift on eval_01:
- 001 (uniform random): 0.3425
- 003 (dinuc-shuffled genomic, composition only): 0.4362
- 013 (intergenic deserts, real DNA): 0.4439
- 002 (random genomic, mixed regions): 0.4967
- 008 (TSS ±25kb): 0.5035

So the +0.16 lift from random→TSS breaks down approximately:
- +0.09 from matched composition (003 over 001)
- +0.01 from real intergenic local structure over dinuc shuffle
- +0.05 from including gene-rich regions
- +0.01 marginal from TSS-biased weighting

**Composition is the biggest single contributor.** Gene-region
inclusion adds a real but smaller boost. TSS-specific weighting is
nearly free at the margin.

## Implication
Two paths forward:
1. Push composition harder — sequences with even better matched
   k-mer / motif content than dinuc shuffle. Try k-mer (5-mer or
   6-mer) Markov chain trained on TSS data.
2. Get more out of gene-rich regions — try CpG islands, promoter
   cores (TSS ±500bp), exonic windows.

Path 1 is more diagnostic: it isolates what fraction of the lift
comes from local k-mer statistics vs longer-range structure.
