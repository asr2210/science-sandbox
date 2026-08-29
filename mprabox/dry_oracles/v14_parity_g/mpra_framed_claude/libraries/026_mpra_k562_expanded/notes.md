# 026 — K562 expansion to 25k (SKNSH 22k)

Layout: SKNSH 22k, HepG2 3k strict, K562 25k (|lfc|≥1.525 — slight loosening from 015's 1.69).

**Result:** mean_r = 0.0040 (vs 015's 0.0045 — modest drop).
- K562 = 0.0025 (FLAT from 015's 0.0024 — K562 expansion gave no K562 lift)
- HepG2 = 0.0026 (DROPPED from 0.0044)
- SKNSH = 0.0074 (UP from 0.0066 even at 22k!)

**Surprise:** SKNSH at 22k is BETTER than SKNSH at 25k (also seen in 024). The bottom 3k SKNSH entries (|lfc|≈0.006-0.10) are likely noise dragging SKNSH r down. SKNSH wants ~22k.

**Updated theory:**
- K562 has hard ~22k floor; expansion to 25k yields nothing.
- HepG2 wants exactly 3k strict; any change hurts.
- SKNSH wants ~22k (not 25k as I previously thought).

**Implication:** ~3k slots are free if we cut SKNSH to 22k. But filling them with K562/HepG2 expansion DOESN'T help (HepG2 expansion actively hurts HepG2).

**Next (027):** Use freed 3k slots for cross-cell-type diversity — try cCRE pELS (proximal enhancer-like, 232k available). Hypothesis: cross-cell promoter/enhancer grammar may help generalization to unseen cell types, particularly eval_08 (consistently negative across all our libraries).
