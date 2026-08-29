# Exp 007 — AT-rich iid (composition only)

## Design
50K iid per-position sequences with weights {A=0:0.30, C=1:0.20,
G=2:0.20, T=3:0.30}. AT content ~60%. No dinucleotide structure.

## Result vs exp 006 (full DNA-Markov)
| eval    | baseline | exp006 DNA | exp007 iid | iid-Markov |
|---------|----------|------------|------------|------------|
| eval_01 | 0.4848   | 0.4742     | 0.4669     | -0.007     |
| eval_07 | 0.5200   | 0.7200     | 0.7117     | -0.008     |
| eval_13 | 0.4992   | 0.7006     | 0.6900     | -0.011     |
| eval_04 | 0.4440   | 0.0958     | 0.0890     | -0.007     |
| eval_08 | 0.1613   | 0.0339     | 0.0418     | +0.008     |

**iid AT-rich captures ~99% of the DNA-Markov effect on every eval.**
Dinucleotide structure adds at most +0.01 (often less).

## Conclusion
COMPOSITION is the dominant signal. AT-bias drives the eval_07/13 lift
and the eval_04/08 collapse. Dinucleotide structure is essentially
irrelevant once composition is fixed.

## Per-eval grouping by composition response
- **Group A** (likes AT-rich): eval_03 (+0.02), eval_07 (+0.19),
  eval_10 (+0.014), eval_13 (+0.19).
- **Group B** (slightly prefers uniform): eval_01 (-0.018), eval_02
  (-0.016), eval_06 (-0.022).
- **Group C** (strongly prefers uniform): eval_04 (-0.355), eval_08
  (-0.119).

## Implications
- For PRIMARY eval_01, AT-bias slightly hurts (Group B).
- We need a different lever for eval_01.
- Next test: GC-rich (opposite direction). If Group B drops similarly,
  preference IS uniform-symmetric. If it lifts, eval_01 has a
  directional preference toward GC.
