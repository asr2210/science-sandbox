# 027 — 013 cCRE with DHS-quality filter

## Design
013 class composition (10K rare + 2.5K abundant), but only sample
cCREs that overlap a DHS with mean_signal >= q75 (across all DHSs)
AND numsamples >= 5. Same DHS filter that gave 009 a +0.020 lift.

Filter outcomes (all seeds):
- PLS, CA-CTCF, pELS, dELS, CA: filter applied (sufficient pool)
- CA-TF: filtered pool 6,108 < target 10,000 → fallback unfiltered
- CA-H3K4me3: filtered pool 9,696 < target 10,000 → fallback unfiltered
- TF: filtered pool 195 < target 2,500 → fallback unfiltered (TF
  cCREs almost never overlap broad-active DHSs — only 0.2%!)

So 5/8 classes get the filter; 3/8 are unfiltered. This itself is
informative: TF-binding-only and CA+TF cCREs are often in regions
without strong cross-cell-type accessibility.

## Results (mean over 3 seeds)
- eval_01 = **0.7432** (vs 013 0.7477 = **-0.005**)
- mean across 14 evals = **0.7859** (vs 013 0.7900 = **-0.004**)
- eval_08 = 0.7048 (vs 013 0.7044 = +0.0004 — tied)

## Per-eval delta vs 013
01:-0.005 02:-0.005 03:-0.005 04:-0.003 05:-0.005 06:-0.004 07:-0.007
08:+0.000 09:-0.002 10:-0.002 11:-0.004 12:-0.004 13:-0.007 14:-0.004

Tight spread, all within +-0.007 of 013. The DHS quality filter
neither helps nor meaningfully hurts.

## Per-seed eval_01
seed 0 (spark01): 0.7523
seed 1 (local):   0.7150
seed 2 (spark04): 0.7623
SD ≈ 0.025.

## Branching outcome
- 027 > 013 → DHS adds info (no)
- 027 ≈ 013 within 0.003 → cCRE class label captures activity (NO,
  technically -0.004 outside that band)
- 027 < 013 → filter too restrictive (yes, very mildly)

Result is on the boundary — basically tied, slight underperformance
likely from reduced effective per-class diversity in filtered classes.

## What this teaches
**T25 (new — cCRE class label and DHS signal-quality are largely
redundant info sources):** Filtering cCREs to those overlapping
high-quality DHSs doesn't add useful signal beyond what the cCRE
class assignment already captures. The model effectively cannot
distinguish "DHS-supported PLS" from "weaker PLS" given the
classifier head it learns.

**T26 (incidental — cCRE classes have very different DHS overlap
rates):** Pure-TF cCREs almost never (0.2%) overlap broad-active
DHSs. CA-TF and CA-H3K4me3 are at ~6-10%. PLS / CA-CTCF / pELS
are higher. This means the cCRE class label correlates strongly with
expected accessibility breadth — confirming the redundancy in T25.

## Best library so far
**013 cCRE extreme upweight, mean = 0.7900**. Holds.
**022 (mean 0.7873, eval_08 0.7529)** alt-best for eval_08-priority.

## Most informative next experiment (028)
Untried angle: cCRE width-quartile-stratified sampling within each
class. Right now 013 samples uniformly from each class's pool, so
the per-class width distribution is whatever ENCODE produced.
Width-stratified means: within each class, divide cCREs into 4
width quartiles, sample n_take/4 from each. Forces width breadth.

**Hypothesis:** cCRE width carries information orthogonal to class
(narrow vs broad regulatory regions may have different functional
signatures). Stratifying across widths within each class teaches
the model both regimes.

Counter-evidence from 020: filtering to >=200bp-wide cCREs lost 0.058.
T19 attributed this to selection bias. But T19 said the LOSS came
from removing the broader/sharper distinction; sampling ALL widths
(including the narrow ones 020 excluded) should be different from
filtering to wide-only.
