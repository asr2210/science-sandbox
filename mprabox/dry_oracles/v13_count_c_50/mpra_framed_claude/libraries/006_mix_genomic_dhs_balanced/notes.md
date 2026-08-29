# 006 — 50/50 Mix: Random Genomic + DHS Index (Component-Balanced)

**Hypothesis:** Theory v3 (d) — cell-type-balanced regulatory sampling
beats cCRE (which is K562-biased) on HepG2/SK-N-SH heads. Use
Meuleman 2020 DHS Index (3.6M peaks across 733 biosamples in 16
components), sample equally across components.

**Design:** 25,000 random genomic + 25,000 DHS-balanced (1,562 from
each of 16 components, centered on summit). Seed 0.

**Results vs exp 004 (50/50 cCRE mix, mean=0.531):**
- eval_01: 0.5477 (-0.021)
- eval_02/05: 0.5486 (-0.021)
- eval_03/12: 0.5538 (-0.015)
- eval_04/09: 0.4723 (-0.050) ← noteworthy drop
- eval_06/11: 0.5473 (-0.020)
- eval_07: 0.6370 (+0.007) ~equal
- eval_08: -0.0096 (-0.092)
- eval_10: 0.5040 (-0.014)
- eval_13: 0.6204 (+0.009) ~equal
- eval_14: 0.5477
- Mean: **0.507** (-0.024 vs 004)

**Per-cell-type drop is uniform:** K562 -0.02, HepG2 -0.02, SKNSH -0.03.
DHS-balanced is NOT a cell-type-targeted improvement over cCRE — it's
just a slightly worse library across the board.

**What this tells me — theory v3 (d) is too simplistic:**

The hypothesis that "cCRE bias toward K562" was the limiting factor on
HepG2/SK-N-SH was WRONG, at least at the DHS-balanced level. DHS
balanced across 16 cell-type components does not consistently improve
HepG2/SK-N-SH prediction.

**What I think is going on:**

1. **cCRE has structural diversity DHS lacks.** cCRE elements come in
   5 classes (PLS, pELS, dELS, CTCF-only, DNase-H3K4me3) with
   different compositional and motif properties — promoters are
   high-GC/CpG, CTCF sites have a specific motif, etc. DHS is mostly
   enhancer-like sequences (all DHS) with less compositional variety.
2. **cCRE is curated (DHS + H3K4me3 + H3K27ac + CTCF marks)**, so
   represents higher-confidence regulatory elements per peak.
   Component-balanced DHS includes many cell-type-specific peaks that
   may be quiet in any specific measurement context — diluting per-
   sequence signal.
3. **cCRE catalogs are NOT as K562-biased as I assumed.** They pool
   across all ENCODE cell types via the same DNase data DHS-Index
   uses. So the "cell-type balance" of cCRE may already be reasonable.

**Theory v4 (refined):**

Cell-type breadth in the *training source data* is overrated as a
direct lever. What matters more is:
- **Compositional diversity within the regulatory half** (PLS vs dELS
  vs CTCF — different sequence regimes)
- **Per-sequence signal density** (curated cCRE > raw DHS)

**Next experiment (007):** Test compositional diversity within cCRE.
Sample 5,000 from each of the 5 cCRE classes (= 25,000) plus 25,000
random genomic. Compare to exp 004's uniform cCRE.

Predictions:
- eval_04/09: 0.52 → 0.55 (more diversity → more GC/CpG variety)
- eval_01: 0.57 → 0.58–0.60
- eval_07/13: similar
- Mean: 0.53 → 0.54
