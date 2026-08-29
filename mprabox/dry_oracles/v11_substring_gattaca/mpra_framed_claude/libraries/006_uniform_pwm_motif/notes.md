# 006 uniform + PWM-sampled JASPAR motifs (λ=3)

Same setup as exp 004 except motifs are sampled per-position from each TF's PWM
(not the consensus). Avg 2.99 motifs/seq across 879 vertebrate motifs.

## Result
- mean_r = 0.842 (eval_01 = 0.855)
- Slightly better than consensus injection (exp 004: 0.836) by 0.006
- Still ~0.01 below pure random uniform (0.852)

## Takeaway
PWM representation > consensus, confirming that fixed-string repetition is
slightly worse than realistic motif variation. But motifs at this density still
don't break above pure random uniform. Either density is too low or the model
extracts motif signal weakly.

Next: try PWM-sampled motifs at high density (λ=10) to test the density axis.
