# 026 — 013 + 022 chimeric dual library

## Design
50K total:
- 25K full 200bp cCRE windows centered on midpoint (013 design,
  classes scaled to 5K each rare + 1.25K each abundant)
- 25K chimeric: 50bp random hg38 flank + 100bp cognate cCRE
  centered on midpoint + 50bp random hg38 flank (022 design,
  same per-class counts)

Both halves draw cCREs independently from per-class pool. Random
flanks from hg38 main-chrom positions >=10kb from any cCRE.
Library shuffled.

## Results (mean over 3 seeds)
- eval_01 = **0.7297** (vs 013 0.7477 = **-0.018**, vs 022 0.7447 = -0.015)
- mean across 14 evals = **0.7716** (vs 013 0.7900 = **-0.018**, vs 022 0.7873 = -0.016)
- eval_08 = **0.7087** (vs 013 0.7044 = +0.004, vs 022 0.7529 = -0.044)

## Per-eval delta vs 013
01:-0.018 02:-0.019 03:-0.020 04:-0.014 05:-0.018 06:-0.019 07:-0.032
08:**+0.004** 09:-0.018 10:-0.020 11:-0.017 12:-0.019 13:-0.029 14:-0.019

Almost all evals lost ~0.018-0.020. eval_08 essentially tied with
013, **NOT** the +0.049 boost 022 had. The chimeric eval_08 boost
got diluted to nothing by mixing with cCRE-only sequences.

## Per-seed eval_01
seed 0 (spark01): 0.7467
seed 1 (local):   0.7632
seed 2 (local):   0.6793
SD ≈ 0.044 — much wider than 013 (0.012-0.017). High variance
indicates training instability — another tell of an inferior library.

## Branching outcome
Pre-experiment branches:
- 026 > 013 AND eval_08 > 0.73 → genuine bridge (no)
- 026 ≈ 022 → chimeric character dominates (no — eval_08 only +0.004)
- 026 < 013 by 0.005+ → cCRE-anchored mixing also hurts (**YES**)

## What this teaches
**T24 (new — chimeric eval_08 boost requires whole-library design):**
022's eval_08 boost (+0.049) and 023's (+0.061) are NOT additive in
proportion. Halving the chimeric fraction doesn't yield half the
boost — it yields ~0% (here, eval_08 = +0.004). The model needs
consistent training signal across the whole library to learn the
"regulatory peak in random context" pattern. Diluting it with
"regulatory peak in cognate context" breaks the regularity.

**T22 generalized:** Mixing two designs hurts EVEN when both are
cCRE-anchored (similar label distributions). Earlier T22 thought it
was about label divergence (cCRE vs random); 026 shows it's also
about design consistency. The model trains best on a homogeneous
library design.

**Decision-relevant updates:**
- Mix-strategies are off the table (024 + 026 both lose).
- 022 stays as the alternative best for eval_08-priority contexts.
- 013 stays as the universal best on mean-across-evals.

## Process note
spark03 also broke during 026 — exit 255 during ssh, only known-hosts
warning shown. Re-ran seed 2 locally. Now both spark03 and spark06
unreliable; only spark01 + local viable.

## Best library so far
**013 cCRE extreme upweight, mean = 0.7900**. Holds.

## Most informative next experiment (027)
Untried angle: cCRE quality/signal filtering using the DHS Index
(Meuleman 2020). The DHS Index has 3.6M hg38 DHS calls with
mean_signal and numsamples columns. Filter cCREs to those that
overlap a high-quality DHS (mean_signal >= q75 AND numsamples >= 5
— same filter as 009's DHS_filtered library that scored 0.7500).
This enriches for cCREs that are actually accessible/active across
multiple cell types — likely real, robust regulatory elements.

Use 013 class composition (10K rare + 2.5K abundant). If the rare
classes lose pool size after filtering (some rare classes have only
10K-50K cCREs total — filtering may leave too few), fall back to
unfiltered for that class.

Branches:
- 027 > 013 → DHS-quality filter on cCREs is informative; new best
- 027 ≈ 013 → cCRE class assignment already captures activity;
  DHS doesn't add info
- 027 < 013 → filter is too restrictive (narrows the pool too
  much, loses class breadth)
