# 019 hybrid_union

**Design:** 10k each from 5 selection rationales (topic-cluster, TFBS-hub, multi-cell DHS, promoter cCRE, random cCRE), deduplicated.

**Result:** eval_01 = 0.0755. Same plateau.

**Interpretation:** Mixing 5 different cCRE-selection strategies gives no advantage over any single one. The signal saturates: cCRE substrate × 50k samples = ~0.075-0.077 eval_01 regardless of selection method.

**Notable:** K562=0.0800, HepG2=0.0808 (highest in family), but SKNSH=0.0657 drags mean down. SKNSH is consistently the hardest cell type.

**Lesson:** Combination doesn't break the ceiling. The 50k budget × small-CNN model has a hard cap around 0.077 on eval_01 for any cCRE-based library.
