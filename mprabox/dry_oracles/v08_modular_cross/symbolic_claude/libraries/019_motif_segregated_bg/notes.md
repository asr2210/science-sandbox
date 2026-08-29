# 019 — Motif segregated bg (bucket char absent from bg)

- mean_r eval_01: 0.0045 (DOWN from 0.0061 in exp 5).
- Removing bucket char from bg HURTS rather than helps.
- Interpretation: predictor benefits from random-uniform bg (exp 5);
  segregating the bg distorts the count statistics in a way that weakens
  the position-90 motif signal.
- Best design for eval_01 remains exp 5 (poly-X len 20 pos 90, uniform bg).
