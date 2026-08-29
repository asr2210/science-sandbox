# 008 — Ratio Test: 30/70 Genomic:cCRE (Class-Balanced)

**Hypothesis:** More regulatory density beats more context. Predict
mean rises to ~0.55+.

**Design:** 15,000 random genomic + 35,000 class-balanced cCRE (7,000
per class). Seed 0.

**Results vs exp 007 (50/50 best, mean=0.541):**
- eval_01: 0.5722 (-0.004) ~ tied
- eval_04/09: 0.5697 (+0.022) ← lift on composition
- eval_07: 0.5991 (-0.027) ← drop on motif-grounded
- eval_08: 0.2121 (+0.083) ← lift on OOD axis
- eval_13: 0.5767 (-0.030) ← drop on motif-grounded
- eval_10: 0.5088 (-0.009)
- Mean: **0.542** (~tied with 007)

**Findings:**

The 50/50 ⟷ 30/70 shift is a clean tradeoff:
- MORE cCRE → composition (eval_04/09) and OOD (eval_08) improve
- LESS genomic → motif-grounded evals (eval_07/13) regress
- eval_01 and overall mean basically unchanged

So 50/50 is close to optimal for primary eval_01 and mean. The ratio
axis is exhausted near this point.

**Per-cell-type pattern:** K562 still benefits most from more cCRE.
HepG2 and SKNSH are saturating — they don't get the same lift as K562.
This is the cCRE K562-bias re-emerging at higher cCRE fractions.

**Theory v5 holds:** mixing genomic + regulatory is super-additive,
but the ratio sweet spot is near 50/50. Pushing to 30/70 trades evals
against each other without net gain.

**Strategic decision:** The "ratio" axis is exhausted. Pivot to NEW
axes:

1. **Different regulatory sources** beyond cCRE (e.g., conserved non-coding
   elements, validated promoter databases)
2. **GC-stratified sampling** to push eval_04/09 (composition axis)
3. **Targeted promoter enrichment** (since promoter regions are high-GC
   and may help compositional generalization)

**Plan for exp 009:** Replace 5k random genomic with 5k *high-GC*
sequences (CpG island regions from UCSC, or just genomic windows
filtered to GC>0.6). Tests whether explicit GC variety beats organic
genomic GC distribution.

Actually — first let me search the literature for evidence on what
data sources help MPRA model generalization most. There is a 2025
bioRxiv paper "Investigating Data Size, Sequence Diversity, and Model
Complexity in MPRA-based Sequence-to-Function Prediction" that may
have direct evidence.
