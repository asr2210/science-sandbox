# 028 — 013 cCRE with width-quartile stratification

## Design
013 class composition (10K rare + 2.5K abundant). Within each class,
divide cCREs into 4 width quartiles by (end - start), sample n/4 from
each quartile uniformly. Forces width-breadth within each class.

Note: cCRE class widths span ~150-1000+bp; quartile boundaries vary
per class. All classes have minimum cCRE width >=150bp; medians
240-320bp.

## Results (mean over 3 seeds)
- eval_01 = **0.7115** (vs 013 0.7477 = **-0.036**)
- mean across 14 evals = **0.7486** (vs 013 0.7900 = **-0.041**)
- eval_08 = 0.6477 (vs 013 0.7044 = -0.057)

## Per-eval delta vs 013
01:-0.036 02:-0.039 03:-0.042 04:-0.032 05:-0.036 06:-0.040 07:-0.054
08:-0.057 09:-0.035 10:-0.045 11:-0.036 12:-0.036 13:-0.053 14:-0.039

ALL evals lost ~0.035-0.057. Width-stratification clearly hurts.

## Per-seed eval_01
seed 0 (spark01): 0.6779
seed 1 (local):   0.7315
seed 2 (spark04): 0.7251
SD ≈ 0.029.

## Branching outcome
- 028 > 013 → width is informative (no)
- 028 ≈ 013 → no marginal info (no)
- 028 < 013 by 0.005+ → forcing width breadth hurts (**YES, -0.041**)

## What this teaches
**T27 (new — cCRE width carries information; narrow > broad
per-instance):** The natural per-class pool sampling (used by 013)
is biased toward whatever width regime is most common, but this
turns out to be approximately optimal. Forcing equal counts across
width quartiles (which lifts up broad cCREs at the expense of
narrow ones) HURTS. Per-instance, narrower cCREs are more
informative — they're sharper peaks with more concentrated
regulatory content. This is consistent with T19's earlier insight:
20's loss came from width-FILTERING away the narrow informative
cCREs.

**Combined T19 + T27:** Both extremes hurt — filtering away narrow
cCREs (020) AND forcing equal width breadth (028) both lose
~0.04-0.06 vs natural per-class pool sampling (013).

**T13 strengthened again:** cCRE midpoints carry concentrated
regulatory information; the more narrowly the cCRE was called, the
more concentrated and informative its midpoint window is. This
maps onto our T20 cognate-region gradient (50bp/100bp/200bp).

## Best library so far
**013 cCRE extreme upweight, mean = 0.7900**. Holds.
**022 (mean 0.7873, eval_08 0.7529)** alt-best for eval_08-priority.

## Most informative next experiment (029)
We've now ruled out:
- mixing strategies (024, 026)
- RC augmentation (025)
- DHS-quality filtering (027 — neutral)
- width-quartile stratification (028)
- width filtering (020)
- off-center extraction (021)
- smaller cognate regions (023)

The only remaining promising axis is the cognate-region gradient
upper end. We've measured: 200bp (013) -> 100bp (022) -> 50bp (023)
gives mean 0.7900 -> 0.7873 -> 0.7784. eval_08: 0.7044 -> 0.7529
-> 0.7649. Could a SMALL random-flank chimera capture some
eval_08 boost while preserving most of 013's mean?

**029 = 022-style chimeric with 160bp cognate cCRE + 20bp random
flank each side.** Tests whether a tiny random-flank scaffold
triggers the chimeric eval_08 effect (T24 said the boost is
"whole-library", not proportional — small flank may still trigger
it) while keeping mean close to 013.

Branches:
- 029 mean ~0.79 AND eval_08 > 0.73 → minimal-flank chimeric is the
  best of both worlds; new top library
- 029 mean ~0.79 AND eval_08 < 0.71 → 20bp flank is too small to
  trigger chimeric effect; gradient is smooth
- 029 mean < 0.78 → cognate fraction matters even at ~80%; 022
  remains the only chimeric configuration that preserves mean
