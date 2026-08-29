# 005 — 3-Way Mix (Uniform + Genomic + cCRE)

**Hypothesis:** Adding random uniform to the genomic+cCRE mix lifts
eval_08 substantially without hurting other evals. Predicted eval_08
recovery to 0.20–0.35 while eval_01 stays 0.54–0.57.

**Design:** 16,668 random uniform + 16,666 random genomic + 16,666
cCRE-centered. Mixed and shuffled. Seed 0.

**Results vs exp 004 (best so far at mean=0.531):**
- eval_01: 0.5291 (down 0.040)
- eval_02/05: 0.5299 (down 0.040)
- eval_03/12: 0.5254 (down 0.043)
- eval_04/09: 0.4877 (down 0.034)
- eval_06/11: 0.5242 (down 0.043)
- eval_07: 0.5750 (down 0.055)
- eval_08: 0.2048 (UP 0.123) ← predicted recovery
- eval_10: 0.4765 (down 0.041)
- eval_13: 0.5535 (down 0.058)
- eval_14: 0.5291
- Mean: **0.500** (down from 0.531)

**Verdict:** Adding 1/3 uniform helped eval_08 (+0.12) but cost a
fairly uniform ~0.04–0.06 on every other eval. Net loss on mean.

K562 on eval_04/09 specifically: 0.45 (004) → 0.36 (005). The flat
50% GC of uniform sequences shifted the model's K562 GC prediction
away from natural. So uniform isn't strictly "extra information" — it
biases the GC distribution of the training set.

**Theory updates:**

- Theory v3 (c) is wrong as stated: distributional breadth doesn't
  monotonically help. 1/3 uniform is "too much non-natural." The 50/50
  natural mix (004) is closer to optimal — uniform actively *pollutes*
  the natural training distribution.
- For eval_08 specifically, ~0.20 with 1/3 uniform vs 0.58 with 100%
  uniform. The recovery curve is sublinear in uniform fraction. To get
  eval_08 to 0.30+ I'd need ≥50% uniform, which would crash mean_r.
- Concrete decision: **eval_08 is not worth chasing aggressively.**
  It costs too much on the other 13 evals to push eval_08 up.

**Refined theory v4:**

- Natural sequences (genomic + cCRE) are the primary training base.
- Mixing within "natural" (genomic + regulatory) is super-additive
  (exp 004).
- Mixing in non-natural distributions (uniform random) is
  super-subtractive — even small amounts pull other evals down.
- The right move now is to diversify *within* the natural distribution
  rather than reach out to non-natural.

**Next experiment:** Diversify the regulatory half. Currently cCRE is
the regulatory source — it has a K562 bias and dominates with distal
enhancers (72% of cCREs are dELS). For cell-type breadth, try:

- exp 006: Multi-cell-type DHS index (ENCODE DHS Index / Roadmap
  consolidated DHS peaks) for the regulatory half. Tests theory v3 (d).
