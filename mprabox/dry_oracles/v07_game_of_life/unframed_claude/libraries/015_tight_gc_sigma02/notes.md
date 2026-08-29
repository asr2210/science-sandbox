# 015_tight_gc_sigma02

## Hypothesis
Per-seq GC count drawn from N(100, 2.0), giving per-seq GC std ≈ 0.010 (3.5× tighter than random uniform's binomial std 0.035). Inside each seq: GC positions randomly G or C (50/50), AT positions randomly A or T (50/50).

If T6 plateau extends below binomial: r ≈ 0.398.
If smooth decline from 012's collapse: r ≈ 0.30.

## Result
- **eval_01 mean_r = 0.3975** (K562=0.6181, HepG2=0.4341, SKNSH=0.1401)
- **Statistically tied with random uniform 0.3981** (within 0.001 noise).

## Interpretation
Per-seq GC std of 0.010 is fine. The plateau extends across ALL of [0.010, 0.082] for GC variance.

**Important nuance**: 015 only constrained the GC TOTAL (sum of G+C positions). Within those positions, G vs C is still binomial; within AT positions, A vs T is still binomial. So per-base count std (per-seq A count, T count, G count, C count) is similar to random uniform (~5 each, vs binomial std=6.12).

So 015 does NOT cleanly test the per-base variance lever. 012 killed ALL per-base variance (each base exactly 50). 015 only constrained the GC total.

**Next**: 016 directly tests per-base variance by drawing each per-seq base count from N(50, σ) with σ_target ~ 1.3 (between 012's 0 and 001's 6.12). This will tell us whether the cliff is at "any per-base variance" or only at "exactly zero per-base variance".

## Updated variance curve

| exp | constraint | per-seq GC std | per-seq A count std | eval_01 |
|---|---|---|---|---|
| 012 | a=c=g=t=50 each | 0 | 0 | 0.024 |
| 015 | GC=100±2 each | 0.010 | ~5 (binomial) | 0.398 |
| 001 | unconstrained | 0.035 (binomial) | 6.12 (binomial) | 0.398 |
| 014 | GC=N(0.5,0.075) | 0.082 | ~7 (slightly inflated) | 0.399 |
| 005 | GC=U(0.1,0.9) | 0.23 | ~12 | 0.365 |
| 004 | bimodal 20/80 | 0.30 | ~22 | 0.340 |

So with respect to GC variance, plateau spans roughly [0.010, 0.082].
The 012 catastrophe was due to per-BASE variance being zero, not per-seq GC variance being zero.
