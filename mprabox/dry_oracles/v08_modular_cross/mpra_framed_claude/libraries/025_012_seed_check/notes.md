# Experiment 025 — 012 recipe stability test (seed=125)

## What I tested
Identical to 012 except SEED=125 instead of SEED=12. Tests whether
012's mean=0.0029 was the recipe's stable value or a lucky draw.

## Result — mean slightly HIGHER, but per-eval shuffled
Mean = 0.0034 (vs 012's 0.0029) — slight improvement.

Per-eval comparison vs 012 (seed=12):
- eval_01,02,03,06,11,14: ALL HIGHER (0.0048-0.0067 vs 012's 0.0030-0.0036)
- eval_07: 0.0041 vs 012's 0.0024 (HepG2 0/SKNSH 0.0116)
- **eval_08: -0.0002 vs 012's 0.0117** — BIG LOSS, "lucky draw"
- eval_10: -0.0042 vs 012's 0.0057 (loss)
- eval_13: 0.0016 vs 012's -0.0001 (slight gain)

## What this tells me
**Major finding:** the recipe's per-eval performance varies
substantially seed-to-seed. eval_08's 0.0117 in 012 was a LUCKY
DRAW, not a stable property. With seed=125 it disappears.

The broad evals (01-06, 11, 14) are MORE STABLE and they consistently
lift to 0.003-0.007.

The recipe-level mean is ~0.003-0.004 regardless of seed; individual
eval magnitudes shuffle.

## Updates to theory
**v3.16 → v3.17:** Many "specific eval wins" attributed to recipe
features may actually be seed-driven random luck. The reliable
signal is the BROAD eval lift (~0.003-0.007 on evals 01-06, 11,14).

Specific evals (07, 08, 10, 13) have high seed variance. The
recipe creates an *opportunity* for these evals to fire, but
whether they fire on any given seed is partially stochastic.

**Implication for final library:** the safest choice is a recipe
that maximizes BROAD eval lift (more stable) rather than chasing
specific eval wins.

## Next
Verify by testing 018 recipe (high-density motifs + pELS) with a
different seed. If 018's eval_07=0.0109 is also seed-luck, that
further confirms the broad-vs-specific stability divide.
