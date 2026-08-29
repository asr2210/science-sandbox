# 010_diff_activity

## Design
50,000 = 2,500 regions × 5 tiles for each of 4 classes:
  - K562-specific DHS (only in K562)
  - HepG2-specific DHS
  - SKNSH-specific DHS
  - Shared (DHS in all 3 cell types)
Maximizes cross-cell-type activity variance.

## Result vs 005 (cCRE dense)
                eval_01  K562    HepG2   SKNSH   eval_08
005 cCRE dense: 0.3177   0.146   0.185   0.622   0.076
010 diff:       0.3180   0.139   0.188   0.627   0.077

Essentially identical. K562 -0.007, HepG2 +0.003, SKNSH +0.005.
Net: -0.0003 on eval_01.

## Interpretation
Differential activity stratification doesn't lift either. The model
sees the same plateau regardless of source-selection refinement
(broad cCRE, K562 DHS, top signal DHS, differential DHS, promoter
dense — all land at ~0.315-0.318).

This is strong evidence the plateau is a property of the model +
50K library budget, not of the library design choices I've explored
within natural-genomic regulatory regions.

## Theory T7 → T8
The natural-genomic single-source family is exhausted. Differential-
activity stratification was the "smart" design I had highest hopes
for, and it gives the same plateau as naive dense cCRE sampling.

To meaningfully test if the plateau is intrinsic, need to try
designs that are categorically different:
- Functionally-validated MPRA-positive sequences (STARR-seq)
- Conservation-filtered (phyloP > 2)
- Multi-source convergent (DNase ∩ H3K27ac ∩ TF ChIP)
- RC-augmented (strand invariance)
- Extremely dense (1K regions × 50 tiles)

## Next
Experiment 011: ENCODE STARR-seq active peaks. These are
functionally MPRA-validated — should be the closest match to
training-distribution that prepare.py's MPRA evaluates. If STARR
peaks don't lift the plateau, the plateau is very probably
intrinsic.
