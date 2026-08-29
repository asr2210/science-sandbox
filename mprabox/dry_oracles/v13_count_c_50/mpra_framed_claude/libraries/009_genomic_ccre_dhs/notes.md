# 009 — 3-Way: Genomic + class-balanced cCRE + balanced DHS

**Hypothesis:** Per Cell 2025 paper, cCRE and DHS carry complementary
regulatory grammars. Mixing both in one library should beat either
alone. Predict mean lifts above 0.55.

**Design:** 25k random genomic + 12.5k class-balanced cCRE + 12.5k
component-balanced DHS. Seed 0.

**Results vs exp 007 (50/50 genomic + cCRE-class-balanced, mean=0.541):**
- eval_01: 0.5701 (-0.006)
- eval_04/09: 0.5243 (-0.023) ← reverted
- eval_07: 0.6333 (+0.007)
- eval_08: 0.0807 (-0.049) ← reverted
- eval_13: 0.6154 (+0.009)
- eval_10: 0.5173 (~0.000)
- Mean: **0.533** (-0.008 vs 007)

**Findings:** DHS does NOT provide complementary value when added
alongside class-balanced cCRE. Replacing half the cCRE with DHS:
- eval_07/13 gained marginally (DHS may add some grammar diversity)
- eval_04/09 lost the compositional diversity benefit (cCRE PLS/CTCF
  classes were what helped)
- eval_08 reverted (DHS-like sequences look more like raw genomic)

**Theory:** The Cell paper's finding about "complementary grammars"
between MPRA and DHS libraries may not generalize to cCRE+DHS. cCRE
is curated from DHS+chromatin marks, so DHS is largely a subset of
cCRE territory minus the curation. The class diversity of cCRE
captures more than the cell-type breadth of DHS.

**Decision:** Stop testing DHS as an alternative source. cCRE
class-balanced + random genomic is the right base. Move on to
genuinely different selection criteria.

**Plan for exp 010:** Replace some cCRE with **phastCons highly
conserved elements** (evolutionarily constrained). Different selection
mechanism (evolution, not chromatin marks) — may capture functional
elements cCRE misses.
