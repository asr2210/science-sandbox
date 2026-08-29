# Experiment 001 — Uniform random baseline

## Setup
- 50,000 uniform random strings of length 200 over {0,1,2,3}.
- Seed 42.

## Results
- eval_01 mean_r = 0.1183, a=0.0090, b=0.1564, c=0.1896.
- Other eval sets cluster (some are identical).
- eval_08 is the strictest: mean_r=0.0563, ~half of others.

## Key observations
- **mean_r == mean(a,b,c)** exactly. So mean_r is the average of three sub-conditions.
- Some eval sets are duplicates (eval_01==02==05==14; 03==12; 06==11; 04==09).
- 8 distinct eval scoring functions across 14 sets.
- condition_a is the *hardest* condition (lowest scores on random) — biggest headroom.
- condition_b is intermediate.
- condition_c is easiest on random.
- All conditions are clearly non-trivial (random gets >0 but well below 1).

## Implications
- Need to find structure that boosts a, b, c — especially a.
- Random is ~0.12 → there's huge headroom toward 1.0.
- Conditions are correlated across eval sets (suggests they probe similar properties).
