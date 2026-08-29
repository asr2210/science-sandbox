# Experiment 007 — 75/25 mix (random-heavy)

## Design
- 37,500 random genomic + 12,500 cCRE-centered windows. GC 42.5%.

## Purpose
Map the random-heavy side of the ratio curve. Together with 005
(50/50, 0.156) and 006 (25/75, 0.134), establishes the shape.

## Result
mean_r ≈ 0.140 (between 006 and 005, but well below 005).
- K562_r: negative on most evals (−0.02 to −0.07).
- HepG2_r: tied to K562.
- SK-N-SH_r: 0.42–0.50.
- eval_06 crashed: 0.121 (same as 006).
- eval_07 stayed strong: 0.187.

## Interpretation
Both off-ratios (006 cCRE-heavy and 007 random-heavy) lose ground vs
005 (50/50). The 50/50 ratio is the local optimum — pushing either
way hurts.

K562_r is small in all libraries (the model can barely predict K562)
but the *sign* depends on training composition. At 50/50 it's slightly
positive; at any other ratio it tends negative.

## Ratio curve summary
| ratio (random/cCRE) | exp | mean_r | K562_r avg |
|--------------------|-----|--------|------------|
| 100/0  (002) | random chr22  | 0.150 | ~0 |
| 75/25  (007) | random-heavy  | 0.140 | -0.02 |
| 50/50  (005) | balanced      | 0.156 | +0.01 |
| 25/75  (006) | cCRE-heavy    | 0.134 | -0.04 |
| 0/100  (004) | all cCRE      | 0.143 | varies (-0.05 to +0.05) |

50/50 wins. Asymmetric: the cCRE-heavy direction is hurt more than
random-heavy.

## Theory update (T6 → T7)
- Mix ratio matters and 50/50 is the optimum among tested.
- K562 prediction is fragile — small but real signal at 50/50, breaks
  at other ratios.
- The signal driving mean_r is dominated by SK-N-SH (~0.45 across all
  mixes), with small modulations from K562/HepG2 swinging things.

## What to try next
**Experiment 008**: stratified cCREs by type — equal counts of PLS,
pELS, dELS, CTCF, plus random. Currently dELS dominates the cCRE pool
~80%; rebalancing by type might give the model broader regulatory
grammar coverage (and especially PROMOTER signal which is currently
weak — only 4% of cCRE samples).
