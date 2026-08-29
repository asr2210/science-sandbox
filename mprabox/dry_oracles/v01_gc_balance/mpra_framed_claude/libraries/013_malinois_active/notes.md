# 013_malinois_active

## Setup
50k Malinois oligos selected as TOP by max(|K562_log2FC|, |HepG2|, |SKNSH|).
Threshold ended up at |log2FC| ≥ 2.99 — only the strongest activator /
silencer sequences.

## Result — REGRESSION
- eval_01 = 0.4950 (cf. random Malinois 0.6856, cCREs 0.6921, **−0.19**)
- eval_07 = 0.5361 vs 0.7521 (catastrophic)
- eval_10 = 0.4001 vs 0.6594 (catastrophic)
- eval_04 = 0.5656 vs 0.5832 (basically OK because eval_04 was already
  the only "high signal" eval)

## Interpretation
Selecting only highly-active sequences is **harmful** — the training
distribution becomes wildly unrepresentative. The model never sees
median-activity sequences, so it learns to predict high values for
everything. When the eval set has the natural activity distribution
(mostly low / median), correlations collapse.

This is consistent with classic biased-sampling literature: when the
training distribution differs from the test distribution, calibration
goes off. Even a model that can rank-order well will get poor
correlation if it's been told "all good training examples are
high-activity" and never learns the gradient.

## Theory update → T5
- **Distribution-matching is more important than per-sample
  informativeness.** A library that subsamples the full activity
  distribution beats one that filters to "informative" cases.
- Random Malinois ≈ cCRE for eval_01 — they're roughly equivalent
  bases. cCRE may have a slight edge because each cCRE is
  pre-selected for regulatory features (better baseline signal).
- The cCRE ceiling at ~0.69 is real. Both selection-by-active (this
  experiment) and selection-by-canonical-regulator (cCREs) are
  near-equivalent. I cannot push beyond by *being more selective*.
- Maybe I can push by *diversifying* — combining sources to expose the
  model to motif arrangements that any one source lacks.

## Takeaway
Do NOT pre-filter training data on the label. Try combining unbiased
sources (cCRE + random Malinois + DHS) for breadth instead.
