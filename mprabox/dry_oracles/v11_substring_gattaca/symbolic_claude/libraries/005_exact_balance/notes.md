# 005 exact_balance

Each sequence is a random permutation of exactly 50 each of {0,1,2,3}.

Result: eval_01 mean_r = **0.8185** (vs 0.8526 uniform).
- condition_a: 0.849 → 0.857 (slight UP)
- condition_b: 0.875 → 0.915 (UP ~0.04)
- condition_c: 0.834 → 0.684 (DOWN ~0.15)

Compositional balance helps condition_b but hurts condition_c, with net slight loss.
condition_c clearly rewards inter-sequence compositional variance.
condition_b rewards uniformity/balance.

So there's a tension between b and c. Net loss for eval_01.
Need to find another axis (k-mer structure? position?) that can boost one without
killing the other.
