# 017 tfbs_hub_ccres

**Design:** Take top 50k cCREs ranked by TFBS-cluster count overlapping their 200bp window (median=44 TFBSs per top window, vs typical cCRE ~5).

**Result:** eval_01 = 0.0756 (vs 011 0.0760, 014 0.0739). Within noise.

**Interpretation:** Information density per sequence (TFBS count) is NOT a useful lever. Sequences that overlap many TF clusters perform same as random cCRE samples.

**Lesson:** keep searching for non-cCRE substrates.
