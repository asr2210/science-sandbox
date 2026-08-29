# 010 — cCRE (35K) + iid (5K) + human (5K) + chicken (5K)

## Result — NEW BEST on every eval, biggest jump in this study
| metric  | 010 | 006 | Δ vs 006 |
|---------|-----|-----|----------|
| eval_01 | **0.7599** | 0.7468 | +0.0131 |
| eval_02 | **0.8550** | 0.8418 | +0.0132 |
| eval_03 | **0.8413** | 0.8262 | +0.0151 |
| eval_04 | **0.8140** | 0.8045 | +0.0095 |
| eval_05 | **0.7599** | 0.7469 | +0.0130 |
| eval_06 | **0.8550** | 0.8420 | +0.0130 |
| eval_07 | **0.8044** | 0.7871 | +0.0173 |
| eval_08 | **0.7515** | 0.7277 | +0.0238 |
| eval_09 | **0.8872** | 0.8753 | +0.0119 |
| eval_10 | **0.8233** | 0.8072 | +0.0161 |
| eval_11 | **0.7464** | 0.7341 | +0.0123 |
| eval_12 | **0.7244** | 0.7112 | +0.0132 |
| eval_13 | **0.8016** | 0.7793 | +0.0223 |
| eval_14 | **0.8551** | 0.8418 | +0.0133 |

Mean 14: **0.8056** vs 006=0.7908. **+0.0148 mean**. Wins every eval. Wall:
1311 s.

## Per-seed eval_01 — tightest spread observed in this study
- seed 0: 0.7645
- seed 1: 0.7603
- seed 2: 0.7549

Spread = **0.0096**. About half of 006's spread (0.0204), and ~7× tighter
than the pre-006 norm (~0.06). Chicken substantially stabilizes seed
variance.

## Pre-registered scorecard
- "010 ≈ 006 (interchangeable at 5K)": **falsified**.
- "010 < 006 by 0.005–0.015 (mammalian proximity matters; mouse > chicken)":
  **falsified strongly — wrong direction**.
- "010 > 006 by ≥ +0.005 (distance > similarity)": **confirmed strongly**.
- "010 < 006 by > 0.015 (chicken needs mouse synergy)": **falsified**.

## Theory update — evolutionary-distance gradient

The previous theory predicted the cross-species axis is "mammalian-grade"
(chicken too distant, mouse just-right). The data now flips this:

| species at 5K | divergence | mean 14 lift over 4-axis baseline (004) |
|---------------|------------|------------------------------------------|
| none (004 baseline) | — | 0      |
| 5K mouse (006)      | ~80 Mya | +0.0083 |
| 5K chicken (010)    | ~310 Mya | **+0.0231** |

Chicken contributes ≈ 2.8× more cross-species value per K than mouse, at
the same per-species mass. The "more distant → more orthogonal calibration"
theory is correct, at least within the vertebrate range.

Probable mechanism: chicken sequences are mammalian-distant enough that
their non-cCRE genomic distribution differs more from human than mouse
does. The model gets a calibration source that probes a more distinct
slice of the "what could a 200bp DNA window look like" distribution. Mouse
non-cCRE is much more redundant with human non-cCRE because their genomes
are ~85% syntenic.

## Refined working theory
> Library value = (i) cCRE backbone (load-bearing past 30K) + (ii) off-genome
> iid (5K plateau) + (iii) in-genome human non-cCRE (5K plateau) +
> (iv) cross-species genomic, with VALUE GROWING with evolutionary distance.
> The optimum cross-species partner is "as distant as possible while still
> sharing the regulatory grammar that makes 200bp windows interpretable".
> Chicken > mouse. Untested: would zebrafish (~430 Mya, fish — past
> tetrapod-fish split) beat chicken? Would Drosophila (~600 Mya, lacks
> mammalian regulatory grammar) collapse?

## What I learned (operational)
1. **Pre-registration is doing real work.** The "mammalian-proximity matters"
   prediction was the most theoretically grounded one, and it was sharply
   falsified. Without pre-registering it, I might have rationalized the
   chicken win as "mouse helped + chicken adds different value" instead of
   confronting the simpler "chicken alone is just better".
2. **Stability gain compounds with chicken.** The seed-stabilization effect
   is monotonically tighter as cross-species distance grows (006 mouse:
   spread 0.020 → 010 chicken: spread 0.010). This is independent evidence
   for the orthogonality claim — distant species reduce per-seed variance
   more, presumably because they sample a larger novel slice of sequence
   space.
3. **Earlier interpretations of 007 were wrong twice.** First "chicken
   doesn't help" (007 alone). Then "chicken helps modestly via 008
   isolation" (estimated +0.024 eval_01). Now we know chicken alone at 5K
   is +0.0131 — close to but not identical to the 008-isolation estimate.
   The 008-isolation estimate was inflated because it conflated chicken's
   value with the cCRE shrinkage cost. Single-axis swap experiments like
   010 are more trustworthy than back-out estimates.

## What to try next
**Two strong candidates:**

A. **Push the distance gradient further: zebrafish (danRer11), ~430 Mya.**
   Same design as 010, swap chicken → zebrafish.
   - 011 > 010: gradient continues; "more distant is better" up to 430 Mya.
   - 011 ≈ 010: gradient saturates at chicken-distance.
   - 011 < 010: there's an optimal-distance sweet spot; past ~310 Mya the
     model loses too much regulatory grammar to extract value.

B. **Stack chicken + another distant species at fixed 50K cap.**
   E.g., 35K cCRE + 5K iid + 5K human + 5K chicken + ... need to find 5K
   somewhere. Could shrink iid to 0K (untested whether iid contributes at
   all post-005), or shrink human to 0K (untested whether human-genomic
   matters when chicken is present).

A is the cleaner first move — it tests the gradient theory end-to-end. B
needs at least one prerequisite ablation (iid removal test). Going with A
for 011.
