# 006 — chr22 random + 2 embedded motifs

## What I tested
Same as 003 (random chr22 windows) but with 2 random TF motifs from the
60-motif set embedded per sequence at random non-overlapping positions.

## Result
- eval_01 = **0.1347** (003: 0.1341, only +0.0006)
- mean of evals = 0.1290 (003: 0.1281)
- K562: 0.037 → 0.039 (tiny lift)
- HepG2: 0.169 → 0.168 (flat)
- SK-N-SH: 0.196 → 0.197 (flat)

## What this means
Adding motifs on top of genomic background is essentially a wash. The
genomic context already contains motif content; adding 2 more doesn't
shift the model's learning meaningfully. This is consistent with the
plateau: more of the same kind of signal doesn't help.

## Theory update
The eval performance under "random genomic + motifs" plateaus near
~0.134. Genomic random is near-optimal for this architecture/scale.
To break through, the library needs *qualitatively different*
information — likely gradient signal (mutagenesis), distributional
shifts (saturation), or much higher diversity types.

## What to try next
007: saturation mutagenesis around 2500 seed sequences (each seed =
random chr22 window + 3 embedded motifs; 19 single-base mutants per
seed + original = 20 variants per seed × 2500 seeds = 50,000).
Tests if gradient information (base-level effect data) breaks the
random-genomic plateau.
