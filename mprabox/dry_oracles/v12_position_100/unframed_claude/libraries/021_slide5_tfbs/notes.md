# 021 slide5_tfbs

**Design:** 5 windows × 10k top-TFBS cCREs. Offsets {-80, -40, 0, 40, 80}.

**Result:** eval_01 = 0.0758 (vs 020's 0.0764). Within noise. More views per region (5) on fewer regions (10k) didn't beat 4 views × 12.5k.

**Lesson:** the 020 ratio (4 views × 12.5k regions) might be near-optimal. Try fewer views × more regions next (e.g., 2 × 25k).
