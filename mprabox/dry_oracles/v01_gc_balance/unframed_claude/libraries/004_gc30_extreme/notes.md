# 004_gc30_extreme

30% GC. Beyond AT-rich, even more biased.

## Result
eval_01: 0.4983 (vs 0.4663 at 40% GC, vs 0.4637 random)
eval_07: 0.6972 (vs 0.7117 at 40% GC) — peaked at 40%
eval_13: 0.6737 (vs 0.6897 at 40% GC) — also peaked
eval_04: 0.1494 (vs 0.4018 random) — worse than random
eval_08: 0.0689 (vs 0.1512 random) — worse than random

## Interpretation
GC trend is NOT monotonic. eval_07/13 peak around 40% GC (matching human
genome average). eval_01 continues climbing as GC drops. eval_04/08 actively
prefer random/balanced composition.

So eval_04/08 might be the "diversity" or "natural variance" evals — they reward
sequences that are NOT compositionally biased. They could be the canaries for
overfitting to GC alone.

Going forward: composition tweaks are saturating. Next big lever is motif content.
