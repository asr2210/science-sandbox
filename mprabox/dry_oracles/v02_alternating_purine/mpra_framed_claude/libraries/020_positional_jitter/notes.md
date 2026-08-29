# Experiment 020 — positional jitter (±50bp)

## Design
- Same as 013 but with ±50bp uniform jitter on positive cCRE midpoints.
- Flanks anchored on unjittered cCRE midpoint.

## Result — mean_r 0.156 (worse than 013)
| eval | 013 | 020 |
|------|-----|-----|
| 06/11 |**0.218**|0.213|
| 07    |**0.177**|0.137|
| 10    |0.151|**0.173** (new high) |
| 13    |0.126|0.113|
| mean  |**0.166**|0.156|

eval_10 new high, eval_06/11 nearly preserved, but eval_07/13 drop.

## Interpretation
Positional jitter helps motif-localization evals (eval_10) by
teaching position-invariance. But hurts eval_07/13 — those evals
may require precise positional cues.

K562_r on eval_07/13 goes very negative (-0.04, -0.05) — model
confused by jitter noise relative to fixed-position flanks.

## Theory T19
Position invariance is a real signal axis but conflicts with
position-sensitive evals.

## Best-per-eval audit (across 020 libraries)
| eval | best lib | best score |
|------|----------|-----------|
| 01-04 | 013 | 0.166-0.184 |
| 05    | 013 | 0.173 |
| 06    | 013 | 0.218 |
| 07    | 018 | 0.203 |
| 08    | 014 | 0.048 |
| 09    | 013 | 0.169 |
| 10    | 020 | 0.173 |
| 11    | 013 | 0.218 |
| 12    | 013 | 0.184 |
| 13    | 002 | 0.176 |
| 14    | 013 | 0.173 |

Oracle mean (best per eval) = 0.174. Only +0.008 headroom over 013.

## Next
021 = test positive:flank ratio. 30K positives (013 ratio) + 20K
far flanks (first 20K positives get a flank). Tests if more positive
diversity + less flank signal beats 013's exact 25:25.
