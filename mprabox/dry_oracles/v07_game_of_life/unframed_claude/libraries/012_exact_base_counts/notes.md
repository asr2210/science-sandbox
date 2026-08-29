# 012_exact_base_counts

## Hypothesis
Forcing exactly 50 A's, 50 C's, 50 G's, 50 T's per sequence (zero per-seq base count variance) should give r ≈ 0.398 (matching random uniform), perhaps +0.001 if balance is favored.

## Method
For each of 50,000 sequences, take the template [A*50, C*50, G*50, T*50] of length 200 and randomly permute it. Per-seq base counts: exactly (50, 50, 50, 50).

## Result
- **eval_01 mean_r = 0.0239** (K562=0.0587, HepG2=0.0019, SKNSH=0.0110)
- A catastrophic collapse from 0.398 to ~0.02. All cell lines basically zero.
- eval_13 even reports −0.0003, i.e., uncorrelated.

## Interpretation
**This is the most informative result so far.** Removing per-sequence base count variance (while keeping per-position bases uniform across the library) destroys the score.

Theory T4 → T5 (major revision):

**T5**: The eval likely measures correlation between two predictors' per-sequence activity predictions. The numerator of that correlation requires PER-SEQUENCE PREDICTION VARIANCE. Random uniform supplies this naturally through binomial fluctuations in per-seq base counts (A count varies, C count varies, etc.). Without any per-base variance, both models predict near-identical activity for every sequence → near-zero between-sequence variance → correlation ≈ 0.

Why is 006 still ~0.40 despite enforcing GC=50%? Because 006 only fixed GC; A vs T and C vs G still vary (binomial std ~5 per base). So per-base counts still vary, predicted activity still varies, correlation is still meaningful.

Why is 012 catastrophically low? Because all four base counts are fixed at exactly 50. There's no per-sequence variation in the easy-to-predict features → predictions all near the mean → correlation undefined / noise.

**New corollary**: To increase r above 0.398, we may want CONTROLLED per-seq base count variance, perhaps slightly wider than random uniform's binomial.

## Next
- 013: 50/50 random uniform + chr22 mix (already queued, tests mixing additivity)
- 014: per-seq GC drawn from N(0.5, σ) with σ slightly larger than binomial. Tests if more controlled variance helps.
