# 027 — MPRA core + cross-cell pELS

Layout: K22/H3/S22 + 3k random ENCODE pELS (proximal enhancer-like).

**Result:** mean_r = 0.0035 (down from 015's 0.0045 — significant drop).
- K562 = 0.0014 (down)
- HepG2 = 0.0030 (down)
- SKNSH = 0.0061 (slight down from 0.0066)
- eval_08 = -0.0038 (no improvement from 015's -0.0033)

**Interpretation:** Cross-cell cCRE pELS sequences are essentially noise from the model's per-cell prediction perspective. Adding 3k untargeted enhancers dilutes the signal across all three measured cells. pELS specifically did NOT help eval_08 either.

**Lesson confirmed:** Don't add cross-cell ENCODE cCRE. Stay pure MPRA.

**Next (028):** SKNSH from TSV with padj<0.05. BED SKNSH includes low-|lfc| (down to 0.006) which 024/026 suggest are noise. TSV padj<0.05 has 39,696 entries; top 25k @ |lfc|≥0.97 — much higher signal density than BED top 25k @ |lfc|≥0.006.
