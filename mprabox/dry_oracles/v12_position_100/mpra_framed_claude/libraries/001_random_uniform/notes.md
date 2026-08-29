# Experiment 001: Random Uniform Baseline

## Design
50,000 sequences, 200bp, sampled i.i.d. uniform from {A,C,G,T}, seed=42.

## Hypothesis
Floor performance — model should pick up *some* signal because short TF
binding sites (6-12bp) occur randomly in 200bp windows, but signal-to-noise
will be low.

## Results
- eval_01: 0.0619 (primary)
- eval_07: 0.1219, eval_10: 0.1176, eval_13: 0.1220 — highest
- eval_08: 0.0442 — lowest
- time: 65s

## Observations
- **Identical eval pairs**: eval_01 ≡ eval_14, eval_02 ≡ eval_05,
  eval_03 ≡ eval_12, eval_04 ≡ eval_09, eval_06 ≡ eval_11. So there are
  effectively ~9 distinct eval sets, not 14.
- eval_07, eval_10, eval_13 give noticeably higher scores — likely easier
  or more diverse held-out sets.
- eval_08 is the hardest.
- All ranges suggest the model is doing very little better than chance.

## What I learned
Baseline established. Random uniform DNA is a weak training signal — the
model gets ~0.06-0.12 Pearson on held-out, barely above noise. Plenty of
room to improve with structured / biological libraries.
