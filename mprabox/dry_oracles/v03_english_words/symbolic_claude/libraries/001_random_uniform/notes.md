# Exp 001: Random uniform baseline

## What
50,000 uniform random strings, length 200, alphabet {0,1,2,3}. Seed=0.

## Result
- eval_01 mean=0.4192 (K562=0.5902, HepG2=0.6228, SKNSH=0.0445)
- Most evals cluster around mean=0.42 (range 0.385–0.428)
- eval_08 is the outlier (lower, mean=0.385)

## Observations
- mean_r is exact average of (K562_r + HepG2_r + SKNSH_r) / 3.
- The K562 and HepG2 columns show high r (~0.6) even for random input.
- SKNSH r is essentially 0 for random.
- This pattern strongly suggests "r" is a correlation (Pearson) between an oracle's
  predicted activity for our sequences and some target signal.
- Several evals produce identical (K562,HepG2,SKNSH) triples → they share underlying
  models or targets; only 14 nominal evals reduce to ~5 distinct (K562,HepG2,SKNSH)
  triples on random input.

## Distinct (K562,HepG2,SKNSH) clusters in this experiment
- A: (0.5902, 0.6228, 0.0445) — evals 01, 14
- B: (0.5897, 0.6225, 0.0438) — evals 02, 05
- C: (0.5909, 0.6203, 0.0458) — evals 03, 12
- D: (0.5967, 0.6309, 0.0562) — evals 04, 09
- E: (0.5909, 0.6213, 0.0454) — evals 06, 11
- F: (0.5981, 0.6238, 0.0571) — eval 07
- G: (0.5335, 0.5762, 0.0461) — eval 08
- H: (0.5963, 0.6316, 0.0549) — eval 10
- I: (0.5910, 0.6249, 0.0680) — eval 13

So 9 distinct triples across 14 evals. Maybe each eval uses a slightly different
model/seed but on a common signal.

## Time
~2 minutes for 50k sequences.
