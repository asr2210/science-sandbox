# 012_tss_plus_random_5050

25k TSS-proximal + 25k uniform random ACGT. 50/50 mix.

## Result
eval_01: 0.4392 (vs 008: 0.5035, -0.064)
eval_08: 0.0775 (vs 001 best: 0.110, -0.033)

**Even worse than 011** — the 50/50 mix loses on EVERY eval
compared to either pure source.

## Per-eval delta vs 008 (TSS ±25kb pure)
- eval_01: -0.064
- eval_03: -0.061
- eval_04: -0.085
- eval_06: -0.069
- eval_07: -0.026
- eval_08: -0.015  (worse, despite 50% random!)
- eval_10: -0.061
- eval_13: -0.043

## Theory v9 confirmed strongly
The model cannot hold two distinct distributions in its capacity.
Even with 25k samples each (enough to learn each separately), the
joint fit is worse than either alone. Striking: eval_08 (which loves
pure random) is now WORSE than mixed runs with less random because:
- 25k random isn't enough to fully calibrate the model for random-
  like sequences
- 25k natural pulls the model's predictions toward natural-DNA
  patterns even when given random input

So eval_08 success on 001 was due to the model having committed
ENTIRELY to random — every weight tuned to predict activity from
random sequences. As soon as some natural is introduced, the model
becomes a hybrid that's bad at both.

## Implication
Don't mix distinct distributions. Commit to one distribution that
best matches the eval mean. For our purposes, this is TSS-proximal
natural (008).

The natural plateau at ~0.50 is fundamental for our budget unless we
find a single distribution that fits eval better than TSS-proximal,
OR we use a method that exploits the multi-distribution structure
without naive mixing (e.g., conditioning).
