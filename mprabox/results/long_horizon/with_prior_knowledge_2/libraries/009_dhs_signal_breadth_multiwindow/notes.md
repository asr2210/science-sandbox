# 009_dhs_signal_breadth_multiwindow

## What I tested
25,000 unique DHS elements (003-style: 12.5K mean_signal-weighted +
12.5K numsamples-weighted, disjoint), with TWO 200bp windows per
element (summit-centered, summit+100bp shifted). 50K total seqs × 3
seeds.

Structural test: more elements × 1 window vs fewer elements × 2 windows
at fixed total budget.

## Result — clear loss
| metric   | 009    | 003    | Δ      |
|----------|--------|--------|--------|
| eval_01  | 0.6994 | 0.7327 | -0.033 |
| eval_07  | 0.7198 | 0.7618 | -0.042 |
| eval_08  | 0.6342 | 0.6984 | **-0.064** |
| eval_09  | 0.8366 | 0.8685 | -0.032 |
| eval_13  | 0.7070 | 0.7469 | -0.040 |
| cross-14 | 0.7358 | 0.7735 | -0.038 |

Per-seed eval_01: 0.7374 / 0.6753 / 0.6854 (std ≈ 0.027).

eval_08 is the biggest loser (-0.064). Whatever eval_08 measures
strongly rewards element diversity. eval_07 and eval_13 (cell-type-
specific signal) also took clear hits.

## Why it lost
Halving unique element count from 50K to 25K is a substantial
information loss. Within-element augmentation (one shifted window with
100bp overlap) does NOT recover that loss: the second window covers
mostly the same regulatory grammar as the first — adjacent positions
in a 200bp DHS share the same TF-motif content. The model gets two
similar training examples instead of one example from each of two
distinct regulatory elements.

## Implication for next experiments
**Element diversity is the dominant signal at 50K budget.** The 003
recipe (50K unique elements via additive signal+breadth) is robust to
this kind of attempted improvement.

Pivot direction:
- Don't reduce unique element count for sequence augmentation.
- The next informative experiment should add a TRULY ORTHOGONAL data
  axis (not derived from DHS Index alone).
- Candidates:
  * SEI chromatin state regions (different annotation source, helps
    eval_07/13 in published `dhs_sei` baseline).
  * H3K27ac-weighted DHS (direct activity mark from a different
    assay).
  * TF-binding density from ENCODE ChIP-seq peaks.
  * Cross-species conserved element overlap (PhastCons/UCEs).
