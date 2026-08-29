# 007 — SKNSH-focused 50/50, matched GC=50%

## Method
25k active: GC=50% + 8 motifs from SKNSH/universal panel (E-box, CREB,
POU3F2, LHX2, SOX, MEF2, NFI, AP-1, SP1). 25k null: plain GC=50%.

## Results (eval_01)
mean_r=+0.0031, K562=+0.0027, HepG2=+0.0019, SKNSH=+0.0048
All three cell lines POSITIVE.

eval_07 stood out: HepG2=+0.0216 (highest yet!), K562=-0.0093, SKNSH=+0.0072.
eval_08: K562=+0.0109, HepG2=+0.0159 also notable.

## Comparison of three focused experiments
|              | mean_r | K562  | HepG2 | SKNSH |
|--------------|--------|-------|-------|-------|
| 005 K562     | 0.0043 | 0.0077| 0.0056|-0.0003|
| 006 HepG2    |-0.0030 |-0.0035| 0.0034|-0.0088|
| 007 SKNSH    | 0.0031 | 0.0027| 0.0019| 0.0048|

## Interpretation
- exp 005 wins eval_01 mean_r because K562 motifs are GC-rich, AP-1
  is in there, etc. — universal-ish.
- exp 007 is broadest (all three positive) because the panel included
  many universal motifs (AP-1, SP1, E-box).
- exp 006 hurt mean_r because AT-rich HepG2 panel disagrees with what
  K562/SKNSH models read as "active".

## Updated theory — variance maximization
For Pearson r, what matters is variance in the "true" model-relevant
quantity. Each 50/50 active-vs-null bumps r by ~ (slope * sd(motif_count))
/ noise. To maximize r I should:
1. Use motifs all 3 cell-line models recognize (universal panel).
2. Push active-half motif count as high as 200bp will hold (~12-15).
3. Keep null half motif-free.
4. Keep composition matched to avoid confounds.

## Next
Exp 008: SATURATED universal motif library. 25k with 12+ motifs each
(universal panel) + 25k null. GC matched.
