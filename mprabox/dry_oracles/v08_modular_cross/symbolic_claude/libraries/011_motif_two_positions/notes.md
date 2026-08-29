# 011 — 4-bucket motif at TWO positions (50 and 90)

- Each string: poly-X motif at BOTH pos 50-69 AND 90-109. 40 chars motif.
- mean_r eval_01: -0.0053 (vs +0.0061 in exp 005). Catastrophic decrease.
- All evals went negative across all conditions.
- Conclusion: Adding a second motif at pos 50 actively *hurts*.
  Either the predictor saw two motifs as conflicting signals, or
  the motif at pos 50 was in a "bad" position for ALL evals
  (consistent with exp 010 where pos 0 hurt eval_01 specifically).
