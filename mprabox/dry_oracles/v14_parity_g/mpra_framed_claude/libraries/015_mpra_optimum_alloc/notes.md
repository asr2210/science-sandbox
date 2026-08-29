# 015 — K22 / H3 (ultra-strict) / S25 — best yet

Final allocation: SKNSH 25,184 (all available, |lfc|≥0) + HepG2 3,000 (|lfc|≥**3.76**, ultra-strict) + K562 21,816 (|lfc|≥1.69).

**Result:** mean_r = **0.0045** (new best, +15% over 013/014).
- K562 avg = 0.0024 (matches 013)
- HepG2 avg = **0.0044** (2× the 014 high of 0.0028, **5× the 011 level of 0.0009**)
- SK-N-SH avg = 0.0066 (slight drop, expected — added lower-|lfc| SKNSH)

**eval_13 mean = 0.0078** (BEST single-eval mean to date). K562=0.0087, HepG2=0.0092 on eval_13.

**Theory update:** Per-cell magnitude threshold is the dominant lever, and HepG2's threshold needs to be EXTREME (|lfc|≥3-4) for the cell's signal to surface. The K562 sweet spot is roughly 18-22k @ |lfc|≥2.

The picture is: trained on Tewhey lab MPRA data, the simulator only learns when given high-confidence per-cell signal. Marginal sequences are anti-features.

**Next (016):** Test SKNSH stringency. SKNSH has been ~0.0075 across many configs — never tested with strict |lfc| filter. Try SKNSH 15k @ |lfc|≥0.7 (stricter), keep HepG2 strict, fill rest with K562.
