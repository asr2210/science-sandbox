# Experiment 011 — stratified positives + paired flanks (doesn't stack)

## Design
- 25K stratified cCRE positives (5K each PLS/pELS/dELS/CTCF/DNH3).
- 25K paired flanks, one per positive (±1.5-3kb shift, overlap-checked).

## Hypothesis
Two winners (008 stratification + 010 paired flanks) should stack
additively: stratification helps enhancer evals, flanks help K562
and general evals. Predicted: 011 > 010 (>0.158).

## Result — WORSE than either (mean_r 0.140)
| eval | 005 | 008 | 010 | 011 |
|------|-----|-----|-----|-----|
| 01   |0.156|0.159|**0.166**|0.135|
| 04   |0.150|0.149|**0.169**|0.154|
| 06   |0.187|**0.202**|0.193|0.133|
| 07   |0.174|0.152|0.167|**0.187**|
| 10   |0.117|0.143|0.146|**0.159**|
| 11   |0.187|**0.202**|0.193|0.133|
| 13   |0.157|0.132|0.121|**0.158**|
| mean |0.156|0.154|**0.158**|0.140|

K562 goes NEGATIVE again (-0.05 on enhancer evals). Enhancer evals
(06/11) crater from 0.193 to 0.133.

## Interpretation
Stratification cuts dELS density from ~74% (natural) to 20% (5K of 25K),
starving the dELS signal that drives enhancer evals.

In 008 the dELS budget was 10K (40%) AND there was 10K random for
contrast — model could still learn enhancer features. In 011, only
5K dELS, paired with 5K dELS-flanks; the model sees too few examples
of the dominant cell-type-relevant pattern.

Surprising bright spots: eval_07/10/13 improve (+0.02-0.04). These
evals reward CTCF/DNH3-style content that stratification boosts.

## Theory update (T10 → T11)
- Stratification + paired flanks DO NOT stack — they interact.
- Stratification's mechanism: balances rare types at the cost of
  abundant ones. Only helps when the abundant type is already over-
  represented AND the rare ones are starved. In 010, paired flanks
  give plenty of dELS contrast already; stratification just removes
  dELS examples without adding new useful signal.
- The natural cCRE distribution is approximately the right
  distribution for these evals (on average).
- eval_07/10/13 specifically reward CTCF/DNH3-type content. Could
  be promoter-distal / insulator-style tests.

## Next
Go back to 010's recipe but address its specific holes (eval_07/13).
012 = hybrid 010 + small random component. Plan:
- 20K cCRE-centered positives (natural distribution)
- 20K paired flanks
- 10K pure random genomic
Tests if a 20% random injection recovers the eval_07/13 signal
without losing K562 gains.
