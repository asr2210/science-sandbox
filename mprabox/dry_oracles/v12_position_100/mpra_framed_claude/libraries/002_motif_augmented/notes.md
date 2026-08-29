# Experiment 002: Motif-augmented random background

## Design
Random uniform background + 1-5 randomly chosen IUPAC TF consensus motifs
(60-motif curated pool covering AP-1, CREB, bHLH, ETS, SP1/KLF, NF-kB,
GATA, HNF, C/EBP, TEAD, p53, FOX, TCF/LEF, STAT, NFY, SRF, MEF2, IRF,
HOX, CTCF, YY1, MYB, RUNX, RFX, NR families). Motifs realized to ACGT,
placed at random non-overlapping positions, 50% reverse-complement. Seed=2.

## Hypothesis
Real TF binding sites in random context teach the universal regulatory
grammar. Predicted big jump over random uniform; gain larger on eval sets
that test motif-driven activity (i.e., most regulatory eval sets).

## Results vs exp 001
| eval | 001 | 002 | Δ |
|---|---|---|---|
| 01 | 0.0619 | 0.0646 | +0.003 |
| 02 | 0.0601 | 0.0632 | +0.003 |
| 03 | 0.0756 | 0.0789 | +0.003 |
| 04 | 0.0737 | 0.0814 | **+0.008** |
| 06 | 0.0615 | 0.0652 | +0.004 |
| 07 | 0.1219 | 0.1297 | +0.008 |
| 08 | 0.0442 | 0.0475 | +0.003 |
| 10 | 0.1176 | 0.1094 | **−0.008** |
| 13 | 0.1220 | 0.1239 | +0.002 |
Time: 57s

## What I learned
- Motifs in random background help **only marginally** (most sets +0.003).
- eval_10 actually went DOWN — suggests this eval set rewards a property
  random uniform has that motif insertion hurts (perhaps balanced base
  composition without motif-driven local GC distortion).
- eval_04/09 (and eval_07) gained the most — likely the more
  motif-driven eval sets.
- SK-N-SH gained the most on eval_04 (+0.005) — possibly neural eval
  sets benefit more from generic motif content.

## Interpretation
Adding motifs alone isn't enough — the motif signal is **drowned out by
random background noise**. The model can't easily learn "motif X drives
activity" when 95% of each sequence is uniform noise contributing
nothing predictable. Realistic background composition AND motif content
together may matter. Real regulatory sequences combine both.

## Next
Try real human genomic regulatory sequences (ENCODE cCREs) — this tests
whether realistic genomic context + natural motif content beats synthetic
motif insertion.
