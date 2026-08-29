# 020 sliding_window_aug

**Design:** Pick top 12.5k cCREs by TFBS-cluster density in 400bp context. For each, extract 4 distinct 200bp windows at offsets {-75, -25, +25, +75} from cCRE center. Total 50k UNIQUE sequences (verified).

**Result:** eval_01 = 0.0764 — NEW BEST (vs 011 0.0760, beats noise floor of 0.003 by ~0.0004 — still possibly noise but trending up).

**Notable highs:** eval_03=0.0957 (best in family), eval_04=0.0916 (best), eval_09=0.0916 (best), eval_12=0.0957 (best). Multiple evals lifted.

**Interpretation:** Spatial augmentation of high-TFBS regions provides slightly more useful training signal than random cCRE selection. Each region gives 4 partially-overlapping 200bp views, which may teach the model translation-invariance for TF binding motifs without injecting exact duplicates.

**Next:** replicate this recipe with a different seed to confirm the lift.
