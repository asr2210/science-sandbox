# Experiment 011: Composition tilt — more DNase

## Design
50K sequences:
- 15K cCREs (6K dELS + 4K pELS + 2K PLS + 1.5K CA_TF + 1.5K CTCF)
- 10K each K562/HepG2/SKNSH DNase peaks (30K total)
- 5K random
Seed=11. Same source mix as 009 but cCRE→DNase=5K shifted.

## Results — REGRESSION vs 009
| eval | 009 (best) | 011 | Δ |
|---|---|---|---|
| 01 | **0.0772** | 0.0759 | -0.0013 |
| 02 | **0.0755** | 0.0742 | -0.0013 |
| 03 | **0.0955** | 0.0948 | -0.0007 |
| 04 | **0.0913** | 0.0888 | -0.0025 |
| 06 | **0.0765** | 0.0755 | -0.0010 |
| 07 | **0.1437** | 0.1420 | -0.0017 |
| 08 | 0.0639 | **0.0661** | +0.0022 |
| 10 | **0.1286** | 0.1268 | -0.0018 |
| 13 | 0.1409 | **0.1414** | +0.0005 |
Time: 90s

011 < 009 on 7/9 distinct eval sets.

## Per-cell eval_01
- K562: 0.0789 (vs 009 0.0799, -0.0010)
- HepG2: 0.0798 (vs 009 0.0812, -0.0014)
- SKNSH: 0.0689 (vs 009 0.0705, -0.0016)
All three cells regress.

## What I learned
**009's cCRE/DNase split is at a local optimum.** Shifting MORE toward
DNase doesn't help — even per-cell prediction got worse (despite
having +5K DNase per cell). The model already had enough DNase signal
at 009's 8K/cell; the marginal value of cCRE diversity (~5K cCREs)
is greater than the marginal value of more DNase per cell.

The slight improvement on eval_08 hints that eval_08 may favor
cell-type-specific signal more than the others.

## Theory update
- Within the cCRE+DNase+random framework, ~20K cCRE / ~25K DNase is the
  composition ceiling
- Improvements beyond 009 will require **qualitatively new** signal,
  not composition tweaks of the same sources

## Next: add cell-type diversity (exp 012)
Add DNase peaks from non-measured cell types. Hypothesis: exposing
the model to MORE cell-type regulatory contexts strengthens its
learning of UNIVERSAL TF motif features (which transfer across cells),
without harming the 3 measured cells.

Plan: replace some cCREs with DNase from 3 unmeasured cells
(GM12878 lymphoblast, A549 lung, HCT116 colon).
