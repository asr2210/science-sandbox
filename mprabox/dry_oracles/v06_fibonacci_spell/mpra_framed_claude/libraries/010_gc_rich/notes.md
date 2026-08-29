# 010 — GC-rich chr22 windows

## What I tested
50k chr22 200bp windows in the top 30% by GC content
(mean GC 0.59, range 0.52-0.90). Random orientation. Seed=42.

## Result
- eval_01 = **0.1186** (003 chr22 random: 0.1341, drop of -0.016)
- mean of evals = 0.1133
- K562: 0.019 (003: 0.037 — half!)
- HepG2: 0.161 (003: 0.169)
- SK-N-SH: 0.177 (003: 0.196)

## What this means
Biasing toward GC-rich composition HURTS. All cell types drop. The
eval rewards matching the natural chr22 composition, not shifting
toward "active-region-like" GC.

## Theory update
The eval composition profile is closer to median genomic than to
GC-rich promoter-like sequences. **Compositional matching, not
biasing, is what works.**

## What to try next
011: AT-rich chr22 windows (bottom 30% by GC). Complete the
compositional axis test. If AT-rich also hurts → ANY compositional
narrowing hurts (median is optimal). If AT-rich is closer to baseline
→ GC-rich was uniquely bad.
