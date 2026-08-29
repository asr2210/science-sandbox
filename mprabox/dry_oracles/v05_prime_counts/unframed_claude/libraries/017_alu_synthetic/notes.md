# Experiment 017 — Synthetic AluY-derived sequences

## Hypothesis
If chr19 repeats drive signal, maybe Alu specifically (most
abundant SINE, harbors TFBSs) is the key. Synthesize 50K
AluY-mutated sequences (15% mutation rate).

## Method
AluY consensus (~289bp). Random 200bp window from it, mutate
each position with 15% prob to random base.

## Results — DISASTER
- eval_01: 0.0027 (chr19 repeat-only: 0.0518) → MUCH WORSE
- K562 negative on most evals
- eval_08: 0.0144 (chr19 repeat-only: 0.0469)

## Interpretation
HYPOTHESIS REJECTED. Pure Alu-derived has TINY variance across
the library (all sequences ~85% similar). Pearson r collapses
without across-library variance.

The "repeats" lever isn't a single sequence class — it's the
DIVERSITY of repeat types/ages/mutations in real chr19.

## Theory update — T11
For high eval_01, library needs:
1. Natural-DNA-like sequence (so axes f and g get coherent signal)
2. HIGH cross-library variance (so Pearson r has range)

Pure synthetic from one consensus = HIGH similarity = LOW variance
= bad r. chr19 repeats = many different repeats with varied
sequences = high variance = good r.

## Next
EXP 18: combine repeat-only windows from chr1 + chr19 + chr22
(50K each → sample 50K). More repeat-class diversity than chr19
alone. Tests if cross-chromosome repeat diversity boosts r further.
