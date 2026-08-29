# 028_triple_combo — notes

## Design
16,667 pELS + 16,667 CA-H3K4me3 + 16,666 CA-CTCF, shuffled.
Three confirmed orthogonal evidence types stacked into 50K.
Three seeds.

## Result — diversity stacking FAILS

Mean across 14 evals = **0.7431**.

| comparison                       | mean_r |
|----------------------------------|--------|
| pELS-only (012)                  | 0.758  |
| **026 pELS+H3K4me3 combo**       | **0.780** |
| 027 pELS+CTCF combo              | 0.763  |
| **028 triple combo (this)**      | **0.743** |
| Δ vs best two-way (026)          | -0.037 |
| Δ vs pELS-only                   | -0.015 |
| Δ vs worst two-way (027)         | -0.020 |

**Triple combo is WORSE than every two-way combo AND worse
than pELS-only.** Hypothesis (C) "per-class depth matters"
strongly confirmed.

## Per-eval pattern

eval_07 (motif-rewarding): 012=0.749, 026=0.783, 027=0.777,
028=0.752 — 028 only matches pELS baseline, no motif gain.
eval_13 (motif-rewarding): 012=0.747, 026=0.783, 027=0.777,
028=0.748 — same pattern.

Even on the evals that should benefit most from motif
diversity, the triple combo provides no advantage. Adding the
third class did NOT add motif diversity — it diluted the
existing signal.

## Theory update

**Two-class synergy is the optimum.** Beyond two evidence
types (at this 50K total cap), per-class depth drops below
the threshold needed for the model to learn each class's
regulatory grammar.

Refined model:
- 1 class @ 50K → ceiling ~0.758 (depth saturated)
- 2 classes @ 25K each → diversification win up to +0.022
- 3 classes @ 16.7K each → depth too low; diversification
  fails

Implication: each evidence type needs ≥ ~25K samples to be
"learned" effectively. With only 16.7K, none of the three
gets adequate representation, and motif diversity gains
collapse.

This is a **hard depth-vs-diversity trade-off** at 50K cap.
The two-class formula is the local optimum for this design
space. Beating 026 requires either:
- Better partner class than CA-H3K4me3 (unlikely; only PLS,
  CA, TF, CA-TF remain, all weaker)
- Different mixing ratio (e.g., 30K pELS + 20K CA-H3K4me3)
- A non-class manipulation (e.g., 026 + 1% mutation noise)

## Next experiment

**Exp 029: CA-H3K4me3 + dELS combo (25K + 25K).** Tests
whether the two-class synergy generalizes beyond pELS as one
of the two anchors.

CA-H3K4me3 alone = 0.749 (active-promoter chromatin mark).
dELS alone = 0.751 (distal enhancer-like, transcription-
flanking). Different evidence types (chromatin mark vs
transcription-flanking) and different genomic locations
(near-promoter vs distal). Should synergize per the rule
established in 026, even without pELS.

If 029 ≥ 0.770: orthogonality rule is general; pELS isn't
required as an anchor. We have a robust principle.
If 029 ≈ 0.755-0.765: rule holds but weaker without pELS;
pELS may be marginally special.
If 029 ≤ 0.750: synergy is pELS-anchor-specific; orthogonality
isn't enough.
