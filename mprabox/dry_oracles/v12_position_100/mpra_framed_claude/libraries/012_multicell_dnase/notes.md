# Experiment 012: Multi-cell DNase diversity

## Design
50K sequences:
- 15K cCREs (6K dELS + 4K pELS + 2K PLS + 1.5K CA_TF + 1.5K CTCF)
- 15K DNase from 3 measured cells (K562/HepG2/SKNSH, 5K each)
- 15K DNase from 3 NON-MEASURED cells (GM12878/A549/HCT116, 5K each)
- 5K random
Seed=12.

Hypothesis: more cell-type contexts → stronger universal motif learning →
better generalization.

## Results — regression vs 009
| eval | 009 | 012 | Δ |
|---|---|---|---|
| 01 | **0.0772** | 0.0758 | -0.0014 |
| 02 | **0.0755** | 0.0742 | -0.0013 |
| 03 | **0.0955** | 0.0938 | -0.0017 |
| 04 | 0.0913 | 0.0898 | -0.0015 |
| 06 | 0.0765 | **0.0770** | +0.0005 |
| 07 | **0.1437** | 0.1394 | -0.0043 |
| 08 | 0.0639 | 0.0640 | 0 |
| 10 | **0.1286** | 0.1280 | -0.0006 |
| 13 | 0.1409 | 0.1412 | +0.0003 |
Time: 78s

012 < 009 on 7/9; trivial wins on 2.

## Per-cell eval_01
- K562: 0.0798 (vs 009 0.0799, ~tie despite fewer K562 peaks!)
- HepG2: 0.0804 (vs 009 0.0812, -0.0008)
- SKNSH: 0.0671 (vs 009 0.0705, **-0.0034 — biggest hit**)

## What I learned
**Adding off-target cell-type DNase peaks doesn't help and hurts SKNSH.**
K562 and HepG2 stay strong even with 5K peaks (vs 8K in 009), suggesting
~5K cell-type DNase peaks is enough to learn that cell's motifs. But SKNSH
suffers (-0.0034) when its quota drops from 9K to 5K, despite the model
seeing 15K more peaks from other cells.

This suggests:
- Cell-type signal saturates ~5K peaks for "easy" cells (K562, HepG2)
- SKNSH is harder and needs MORE per-cell peaks (was 9K in 009 → 0.0705,
  is 5K here → 0.0671)
- Off-target cell DNase does NOT substitute for on-target DNase

## Theory update
- The 3 measured cells are the actual eval targets. Diversity from
  unmeasured cells doesn't help the model predict measured cells better.
- The bottleneck is SKNSH. It needs more, not less, per-cell data.
- 010/011/012 all regress slightly from 009 (~0.001-0.002 on eval_01).
  This is suspiciously close to noise floor — must measure with reseed.

## Next: measure noise floor (exp 013)
Rerun 009 composition with SEED=13. If eval_01 lands 0.075-0.078, then
010-012 are within noise and we can't distinguish "neutral" from "harmful"
without multiple replicates. If 013 lands ~0.0770, then 009 is real and
010-012 are genuine regressions.
