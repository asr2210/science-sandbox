# 016 — Shared H3K27ac peaks across K562 + HepG2 + SKNSH

## Method
Bin midpoints at 500bp per chrom; take intersection of (chrom, bin) across
all 3 cells. 5,728 shared bins. Expand to 25k via ±60bp midpoint jitter.
Null = dinuc-shuffled.

## Results (eval_01)
mean_r = -0.0020 (K562=-0.0001, HepG2=-0.0052, SKNSH=-0.0007)

## Lesson
- Broadly active enhancers HURT (eval_01 = -0.0020 < shuffled peaks).
- Constitutive enhancers likely saturate the models; predictions cluster
  around "high", losing dynamic range → low Pearson r.
- HepG2 on eval_01 went NEGATIVE despite 015 giving best HepG2.
- eval_13 K562=+0.0125 was strong; eval_08 mean=+0.0042.

## Implication
"Active" sequences need to be DIFFERENT FROM EACH OTHER (high variance in
predicted activity, not uniformly high). Shared-active enhancers compress
the distribution.

## Next (exp 017)
Push the saturated-motif strategy further. Increase motif count to 20+
per sequence and widen GC contrast (active GC=70, null GC=15). The bet:
the +0.0045 plateau came from exp 012 hitting a sweet spot on motif
density × GC contrast; pushing both further should extend it.
