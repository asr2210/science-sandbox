# 005_ccre_dense_tile

## Design
50,000 = 10,000 cCREs × 5 random-offset 200bp tiles each. Each tile
offset uniformly in [-100, +100] from cCRE midpoint. Tests dense
per-region coverage (PARM-style).

## Hypothesis
Dense per-region coverage gives model more position-context diversity
per motif. Should lift HepG2 r above 0.18; maybe K562 lift; SKNSH
similar.

## Result vs 002
                eval_01  K562    HepG2   SKNSH   eval_08
002 cCRE 1×:    0.3154   0.145   0.177   0.625   0.076
005 cCRE 5×:    0.3177   0.146   0.185   0.622   0.076

Minute lift (+0.002). HepG2 +0.008. K562 +0.001. SKNSH -0.003.

## Interpretation
At 50K total library size, 5× redundancy per region gives ~zero lift.
PARM achieved its big numbers at 240× coverage × 30K regions = 7M
sequences. The redundancy effect either needs much more data than
50K can provide, or my model architecture saturates earlier than
PARM's.

Confirms: the mean_r ≈ 0.32 plateau is robust to natural-region
design choices (broad vs cell-specific source, single vs dense
tiling, real-only vs shuffled-paired). The plateau is set by per-
cell-type ceilings: K562 ~0.14, HepG2 ~0.18, SKNSH ~0.63.

## Theory T4
- Density × diversity tradeoff at 50K size: roughly neutral.
- The plateau is robust across all natural-sequence designs.
- Hypothesis to test: are SYNTHETIC sequences with controlled motif
  content sufficient to drive HepG2/K562 activity? If yes,
  motif identity dominates over genomic context, and the library
  can be optimized around motif diversity. If no, natural genomic
  context provides irreducible signal that synthetic libraries lack.

## Next
Experiment 006: Synthetic library — random scaffold + planted JASPAR
TF motifs. Tests motif-vs-context decomposition. Categorically
different design from all prior experiments.
