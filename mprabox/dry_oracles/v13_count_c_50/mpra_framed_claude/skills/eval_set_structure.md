# Skill: Eval set structure (what we know about the 14 evals)

## Source
Observed from experiment 001 (uniform random library). See
`libraries/001_uniform_random/result.json`.

## Duplicates / equivalences observed
On the uniform-random library, these evals return identical or near-identical
per-cell correlations:

| Group | Members |
|-------|---------|
| A     | eval_01, eval_14 |
| B     | eval_02, eval_05 |
| C     | eval_03, eval_12 |
| D     | eval_06, eval_11 |
| E     | eval_04, eval_09 |
| F     | eval_07, eval_13 |
| —     | eval_08 (unique) |
| —     | eval_10 (unique) |

So effective number of independent evaluations is ~8. **eval_01 is the
primary reported metric.**

(Verify on each subsequent library — equivalence may be model/library
dependent, not a fundamental eval-set property. But if it holds, expect
group F to be hardest to optimize because of opposite gradient.)

## Per-eval character (from random baseline)
- **eval_08**: dominated by composition. Random sequences reach r=0.58.
  HepG2 0.76, SKNSH 0.80 — but K562 only 0.18. Hypothesis: a set with
  strong GC/composition-driven target, mostly read by HepG2 and SKNSH.
- **eval_04 / eval_09**: r=0.39 from random. Balanced across cells.
  Either compositional or partially compositional.
- **eval_01 / eval_14** (primary): r=0.13. K562 carries (0.24), HepG2 ~0.
  Likely TF-grammar driven.
- **eval_07 / eval_13**: r=-0.14. K562 positive (0.23), but HepG2/SKNSH
  strongly negative (-0.33). A composition-based prediction *anti-correlates*
  with the HepG2/SKNSH targets in these sets. Active regions are
  compositionally distinct from random.
- **eval_02 / eval_05, eval_06 / eval_11, eval_03 / eval_12, eval_10**:
  modest positive 0.07–0.13 from random.

## K562 baseline
K562 correlation is consistently 0.18–0.33 across *all* evals from random
library. Two interpretations:
1. K562 readouts are relatively simple to predict (largely compositional).
2. The K562 model branch always finds *some* compositional signal.

## Implications for library design
- A library that improves only the compositional axis will saturate eval_08
  but barely move eval_01.
- A library focused on TF motifs / grammar should especially help eval_01,
  eval_07/13, eval_02/05.
- Watch for libraries that *push eval_08 down* — losing the compositional
  signal there hurts the mean.
- The K562 head responds even to weak input — be careful interpreting K562
  improvements as evidence of grammar learning.
