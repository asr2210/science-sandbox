# Experiment 023 — GC-stratified DHS only

## Design
50K DHS windows, 10K per GC bin. All anchored ±30-170bp from
DHS summit. No natural backbone.

## Result
- eval_01: 0.3921 (Δ -0.0018 vs GC-strat natural)
- K562: 0.6039, HepG2: 0.4286, SK-N-SH: 0.1438

Within noise. **Pure regulatory + GC = natural + GC.**

## Theory
Confirms T8 + T9 together:
- T8: GC composition is the lever
- T9: any single source (DHS only) doesn't collapse, IF its
  composition is broadly balanced (here via GC-strat)

The PLS-only catastrophe was because PLS is intrinsically narrow
(all promoters, all high-GC). DHS spans a much broader range of
contexts, so DHS-only with GC strat is fine.

## Final theory: T10
**Library design impact on mean_r is mediated entirely by the
training distribution's composition (esp. GC). Any source (natural,
DHS, cCRE) that supports a balanced GC distribution → 0.394
ceiling. Source identity doesn't matter; composition does.**

The catastrophic floor for over-narrow sources (PLS-only, TF-density
top tiles) is the failure mode of GENRE collapse, not a positive
mechanism.
