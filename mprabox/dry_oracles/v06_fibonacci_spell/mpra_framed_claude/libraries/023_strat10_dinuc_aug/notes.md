# 023 — 10-bin GC strat × 2.5k unique chr22 + dinuc-shuffle aug

## What I tested
Combined 013's 10-bin granularity with 018's 2× dinuc-shuffle aug.
10 GC bins × 2,500 unique chr22 windows × 2 versions (real + dinuc-
shuffled). 50k total. Random orientation. Seed=42.

## Result — combined design HURTS
- eval_01 = **0.1332** (013: 0.1375, -0.004; 018: 0.1367, -0.0035)
- mean of evals = 0.1278
- K562: 0.033, HepG2: 0.170, SK-N-SH: 0.197

The combination is WORSE than either component alone.

## Why it hurts
The augmentation halves the number of UNIQUE natural chr22 windows
per bin (5k → 2.5k). Dinuc-shuffled variants don't provide
equivalent information to natural windows. So the lost diversity
(natural) outweighs the gained diversity (shuffled).

## Theory update (T22)
**UNIQUE NATURAL CHR22 WINDOWS per bin is the key resource.**
Augmentation is not a substitute. The model values the natural
higher-order structure (even if it can't directly learn motifs,
some local k-mer patterns matter) more than dinuc-equivalent
noise.

This implies: to beat 0.1375, I need MORE natural chr22-like
windows per bin without sacrificing chr22-specificity.

## What to try next
024: Download chr20 (~64Mb, similar GC to chr22, less gene-dense
than chr19). Combine chr20+chr22 stratified 10 bins × 5k each
(now from ~2x candidate pool). Tests if chr20 windows are
chr22-compatible enough to add net value (unlike chr19 which hurt).
