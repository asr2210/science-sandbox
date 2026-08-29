# 009_top_signal_dhs

## Design
50,000 = 10,000 TOP-SIGNAL peaks (3.33k each from K562/HepG2/SKNSH
DNase ranked by max_density) × 5 random-offset 200bp tiles.

## Hypothesis
Top-signal peaks = highest-confidence regulatory elements = cleaner
training pairs. Should lift performance.

## Result vs 002 / 005
                eval_01  K562    HepG2   SKNSH   eval_08
002 cCRE:       0.3154   0.145   0.177   0.625   0.076
005 cCRE dense: 0.3177   0.146   0.185   0.622   0.076
009 top DHS:    0.2529   0.137   0.003   0.619   0.078

DISASTER. eval_01 dropped 0.06. HepG2 collapsed to ~0.

## Interpretation
Top-signal DHS peaks are dominated by HOUSEKEEPING regions
(constitutively active promoters, CpG islands). These regions:
- Have very HIGH but LOW-VARIANCE activity across all cell types
- Are heavily REDUNDANT — top-K562 ≈ top-HepG2 ≈ top-SKNSH peaks
  (the same housekeeping regions)
- Provide a narrow training distribution

The model trained on this can't learn what makes things
DIFFERENTIALLY active. HepG2 prediction collapses because there's
no variance signal to learn from.

## Theory T6 → T7
Training data needs not just regulatory content but ACTIVITY
VARIANCE — sequences spanning a wide range of activity levels per
cell type. Top-peak filtering reduces variance and is therefore
counterproductive. cCRE class diversity (PLS+pELS+dELS+CTCF+
DNase-H3K4me3) naturally encodes this variance.

The "right" lever: identify sequences with HIGH VARIANCE across
cell types (differentially-active elements). These give the model
the strongest signal-to-noise for learning what makes a sequence
differentially active.

## Next
Experiment 010: Build a library balanced across differential
activity classes:
- K562-specific accessible regions (K562 DHS, NOT HepG2, NOT SKNSH)
- HepG2-specific accessible regions
- SKNSH-specific accessible regions
- Shared (all 3 DHS overlap)
2,500 regions per class × 5 tiles = 50K.

Tests "cross-cell-variance is the signal" hypothesis.
