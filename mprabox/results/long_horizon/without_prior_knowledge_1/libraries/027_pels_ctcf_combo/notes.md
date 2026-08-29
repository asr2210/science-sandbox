# 027_pels_ctcf_combo — notes

## Design
25K pELS + 25K CA-CTCF, shuffled. Same protocol as 026, only
partner class swapped. Tests whether the +0.022 synergy
generalizes to other orthogonal partners.

## Result

Mean across 14 evals = **0.7631**.

| comparison        | mean_r |
|-------------------|--------|
| pELS-only (012)   | 0.758  |
| CA-CTCF-only (018)| 0.710  |
| **027 combo**     | **0.763** |
| best parent       | 0.758  |
| Δ vs pELS-only    | +0.005 |
| Δ vs 026 combo    | -0.017 |

**Synergy is real but small.** Hypothesis (B) confirmed:
orthogonality contributes, but partner strength matters.

## Per-eval comparison (delta vs pELS-only, 012)

| eval | 012     | 026 (H3K4me3) | 027 (CTCF) | Δ026   | Δ027   |
|------|---------|---------------|------------|--------|--------|
| 01   | 0.7203  | 0.7375        | 0.7205     | +0.017 | +0.000 |
| 02   | 0.8129  | 0.8340        | 0.8138     | +0.021 | +0.001 |
| 03   | 0.7958  | 0.8203        | 0.8025     | +0.025 | +0.007 |
| 04   | 0.7603  | 0.7755        | 0.7519     | +0.015 | -0.008 |
| 05   | 0.7203  | 0.7375        | 0.7203     | +0.017 | +0.000 |
| 06   | 0.8133  | 0.8343        | 0.8142     | +0.021 | +0.001 |
| 07   | 0.7489  | 0.7827        | 0.7770     | +0.034 | **+0.028** |
| 08   | 0.6844  | 0.7053        | 0.6898     | +0.021 | +0.005 |
| 09   | 0.8238  | 0.8403        | 0.8166     | +0.017 | -0.007 |
| 10   | 0.7729  | 0.8026        | 0.7879     | +0.030 | +0.015 |
| 11   | 0.7083  | 0.7249        | 0.7082     | +0.017 | -0.000 |
| 12   | 0.6853  | 0.7047        | 0.6899     | +0.019 | +0.005 |
| 13   | 0.7473  | 0.7825        | 0.7765     | +0.035 | **+0.029** |
| 14   | 0.8129  | 0.8340        | 0.8139     | +0.021 | +0.001 |

**Striking pattern: 027 wins big on the SAME two evals as 026
(eval_07 and eval_13)** — the "motif content matters most"
evals (per exp 003 dinuc shuffle analysis).

## Theory refinement

**Two synergy components:**
1. **Motif diversity** — adding ANY orthogonal evidence type
   helps motif-rewarding evals (eval_07, 13). CA-CTCF
   delivers this even though it's a weak class on its own.
2. **Broad coverage** — strong partners (high mean alone) also
   improve other evals. CA-H3K4me3 is strong (0.749), so it
   contributes broadly. CA-CTCF is weaker (0.710), so its
   contribution is concentrated on the motif evals.

**Predicted formula:** combo_mean ≈ pELS_baseline + α(motif_diversity) + β·partner_strength

For 026 (CA-H3K4me3): both α and β·strong contribute.
For 027 (CA-CTCF): α contributes; β·weak adds little or
slightly hurts on some evals (eval_04, 09, 11 went down).

## Implication for next experiments

Triple-combo with strong partners should stack motif-diversity
gains while keeping broad coverage. 16.7K each may be enough
samples per evidence type given that the gain in 026 came
from diversification, not depth.

## Next experiment

**Exp 028: triple combo pELS + CA-H3K4me3 + dELS (16.7K each).**
Tests whether stacking orthogonal evidence types compounds.

Wait — dELS antagonized pELS in 013 (-0.027). Better to use
known-orthogonal triple: pELS + CA-H3K4me3 + CA-CTCF.

**Revised: Exp 028 = pELS + CA-H3K4me3 + CA-CTCF triple
(16.7K each, shuffled).** All three are confirmed orthogonal
partners; CA-H3K4me3 contributes broadly, CA-CTCF contributes
motif diversity. If triple > 0.78 (best so far), diversity
stacking is real and we should keep adding orthogonal classes.
If triple ≤ 0.78, two orthogonal classes saturate the gain.
