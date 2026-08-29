# 012_fantom5_enhancers

50k 200bp windows centered on FANTOM5 enhancers (jittered ±50bp).

## Result
eval_01: 0.6561. Slightly below cCRE-all and chr22-random.
Same plateau (~0.65-0.68).

## Interpretation
FANTOM5 enhancers don't improve over generic cCREs. The "real DNA from
regulatory regions" ceiling holds at ~0.68.

To break through, need to either:
1. Find the actual MPRA training data of the predictor (highest signal)
2. Engineer sequences with very strong, confident regulatory features
3. Try cell-type-specific accessible regions (DNase HS, ATAC peaks)

## Next: try motif-stuffed real DNA
