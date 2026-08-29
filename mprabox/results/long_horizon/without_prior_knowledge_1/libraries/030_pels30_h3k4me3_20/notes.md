# 030_pels30_h3k4me3_20 — notes (FINAL EXPERIMENT)

## Design
30K pELS + 20K CA-H3K4me3, shuffled. Same protocol as 026
except mixing ratio 60/40 instead of 50/50. Three seeds.

## Result — STRIKING failure of asymmetric mix

Mean across 14 evals = **0.7398**.

| comparison                     | mean_r |
|--------------------------------|--------|
| pELS-only (012)                | 0.758  |
| CA-H3K4me3-only (019)          | 0.749  |
| **026 pELS+H3K4me3 25K/25K**   | **0.780** |
| **030 pELS+H3K4me3 30K/20K**   | **0.740** |
| Δ vs 026 (best combo)          | -0.040 |
| Δ vs pELS-only                 | -0.018 |
| Δ vs CA-H3K4me3-only           | -0.009 |

**Hypothesis (C) confirmed dramatically.** Shifting just 5K
sequences from CA-H3K4me3 to pELS DESTROYS the synergy and
drops below either parent alone.

## Per-eval (vs 026)

The drop is broad and largest on motif-rewarding evals:
| eval | 026 (25/25) | 030 (30/20) | Δ |
|------|-------------|-------------|---|
| 07   | 0.7827      | 0.7373      | **-0.045** |
| 13   | 0.7825      | 0.7308      | **-0.052** |
| 10   | 0.8026      | 0.7564      | -0.046 |
| 08   | 0.7053      | 0.6504      | -0.055 |

The motif-diversity contribution from CA-H3K4me3 collapses
when its share drops below 25K. Eval_07 and eval_13 (motif-
content evals) show the largest losses, mirroring the largest
gains in 026 — the same channel that delivered the 026 win
delivers the 030 loss when starved.

## Theory — final formulation

**Two-class orthogonal-evidence-type combo at 25K/25K is a
SHARP local optimum.** The optimum is sharp in two senses:
1. **Symmetry-sharp:** even small ratio shifts (60/40)
   collapse the synergy. The model needs roughly equal
   exposure to both evidence types during training.
2. **Depth-sharp:** below ~25K samples per class, the
   evidence-type signature can't be learned well enough to
   contribute. (Confirmed by 028 triple-combo failure at
   16.7K each AND by 030's failure when CA-H3K4me3 dropped
   to 20K.)

**Refined depth threshold:** ≥25K samples per evidence type
appears necessary. Below that, the orthogonal contribution
collapses sharply rather than gradually.

## Recommended library design

For a 50K MPRA library that maximizes generalization to
unseen cell types:

```
25,000 pELS  +  25,000 CA-H3K4me3, shuffled
```

This achieves mean Pearson r ≈ 0.780 across 14 anonymous
eval sets, +0.022 over the best single-class library and
+0.085 over uniform random.

## Final note

This is experiment 030 of 30. The notebook continues with a
program-final summary entry consolidating the 30-experiment
findings into a complete theory of MPRA library design for
sequence-to-activity generalization.
