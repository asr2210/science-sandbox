# 007 — cCRE (30K) + iid (5K) + human (5K) + mouse (5K) + chicken (5K)

## Result — slight regression vs 006, within seed noise
| metric  | 007 | 006 | 004 | Δ vs 006 |
|---------|-----|-----|-----|----------|
| eval_01 | 0.7446 | **0.7468** | 0.7395 | −0.0022 |
| eval_02 | 0.8397 | **0.8418** | 0.8342 | −0.0021 |
| eval_03 | 0.8253 | **0.8262** | 0.8178 | −0.0009 |
| eval_04 | 0.8009 | **0.8045** | 0.7998 | −0.0036 |
| eval_05 | 0.7445 | **0.7469** | 0.7395 | −0.0024 |
| eval_06 | 0.8401 | **0.8420** | 0.8343 | −0.0019 |
| eval_07 | 0.7868 | **0.7871** | 0.7724 | −0.0003 |
| eval_08 | 0.7231 | **0.7277** | 0.7160 | −0.0046 |
| eval_09 | 0.8711 | **0.8753** | 0.8712 | −0.0042 |
| eval_10 | 0.8049 | **0.8072** | 0.7989 | −0.0023 |
| eval_11 | 0.7320 | **0.7341** | 0.7265 | −0.0021 |
| eval_12 | 0.7096 | **0.7112** | 0.7029 | −0.0016 |
| eval_13 | **0.7825** | 0.7793 | 0.7671 | +0.0032 |
| eval_14 | 0.8398 | **0.8418** | 0.8344 | −0.0020 |

Mean 14: **0.7889** vs 006=0.7908 (−0.0019), but +0.0064 vs 004 and +0.0140
vs 005. Wins eval_13 by +0.0032 (only positive). Wall: 1279 s.

## Per-seed eval_01
- seed 0: 0.7556
- seed 1: 0.7332
- seed 2: 0.7449

Spread = 0.0224. Comparable to 006's 0.0204 — the cross-species component
keeps stabilizing seed variance vs pre-006 experiments (~0.06).

## Pre-registered scorecard
- "007 > 006 by ≥ +0.003 → 4-species stack works": **falsified** (−0.0019).
- "0 ≤ 007 − 006 < +0.003 → marginal benefit OR cCRE-shrink cancels":
  borderline; result is at −0.0019 (just outside the predicted band on the
  negative side). Within seed-noise of "no benefit".
- "007 < 006 by < 0.003 → chicken slightly redundant OR cCRE shrink hurts":
  **confirmed** (−0.0019).
- "007 < 006 by ≥ 0.005 → chicken actively confuses or cCRE shrink is sharp":
  **falsified** (delta is much smaller).

## Confound analysis
Two changes vs 006: cCRE 35K → 30K AND added 5K chicken (replacing nothing —
just expanded total composition). Cannot fully attribute:
- −0.002 could be cCRE shrinkage being mildly harmful AND chicken adding
  a tiny offsetting benefit
- OR cCRE shrinkage being benign AND chicken being approximately neutral
- OR cCRE shrinkage being mildly beneficial (saturating axis) AND chicken
  being mildly harmful

The clean disentangling is exp 008: drop chicken, keep cCRE at 30K, double
mouse to 10K. If 008 ≥ 007, more mouse beats new species. If 008 ≥ 006, cCRE
30K is fine and mouse-scaling within species works.

## What I learned
1. **The cross-species axis saturates quickly after one non-human species.**
   Adding a second non-human species (chicken, ~310 Mya from human) at the
   cost of cCRE backbone is approximately neutral, possibly slightly
   negative.
2. **The amniote-vertebrate generalization test is approximately negative.**
   Chicken's regulatory architecture, while amniote, is too distant to
   contribute orthogonal calibration that mouse hasn't already covered.
   This narrows the working theory: the useful cross-species signal is
   probably mammalian-grade, not vertebrate-grade.
3. **The seed-spread tightening (~0.02 vs ~0.06 pre-006) is robust.** This
   may be a methodological win on its own — 3-seed averages are now
   ~3× more precise. Worth flagging in any future statistical claims.

## Theory update
> Cross-species axis: the gain from adding non-human genomic content
> appears to come predominantly from "mammalian regulatory grammar in a
> different evolutionary trajectory" — not from "any non-human DNA". Adding
> a more distant vertebrate (chicken) does not stack with mouse. The axis
> is real but narrow: probably one mammalian source captures most of it.
>
> Open: would a SECOND mammal (e.g., rat rn7 or dog canFam6) stack with
> mouse? The theory predicts yes — close mammals share grammar but their
> specific sequences are different. Or have we already saturated even within
> mammals?

## What to try next
**008: cCRE saturation control + mouse scaling.** 30K cCRE + 5K iid + 5K
human + 10K mouse. Same total mass and same cCRE backbone as 007. Replaces
5K chicken with 5K more mouse.
- 008 > 006 by ≥ 0: cCRE 30K is OK, scaling mouse within species works.
- 006 ≥ 008 > 007: cCRE 30K is mildly costly but recovered by mouse scaling.
  Implies the cross-species axis is per-species saturating (each species adds
  fixed value, then plateaus).
- 008 < 007: chicken actually helped (its sequences provided non-redundant
  signal that double-mouse can't match), AND cCRE shrinkage is the dominant
  loss. Surprising; would re-open chicken hypothesis.
