# 017 block_dirichlet

50k sequences, each = 4 blocks x 50bp, each block its own Dirichlet(0.5) composition.

## Result
eval_01 = +0.0001 (worse than pure Dirichlet +0.0030).

## Conditions vs pure Dirichlet(0.5) on eval_01
| | a | b | c | mean |
|---|---|---|---|---|
| pure dirichlet (005) | +0.0003 | +0.0070 | +0.0016 | +0.0030 |
| block dirichlet (this) | +0.0039 | -0.0001 | -0.0037 | +0.0001 |

Block structure raises condition_a (more structured) but tanks b and c.
Net: hurts eval_01.

## Interpretation
Splitting into compositional blocks reduces overall composition diversity per sequence
(each seq's aggregate composition averages toward uniform), explaining the c drop.
The b drop (from +0.0070) suggests per-seq compositional consistency matters for b.

Pure Dirichlet(0.5) still wins.
