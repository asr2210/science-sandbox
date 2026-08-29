# 004_varied_composition

50,000 distinct random strings, each with its own single-character bias (p0 ~ Uniform[0,1]).

## Result
- eval_01 mean_r = **0.1075** (worse than 001's 0.1159)
- condition_a/b still ≈ 0 across all evals
- condition_c about same as 001 (0.32 vs 0.36)
- No NaNs (50k distinct strings is plenty for the harness)

## Interpretation
Varying single-character composition does NOT push the correlations up. The predictors
don't seem to care about bulk composition as a dominant axis. condition_a/b are still
0, meaning whatever signal they need is NOT composition.

## Theory update
The dominant axis the predictors agree on is **not bulk single-character composition**.
Candidates left:
- specific k-mer / motif structure
- position-dependent patterns
- repetitive / periodic structure
- biologically-relevant motif content
