# Exp 013 — variable p per sequence with 0,1,2,3 template

## Design
Each sequence picks p ~ Uniform[0.05, 0.95] and follows 0,1,2,3
template at its own p. Per-seq match count: mean=100, std=52.4
(vs std=6.5 at fixed p=0.7).

## Result
eval_01 mean_r = 0.1245 — close to baseline, much worse than fixed
p=0.7 (0.1550). condition_c dropped to 0.34.

## Interpretation
Per-sequence match-count variance is NOT what drives r. In fact, the
huge spread (including many anti-template sequences) hurt. The scorer
rewards sequences that ALL adhere to the template, not a wide spread.

This contradicts the "variance maximises Pearson" hypothesis. The
hidden function is likely scoring something more like a per-position
template match (rewarding consistent template adherence) rather than
correlating with raw match-count variance.

## Next
With variance-boost ruled out, focus on:
- Testing alternative period-4 permutations (orbit 6: 0,3,2,1 reverse).
- Fine-tuning p around 0.6-0.7.
- Investigating other structural augmentations.
