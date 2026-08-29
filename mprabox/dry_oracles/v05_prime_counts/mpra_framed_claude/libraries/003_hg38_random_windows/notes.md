# Exp 003 — Random hg38 genomic windows (chr8/19/22)

## Design
50K x 200bp sampled uniformly from chr8, chr19, chr22 (proportional to length),
forward strand only, N-free. Empirical GC = 0.433.

## Result
eval_01 = 0.0490, mean ≈ 0.045. Only marginal improvement over random uniform
(0.042 eval_01). eval_08 actually DROPPED to 0.049 from 0.124 in random uniform.

| metric | uniform_001 | dinuc_002 | hg38_003 |
|--------|-------------|-----------|----------|
| eval_01 | 0.042 | 0.009 | 0.049 |
| eval_07 | 0.025 | 0.007 | 0.032 |
| eval_08 | 0.124 | 0.066 | 0.049 |
| eval_13 | 0.020 | 0.002 | 0.034 |

eval_13 (the hardest, most sequence-specific eval) got a real lift (~70%).
eval_08 fell further.

## Interpretation
Real DNA is *barely* better than uniform random on average. This is a strong
result. The simplest reading: most random genomic windows are non-regulatory
(gene deserts, intergenic, repeats). They produce essentially flat activity
measurements, giving the model very little dynamic range to fit. The model
can't learn cis-grammar from a library where everything is silent.

The dynamic-range bottleneck appears to be the real constraint, not raw
realism of the input distribution.

eval_13 lift confirms that *some* sequence-specific signal exists in real
DNA that synthetic random doesn't capture — but only weakly.

## Next step
Sample from ENCODE candidate cis-regulatory elements (cCREs) — known active
regulatory regions. This should dramatically widen the activity distribution
and let the model learn useful features.

## Time
10s evaluator, ~40s wall. (Faster than earlier — eval caches loaded.)
