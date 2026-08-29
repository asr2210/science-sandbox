# Exp 021 — positional gradient p (0.95 first half, 0.5 second half)

## Result
eval_01 = 0.1505 (vs 0.1550 uniform p=0.7).
condition_c = 0.3995 (slight drop).

## Interpretation
Positions are approximately uniformly weighted. Gradient doesn't help.
Slight drop suggests heterogeneous p is sub-optimal vs uniform sweet
spot at p=0.7.

## Next
Test within-sequence phase block: positions 0-99 use phase 0,
positions 100-199 use phase 0 again BUT with a 2-position SHIFT, i.e.,
template = (0,1,2,3, ..., 0,1,2,3, 2,3,0,1, 2,3,0,1, ...). Tests
whether eval picks up global phase or local phase.
