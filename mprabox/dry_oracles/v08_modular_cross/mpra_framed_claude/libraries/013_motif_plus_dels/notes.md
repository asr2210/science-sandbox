# Experiment 013 — 35k motifs + 15k dELS cCREs

## What I tested
Mirror of 012 with dELS (distal Enhancer-Like, 510k available) in
place of pELS. Same 70/30 ratio, same motif scaffold recipe.

## Hypothesis
If enhancer-class sequence is the universal transferable signal,
dELS should perform similarly to pELS. If proximity-to-TSS matters,
dELS would underperform (or hit different evals).

## Result
- **eval_10: mean=0.0085, K562=0.0099, HepG2=0.0128** — NEW RECORD
  on eval_10 mean and HepG2 (beats 012's 0.0057 and 011's 0.0041).
- **eval_13: mean=0.0025, HepG2=0.0097** — first time eval_13 went
  positive across all 13 experiments!
- eval_07: SKNSH=0.0080 (high)
- eval_04/09: mean=0.0034 (tied 011)
- eval_08: -0.0025 (LOST — was 012's record at 0.0117)
- Mean across 14 ≈ 0.0015 (lower than 012's 0.0029)

## What this tells me
**dELS and pELS hit different evals.** They are NOT interchangeable
despite both being "enhancer-like":
- pELS: lifts eval_08 (massively), eval_07 SKNSH
- dELS: lifts eval_10 (massively), unlocks eval_13 for first time
- Both lose ground on eval_04/09 vs motif-only baseline (007)

This is the same pattern we've seen across the cCRE classes: each
sub-class is essentially a different "training distribution" and
each unlocks a different subset of evals.

## Updates to theory
**v3.5 → v3.6:** The cCRE classes (PLS, pELS, dELS) act as
**independent eval-axes**, not graded versions of the same signal.
This means the optimal library should COMBINE multiple cCRE classes
+ motifs, even if it dilutes per-class signal — because the goal is
to hit max eval coverage.

eval_13 going positive for the FIRST TIME with dELS is the strongest
signal yet: there is an eval that specifically requires distal-
enhancer-class sequence to register at all.

## Next
Try mega-mix: motifs + pELS + dELS together. If the per-class
signals are roughly preserved (not extinguished by dilution), this
could be the highest mean library yet.

Specifically: 25k motifs + 12.5k pELS + 12.5k dELS (mirror of 011's
3-way ratio but with dELS swapped in for PLS+promoters).
