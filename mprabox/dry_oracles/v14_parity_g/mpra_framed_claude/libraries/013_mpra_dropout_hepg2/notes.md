# 013 — Reduce HepG2 to 10k, redistribute (K562=20k, SKNSH=20k)

**Result:** mean_r = **0.0039** (best yet, up from 011's 0.0036). Per-cell:
- K562 avg = 0.0020 (slight drop from 011's 0.0024)
- HepG2 avg = **0.0021** (UP from 011's 0.0009 — 2.3× improvement!)
- SKNSH avg = 0.0076 (matches)

Per-eval highlights: eval_03 SKNSH = 0.0153, eval_12 = 0.0153, eval_13 HepG2 = 0.0074, eval_03 HepG2 = 0.0062.

**Key insight — HepG2 marginal sequences are actively dilutive.** Cutting HepG2 budget by 40% INCREASED HepG2 signal 2.3×. The 011 HepG2 threshold (|lfc|≥0.97) was including too many low-confidence sequences that confuse the model. New threshold |lfc|≥1.26 → cleaner HepG2 signal.

**Theory update:** quality > quantity at the per-cell level. For HepG2 (and likely all cells), an |lfc| threshold around 1.5+ is the cliff above which sequences contribute trustworthy signal.

**Next (014):** Push further. K562=25k, HepG2=5k (top, |lfc|>1.5+), SKNSH=20k. If HepG2 climbs further with strict cut, the per-cell quality cliff is real and we should find each cell's optimum.
