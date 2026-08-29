# 005 — Dirichlet composition per seq

Each sequence gets its own composition ~ Dirichlet(alpha=1) on the 3-simplex,
then iid sample length-200 from it.

## Result
- eval_01: mean_r = 0.3590 (vs 0.4200 baseline) — WORSE
- a = 0.4989, b = 0.5064, c = 0.0716

## Interpretation
- a, b still BELOW baseline. So MORE composition variance doesn't help a, b.
- c is HIGHER than baseline (0.072 vs 0.053). c rewards composition variance.

Combined with 001, 003, 004:
**c monotonically with composition variance:**
- 004 (zero var): c=0.018
- 001 (binomial): c=0.053
- 003 (4-cluster): c=0.062
- 005 (Dirichlet): c=0.072

**a, b peak near iid random (binomial-level variance):**
- 004 (zero): a=0.43, b=0.47
- 001 (binomial): a=0.59, b=0.62
- 003 (cluster): a=0.46, b=0.48
- 005 (Dirichlet): a=0.50, b=0.51

So a, b love iid-random-style sequences. c rewards more spread.

Since mean_r = (a+b+c)/3 and a,b dominate, focus on a, b.

## Next probe
Test k-mer structure: Markov order-1 with biased transitions but uniform
stationary distribution. Keeps composition uniform but adds dinucleotide bias.
