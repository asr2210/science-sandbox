# 018 CpG bisect: T[C→G]=0.70 at GC=0.55

50k Markov. CpG dinucleotide rate=0.192.

## Result
- mean_r = 0.864 (eval_01 = 0.881)
- Between 015 (0.868, T[C→G]=0.65) and 016 (0.857, T[C→G]=0.80)

## CpG curve confirmed
| T[C→G] | CpG rate | mean_r | eval_01 |
|--------|----------|--------|---------|
| 0.275 (iid, exp 012) | 0.076 | 0.857 | 0.868 |
| 0.50 (exp 014, GC=0.49) | 0.117 | 0.858 | 0.872 |
| 0.65 (exp 015) | 0.179 | 0.868 | 0.884 |
| 0.70 (this) | 0.192 | 0.864 | 0.881 |
| 0.80 (exp 016) | 0.219 | 0.857 | 0.876 |

Smooth quadratic-like peak at T[C→G] ≈ 0.65 (CpG rate ≈ 0.18).

## Takeaway
Peak confirmed. Stop sweeping T[C→G]. 015 remains best.

## Next
Explore a different lever. Options:
- 2nd-order Markov chain with trinucleotide enrichment (carefully designed
  to preserve local uniformity)
- Joint optimization: CpG=0.65 + slightly different GC (e.g., GC=0.58)
- Test CpG=0.65 with a noise seed (verify robustness)
