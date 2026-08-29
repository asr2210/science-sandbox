# Experiment 011 — chr19 windows filtered to 40-50% GC

## Hypothesis
If sweet-spot GC (~50%) is the lever for natural DNA, filtering
chr19 windows to 40-50% GC should beat plain chr19.

## Method
Random chr19 200bp windows, kept only if 40-50% GC. 138K attempts
to yield 50K.

## Results
- eval_01: 0.0439 (full chr19: 0.0502)  → WORSE
- eval_08: 0.0678 (full chr19: 0.0551)  → BETTER
- avg: lower than full chr19

## Interpretation
Filtering chr19 to tight GC range HURT eval_01. So the chr19
advantage isn't from being at narrow 40-50% GC; the FULL GC
distribution of chr19 (variance and tails) is part of what helps.

eval_08 went up though — likely because narrower-GC sequences
are more "uniform-random-like" which eval_08 loves.

## Theory update — T6
Different evals reward different things:
- eval_08 ("entropy-loving"): uniform random / narrow GC
- Most others: full chr19 distribution
- The chr19 advantage seems to come from BOTH ends of its GC
  distribution (sweet-spot AND tails), not just one part

A mixed library combining real chr19 + uniform random may serve
both eval_08 (random part) AND others (real DNA part).

## Next
EXP 12: mixed library 25K chr19 + 25K random uniform.
