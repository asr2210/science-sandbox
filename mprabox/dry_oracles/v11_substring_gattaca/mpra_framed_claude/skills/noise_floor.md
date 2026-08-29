# Noise floor of prepare.py mean_r

Measured between random-uniform seed=0 (exp 001) and seed=1 (exp 008):
- mean_r: 0.8516 vs 0.8494 → Δ = 0.0022
- eval_01: 0.8620 vs 0.8587 → Δ = 0.0033
- eval_08 (hardest): 0.7755 vs 0.7721 → Δ = 0.0034
- eval_13: 0.8313 vs 0.8236 → Δ = 0.0077

**Rule of thumb:** Differences below ~0.005 on mean_r or eval_01 are within
seed noise and should not be over-interpreted. Differences above ~0.01 are
real signal.

For high-stakes claims, consider running ≥2 seeds and reporting average + range.

## Useful corollary
The HARDER evals (07, 08, 10, 13) have slightly higher per-eval noise. The
PAIRED evals (01/14, 02/05, etc.) are tighter. When comparing libraries that
shift things by 0.01–0.02, look at the agreement across multiple evals, not
just eval_01.
