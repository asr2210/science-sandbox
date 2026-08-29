# 018 — K562 + SKNSH combo banks

## Method
12.5k K562-saturated (GC=65, 12 motifs) + 12.5k SKNSH motifs (GC=50, 8 motifs)
+ 25k null at GC=40. Goal: lift K562 and SKNSH simultaneously.

## Results (eval_01)
mean_r = -0.0004 (K562=+0.0052, HepG2=-0.0083, SKNSH=+0.0018)

## Lesson
- K562 lift held (+0.0052) but lower than exp 012's +0.0089.
- SKNSH only modestly positive (+0.0018).
- HepG2 DEEPLY negative (-0.0083). The null at GC=40 with no motifs may
  look like a typical HepG2-region BG, with the active bank's K562/SKNSH
  motifs being non-HepG2 → HepG2 model ranks inversely.
- eval_04 = +0.0045 was surprisingly strong (different from eval_01).

## Implication
- Splitting motif identity by cell dilutes per-cell K562 signal.
- HepG2 is fragile; needs HepG2-specific signal OR neutral content.

## Next (exp 019)
Try a CONTINUOUS GRADIENT design — 5 strength levels of motif density
across 10k each. Hypothesis: both predictors track motif count
monotonically; gradient should produce higher Pearson r than bimodal.
