# 015 activity_contrast

**Design:** 25k positives (multi-cell DHS summits, 4-mer K-Means(50) topic-stratified) + 25k negatives (intergenic 200bp windows ≥10kb from any cCRE).

**Result:** eval_01 = 0.0723 (vs 014 0.0739, 011 0.0760). Worse.

**Interpretation:** Adding "true silent" negative anchors did NOT help. The model doesn't learn better from contrast. Likely because the negative 25k is effectively random-intergenic ACGT — same statistical regime as random_uniform (~0.065 floor). Half the library being floor-quality drags the score down.

**Lesson:** all signal seems to come from cCRE-like training sequences. Adding non-cCRE sequences dilutes. Bigger negative set != better.

**Next:** measure noise floor (exp 016) so I know whether the 0.001-0.003 deltas I'm chasing are real.
