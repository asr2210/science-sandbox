# Exp 006 — Multi-source diverse mix

## Design
50K sequences in three equal parts:
- 16,667 ENCODE cCRE-centered windows
- 16,667 random hg38 windows
- 16,666 synthetic backgrounds with ~10 dense motifs each
GC = 0.457.

## Result
eval_01 = 0.0446. eval_08 = 0.0802. Average across evals ≈ 0.045.

| eval | random | dinuc | hg38 | cCRE | motif | multi |
|------|--------|-------|------|------|-------|-------|
| 01 | 0.042 | 0.009 | 0.049 | 0.043 | 0.040 | 0.045 |
| 07 | 0.025 | 0.007 | 0.032 | 0.025 | 0.028 | 0.030 |
| 08 | 0.124 | 0.066 | 0.049 | 0.066 | 0.124 | 0.080 |
| 13 | 0.020 | 0.002 | 0.034 | 0.025 | 0.022 | 0.032 |

## Interpretation
Mixing sources didn't break out of the band. eval_01 lifted very slightly
over single-source libraries. eval_08 lands between random (0.124) and
regulatory (0.066) as expected for a mixed distribution.

The 0.04–0.05 floor for eval_01 holds. It cluster across 6 wildly different
designs. Either the trained model is the bottleneck, or my hypothesis space
(natural DNA + simple synthetic) is too narrow.

## Next step
Test if **massively dense** motif content (40+ motifs per 200bp, leaving
little background) can move eval_01. This is qualitatively different — the
sequence statistics become dominated by motif content rather than random
background.

## Time
10s evaluator, 42s wall.
