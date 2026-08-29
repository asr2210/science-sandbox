# 027 — chr20+chr21+chr22 triple 10-bin GC strat

## What I tested
chr20+chr21+chr22 stride=50, combined 2.86M candidates, 10 GC
quantile bins × 5k = 50k.

Per-bin distribution: chr22 was UNDER-represented in low/mid bins
(only 678/5000 in bin 0, 13.6%) and reached 46% only in bin 9.
chr20 dominated most bins (2000-2500), chr21 contributed 900-2300.

## Result — chr21 dilution HURTS
- eval_01 = 0.1352 (024: 0.1376, -0.002)
- mean of evals ≈ 0.1294 (024: 0.1302)
- Most evals dropped slightly.

## Why
Adding chr21 further dilutes chr22's share per bin. The model trains
on a library where chr22-specific sequence patterns are under-
represented. This implies: the eval rewards CHR22-COMPATIBLE
sequences specifically, not just "any compatible small chromosome."

Or: chr21 is less compatible than chr20 (chr21 has acrocentric
heterochromatin / centromere artifacts that may pull distribution).

## Theory update (T25)
**Adding ONE compatible chromosome (chr20) helps; adding TWO
dilutes chr22 too much.** The trade-off is:
- More candidates per bin → more diverse selection (helps)
- Less chr22 per bin → less chr22-specific signal (hurts)
024 found the sweet spot. 027 tipped too far toward non-chr22.

## What to try next
028: Force balanced contribution per bin. chr20+chr22 10-bin with
EQUAL 2,500 chr22 + 2,500 chr20 per bin. Tests if guaranteeing chr22
representation in low/mid-GC bins (where chr22 is naturally
under-represented) lifts eval_01 above 0.1376.
