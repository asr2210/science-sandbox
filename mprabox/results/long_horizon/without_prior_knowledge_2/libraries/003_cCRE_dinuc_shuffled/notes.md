# 003 — dinucleotide-shuffled cCREs

## Design
50K cCREs (same sampling strategy as 002), each sequence then dinucleotide-
shuffled via Hierholzer's Eulerian-walk algorithm. Dinucleotide multiset
exactly preserved per sequence (and thus all dinucleotide and mononucleotide
frequencies); motif structure destroyed.

## Results (mean over 3 seeds)
- eval_01 = **0.6189** (vs 001 random 0.6954 = **−0.077**, vs 002 cCRE 0.7263 = **−0.107**)
- mean across 14 evals ≈ **0.660** (vs 001 ≈ 0.732, **−0.072**; vs 002 ≈ 0.762, **−0.102**)

## Per-eval comparison
```
eval  001 rand  002 cCRE  003 dinuc-shuf
01    0.6954    0.7263    0.6189   (003 < 001)
02    0.7848    0.8195    0.6989   (003 < 001)
03    0.7612    0.8064    0.6828   (003 < 001)
04    0.7494    0.7605    0.6591   (003 < 001)
05    0.6951    0.7263    0.6187   (003 < 001)
06    0.7853    0.8199    0.7012   (003 < 001)
07    0.6684    0.7734    0.6482   (003 < 001)
08    0.7841    0.6880    0.5912   (worst!)
09    0.8115    0.8229    0.7113   (003 < 001)
10    0.7564    0.7909    0.6735   (003 < 001)
11    0.6833    0.7140    0.6104   (003 < 001)
12    0.6553    0.6928    0.5878   (003 < 001)
13    0.6584    0.7714    0.6609   (≈ 001, 002 wins big)
14    0.7851    0.8194    0.6991   (003 < 001)
```
003 is below 001 on **13/14** evals (eval_13 essentially tied).

## Across-seed variability
eval_01: 0.6515 / 0.6329 / 0.5722 → SD ≈ 0.034 — even higher than 002.
Each per-sequence shuffle is random AND each seed picks a different cCRE
subset, so two sources of variation compound.

## Interpretation — this falsifies the "compositional gain" hypothesis
003 was designed as a 3-way mechanism test (001 < 003 < 002 expected).
Instead 003 < 001 on 13/14. So:

1. **Real TF motifs in cCREs are doing all the work** in 002's gain over
   001 — and then some. Without motifs, the natural sequences are
   actively WORSE than uniform random.
2. **Compositional bias of natural sequences is harmful in isolation.**
   Preserving GC content / CpG / dinucleotide structure narrows the
   sequence-space coverage relative to uniform random, but provides no
   compensating signal once motifs are gone.

## What this updates in T2 → T3

**T3:** Two factors govern library informativeness for generalizing
sequence-to-activity models:

  (a) **Sequence-space coverage.** Random uniform DNA spans the largest
      coverage; natural sequences are concentrated in a biased region.
      Coverage helps the model extrapolate to held-out sequence types.

  (b) **Motif content.** Real TF binding motifs in real positional
      context provide strong, learnable signal. Random has chance
      motifs; cCREs have dense real motifs; shuffled cCREs have neither.

Library "informativeness" = motif gain (b) − coverage cost (a).
Real cCREs net positive over random because (b) > (a) cost.
Shuffled cCREs net negative because there's no (b) but full (a) cost.

## Implication
The optimal library should combine both: **real motifs embedded in
broad sequence backgrounds.** Either:
- Mix random + cCREs
- Embed TF motifs into random scaffolds
- Use synthetic motif-grammar libraries

## Most informative next experiment (004)
**Embed TF motifs into uniform random scaffolds.** Take 50K random
200bp sequences (003 background) and embed 1–3 random TF motifs from a
core motif set (HOCOMOCO/JASPAR human core). If T3 is right:
  - Motifs-in-random > random (motifs added)
  - Motifs-in-random vs cCREs: tests whether real-context cCRE motifs
    are more informative than orphan motifs in random background.
This sharply tests whether motif IDENTITY alone is sufficient or whether
real cCRE positional/context structure matters.
