# 004_gc_biased

## Setup
50K different random sequences, each char iid with P(0)=P(3)=0.15, P(1)=P(2)=0.35.

## Results (all dropped relative to uniform random)
- eval_01: -0.107 (random was 0.504, drop 0.61)
- eval_07: -0.437 (random was 0.546, drop 0.98 — most sensitive)
- eval_13: -0.401 (random was 0.529, drop 0.93)
- eval_04/09: 0.228 (random was 0.451, drop 0.22 — least sensitive)
- eval_08: 0.081 (random was 0.154, drop 0.07 — barely)

## Insights
1. **Scores can be negative**: raw Pearson r, not (r+1)/2 mapping.
2. **Uniform random was NOT a chance baseline** — r=0.5 is a real correlation.
3. **Composition strongly affects score** in most evals.
4. **GC-bias HURT every eval** — none improved.
5. eval_04/09 are barely composition-sensitive; eval_07/13 are most sensitive.
6. Pattern: condition_a < condition_b < condition_c often inverts when scores
   become negative. The condition relationships flipped sign.

## Implications for theory
- Strongly suggests there's a fixed per-row target activity for each row.
- Uniform random ⟹ uniform predicted-activity distribution that has moderate
  correlation with targets. Biasing concentrates activities → less variance →
  lower r.
- OR: target distribution is itself "uniform-like" and bias deviates from it.

## Next direction
Test AT-bias (opposite). If also bad → composition uniformity is paramount.
If good → there's a directional preference we can exploit.
