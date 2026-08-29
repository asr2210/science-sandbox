# 022 comp_random_walk

Per-sequence random walk in composition space.

## Result: HUGE DROP
- eval_01: 0.1632 (back to near-random-uniform!)
- All conditions reverted close to uniform-random levels

## Why it failed
With eps=0.05 random walk + 200 steps, the per-sequence AVERAGE composition
converges (LLN) to the perturbation distribution mean = (0.25, 0.25, 0.25, 0.25).
So between-sequence composition variance disappears — same as random uniform.

## Key insight
BETWEEN-SEQUENCE composition variance is the dominant signal driver, not just
within-sequence variance. Our gradient works because its endpoints from
Dirichlet(0.5) give per-sequence average compositions that vary widely between
sequences.
