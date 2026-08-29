# 009 — Random + 15bp real-CRE fragment per sequence

**Design.** Same as 008 but 15bp fragment (vs 25bp).

**Result.** eval_01 = **0.4169**. K562 = 0.585, HepG2 = 0.612, SK-N-SH = 0.054.

| Frag size | K562 | HepG2 | SK-N-SH | eval_01 |
|---|---|---|---|---|
| 0 (001 random) | 0.590 | 0.623 | 0.045 | 0.4192 |
| 15bp (009) | 0.585 | 0.612 | 0.054 | 0.4169 |
| 25bp (008) | 0.582 | 0.610 | 0.060 | 0.4174 |

**Interpretation.** Smaller fragment → smaller K562/HepG2 cost but also smaller SK-N-SH lift. The trade-off seems roughly proportional to fragment length. 25bp gives slightly better net than 15bp.

**Next.** Try larger fragment (50bp) to see if SK-N-SH lift continues scaling and where K562/HepG2 hits its floor. The shape of this curve tells us whether the "sweet spot" is sub-25bp, 25bp, or beyond.
