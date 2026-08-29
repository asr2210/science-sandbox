# 015 — cCRE (30K) + iid (5K) + human (5K) + chicken (10K)

## Result — chicken 10K REGRESSES, cross-species cap is universal at 5K
| metric  | 015 | 010 | 014 | Δ vs 010 |
|---------|-----|-----|-----|----------|
| eval_01 | 0.7117 | **0.7599** | 0.7285 | −0.0482 |
| eval_02 | 0.8037 | **0.8550** | 0.8196 | −0.0513 |
| eval_03 | 0.7861 | **0.8413** | 0.8020 | −0.0552 |
| eval_04 | 0.7683 | **0.8140** | 0.7888 | −0.0457 |
| eval_05 | 0.7118 | **0.7599** | 0.7284 | −0.0481 |
| eval_06 | 0.8037 | **0.8550** | 0.8198 | −0.0513 |
| eval_07 | 0.7417 | **0.8044** | 0.7531 | −0.0627 |
| eval_08 | 0.6624 | **0.7515** | 0.7015 | −0.0891 |
| eval_09 | 0.8333 | **0.8872** | 0.8579 | −0.0539 |
| eval_10 | 0.7600 | **0.8233** | 0.7811 | −0.0633 |
| eval_11 | 0.6991 | **0.7464** | 0.7155 | −0.0473 |
| eval_12 | 0.6752 | **0.7244** | 0.6903 | −0.0492 |
| eval_13 | 0.7377 | **0.8016** | 0.7419 | −0.0639 |
| eval_14 | 0.8037 | **0.8551** | 0.8200 | −0.0514 |

Mean 14: **0.7499** vs 010=0.8056 (−0.0557) vs 014=0.7677 (−0.0178). Wall: 827 s.

## Per-seed eval_01
- seed 0: 0.7330
- seed 1: 0.7004
- seed 2: 0.7016

Spread 0.033, between 010's tight 0.010 and 014's wide 0.060.

## Pre-registered scorecard
- "015 > 010 by ≥ +0.005 (chicken stacks past 5K, NEW BEST)":
  **strongly falsified**.
- "015 ≈ 010 (chicken adds enough to offset cCRE loss)": falsified.
- "015 < 010 by 0.005-0.015 (chicken adds slowly past 5K)": falsified.
- "015 < 010 by > 0.015 (chicken caps at 5K, cross-species cap
  universal)": **confirmed**, magnitude (−0.056) consistent with both
  cCRE 35→30K loss AND chicken-stacking failure.

## Disentangling the −0.0557
From 014: cCRE 35→40K elasticity ≈ −0.031 mean. By symmetry assumption
(small move, locally linear), cCRE 35→30K elasticity ≈ −0.031 mean
(losing 5K from a peak hurts).

Therefore: chicken 5→10K contribution ≈ −0.0557 − (−0.031) = **−0.025
mean**. Chicken at 10K is ~0.025 worse than at 5K. Cross-species axis
not only saturates at 5K, going past 5K **actively hurts** — same
plateau-shape we saw for cCRE near 35K and mouse mass in 008.

## Cross-species axis NOW FULLY MAPPED
| condition | result |
|-----------|--------|
| 0K mouse (004 baseline) | mean 0.7989 |
| 2.5K mouse + 2.5K chicken (009) | 0.7762 (sub-cap, hurts) |
| 5K mouse alone (006) | 0.7908 (+0.008 vs no-cross) |
| 5K chicken alone (010) | 0.8056 (peak species at peak mass) |
| 5K zebrafish alone (011) | 0.7990 (hump-shape) |
| 5K mouse + 5K chicken (013) | 0.7985 (no stacking) |
| 10K mouse alone (008) | 0.7547 (over-cap, hurts) |
| 10K chicken alone (015) | 0.7499 (over-cap, hurts) |

The cross-species axis is a universal step function:
- < 5K: too sparse, value underwhelming
- = 5K: sweet spot, value depends on species (chicken peak)
- > 5K: actively hurts, regardless of species choice

## Theory state — best 4-axis library is 010, axes are saturated
> Best library so far: 010 (35K cCRE + 5K iid + 5K human + 5K chicken).
> All four axes are at their saturation points. To improve from here,
> need:
>   (a) a 5th axis at small mass (< 5K) that adds value despite being
>       below the per-axis saturation point, OR
>   (b) sub-axis structure within an existing axis (e.g., cCRE class
>       reweighting, or conservation-stratified human-gen), OR
>   (c) a different cross-species better than chicken at 5K (xenopus
>       at ~360 Mya is the most likely hump-peak candidate).

## What I learned (operational)
1. **Step-function axes have symmetric falloff at both ends.** cCRE,
   mouse, chicken all show this. The "best mass" is a thin plateau
   that hurts on both sides. Future axis-mass tests should sweep
   above and below the proven sweet spot before declaring a value.
2. **The 4-axis library design is saturated.** Three independent
   probes (014 push cCRE up, 015 push chicken up, both fail) confirm
   that ~50K of (cCRE + iid + human + chicken) is at a local optimum.
   Future progress requires DIFFERENT components, not more of
   existing ones.
3. **The 008 mouse-10K result was real, not confounded.** 015 chicken-
   10K confirms it independent of species choice. The 008-vs-006
   contrast had cCRE confound, but the underlying signal (per-species
   cap at 5K) was correct.

## What to try next
**016: test hard-negative axis (dinuc-shuffled cCRE) as substitute for
human-gen.** Design: 35K cCRE + 5K iid + 5K chicken + 5K dinuc-shuffled
cCRE. Mirror of 014 (which dropped human-gen for more cCRE) but with
dinuc-shuffled cCRE replacing the freed human-gen 5K. This tests:
  - Does a hard-negative axis (preserves dinucleotide stats, breaks
    long-range structure) substitute for human-gen as a stabilizer?
  - Is "regulatory-grammar-broken DNA" a 5th orthogonal axis we
    haven't yet exploited?

The 005 mono-shuffled was a regression vs 004, but mono-shuffled is too
easy a negative — model can distinguish via single-nucleotide stats.
Dinuc-shuffled is harder: matches CpG, dinuc TF motif counts, GC%
distribution, but breaks longer regulatory motifs.

Pre-registered predictions:
- 016 ≈ 010 (within ±0.005): dinuc substitutes for human-gen as
  stabilizer + adds hard-negative value. NEW AXIS, push further next.
- 016 between 010 and 014 (loss 0.005-0.030): dinuc adds something
  but doesn't fully substitute. Useful supplement at smaller mass.
- 016 ≈ 014 (loss ~0.038): dinuc adds nothing beyond just dropping
  human-gen. Mono-shuffled lesson generalizes.
- 016 < 014 (loss > 0.04): dinuc actively confuses. Hard negatives
  derived from cCRE create bad gradient signal.

This is the most efficient way to test whether HARD NEGATIVES are a
useful 5th axis in the saturated 4-axis library. Easy to generate
(no new genome), small data range (50K total), tightly comparable to
both 010 and 014.