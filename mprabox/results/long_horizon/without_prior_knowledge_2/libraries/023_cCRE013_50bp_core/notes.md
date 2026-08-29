# 023 — cCRE 013 with 50bp cCRE core + 150bp random flank

## Design
Each 200bp sequence is built as:
  [75bp random hg38 main-chrom flank]
  [50bp cognate cCRE region centered on cCRE midpoint]
  [75bp random hg38 main-chrom flank]

Random flanks drawn from main-chrom positions >=10kb from any
cCRE (same scaffold source as 022). Class composition matches 013
(10K each rare + 2.5K each abundant = 50K). ALL cCREs eligible
(no width filter — clean test of T19).

## Results (mean over 3 seeds)
- eval_01 = **0.7351** (vs 022 0.7447 = **-0.010**, vs 013 0.7477 = **-0.013**)
- mean across 14 evals = **0.7784** (vs 022 0.7873 = **-0.009**, vs 013 0.7900 = **-0.012**)

## Per-eval delta vs 013
01:-0.013 02:-0.013 03:-0.013 04:-0.030 05:-0.013 06:-0.013 07:-0.027
08:**+0.061** 09:-0.036 10:-0.012 11:-0.012 12:-0.010 13:-0.019 14:-0.013

Pattern is tight: most evals lose 0.010-0.013, three lose 0.020-0.036
(04, 07, 09 — same evals 022 also stumbled), and **eval_08 gains
+0.061** (even more than 022's +0.049). Random flank really helps
eval_08; the gradient: 013 0.7044 -> 022 0.7529 -> 023 0.7649.

## Per-seed eval_01
seed 0 (spark01): 0.7463
seed 1 (local):   0.7222
seed 2 (spark03): 0.7369
SD ~ 0.012, smaller than 022's 0.018. Local seed slowest again.

## Branching outcome
Pre-experiment branches:
- 023 ≈ 013 → 50bp peak alone is enough (no — lost 0.012)
- 023 between 022 and 020 → ~100bp cCRE pinpointed (YES)
- 023 ≈ 020 → needs >100bp (no — still much better than 020's 0.7317)

Result: **gradient confirmed**. Cognate-region size matters in the
50-100bp range, but with diminishing returns.

| Cognate region | Random flank | mean across 14 |
|---|---|---|
| 200bp (013, all cognate) | 0bp | 0.7900 |
| 100bp (022) | 100bp | 0.7873 (-0.003) |
| 50bp (023)  | 150bp | 0.7784 (-0.012) |
| 0bp (020 widthfilt, no flank) | n/a | 0.7317 (-0.058) |

## What this updates in the theory

**T20 (new — regulatory unit gradient, not step):** The cCRE
"regulatory unit" is not a sharp boundary. Going from 100bp -> 50bp
loses ~0.009 mean; going from 50bp -> 0bp would lose another large
chunk (extrapolating the curve). Useful regulatory signal extends
at least to ~+/-50bp of the cCRE midpoint, with the most-concentrated
signal in the inner ~25-50bp.

**T17 (further refined):** Random flank really is scaffold for
the model's receptive field — the cCRE element shrinking by 50bp
and being padded by random sequence loses only 0.009. Most of the
"pure cCRE element" signal lives inside ~50bp of the midpoint.

**T19 (confirmed):** 023 used ALL cCREs (no width filter) and lost
only 0.012 vs 013, while 020 (>=200bp width filter, pure cCRE) lost
0.058. Width-filter selection bias accounts for most of 020's drop.
The narrow cCREs that 020 excluded are exactly the high-signal
sharp peaks the model needs.

**T21 (new — eval_08 is broader-coverage benchmark):** Random-flank
libraries (022, 023) consistently outperform cCRE-only libraries
(013) on eval_08 by +0.05 to +0.06, and the gain scales with the
amount of random sequence in the library (013 0.7044 < 022 0.7529 <
023 0.7649). eval_08 likely tests genome-wide / broad-context
sequences. Coverage diversity > peak-only signal for that one eval.
This means the optimal library mix depends on which eval set we
prioritize.

## Best library so far
**013 cCRE extreme upweight, mean = 0.7900**. Holds.
**022 (mean 0.7873) and 023 (mean 0.7784)** both close, with
eval_08 trading higher for them.

## Process note
scratch_multirun.py worked cleanly on second run too: spark01,
local, spark03 in parallel, no spark06 hangs. ~33 min total. Local
seed slowest (~33 min wall) but matches per-seed cluster runs.

## Most informative next experiment (024)
The cognate-size gradient (T20) and the eval_08 vs cCRE tradeoff
(T21) suggest two complementary directions:

1. **Push the gradient endpoint** — if 50bp -> 25bp drops sharply,
   we bracket the irreducible peak width. If 25bp ≈ 50bp, the
   regulatory unit is even tighter.
2. **Mix random + cCRE within a library** — if eval_08 likes random
   sequence, but cCRE upweighting wins on most others, blend them.
   013 + uniform random (e.g., 80/20 mix) might give us the eval_08
   gain without the peak losses.

Mix-libraries (option 2) is more decision-relevant for "what's the
best library" — the gradient (option 1) is for theory polish.
**Pick option 2.** 024 = 40K from 013 cCRE recipe + 10K uniform
random hg38 main-chrom 200bp windows (>=10kb from cCREs, same source
as 022/023's flank pool). If eval_08 jumps and others mostly hold,
this is a free-ish win.

Branches:
- 024 > 013 mean → mixing wins; tune the ratio later
- 024 ≈ 013 mean, eval_08 up → tradeoff; need to decide priority
- 024 < 013 across the board → diluting cCRE hurts more than coverage
  helps; abandon the mix idea
