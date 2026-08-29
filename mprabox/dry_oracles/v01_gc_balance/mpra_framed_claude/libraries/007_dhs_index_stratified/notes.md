# 007_dhs_index_stratified

## Setup
50k DHS sites from Meuleman 2020 DHS index (~3.6M elements). Stratified across
16 tissue components (3125 per). Within each component, sampling probability ∝
log(1 + numsamples) so broader/more-reproducible elements are preferred.
Windows centered on DHS summit, 200bp.

## Result vs exp 002 (cCRE stratified)
| Eval        | 002    | 007    | Δ       |
|-------------|--------|--------|---------|
| eval_01     | 0.6921 | 0.6631 | −0.029  |
| eval_03     | 0.6992 | 0.6730 | −0.026  |
| eval_04/09  | 0.5977 | 0.5053 | −0.092  |
| eval_07     | 0.7562 | 0.7558 |  0.000  |
| eval_08     | 0.1248 | 0.1184 | −0.006  |
| eval_10     | 0.6673 | 0.6593 | −0.008  |
| eval_13     | 0.7466 | 0.7425 | −0.004  |

K562 r dropped (0.70 → 0.66) more than HepG2 or SKNSH r. The stratification
across 16 components dilutes elements active in K562 (which fall in
"Myeloid / erythroid").

## Interpretation
- DHS alone is *slightly* worse than cCRE for eval_01.
- Big drop on eval_04/09 suggests DHS sites carry less of whatever signal
  those evals need (possibly: they have less promoter/PLS content vs
  cCREs).
- eval_07/13 unchanged → DHS retains the motif-rich signal cCRE has.
- Cross-tissue stratification hurts cell-specific evals — the trade-off
  is real.

## Theory update
"Broader regulatory data" is not strictly better. The signal in the
training library must be aligned with the eval distribution. cCREs from
all biosamples (unstratified by component) inherently match the eval
distribution (which is K562/HepG2/SKNSH-centric) better than DHS stratified
to give equal weight to neural / embryonic / stromal etc.

For cross-cell-type generalization to *unseen* cell types, the DHS approach
might still be better in expectation; but the visible eval is biased toward
the three measured cell types, so we can't validate that directly.

## Next direction
Try combining cCREs + DHS (best of both: cCRE quality + DHS coverage).
