# Exp 005: Random uniform reversed (order test)

## What
Same sequences as exp 001 (seed=0), but order in file reversed.

## Result
Identical to exp 001 across ALL 14 evals (down to the 4th decimal).

## Interpretation
**Score is invariant to sequence order.** Target is content-based, not index-based.

This rules out the hypothesis that target depends on position in our submitted file.
The scoring computes per-sequence prediction & per-sequence target both as deterministic
functions of sequence content, then Pearson r over the 50k pairs (order-invariant).

## Implications
- No benefit from sorting/ordering our submissions.
- Maximizing r requires designing sequences where prediction & target correlate strongly.
- Random uniform gives some baseline correlation; need to amplify shared signal.

## Time
~2 minutes.
