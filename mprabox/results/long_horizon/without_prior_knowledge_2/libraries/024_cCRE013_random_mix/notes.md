# 024 — 013 cCRE 80% + 20% uniform random hg38 mix

## Design
50K library:
- 40K cCRE (013 recipe scaled 80%): 8K each rare + 2K each abundant
- 10K uniform random hg38 main-chrom 200bp windows >=10kb from any cCRE

Library shuffled together. Random source = same scaffold pool used
for 022/023 chimeric flanks.

## Results (mean over 3 seeds)
- eval_01 = **0.6894** (vs 013 0.7477 = **-0.058**)
- mean across 14 evals = **0.7235** (vs 013 0.7900 = **-0.067**)
- eval_08 = **0.6198** (vs 013 0.7044 = **-0.085**, vs 023 0.7649 = **-0.145**!)

## Per-eval delta vs 013
01:-0.058 02:-0.064 03:-0.069 04:-0.051 05:-0.058 06:-0.064 07:-0.086
08:**-0.085** 09:-0.060 10:-0.074 11:-0.057 12:-0.060 13:-0.080 14:-0.064

**Every eval lost. eval_08 LOST 0.085** — the OPPOSITE of what
T21 predicted. Standalone random sequences hurt eval_08 more than
they helped.

## Per-seed eval_01
seed 0 (spark01): 0.6885
seed 1 (local):   0.6897
seed 2 (spark03): 0.6900
SD ≈ 0.0008 — extraordinarily tight (vs 0.018 for 013/022).

## What this overturns
**T21 (REVISED — chimeric flanks ≠ standalone random):** The eval_08
boost in 022 (0.7529) and 023 (0.7649) does NOT come from "random
sequence in the library". Standalone random sequences (024) are
catastrophic for eval_08 (0.6198, even worse than 005's 0.7016 of
pure random). The chimeric design (cCRE peak embedded in random
flank) is what helps eval_08 — the model needs to see "regulatory
signal embedded in inactive context" for that benchmark, not
"random sequence" per se.

**T22 (new — mixing label-divergent sources hurts more than either
pure source):** 100% cCRE mean = 0.7900, 100% random = 0.7016.
Linear interpolation predicts 80/20 mix at 0.7723. Actual: 0.7235
(-0.049 below interpolation). The model can't reconcile two sources
with very different activity-label distributions; it underfits both.

**T20 / T17 still hold:** 023's regulatory-unit gradient and 022's
"flank is scaffold" findings are unaffected. The chimeric design
preserves coherent cCRE-anchored sequences; this matters.

## Process note
Per-seed eval_01 nearly identical (0.6885-0.6900, SD ≈ 0.0008).
Time was 1145s vs 1969s for 023 — possibly the regression problem
is simpler when the training set has bimodal high/low activity (the
model converges fast to a near-trivial solution). This near-zero
seed-variance is a tell of underfitting/over-regularization, not
signal of a great library.

## Best library so far
**013 cCRE extreme upweight, mean = 0.7900**. Holds.
**022 (mean 0.7873, eval_08 0.7529)** is the most interesting
"alternative best" — slightly lower mean but much better on the
hardest eval. Decision depends on whether we weight all evals
equally (013 wins) or weight worst-case evals (022 wins).

## Most informative next experiment (025)
We've now exhaustively probed:
- Class composition (012/013/014/015/016) → 013 wins
- Mixing with DHS atlas (019) → loses
- Width filter (020) → loses (selection bias)
- Off-center extraction (021) → loses
- Random-flank chimera (022) → ties + eval_08 boost
- Smaller cognate region (023) → small gradient loss
- Standalone random mix (024) → catastrophic loss

Untested axes that could move the needle:
1. **Reverse-complement augmentation** of 013 — standard ML practice.
   For each cCRE, half forward / half reverse-complement. Should
   teach the model strand-invariant motifs explicitly.
2. **Dual library (013 + chimeric 022)** — keep 013 bulk but add
   some chimeric sequences for the eval_08 boost.
3. **Signal-quality filtering** — DHS Index intersection to enrich
   for active cCREs.

Pick **025 = 013 with RC augmentation**. Cleanest test, low-risk,
likely free win. If +0.005 or more on mean, new best; if neutral,
RC isn't useful (model already strand-invariant via prepare.py
training) and 026 can pivot to dual-library.
