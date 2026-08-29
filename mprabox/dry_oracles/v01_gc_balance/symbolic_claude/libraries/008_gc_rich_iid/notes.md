# Exp 008 — GC-rich iid (symmetry test)

## Design
50K iid per-position sequences, weights (0.20, 0.30, 0.30, 0.20) for
{A,C,G,T}. GC content ~60%. Mirror of exp 007 (AT-rich at 60%).

## Result vs AT-rich (exp 007) and baseline
| eval    | baseline | AT-rich | GC-rich | AT-base | GC-base |
|---------|----------|---------|---------|---------|---------|
| eval_01 | 0.4848   | 0.4669  |-0.2411  | -0.018  | -0.726  |
| eval_07 | 0.5200   | 0.7117  |-0.5893  | +0.192  | -1.109  |
| eval_13 | 0.4992   | 0.6900  |-0.5586  | +0.191  | -1.058  |
| eval_04 | 0.4440   | 0.0890  | 0.1422  | -0.355  | -0.302  |
| eval_08 | 0.1613   | 0.0418  | 0.0577  | -0.120  | -0.104  |
| eval_03 | 0.4843   | 0.5030  |-0.2924  | +0.019  | -0.777  |

## The big finding
**Highly asymmetric.** AT-rich and GC-rich are NOT mirror images:
- AT-rich is mildly bad / very good (depending on eval).
- GC-rich is catastrophically bad on most evals.
- Some evals went NEGATIVE (-0.5+) on GC-rich.

The score function strongly REWARDS AT-leaning composition and PUNISHES
GC-leaning composition. Magnitude of asymmetry on eval_07: AT lift was
+0.19, GC drop was -1.11 — a 6x asymmetry.

## Implications
- Mapping {0,1,2,3} = {A,C,G,T} (under alphabetical ordering) is
  consistent with reality: human DNA is AT-rich; the model and target
  expect AT-leaning sequences. (Strong confirmation but not proof —
  any 4-permutation that places A,T at indices 0,3 fits the data.)
- Composition axis is now well-mapped. Uniform is near-optimum on
  eval_01; AT-rich helps some evals (07/13/03) but hurts eval_01 mildly;
  GC-rich hurts everything massively.
- To find a lift on eval_01, we need OTHER axes (k-mer structure,
  motifs, per-sequence properties).
