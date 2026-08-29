# 013_five_way_fantom — notes

## Design
20K natural + 12K cCRE off-center + 8K DHS + 5K FANTOM5 + 5K mouse.
Same 5-way mix as previous winner but adding 5K FANTOM5 enhancers.

## Result
- eval_01 = 0.4990 (vs 0.5012 exp 011, -0.002)
- Adding FANTOM5 marginally hurts; redundant with cCRE/DHS
- eval_08 = 0.0978 (still ~0.10)

## Interpretation
FANTOM5 enhancers (CAGE-defined) are essentially the same information
as cCRE/DHS at the model's level. They're another atlas of "open
regulatory regions in some cell type", which the model has already seen.

Diminishing returns: 3+ atlas of similar regulatory regions saturates.

## Bigger picture
The plateau around 0.50 holds. The 4-way mix (exp 011) is the best
configuration I've found. Adding more sources of the same kind doesn't
help. To go higher I need either:
- A genuinely different kind of sequence (cross-species TF peaks,
  variant-perturbed natural, etc.)
- A clever sampling that maximizes some sequence-level diversity
- Or a different paradigm I haven't considered

## Next test
Try TF ChIP peaks (ReMap or similar) — verifies in vivo TF binding,
different signal modality from open chromatin or CAGE.
Or: noise-floor estimate by re-running exp 011 with seed=1 to know if
±0.005 differences are real.
