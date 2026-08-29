# 005 k562_dhs_centered

**Design:** 200bp windows centered on K562 DNase-seq peak summits (top by smoothed_peak_height), 5 ENCODE files combined, autosomes+chrX. 470k unique K562 summits available, top 50k by height kept.

**Result:** eval_01 = 0.0735. Same band as everything else.

**Interpretation:** matched cell-type accessibility doesn't move the needle. The "biological grounding wins" theory is wrong (or insufficient). All natural-DNA libraries cluster in 0.07-0.08.

Need to test a different axis: motif density, library diversity, or sequence activity range.
