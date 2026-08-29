# 015 — deterministic GC = exactly 0.5 (100 GC, 100 AT per seq)

## Design
Every sequence has exactly 100 G+C and 100 A+T (deterministic GC=0.500, std=0). Within those positions, G/C and A/T sampled uniformly.

## Result
- eval_01 mean_r = **0.5191** (vs random uniform binomial 0.5177)
- K562 r = 0.9939
- HepG2 r = 0.5650
- SK-N-SH r = -0.002

## Reading
Forcing GC=0.5 exactly is comparable to baseline. Within noise. So GC variance neither helps nor hurts much (compared to natural binomial variance of std=0.035).

The eval distribution is composition-tolerant within reasonable bounds.

## Implication
GC fine-tuning is dead end. Look at higher-order structure: motif cassettes, positional encoding, multi-motif designs.
