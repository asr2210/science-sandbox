# Exp 006 — Human DNA-like Markov

## Design
50K Markov-1 sequences with transitions derived from human dinucleotide
frequencies; assumed mapping {0,1,2,3} = {A,C,G,T}.
Stationary marginals: 0.298, 0.213, 0.211, 0.278 (AT-rich, GC-poor).

## Result vs baseline
| eval    | baseline | exp006 | delta   |
|---------|----------|--------|---------|
| eval_01 | 0.4848   | 0.4742 | -0.011  |
| eval_03 | 0.4843   | 0.5066 | +0.022  |
| eval_07 | 0.5200   | 0.7200 | **+0.200** |
| eval_13 | 0.4992   | 0.7006 | **+0.201** |
| eval_10 | 0.4700   | 0.4874 | +0.017  |
| eval_04 | 0.4440   | 0.0958 | **-0.348** |
| eval_08 | 0.1613   | 0.0339 | -0.127  |

## Big insight
**Evals respond DIFFERENTLY to biological structure.**
- Evals 07 and 13 LOVE DNA-Markov (+0.20). Probably trained on real DNA.
- Eval_04 collapses (-0.35). Probably entropy-focused / uniform-loving.
- Eval_01 (primary) slightly down (-0.01) — near indifferent.

## Implications
- The 14 evals are NOT measuring the same thing. We can hill-climb on
  some without hurting others, but global optimization will require
  finding a sweet spot.
- For PRIMARY eval_01, uniform random remains best so far.
- For eval_07/13, biological structure helps massively.

## Open questions
- Is the eval_07/13 lift from COMPOSITION (AT-rich) or from DINUCLEOTIDE
  STRUCTURE (CpG depletion, etc.)?
- What features does eval_01 actually care about?
- Can we find a hybrid that helps biology evals without hurting
  uniform-loving evals?
