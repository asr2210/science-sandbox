# Experiment 006 — low-diversity library (single scaffold + 5% noise)

## Result
- mean_r=**0.1802**, K562=0.6944, HepG2=-0.1569, SKNSH=0.0032

## Interpretation
**Negative HepG2!** First time. Low diversity ≠ better correlation.
The predictors don't just produce noise around a fixed mean — they
extrapolate differently in low-diversity regimes (likely OOD for them).

So K562 r=0.99 with random uniform is NOT a low-variance artifact in
the trivial sense. The predictors are doing something real, and uniform
random sequences are where they agree best.

This means the optimum is probably near the baseline. Hard to beat
unless I find a regime where predictors agree even better than on
i.i.d. uniform. Try CpG-depleted (real-human-like dinucleotide
structure) next.
