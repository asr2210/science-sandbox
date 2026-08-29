# Experiment 002 — random genomic 200bp windows from GRCh38 chr22

## Design
- 50,000 random 200bp windows sampled uniformly at random from chr22
  (hg38). N-containing windows rejected and resampled.
- Source: `data/chr22.fa` from UCSC.
- GC content ~46.8% (chr22 average), vs 50% for the random uniform
  baseline.

## Purpose
Isolate the effect of *natural DNA composition* (k-mer statistics, GC,
repeat content, occasional regulatory motif at genome-wide density)
from regulatory enrichment. Compared to 001 this library has:
- realistic k-mer / dinucleotide / motif statistics
- realistic repeat content
- only a small fraction of true regulatory elements (genome density)

## Result
mean_r ≈ 0.15 (vs 0.12 in 001).
- K562_r: ~0 (range -0.04 to +0.04). Unchanged from 001.
- HepG2_r: identical to K562_r (collapsed). Unchanged.
- SK-N-SH_r: ~0.46 (up from 0.36).
- eval_07: 0.20 (best). eval_08: 0.03 (worst, even lower than 001).

## Interpretation
1. Natural sequence stats add ~0.10 to SK-N-SH but **nothing to K562
   or HepG2**. Whatever the model is doing in SK-N-SH is sensitive to
   simple composition / k-mer features that genomic windows have but
   uniform-random doesn't. K562/HepG2 either need real regulatory
   motifs to learn anything, or the eval is measuring something that
   natural background can't predict.
2. eval_08 actively got *worse* (0.05 → 0.03). Suggests eval_08
   penalizes some chr22-specific characteristic — possibly its eval
   sequences are short / synthetic / designed and chr22's repeat
   content steers the model away from useful features for them.
3. eval_07 and eval_13 jumped the most → these evals might be most
   sensitive to natural composition.

## Theory update
- Floor for SK-N-SH with any sensible training set: ~0.36–0.46.
  Real regulatory motifs should push SK-N-SH well above 0.5.
- To meaningfully lift K562 and HepG2 we likely need explicit
  regulatory content (cCREs / DHS / motif-enriched sequences).
- The K562 == HepG2 numerical collapse persists. Maybe `prepare.py`
  shares the regression heads or the model collapses both to the same
  features when training data lacks cell-type-distinguishing signal.

## What to try next
Experiment 003: regulatory-enriched library — 200bp windows centered on
ENCODE cCREs distributed genome-wide. Tests whether *enriching for
real regulatory elements* (vs random genome) lifts K562/HepG2 above
zero. If yes, the theory is on track. If no, the eval sets might
require something different (synthetic designed sequences, motif
libraries, or cell-type-specific enrichment).
