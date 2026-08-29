# 008 — saturated universal motifs (50/50)

## Method
25k active: GC=50% + 14 motifs each (universal panel: AP-1, SP1, NF-Y,
CREB, ETS, MYC E-box, GATA, KLF, NR half, NEUROD, homeobox). 25k null:
GC=50% no motifs.

## Results (eval_01)
mean_r=+0.0037, K562=+0.0046, HepG2=-0.0004, SKNSH=+0.0069

## Lessons
- Saturation didn't dramatically beat exp 005 or 007. The motif-density
  ramp has diminishing returns.
- HepG2 went slightly negative again (GC=50% null is "too GC" for it).
- eval_13 lit up especially: K562=+0.0127, mean=+0.0065.
- Bottom-line: synthetic motif stuffing tops out around mean_r=+0.004 to +0.007.

## Pivot
The signal ceiling for "random background + dense motif insertion"
seems to be in the +0.003 to +0.007 range. To break this, I should
try:
1. REAL human regulatory sequences (DHS peaks, ENCODE candidate
   cis-regulatory elements, FANTOM CAGE peaks) — these contain the
   full natural context that models were trained on.
2. Published MPRA datasets with measured activity.

Internet is available. Going to grab real cCRE (candidate cis-regulatory
element) sequences from ENCODE next.
