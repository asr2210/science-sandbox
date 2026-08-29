# 003 — Composition gradient (fraction of '1')

- 50 000 strings, string i has exactly round(200*i/49999) ones, rest zeros, shuffled.
- Result: all 14 evals near zero (condition_a ranges -0.011 to +0.004).
- No NaN, so prediction wasn't constant.
- Conclusion: scorer's feature isn't simple #1 content (or '1' content is
  uncorrelated with the hidden target).
