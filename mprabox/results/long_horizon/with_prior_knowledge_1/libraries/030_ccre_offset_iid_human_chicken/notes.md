# 030 (FINAL) — random cCRE midpoint offset (±50bp positional augmentation)

## Result — positional augmentation HURTS significantly

| metric  | 030 | 010 | Δ vs 010 |
|---------|-----|-----|----------|
| eval_01 | 0.7238 | **0.7599** | −0.0361 |
| eval_02 | 0.8153 | **0.8550** | −0.0397 |
| eval_03 | 0.7969 | **0.8413** | −0.0444 |
| eval_04 | 0.7812 | **0.8140** | −0.0328 |
| eval_05 | 0.7236 | **0.7599** | −0.0363 |
| eval_06 | 0.8156 | **0.8550** | −0.0394 |
| eval_07 | 0.7543 | **0.8044** | −0.0501 |
| eval_08 | 0.6853 | **0.7515** | −0.0662 |
| eval_09 | 0.8466 | **0.8872** | −0.0406 |
| eval_10 | 0.7716 | **0.8233** | −0.0517 |
| eval_11 | 0.7109 | **0.7464** | −0.0355 |
| eval_12 | 0.6856 | **0.7244** | −0.0388 |
| eval_13 | 0.7477 | **0.8016** | −0.0539 |
| eval_14 | 0.8156 | **0.8551** | −0.0395 |

Mean 14: **0.7624** vs 010=0.8056 (Δ=**−0.0432**). Wall: 1263s.
Per-seed eval_01: seed_0=0.7586, seed_1=0.7107, seed_2=0.7021
(spread **0.057** — very high, comparable to 026/028/029).

## Pre-registered scorecard
- "030 > 010 by +0.005-0.015 (NEW BEST, positional augmentation
  helps)": **falsified** (Δ=−0.043, opposite direction).
- "030 ≈ 010 within ±0.005 (model is position-invariant)":
  **falsified** (Δ=−0.043, far outside band).
- "030 < 010 by 0.005-0.015 (offset disrupts midpoint anchor)":
  **direction confirmed, magnitude 3× the predicted ceiling**.

## Theory update (v14, FINAL) — model RELIES on cCRE midpoint anchoring

**Refined theory:**
> The model is NOT position-invariant for cCRE windows. Random
> ±50bp offset around the cCRE midpoint disrupts training because:
>   (i) cCRE midpoints are biologically meaningful — TSSs for PLS,
>       CTCF motifs near CTCF-only midpoints, etc. The model has
>       learned to expect motifs at specific within-window positions.
>   (ii) The MPRA evaluation likely uses centered windows for the
>       label-assignment step, so offset training data drifts away
>       from the eval distribution.
>   (iii) Even ±50bp (25% of WIN=200bp) is enough to push core
>        motifs out of their expected position range.

**Operational corollary:** the 010 strategy of "extract 200bp
exactly centered on cCRE midpoint" is the 15th verified joint
constraint. Positional augmentation is HARMFUL, not helpful.

## The full 010 design — 15 verified joint constraints

After 30 experiments, 010 sits at the joint optimum of:

1. **cCRE mass = 35K** (sharp peak; +5K=−0.038 from 014, −5K=−0.025 from 015)
2. **cCRE class balance = 7K each across 5 classes** (near-flat-bottom optimum from 019/020)
3. **cCRE class composition includes structural classes (CTCF/DNase)** (removing them = −0.073 from 018)
4. **cCRE midpoint centering, NO offset augmentation** (030, NEW)
5. **iid mass = 5K** (sharp peak; +2.5K=−0.056 from 024)
6. **iid composition = uniform 50% GC** (asymmetric peak; high-GC=−0.047 from 022)
7. **iid coherence = single composition, no mixing** (028, NEW)
8. **No hard negatives (dinuc-shuf, RC-cCRE, near-flank)** (016, 025, 027)
9. **4-component design at 5K each** (012 collapse without iid)
10. **Same-species human-gen for slot 4** (cross-species in slot 4 = −0.011 to −0.023, 013/026)
11. **Slot-4 sampling = random across non-cCRE, NOT deep-only** (U-shaped, 027/029)
12. **Cross-species count = 1 species in slot 5** (007/008/009 saturate at 1)
13. **Cross-species choice = chicken** (sharply special vs zebrafish/xenopus/mouse, 011/017)
14. **Cross-species per-species mass = 5K** (universal cap, 008/015)
15. **No RC-augmentation at training time** (025 confirms model is strand-aware)

## What I learned from the full 30-experiment loop

(See notebook.md final synthesis entry for the program-level summary.)

This experiment closes the loop. The model has a sharply-peaked
optimum at the 010 design across many independently-tested axes.
After 20 follow-up experiments probing every single design variable
(cCRE mass / class balance / class composition / midpoint centering;
iid mass / composition / coherence; cross-species choice / mass /
count; slot-4 species / sampling distance; alternative 4th
components RC/shuf/near-flank), no library has beaten 010.

The 010 design's strength comes from the CONCURRENT alignment of
~15 sub-axes at their individual optima — a remarkable coincidence
since 010 was chosen by direct comparison to 006 (mouse swap), not
by gradient ascent over each axis.

## Final library: 010
**libraries/010_ccre_iid_human_chicken/**
- 35K cCRE 7K-each across PLS/pELS/dELS/CTCF-only/DNase-H3K4me3
  (200bp centered)
- 5K uniform iid (50% GC)
- 5K human genomic (≥200bp from any cCRE, random sampling)
- 5K chicken genomic (galGal6, all named chromosomes)
- Total: 50,000 sequences
- Mean 14-eval: **0.8056**
- eval_01: **0.7599**
- Per-seed eval_01 spread: 0.012 (lowest variance of any tested
  library — robust, reproducible).
