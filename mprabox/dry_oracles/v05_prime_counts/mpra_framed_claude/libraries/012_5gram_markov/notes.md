# Exp 012 — 5-gram Markov chain matched to hg38

## Bug + fix
Initial run had a bug in `prev_pref` recovery from modular arithmetic
(only the 3-mer suffix was retained as the prefix). Fixed by rolling
`pref` forward AFTER counting the transition. Re-ran with fix:
GC=0.402, CpG=0.0092 (matches chr8 globally — fix verified).

## Result (after fix)
**eval_01 = -0.0261. All evals NEGATIVE.** Worst result of any experiment
so far.

| eval | mean_r |
|------|--------|
| 01 | -0.0261 |
| 07 | -0.0154 |
| 08 | -0.0541 |
| 13 | -0.0099 |

## Interpretation
A 5-gram Markov library that matches hg38 local statistics EXACTLY produces
a model that systematically *anti-predicts* activity on real-DNA evals.

This is the dinuc-002 result (which had partial negative HepG2) amplified
into universal anti-correlation. The pattern:

- **Random uniform** (no info): model latches onto noise but it's roughly
  neutral → eval_01 ≈ 0.04.
- **Real DNA** (info correlates with activity): model learns
  weakly-positive features → eval_01 ≈ 0.05.
- **Local-statistics-matched synthetic** (info matches composition but
  NOT activity): model learns features that ANTI-correlate with truth
  on real DNA → eval_01 ≈ -0.03.

**Strong theory update.** What makes real DNA work is NOT its composition.
A library that mimics composition but lacks the activity-correlated
features actively hurts. The model can learn "GC + CpG + k-mer stats →
some output", but if that mapping is wrong (because synthetic), the output
is anti-predictive.

## Implication
- The model **does** learn from local k-mer/composition features.
- Whether those features generalize depends on whether they're paired
  with the *right* labels (which only happens for real DNA).
- Synthetic libraries with matched stats but uncorrelated activity =
  worse than uniform random because they teach the WRONG mapping.

## Next step
Stick with real DNA. Test if slight regulatory enrichment of a mostly-
random hg38 library lifts performance (40K random + 10K cCREs).

## Time
14s evaluator, 46s wall.
