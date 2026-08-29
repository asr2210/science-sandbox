# 011 — Random + 3x10bp distributed cCRE fragments

**Design.** 50K random 200bp; each gets 3 fragments of 10bp from random cCREs at distinct positions (30bp total bio).

**Result.** eval_01 = **0.4177** (NEW best non-random). K562 = 0.589, HepG2 = 0.615, SK-N-SH = 0.048.

| | K562 | HepG2 | SK-N-SH | eval_01 |
|---|---|---|---|---|
| 001 random | 0.590 | 0.623 | 0.045 | 0.4192 |
| **011 3x10bp** | **0.589** | **0.615** | **0.048** | **0.4177** |
| 008 1x25bp | 0.582 | 0.610 | 0.060 | 0.4174 |
| 009 1x15bp | 0.585 | 0.612 | 0.054 | 0.4169 |
| 010 1x50bp | 0.577 | 0.602 | 0.054 | 0.4109 |

**Interpretation.** Distributing bio across multiple short fragments preserves K562/HepG2 better than concentrating, but gives a smaller SK-N-SH lift. The trade-off: distributed → recover ~0.011 K562/HepG2 vs concentrated, but lose ~0.012 SK-N-SH.

Net: 011 and 008 are essentially tied (Δ +0.0003).

**Theory v9 (still holds).** I can closely approach random's eval_01 but not exceed it via bio insertion. The K562/HepG2 ceiling for this model+eval combo appears tight. SK-N-SH lift seems capped near 0.08.

**Next.** Pivot to bolder experiments. Try PLS-only fragments (promoter-like elements have strongest MPRA signal) as a higher-information-density biology source.
