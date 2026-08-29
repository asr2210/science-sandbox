# Exp 017 — chr22 random tiles with CpG-island filter

50k 200bp windows from chr22, dropping windows that look like CpG
islands (GC>=55% AND CpG_obs/exp>=0.6). Only ~2.5% (1277/50k) dropped.

## Result

| metric  | chr22 random (009) | chr22 - CpG islands |
|---------|-------------------:|--------------------:|
| eval_01 | 0.3202             | 0.3095              |
| k562    | 0.1443             | 0.1439              |
| hepg2   | 0.1990             | 0.1980              |
| sknsh   | 0.6173             | 0.5867              |

K562/HepG2 unchanged. SKNSH dropped 0.031. Filter hurt mostly because
seed change shifted sampling and the 2.5% CpG islands actually were
SKNSH-friendly (sitting near 50% GC optimum).

Lesson: don't filter chr22 tiles. The natural distribution including
CpG islands is at the SKNSH sweet spot. Removing them removes the
GC-rich shoulder that SKNSH likes.

This is the third experiment that fails to beat chr22 random
(009→0.3202). Pivot strategy: stop trying to filter; instead try
AUGMENTATION that adds without removing.
