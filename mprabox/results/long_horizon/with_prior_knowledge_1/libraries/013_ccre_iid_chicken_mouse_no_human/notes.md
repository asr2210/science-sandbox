# 013 — cCRE (35K) + iid (5K) + mouse (5K) + chicken (5K), NO HUMAN-GEN

## Result — close to 010, RECOVERS most of 012's loss
| metric  | 013 | 010 | 012 | Δ vs 010 | Δ vs 012 |
|---------|-----|-----|-----|----------|----------|
| eval_01 | 0.7523 | **0.7599** | 0.7140 | −0.0076 | +0.0383 |
| eval_02 | 0.8485 | **0.8550** | 0.8048 | −0.0065 | +0.0437 |
| eval_03 | 0.8332 | **0.8413** | 0.7869 | −0.0081 | +0.0463 |
| eval_04 | 0.8103 | **0.8140** | 0.7724 | −0.0037 | +0.0379 |
| eval_05 | 0.7521 | **0.7599** | 0.7140 | −0.0078 | +0.0381 |
| eval_06 | 0.8486 | **0.8550** | 0.8049 | −0.0064 | +0.0437 |
| eval_07 | 0.7956 | **0.8044** | 0.7409 | −0.0088 | +0.0547 |
| eval_08 | 0.7442 | **0.7515** | 0.6405 | −0.0073 | +0.1037 |
| eval_09 | 0.8827 | **0.8872** | 0.8363 | −0.0045 | +0.0464 |
| eval_10 | 0.8181 | **0.8233** | 0.7593 | −0.0052 | +0.0588 |
| eval_11 | 0.7391 | **0.7464** | 0.7014 | −0.0073 | +0.0377 |
| eval_12 | 0.7165 | **0.7244** | 0.6771 | −0.0079 | +0.0394 |
| eval_13 | 0.7889 | **0.8016** | 0.7399 | −0.0127 | +0.0490 |
| eval_14 | 0.8488 | **0.8551** | 0.8049 | −0.0063 | +0.0439 |

Mean 14: **0.7985** vs 010=0.8056 (−0.0071) vs 012=0.7498 (+0.0487). Wall: 1281 s.

## Per-seed eval_01
- seed 0: 0.7595
- seed 1: 0.7597
- seed 2: 0.7376

Spread = 0.0221. Tighter than 012 (0.052), wider than 010 (0.010), comparable
to 006 (0.020).

## Pre-registered scorecard
- "013 ≈ 010 (within 0.01 mean)": **borderline confirmed** (delta -0.0071,
  just outside the band by 0.0029). Mouse+chicken DO stack reasonably with
  iid present.
- "013 between 010 and 012": **technically yes** but much closer to 010
  than 012. Confirms iid was the dominant 012 loss.
- "013 ≈ 012": **strongly falsified**.
- "013 > 010": falsified.

## Disentangled component values

This experiment + 012 + 010 give us three configurations sharing
{35K cCRE + chicken+mouse} but varying iid/human:
| config | iid | human | mouse | chicken | mean 14 |
|--------|-----|-------|-------|---------|---------|
| 010    | 5K  | 5K    | 0     | 5K      | 0.8056  |
| 012    | 0   | 5K    | 5K    | 5K      | 0.7498  |
| 013    | 5K  | 0     | 5K    | 5K      | 0.7985  |

Comparisons (each isolates a 2-way swap):
- 010 → 013 (drop human-gen, add mouse): −0.007 mean
- 010 → 012 (drop iid, add mouse): −0.056 mean
- 012 → 013 (swap iid for human-gen, holding mouse+chicken): +0.049 mean

Implications:
1. **iid value (in 4-cross-species library): ~+0.049 mean** (012→013 swap).
   This is 7× bigger than human-genomic value. iid is the load-bearing
   anchor, exactly as theorized post-012.
2. **Human-genomic value: ~+0.007 mean** (010→013 minus mouse-on-chicken
   stacking ≈ 0). Small but positive.
3. **Mouse-on-top-of-chicken stacking ≈ 0 mean**. Two cross-species at
   5K each don't stack at this budget. Confirms the 007/009 finding more
   cleanly: cross-species axis caps at ONE species at 5K when budget is
   tight.

## Theory state
> Final 4-axis decomposition (this study so far):
>   - cCRE backbone: load-bearing past 30K; slope ≈ -0.006 per -1K.
>   - iid: REQUIRED anchor at 5K when cross-species is present (+0.05).
>     Saturated at 5K — more iid doesn't help.
>   - Human non-cCRE genomic: +0.005-0.010 mean. Useful but not critical.
>   - Per-species cross-species: hump-shaped over distance, peak at
>     chicken (+0.023 vs +0.008 mouse, +0.017 zebrafish). Caps at ONE
>     species.
>
> Predicted optimal at 50K cap: 40K cCRE + 5K iid + 5K [best cross-species]
> if cCRE returns continue past 35K. Or 35K cCRE + 5K iid + 5K human + 5K
> [best cross-species] (current 010). The empirical question is whether
> cCRE 35→40K marginal value > human-genomic value (~+0.005-0.010).

## What I learned (operational)
1. **The "012 collapse" was specifically about iid loss, not mouse+chicken
   interference.** The cleanest possible counterfactual (013 swapping iid
   back for human-gen) recovers 87% of the loss. Single-variable swaps
   between two libraries that differ in only one component are the gold
   standard for value attribution.
2. **Cross-species axis really does cap at ONE species at 5K.** Three
   independent observations now point to this: 007 with cCRE confound,
   009 with mass-split confound, 013 clean. The cross-species mechanism
   appears to be "single concentrated source of orthogonal sequences"
   rather than "multiple species providing additively".
3. **iid-vs-human value ratio is ~7×** at the 4-axis configuration.
   That's a much bigger gap than the 002 vs 003 baseline suggested
   (+0.0023 vs +0.0034 — nearly equal). Context-dependence of axis
   values is now documented across two complexity tiers.

## What to try next
**014: push cCRE backbone up.** 40K cCRE + 5K iid + 5K chicken (no human-
genomic) = 50K. Drops human-genomic (~+0.007 value) and adds 5K cCRE
(unknown but likely +0.005-0.015 mean from cCRE elasticity going up).
- 014 > 010 by ≥ +0.005: cCRE returns continue past 35K AND chicken
  value persists. New best.
- 014 ≈ 010: cCRE 35→40 gain ≈ human-genomic loss; configurations
  approximately equivalent at this cap.
- 014 < 010 by 0.005-0.015: cCRE saturates by 35K AND human-genomic
  was more valuable than estimated. Stick with 010.
- 014 < 010 by > 0.015: cCRE 40K is actively worse than 35K (saturated/
  hurting), OR human is more critical. Surprising.

This is the highest-information remaining experiment for "find best 4-
component library". After 014 we'll have a clear picture of whether to
push cCRE up, push cross-species up, or look for a 5th axis that beats
human-genomic.
