# 008_ccre_dhs_combined

## Setup
25k cCREs (halved exp 002 quotas) + 25k DHS sites (numsamples ≥ 5, uniform
random from DHS index). Summit/midpoint-centered 200bp windows.

## Result vs exp 002 (pure cCRE)
| Eval        | 002    | 008    | Δ       |
|-------------|--------|--------|---------|
| eval_01     | 0.6921 | 0.6835 | −0.009  |
| eval_03     | 0.6992 | 0.6909 | −0.008  |
| eval_04/09  | 0.5977 | 0.5728 | −0.025  |
| eval_07     | 0.7562 | 0.7549 | −0.001  |
| eval_08     | 0.1248 | 0.1224 | −0.002  |
| eval_10     | 0.6673 | 0.6650 | −0.002  |
| eval_13     | 0.7466 | 0.7424 | −0.004  |

## Interpretation
Combining cCRE + DHS is slightly *worse* than cCRE alone. DHS uniformly
sampled is dominated by tissue-specific elements (most DHS sites have
numsamples in single digits even after the >=5 filter), many of which are
active in non-K562/HepG2/SKNSH biosamples. Those don't add evaluable signal.

## Theory update
"More regulatory data" isn't strictly better if the added data is biased
toward biosamples that don't match the eval. The model has fixed capacity
(50k examples); each example must align with the eval distribution to be
useful.

## Implication
- Don't add data that's off-distribution from the eval — even if it's
  "real" regulatory data.
- For cross-cell-type generalization, the optimal mix likely weights toward
  data that intersects MANY cell types (tissue-invariant) and adds
  cell-type-specific data only when the eval is in those cell types.
- Next: try DHS filtered for the *relevant* tissue components
  (Myeloid/erythroid for K562, Digestive/Epithelial for HepG2, Neural for
  SKNSH) to make the DHS arm actually match the eval distribution.
