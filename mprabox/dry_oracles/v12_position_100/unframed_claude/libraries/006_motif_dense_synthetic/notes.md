# 006 motif_dense_synthetic

**Design:** 50k synthetic 200bp sequences. Each contains 6-10 copies of one primary TF motif (from a list of 20) plus 2-4 secondary motifs, all separated by random spacers.

**Result:** eval_01 = 0.0640. SLIGHTLY LOWER than random (0.0648).

**Surprising:** packing motifs hurts (or doesn't help). This rules out "motif density is the bottleneck."

**Updated theory:** the model is NOT simply learning motif → activity. Two possibilities remain:
- (H3 refined) Library diversity matters: stratified coverage of regulatory programs.
- (H4) Activity range matters: library needs sequences spanning low → high activity for model training.

Both could be addressed by a MIXED library: real DHS + random + motif-rich combined.
