# 008_gradient_strong

## Setup
Deterministic per-row counts. Row i has counts:
- AT chars (0 and 3): round(5 + 90 * i/49999) each
- GC chars (1 and 2): 100 - count_AT each
Within row: random permutation. Sum = 200.
Row 0: counts (5, 95, 95, 5). Row 49999: counts (95, 5, 5, 95).

## Results vs 007
- eval_01: 0.5949 (007 was 0.5725, +0.022)
- eval_07: 0.6621 (007: 0.6351, +0.027)
- eval_13: 0.6318 (007: 0.6072)
- eval_04/09: 0.5002 (007: 0.4588, +0.041)
- eval_08: 0.1229 (slight drop from 007 0.134)

## Insights
- Stronger composition gradient → continued improvement on most evals
- eval_04/09 saw the BIGGEST relative gain (+0.041) — they benefit from
  the extreme variance more than from any particular composition
- eval_08 is stuck regardless (different mechanism)
- All conditions defined; no NaN despite min count = 5

## Diminishing returns analysis
- 007 to 008: gradient delta increased from 0.30 to 0.45 (factor 1.5x);
  eval_01 increased by 0.022 (factor ~3% relative)
- Marginal value of pushing harder is shrinking
- Probably another 0.01-0.02 left in pure composition gradient
