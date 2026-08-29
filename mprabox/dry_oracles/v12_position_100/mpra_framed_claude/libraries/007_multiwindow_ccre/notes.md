# Experiment 007: Multi-window per cCRE (positional augmentation)

## Design
16,700 unique cCREs × 3 windows each (center-60, center, center+60),
balanced across dELS/pELS/PLS/CA_TF/CA-CTCF. Seed=7.

## Results vs 003 (50K unique cCREs)
| eval | 003 | 007 | Δ |
|---|---|---|---|
| 01 | 0.0758 | 0.0747 | -0.001 |
| 03 | 0.0949 | 0.0936 | -0.001 |
| 04 | 0.0863 | 0.0896 | **+0.003** |
| 07 | 0.1444 | 0.1458 | **+0.001** |
| 08 | 0.0652 | 0.0626 | -0.003 |
| 10 | 0.1277 | 0.1303 | **+0.003** |
| 13 | 0.1429 | 0.1406 | -0.002 |
Time: 52s

## What I learned
- **Multi-window augmentation roughly matches 50K unique cCREs.**
- Some eval sets (eval_04, eval_07, eval_10) slightly improved; others
  (eval_01, eval_08, eval_13) slightly dropped.
- Net result: 16.7K unique × 3 windows ≈ 50K unique × 1.
- Tradeoff: less unique sequence diversity (16K vs 50K cCREs) is largely
  compensated for by positional augmentation.

## Interpretation
The model treats 3 shifted windows of the same cCRE as ~roughly
as informative as 3 unique cCREs. So augmentation IS a real lever —
it adds the equivalent of ~2 cCREs worth of information per cCRE.
But it doesn't open up a new performance regime.

## Implication
We've hit the cCRE plateau (~0.075-0.076). To push past, we need:
- A different sequence source (ChIP-seq peaks, cell-specific
  accessibility, MPRA datasets)
- Activity-stratified sampling (force coverage of high/low activity)
- Conservation-weighted sampling (functional importance prior)

## Next
Try cell-type-specific ChIP-seq peaks for K562/HepG2/SK-N-SH. These
have direct TF-binding evidence in our measured cell types, so should
give cleaner labels per sequence. Tests if narrowing to known-binding
regions helps performance even if it might bias generalization.
