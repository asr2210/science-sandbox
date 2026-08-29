# 024 — HepG2 expanded to 6k unique sites

Layout: SKNSH 22k, HepG2 6k unique (|lfc|≥2.83, top 6k), K562 22k.

**Result:** mean_r = 0.0043 (vs 015's 0.0045 — marginal drop).
- K562 = 0.0029 (UP from 015's 0.0024 — small surprise)
- HepG2 = 0.0027 (DOWN from 015's 0.0044 — diluted!)
- SKNSH = 0.0073 (UP from 015's 0.0066 even at 22k vs 25k!)

**Interpretation:** Expanding HepG2 to 6k less-strict pulls in regulatory grammar that's broadly useful (boosts K562 and SKNSH r) but DILUTES HepG2-specific signal (top 6k @ |lfc|≥2.83 includes noise that distracts HepG2 cell prediction).

**Pattern emerging:** HepG2 has a *signal cliff* at top ~3k strict (|lfc|≥3.76). Beyond that, sequences contribute broadly-relevant grammar but stop sharpening HepG2-specific prediction.

**Net:** SKNSH+K562 gains barely offset HepG2 loss. Wash vs 015.

**Next (025):** Same-strand HepG2 dups w/ K22 preserved. 018 had H6 (3 unique + 3 dups) with mean=0.0038 but K dropped to 19 below floor. Try H6 dup pattern with S→22 to preserve K=22 — should isolate the same-strand-dup gain (HepG2 r=0.0049 in 018) at full K floor. Compare to 015's HepG2 r=0.0044 and 022's HepG2-RC r=0.0029.
