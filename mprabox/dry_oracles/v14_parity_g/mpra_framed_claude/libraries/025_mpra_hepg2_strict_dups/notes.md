# 025 — HepG2 strict + same-strand dup, K22 preserved

Layout: SKNSH 22k, HepG2 3k unique + 3k same-strand dup = 6 slots, K562 22k preserved.

**Result:** mean_r = 0.0036 (vs 015's 0.0045 — significant drop).
- K562 = 0.0014 (DROPPED from 015's 0.0024, despite preserving 22k unique sites)
- HepG2 = 0.0037 (DROPPED from 015's 0.0044)
- SKNSH = 0.0058 (DROPPED from 015's 0.0066, partly from 25k→22k)

**Surprise:** Same-strand HepG2 dups hurt K562 too, even though K562 budget was preserved at 22k. The duplicated HepG2 sequences create training-set bias that distracts from K562 prediction.

**Reinterprets 018:** 018 (K19/H6-dup/S25) had mean=0.0038, HepG2 r=0.0049. I previously attributed HepG2 gain to dups, but the K22-preserved version (this) shows dups don't actually help HepG2 (0.0037 < 0.0044) and hurt K562. So 018's HepG2 r=0.0049 must've come from interaction with K19/S25 specifically — not the dup mechanism.

**Lesson confirmed:** No augmentation (dups, RC, alt) helps for any cell. Strict unique sequences win every time.

**Next (026):** Try modest K562 expansion to K25, dropping SKNSH to 22. Tests if K562 has unused signal beyond top 22k (or if 22k is genuinely saturated).
