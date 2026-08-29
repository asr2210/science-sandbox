# 013_mix_random_chr22

## Hypothesis
50/50 mixture of random uniform (001 → 0.3981) and chr22 tiles (002 → 0.3928). If r is roughly the average of the components, expect ~0.3955. If random uniform dominates, ~0.397. If the bio half drags more, ~0.392.

## Method
25,000 random uniform 200bp + 25,000 chr22 random 200bp tiles (no Ns), concatenated and shuffled with seed 42.

## Result
- **eval_01 mean_r = 0.3889** (K562=0.5997, HepG2=0.4226, SKNSH=0.1444)
- Slightly *below* the naive average (0.3955). The mixed library underperforms both pure components by a small but real margin.

## Interpretation
Mixing is sub-additive. Possible reasons:
1. The per-sequence stats of the mixed library now span two modes (random uniform GC ~50% binomial vs chr22 GC ~41% with larger variance), increasing per-seq stats variance more than either pure library, which T3 says costs r.
2. The eval may also penalize libraries whose per-sequence GC distribution is bimodal even mildly — consistent with the 004 bimodal-GC collapse.

This is consistent with T4/T5: any departure from a smooth, tight per-sequence stats distribution hurts. Mixing two pure distributions creates a bimodal-ish per-seq stats distribution and loses ~0.005.

## Next
- 014: per-seq GC N(0.5, 0.075). Tests whether widening per-seq GC slightly (~2× binomial std) hurts OR helps. T5 predicts MORE variance might help if there's room above 0.398; T3 predicts it hurts smoothly.
