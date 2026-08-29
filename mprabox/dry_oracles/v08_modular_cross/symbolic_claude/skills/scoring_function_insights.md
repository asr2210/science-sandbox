# Scoring function insights

## Confirmed
- `mean_r = (condition_a + condition_b + condition_c) / 3`
- Scoring uses `scipy.stats.pearsonr` → uses Pearson correlation.
- Correlation is across the 50k sequences in the submission.
- Constant per-condition output → NaN.
- 9 unique evals out of 14 (01==14, 02==05, 03==12, 04==09, 06==11).
- Random uniform sequences → mean_r ≈ 0 for all evals.
- **ORDER DOES NOT MATTER** (exp 003 vs 004 identical). Multiset only.
- Hidden target is a function of sequence content: `r = pearsonr(M(seq_i), f(seq_i))`.

## CRITICAL: NOISE FLOOR (exp 020, 2026-06-03)
- Same generative method (Dirichlet 0.5), different seed → eval_01 swung from
  +0.0030 (seed 11) to -0.0024 (seed 997). Swing ~0.005.
- Pearson SE for N=50k: 1/sqrt(50k) ≈ 0.0045 — matches observed noise.
- **All my method-level differences are within noise floor.**
- Methods are essentially indistinguishable for eval_01 within ±0.005 band.

## Implication for strategy
- Don't chase 0.001-0.003 improvements; they're noise.
- Either find a method that moves the needle by 0.01+ (genuinely correlates with
  the hidden target), or pick a stable safe-bet library.
- Best single-seed observation (+0.003) is a lucky draw.

## Per-condition tendencies (eval_01, qualitative across exps)
- condition_a: structured / repetitive content (block dirichlet boosted a)
- condition_b: high-entropy / random content
- condition_c: compositional diversity / motif presence
- These pull in opposite directions; net effect on mean_r ≈ noise.

## Strategy
- Pivot from exploration to safe final submission.
- Pure random uniform is simplest, reproducible, and within noise of zero.
- Dirichlet(0.5) gives same expected score with more variance.

## Hypothesis about computation
The scorer likely:
1. Runs a pretrained model M on each of our 50k sequences
2. Gets per-sequence prediction (3 outputs, conditions a/b/c)
3. Computes Pearson r between predictions and a hidden target vector f(seq)
4. Returns r for each condition + mean
