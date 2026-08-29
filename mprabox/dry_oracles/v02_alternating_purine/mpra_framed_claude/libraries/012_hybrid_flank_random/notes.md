# Experiment 012 — hybrid cCRE+flanks + 10K random (modestly worse)

## Design
- 20K cCRE-centered positives (natural distribution)
- 20K paired flanks (one per positive)
- 10K pure random genomic

## Hypothesis
Adding random should recover 010's losses on eval_07 (-0.007) and
eval_13 (-0.036) without sacrificing the K562/general-eval gains.

## Result — modestly worse (mean_r 0.153 vs 010's 0.158)
| eval | 010 | 011 | 012 |
|------|-----|-----|-----|
| 01   |**0.166**|0.135|0.161 |
| 04   |**0.169**|0.154|0.155 |
| 06   |**0.193**|0.133|0.187 |
| 07   |0.167|**0.187**|0.152 |
| 13   |0.121|**0.158**|0.118 |
| mean |**0.158**|0.140|0.153 |

eval_07 went DOWN (-0.015 vs 010), not up. eval_13 went DOWN too
(-0.003). The random hypothesis is FALSIFIED.

## Re-interpretation
Look at the table: 011 had the HIGHEST eval_07 (0.187) and eval_13
(0.158) of all libraries, despite being the lowest-mean library and
having NO random component. So eval_07/13 don't reward random —
they reward STRATIFICATION (specifically CTCF/DNH3 over-representation
from 011's 5K each).

In 010, CTCF and DNH3 sampled at natural frequency (~3% and ~2%) =
only ~750 CTCF and ~500 DNH3 examples. In 011, 5K each = 7-10x more.

eval_07/13 likely tests CTCF-binding or insulator/promoter-distal
content; the model needs enough examples of these patterns to learn
them.

## Theory update (T11 → T12)
- Different evals reward different *content types*:
  - eval_06/11: dELS quantity (enhancer-like)
  - eval_07/13: CTCF/DNH3 quantity (insulator/promoter-distal)
  - evals 01-04: general cCRE+flank discrimination
- 011 over-corrected: stratification 1:1:1:1:1 starved dELS for
  the CTCF/DNH3 boost.
- The right mix is *asymmetric stratification*: keep dELS dominant
  (12-15K of 25K) but ensure CTCF and DNH3 each have 3-5K.

## Next
013 = paired flanks (proven) + boosted CTCF/DNH3.
- 15K uniform cCRE positives (natural distribution, ~80% dELS = ~12K)
- 5K CTCF + 5K DNH3 explicit (boosted from natural ~750/500)
- 25K paired flanks (one per positive)
Expected: lifts eval_07/13 without losing 010's general edge.
