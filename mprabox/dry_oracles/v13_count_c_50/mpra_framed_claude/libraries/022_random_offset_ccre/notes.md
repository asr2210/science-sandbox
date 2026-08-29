# 022 — Random-offset cCRE windowing (anchor breadth swing)

**Hypothesis:** 20k unique cCREs × 1 random-offset window each may
beat 4k unique × 5 fixed-offset windows by providing more anchor
breadth at same library budget.

**Design:** 22.5k genomic + 20k cCRE (20k unique × 1 random offset
in [-200,+200]) + 5k CpGi 5-window + 1.25k uniform + 1.25k shuffled.

**Results vs exp 020 (4k × 5 fixed):**
- eval_01:    0.5778 (-0.001)
- eval_04/09: 0.5657 (-0.001)
- eval_07:    0.6159 (-0.001)
- eval_08:    0.1766 (+0.002)
- eval_13:    0.5955 (-0.001)
- eval_10:    0.5142 (+0.000)
- Mean:       **0.5462** (-0.0006, within noise)

**Findings:**

Random-offset with 5x anchor breadth ≈ fixed-offset with 5x per-anchor
windows. Statistically indistinguishable. Either windowing strategy
works. The lift comes from "positional diversity per anchor" — fixed
vs random doesn't matter.

**Plan exp 023:** Try a genuinely new source — TF ChIP-seq peaks
from ReMap CRM (Cis-Regulatory Modules). TF ChIP captures actual
TF binding events, not just chromatin accessibility — may add motif
density beyond cCRE.

Download: remap2022_crm_macs2_hg38_v1_0.bed.gz (~200MB).
