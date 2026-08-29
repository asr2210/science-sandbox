# 016 — Hybrid 25k GC-strat + 25k CpG-strat chr22

## What I tested
25k chr22 windows from 5-bin GC stratification + 25k chr22 windows
from 5-bin CpG stratification (positions unique across both halves)
= 50k total. Random orientation. Seed=42.

## Result — averages between 012 and 014, wins neither
- eval_01 = 0.1357 (012: 0.1367, 014: 0.1361)
- mean of evals = 0.1288 (012: 0.1308, 014: 0.1299)
- eval_07 = 0.1307 (014: 0.1310)
- eval_13 = 0.1353 (012: 0.1317, 014: 0.1323)

Hybrid is an INTERPOLATION, not a UNION. It does not pick up the best
of both per-eval emphases; it lands between them everywhere.

## Theory update
Per-eval emphases conflict — you can't have both at once with a
single library. The "compositional emphasis" is global to the library:
the model trains on the mix and predicts toward the average. So mixing
two halves of differently-stratified data just averages the prediction
distribution.

This means: optimizing for eval_01 may require committing to a single
compositional emphasis (GC-strat) rather than hybridizing.

## What to try next
017: cCRE-centered chr22 (chr22 ONLY this time — 004 included chr19
which we've now established hurts). Tests if functional enrichment
beats random/stratified when restricted to the right chromosome.
This could provide either:
- a new ceiling if functional enrichment helps
- or a useful negative result clarifying that COMPOSITION (not
  function) is what the model learns at this scale
