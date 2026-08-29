# 026_pels_h3k4me3_combo — notes

## Design
25K pELS + 25K CA-H3K4me3 from each pool, no replacement,
shuffled. Central 200bp. Three seeds.

## Result — NEW BEST, BIG WIN

Mean across 14 evals = **0.7797**.

Previous best: 023 mut1pct = 0.761 (likely noise)
True best baseline: 012 pELS-only = 0.758
**Δ vs pELS-only: +0.022** (large, well beyond seed noise)

Per-eval comparison:

| eval | pELS012 | H3K4me3 019 | combo026 | Δ vs pELS | Δ vs better |
|------|---------|-------------|----------|-----------|-------------|
| 01   | 0.7203  | 0.7095      | 0.7375   | +0.017    | +0.017      |
| 02   | 0.8129  | 0.8009      | 0.8340   | +0.021    | +0.021      |
| 03   | 0.7958  | 0.7884      | 0.8203   | +0.025    | +0.025      |
| 04   | 0.7603  | 0.7496      | 0.7755   | +0.015    | +0.015      |
| 05   | 0.7203  | 0.7095      | 0.7375   | +0.017    | +0.017      |
| 06   | 0.8133  | 0.8012      | 0.8343   | +0.021    | +0.021      |
| 07   | 0.7489  | 0.7563      | 0.7827   | +0.034    | +0.026      |
| 08   | 0.6844  | 0.6512      | 0.7053   | +0.021    | +0.021      |
| 09   | 0.8238  | 0.8125      | 0.8403   | +0.017    | +0.017      |
| 10   | 0.7729  | 0.7721      | 0.8026   | +0.030    | +0.030      |
| 11   | 0.7083  | 0.6974      | 0.7249   | +0.017    | +0.017      |
| 12   | 0.6853  | 0.6772      | 0.7047   | +0.019    | +0.019      |
| 13   | 0.7473  | 0.7540      | 0.7825   | +0.035    | +0.029      |
| 14   | 0.8129  | 0.8009      | 0.8340   | +0.021    | +0.021      |

**Every single eval improves over BOTH parent classes alone.**
This is super-additive, not averaging.

## Interpretation — orthogonal evidence types synergize

This is the first genuinely large positive intervention. The
union of two classes that cover ORTHOGONAL evidence types
(pELS = transcription-flanking enhancer-like; CA-H3K4me3 =
chromatin-accessible + active-promoter mark) outperforms
either parent class.

**Crucial contrast: pELS + dELS HURTS (exp 013, mean=0.731).**
Both ELS classes are "enhancer-like"; combining them is
combining two samples of the SAME evidence space → dilution.
pELS + CA-H3K4me3 combines samples of DIFFERENT evidence
spaces → broader motif coverage → better generalization.

| combo                          | mean_r | Δ vs best parent |
|--------------------------------|--------|------------------|
| pELS + dELS (013)              | 0.731  | -0.027 (dilution) |
| **pELS + CA-H3K4me3 (026)**    | **0.780** | **+0.022 (synergy)** |

Same total N (50K), same shuffling protocol — only difference
is partner class. The partner class's evidence-type identity
determines synergy vs. dilution.

## Theory

**Generalization requires evidence-type diversity, not sample
volume.** A 50K sample drawn entirely from one evidence type
(pELS-only, dELS-only) hits a ceiling at ~0.75-0.76 because
every additional sequence teaches the model variants of the
same regulatory grammar. Mixing 25K from a complementary
evidence type teaches NEW grammar — the model has to learn to
predict activity for sequences with chromatin-mark-style
context (where TF binding signature differs from
transcription-flanking enhancers).

**Largest gains on motif-rewarding evals.** Eval_07 (+0.026
over best parent) and eval_13 (+0.029 over best parent) — the
"motif content matters most" evals (per exp 003 dinuc shuffle
analysis). The combo specifically improves motif-recognition
performance, consistent with broader motif coverage.

## Implication for next experiments

Strong signal. We have 4 experiments left to characterize the
synergy:
- **Generality check:** does pELS + CA-CTCF (different
  orthogonal class) also synergize? Or is CA-H3K4me3 special?
- **Saturation:** does adding a third orthogonal class help
  further, or saturate?
- **Class identity:** does pELS need to be one of the classes,
  or do any two orthogonal classes synergize?

## Next experiment

**Exp 027: pELS + CA-CTCF combo (25K + 25K).** CA-CTCF mean
alone = 0.710 (substantially weaker than CA-H3K4me3's 0.749),
but it's a different evidence type from pELS (chromatin
accessibility + CTCF-bound vs transcription-flanking enhancer).
Tests whether the synergy is general to "any orthogonal
evidence type" or specific to CA-H3K4me3.

If pELS + CA-CTCF ≥ 0.78, synergy is general — orthogonal
evidence type wins regardless of partner's solo strength.
If pELS + CA-CTCF ≈ pELS-only, the combo win is specific to
the CA-H3K4me3 class. Either result is highly informative.
