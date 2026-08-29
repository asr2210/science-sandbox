# 029_h3k4me3_dels_combo — notes

## Design
25K CA-H3K4me3 + 25K dELS, shuffled. Same protocol as 026,
swap pELS → dELS. Tests whether two-class orthogonality rule
generalizes without pELS as anchor.

## Result

Mean across 14 evals = **0.7620**.

| comparison                       | mean_r |
|----------------------------------|--------|
| CA-H3K4me3-only (019)            | 0.749  |
| dELS-only (007)                  | 0.751  |
| **029 combo (this)**             | **0.762** |
| best parent                      | 0.751  |
| Δ vs best parent                 | +0.011 |
| Δ vs pELS-only baseline (012)    | +0.004 |
| Δ vs 026 (pELS+H3K4me3)          | -0.018 |

**Synergy is real (+0.011 over best parent), confirming the
orthogonality rule generalizes without pELS.** But synergy is
smaller than 026's +0.022 — pELS-anchored combos remain the
strongest.

## Synergy compendium

| combo (25K+25K)         | parent A | parent B | best parent | combo  | Δ over best parent |
|-------------------------|----------|----------|-------------|--------|---------------------|
| 013 pELS + dELS         | 0.758    | 0.751    | 0.758       | 0.731  | -0.027 (dilution)   |
| 026 pELS + CA-H3K4me3   | 0.758    | 0.749    | 0.758       | 0.780  | **+0.022**          |
| 027 pELS + CA-CTCF      | 0.758    | 0.710    | 0.758       | 0.763  | +0.005              |
| 029 CA-H3K4me3 + dELS   | 0.749    | 0.751    | 0.751       | 0.762  | +0.011              |

**Pattern:** All non-similar (orthogonal-evidence-type) combos
synergize. Same-evidence-type combos dilute. The magnitude
of synergy is variable — maximized for pELS+CA-H3K4me3.

## Theory — solidified

**Two-class orthogonal-evidence-type combo is the optimal
design pattern at 50K cap.** The orthogonality principle is
general (proven across three positive instances: 026, 027,
029). The depth principle is firm (028 triple at 16.7K
fails). The dilution principle is firm (013 same-type combo
fails).

**For maximum gain pick:**
1. The two strongest single classes by evidence type
2. Confirm they have ORTHOGONAL evidence types (not both
   "transcription-flanking enhancer" or both "chromatin
   accessibility")
3. Mix 25K each, shuffle

Best instantiation: pELS (transcription-flanking, near-
promoter) + CA-H3K4me3 (chromatin-mark, active-promoter
adjacent) → 0.780.

## Why pELS+CA-H3K4me3 wins

Both are "active regulatory elements near promoters" but their
EVIDENCE for being so is orthogonal:
- pELS: TF binding signature in transcription-flanking pattern
- CA-H3K4me3: chromatin accessibility + H3K4me3 (active-
  promoter histone mark)

So they share GENOMIC context (proximal regulatory regions)
but differ in detection mode. The model gets:
- Same activity-relevant local context (proximal regulatory
  motifs, GC content)
- Two complementary "perspectives" on what makes a sequence
  active

dELS instead is distal — different genomic context AND
different evidence type. Less context overlap = less synergy
boost beyond raw motif diversity.

## Next experiment (final)

**Exp 030: 30K pELS + 20K CA-H3K4me3.** Tests whether the
25K/25K ratio in 026 is optimal or whether biasing slightly
toward the stronger parent (pELS, 0.758 vs 0.749) further
helps. If 30K/20K > 0.780, ratio matters; we have a new best.
If ≈ 0.780, ratios within ±20% are equivalent. If < 0.780,
25/25 was at the optimum.

This is the LAST experiment of the 30-experiment program.
After 030, write final summary.
