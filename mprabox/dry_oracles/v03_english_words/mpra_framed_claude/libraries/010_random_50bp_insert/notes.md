# 010 — Random + 50bp real-CRE fragment

**Design.** As 008/009 but 50bp fragment.

**Result.** eval_01 = **0.4109**. K562 = 0.577, HepG2 = 0.602, SK-N-SH = 0.054.

| Frag size | K562 | HepG2 | SK-N-SH | eval_01 |
|---|---|---|---|---|
| 0 | 0.590 | 0.623 | 0.045 | 0.4192 |
| 15bp | 0.585 | 0.612 | 0.054 | 0.4169 |
| **25bp** | **0.582** | **0.610** | **0.060** | **0.4174** |
| 50bp | 0.577 | 0.602 | 0.054 | 0.4109 |

**Curve shape.** Non-monotonic — 25bp is the local peak. 50bp gives MORE composition disruption but LESS SK-N-SH lift (50bp window may bring in too much non-motif content, diluting the regulatory signal).

**Interpretation.** A 25bp window seems to capture one strong motif + flanking context most often. Going to 50bp adds non-informative bases that just disrupt composition.

**Next.** Try DISTRIBUTED biology — 3x10bp small fragments per sequence (30bp total, but spread across the sequence). This tests whether distributing biology is better than concentrating it, and whether multiple small motif-like inserts are stronger signal than one larger insert.
