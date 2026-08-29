# Experiment 003 — chr22 cCRE-centered windows

## Design
- 21,578 chr22 cCREs from ENCODE SCREEN registry V3.
- For each cCRE, midpoint computed and used as window center.
- 200bp window taken centered on midpoint, jittered ±25bp.
- Sampled 50,000 windows with replacement (~2.3× over-sampling).
- GC content: 53.8% (higher than 002's 46.8%, reflecting GC-richness
  of regulatory elements).
- cCRE type distribution: dELS 42%, dELS+CTCF 29%, pELS+CTCF 13%,
  pELS 9%, PLS 4–5%, CTCF-only 2%, DNase-H3K4me3 2%.

## Purpose
Test "regulatory enrichment matters" hypothesis: would training the
model on sequences known to be regulatory elements lift K562/HepG2
predictions off zero?

## Result
mean_r ≈ 0.14 — **worse than experiment 002** (0.15) across most evals!
- K562_r: -0.01 to +0.02 (still essentially zero, very slight rise).
- HepG2_r: identical to K562 (collapsed).
- SK-N-SH_r: ~0.42 (down from 0.46 in 002).
- eval_13 dropped most (0.18 → 0.13).
- eval_07 dropped (0.20 → 0.16).
- eval_08 still worst, slightly worse than 002.

## Interpretation
The regulatory-enrichment hypothesis is **partially refuted** in its
simple form. cCRE-only is not better than random genomic. Possible
reasons:
1. **Lack of negative examples**: with all windows being regulatory,
   the model can't learn what "non-regulatory" looks like, hurting
   its ability to predict across an activity range.
2. **Diversity loss from oversampling**: 50K samples drawn from 21K
   cCREs with ±25bp jitter means many near-duplicate windows;
   effective training-set size dropped from ~50K (in 002) to ~21K.
3. **Motif homogeneity**: chr22's cCRE catalog likely repeats the
   same TF motifs (e.g., CTCF, AP-1) without representing the broader
   genome-wide regulatory diversity.
4. **GC-content artifact**: the +7% GC shift may push the model to
   over-rely on GC, hurting predictions on lower-GC eval sequences.

Tiny K562 lift (+0.02 on a couple evals) is the only positive signal
for regulatory enrichment, but it's overwhelmed by SK-N-SH loss.

## Theory update (T2 → T3)
- New: a good library needs **diversity across the regulatory spectrum
  (positives AND negatives)**, not over-enrichment for positives alone.
- New: oversampling a small pool with jitter produces near-duplicates
  that hurt rather than help; truly diverse samples matter.
- Still open: would genome-wide cCREs (1M elements, no oversampling
  needed) help? Or is the cCRE-only design fundamentally flawed?

## What to try next
Two routes:
A) **Genome-wide cCRE** (waiting for hg38.fa to finish decompressing).
   Tests whether the chr22-only issue was diversity, not enrichment.
B) **Mix**: random genomic + cCREs (e.g., 50/50). Tests the
   "positives + negatives" theory.

Will do A first because it's the cleaner test of "is cCRE
enrichment actually bad, or just chr22-limited cCRE enrichment?"
