# Experiment 015: SKNSH-heavy library

## Design
- 10K cCRE (5K dELS + 3K pELS + 1K PLS + 1K CTCF)
- 8K K562 DNase + 8K HepG2 DNase + 14K SKNSH DNase
- 5K SKNSH H3K27ac
- 5K random
SKNSH = 19K (38% of library), 2.4x other cells. Seed=15.

## Results — SKNSH did NOT lift
eval_01 = **0.0730**, SKNSH = **0.0646** (vs 009 SKNSH 0.0705, worse).

| eval | 009 | 015 |
|---|---|---|
| 01 mean | 0.0772 | 0.0730 |
| 01 K562 | 0.0799 | 0.0770 |
| 01 HepG2 | 0.0812 | 0.0773 |
| 01 SKNSH | 0.0705 | **0.0646** |

Despite getting 2.1x more SKNSH peaks, SKNSH per-cell DROPPED.

## What I learned
**SKNSH is not data-limited; it's sequence-intrinsic-limited.**
Doubling SKNSH-specific data made SKNSH eval WORSE, not better. Possible
reasons:
- SKNSH MPRA activity is inherently harder to predict from sequence
  (more noisy assay? More chromatin-context-dependent activity?)
- Excess SKNSH peaks crowded out cCRE diversity (only 10K cCREs vs 20K
  in 009), which apparently mattered

Combined with 014 (top-signal didn't help), 012 (multi-cell didn't help),
the pattern is consistent: **within-noise-band on eval_01 regardless of
sensible composition adjustments**.

## Theory update
The bottleneck on this pipeline appears to be **model capacity / training
stochasticity**, not library composition (within the "genomic regulatory"
class). Single-seed eval_01 has noise ±0.004; any change smaller than
that is invisible.

## Next: change the AXIS of variation
Composition tweaks have plateaued. Try positional/window augmentation:
**exp 016: multi-window on 009 composition** — 3 shifted windows per loci.
Gives the model multiple "views" of the same regulatory element. exp 007
tried this on cCREs only (within noise); test on the hybrid mix now.
