# 011 — Per-cell-type stratified top-|log2FC| (16.7k each)

K562 top 16,667 + HepG2 top 16,667 + SK-N-SH top 16,666 by |log2FC| within each cell's BED. Excl chr7/13. Per-cell |lfc| thresholds: K562 ≥ 2.26, HepG2 ≥ 0.97, SK-N-SH ≥ 0.27.

**Result:** mean_r = **0.0036** (best yet, up from 010's 0.0023, 008's 0.0020).
- K562 avg r = **0.0024** (best K562 yet, up from 010's 0.0004)
- HepG2 avg r = 0.0009 (essentially flat)
- SK-N-SH avg r = 0.0075 (matches 010 — stable)

Per-eval highs: eval_03 SKNSH = 0.0159, eval_03 K562 = 0.0071, eval_13 HepG2 = **0.0097** (new HepG2 high). eval_13 mean = 0.0049.

**Interpretation:** Per-cell stratification cleanly recovered K562 signal that 010's global top-|lfc| sort had ceded to SK-N-SH. K562 needed strict |lfc| (>2.26) to learn, which it now has. SK-N-SH retained its strong signal even at lower budget.

HepG2 puzzle: HepG2 top 16.7k @ |lfc|>0.97 barely moves the needle. Hypothesis: HepG2 MPRA is noisier so needs higher quality bar (stricter threshold) OR more sequences to extract signal.

**Next (012):** Reallocate budget toward HepG2 — try K562=15k, HepG2=25k, SKNSH=10k. Tests whether HepG2 signal scales with sequence count.
