# Exp 018 — chr22 tiles + GATA1 + KLF1 (erythroid motifs)

50k 200bp chr22 windows + 1 GATA1 (AGATAA) + 1 KLF1 (CACACC) inserted
at random positions. Strand balanced. ~12bp displaced of 200bp (6%).

Goal: bump K562 (laggard at 0.144) via cell-specific TFs.

## Result

| metric  | chr22 random (009) | + GATA1 + KLF1 |
|---------|-------------------:|---------------:|
| eval_01 | 0.3202             | 0.3174         |
| k562    | 0.1443             | 0.1447         |
| hepg2   | 0.1990             | 0.1969         |
| sknsh   | 0.6173             | 0.6105         |

K562 essentially unchanged (+0.0004). HepG2 -0.002, SKNSH -0.007.

**Lesson**: K562 score is NOT driven by GATA1/KLF1 motifs. Earlier
result (exp 004 K562 +0.016 from cell-typed motifs) was likely driven
by the OTHER motifs (NFY/SP1) compensating for synthetic background.
In real DNA background, GATA/KLF don't help.

Implication: K562 score may be capped at ~0.14 for natural-DNA-like
libraries. Need either a completely different motif (NFE2/MARE?
TAL1/E-box?) or accept the cap.
