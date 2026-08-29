# 004 — motifs embedded in uniform random

## Design
50K x 200bp uniform random scaffolds. Per sequence, embed 1-3 motif
instances. Each: random PWM from JASPAR 2024 CORE vertebrate non-redundant
(2,346 PWMs), probabilistic per-position sample, random non-overlapping
position, random orientation (50% RC).

## Results (mean over 3 seeds)
- eval_01 = **0.6397** (vs 001 random 0.6954 = **−0.056**, vs 002 cCRE 0.7263 = **−0.087**)
- mean across 14 evals ≈ **0.682** (vs 001 ≈ 0.732, vs 002 ≈ 0.762)

## Per-eval comparison (4-way)
```
eval  001 rand  002 cCRE  003 dinuc-shuf  004 motifs-in-rand
01    0.6954    0.7263    0.6189          0.6397
02    0.7848    0.8195    0.6989          0.7237
03    0.7612    0.8064    0.6828          0.6927
04    0.7494    0.7605    0.6591          0.6974
05    0.6951    0.7263    0.6187          0.6390
06    0.7853    0.8199    0.7012          0.7238
07    0.6684    0.7734    0.6482          0.6022
08    0.7841    0.6880    0.5912          0.7110  (≈ 001!)
09    0.8115    0.8229    0.7113          0.7553
10    0.7564    0.7909    0.6735          0.6969
11    0.6833    0.7140    0.6104          0.6279
12    0.6553    0.6928    0.5878          0.5952
13    0.6584    0.7714    0.6609          0.5881
14    0.7851    0.8194    0.6991          0.7245
```
Order on most evals: **003 < 004 < 001 < 002**.
Exception: eval_08 — 004 (0.7110) is close to 001 (0.7841) and well
above 002/003. eval_08 likely contains synthetic/artificial sequences
that benefit from broad coverage.

## Across-seed
eval_01 by seed: 0.6323 / 0.6680 / 0.6189 → SD ≈ 0.025.

## Major surprise — falsifies T3
T3 predicted 004 (motifs + broad coverage) would beat 001 (just coverage)
and possibly 002 (motifs + narrow coverage). **The opposite happened.**
Adding motifs to random scaffolds HURT performance.

## Why might this be?
1. **Motif-out-of-context is mis-learned.** The MPRA assays the actual
   activity of these embedded-motif sequences. The model then learns
   "single isolated motif → activity X" correlations that don't
   generalize to real regulatory elements (which contain cooperative
   motif clusters with complex spacing/orientation grammar).

2. **Reduced effective diversity.** 50K sequences each with 1-3
   instances from 2.3K PWMs creates highly recognizable patterns that
   the model can memorize, reducing the effective sequence-space
   coverage relative to pure uniform random.

3. **Distribution mismatch with eval sets.** Eval sequences (whatever
   they are) likely come from distributions where motifs appear in
   biologically realistic context. Models trained on "isolated motif
   in random soup" fail to match.

## What this updates: T3 → T4

**T4:** A library is informative when its sequences contain real motifs
**embedded in realistic regulatory context** (cooperative clusters,
appropriate spacing, surrounding genomic features). Three failure
modes:
- (a) Pure random (001): broad coverage, no motifs, no context → modest
- (b) Real cCREs (002): motifs in real context → BEST
- (c) Stripped composition (003): bias without motifs → worst
- (d) Bare motif insertion (004): motifs without context → second-worst

The "context" matters in a way that I cannot yet fully characterize.
It includes co-occurring motifs, spacing, possibly chromatin-derived
features captured in genomic sequence.

## Most informative next experiment (005)
**Random 200bp genomic windows (not cCRE-selected).** This separates
"genomic context" from "regulatory selection":
- 005 ≈ 001 (random uniform) → genomic context per se doesn't help;
  cCRE regulatory selection is the active ingredient
- 005 ≈ 002 (cCREs) → any genomic context is sufficient; cCRE
  regulatory selection adds nothing
- 005 between → both genomic context AND regulatory selection contribute
This is a direct, decisive test of where the cCRE benefit comes from.
