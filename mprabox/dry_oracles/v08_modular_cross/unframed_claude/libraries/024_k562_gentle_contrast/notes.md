# 024 — K562 motifs gentle GC contrast (60/40)

## Method
25k active: GC=60, 8 K562 motifs (exp 005 panel exactly).
25k null: GC=40, no motifs.

## Results (eval_01)
mean_r = +0.0037 (K562=+0.0033, HepG2=+0.0005, SKNSH=+0.0074)

## Lesson
- K562 DROPPED to +0.0033 (was +0.0077 at GC=50, +0.0089 at GC=65).
  Going from GC=50 to GC=60 reduced K562 r — unexpected.
- HepG2 collapsed to +0.0005 (vs +0.0056 at GC=50). GC=60/40 already
  hurts HepG2.
- SKNSH SHOT UP to +0.0074 (new SKNSH max for eval_01!).
- The active half (motifs + GC=60) looks "SKNSH-like" to the SKNSH model.

## Implication
- Per-cell maxima are diverging across designs:
  - K562 max: +0.0089 in exp 012 (K562-sat GC=65/25)
  - HepG2 max: +0.0069 in exp 015 (real H3K27ac)
  - SKNSH max: +0.0074 in exp 024 (K562 motifs GC=60/40)
- If achievable in single library, mean would be (89+69+74)/3 = +0.0077.
- But achievable conditions are mutually exclusive in a single homogeneous
  library.

## Next (exp 025)
Triple bank — split 50k into 3 cell-specific banks of ~16.5k each, each
internally 50/50 active/null. Each bank engineered for max per-cell lift.
Hypothesis: per-cell r scales sub-linearly with bank size, but additive
across cells could push mean above plateau.
