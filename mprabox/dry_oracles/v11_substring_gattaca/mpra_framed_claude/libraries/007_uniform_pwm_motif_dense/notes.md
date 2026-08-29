# 007 uniform + PWM-sampled JASPAR motifs (λ=10)

50k random uniform background with ~10 PWM-sampled motifs/seq injected at
non-overlapping random positions. Avg 9.82 motifs/seq, ~80–100bp motif content
per 200bp.

## Result
- mean_r = 0.819 (eval_01 = 0.837)
- WORSE than λ=3 (0.842) and pure uniform (0.852)
- Monotonic decline with motif density:
  | λ | mean_r |
  |---|--------|
  | 0 | 0.852 |
  | 3 | 0.842 |
  | 10 | 0.819 |

## Takeaway
Adding more motifs ALWAYS hurts in this regime. Motifs displace random k-mer
coverage faster than they add usable signal — confirms k-mer dominance of the
model. Random uniform is robustly at ceiling.

Next: check noise floor with a second random uniform seed.
