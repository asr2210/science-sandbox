# 011_multisource_blend

30k TSS ±25kb + 10k broad genomic + 10k uniform random. 50k total.

## Result
eval_01: 0.4793 (vs 008 best: 0.5035; -0.024)
eval_08: 0.0859 (vs 001 best: 0.110; -0.024)
Mean across 14: ~0.50

**Hurt everything**, including eval_08 (which I was trying to help).

## Per-eval delta vs 008 (best single source)
- eval_01: -0.024
- eval_03: -0.022
- eval_04: -0.030
- eval_06: -0.025
- eval_07: -0.003
- eval_08: -0.006  (worse, not better!)
- eval_10: -0.017
- eval_13: -0.012

## Key insight
Mixing across distinct distributions DILUTES the model's signal on each.
The 10k random sequences are not enough to calibrate eval_08 toward
0.110 (the random library needed all 50k to reach that score), but
they ARE enough to dilute the natural training signal for the
gene-proximal evals.

So eval_08's preference for random is an "all or nothing" effect:
the model needs to commit to random training data to handle random-
like test sequences. A small random component in a mostly-natural
library doesn't carry across.

## Implication for theory (v8 refined)
Capacity constraint: at our model size and 50k sample budget, the
model has limited ability to fit multiple distinct distributions
simultaneously. Mixing distributions either dilutes the dominant one
(if minority is small) or fragments learning (if balanced). The
exception is mixing across CLOSELY RELATED distributions (e.g.,
cCREs + broad genomic, both natural human DNA), which is benign
because the underlying distribution is similar.

## Next direction
Stick with single-source TSS-proximal as the foundation. Try EVEN
LESS dilution: 45k TSS + 5k another natural source. Or pure single-
source variants I haven't tested (CpG islands, DHS peaks, etc.).
