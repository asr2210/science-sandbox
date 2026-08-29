# 003_ccre_random_mix

## Setup
25,000 ENCODE cCREs (same stratified mix as 002, halved quotas, seed=3) +
25,000 uniform random 200bp sequences. Shuffled before writing.

## Result
- eval_01: 0.6921 → **0.5711** (−0.12, big drop)
- eval_07: 0.7562 → 0.6485 (−0.11)
- eval_13: 0.7466 → 0.6254 (−0.12)
- eval_04/09: 0.5977 → 0.4517 (−0.15)
- eval_08: 0.1248 → 0.1296 (essentially unchanged)
- Mean across 14 evals: ~0.53 (was 0.62)

## What this tells us
Hypothesis disconfirmed: mixing random does NOT help eval_08, and it
dramatically hurts every other eval. The model is not effortlessly learning
both distributions; the random sequences seem to dilute the cCRE signal
without contributing anything useful.

Two takeaways:
1. eval_08's anomaly is not about "missing random composition." It's
   something more specific (designed motifs? extreme features? negative
   controls?). Mixing random isn't the lever.
2. **Sample efficiency matters**: halving the cCRE count hurt all other
   evals roughly proportionally (~0.12 drop). The model is hungry for
   real cCRE data — more is better.

## Theory update
- T3 starts to form: real cCRE training data has high "signal per sequence"
  for the bulk of evals. Adding off-distribution data (random) is pure
  dilution.
- The right way to fix eval_08, if any, is to add training data from a
  distribution that *matches eval_08*, not just any distribution.

## Next direction
Stop trying to fix eval_08 by mixing. Instead:
1. Maximize eval_01 with the best possible cCRE-driven library.
2. Test synthetic motif libraries (JASPAR-planted random) as a separate
   theoretical probe — they isolate "motifs alone" from context.
