# 011 — AT-rich chr22 windows

## What I tested
50k chr22 200bp windows from bottom 30% by GC (mean GC 0.35,
range 0.01-0.41). Random orientation. Seed=42.

## Result
- eval_01 = **0.1264** (003 chr22 random: 0.134, drop -0.008)
- mean of evals = 0.1207
- K562: 0.031 (003: 0.037)
- HepG2: 0.165 (003: 0.169)
- SK-N-SH: 0.184 (003: 0.196)

## Comparison across GC axis
- AT-rich (mean GC 0.35): 0.126
- chr22 random (mean GC 0.48): 0.134 ← best
- GC-rich (mean GC 0.59): 0.119

Both biasing directions hurt, but GC-rich hurts more (-0.015 vs -0.008).
Natural variance wins.

## Theory update
Compositional VARIANCE matters. Any narrowing (toward GC-rich or
AT-rich) loses information. The eval rewards a library spanning the
natural compositional distribution.

## What to try next
012: Explicit stratified-GC mix. Combine ~17k AT-rich + 17k chr22
mid + 16k GC-rich to test if explicit compositional breadth helps
beyond natural chr22 sampling.
