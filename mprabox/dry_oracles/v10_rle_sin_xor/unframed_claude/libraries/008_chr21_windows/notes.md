# Experiment 008 — random 200bp windows from human chr21 (hg38)

## Result
- mean_r=**0.4880**, K562=0.8993, HepG2=0.5579, SKNSH=0.0068

## Interpretation
Real DNA gives ~same scores as a uniform 41% GC iid library (exp 005,
K562=0.88, HepG2=0.55) — chr21 GC ≈ 41%. So **the predictor doesn't
respond to "realism", just to gross base composition**. There's no
hidden benefit to using real sequences over synthetic matched-composition.

SKNSH a hair above zero but well within noise.

Optimum library is uniform 50% GC. Question now: can we tighten this
further (per-position balance)?
