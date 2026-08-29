# 004 tfbs_centered_windows

**Design:** 200bp windows centered on ENCODE TFBS cluster midpoints from chr17/19/22 (1.2M intervals, sample 50k).

**Result:** eval_01 = 0.0764 (vs random genome 0.0752, +0.001). Mean ≈ 0.097.

**Surprising:** real regulatory regions barely beat random genome. This contradicts the naive "biological grounding wins" theory.

**Updated theory:** the model probably trains fine on TFBS sequences, but TFBS-centered windows from any chromosome look statistically similar to random genome (most of the genome contains some weak TF motifs). The signal at this score range is dominated by COMPOSITION + MOTIF DENSITY, not by mere regulatory annotation. Need either:
1. Cell-type-specific accessibility (DHS for K562/HepG2/SK-N-SH directly)
2. Much higher motif density per sequence
3. Sequence diversity stratified across regulatory categories (LDA "topics")

Next plan: try cell-type-specific DHS peaks (matches eval cell types).
