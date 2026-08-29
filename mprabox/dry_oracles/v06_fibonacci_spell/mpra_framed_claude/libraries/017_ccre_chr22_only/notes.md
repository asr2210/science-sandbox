# 017 — chr22-only cCRE-centered

## What I tested
50k 200bp windows centered on ENCODE chr22 cCREs (~17k unique cCREs
sampled with replacement to 50k). Random orientation. Seed=42.
Mean GC of resulting library: 0.529 (vs chr22 random ~0.48).

## Result — function-enrichment HURTS (even on chr22)
- eval_01 = **0.1264** (003 chr22 random: 0.1341, drop -0.008)
- mean of evals ≈ 0.121 (much worse than 003's 0.128)
- K562: 0.030 (003: 0.037)
- HepG2: 0.162 (003: 0.169)
- SK-N-SH: 0.187 (003: 0.196)

Comparable to 004 (chr19+22 cCRE): both around 0.126. The chr19
inclusion in 004 was NOT the root cause — cCRE-centering itself is
the problem.

## Why
cCREs are heavily biased toward CpG islands and promoters, pulling
mean GC up to 0.53 from chr22's natural ~0.48. The library
oversamples high-GC sequences and undersamples mid/low-GC, exactly
the "GC-biased and narrow" failure mode we already saw in 010
(GC-rich gave 0.119).

cCRE-centering ≈ a soft version of "select for high GC + low entropy
+ promoter-like syntax," which exactly hits the bad spot of the
composition axis.

## Critical theory update (T16) — STRONG NEGATIVE
Functional enrichment does NOT help this eval. The model at this
scale is NOT learning functional grammar; it's learning compositional
statistics. Selecting for cCREs only narrows the composition
distribution (toward CGI-like), which always hurts.

This is consistent with 002 (motifs alone) being only 0.117, and
006 (chr22 + embedded motifs) being equivalent to 003. The model
doesn't learn motifs from these libraries.

## Pivot
Stop trying functional enrichment. Stick with:
1. Compositional breadth (stratified chr22; 012/013 are current best)
2. Per-eval emphasis adjustments (different stratification axes)
3. Generative augmentation that preserves composition

## What to try next
018: 5-bin GC-stratified chr22, but DOUBLE each window with its
dinucleotide-shuffled variant. Tests if dinucleotide-equivalent
augmentation (more sequence diversity at same compositional content)
helps beyond raw stratification.
