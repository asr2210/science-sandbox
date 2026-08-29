# Experiment 019 — type-targeted flank distance (doesn't work)

## Design
- 15K uniform cCRE + 15K FAR flanks (1500-3000bp)
- 5K CTCF + 5K NEAR flanks (500-1500bp)
- 5K DNH3 + 5K NEAR flanks (500-1500bp)

## Hypothesis
Type-targeted flanks isolate signals: uniform/dELS gets far flanks
for eval_06/11 enhancer signal; CTCF/DNH3 gets near flanks for
eval_07/13.

## Result — mean_r 0.142 (worse than 013)
| eval | 013 | 018 (all-near mix) | 019 (targeted) |
|------|-----|--------------------|----------------|
| 06/11 |**0.218**|0.097|0.162|
| 07    |0.177|**0.203**|0.162|
| 13    |0.126|0.173|**0.158**|
| mean  |**0.166**|0.133|0.142|

eval_06/11 dropped to 0.162 even though uniform cCRE got far flanks.
Apparently the model can't fully isolate signals when training data
mixes flank distances.

## Interpretation
Type-targeted flanks don't simply preserve signal: when ANY near-flank
pairs exist in the library, the model's K562 enhancer signal weakens.
The eval_06/11 signal seems to require pure far-flank training across
ALL positives, not just uniform/dELS ones.

## Theory T18
- Multi-distance flanks can't simply be additively combined.
- 013's strength is that it's all-far flanks for ALL positives —
  homogeneous training signal.
- The eval_07/13 lift from near flanks is REAL but comes at a
  homogeneity cost that hurts everything else.

## Next
Move to a different axis: 020 = positional jitter on cCRE midpoint.
±50bp jitter as data augmentation. Tests if positional invariance
helps the model learn more robust motif features.
