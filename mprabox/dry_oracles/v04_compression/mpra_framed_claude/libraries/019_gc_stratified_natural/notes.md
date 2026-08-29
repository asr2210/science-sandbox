# 019_gc_stratified_natural — notes

## Design
Exp 011 design but 20K natural sampled uniformly across 6 GC bins
(15-30, 30-40, 40-50, 50-60, 60-70, 70-85%) instead of random genomic.

## Result
- eval_01 = 0.4966 (vs exp 011 = 0.5012, Δ = -0.005, within noise)
- eval_07 = 0.5948 (slight uptick over 011's 0.5946)
- eval_08 = **0.0877** (lowest non-random library!) — GC stratification
  hurts eval_08 specifically
- Time: 43s (slower due to rejection sampling for rare GC bins)

## Interpretation
GC stratification is neutral on eval_01 (within noise). Doesn't unlock
the plateau. But it hurts eval_08 by ~0.01 — eval_08 likely cares about
the natural GC distribution (not the flattened uniform one).

## Implication
Random natural sampling is already "close enough" for GC coverage of
what evals need. Forcing uniform GC trades match-to-natural for
broader extreme-GC coverage, and the trade isn't favorable.

## eval_08 sensitivity note
eval_08 has the most variable response across libraries (random=0.110,
GC-strat=0.088, mouse-mix=0.096, mostly ~0.095). It seems to test
something close to NATURAL GC distribution itself rather than motif
recognition. Targeting eval_08 specifically isn't likely to help eval_01.

## Next test
TF-balanced ChIP peaks. Use ReMap but ensure ≤50 peaks per TF, spreading
across all ~2000 TFs. This forces TF-motif diversity, which random ChIP
sampling fails to do (the few highly-studied TFs dominate the random
sample).
