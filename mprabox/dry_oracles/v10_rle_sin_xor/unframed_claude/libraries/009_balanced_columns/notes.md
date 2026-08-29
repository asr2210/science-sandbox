# Experiment 009 — per-position balanced 50% GC

## Setup
Each column has exactly 12500 of each {A,C,G,T} across the 50k sequences.
Eliminates the per-position sampling noise from independent Bernoulli draws.

## Result
- mean_r=**0.5195**, K562=0.9945, HepG2=0.5682, SKNSH=-0.0042

## Interpretation
**Tiny improvement over baseline** (0.5187 → 0.5195, +0.0008). HepG2 went
up 0.0013, SKNSH 0.0012; K562 unchanged. Could be noise but is the first
positive delta. Worth a follow-up.

If "remove noise from random" actually helps, going further (per-row
balance too) might compound. Test next.
