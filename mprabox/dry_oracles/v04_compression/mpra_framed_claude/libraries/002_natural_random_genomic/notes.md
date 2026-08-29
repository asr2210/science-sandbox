# 002_natural_random_genomic — notes

## Design
50,000 random 200bp windows from hg38 primary chromosomes (chr1-22, X, Y),
weighted by chromosome length. N-containing windows skipped. Soft-masked
repeats uppercased. Seed 0.

## Generalization argument
Random genomic windows are a representative sample of the human regulatory
landscape, not biased toward any single cell type. A model trained on this
sees the "average" natural sequence distribution and learns
cell-type-agnostic features (CpG depletion, k-mer co-occurrence, dispersed
TFBS, repeat element patterns).

## Result (50s training, 82s wall)
- eval_01: 0.4798 (vs 0.3068 random, +0.173)
- range: 0.093 (eval_08) to 0.600 (eval_07)
- Mean improvement vs random: +0.13 mean_r
- **eval_08 got WORSE** (0.110 → 0.093). Notable. Maybe eval_08 contains
  random/synthetic sequences where natural-DNA features mislead the model.

## Observations
1. Natural DNA gives ~+15% absolute correlation gain — huge.
2. Most evals improve uniformly; only eval_08 regresses.
3. K562 still exactly equals HepG2. Confirmed: this is a property of the
   eval labels, not the model. (Or the simulator combines them.) Either
   way, optimizing K562 ≡ optimizing HepG2.
4. SK-N-SH consistently scores slightly higher than K562/HepG2 across evals.

## Update to theory
- Natural sequence composition + dispersed regulatory elements explain
  ~half the eval headroom over random DNA.
- The remaining gap (~0.40 from 0.60 to 1.0) likely comes from:
  (a) denser regulatory content (most genomic DNA is non-regulatory)
  (b) activity-range coverage (most random windows are weak expressors)
  (c) motif-syntax diversity that natural DNA underrepresents
- eval_08 is special — probably a stress test for sequences without natural
  context (synthetic motifs? random? scrambled?).
