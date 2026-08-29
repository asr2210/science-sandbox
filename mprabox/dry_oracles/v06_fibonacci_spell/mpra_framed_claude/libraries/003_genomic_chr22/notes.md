# 003 — Real genomic chr22 sequences

## What I tested
50k 200bp windows randomly sampled from human hg38 chr22 (non-N bases only),
random orientation. Seed=42.

## Result
- eval_01 = **0.1341**  (002=0.124, 001=0.116)
- mean of evals = ~0.128
- K562: 0.011 → 0.022 → **0.037** (still low)
- HepG2: 0.15 → 0.158 → **0.167**
- SK-N-SH: 0.18 → 0.191 → **0.196**
- eval_08 still locked low (0.060)
- All evals lift together by ~0.01

## What this means
Real genomic context is better than motifs-in-random-background. The model
learns from natural motif clusters, dinucleotide composition, and CRE syntax.
But K562 is still ~0.04 — most of chr22 is non-regulatory and provides weak
signal for cell-type-specific activity.

## Theory update
- Context distribution matters more than motif presence alone (confirmed).
- The remaining gap to "good" performance is likely about *enrichment for
  functional regulatory regions*: most random genomic windows are inactive
  in any cell type, so the model lacks active examples to learn from.
- Active learning literature: "small but highly active" beats "large but
  less active" by ~10× factor.

## What to try next
Experiment 004: enrich the library for known regulatory elements (CREs).
Either (a) tile around gene TSSs / promoters, or (b) use ENCODE cCRE
BED file. Hypothesis: regulatory-region-enriched library will improve
K562 substantially because most K562 signal lives in CREs.
